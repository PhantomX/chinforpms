#!/usr/bin/bash

set -e

DUCKSTATIONDIR="_RPM_DATADIR_"

if [[ "${XDG_CONFIG_HOME}" ]] ;then
  DUCKSTATIONHOME="${XDG_CONFIG_HOME}/duckstation"
else
  DUCKSTATIONHOME="${HOME}/.local/share/duckstation"
fi

shopt -s nullglob

mkdir -p "${DUCKSTATIONDIR}"

pushd "${DUCKSTATIONDIR}" >/dev/null 2>&1
while read -r file
do
  if ! [[ -e "${DUCKSTATIONHOME}/${file}" ]] ;then
    install -D "${file}" -pm0644 "${DUCKSTATIONHOME}/${file}" >/dev/null 2>&1
  fi
done < <(find inputprofiles -type f)
popd >/dev/null 2>&1

exec "${BASH_SOURCE[0]}.bin" "$@"
