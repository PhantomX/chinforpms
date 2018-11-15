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

pf="
KSM_LEGACY
"
pfy="
SCHED_PDS
UKSM
SMT_NICE
"

if [ "$1" != "del" ] && [ "$1" != "pf" ] ;then
  pfs=
fi

SCRIPT="$(readlink -f $0)"
SCRIPT_DIR="$(dirname ${SCRIPT})"
OUTPUT_DIR="${SCRIPT_DIR}/configs/fedora/generic"

cd "${SCRIPT_DIR}"

if [ -w "${OUTPUT_DIR}" ] ;then
  if [ "$1" = "del" ] ;then
    for i in ${cpus} ${pf} ${pfy}
    do
      rm -fv "${OUTPUT_DIR}/CONFIG_${i}"
    done
  else
    for i in ${cpus} ${pf}
    do
      echo "# CONFIG_${i} is not set" > "${OUTPUT_DIR}/CONFIG_${i}"
    done
    for i in ${pfy}
    do
      echo "CONFIG_${i}=y" > "${OUTPUT_DIR}/CONFIG_${i}"
    done
  fi
fi

./build_configs.sh
