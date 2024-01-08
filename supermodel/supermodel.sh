#!/usr/bin/bash

set -e

supermodeldir="_RPM_DATADIR_"
supermodelconfig="${HOME}/.config/supermodel"
supermodeldata="${HOME}/.local/share/supermodel"

shopt -s nullglob

mkdir -p "${supermodelconfig}"/Config
mkdir -p "${supermodeldata}"/Assets

find -L "${supermodelconfig}" -type l -delete
find -L "${supermodeldata}" -type l -delete

pushd "${supermodeldir}" >/dev/null 2>&1
while read -r file
do
  if ! [[ -e "${supermodeldata}/${file}" ]] ;then
    ln -s "${supermodeldir}/${file}" "${supermodeldata}/${file}" >/dev/null 2>&1
  fi
done < <(find Assets -type f)

while read -r file
do
  if ! [[ -e "${supermodelconfig}/${file}" ]] ;then
    install -D -pm0644 "${file}" "${supermodelconfig}/${file}" >/dev/null 2>&1
  fi
done < <(find Config/*.ini -type f)

while read -r file
do
  if ! [[ -e "${supermodelconfig}/${file}" ]] ;then
    ln -s "${supermodeldir}/${file}" "${supermodelconfig}/${file}" >/dev/null 2>&1
  fi
done < <(find Config/*.xml -type f)
popd >/dev/null 2>&1

exec "_RPM_LIBEXECPATH_" "$@"
