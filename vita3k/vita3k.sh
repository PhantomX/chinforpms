#!/usr/bin/bash

set -e

VITA3KDIR="_RPM_DATADIR_"

if [[ "${XDG_DATA_HOME}" ]] ;then
  VITA3KHOME="${XDG_DATA_HOME}/Vita3K"
else
  VITA3KHOME="${HOME}/.local/share/Vita3K"
fi

shopt -s nullglob

mkdir -p "${VITA3KDIR}"

pushd "${VITA3KDIR}" >/dev/null 2>&1
while read -r file
do
  if ! [[ -e "${VITA3KHOME}/${file}" ]] ;then
    install -D "${file}" -pm0644 "${VITA3KHOME}/${file}" >/dev/null 2>&1
  fi
done < <(find shaders-builtin -type f)
popd >/dev/null 2>&1

exec "_RPM_BINDIR_/vita3k" "$@"

