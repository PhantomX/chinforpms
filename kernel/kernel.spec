# We have to override the new %%install behavior because, well... the kernel is special.
%global __spec_install_pre %{___build_pre}

# At the time of this writing (2019-03), RHEL8 packages use w2.xzdio
# compression for rpms (xz, level 2).
# Kernel has several large (hundreds of mbytes) rpms, they take ~5 mins
# to compress by single-threaded xz. Switch to threaded compression,
# and from level 2 to 3 to keep compressed sizes close to "w2" results.
#
# NB: if default compression in /usr/lib/rpm/redhat/macros ever changes,
# this one might need tweaking (e.g. if default changes to w3.xzdio,
# change below to w4T.xzdio):
#
# This is disabled on i686 as it triggers oom errors

%ifnarch i686
%define _binary_payload w3T.xzdio
%endif

Summary: The Linux kernel

# For a kernel released for public testing, released_kernel should be 1.
# For internal testing builds during development, it should be 0.
# For rawhide and/or a kernel built from an rc or git snapshot,
# released_kernel should be 0.
# For a stable, released kernel, released_kernel should be 1.
%global released_kernel 1

%if 0%{?fedora}
%define secure_boot_arch x86_64
%else
%define secure_boot_arch x86_64 aarch64 s390x ppc64le
%endif

# Signing for secure boot authentication
%ifarch %{secure_boot_arch}
%global signkernel 1
%else
%global signkernel 0
%endif

# Sign modules on all arches
%global signmodules 1

# Compress modules only for architectures that build modules
%ifarch noarch
%global zipmodules 0
%else
%global zipmodules 1
%endif

%if %{zipmodules}
%global zipsed -e 's/\.ko$/\.ko.xz/'
%endif

%global buildid .chinfo

%if 0%{?fedora}
%define primary_target fedora
%else
%define primary_target rhel
%endif

# baserelease defines which build revision of this kernel version we're
# building.  We used to call this fedora_build, but the magical name
# baserelease is matched by the rpmdev-bumpspec tool, which you should use.
#
# We used to have some extra magic weirdness to bump this automatically,
# but now we don't.  Just use: rpmdev-bumpspec -c 'comment for changelog'
# When changing base_sublevel below or going from rc to a final kernel,
# reset this by hand to 1 (or to 0 and then use rpmdev-bumpspec).
# scripts/rebase.sh should be made to do that for you, actually.
#
# NOTE: baserelease must be > 0 or bad things will happen if you switch
#       to a released kernel (released version will be < rc version)
#
# For non-released -rc kernels, this will be appended after the rcX and
# gitX tags, so a 3 here would become part of release "0.rcX.gitX.3"
#
%global baserelease 500
%global fedora_build %{baserelease}

%define major_ver 5

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%define base_sublevel 7

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%define stable_update 12

# Apply post-factum patches? (pf release number to enable, 0 to disable)
# https://gitlab.com/post-factum/pf-kernel/
# pf applies stable patches without updating stable_update number
# stable_update above needs to match pf applied stable patches to proper rpm updates
%global post_factum 6
%global pf_url https://gitlab.com/post-factum/pf-kernel/commit
%if 0%{?post_factum}
%global pftag pf%{post_factum}
# Set a git commit hash to use it instead tag, 0 to use above tag
%global pfcommit 36ca7676257fe57d3963dca94285365fc5dc4a6e
%if "%{pfcommit}" == "0"
%global pfrange v%{major_ver}.%{base_sublevel}-%{pftag}
%else
%global pfrange %(c=%{pfcommit}; echo ${c:0:7})
%endif
%global extra_patch https://github.com/pfactum/pf-kernel/compare/v%{major_ver}.%{base_sublevel}...%{pfcommit}.diff#/pf-kernel-v%{major_ver}.%{base_sublevel}-%{pfrange}.patch

# Apply a patch range from stable repository, extending pf unmantained branches
# Root Makefile are stripped from patching
%global pf_stable_extra 0
%if 0%{?pf_stable_extra}
%global variant -old
%global st_first_commit f7688b48ac46e9a669e279f1bc167722d5141eda
%global st_last_commit 957a16c3e6e19777865c2d629408d8b4396d6a4b
%global short_st_first %(c=%{st_first_commit}; echo ${c:0:7})
%global short_st_last %(c=%{st_last_commit}; echo ${c:0:7})
%global stable_extra_patch https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/patch/?h=linux-%{major_ver}.%{base_sublevel}.y&id=%{st_last_commit}&id2=%{st_first_commit}#/kernel-stable-v%{major_ver}.%{base_sublevel}-%{short_st_first}-%{short_st_last}.patch
%endif
%endif

# Apply zen patches? (zen release number to enable, 0 to disable)
# This is not very tested
%global zen 0
%if 0%{?zen}
# Disable post_factum if zen is requested
%global post_factum 0
%endif

%global opensuse_id 501599469bceacc25b7494a8c45b87fefd7ea51a

%if 0%{?zen}
%global extra_patch https://github.com/zen-kernel/zen-kernel/releases/download/v%{major_ver}.%{base_sublevel}.%{?stable_update}-zen%{zen}/v%{major_ver}.%{base_sublevel}.%{?stable_update}-zen%{zen}.patch.xz
%endif

# Set rpm version accordingly
%if 0%{?stable_update}
%define stablerev %{stable_update}
%define stable_base %{stable_update}
%endif
%define rpmversion %{major_ver}.%{base_sublevel}.%{stable_update}

## The not-released-kernel case ##
%else
# The next upstream release sublevel (base_sublevel+1)
%define upstream_sublevel %(echo $((%{base_sublevel} + 1)))
# The rc snapshot level
%global rcrev 0
# The git snapshot level
%define gitrev 0
# Set rpm version accordingly
%define rpmversion %{major_ver}.%{upstream_sublevel}.0
%endif
# Nb: The above rcrev and gitrev values automagically define Patch00 and Patch01 below.

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks.

