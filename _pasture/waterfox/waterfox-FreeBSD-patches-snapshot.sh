#!/bin/bash

set -e

module=$(basename "$0" -snapshot.sh)
snaproot="https://svn.freebsd.org/ports/head/www/waterfox/files"

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
  set +e
  ([ -z "${tmp}" ] || [ ! -d "${tmp}" ]) || rm -rf "${tmp}"
}

unset CDPATH
unset SNAP_COOPTS
pwd=$(pwd)
snap=${snap:-$(date +%Y%m%d)}

[ "${snap}" = "$(date +%Y%m%d)" ] || SNAP_COOPTS="-r {$snap}"
if [ -n "${rev}" ] ; then
  SNAP_COOPTS="-r ${rev}"
  snap="${rev}"
fi

pushd "${tmp}"
  svn co ${SNAP_COOPTS} ${snaproot} ${module}
  rev=$(svnversion "${module}")
  rev="${rev//[!0-9]/}"
  mv "${module}" "${module}-r${rev}"
  tar -Jcf "${pwd}/${module}-r${rev}.tar.xz" --exclude=.svn "${module}-r${rev}"
popd >/dev/null
