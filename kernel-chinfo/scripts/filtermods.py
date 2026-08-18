#!/usr/bin/env python3
"""
filter kmods into groups for packaging, see filtermods.adoc

Algorithm overview
==================
Assigns each kernel module (kmod) to exactly one RPM sub-package while
respecting kmod dependency constraints: if kmod A depends on kmod B, then
B's package must be reachable from A's package (same package, or one that
A's package transitively depends on).

The solver uses constraint propagation (AC-3 arc consistency) followed by
greedy instantiation.  Each kmod keeps an allowed_list — a set of packages
it could still be placed in.  The algorithm narrows these sets until every
kmod has exactly one package.

Phases
------

                        ┌─────────────────────────────────────────────────────────────┐
                        │                      sort_kmods()                           │
                        └─────────────────────────────────────────────────────────────┘

  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
  │  1. init labels  │──▶│  2. propagate    │──▶│  3. resolve      │──▶│  4. resolve       │
  │                  │   │                  │   │     preferred    │   │     remaining    │
  └──────────────────┘   └──────────────────┘   └──────────────────┘   └──────────────────┘

  allowed_list per kmod — how it evolves through the phases:

  Phase 0 (setup):       {all packages}          — every kmod starts with full set
                              │
  Phase 1 (init labels):      ▼
      needs rule:        {exact_pkg}             — hard lock to one package
      wants rule:        {target ∪ ancestors}    — target package and those it depends on
      no rule:           {all packages}          — unchanged
                              │
  Phase 2 (propagate):        ▼
      worklist loop:     prune infeasible pkgs   — for each pkg in allowed_list, check
                         from allowed_list         that every kmod neighbor has at least
                              │                    one compatible pkg; if not, remove it
                              │                    re-queue neighbors when set shrinks
                              ▼
                         arc-consistent state    — fixed point, all remaining pkgs are
                              │                    locally compatible with every neighbor
  Phase 3 (resolve preferred):▼
      for each kmod      narrow to {preferred}   — if kmod has a wants rule and its
      with wants rule:   then propagate            preferred pkg is still allowed, pick it
                              │                    (or nearest ancestor); re-propagate
                              │
  Phase 4 (resolve remaining):▼
      reverse topo order narrow to {default}     — pick default pkg (or nearest ancestor);
      for remaining:     then propagate            reverse topo so parents settle first
                              │
                              ▼
                         {single package}        — every kmod assigned to exactly one pkg

Convergence: allowed_list sets only shrink (monotonic).  The potential
  sum(|allowed_list|) is bounded below by 0 and strictly decreases on every
  productive prune, so the worklist always drains.

Correctness: pruning only removes packages provably incompatible with at
  least one neighbor.  For tree-shaped package hierarchies (the common case),
  arc consistency guarantees that the greedy resolve phases cannot cause
  dead ends.
"""

import argparse
import os
import re
import subprocess
import sys
import yaml
import unittest
from collections import deque

from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET, FileHandler, StreamHandler, Formatter
from typing import Optional

log = getLogger('filtermods')


def get_td(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, 'filtermods-testdata', filename)