# The following build options are enabled by default.
# Use either --without <opt> in your rpmbuild command or force values
# to 0 in here to disable them.
#
# standard kernel
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# kernel PAE (only valid for ARM (lpae))
%define with_pae       %{?_without_pae:       0} %{?!_without_pae:       1}
# kernel-debug
%define with_debug     0
# kernel-doc
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       1}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
%define with_cross_headers   %{?_without_cross_headers:   0} %{?!_without_cross_headers:   1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# Want to build a the vsdo directories installed
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
# kernel-zfcpdump (s390 specific kernel for zfcpdump)
%define with_zfcpdump  %{?_without_zfcpdump:  0} %{?!_without_zfcpdump:  1}
# kernel-abi-whitelists
%define with_kernel_abi_whitelists %{?_without_kernel_abi_whitelists: 0} %{?!_without_kernel_abi_whitelists: 1}
# internal samples and selftests
%define with_selftests %{?_without_selftests: 0} %{?!_without_selftests: 1}
#
# Additional options for user-friendly one-off kernel building:
#
# Only build the base kernel (--with baseonly):
%define with_baseonly  %{?_with_baseonly:     1} %{?!_with_baseonly:     0}
# Only build the pae kernel (--with paeonly):
%define with_paeonly   %{?_with_paeonly:      1} %{?!_with_paeonly:      0}
# Only build the debug kernel (--with dbgonly):
%define with_dbgonly   0
#
# Control whether we perform a compat. check against published ABI.
%define with_kabichk   %{?_without_kabichk:   0} %{?!_without_kabichk:   1}
# Temporarily disable kabi checks until RC.
%define with_kabichk 0
# Control whether we perform a compat. check against DUP ABI.
%define with_kabidupchk %{?_with_kabidupchk:  1} %{?!_with_kabidupchk:   0}
#
# Control whether to run an extensive DWARF based kABI check.
# Note that this option needs to have baseline setup in SOURCE300.
%define with_kabidwchk %{?_without_kabidwchk: 0} %{?!_without_kabidwchk: 1}
%define with_kabidw_base %{?_with_kabidw_base: 1} %{?!_with_kabidw_base: 0}
#
# should we do C=1 builds with sparse
%define with_sparse    %{?_with_sparse:       1} %{?!_with_sparse:       0}
#
# Cross compile requested?
%define with_cross    %{?_with_cross:         1} %{?!_with_cross:        0}
#
# build a release kernel on rawhide
%define with_release   %{?_with_release:      1} %{?!_with_release:      0}

# verbose build, i.e. no silent rules and V=1
%define with_verbose %{?_with_verbose:        1} %{?!_with_verbose:      0}

#
# check for mismatched config options
%define with_configchecks %{?_without_configchecks:        0} %{?!_without_configchecks:        1}

#
# gcov support
%define with_gcov %{?_with_gcov: 1} %{?!_with_gcov: 0}

#
# ipa_clone support
%define with_ipaclones %{?_without_ipaclones: 0} %{?!_without_ipaclones: 1}

# Want to build a vanilla kernel build without any non-upstream patches?
%define with_vanilla %{?_with_vanilla: 1} %{?!_with_vanilla: 0}

### CPU optimizations
### with native take precedence, next is generic, then one set in kernel-local-cpu
# Use kernel-local-native (CONFIG_MNATIVE=y)
%global with_native  %{?_with_native:     1} %{?!_with_native:     0}

# Use kernel-local-generic (CONFIG_GENERIC_CPU=y)
%global with_generic %{?_with_generic:     1} %{?!_with_generic:     0}

# Set debugbuildsenabled to 1 for production (build separate debug kernels)
#  and 0 for rawhide (all kernels are debug kernels).
# See also 'make debug' and 'make release'.
%define debugbuildsenabled 1

%if 0%{?fedora}
# Kernel headers are being split out into a separate package
%define with_headers 0
%define with_cross_headers 0
# no selftests for now
%define with_selftests 0
# no ipa_clone for now
%define with_ipaclones 0
# no whitelist
%define with_kernel_abi_whitelists 0
# Fedora builds these separately
%define with_perf 0
%define with_tools 0
%define with_bpftool 0
%endif

%if %{with_verbose}
%define make_opts V=1
%else
%define make_opts -s
%endif

%if 0%{!?nopatches:1}
%define nopatches 0
%endif

%if %{with_vanilla}
%define nopatches 1
%endif

%if %{nopatches}
%global variant -vanilla
%endif

%global variantid  %{lua:variantid = string.gsub(rpm.expand("%{?variant}"), "-", "."); print(variantid)}

# pkg_release is what we'll fill in for the rpm Release: field
%if 0%{?released_kernel}

%define pkg_release %{fedora_build}%{?buildid}%{?variantid}%{?dist}

%else

# non-released_kernel
%if 0%{?rcrev}
%define rctag .rc%rcrev
%else
%define rctag .rc0
%endif
%if 0%{?gitrev}
%define gittag .git%gitrev
%else
%define gittag .git0
%endif
%define pkg_release 0%{?rctag}%{?gittag}.%{fedora_build}%{?buildid}%{?variantid}%{?dist}

%endif

# The kernel tarball/base version
%define kversion %{major_ver}.%{base_sublevel}


# turn off debug kernel and kabichk for gcov builds
%if %{with_gcov}
%define with_debug 0
%define with_kabichk 0
%define with_kabidupchk 0
%define with_kabidwchk 0
%endif

# turn off kABI DWARF-based check if we're generating the base dataset
%if %{with_kabidw_base}
%define with_kabidwchk 0
%endif

# kpatch_kcflags are extra compiler flags applied to base kernel
# -fdump-ipa-clones is enabled only for base kernels on selected arches
%if %{with_ipaclones}
%ifarch x86_64 ppc64le
%define kpatch_kcflags -fdump-ipa-clones
%else
%define with_ipaclones 0
%endif
%endif

%define make_target bzImage
%define image_install_path boot

%define KVERREL %{version}-%{release}.%{_target_cpu}
%define KVERREL_RE %(echo %KVERREL | sed 's/+/[+]/g')
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug
# Needed because we override almost everything involving build-ids
# and debuginfo generation. Currently we rely on the old alldebug setting.
%global _build_id_links alldebug

# kernel PAE is only built on ARMv7
%ifnarch armv7hl
%define with_pae 0
%endif

# if requested, only build base kernel
%if %{with_baseonly}
%define with_pae 0
%define with_debug 0
%endif

# if requested, only build pae kernel
%if %{with_paeonly}
%define with_up 0
%define with_debug 0
%endif

# if requested, only build debug kernel
%if %{with_dbgonly}
%define with_up 0
%endif

# turn off kABI DUP check and DWARF-based check if kABI check is disabled
%if !%{with_kabichk}
%define with_kabidupchk 0
%define with_kabidwchk 0
%endif

%if %{with_vdso_install}
%define use_vdso 1
%endif


%ifnarch noarch
%define with_kernel_abi_whitelists 0
%endif

# Overrides for generic default options

# only package docs noarch
%ifnarch noarch
%define with_doc 0
%define doc_build_fail true
%endif

%if 0%{?fedora}
# don't do debug builds on anything but i686 and x86_64
%ifnarch i686 x86_64
%define with_debug 0
%endif
%endif

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_up 0
%define with_headers 0
%define with_cross_headers 0
%define with_selftests 0
%define with_debug 0
%define all_arch_configs kernel-%{version}-*.config
%endif

# sparse blows up on ppc
%ifnarch ppc64le
%define with_sparse 0
%endif

# zfcpdump mechanism is s390 only
%ifnarch s390x
%define with_zfcpdump 0
%endif

%if 0%{?fedora}
# This is not for Fedora
%define with_zfcpdump 0
%endif

# Per-arch tweaks

%ifarch i686
%define asmarch x86
%define hdrarch i386
%define all_arch_configs kernel-%{version}-i?86*.config
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
%define all_arch_configs kernel-%{version}-x86_64*.config
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch ppc64le
%define asmarch powerpc
%define hdrarch powerpc
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%define all_arch_configs kernel-%{version}-ppc64le*.config
%define kcflags -O3
%endif

%ifarch s390x
%define asmarch s390
%define hdrarch s390
%define all_arch_configs kernel-%{version}-s390x.config
%define kernel_image arch/s390/boot/bzImage
%endif

%ifarch %{arm}
%define all_arch_configs kernel-%{version}-arm*.config
%define skip_nonpae_vdso 1
%define asmarch arm
%define hdrarch arm
%define make_target bzImage
%define kernel_image arch/arm/boot/zImage
# http://lists.infradead.org/pipermail/linux-arm-kernel/2012-March/091404.html
%define kernel_mflags KALLSYMS_EXTRA_PASS=1
# we only build headers/perf/tools on the base arm arches
# just like we used to only build them on i386 for x86
%ifnarch armv7hl
%define with_headers 0
%define with_cross_headers 0
%endif
# These currently don't compile on armv7
%define with_selftests 0
%endif

%ifarch aarch64
%define all_arch_configs kernel-%{version}-aarch64*.config
%define asmarch arm64
%define hdrarch arm64
%define make_target Image.gz
%define kernel_image arch/arm64/boot/Image.gz
%endif

# Should make listnewconfig fail if there's config options
# printed out?
%if %{nopatches}
%define with_configchecks 0
%endif

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We only build kernel-headers on the following...
%if 0%{?fedora}
%define nobuildarches i386
%else
%define nobuildarches i386 i686 %{arm}
%endif

%ifarch %nobuildarches
# disable BuildKernel commands
%define with_up 0
%define with_debug 0
%define with_pae 0
%define with_zfcpdump 0

%define with_debuginfo 0
%define with_perf 0
%define with_tools 0
%define with_bpftool 0
%define with_selftests 0
%define _enable_debug_packages 0
%endif

%if %{use_vdso}

%if 0%{?skip_nonpae_vdso}
%define _use_vdso 0
%else
%define _use_vdso 1
%endif

%else
%define _use_vdso 0
%endif

#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  coreutils, systemd >= 203-2, /usr/bin/kernel-install
%define initrd_prereq  dracut >= 027


Name: kernel%{?variant}
License: GPLv2 and Redistributable, no modification permitted
URL: https://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
%if 0%{?fedora}
ExclusiveArch: x86_64 s390x %{arm} aarch64 ppc64le
%else
ExclusiveArch: noarch i386 i686 x86_64 s390x %{arm} aarch64 ppc64le
%endif
ExclusiveOS: Linux
%ifnarch %{nobuildarches}
Requires: kernel-core-uname-r = %{KVERREL}
Requires: kernel-modules-uname-r = %{KVERREL}
%endif


#
# List the packages used during the kernel build
#
BuildRequires: kmod, patch, bash, tar, git-core
BuildRequires: bzip2, xz, findutils, gzip, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex
BuildRequires: net-tools, hostname, bc, elfutils-devel
%if 0%{?fedora}
BuildRequires: dwarves
%endif
%if 0%{?pf_stable_extra}
BuildRequires: patchutils
%endif
BuildRequires: python3-devel
%if %{with_headers}
BuildRequires: rsync
%endif
%if %{with_doc}
BuildRequires: xmlto, asciidoc, python3-sphinx
%endif
%if %{with_sparse}
BuildRequires: sparse
%endif
%if %{with_selftests}
%if 0%{?fedora}
BuildRequires: clang llvm
%else
BuildRequires: llvm-toolset
%endif
%ifnarch %{arm}
BuildRequires: numactl-devel
%endif
BuildRequires: libcap-devel libcap-ng-devel rsync
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
BuildConflicts: rpm < 4.13.0.1-19
%if 0%{?fedora}
BuildConflicts: dwarves < 1.13
%endif
# Most of these should be enabled after more investigation
%undefine _include_minidebuginfo
%undefine _find_debuginfo_dwz_opts
%undefine _unique_build_ids
%undefine _unique_debug_names
%undefine _unique_debug_srcs
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%global _find_debuginfo_opts -r
%global _missing_build_ids_terminate_build 1
%global _no_recompute_build_ids 1
%endif
%if %{with_kabidwchk} || %{with_kabidw_base}
BuildRequires: kabi-dw
%endif

%if %{signkernel}%{signmodules}
BuildRequires: openssl openssl-devel
%if %{signkernel}
%ifarch x86_64 aarch64
BuildRequires: nss-tools
BuildRequires: pesign >= 0.10-4
%endif
%endif
%endif

%if %{with_cross}
BuildRequires: binutils-%{_build_arch}-linux-gnu, gcc-%{_build_arch}-linux-gnu
%define cross_opts CROSS_COMPILE=%{_build_arch}-linux-gnu-
%endif

Source0: https://cdn.kernel.org/pub/linux/kernel/v%{major_ver}.x/linux-%{kversion}.tar.xz

Source1: Makefile.rhelver

# Name of the packaged file containing signing key
%ifarch ppc64le
%define signing_key_filename kernel-signing-ppc.cer
%endif
%ifarch s390x
%define signing_key_filename kernel-signing-s390.cer
%endif

Source10: x509.genkey.rhel
Source11: x509.genkey.fedora
%if %{?released_kernel}

Source12: redhatsecurebootca5.cer
Source13: redhatsecurebootca1.cer
Source14: redhatsecureboot501.cer
Source15: redhatsecureboot301.cer
Source16: secureboot_s390.cer
Source17: secureboot_ppc.cer

%define secureboot_ca_1 %{SOURCE12}
%define secureboot_ca_0 %{SOURCE13}
%ifarch x86_64 aarch64
%define secureboot_key_1 %{SOURCE14}
%define pesign_name_1 redhatsecureboot501
%define secureboot_key_0 %{SOURCE15}
%define pesign_name_0 redhatsecureboot301 
%endif
%ifarch s390x
%define secureboot_key_0 %{SOURCE16}
%define pesign_name_0 redhatsecureboot302 
%endif
%ifarch ppc64le
%define secureboot_key_0 %{SOURCE17}
%define pesign_name_0 redhatsecureboot303 
%endif

# released_kernel
%else

Source12: redhatsecurebootca4.cer
Source13: redhatsecurebootca2.cer
Source14: redhatsecureboot401.cer
Source15: redhatsecureboot003.cer 

%define secureboot_ca_1 %{SOURCE12}
%define secureboot_ca_0 %{SOURCE13}
%define secureboot_key_1 %{SOURCE14}
%define pesign_name_1 redhatsecureboot401
%define secureboot_key_0 %{SOURCE15}
%define pesign_name_0 redhatsecureboot003 

# released_kernel
%endif

Source22: mod-extra.list.rhel
Source23: mod-extra.list.fedora
Source24: mod-blacklist.sh
Source18: mod-sign.sh
Source79: parallel_xz.sh

Source80: filter-x86_64.sh.fedora
Source81: filter-armv7hl.sh.fedora
Source82: filter-i686.sh.fedora
Source83: filter-aarch64.sh.fedora
Source86: filter-ppc64le.sh.fedora
Source87: filter-s390x.sh.fedora
Source89: filter-modules.sh.fedora

Source90: filter-x86_64.sh.rhel
Source91: filter-armv7hl.sh.rhel
Source92: filter-i686.sh.rhel
Source93: filter-aarch64.sh.rhel
Source96: filter-ppc64le.sh.rhel
Source97: filter-s390x.sh.rhel
Source99: filter-modules.sh.rhel
%define modsign_cmd %{SOURCE18}

Source20: kernel-aarch64-rhel.config
Source21: kernel-aarch64-debug-rhel.config
Source30: kernel-ppc64le-rhel.config
Source31: kernel-ppc64le-debug-rhel.config
Source32: kernel-s390x-rhel.config
Source33: kernel-s390x-debug-rhel.config
Source34: kernel-s390x-zfcpdump-rhel.config
Source35: kernel-x86_64-rhel.config
Source36: kernel-x86_64-debug-rhel.config

Source37: kernel-aarch64-fedora.config
Source38: kernel-aarch64-debug-fedora.config
Source39: kernel-armv7hl-fedora.config
Source40: kernel-armv7hl-debug-fedora.config
Source41: kernel-armv7hl-lpae-fedora.config
Source42: kernel-armv7hl-lpae-debug-fedora.config
Source43: kernel-i686-fedora.config
Source44: kernel-i686-debug-fedora.config
Source45: kernel-ppc64le-fedora.config
Source46: kernel-ppc64le-debug-fedora.config
Source47: kernel-s390x-fedora.config
Source48: kernel-s390x-debug-fedora.config
Source49: kernel-x86_64-fedora.config
Source50: kernel-x86_64-debug-fedora.config

Source51: generate_all_configs.sh

Source52: process_configs.sh
Source53: generate_bls_conf.sh
Source56: update_scripts.sh

Source54: mod-internal.list

Source200: check-kabi

Source201: Module.kabi_aarch64
Source202: Module.kabi_ppc64le
Source203: Module.kabi_s390x
Source204: Module.kabi_x86_64

Source210: Module.kabi_dup_aarch64
Source211: Module.kabi_dup_ppc64le
Source212: Module.kabi_dup_s390x
Source213: Module.kabi_dup_x86_64

# Some people enjoy building customized kernels from the dist-git in Fedora and
# use this to override configuration options. One day they may all use the
# source tree, but in the mean time we carry this to support the legacy workflow
Source3000: merge.pl
Source3001: kernel-local

# This file is intentionally left empty in the stock kernel. Its a nicety
# added for those wanting to do custom rebuilds with altered config opts.
Source3011: kernel-local-cpu
Source3012: kernel-local-native
Source3013: kernel-local-pf
Source3014: kernel-local-zen
Source3015: kernel-local-generic

Source4000: README.rst

## Patches needed for building this package

# Patch1: patch-%%{rpmversion}-redhat.patch

# empty final patch to facilitate testing of kernel patches
# Patch999999: linux-kernel-test.patch

# Here should be only the patches up to the upstream canonical Linus tree.

%if 0%{?post_factum} || 0%{?zen}
Source5000: %{extra_patch}
%if 0%{?pf_stable_extra}
Source5002: %{stable_extra_patch}
%endif
%else
# For a stable release kernel
%if 0%{?stable_update}
%if 0%{?stable_base}
%define    stable_patch_00  patch-%{major_ver}.%{base_sublevel}.%{stable_base}.xz
Source5000: https://cdn.kernel.org/pub/linux/kernel/v%{major_ver}.x/%{stable_patch_00}
%endif

# non-released_kernel case
# These are automagically defined by the rcrev and gitrev values set up
# near the top of this spec file.
%else
%if 0%{?rcrev}
Source5000: patch-%{major_ver}.%{upstream_sublevel}-rc%{rcrev}.xz
%if 0%{?gitrev}
Source5001: patch-%{major_ver}.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}.xz
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
Source5000: patch-%{major_ver}.%{base_sublevel}-git%{gitrev}.xz
%endif
%endif
%endif
%endif

