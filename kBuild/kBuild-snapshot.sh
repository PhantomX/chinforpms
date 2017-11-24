#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
svn=$(date +%Y%m%d)

#cd "$tmp"
svn co http://svn.netlabs.org/repos/kbuild/trunk/ kBuild
revision=$(svnversion kBuild)
tar zcf kBuild-r$revision\.tar.gz --exclude=kBuild/bin --exclude=.svn kBuild
rm -rf kBuild
#cd - >/dev/null