def run_command(cmd, cwddir=None):
    p = subprocess.Popen(cmd, cwd=cwddir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out_str = out.decode('utf-8')
    err_str = err.decode('utf-8')
    return p.returncode, out_str, err_str


def safe_run_command(cmd, cwddir=None):
    log.info('%s', cmd)
    retcode, out, err = run_command(cmd, cwddir)
    if retcode != 0:
        log.warning('Command failed: %s, ret_code: %d', cmd, retcode)
        log.warning(out)
        log.warning(err)
        raise Exception(err)
    log.info('  ^^[OK]')
    return retcode, out, err


def setup_logging(log_filename, stdout_log_level):
    log_format = '%(asctime)s %(levelname)7.7s %(funcName)20.20s:%(lineno)4s %(message)s'
    log = getLogger('filtermods')
    log.setLevel(DEBUG)

    handler = StreamHandler(sys.stdout)
    formatter = Formatter(log_format, '%H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(stdout_log_level)
    log.addHandler(handler)
    log.debug('stdout logging on')

    if log_filename:
        file_handler = FileHandler(log_filename, 'w')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(DEBUG)
        log.addHandler(file_handler)
        log.info('file logging on: %s', log_filename)

    return log


def strip_ko_suffix(name: str) -> str:
    for ext in ('.xz', '.zst', '.gz'):
        if name.endswith(ext):
            name = name[:-len(ext)]
            break
    return name


def canon_modname(kmod_pathname: str) -> str:
    return strip_ko_suffix(os.path.basename(kmod_pathname))


class HierarchyObject:
    def __init__(self):
        self.depends_on = set()


def get_topo_order(obj_list: list[HierarchyObject], func_get_linked_objs=lambda x: x.depends_on) -> list[HierarchyObject]:
    topo_order = []
    objs_to_sort = set(obj_list)
    objs_sorted = set()

    while len(objs_to_sort) > 0:
        no_deps = set()
        for obj in objs_to_sort:
            linked = func_get_linked_objs(obj)
            if not linked:
                no_deps.add(obj)
            else:
                all_deps_sorted = True
                for dep in linked:
                    if dep not in objs_sorted:
                        all_deps_sorted = False
                        break
                if all_deps_sorted:
                    no_deps.add(obj)

        if not no_deps:
            cycle_names = [str(obj) for obj in objs_to_sort]
            raise Exception('Dependency cycle detected among: %s' % ', '.join(cycle_names))

        for obj in no_deps:
            topo_order.append(obj)
            objs_sorted.add(obj)
            objs_to_sort.remove(obj)

    return topo_order


class KMod(HierarchyObject):
    def __init__(self, kmod_pathname: str) -> None:
        super(KMod, self).__init__()
        self.name: str = canon_modname(kmod_pathname)
        self.kmod_pathname: str = kmod_pathname
        self.is_dependency_for: set[KMod] = set()
        self.assigned_to_pkg: Optional[KModPackage] = None
        self.preferred_pkg: Optional[KModPackage] = None
        self.allowed_list: Optional[set[KModPackage]] = None
        self.err = 0

    def __str__(self):
        depends_on = ''
        for kmod in self.depends_on:
            depends_on = depends_on + ' ' + kmod.name
        return '%s {%s}' % (self.name, depends_on)


class KModList():
    def __init__(self) -> None:
        self.name_to_kmod_map: dict[str, KMod] = {}
        self.topo_order: Optional[list[KMod]] = None

    def get(self, kmod_pathname, create_if_missing=False):
        kmod_name = canon_modname(kmod_pathname)
        if kmod_name in self.name_to_kmod_map:
            return self.name_to_kmod_map[kmod_name]
        if not create_if_missing:
            return None

        kmod = KMod(kmod_pathname)
        # log.debug('Adding kmod %s (%s) to list', kmod.name, kmod.kmod_pathname)
        if kmod.kmod_pathname != kmod_pathname:
            raise Exception('Already have %s, but path changed? %s' % (kmod_name, kmod_pathname))
        if not kmod.name:
            raise Exception('Each kmod needs a name')
        self.name_to_kmod_map[kmod_name] = kmod
        return kmod

    def process_depmod_line(self, line):
        tmp = line.split(':')
        if len(tmp) != 2:
            raise Exception('Depmod line has unexpected format: %s' % line)
        kmod_pathname = tmp[0].strip()
        dependencies_pathnames = tmp[1].strip()
        kmod = self.get(kmod_pathname, create_if_missing=True)

        if dependencies_pathnames:
            for dep_pathname in dependencies_pathnames.split(' '):
                dep_kmod = self.get(dep_pathname, create_if_missing=True)
                kmod.depends_on.add(dep_kmod)
                dep_kmod.is_dependency_for.add(kmod)

    def load_depmod_file(self, filepath):
        with open(filepath) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                self.process_depmod_line(line)
        log.info('depmod %s loaded, number of kmods: %s', filepath, len(self.name_to_kmod_map))

    def dump(self):
        for kmod in self.name_to_kmod_map.values():
            print(kmod)

    def get_topo_order(self):
        if self.topo_order is None:
            self.topo_order = get_topo_order(self.name_to_kmod_map.values())
        # TODO: what if we add something after?
        return self.topo_order

    def get_alphabetical_order(self):
        kmods = list(self.name_to_kmod_map.values())
        kmods.sort(key=lambda k: k.kmod_pathname)
        return kmods

    def load_kmods_from_dir(self, topdir):
        ret = []
        for root, dirs, files in os.walk(topdir):
            for filename in files:
                if strip_ko_suffix(filename).endswith('.ko'):
                    kmod_pathname = os.path.join(root, filename)
                    ret.append(kmod_pathname)

        return ret

    def check_depmod_has_all_kmods(self, dirpath):
        ret = self.load_kmods_from_dir(dirpath)
        for kmod_pathname in ret:
            kmod = self.get(kmod_pathname)
            if not kmod:
                raise Exception('Could not find kmod %s in depmod' % kmod_pathname)
        log.debug('OK: all (%s) kmods from %s are known', len(ret), dirpath)


class KModPackage(HierarchyObject):
    def _get_depends_on(pkg):
        return pkg.depends_on

    def _get_deps_for(pkg):
        return pkg.is_dependency_for

    def __init__(self, name: str, depends_on=None) -> None:
        if depends_on is None:
            depends_on = []
        self.name: str = name
        self.depends_on: set[KModPackage] = set(depends_on)
        self.is_dependency_for: set[KModPackage] = set()

        for pkg in self.depends_on:
            pkg.is_dependency_for.add(self)
        self.all_depends_on_list: list[KModPackage] = self._get_all_linked(KModPackage._get_depends_on)
        self.all_depends_on: set[KModPackage] = set(self.all_depends_on_list)
        self.all_deps_for: Optional[set[KModPackage]] = None
        self.self_and_below: set[KModPackage] = set()
        self.self_and_above: set[KModPackage] = set()
        self.default = False
        log.debug('KModPackage created %s, depends_on: %s', name, [pkg.name for pkg in depends_on])

    def __repr__(self):
        return self.name

    def get_all_deps_for(self):
        if self.all_deps_for is None:
            self.all_deps_for = set(self._get_all_linked(KModPackage._get_deps_for))
        return self.all_deps_for

    def _get_all_linked(self, func_get_links):
        ret = []
        explore = func_get_links(self)

        while len(explore) > 0:
            new_explore = set()
            for pkg in explore:
                if pkg not in ret:
                    ret.append(pkg)
                    for dep in func_get_links(pkg):
                        new_explore.add(dep)
            explore = new_explore
        return ret


class KModPackageList(HierarchyObject):
    def __init__(self) -> None:
        self.name_to_obj: dict[str, KModPackage] = {}
        self.kmod_pkg_list: list[KModPackage] = []
        self.rules: list[tuple[str, str, str, bool]] = []

    def get(self, pkgname):
        if pkgname in self.name_to_obj:
            return self.name_to_obj[pkgname]
        return None

    def add_kmod_pkg(self, pkg):
        self.name_to_obj[pkg.name] = pkg
        self.kmod_pkg_list.append(pkg)

    def __iter__(self):
        return iter(self.kmod_pkg_list)


def get_kmods_matching_re(kmod_list: KModList, param_re: str) -> list[KMod]:
    ret = []
    # first subdir can be anything - this is because during build everything
    # goes to kernel, but subpackages can move it (e.g. to extra)
    param_re = '[^/]+/' + param_re
    pattern = re.compile(param_re)

    for kmod in kmod_list.get_topo_order():
        m = pattern.match(kmod.kmod_pathname)
        if m:
            ret.append(kmod)
    return ret


def walk_kmod_chain(kmod, myfunc):
    visited = set()

    def visit_kmod(kmod, parent_kmod, func_to_call):
        func_to_call(kmod, parent_kmod)
        visited.add(kmod)
        for dep in kmod.depends_on:
            if dep not in visited:
                visit_kmod(dep, kmod, func_to_call)

    visit_kmod(kmod, None, myfunc)
    return visited


def pick_best(allowed_set: set[KModPackage], target_pkg: KModPackage = None) -> Optional[KModPackage]:
    """Pick one package from allowed_set for a kmod to be assigned to.

    If target_pkg is given, try it first, then walk down its dependency
    chain and return the first match found in allowed_set.

    If there is no target or no match, pick the package that sits highest
    in the dependency tree (has the most dependencies below it).

    Example with: modules-extra -> modules-core
                  modules       -> modules-core

      pick_best({modules, modules-extra})           => modules-extra
          (tied on depth, breaks tie by name)
      pick_best({modules, modules-core})            => modules
          (modules sits higher, it depends on modules-core)
      pick_best({modules, modules-core}, modules)   => modules
          (target_pkg matches directly)
      pick_best({modules-core}, modules)            => modules-core
          (target_pkg not in set, but its dependency is)
    """
    if not allowed_set:
        return None
    if target_pkg:
        if target_pkg in allowed_set:
            return target_pkg
        for child in target_pkg.all_depends_on_list:
            if child in allowed_set:
                return child
    return max(allowed_set, key=lambda p: (len(p.all_depends_on), p.name))


def prune_allowed(kmod: KMod) -> bool:
    """Remove packages from kmod's allowed_list that are incompatible
    with its kmod neighbors (dependencies and dependents).

    For each package P in kmod's allowed_list, remove P if:
    - any kmod dependency has allowed_list & P.self_and_below == {}, or
    - any kmod dependent  has allowed_list & P.self_and_above == {}

    where:
      P.self_and_below = {P} | P.all_depends_on      (P and everything P depends on)
      P.self_and_above = {P} | P.get_all_deps_for()   (P and everything that depends on P)

    This ensures that if a kmod is placed in package P, its dependencies
    can go into P or a package below P, and its dependents can go into P
    or a package above P. Packages that violate this are eliminated.

    Returns True if any packages were removed, False otherwise.
    Sets kmod.err if the entire allowed_list becomes empty.
    """
    if kmod.err or not kmod.allowed_list:
        return False

    to_remove = set()
    for pkg in kmod.allowed_list:
        for kmod_dep in kmod.depends_on:
            if not kmod_dep.allowed_list or kmod_dep.err:
                continue
            if not (pkg.self_and_below & kmod_dep.allowed_list):
                to_remove.add(pkg)
                log.debug('%s: remove %s, child %s has %s',
                          kmod.name, pkg.name, kmod_dep.name, [x.name for x in kmod_dep.allowed_list])
                break

        if pkg in to_remove:
            continue

        for kmod_par in kmod.is_dependency_for:
            if not kmod_par.allowed_list or kmod_par.err:
                continue
            if not (pkg.self_and_above & kmod_par.allowed_list):
                to_remove.add(pkg)
                log.debug('%s: remove %s, parent %s has %s',
                          kmod.name, pkg.name, kmod_par.name, [x.name for x in kmod_par.allowed_list])
                break

    if not to_remove:
        return False

    kmod.allowed_list -= to_remove
    log.debug('%s: pruned to %s', kmod.name, [x.name for x in kmod.allowed_list])
    if not kmod.allowed_list:
        log.error('%s: cleared entire allow list', kmod.name)
        kmod.err = 1
    return True


def propagate(kmod_list: KModList, seed_kmods=None):
    """Run prune_allowed() across kmods until no more changes occur.

    When seed_kmods is None, starts with all kmods in topological order.
    When seed_kmods is given, starts with their immediate neighbors only.

    Each time prune_allowed() removes a package from a kmod's allowed_list,
    that kmod's neighbors are re-queued, since the change may make some of
    their packages incompatible too.
    """
    if seed_kmods is None:
        queue = deque(kmod_list.get_topo_order())
    else:
        queue = deque()
        for kmod in seed_kmods:
            for neighbor in kmod.depends_on | kmod.is_dependency_for:
                queue.append(neighbor)
    in_queue = set(queue)

    while queue:
        kmod = queue.popleft()
        in_queue.discard(kmod)
        if prune_allowed(kmod):
            for neighbor in kmod.depends_on | kmod.is_dependency_for:
                if neighbor not in in_queue:
                    queue.append(neighbor)
                    in_queue.add(neighbor)


def apply_initial_labels(pkg_list: KModPackageList, kmod_list: KModList, treat_default_as_wants=False):
    log.debug('')
    for cur_rule in ['needs', 'wants', 'default']:
        for package_name, rule_type, rule, ignore_deps in pkg_list.rules:
            pkg_obj = pkg_list.get(package_name)

            if not pkg_obj:
                log.error('no package with name %s', package_name)

            if cur_rule != rule_type:
                continue

            if rule_type == 'default' and treat_default_as_wants:
                rule_type = 'wants'

            if 'needs' == rule_type:
                kmod_matching = get_kmods_matching_re(kmod_list, rule)
                for kmod in kmod_matching:
                    if kmod.assigned_to_pkg and kmod.assigned_to_pkg != pkg_obj:
                        log.error('%s: can not be required by 2 pkgs %s %s', kmod.name, kmod.assigned_to_pkg, pkg_obj.name)
                    else:
                        kmod.assigned_to_pkg = pkg_obj
                        kmod.allowed_list = {pkg_obj}
                        log.debug('%s: needed by %s', kmod.name, [pkg_obj.name])
                        if ignore_deps:
                            for dep in kmod.depends_on:
                                dep.is_dependency_for.discard(kmod)
                            for parent in kmod.is_dependency_for:
                                parent.depends_on.discard(kmod)
                            kmod.depends_on.clear()
                            kmod.is_dependency_for.clear()
                            log.debug('%s: deps severed (ignore_deps)', kmod.name)

            elif 'wants' == rule_type:
                kmod_matching = get_kmods_matching_re(kmod_list, rule)
                for kmod in kmod_matching:
                    if not kmod.assigned_to_pkg and not kmod.preferred_pkg:
                        kmod.allowed_list = {pkg_obj} | pkg_obj.all_depends_on
                        kmod.preferred_pkg = pkg_obj
                        log.debug('%s: wanted by %s, allowed: %s', kmod.name, [pkg_obj.name], [p.name for p in kmod.allowed_list])
                    elif kmod.assigned_to_pkg:
                        log.debug('%s: ignoring wants by %s, assigned to %s', kmod.name, pkg_obj.name, kmod.assigned_to_pkg.name)
                    else:
                        log.debug('already have wants for %s %s, new rule: %s', kmod.name, kmod.preferred_pkg, rule)

            elif 'default' == rule_type:
                pkg_obj.default = True


def resolve_preferred(kmod_list: KModList):
    """Resolve kmods that have a preferred_pkg (set by 'wants' rules).

    For each kmod with multiple allowed packages and a preferred_pkg,
    use pick_best() to select the preferred package (or closest match)
    and narrow allowed_list to just that one. Then propagate the change
    to neighbors.
    """
    log.info('')
    for kmod in kmod_list.get_topo_order():
        if kmod.err or not kmod.allowed_list or len(kmod.allowed_list) <= 1:
            continue
        if not kmod.preferred_pkg:
            continue
        chosen = pick_best(kmod.allowed_list, kmod.preferred_pkg)
        if chosen:
            kmod.allowed_list = {chosen}
            log.debug('%s: resolved to preferred %s', kmod.name, chosen.name)
            propagate(kmod_list, [kmod])


def resolve_remaining(pkg_list: KModPackageList, kmod_list: KModList):
    """Final pass: resolve kmods that still have multiple allowed packages
    after resolve_preferred().

    Walks kmods in reverse topological order (dependents before dependencies),
    using pick_best() with the default package as target. Falls back to
    pick_best() without a target if the default package doesn't match.
    Each resolution is propagated to neighbors.
    """
    log.info('')
    default_pkg = None
    for pkg_obj in pkg_list:
        if pkg_obj.default:
            if default_pkg:
                log.warning('Already have default pkg: %s / %s', default_pkg.name, pkg_obj.name)
            else:
                default_pkg = pkg_obj

    for kmod in reversed(list(kmod_list.get_topo_order())):
        if kmod.err or not kmod.allowed_list or len(kmod.allowed_list) <= 1:
            continue
        chosen = None
        if default_pkg:
            chosen = pick_best(kmod.allowed_list, default_pkg)
        if not chosen:
            chosen = pick_best(kmod.allowed_list)
        if chosen:
            kmod.allowed_list = {chosen}
            log.debug('%s: resolved to %s', kmod.name, chosen.name)
            propagate(kmod_list, [kmod])


def load_config(config_pathname: str, kmod_list: KModList, variants=None):
    if variants is None:
        variants = []
    kmod_pkg_list = KModPackageList()

    with open(config_pathname, 'r') as file:
        yobj = yaml.safe_load(file)

    for pkg_dict in yobj['packages']:
        pkg_name = pkg_dict['name']
        depends_on = pkg_dict.get('depends-on', [])
        if_variant_in = pkg_dict.get('if_variant_in')

        if if_variant_in is not None:
            if not (set(variants) & set(if_variant_in)):
                log.debug('Skipping %s for variants %s', pkg_name, variants)
                continue

        pkg_dep_list = []
        for pkg_dep_name in depends_on:
            pkg_dep = kmod_pkg_list.get(pkg_dep_name)
            if pkg_dep is None:
                raise Exception('Package %s depends on unknown package %s' % (pkg_name, pkg_dep_name))
            pkg_dep_list.append(pkg_dep)

        pkg_obj = kmod_pkg_list.get(pkg_name)
        if not pkg_obj:
            pkg_obj = KModPackage(pkg_name, pkg_dep_list)
            kmod_pkg_list.add_kmod_pkg(pkg_obj)
        else:
            log.error('package %s already exists?', pkg_name)

    rules_list = yobj.get('rules', [])
    for rule_dict in rules_list:
        if_variant_in = rule_dict.get('if_variant_in')
        exact_pkg = rule_dict.get('exact_pkg')
        ignore_deps = rule_dict.get('ignore_deps', False)

        if ignore_deps and exact_pkg is not True:
            raise Exception(
                'ignore_deps requires exact_pkg to be True'
            )

        for key, value in rule_dict.items():
            if key in ['if_variant_in', 'exact_pkg', 'ignore_deps']:
                continue

            if if_variant_in is not None:
                if not (set(variants) & set(if_variant_in)):
                    continue

            rule = key
            package_name = value

            if not kmod_pkg_list.get(package_name):
                raise Exception('Unknown package ' + package_name)

            rule_type = 'wants'
            if exact_pkg is True:
                rule_type = 'needs'
            elif key == 'default':
                rule_type = 'default'
                rule = '.*'

            log.debug('found rule: %s', (package_name, rule_type, rule, ignore_deps))
            kmod_pkg_list.rules.append((package_name, rule_type, rule, ignore_deps))

    log.info('loaded config, rules: %s', len(kmod_pkg_list.rules))
    return kmod_pkg_list


def make_pictures(pkg_list: KModPackageList, kmod_list: KModList, filename: str, print_allowed=True):
    f = open(filename + '.dot', 'w')

    f.write('digraph {\n')
    f.write('node [style=filled fillcolor="#f8f8f8"]\n')
    f.write('  subgraph kmods {\n')
    f.write('  "Legend" [shape=note label="kmod name\\n{desired package}\\nresulting package(s)"]\n')

    for kmod in kmod_list.get_topo_order():
        pkg_name = ''
        attr = ''
        if kmod.assigned_to_pkg:
            attr = 'fillcolor="#eddad5" color="#b22800"'
            pkg_name = kmod.assigned_to_pkg.name + "!"
        if kmod.preferred_pkg:
            attr = 'fillcolor="#ddddf5" color="#b268fe"'
            pkg_name = kmod.preferred_pkg.name + "?"
        allowed = ''
        if kmod.allowed_list and print_allowed:
            allowed = '=' + ' '.join([pkg.name for pkg in kmod.allowed_list])
        f.write(' "%s" [label="%s\\n%s\\n%s" shape=box %s] \n' % (kmod.name, kmod.name, pkg_name, allowed, attr))

    for kmod in kmod_list.get_topo_order():
        for kmod_dep in kmod.depends_on:
            f.write('    "%s" -> "%s";\n' % (kmod.name, kmod_dep.name))
    f.write('  }\n')

    f.write('  subgraph packages {\n')
    for pkg in pkg_list:
        desc = ''
        if pkg.default:
            desc = '/default'
        f.write(' "%s" [label="%s\\n%s"] \n' % (pkg.name, pkg.name, desc))
        for pkg_dep in pkg.depends_on:
            f.write('    "%s" -> "%s";\n' % (pkg.name, pkg_dep.name))
    f.write('  }\n')
    f.write('}\n')

    f.close()

    # safe_run_command('dot -Tpng -Gdpi=150 %s.dot > %s.png' % (filename, filename))
    safe_run_command('dot -Tsvg %s.dot > %s.svg' % (filename, filename))


def sort_kmods(depmod_pathname: str, config_str: str, variants=None, do_pictures=''):
    if variants is None:
        variants = []
    log.info('%s %s', depmod_pathname, config_str)
    kmod_list = KModList()
    kmod_list.load_depmod_file(depmod_pathname)

    pkg_list = load_config(config_str, kmod_list, variants)
    all_pkgs = set(pkg_list)

    for pkg in pkg_list:
        pkg.self_and_below = {pkg} | pkg.all_depends_on
        pkg.self_and_above = {pkg} | pkg.get_all_deps_for()

    for kmod in kmod_list.name_to_kmod_map.values():
        kmod.allowed_list = set(all_pkgs)

    basename = os.path.splitext(config_str)[0]

    apply_initial_labels(pkg_list, kmod_list)
    if '0' in do_pictures:
        make_pictures(pkg_list, kmod_list, basename + "_0", print_allowed=False)

    try:
        propagate(kmod_list)
        if '1' in do_pictures:
            make_pictures(pkg_list, kmod_list, basename + "_1")
        resolve_preferred(kmod_list)
        resolve_remaining(pkg_list, kmod_list)
    finally:
        if 'f' in do_pictures:
            make_pictures(pkg_list, kmod_list, basename + "_f")

    return pkg_list, kmod_list


def abbrev_list_for_report(alist: list[KMod]) -> str:
    tmp_str = []
    for kmod in alist:
        if kmod.allowed_list:
            tmp_str.append('%s(%s)' % (kmod.name, ' '.join([x.name for x in kmod.allowed_list])))
    ret = ', '.join(tmp_str)
    return ret


def print_report(pkg_list: KModPackageList, kmod_list: KModList):
    log.info('*'*26 + ' REPORT ' + '*'*26)

    kmods_err = 0
    kmods_moved = 0
    kmods_good = 0
    for kmod in kmod_list.get_topo_order():
        if not kmod.allowed_list:
            log.error('%s: not assigned to any package! Please check the full log for details', kmod.name)
            kmods_err = kmods_err + 1
            continue

        if len(kmod.allowed_list) > 1:
            log.error('%s: assigned to more than one package! Please check the full log for details', kmod.name)
            kmods_err = kmods_err + 1
            continue

        if not kmod.preferred_pkg:
            # config doesn't care where it ended up
            kmods_good = kmods_good + 1
            continue

        if kmod.preferred_pkg in kmod.allowed_list:
            # it ended up where it needs to be
            kmods_good = kmods_good + 1
            continue

        bad_parent_list = []
        for kmod_parent in kmod.is_dependency_for:
            if not (kmod.preferred_pkg.self_and_above & kmod_parent.allowed_list):
                bad_parent_list.append(kmod_parent)

        bad_child_list = []
        for kmod_child in kmod.depends_on:
            if not (kmod.preferred_pkg.self_and_below & kmod_child.allowed_list):
                bad_child_list.append(kmod_child)

        log.info('%s: wanted by %s but ended up in %s', kmod.name, [kmod.preferred_pkg.name], [pkg.name for pkg in kmod.allowed_list])
        if bad_parent_list:
            log.info('\thas conflicting parent: %s', abbrev_list_for_report(bad_parent_list))
        if bad_child_list:
            log.info('\thas conflicting children: %s', abbrev_list_for_report(bad_child_list))

        kmods_moved = kmods_moved + 1

    log.info('No. of kmod(s) assigned to preferred package: %s', kmods_good)
    log.info('No. of kmod(s) moved to a related package: %s', kmods_moved)
    log.info('No. of kmod(s) which could not be assigned: %s', kmods_err)
    log.info('*'*60)

    return kmods_err


def write_modules_lists(path_prefix: str, pkg_list: KModPackageList, kmod_list: KModList):
    kmod_list_alphabetical = sorted(kmod_list.get_topo_order(), key=lambda x: x.kmod_pathname)
    for pkg in pkg_list:
        output_path = os.path.join(path_prefix, pkg.name + '.list')
        i = 0
        with open(output_path, "w") as file:
            for kmod in kmod_list_alphabetical:
                if kmod.allowed_list and pkg in kmod.allowed_list:
                    file.write(kmod.kmod_pathname)
                    file.write('\n')
                    i = i + 1
        log.info('Module list %s created with %s kmods', output_path, i)


class FiltermodTests(unittest.TestCase):
    do_pictures = ''

    def setUp(self):
        self.pkg_list = None
        self.kmod_list = None

    def _is_kmod_pkg(self, kmodname, pkgnames):
        self.assertIsNotNone(self.pkg_list)
        self.assertIsNotNone(self.kmod_list)

        if type(pkgnames) is str:
            pkgnames = [pkgnames]

        expected_pkgs = []
        for pkgname in pkgnames:
            pkg = self.pkg_list.get(pkgname)
            self.assertIsNotNone(pkg)
            expected_pkgs.append(pkg)

        kmod = self.kmod_list.get(kmodname)
        self.assertIsNotNone(kmod)

        if expected_pkgs:
            self.assertTrue(len(kmod.allowed_list) == 1)
            self.assertIn(next(iter(kmod.allowed_list)), expected_pkgs)
        else:
            self.assertEqual(kmod.allowed_list, set())

    def test1a(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test1.dep'), get_td('test1.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')

    def test1b(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test1.dep'), get_td('test1.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures,
                                                   variants=['rt'])

        self.assertIsNotNone(self.pkg_list.get('modules-other'))
        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules-other')

    def test2(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test2.dep'), get_td('test2.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-extra')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules-core')
        self._is_kmod_pkg('kmod4', 'modules-core')
        self._is_kmod_pkg('kmod5', 'modules-core')
        self._is_kmod_pkg('kmod6', 'modules-extra')
        self._is_kmod_pkg('kmod8', 'modules')

    def test3(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test3.dep'), get_td('test3.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod2', ['modules-core', 'modules'])
        self._is_kmod_pkg('kmod4', ['modules-core', 'modules-extra'])
        self._is_kmod_pkg('kmod5', 'modules-core')
        self._is_kmod_pkg('kmod6', 'modules-core')

    def test4(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test4.dep'), get_td('test4.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod0', 'modules')
        self._is_kmod_pkg('kmod1', 'modules')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')
        self._is_kmod_pkg('kmod5', 'modules')
        self._is_kmod_pkg('kmod6', 'modules')
        self._is_kmod_pkg('kmod7', 'modules-partner2')
        self._is_kmod_pkg('kmod8', 'modules-partner')
        self._is_kmod_pkg('kmod9', 'modules-partner')

    def _check_preferred_pkg(self, kmodname, pkgname):
        kmod = self.kmod_list.get(kmodname)
        self.assertIsNotNone(kmod)
        self.assertEqual(kmod.preferred_pkg.name, pkgname)

    def test5(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test5.dep'), get_td('test5.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._check_preferred_pkg('kmod2', 'modules')
        self._check_preferred_pkg('kmod3', 'modules-partner')
        self._check_preferred_pkg('kmod4', 'modules-partner')

    def test6(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test6.dep'), get_td('test6.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')
        self._is_kmod_pkg('kmod1', [])

    def test7(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test7.dep'), get_td('test7.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules-other')
        self._is_kmod_pkg('kmod4', 'modules')

    def test8_needs_exact_pkg(self):
        """needs (exact_pkg) locks kmod to a specific package, deps adjust accordingly"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test8.dep'), get_td('test8.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod1', 'modules-extra')
        self._is_kmod_pkg('kmod3', 'modules')

        kmod2 = self.kmod_list.get('kmod2')
        self.assertEqual(kmod2.assigned_to_pkg.name, 'modules')

    def test9_needs_overrides_wants(self):
        """needs takes priority over wants on the same kmod"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test9.dep'), get_td('test9.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')

        kmod1 = self.kmod_list.get('kmod1')
        self.assertEqual(kmod1.assigned_to_pkg.name, 'modules-core')
        self.assertIsNone(kmod1.preferred_pkg)

    def test10_default_only(self):
        """with only a default rule, all kmods go to the default package"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test10.dep'), get_td('test10.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules')

    def test11_deep_chain(self):
        """5-level dep chain with both ends constrained, middle gets default"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test11.dep'), get_td('test11.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-extra')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')
        self._is_kmod_pkg('kmod5', 'modules-core')

    def test12_diamond_deps(self):
        """diamond in kmod deps: kmod1->kmod2->kmod4, kmod1->kmod3->kmod4"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test12.dep'), get_td('test12.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-extra')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules-core')

    def test13_disconnected_subgraphs(self):
        """two independent subgraphs are assigned independently"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test13.dep'), get_td('test13.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-extra')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules-core')
        self._is_kmod_pkg('kmod4', 'modules-core')

    def test14_wants_overridden_by_constraint(self):
        """kmod2 wants extra but kmod1's constraint forces it to core"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test14.dep'), get_td('test14.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')

        kmod2 = self.kmod_list.get('kmod2')
        self.assertEqual(kmod2.preferred_pkg.name, 'modules-extra')

    def test15_deep_propagation_across_branches(self):
        """constraint from kmod1 (extra branch) propagates 4 levels to override kmod6's partner preference"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test15.dep'), get_td('test15.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-extra')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')
        self._is_kmod_pkg('kmod5', 'modules')
        self._is_kmod_pkg('kmod6', 'modules-core')
        self._is_kmod_pkg('kmod7', 'modules-extra')

        kmod6 = self.kmod_list.get('kmod6')
        self.assertEqual(kmod6.preferred_pkg.name, 'modules-partner')

    def test16_complex_multi_branch_realistic(self):
        """realistic scenario: 5 packages (2 branches), 11 kmods (net+storage subgraphs
        joined by shared deps), needs/wants/default rules, cross-branch constraint override

        Package hierarchy (depends-on):        Kmod dependencies (A: B = A depends on B):

          modules-extra ─┐                       net_bridge ──► net_virt ──► net_base ──► crypto
                         ├─ modules ─┐                                          ▲
          modules-internal ─┘        ├─ core     net_ovs ───┬──► net_virt       │
                                     │                      │               stor_base ◄── stor_raid ◄── stor_dm
          modules-partner ───────────┘           helper ◄───┴───────────────────────────────────────────┘

                                                 partner_drv (standalone)     internal_test (standalone)

        Rules:                                  Expected result:
          net_bridge  → needs extra               net_bridge     = extra     (needs satisfied)
          internal_test → needs internal           internal_test  = internal  (needs satisfied)
          net_ovs     → wants extra                net_ovs        = extra     (wants satisfied)
          stor_dm     → wants extra                stor_dm        = extra     (wants satisfied)
          helper      → wants partner              partner_drv    = partner   (wants satisfied)
          partner_drv → wants partner              helper         = core      (wants OVERRIDDEN: partner
          default     → modules                                                unreachable from extra)
                                                   net_virt/net_base/stor_raid/stor_base/crypto = modules
        """
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test16.dep'), get_td('test16.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        # needs rules: hard-locked to exact package
        self._is_kmod_pkg('kmod_net_bridge', 'modules-extra')
        self._is_kmod_pkg('kmod_internal_test', 'modules-internal')

        # wants rules satisfied: standalone or unconstrained
        self._is_kmod_pkg('kmod_net_ovs', 'modules-extra')
        self._is_kmod_pkg('kmod_stor_dm', 'modules-extra')
        self._is_kmod_pkg('kmod_partner_drv', 'modules-partner')

        # wants overridden by cross-branch constraint: helper wanted partner
        # but net_ovs and stor_dm (both extra) depend on it, and partner is
        # not in extra's dependency chain, so helper is forced to core
        self._is_kmod_pkg('kmod_helper', 'modules-core')
        helper = self.kmod_list.get('kmod_helper')
        self.assertEqual(helper.preferred_pkg.name, 'modules-partner')

        # default fallback: intermediate and shared kmods go to modules
        self._is_kmod_pkg('kmod_net_virt', 'modules')
        self._is_kmod_pkg('kmod_net_base', 'modules')
        self._is_kmod_pkg('kmod_stor_raid', 'modules')
        self._is_kmod_pkg('kmod_stor_base', 'modules')
        self._is_kmod_pkg('kmod_crypto', 'modules')


    def test17_ignore_deps(self):
        """ignore_deps severs edges so test kmod doesn't drag real kmod across sibling pkgs"""
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test17.dep'), get_td('test17.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('test_kunit.ko', 'modules-internal')
        self._is_kmod_pkg('real.ko', 'modules-partner')
        self._is_kmod_pkg('base.ko', 'modules')

        test_kmod = self.kmod_list.get('test_kunit.ko')
        self.assertEqual(test_kmod.assigned_to_pkg.name, 'modules-internal')
        self.assertEqual(len(test_kmod.depends_on), 0)
        self.assertEqual(len(test_kmod.is_dependency_for), 0)


def do_rpm_mapping_test(config_pathname, kmod_rpms):
    """Check that kmod-to-package assignments in built RPMs match config rules."""
    import shlex
    kmod_dict = {}

    for kmod_rpm in kmod_rpms.split():
        filename = os.path.basename(kmod_rpm)

        m = re.match(r'.*-modules-([^-]+)', filename)
        if not m:
            raise Exception('Unrecognized rpm ' + kmod_rpm + ', expected a kernel-modules* rpm')
        pkgname = 'modules-' + m.group(1)
        if re.match(r'modules-([0-9.]+)', pkgname):
            pkgname = 'modules'

        tmpdir = os.path.join('tmp.filtermods', filename, pkgname)
        if not os.path.exists(tmpdir):
            log.info('creating tmp dir %s', tmpdir)
            os.makedirs(tmpdir)
            safe_run_command('rpm2cpio %s | cpio -id' % (shlex.quote(os.path.abspath(kmod_rpm))), cwddir=tmpdir)
        else:
            log.info('using cached content of tmp dir: %s', tmpdir)

        for path, subdirs, files in os.walk(tmpdir):
            for name in files:
                ret = re.match(r'.*/'+pkgname+'/lib/modules/[^/]+/[^/]+/(.*)', os.path.join(path, name))
                if not ret:
                    continue

                kmod_pathname = 'kernel/' + ret.group(1)
                if not re.search(r'\.ko(\.\w+)?$', kmod_pathname):
                    continue
                if kmod_pathname in kmod_dict:
                    if pkgname not in kmod_dict[kmod_pathname]['target_pkgs']:
                        kmod_dict[kmod_pathname]['target_pkgs'].append(pkgname)
                else:
                    kmod_dict[kmod_pathname] = {'target_pkgs': [pkgname], 'pkg': None, 'rule': None}

    kmod_pkg_list = load_config(config_pathname, None)

    default_pkg_name = None
    for package_name, rule_type, rule, _ignore_deps in kmod_pkg_list.rules:
        if rule_type == 'default':
            default_pkg_name = package_name
            continue

        param_re = '^kernel/' + rule
        pattern = re.compile(param_re)

        for kmod_pathname, kmod_rec in kmod_dict.items():
            if pattern.match(kmod_pathname):
                if rule_type == 'needs' or kmod_rec['pkg'] is None:
                    kmod_rec['pkg'] = package_name
                    kmod_rec['rule'] = '%s: %s' % (rule_type, rule)

    for kmod_pathname, kmod_rec in kmod_dict.items():
        if kmod_rec['pkg'] is None:
            kmod_rec['pkg'] = default_pkg_name
            kmod_rec['rule'] = 'default'

    for kmod_pathname, kmod_rec in kmod_dict.items():
        if kmod_rec['pkg'] is None:
            log.warning('kmod %s not matched by any config rule and no default package, in tree it is: %s', kmod_pathname, kmod_rec['target_pkgs'])
        elif kmod_rec['pkg'] not in kmod_rec['target_pkgs']:
            if kmod_rec['rule'] == 'default':
                log.info('kmod %s wanted by config in %s (rule: %s), in tree it is: %s', kmod_pathname, [kmod_rec['pkg']], kmod_rec['rule'], kmod_rec['target_pkgs'])
            else:
                log.warning('kmod %s wanted by config in %s (rule: %s), in tree it is: %s', kmod_pathname, [kmod_rec['pkg']], kmod_rec['rule'], kmod_rec['target_pkgs'])
        elif len(kmod_rec['target_pkgs']) > 1:
            log.warning('kmod %s multiple matches in tree: %s/%s', kmod_pathname, [kmod_rec['pkg']], kmod_rec['target_pkgs'])


def cmd_sort(options):
    do_pictures = ''
    if options.graphviz:
        do_pictures = '0f'

    pkg_list, kmod_list = sort_kmods(options.depmod, options.config,
                                     options.variants, do_pictures)
    ret = print_report(pkg_list, kmod_list)
    if options.output:
        write_modules_lists(options.output, pkg_list, kmod_list)

    return ret


def cmd_print_rule_map(options):
    kmod_list = KModList()
    kmod_list.load_depmod_file(options.depmod)
    pkg_list = load_config(options.config, kmod_list, options.variants)
    apply_initial_labels(pkg_list, kmod_list, treat_default_as_wants=True)

    for kmod in kmod_list.get_alphabetical_order():
        print('%-20s %s' % (kmod.preferred_pkg, kmod.kmod_pathname))


def cmd_selftest(options):
    if options.graphviz:
        FiltermodTests.do_pictures = '0f'

    for arg in ['selftest', '-g', '--graphviz']:
        if arg in sys.argv:
            sys.argv.remove(arg)

    unittest.main()
    sys.exit(0)


def cmd_cmp2rpm(options):
    do_rpm_mapping_test(options.config, options.kmod_rpms)


def main():
    global log

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose',
                        help='be more verbose', action='count', default=4)
    parser.add_argument('-q', '--quiet', dest='quiet',
                        help='be more quiet', action='count', default=0)
    parser.add_argument('-l', '--log-filename', dest='log_filename',
                        help='log filename', default='')

    subparsers = parser.add_subparsers(dest='cmd')

    def add_graphviz_arg(p):
        p.add_argument('-g', '--graphviz', dest='graphviz',
                       help='generate graphviz visualizations',
                       action='store_true', default=False)

    def add_config_arg(p):
        p.add_argument('-c', '--config', dest='config', required=True,
                       help='path to yaml config with rules')

    def add_depmod_arg(p):
        p.add_argument('-d', '--depmod', dest='depmod', required=True,
                       help='path to modules.dep file')

    def add_output_arg(p):
        p.add_argument('-o', '--output', dest='output', default=None,
                       help='output $module_name.list files to directory specified by this parameter')

    def add_variants_arg(p):
        p.add_argument('-r', '--variants', dest='variants', action='append', default=[],
                       help='variants to enable in config')

    def add_kmod_rpms_arg(p):
        p.add_argument('-k', '--kmod-rpms', dest='kmod_rpms', required=True,
                       help='compare content of specified rpm(s) against yaml config rules')

    parser_sort = subparsers.add_parser('sort', help='assign kmods specified by modules.dep using rules from yaml config')
    add_config_arg(parser_sort)
    add_depmod_arg(parser_sort)
    add_output_arg(parser_sort)
    add_variants_arg(parser_sort)
    add_graphviz_arg(parser_sort)

    parser_rule_map = subparsers.add_parser('rulemap', help='print how yaml config maps to kmods')
    add_config_arg(parser_rule_map)
    add_depmod_arg(parser_rule_map)
    add_variants_arg(parser_rule_map)

    parser_test = subparsers.add_parser('selftest', help='runs a self-test')
    add_graphviz_arg(parser_test)

    parser_cmp2rpm = subparsers.add_parser('cmp2rpm', help='compare ruleset against RPM(s)')
    add_config_arg(parser_cmp2rpm)
    add_kmod_rpms_arg(parser_cmp2rpm)

    options = parser.parse_args()

    if options.cmd == "selftest":
        options.verbose = options.verbose - 2
    options.verbose = max(options.verbose - options.quiet, 0)
    levels = [NOTSET, CRITICAL, ERROR, WARNING, INFO, DEBUG]
    stdout_log_level = levels[min(options.verbose, len(levels) - 1)]

    log = setup_logging(options.log_filename, stdout_log_level)

    ret = 0
    if options.cmd == "sort":
        ret = cmd_sort(options)
    elif options.cmd == "rulemap":
        cmd_print_rule_map(options)
    elif options.cmd == "selftest":
        cmd_selftest(options)
    elif options.cmd == "cmp2rpm":
        cmd_cmp2rpm(options)
    else:
        parser.print_help()

    return ret


if __name__ == '__main__':
    # import profile
    # profile.run('main()', sort=1)
    sys.exit(main())