## Patches needed for building this package

## compile fixes

%if !%{nopatches}

Patch6: 0001-ACPI-APEI-arm64-Ignore-broken-HPE-moonshot-APEI-supp.patch
Patch8: 0001-ACPI-irq-Workaround-firmware-issue-on-X-Gene-based-m.patch
Patch9: 0001-aarch64-acpi-scan-Fix-regression-related-to-X-Gene-U.patch
Patch11: 0001-kdump-round-up-the-total-memory-size-to-128M-for-cra.patch
Patch12: 0001-kdump-add-support-for-crashkernel-auto.patch
Patch15: 0001-kdump-fix-a-grammar-issue-in-a-kernel-message.patch
Patch19: 0001-Vulcan-AHCI-PCI-bar-fix-for-Broadcom-Vulcan-early-si.patch
Patch20: 0001-ahci-thunderx2-Fix-for-errata-that-affects-stop-engi.patch
Patch24: 0001-scsi-smartpqi-add-inspur-advantech-ids.patch
Patch28: 0001-iommu-arm-smmu-workaround-DMA-mode-issues.patch
Patch29: 0001-arm-aarch64-Drop-the-EXPERT-setting-from-ARM64_FORCE.patch
Patch31: 0001-Add-efi_status_to_str-and-rework-efi_status_to_err.patch
Patch32: 0001-Make-get_cert_list-use-efi_status_to_str-to-print-er.patch
Patch33: 0001-security-lockdown-expose-a-hook-to-lock-the-kernel-d.patch
Patch34: 0001-efi-Add-an-EFI_SECURE_BOOT-flag-to-indicate-secure-b.patch
Patch35: 0001-efi-Lock-down-the-kernel-if-booted-in-secure-boot-mo.patch
Patch36: 0001-s390-Lock-down-the-kernel-when-the-IPL-secure-flag-i.patch
Patch37: 0001-Add-option-of-13-for-FORCE_MAX_ZONEORDER.patch
Patch58: 0001-arm-make-CONFIG_HIGHPTE-optional-without-CONFIG_EXPE.patch
Patch59: 0001-ARM-tegra-usb-no-reset.patch
Patch62: 0001-Input-rmi4-remove-the-need-for-artificial-IRQ-in-cas.patch
Patch63: 0001-Drop-that-for-now.patch
Patch64: 0001-KEYS-Make-use-of-platform-keyring-for-module-signatu.patch
Patch65: 0001-mm-kmemleak-skip-late_init-if-not-skip-disable.patch
Patch66: 0001-ARM-fix-__get_user_check-in-case-uaccess_-calls-are-.patch
Patch67: 0001-soc-bcm2835-Sync-xHCI-reset-firmware-property-with-d.patch
Patch68: 0001-firmware-raspberrypi-Introduce-vl805-init-routine.patch
Patch69: 0001-PCI-brcmstb-Wait-for-Raspberry-Pi-s-firmware-when-pr.patch
Patch70: 0001-USB-pci-quirks-Add-Raspberry-Pi-4-quirk.patch
Patch75: 0001-e1000e-bump-up-timeout-to-wait-when-ME-un-configure-.patch
Patch76: 0001-perf-cs-etm-Move-defined-of-traceid_list.patch
Patch79: 0001-disp-gv100-expose-capabilities-class.patch
Patch80: 0001-core-memory-remove-redundant-assignments-to-variable.patch
Patch81: 0001-acr-Use-kmemdup-instead-of-kmalloc-and-memcpy.patch
Patch82: 0001-drm-Use-generic-helper-to-check-_PR3-presence.patch
Patch83: 0001-mmu-Remove-unneeded-semicolon.patch
Patch84: 0001-device-rework-mmio-mapping-code-to-get-rid-of-second.patch
Patch85: 0001-device-detect-if-changing-endianness-failed.patch
Patch86: 0001-device-detect-vGPUs.patch
Patch87: 0001-device-use-regular-PRI-accessors-in-chipset-detectio.patch
Patch89: 0001-disp-nv50-increase-timeout-on-pio-channel-free-polli.patch
Patch90: 0001-disp-hda-gt215-pass-head-to-nvkm_ior.hda.eld.patch
Patch91: 0001-disp-hda-gf119-add-HAL-for-programming-device-entry-.patch
Patch92: 0001-disp-hda-gf119-select-HDA-device-entry-based-on-boun.patch
Patch93: 0001-disp-hda-gv100-NV_PDISP_SF_AUDIO_CNTRL0-register-mov.patch
Patch94: 0001-kms-nv50-Initialize-core-channel-in-nouveau_display_.patch
Patch95: 0001-kms-nv50-Probe-SOR-and-PIOR-caps-for-DP-interlacing-.patch
Patch96: 0001-kms-gv100-Add-support-for-interlaced-modes.patch
Patch97: 0001-kms-nv50-Move-8BPC-limit-for-MST-into-nv50_mstc_get_.patch
Patch98: 0001-kms-nv50-Share-DP-SST-mode_valid-handling-with-MST.patch
Patch107: 0001-platform-x86-thinkpad_acpi-Add-support-for-dual-fan-.patch
Patch108: selinux_allow_reading_labels_before_policy_is_loaded.patch 

# Latest upstream screen driver - https://patchwork.kernel.org/patch/11627069/
Patch110: 0001-dt-bindings-vendor-prefixes-Add-Xingbangda.patch
Patch111: 0002-dt-bindings-panel-Convert-rocktech-jh057n00900-to-ya.patch
Patch112: 0003-dt-bindings-panel-Add-compatible-for-Xingbangda-XBD5.patch
Patch113: 0004-drm-panel-rocktech-jh057n00900-Rename-the-driver-to-.patch
Patch114: 0005-drm-panel-st7703-Rename-functions-from-jh057n-prefix.patch
Patch115: 0006-drm-panel-st7703-Prepare-for-supporting-multiple-pan.patch
Patch116: 0007-drm-panel-st7703-Move-code-specific-to-jh057n-closer.patch
Patch117: 0008-drm-panel-st7703-Move-generic-part-of-init-sequence-.patch
Patch118: 0009-drm-panel-st7703-Add-support-for-Xingbangda-XBD599.patch
Patch119: 0010-drm-panel-st7703-Enter-sleep-after-display-off.patch
Patch120: 0011-drm-panel-st7703-Assert-reset-prior-to-powering-down.patch
Patch121: 0012-arm64-dts-sun50i-a64-pinephone-Enable-LCD-support-on.patch
Patch122: 0013-arm64-dts-sun50i-a64-pinephone-Add-touchscreen-suppo.patch
# Back port from 5.8
Patch123: 0001-usb-fusb302-Convert-to-use-GPIO-descriptors.patch

# rhbz 1857101
Patch125: 0001-ALSA-hda-Workaround-for-spurious-wakeups-on-some-Int.patch 

### Extra

### openSUSE patches - http://kernel.opensuse.org/cgit/kernel-source/

%global opensuse_url https://github.com/openSUSE/kernel-source/raw/%{opensuse_id}/patches.suse

Patch1010: %{opensuse_url}/vfs-add-super_operations-get_inode_dev#/openSUSE-vfs-add-super_operations-get_inode_dev.patch
Patch1011: %{opensuse_url}/btrfs-provide-super_operations-get_inode_dev#/openSUSE-btrfs-provide-super_operations-get_inode_dev.patch
Patch1012: %{opensuse_url}/btrfs-fs-super.c-add-new-super-block-devices-super_block_d.patch#/openSUSE-btrfs-fs-super.c-add-new-super-block-devices-super_block_d.patch
Patch1013: %{opensuse_url}/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch#/openSUSE-btrfs-btrfs-use-the-new-VFS-super_block_dev.patch
Patch1014: %{opensuse_url}/btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch#/openSUSE-btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch
Patch1015: %{opensuse_url}/dm-mpath-leastpending-path-update#/openSUSE-dm-mpath-leastpending-path-update.patch
Patch1016: %{opensuse_url}/dm-table-switch-to-readonly#/openSUSE-dm-table-switch-to-readonly.patch
Patch1017: %{opensuse_url}/dm-mpath-no-partitions-feature#/openSUSE-dm-mpath-no-partitions-feature.patch
Patch1018: %{opensuse_url}/pstore_disable_efi_backend_by_default.patch#/openSUSE-pstore_disable_efi_backend_by_default.patch

%global patchwork_url https://patchwork.kernel.org/patch
%global patchwork_xdg_url https://patchwork.freedesktop.org/patch
Patch2000: %{patchwork_url}/10045863/mbox/#/patchwork-radeon_dp_aux_transfer_native-74-callbacks-suppressed.patch
%if !0%{?post_factum}

#Patch3000: postfactum-merge-fixes.patch
%if !0%{?zen}
#Patch3001: %{pf_url}/a6c083c2e4274c7e203c5ef989f568c6d5f945eb.patch#/pf-a6c083c.patch
%endif

#Patch3500: postfactum-merge-fixes-2.patch

%if !0%{?zen}
# Add additional cpu gcc optimization support
# https://github.com/graysky2/kernel_gcc_patch
%global graysky2_id b9aeee77b2c3e76c1faeca297e4e4a448babaaee
Source4000: https://github.com/graysky2/kernel_gcc_patch/raw/%{graysky2_id}/enable_additional_cpu_optimizations_for_gcc_v9.1+_kernel_v5.5+.patch
%endif

%endif

%if !0%{?zen}
Patch4010: 0001-block-elevator-default-blk-mq-to-bfq.patch
%endif

# END OF PATCH DEFINITIONS

%endif


