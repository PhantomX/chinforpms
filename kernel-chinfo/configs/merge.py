#!/usr/bin/python3
# SPDX-License-Identifier: GPL-2.0
# Author: Clark Williams <williams@redhat.com>
# Copyright (C) 2022 Red Hat, Inc.
#
# merge.py - a direct replacement for merge.pl in the redhat/configs directory
#
# invocation:   python merge.py overrides baseconfig
#
# Both input files are kernel config files, where overides is config overides
# to the baseconfig file. Both are read into python dictionaries with the
# keys being the config name and the values being the config file text

# The script iterates through the overrides keys adding/replacing the contents
# of the baseconfig values and then outputs the new baseconfig to stdout.
#

import sys
import os.path

def usage(msg):
    print(msg)
    print("usage: merge.py overrides baseconfig")
    sys.exit(1)

# read a config file and return a dictionary of the contents
def read_config_file(cfgfile):
    configs = {}
    with open(cfgfile) as f:
        for l in [n.strip() for n in f.readlines()]:
            if not l:  continue
            if l.startswith("# CONFIG_"):
                configs[l.split()[1]] = l
                continue
            if l.startswith("CONFIG_"):
                configs[l.split('=')[0]] = l
                continue
    return configs


if len(sys.argv) < 3: usage("must have two input files")

# read in the overides file
if not os.path.exists(sys.argv[1]):
    usage("overrides config file %s does not exist!" % sys.argv[1])
overrides = read_config_file(sys.argv[1])

# read in the base config file
if not os.path.exists(sys.argv[2]):
    usage("base config file %s does not exist!" % sys.argv[2])
baseconfigs = read_config_file(sys.argv[2])

# update baseconfigs with the overrides values
baseconfigs.update(overrides)

# print the new config to stdout
for v in baseconfigs.values():
    print(v)
