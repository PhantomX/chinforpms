#!/bin/bash

set -e

cpus="
MK8SSE3
MK10
MBARCELONA
MBOBCAT
MJAGUAR
MBULLDOZER
MPILEDRIVER
MSTEAMROLLER
MEXCAVATOR
MZEN
MNEHALEM
MWESTMERE
MSILVERMONT
MSANDYBRIDGE
MIVYBRIDGE
MHASWELL
MBROADWELL
MSKYLAKE
MSKYLAKEX
MCANNONLAKE
MICELAKE
MNATIVE
"

SCRIPT="$(readlink -f $0)"
SCRIPT_DIR="$(dirname ${SCRIPT})"
OUTPUT_DIR="${SCRIPT_DIR}/configs/fedora/generic"

cd "${SCRIPT_DIR}"

if [ -w "${OUTPUT_DIR}" ] ;then
  for i in ${cpus}
  do
    if [ "$1" = del ] ;then
      rm -fv "${OUTPUT_DIR}/CONFIG_${i}"
    else
      echo "# CONFIG_${i} is not set" > "${OUTPUT_DIR}/CONFIG_${i}"
    fi
  done
fi

./build_configs.sh