%description
The kernel meta package

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#    %%kernel_reqprovconf <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
#
%define kernel_reqprovconf \
Provides: kernel = %{rpmversion}-%{pkg_release}\
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{pkg_release}%{?1:+%{1}}\
Provides: kernel-drm-nouveau = 16\
Provides: kernel-uname-r = %{KVERREL}%{?1:+%{1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(pre): linux-firmware >= 20150904-56.git6ebf5d57\
Requires(preun): systemd >= 200\
Conflicts: xfsprogs < 4.3.0-1\
Conflicts: xorg-x11-drv-vmmouse < 13.0.99\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}


%package doc
Summary: Various documentation bits found in the kernel source
Group: Documentation
%description doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.


%package headers
Summary: Header files for the Linux kernel for use by glibc
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if "0%{?variant}"
Obsoletes: kernel-headers < %{rpmversion}-%{pkg_release}
Provides: kernel-headers = %{rpmversion}-%{pkg_release}
%endif
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc
%description cross-headers
Kernel-cross-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
cross-glibc package.


%package debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by %{name}-debuginfo packages
Provides: installonlypkg(kernel)
%description debuginfo-common-%{_target_cpu}
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.

%if %{with_selftests}
%package selftests-internal
Summary: Kernel samples and selftests
License: GPLv2
Requires: binutils, bpftool, iproute-tc, nmap-ncat
Requires: kernel-modules-internal = %{version}-%{release}
%description selftests-internal
Kernel sample programs and selftests.
%{nil}
# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_libexecdir}/(ksamples|kselftests)/.*|XXX' -o selftests-debuginfo.list}

# with_selftests
%endif

%if %{with_gcov}
%package gcov
Summary: gcov graph and source files for coverage data collection.
%description gcov
kernel-gcov includes the gcov graph and source files for gcov coverage collection.
%endif

%package -n kernel-abi-whitelists
Summary: The Red Hat Enterprise Linux kernel ABI symbol whitelists
AutoReqProv: no
%description -n kernel-abi-whitelists
The kABI package contains information pertaining to the Red Hat Enterprise
Linux kernel ABI, including lists of kernel symbols that are needed by
external Linux kernel modules, and a yum plugin to aid enforcement.

%if %{with_kabidw_base}
%package kabidw-base
Summary: The baseline dataset for kABI verification using DWARF data
Group: System Environment/Kernel
AutoReqProv: no
%description kabidw-base
The kabidw-base package contains data describing the current ABI of the Red Hat
Enterprise Linux kernel, suitable for the kabi-dw tool.
%endif

#
# This macro creates a kernel-<subpackage>-debuginfo package.
#    %%kernel_debuginfo_package <subpackage>
#
# Explanation of the find_debuginfo_opts: We build multiple kernels (debug
# pae etc.) so the regex filters those kernels appropriately. We also
# have to package several binaries as part of kernel-devel but getting
# unique build-ids is tricky for these userspace binaries. We don't really
# care about debugging those so we just filter those out and remove it.
%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{version}-%{release}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
%description %{?1:%{1}-}debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*\/usr\/src\/kernels/.*|XXX' -o ignored-debuginfo.list -p '/.*/%%{KVERREL_RE}%{?1:[+]%{1}}/.*|/.*%%{KVERREL_RE}%{?1:\+%{1}}(\.debug)?' -o debuginfo%{?1}.list}\


%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#    %%kernel_devel_package <subpackage> <pretty-name>
#
%define kernel_devel_package() \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Provides: kernel%{?1:-%{1}}-devel-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{?1:+%{1}}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
Requires(pre): findutils\
Requires: findutils\
Requires: perl-interpreter\
%description %{?1:%{1}-}devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# kernel-<variant>-ipaclones-internal package
#
%define kernel_ipaclones_package() \
%package %{?1:%{1}-}ipaclones-internal\
Summary: *.ipa-clones files generated by -fdump-ipa-clones for kernel%{?1:-%{1}}\
Group: System Environment/Kernel\
AutoReqProv: no\
%description %{?1:%{1}-}ipaclones-internal\
This package provides *.ipa-clones files.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-internal package.
#    %%kernel_modules_internal_package <subpackage> <pretty-name>
#
%define kernel_modules_internal_package() \
%package %{?1:%{1}-}modules-internal\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: kernel%{?1:-%{1}}-modules-internal-%{_target_cpu} = %{version}-%{release}\
Provides: kernel%{?1:-%{1}}-modules-internal-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel%{?1:-%{1}}-modules-internal = %{version}-%{release}%{?1:+%{1}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-internal-uname-r = %{KVERREL}%{?1:+%{1}}\
Requires: kernel-uname-r = %{KVERREL}%{?1:+%{1}}\
Requires: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{?1:+%{1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-internal\
This package provides kernel modules for the %{?2:%{2} }kernel package for Red Hat internal usage.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-extra package.
#    %%kernel_modules_extra_package <subpackage> <pretty-name>
#
%define kernel_modules_extra_package() \
%package %{?1:%{1}-}modules-extra\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Provides: kernel%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{version}-%{release}\
Provides: kernel%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel%{?1:-%{1}}-modules-extra = %{version}-%{release}%{?1:+%{1}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-extra-uname-r = %{KVERREL}%{?1:+%{1}}\
Requires: kernel-uname-r = %{KVERREL}%{?1:+%{1}}\
Requires: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{?1:+%{1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-extra\
This package provides less commonly used kernel modules for the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules package.
#    %%kernel_modules_package <subpackage> <pretty-name>
#
%define kernel_modules_package() \
%package %{?1:%{1}-}modules\
Summary: kernel modules to match the %{?2:%{2}-}core kernel\
Provides: kernel%{?1:-%{1}}-modules-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-modules-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel-modules = %{version}-%{release}%{?1:+%{1}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{?1:+%{1}}\
Requires: kernel-uname-r = %{KVERREL}%{?1:+%{1}}\
Recommends: alsa-sof-firmware\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules\
This package provides commonly used kernel modules for the %{?2:%{2}-}core kernel package.\
%{nil}

#
# this macro creates a kernel-<subpackage> meta package.
#    %%kernel_meta_package <subpackage>
#
%define kernel_meta_package() \
%package %{1}\
summary: kernel meta-package for the %{1} kernel\
Requires: kernel-%{1}-core-uname-r = %{KVERREL}+%{1}\
Requires: kernel-%{1}-modules-uname-r = %{KVERREL}+%{1}\
Provides: installonlypkg(kernel)\
%description %{1}\
The meta-package for the %{1} kernel\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#    %%define variant_summary The Linux kernel compiled for <configuration>
#    %%kernel_variant_package [-n <pretty-name>] <subpackage>
#
%define kernel_variant_package(n:) \
%package %{?1:%{1}-}core\
Summary: %{variant_summary}\
Provides: kernel-%{?1:%{1}-}core-uname-r = %{KVERREL}%{?1:+%{1}}\
Provides: installonlypkg(kernel)\
%ifarch ppc64le\
Obsoletes: kernel-bootwrapper\
%endif\
%{expand:%%kernel_reqprovconf}\
%if %{?1:1} %{!?1:0} \
%{expand:%%kernel_meta_package %{?1:%{1}}}\
%endif\
%{expand:%%kernel_devel_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_modules_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_modules_extra_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_modules_internal_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_debuginfo_package %{?1:%{1}}}\
%{nil}

# Now, each variant package.

%if %{with_pae}
%define variant_summary The Linux kernel compiled for Cortex-A15
%kernel_variant_package lpae
%description lpae-core
This package includes a version of the Linux kernel with support for
Cortex-A15 devices with LPAE and HW virtualisation support
%endif

%if %{with_zfcpdump}
%define variant_summary The Linux kernel compiled for zfcpdump usage
%kernel_variant_package zfcpdump
%description zfcpdump-core
The kernel package contains the Linux kernel (vmlinuz) for use by the
zfcpdump infrastructure.
# with_zfcpdump
%endif

%define variant_summary The Linux kernel compiled with extra debugging enabled
%kernel_variant_package debug
%description debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.

# And finally the main -core package

%define variant_summary The Linux kernel
%kernel_variant_package
%description core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

%if %{with_ipaclones}
%kernel_ipaclones_package
%endif

%prep
# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_up}%{with_pae}
echo "Cannot build --with baseonly, up build is disabled"
exit 1
%endif
%endif

%if "%{baserelease}" == "0"
echo "baserelease must be greater than zero"
exit 1
%endif

# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      echo "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"
      exit 1
    fi
  done
fi 2>/dev/null

patch_command='patch -p1 -F1 -s'

# First we unpack the kernel tarball.
# If this isn't the first make prep, we use links to the existing clean tarball
# which speeds things up quite a bit.

# Update to latest upstream.
%if 0%{?released_kernel}
%define vanillaversion %{major_ver}.%{base_sublevel}
# non-released_kernel case
%else
%if 0%{?rcrev}
%define vanillaversion %{major_ver}.%{upstream_sublevel}-rc%{rcrev}
%if 0%{?gitrev}
%define vanillaversion %{major_ver}.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
%define vanillaversion %{major_ver}.%{base_sublevel}-git%{gitrev}
%else
%define vanillaversion %{major_ver}.%{base_sublevel}
%endif
%endif
%endif

# %%{vanillaversion} : the full version name, e.g. 2.6.35-rc6-git3
# %%{kversion}       : the base version, e.g. 2.6.34

# Use kernel-%%{kversion}%%{?dist} as the top-level directory name
# so we can prep different trees within a single git directory.

# Build a list of the other top-level kernel tree directories.
# This will be used to hardlink identical vanilla subdirs.
sharedirs=$(find "$PWD" -maxdepth 1 -type d -name 'kernel-%{major_ver}.*' \
            | grep -x -v "$PWD"/kernel-%{kversion}%{?dist}) ||:

# Delete all old stale trees.
if [ -d kernel-%{kversion}%{?dist} ]; then
  cd kernel-%{kversion}%{?dist}
  for i in linux-*
  do
     if [ -d $i ]; then
       # Just in case we ctrl-c'd a prep already
       rm -rf deleteme.%{_target_cpu}
       # Move away the stale away, and delete in background.
       mv $i deleteme-$i
       rm -rf deleteme* &
     fi
  done
  cd ..
fi

# Generate new tree
if [ ! -d kernel-%{kversion}%{?dist}/vanilla-%{vanillaversion} ]; then

  if [ -d kernel-%{kversion}%{?dist}/vanilla-%{kversion} ]; then

    # The base vanilla version already exists.
    cd kernel-%{kversion}%{?dist}

    # Any vanilla-* directories other than the base one are stale.
    for dir in vanilla-*; do
      [ "$dir" = vanilla-%{kversion} ] || rm -rf $dir &
    done

  else

    rm -f pax_global_header
    # Look for an identical base vanilla dir that can be hardlinked.
    for sharedir in $sharedirs ; do
      if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{kversion} ]] ; then
        break
      fi
    done
    if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{kversion} ]] ; then
%setup -q -n kernel-%{kversion}%{?dist} -c -T
      cp -al $sharedir/vanilla-%{kversion} .
    else
%setup -q -n kernel-%{kversion}%{?dist} -c
      mv linux-%{kversion} vanilla-%{kversion}
    fi

  fi

%if "%{kversion}" != "%{vanillaversion}"

  for sharedir in $sharedirs ; do
    if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{vanillaversion} ]] ; then
      break
    fi
  done
  if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{vanillaversion} ]] ; then

    cp -al $sharedir/vanilla-%{vanillaversion} .

  else

    # Need to apply patches to the base vanilla version.
    cp -al vanilla-%{kversion} vanilla-%{vanillaversion}
    cd vanilla-%{vanillaversion}

cp %{SOURCE12} .

# Update vanilla to the latest upstream.
# (non-released_kernel case only)
%if 0%{?rcrev}
    xzcat %{SOURCE5000} | $patch_command
%if 0%{?gitrev}
    xzcat %{SOURCE5001} | $patch_command
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
    xzcat %{SOURCE5000} | $patch_command
%endif
%endif
    git init
    git config user.email "kernel-team@fedoraproject.org"
    git config user.name "Fedora Kernel Team"
    git config gc.auto 0
    git add .
    git commit -a -q -m "baseline"

    cd ..

  fi

%endif

else

  # We already have all vanilla dirs, just change to the top-level directory.
  cd kernel-%{kversion}%{?dist}

fi

# Now build the fedora kernel tree.
cp -al vanilla-%{vanillaversion} linux-%{KVERREL}

cd linux-%{KVERREL}
cp -a %{SOURCE1} .

if [ ! -d .git ]; then
    git init
    git config user.email "kernel-team@fedoraproject.org"
    git config user.name "Fedora Kernel Team"
    git config gc.auto 0
    git add .
    git commit -a -q -m "baseline"
fi


%if 0%{?post_factum}
$patch_command -i %{SOURCE5000}
%if 0%{?pf_stable_extra}
filterdiff -p1 -x Makefile %{SOURCE5002} > pf_stable_extra.patch
$patch_command -i pf_stable_extra.patch
rm -f pf_stable_extra.patch
%endif
git add .
git commit -a -m "Stable post-factum update"
%else
# released_kernel with possible stable updates
%if 0%{?stable_base}
# This is special because the kernel spec is hell and nothing is consistent
xzcat %{SOURCE5000} | $patch_command
git commit -a -m "Stable update"
%endif
%endif

# Note: Even in the "nopatches" path some patches (build tweaks and compile
# fixes) will always get applied; see patch defition above for details

git am %{patches}

%if !0%{?post_factum} && !0%{?zen}
$patch_command -i %{SOURCE4000}
%endif

# END OF PATCH APPLICATIONS

# Any further pre-build tree manipulations happen here.

chmod +x scripts/checkpatch.pl
chmod +x tools/objtool/sync-check.sh
mv COPYING COPYING-%{version}-%{release}

# This Prevents scripts/setlocalversion from mucking with our version numbers.
touch .scmversion

# Mangle /usr/bin/python shebangs to /usr/bin/python3
# Mangle all Python shebangs to be Python 3 explicitly
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# This fixes errors such as
# *** ERROR: ambiguous python shebang in /usr/bin/kvm_stat: #!/usr/bin/python. Change it to python3 (or python2) explicitly.
# We patch all sources below for which we got a report/error.
pathfix.py -i "%{__python3} %{py3_shbang_opts}" -p -n \
    tools/kvm/kvm_stat/kvm_stat \
    scripts/show_delta \
    scripts/diffconfig \
    scripts/bloat-o-meter \
    scripts/jobserver-exec \
    tools/perf/tests/attr.py \
    tools/perf/scripts/python/stat-cpi.py \
    tools/perf/scripts/python/sched-migration.py \
    tools/testing/selftests/drivers/net/mlxsw/sharedbuffer_configuration.py \
    Documentation \
    scripts/gen_compile_commands.py

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

if [ -L configs ]; then
    rm -f configs
fi
# Deal with configs stuff
mkdir configs
cd configs

# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/kernel-*.config .
cp %{SOURCE3001} .
%if %{with_native}
cat %{SOURCE3012} >> kernel-local
%else
%if %{with_generic}
cat %{SOURCE3015} >> kernel-local
%else
cat %{SOURCE3011} >> kernel-local
%endif
%endif

%if 0%{?post_factum}
cat %{SOURCE3013} >> kernel-local
%endif
%if 0%{?zen}
cat %{SOURCE3014} >> kernel-local
%endif
cp %{SOURCE51} .
# merge.pl
cp %{SOURCE3000} .
VERSION=%{version} ./generate_all_configs.sh %{primary_target} %{debugbuildsenabled}


# Merge in any user-provided local config option changes
%ifnarch %nobuildarches
for i in %{all_arch_configs}
do
  mv $i $i.tmp
  ./merge.pl kernel-local $i.tmp > $i
  rm $i.tmp
done
%endif

%if !%{debugbuildsenabled}
rm -f kernel-%{version}-*debug.config
%endif

# enable GCOV kernel config options if gcov is on
%if %{with_gcov}
for i in *.config
do
  sed -i 's/# CONFIG_GCOV_KERNEL is not set/CONFIG_GCOV_KERNEL=y\nCONFIG_GCOV_PROFILE_ALL=y\n/' $i
done
%endif

cp %{SOURCE52} .
OPTS=""
%if %{with_configchecks}
    OPTS="$OPTS -w -n -c"
%endif
./process_configs.sh $OPTS kernel %{rpmversion}

cp %{SOURCE56} .
RPM_SOURCE_DIR=$RPM_SOURCE_DIR ./update_scripts.sh %{primary_target}

# end of kernel config
%endif

cd ..
# # End of Configs stuff

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -delete >/dev/null

# remove unnecessary SCM files
find . -name .gitignore -delete >/dev/null

cd ..

###
### build
###
%build

%if %{with_sparse}
%define sparse_mflags    C=1
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

# Note we need to disable these flags for cross builds because the flags
# from redhat-rpm-config assume that host == target so target arch
# flags cause issues with the host compiler.
%if !%{with_cross}
%define build_hostcflags  %{?build_cflags}
%define build_hostldflags %{?build_ldflags}
%endif

%define make %{__make} %{?cross_opts} %{?make_opts} LD=ld.bfd HOSTCFLAGS="%{?build_hostcflags}" HOSTLDFLAGS="%{?build_hostldflags}"

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$4
    DoVDSO=$3
    Flav=${Flavour:++${Flavour}}
    InstallName=${5:-vmlinuz}

    DoModules=1
    if [ "$Flavour" = "zfcpdump" ]; then
        DoModules=0
    fi

    # Pick the right config file for the kernel we're building
    Config=kernel-%{version}-%{_target_cpu}${Flavour:+-${Flavour}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Flav}

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

    KernelVer=%{version}-%{release}.%{_target_cpu}${Flav}
    echo BUILDING A KERNEL FOR ${Flavour} %{_target_cpu}...

    %if 0%{?stable_update}
    # make sure SUBLEVEL is incremented on a stable release.  Sigh 3.x.
    perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{?stablerev}/" Makefile
    %endif

    # make sure EXTRAVERSION says what we want it to say
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}.%{_target_cpu}${Flav}/" Makefile

    # if pre-rc1 devel kernel, must fix up PATCHLEVEL for our versioning scheme
    %if !0%{?rcrev}
    %if 0%{?gitrev}
    perl -p -i -e 's/^PATCHLEVEL.*/PATCHLEVEL = %{upstream_sublevel}/' Makefile
    %endif
    %endif

    # and now to start the build process

    %{make} %{?_smp_mflags} mrproper
    cp configs/$Config .config

    %if %{signkernel}%{signmodules}
    cp $RPM_SOURCE_DIR/x509.genkey certs/.
    %endif

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    KCFLAGS="%{?kcflags}"

    # add kpatch flags for base kernel
    if [ "$Flavour" == "" ]; then
        KCFLAGS="$KCFLAGS %{?kpatch_kcflags}"
    fi

    %{make} ARCH=$Arch olddefconfig >/dev/null

    # This ensures build-ids are unique to allow parallel debuginfo
    perl -p -i -e "s/^CONFIG_BUILD_SALT.*/CONFIG_BUILD_SALT=\"%{KVERREL}\"/" .config
    %{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?kernel_mflags}
    if [ $DoModules -eq 1 ]; then
    %{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} modules %{?sparse_mflags} || exit 1
    fi

    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif

%ifarch %{arm} aarch64
    %{make} ARCH=$Arch dtbs INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    %{make} ARCH=$Arch dtbs_install INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    cp -r $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/dtb
    find arch/$Arch/boot/dts -name '*.dtb' -type f -delete
%endif

    # Start installing the results
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/config
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/System.map

    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=20

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/lib/modules/$KernelVer/zImage.stub-$KernelVer || :
    fi

    %if %{signkernel}
    if [ "$KernelImage" = vmlinux ]; then
        # We can't strip and sign $KernelImage in place, because
        # we need to preserve original vmlinux for debuginfo.
        # Use a copy for signing.
        $CopyKernel $KernelImage $KernelImage.tosign
        KernelImage=$KernelImage.tosign
        CopyKernel=cp
    fi

    # Sign the image if we're using EFI
    # aarch64 kernels are gziped EFI images
    KernelExtension=${KernelImage##*.}
    if [ "$KernelExtension" == "gz" ]; then
        SignImage=${KernelImage%.*}
    else
        SignImage=$KernelImage
    fi

    %ifarch x86_64 aarch64
     %pesign -s -i $SignImage -o vmlinuz.tmp -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
     %pesign -s -i vmlinuz.tmp -o vmlinuz.signed -a %{secureboot_ca_1} -c %{secureboot_key_1} -n %{pesign_name_1}
     rm vmlinuz.tmp 
    %endif
    %ifarch s390x ppc64le
    if [ -x /usr/bin/rpm-sign ]; then
    rpm-sign --key "%{pesign_name_0}" --lkmsign $SignImage --output vmlinuz.signed
    elif [ $DoModules -eq 1 ]; then
    chmod +x scripts/sign-file
    ./scripts/sign-file -p sha256 certs/signing_key.pem certs/signing_key.x509 $SignImage vmlinuz.signed
    else
    mv $SignImage vmlinuz.signed
    fi
    %endif

    if [ ! -s vmlinuz.signed ]; then
        echo "pesigning failed"
        exit 1
    fi
    mv vmlinuz.signed $SignImage
    if [ "$KernelExtension" == "gz" ]; then
        gzip -f9 $SignImage
    fi
    # signkernel
    %endif
    $CopyKernel $KernelImage \
                $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    cp $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/$InstallName

    # hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    sha512hmac $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer | sed -e "s,$RPM_BUILD_ROOT,," > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;
    cp $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac $RPM_BUILD_ROOT/lib/modules/$KernelVer/.vmlinuz.hmac

    if [ $DoModules -eq 1 ]; then
    # Override $(mod-fw) because we don't want it to install any firmware
    # we'll get it from the linux-firmware package and we don't want conflicts
    %{make} %{?_smp_mflags} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=
    fi

%if %{with_gcov}
    # install gcov-needed files to $BUILDROOT/$BUILD/...:
    #   gcov_info->filename is absolute path
    #   gcno references to sources can use absolute paths (e.g. in out-of-tree builds)
    #   sysfs symlink targets (set up at compile time) use absolute paths to BUILD dir
    find . \( -name '*.gcno' -o -name '*.[chS]' \) -exec install -D '{}' "$RPM_BUILD_ROOT/$(pwd)/{}" \;
%endif

    # add an a noop %%defattr statement 'cause rpm doesn't like empty file list files
    echo '%%defattr(-,-,-)' > ../kernel${Flavour:+-${Flavour}}-ldsoconf.list
    if [ $DoVDSO -ne 0 ]; then
        %{make} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
        if [ -s ldconfig-kernel.conf ]; then
             install -D -m 444 ldconfig-kernel.conf \
                $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
         echo /etc/ld.so.conf.d/kernel-$KernelVer.conf >> ../kernel${Flavour:+-${Flavour}}-ldsoconf.list
        fi

        rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/vdso/.build-id
    fi

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
%if 0%{!?fedora:1}
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates
%endif
    # CONFIG_KERNEL_HEADER_TEST generates some extra files in the process of
    # testing so just delete
    find . -name *.h.s -delete 
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi

    # create the kABI metadata for use in packaging
    # NOTENOTE: the name symvers is used by the rpm backend
    # NOTENOTE: to discover and run the /usr/lib/rpm/fileattrs/kabi.attr
    # NOTENOTE: script which dynamically adds exported kernel symbol
    # NOTENOTE: checksums to the rpm metadata provides list.
    # NOTENOTE: if you change the symvers name, update the backend too
    echo "**** GENERATING kernel ABI metadata ****"
    gzip -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz
    cp $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz $RPM_BUILD_ROOT/lib/modules/$KernelVer/symvers.gz
%if %{with_kabichk}
    echo "**** kABI checking is enabled in kernel SPEC file. ****"
    chmod 0755 $RPM_SOURCE_DIR/check-kabi
    if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
        echo "**** NOTE: Cannot find reference Module.kabi file. ****"
    fi
%endif

%if %{with_kabidupchk}
    echo "**** kABI DUP checking is enabled in kernel SPEC file. ****"
    if [ -e $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Flavour ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Flavour $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
        echo "**** NOTE: Cannot find DUP reference Module.kabi file. ****"
    fi
%endif

%if %{with_kabidw_base}
    # Don't build kabi base for debug kernels
    if [ "$Flavour" != "kdump" -a "$Flavour" != "debug" ]; then
        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf
        tar xjvf %{SOURCE301} -C $RPM_BUILD_ROOT/kabi-dwarf

        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf/whitelists
        tar xjvf %{SOURCE300} -C $RPM_BUILD_ROOT/kabi-dwarf/whitelists

        echo "**** GENERATING DWARF-based kABI baseline dataset ****"
        chmod 0755 $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh
        $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh generate \
            "$RPM_BUILD_ROOT/kabi-dwarf/whitelists/kabi-current/kabi_whitelist_%{_target_cpu}" \
            "$(pwd)" \
            "$RPM_BUILD_ROOT/kabidw-base/%{_target_cpu}${Flavour:+.${Flavour}}" || :

        rm -rf $RPM_BUILD_ROOT/kabi-dwarf
    fi
%endif

%if %{with_kabidwchk}
    if [ "$Flavour" != "kdump" ]; then
        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf
        tar xjvf %{SOURCE301} -C $RPM_BUILD_ROOT/kabi-dwarf
        if [ -d "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Flavour:+.${Flavour}}" ]; then
            mkdir -p $RPM_BUILD_ROOT/kabi-dwarf/whitelists
            tar xjvf %{SOURCE300} -C $RPM_BUILD_ROOT/kabi-dwarf/whitelists

            echo "**** GENERATING DWARF-based kABI dataset ****"
            chmod 0755 $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh generate \
                "$RPM_BUILD_ROOT/kabi-dwarf/whitelists/kabi-current/kabi_whitelist_%{_target_cpu}" \
                "$(pwd)" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Flavour:+.${Flavour}}.tmp" || :

            echo "**** kABI DWARF-based comparison report ****"
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh compare \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Flavour:+.${Flavour}}" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Flavour:+.${Flavour}}.tmp" || :
            echo "**** End of kABI DWARF-based comparison report ****"
        else
            echo "**** Baseline dataset for kABI DWARF-BASED comparison report not found ****"
        fi

        rm -rf $RPM_BUILD_ROOT/kabi-dwarf
    fi
%endif

    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/tracing
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/spdxcheck.py

    # Files for 'make scripts' to succeed with kernel-devel.
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/security/selinux/include
    cp -a --parents security/selinux/include/classmap.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents security/selinux/include/initial_sid_to_string.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/include/tools
    cp -a --parents tools/include/tools/be_byteshift.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/tools/le_byteshift.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    if [ -f tools/objtool/objtool ]; then
      cp -a tools/objtool/objtool $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
    fi
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    if [ -f arch/%{asmarch}/kernel/module.lds ]; then
      cp -a --parents arch/%{asmarch}/kernel/module.lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
%ifarch ppc64le
    cp -a --parents arch/powerpc/lib/crtsavres.[So] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
%ifarch aarch64
    # arch/arm64/include/asm/xen references arch/arm
    cp -a --parents arch/arm/include/asm/xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    # arch/arm64/include/asm/opcodes.h references arch/arm
    cp -a --parents arch/arm/include/asm/opcodes.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    # include the machine specific headers for ARM variants, if available.
%ifarch %{arm}
    if [ -d arch/%{asmarch}/mach-${Flavour}/include ]; then
      cp -a --parents arch/%{asmarch}/mach-${Flavour}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    # include a few files for 'make prepare'
    cp -a --parents arch/arm/tools/gen-mach-types $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/arm/tools/mach-types $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/

%endif
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
%ifarch i686 x86_64
    # files for 'make prepare' to succeed with kernel-devel
    cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscalltbl.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscallhdr.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_32.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_64.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_common.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents tools/include/tools/le_byteshift.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/purgatory.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/stack.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/setup-x86_64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/entry64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/ctype.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h

    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
    eu-readelf -n vmlinux | grep "Build ID" | awk '{print $NF}' > vmlinux.id
    cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id

    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
        LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      if [ ! -z "$3" ]; then
        sed -r -e "/^($3)\$/d" -i $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      fi
    }

    collect_modules_list networking \
      'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
      'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
    collect_modules_list drm \
      'drm_open|drm_init'
    collect_modules_list modesetting \
      'drm_crtc_init'

    # detect missing or incorrect license tags
    ( find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name '*.ko' | xargs /sbin/modinfo -l | \
        grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1

    # remove files that will be auto generated by depmod at rpm -i time
    pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
        rm -f modules.{alias*,builtin.bin,dep*,*map,symbols*,devname,softdep}
    popd

    # Identify modules in the kernel-modules-extras package
    %{SOURCE24} $RPM_BUILD_ROOT lib/modules/$KernelVer $RPM_SOURCE_DIR/mod-extra.list
    # Identify modules in the kernel-modules-extras package
    %{SOURCE24} $RPM_BUILD_ROOT lib/modules/$KernelVer %{SOURCE54} internal

    #
    # Generate the kernel-core and kernel-modules files lists
    #

    # Copy the System.map file for depmod to use, and create a backup of the
    # full module tree so we can restore it after we're done filtering
    cp System.map $RPM_BUILD_ROOT/.
    pushd $RPM_BUILD_ROOT
    mkdir restore
    cp -r lib/modules/$KernelVer/* restore/.

    # don't include anything going into kernel-modules-extra in the file lists
    xargs rm -rf < mod-extra.list
    # don't include anything going int kernel-modules-internal in the file lists
    xargs rm -rf < mod-internal.list


    if [ $DoModules -eq 1 ]; then
    # Find all the module files and filter them out into the core and
    # modules lists.  This actually removes anything going into -modules
    # from the dir.
    find lib/modules/$KernelVer/kernel -name *.ko | sort -n > modules.list
    cp $RPM_SOURCE_DIR/filter-*.sh .
    ./filter-modules.sh modules.list %{_target_cpu}
    rm filter-*.sh

    # Run depmod on the resulting module tree and make sure it isn't broken
    depmod -b . -aeF ./System.map $KernelVer &> depmod.out
    if [ -s depmod.out ]; then
        echo "Depmod failure"
        cat depmod.out
        exit 1
    else
        rm depmod.out
    fi
    else
    # Ensure important files/directories exist to let the packaging succeed
    echo '%%defattr(-,-,-)' > modules.list
    echo '%%defattr(-,-,-)' > k-d.list
    mkdir -p lib/modules/$KernelVer/kernel
    # Add files usually created by make modules, needed to prevent errors
    # thrown by depmod during package installation
    touch lib/modules/$KernelVer/modules.order
    touch lib/modules/$KernelVer/modules.builtin
    fi

    # remove files that will be auto generated by depmod at rpm -i time
    pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
        rm -f modules.{alias*,builtin.bin,dep*,*map,symbols*,devname,softdep}
    popd

    # Go back and find all of the various directories in the tree.  We use this
    # for the dir lists in kernel-core
    find lib/modules/$KernelVer/kernel -mindepth 1 -type d | sort -n > module-dirs.list

    # Cleanup
    rm System.map
    cp -r restore/* lib/modules/$KernelVer/.
    rm -rf restore
    popd

    # Make sure the files lists start with absolute paths or rpmbuild fails.
    # Also add in the dir entries
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/k-d.list > ../kernel${Flavour:+-${Flavour}}-modules.list
    sed -e 's/^lib*/%dir \/lib/' %{?zipsed} $RPM_BUILD_ROOT/module-dirs.list > ../kernel${Flavour:+-${Flavour}}-core.list
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/modules.list >> ../kernel${Flavour:+-${Flavour}}-core.list
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/mod-extra.list >> ../kernel${Flavour:+-${Flavour}}-modules-extra.list
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/mod-internal.list >> ../kernel${Flavour:+-${Flavour}}-modules-internal.list

    # Cleanup
    rm -f $RPM_BUILD_ROOT/k-d.list
    rm -f $RPM_BUILD_ROOT/modules.list
    rm -f $RPM_BUILD_ROOT/module-dirs.list
    rm -f $RPM_BUILD_ROOT/mod-extra.list
    rm -f $RPM_BUILD_ROOT/mod-internal.list

%if %{signmodules}
    if [ $DoModules -eq 1 ]; then
    # Save the signing keys so we can sign the modules in __modsign_install_post
    cp certs/signing_key.pem certs/signing_key.pem.sign${Flav}
    cp certs/signing_key.x509 certs/signing_key.x509.sign${Flav}
    fi
%endif

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir

    # This is going to create a broken link during the build, but we don't use
    # it after this point.  We need the link to actually point to something
    # when kernel-devel is installed, and a relative link doesn't work across
    # the F17 UsrMove feature.
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -delete

    # build a BLS config for this kernel
    %{SOURCE53} "$KernelVer" "$RPM_BUILD_ROOT" "%{?variant}"

    # Red Hat UEFI Secure Boot CA cert, which can be used to authenticate the kernel
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer
    %ifarch x86_64 aarch64
        install -m 0644 %{secureboot_ca_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca-20200609.cer
        install -m 0644 %{secureboot_ca_1} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca-20140212.cer
        ln -s kernel-signing-ca-20200609.cer $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
    %else
        install -m 0644 %{secureboot_ca_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
    %endif
    %ifarch s390x ppc64le
    if [ $DoModules -eq 1 ]; then
    if [ -x /usr/bin/rpm-sign ]; then
        install -m 0644 %{secureboot_key_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
    else
        install -m 0644 certs/signing_key.x509.sign${Flav} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
        openssl x509 -in certs/signing_key.pem.sign${Flav} -outform der -out $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
        chmod 0644 $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
    fi
    fi
    %endif

%if %{with_ipaclones}
    MAXPROCS=$(echo %{?_smp_mflags} | sed -n 's/-j\s*\([0-9]\+\)/\1/p')
    if [ -z "$MAXPROCS" ]; then
        MAXPROCS=1
    fi
    if [ "$Flavour" == "" ]; then
        mkdir -p $RPM_BUILD_ROOT/$DevelDir-ipaclones
        find . -name '*.ipa-clones' | xargs -i{} -r -n 1 -P $MAXPROCS install -m 644 -D "{}" "$RPM_BUILD_ROOT/$DevelDir-ipaclones/{}"
    fi
%endif

}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd linux-%{KVERREL}


%if %{with_debug}
BuildKernel %make_target %kernel_image %{_use_vdso} debug
%endif

%if %{with_zfcpdump}
BuildKernel %make_target %kernel_image %{_use_vdso} zfcpdump
%endif

%if %{with_pae}
BuildKernel %make_target %kernel_image %{use_vdso} lpae
%endif

%if %{with_up}
BuildKernel %make_target %kernel_image %{_use_vdso}
%endif

%if %{with_selftests}
%{make} -s ARCH=$Arch V=1 samples/bpf/
pushd tools/testing/selftests
# We need to install here because we need to call make with ARCH set which
# doesn't seem possible to do in the install section.
%{make} -s ARCH=$Arch V=1 TARGETS="bpf livepatch net" INSTALL_PATH=%{buildroot}%{_libexecdir}/kselftests install
popd
%endif

%if %{with_doc}
# Make the HTML pages.
make LD=ld.bfd PYTHON=/usr/bin/python3 htmldocs || %{doc_build_fail}

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w
%endif

# In the modsign case, we do 3 things.  1) We check the "flavour" and hard
# code the value in the following invocations.  This is somewhat sub-optimal
# but we're doing this inside of an RPM macro and it isn't as easy as it
# could be because of that.  2) We restore the .tmp_versions/ directory from
# the one we saved off in BuildKernel above.  This is to make sure we're
# signing the modules we actually built/installed in that flavour.  3) We
# grab the arch and invoke mod-sign.sh command to actually sign the modules.
#
# We have to do all of those things _after_ find-debuginfo runs, otherwise
# that will strip the signature off of the modules.
#
# Don't sign modules for the zfcpdump flavour as it is monolithic.

%define __modsign_install_post \
  if [ "%{signmodules}" -eq "1" ]; then \
    if [ "%{with_pae}" -ne "0" ]; then \
       %{modsign_cmd} certs/signing_key.pem.sign+lpae certs/signing_key.x509.sign+lpae $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+lpae/ \
    fi \
    if [ "%{with_debug}" -ne "0" ]; then \
      %{modsign_cmd} certs/signing_key.pem.sign+debug certs/signing_key.x509.sign+debug $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+debug/ \
    fi \
    if [ "%{with_up}" -ne "0" ]; then \
      %{modsign_cmd} certs/signing_key.pem.sign certs/signing_key.x509.sign $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/ \
    fi \
  fi \
  if [ "%{zipmodules}" -eq "1" ]; then \
    find $RPM_BUILD_ROOT/lib/modules/ -type f -name '*.ko' | %{SOURCE79} %{?_smp_mflags}; \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}

%ifnarch noarch
%global __debug_package 1
%files -f debugfiles.list debuginfo-common-%{_target_cpu}
%endif

%endif

# We don't want to package debuginfo for self-tests and samples but
# we have to delete them to avoid an error messages about unpackaged
# files.
# Delete the debuginfo for kernel-devel files
%define __remove_unwanted_dbginfo_install_post \
  if [ "%{with_selftests}" -ne "0" ]; then \
    rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/libexec/ksamples; \
    rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/libexec/kselftests; \
  fi \
  rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/src; \
%{nil}

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__remove_unwanted_dbginfo_install_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd linux-%{KVERREL}

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/kernel-doc-%{rpmversion}

# copy the source over
mkdir -p $docdir
tar -h -f - --exclude=man --exclude='.*' -c Documentation | tar xf - -C $docdir

# with_doc
%endif

# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

%if %{with_headers}
# Install kernel headers
%{__make} ARCH=%{hdrarch} LD=ld.bfd INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

%endif

%if %{with_cross_headers}
%if 0%{?fedora}
HDR_ARCH_LIST='arm arm64 powerpc s390 x86'
%else
HDR_ARCH_LIST='arm64 powerpc s390 x86'
%endif
mkdir -p $RPM_BUILD_ROOT/usr/tmp-headers

for arch in $HDR_ARCH_LIST; do
    mkdir $RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch}
    %{__make} ARCH=${arch} LD=ld.bfd INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch} headers_install
done

find $RPM_BUILD_ROOT/usr/tmp-headers \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

# Copy all the architectures we care about to their respective asm directories
for arch in $HDR_ARCH_LIST ; do
    mkdir -p $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include
    mv $RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch}/include/* $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include/
done

rm -rf $RPM_BUILD_ROOT/usr/tmp-headers
%endif

%if %{with_kernel_abi_whitelists}
# kabi directory
INSTALL_KABI_PATH=$RPM_BUILD_ROOT/lib/modules/
mkdir -p $INSTALL_KABI_PATH
# install kabi releases directories
tar xjvf %{SOURCE300} -C $INSTALL_KABI_PATH
# with_kernel_abi_whitelists
%endif

%if %{with_selftests}
pushd samples
install -d %{buildroot}%{_libexecdir}/ksamples
# install bpf samples
pushd bpf
install -d %{buildroot}%{_libexecdir}/ksamples/bpf
find -type f -executable -exec install -m755 {} %{buildroot}%{_libexecdir}/ksamples/bpf \;
install -m755 *.sh %{buildroot}%{_libexecdir}/ksamples/bpf
# test_lwt_bpf.sh compiles test_lwt_bpf.c when run; this works only from the
# kernel tree. Just remove it.
rm %{buildroot}%{_libexecdir}/ksamples/bpf/test_lwt_bpf.sh
install -m644 tcp_bpf.readme %{buildroot}%{_libexecdir}/ksamples/bpf
popd
# install pktgen samples
pushd pktgen
install -d %{buildroot}%{_libexecdir}/ksamples/pktgen
find . -type f -executable -exec install -m755 {} %{buildroot}%{_libexecdir}/ksamples/pktgen/{} \;
find . -type f ! -executable -exec install -m644 {} %{buildroot}%{_libexecdir}/ksamples/pktgen/{} \;
popd
popd
# install drivers/net/mlxsw selftests
pushd tools/testing/selftests/drivers/net/mlxsw
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
popd
# install net/forwarding selftests
pushd tools/testing/selftests/net/forwarding
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
popd
# install tc-testing selftests
pushd tools/testing/selftests/tc-testing
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
popd
# install livepatch selftests
pushd tools/testing/selftests/livepatch
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/livepatch/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/livepatch/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/livepatch/{} \;
popd
%endif

# We have to do the headers checksum calculation after the tools install because
# these might end up installing their own set of headers on top of kernel's
%if %{with_headers}
# compute a content hash to export as Provides: kernel-headers-checksum
HEADERS_CHKSUM=$(export LC_ALL=C; find $RPM_BUILD_ROOT/usr/include -type f -name "*.h" \
			! -path $RPM_BUILD_ROOT/usr/include/linux/version.h | \
		 sort | xargs cat | sha1sum - | cut -f 1 -d ' ');
# export the checksum via usr/include/linux/version.h, so the dynamic
# find-provides can grab the hash to update it accordingly
echo "#define KERNEL_HEADERS_CHECKSUM \"$HEADERS_CHKSUM\"" >> $RPM_BUILD_ROOT/usr/include/linux/version.h
%endif

###
### clean
###

###
### scripts
###

#
# This macro defines a %%post script for a kernel*-devel package.
#    %%kernel_devel_post [<subpackage>]
# Note we don't run hardlink if ostree is in use, as ostree is
# a far more sophisticated hardlink implementation.
# https://github.com/projectatomic/rpm-ostree/commit/58a79056a889be8814aa51f507b2c7a4dccee526
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink -a ! -e /run/ostree-booted ] \
then\
    (cd /usr/src/kernels/%{KVERREL}%{?1:+%{1}} &&\
     /usr/bin/find . -type f | while read f; do\
       hardlink -c /usr/src/kernels/*%{?dist}.*/$f $f\
     done)\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-extra package.
# It also defines a %%postun script that does the same thing.
#    %%kernel_modules_extra_post [<subpackage>]
#
%define kernel_modules_extra_post() \
%{expand:%%post %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-internal package.
# It also defines a %%postun script that does the same thing.
#    %%kernel_modules_internal_post [<subpackage>]
#
%define kernel_modules_internal_post() \
%{expand:%%post %{?1:%{1}-}modules-internal}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-internal}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules package.
# It also defines a %%postun script that does the same thing.
#    %%kernel_modules_post [<subpackage>]
#
%define kernel_modules_post() \
%{expand:%%post %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

# This macro defines a %%posttrans script for a kernel package.
#    %%kernel_variant_posttrans [<subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans() \
%{expand:%%posttrans %{?1:%{1}-}core}\
%if 0%{!?fedora:1}\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --add-kernel %{KVERREL}%{?1:+%{1}} || exit $?\
fi\
%endif\
/bin/kernel-install add %{KVERREL}%{?1:+%{1}} /lib/modules/%{KVERREL}%{?1:+%{1}}/vmlinuz || exit $?\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#    %%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:r:) \
%{expand:%%kernel_devel_post %{?-v*}}\
%{expand:%%kernel_modules_post %{?-v*}}\
%{expand:%%kernel_modules_extra_post %{?-v*}}\
%{expand:%%kernel_modules_internal_post %{?-v*}}\
%{expand:%%kernel_variant_posttrans %{?-v*}}\
%{expand:%%post %{?-v*:%{-v*}-}core}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#    %%kernel_variant_preun <subpackage>
#
%define kernel_variant_preun() \
%{expand:%%preun %{?1:%{1}-}core}\
/bin/kernel-install remove %{KVERREL}%{?1:+%{1}} /lib/modules/%{KVERREL}%{?1:+%{1}}/vmlinuz || exit $?\
%if 0%{!?fedora:1}\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --remove-kernel %{KVERREL}%{?1:+%{1}} || exit $?\
fi\
%endif\
%{nil}

%kernel_variant_preun
%kernel_variant_post -r kernel-smp

%if %{with_pae}
%kernel_variant_preun lpae
%kernel_variant_post -v lpae -r (kernel|kernel-smp)
%endif

%kernel_variant_preun debug
%kernel_variant_post -v debug

%if %{with_zfcpdump}
%kernel_variant_preun zfcpdump
%kernel_variant_post -v zfcpdump
%endif

if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

###
### file lists
###

%if %{with_headers}
%files headers
/usr/include/*
%endif

%if %{with_cross_headers}
%files cross-headers
/usr/*-linux-gnu/include/*
%endif

%if %{with_kernel_abi_whitelists}
%files -n kernel-abi-whitelists
/lib/modules/kabi-*
%endif

%if %{with_kabidw_base}
%ifarch x86_64 s390x ppc64 ppc64le aarch64
%files kabidw-base
%defattr(-,root,root)
/kabidw-base/%{_target_cpu}/*
%endif
%endif

# only some architecture builds need kernel-doc
%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}
%endif

%if %{with_selftests}
%files selftests-internal
%{_libexecdir}/ksamples
%{_libexecdir}/kselftests
%endif

# empty meta-package
%ifnarch %nobuildarches noarch
%files
%endif

%if %{with_gcov}
%ifarch x86_64 s390x ppc64le aarch64
%files gcov
%{_builddir}
%endif
%endif

# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#    %%kernel_variant_files [-k vmlinux] <condition> <subpackage> <without_modules>
#
%define kernel_variant_files(k:) \
%if %{2}\
%{expand:%%files -f kernel-%{?3:%{3}-}core.list %{?1:-f kernel-%{?3:%{3}-}ldsoconf.list} %{?3:%{3}-}core}\
%{!?_licensedir:%global license %%doc}\
%license linux-%{KVERREL}/COPYING-%{version}-%{release}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}\
%ghost /%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/.vmlinuz.hmac \
%ghost /%{image_install_path}/.vmlinuz-%{KVERREL}%{?3:+%{3}}.hmac \
%ifarch %{arm} aarch64\
/lib/modules/%{KVERREL}%{?3:+%{3}}/dtb \
%ghost /%{image_install_path}/dtb-%{KVERREL}%{?3:+%{3}} \
%endif\
%attr(600,root,root) /lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
%ghost /boot/System.map-%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/symvers.gz\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
%ghost /boot/symvers-%{KVERREL}%{?3:+%{3}}.gz\
%ghost /boot/config-%{KVERREL}%{?3:+%{3}}\
%ghost /boot/initramfs-%{KVERREL}%{?3:+%{3}}.img\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}/kernel\
/lib/modules/%{KVERREL}%{?3:+%{3}}/build\
/lib/modules/%{KVERREL}%{?3:+%{3}}/source\
/lib/modules/%{KVERREL}%{?3:+%{3}}/updates\
/lib/modules/%{KVERREL}%{?3:+%{3}}/bls.conf\
%if 0%{!?fedora:1}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/weak-updates\
%endif\
%{_datadir}/doc/kernel-keys/%{KVERREL}%{?3:+%{3}}/kernel-signing-ca*.cer\
%ifarch s390x ppc64le\
%if 0%{!?4:1}\
%{_datadir}/doc/kernel-keys/%{KVERREL}%{?3:+%{3}}/%{signing_key_filename} \
%endif\
%endif\
%if %{1}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/vdso\
%endif\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.*\
%{expand:%%files -f kernel-%{?3:%{3}-}modules.list %{?3:%{3}-}modules}\
%{expand:%%files %{?3:%{3}-}devel}\
%defverify(not mtime)\
/usr/src/kernels/%{KVERREL}%{?3:+%{3}}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-extra.list %{?3:%{3}-}modules-extra}\
%config(noreplace) /etc/modprobe.d/*-blacklist.conf\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-internal.list %{?3:%{3}-}modules-internal}\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?3}.list %{?3:%{3}-}debuginfo}\
%endif\
%endif\
%if %{?3:1} %{!?3:0}\
%{expand:%%files %{3}}\
%endif\
%endif\
%{nil}

%kernel_variant_files %{_use_vdso} %{with_up}
%kernel_variant_files %{_use_vdso} %{with_debug} debug
%kernel_variant_files %{use_vdso} %{with_pae} lpae
%kernel_variant_files %{_use_vdso} %{with_zfcpdump} zfcpdump 1

%define kernel_variant_ipaclones(k:) \
%if %{1}\
%if %{with_ipaclones}\
%{expand:%%files %{?2:%{2}-}ipaclones-internal}\
%defattr(-,root,root)\
%defverify(not mtime)\
/usr/src/kernels/%{KVERREL}%{?2:+%{2}}-ipaclones\
%endif\
%endif\
%{nil}

%kernel_variant_ipaclones %{with_up}

# plz don't put in a version string unless you're going to tag
# and build.
#
#
%changelog
* Fri Jul 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.12-500.chinfo
- 5.7.12 - pf8

* Wed Jul 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.11-500.chinfo
- 5.7.11 - pf8

* Sun Jul 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.10-501.chinfo
- 5.7.10 - pf6

* Wed Jul 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.10-500.chinfo
- 5.7.10 - pf5

* Thu Jul 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.9-500.chinfo
- 5.7.9 - pf5

* Wed Jul 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.8-501.chinfo
- Revert some patches to try to fix kernelbz#207383
- f32 sync

* Thu Jul 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.8-500.chinfo
- 5.7.8 - pf4

* Thu Jul 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.7-500.chinfo
- 5.7.7 - pf4

* Wed Jun 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.6-500.chinfo
- 5.7.6 - pf3

* Mon Jun 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.5-500.chinfo
- 5.7.5 - pf3

* Thu Jun 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.4-500.chinfo
- 5.7.4 - pf3
- stabilization sync

* Wed Jun 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.3-500.chinfo
- 5.7.3 - pf3

* Thu Jun 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.2-500.chinfo
- 5.7.2 - pf1

* Sun Jun 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.0-500.chinfo
- 5.7.0 - pf1

* Tue Jun 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.7.0-500.chinfo
- 5.7.0 - pf1
- Rawhide sync

* Wed May 27 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.15-500.chinfo
- 5.6.15 - pf8
- f32 sync

* Wed May 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.14-500.chinfo
- 5.6.14 - pf8
- f32 sync
- Disable gcc 10 workaround

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.13-500.chinfo
- 5.6.13 - pf7
- f32 sync

* Mon May 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.12-500.chinfo
- 5.6.12 - pf7

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.11-500.chinfo
- 5.6.11 - pf7

* Sat May 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.10-500.chinfo
- 5.6.10 - pf6

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.8-500.chinfo
- 5.6.8 - pf6
- f32 sync

* Thu Apr 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.7-500.chinfo
- 5.6.7 - pf5
- f32 sync

* Tue Apr 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.6-500.chinfo
- 5.6.6 - pf4

* Mon Apr 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.5-501.chinfo
- 5.6.5 - pf4

* Fri Apr 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.4-500.chinfo
- 5.6.5 - pf3
- f32 sync

* Mon Apr 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.4-500.chinfo
- 5.6.4 - pf3

* Wed Apr 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.3-500.chinfo
- 5.6.3 - pf3
- f32 sync

* Thu Apr 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.2-500.chinfo
- 5.6.2 - pf2

* Wed Apr 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.1-500.chinfo
- 5.6.1 - pf2

* Mon Mar 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.6.0-500.chinfo
- 5.6.0 - pf0
- Rawhide sync

* Wed Mar 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.13-500.chinfo
- 5.5.13 - pf8

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.11-500.chinfo
- 5.5.11 - pf8

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.10-500.chinfo
- 5.5.10 - pf7

* Thu Mar 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.9-500.chinfo
- 5.5.9 - pf7

* Thu Mar 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.8-500.chinfo
- 5.5.8 - pf6

* Sun Mar 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.7-500.chinfo
- 5.5.7 - pf6

* Mon Feb 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.6-500.chinfo
- 5.5.6 - pf6
- f31 sync

* Thu Feb 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.5-500.chinfo
- 5.5.5 - pf5

* Fri Feb 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.4-500.chinfo
- 5.5.4 - pf4

* Tue Feb 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.3-500.chinfo
- 5.5.3

* Tue Feb 04 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.2-500.chinfo
- 5.5.2
- stabilization sync

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.1-500.chinfo
- 5.5.1

* Fri Jan 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.0-501.chinfo
- 5.5.0 - pf2

* Tue Jan 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.5.0-500.chinfo
- 5.5.0
- Rawhide sync

* Sun Jan 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.14-500.chinfo
- 5.4.15

* Thu Jan 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.14-500.chinfo
- 5.4.14 - pf7

* Sat Jan 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.13-500.chinfo
- 5.4.13

* Wed Jan 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.12-500.chinfo
- 5.4.12 - pf6

* Mon Jan 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.11-500.chinfo
- 5.4.11

* Thu Jan 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.10-500.chinfo
- 5.4.10 - pf5
- f31 sync

* Sat Jan 04 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.8-500.chinfo
- 5.4.8

* Wed Jan 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.7-500.chinfo
- 5.4.7 - pf4

* Tue Dec 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.4.6-501.chinfo
- pf sync

* Sat Dec 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.4.6-500.chinfo
- 5.4.6

* Fri Dec 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.4.5-500.chinfo
- 5.4.5

* Fri Dec 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.4.3-500.chinfo
- 5.4.3
- stabilization sync

* Thu Dec 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.4.2-500.chinfo
- 5.4.2
- stabilization sync

* Fri Nov 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.4.1-500.chinfo
- 5.4.1 - pf2

* Mon Nov 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.4.0-500.chinfo
- 5.4.0 - pf1
- Rawhide sync

* Sun Nov 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.13-500.chinfo
- 5.3.13
- f31 sync

* Thu Nov 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.12-500.chinfo
- 5.3.12 - pf9

* Thu Nov 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.11-502.chinfo
- pf8, BFQ fix
- Add some openSUSE patches

* Wed Nov 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.11-501.chinfo
- Revert bfq patch

* Tue Nov 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.11-500.chinfo
- 5.3.11 - pf7
- f31 sync

* Sun Nov 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.10-500.chinfo
- 5.3.10

* Wed Nov 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.9-500.chinfo
- 5.3.9 - pf6

* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.8-500.chinfo
- 5.3.8 - pf5

* Fri Oct 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.7-500.chinfo
- 5.3.7
- f31 sync

* Mon Oct 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.6-500.chinfo
- 5.3.6 - pf4

* Mon Oct 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.5-500.chinfo
- 5.3.5

* Sat Oct 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.4-500.chinfo
- 5.3.4

* Tue Oct 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.2-500.chinfo
- 5.3.2
- f31 sync

* Sun Sep 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.1-501.chinfo
- Add some patchwork amdgpu bits

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.1-500.chinfo
- 5.3.1 - pf2
- f31 sync

* Mon Sep 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.0-500.chinfo
- 5.3.0 - pf1
- Rawhide sync

* Thu Sep 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.14-501.chinfo
- Try some amdgpu patches

* Tue Sep 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.14-500.chinfo
- 5.2.14

* Fri Sep 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.13-500.chinfo
- 5.2.13 - pf8

* Thu Aug 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.11-500.chinfo
- 5.2.11

* Mon Aug 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.10-500.chinfo
- 5.2.10 - pf7

* Fri Aug 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.9-500.chinfo
- 5.2.9 - pf6

* Fri Aug 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.8-500.chinfo
- 5.2.8
- Experimental fsync patch

* Wed Aug 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.7-501.chinfo
- BFQ updates

* Tue Aug 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.7-500.chinfo
- 5.2.7

* Sun Aug 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.6-500.chinfo
- 5.2.6

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.5-500.chinfo
- 5.2.5
- f30 sync

* Mon Jul 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.4-500.chinfo
- 5.2.4

* Sun Jul 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.21-500.chinfo
- 5.1.21

* Fri Jul 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.20-500.chinfo
- 5.1.20

* Sun Jul 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.19-500.chinfo
- 5.1.19

* Sun Jul 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.18-500.chinfo
- 5.1.18

* Wed Jul 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.17-500.chinfo
- 5.1.17
- Option to apply stable patches over pf

- f30 sync
* Wed Jul 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.16-500.chinfo
- 5.1.16 - pf8
- f30 sync

* Tue Jun 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.15-500.chinfo
- 5.1.15

* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.14-500.chinfo
- 5.1.14

* Wed Jun 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.12-500.chinfo
- 5.1.12

* Mon Jun 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.11-500.chinfo
- 5.1.11

* Sun Jun 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.10-500.chinfo
- 5.1.10

* Tue Jun 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.9-500.chinfo
- 5.1.9
- f30 sync

* Sun Jun 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.8-500.chinfo
- 5.1.8 - pf6
- f30 sync

* Tue Jun 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.7-500.chinfo
- 5.1.7
- f30 sync

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.6-500.chinfo
- 5.1.6
- f30 sync

* Sat May 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.5-500.chinfo
- 5.1.5

* Fri May 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.4-501.chinfo
- pf4

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.4-500.chinfo
- 5.1.4

* Thu May 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.3-500.chinfo
- 5.1.3 - pf3

* Tue May 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.2-500.chinfo
- 5.1.2

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.1-500.chinfo
- 5.1.1 -pf2

* Wed May 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.0-501.chinfo
- Disable UKSM

* Mon May 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.0-500.chinfo
- 5.1.0 - pf1
- Rawhide sync

###
# The following Emacs magic makes C-c C-e use UTC dates.
# Local Variables:
# rpm-change-log-uses-utc: t
# End:
###
