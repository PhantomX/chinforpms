#!/bin/bash

# This scripts sets extra files with configs for external patchsets
# del parameter deletes all the files
# pf parameter for post_factum patchset
# zen parameter for zen patchset
# nothing for Graysky cpu patch

# 20230425
# 6.3
# pf1

set -e

default="
MALDERLAKE
MBARCELONA
MBOBCAT
MBROADWELL
MBULLDOZER
MCANNONLAKE
MCASCADELAKE
MCOOPERLAKE
MEXCAVATOR
GENERIC_CPU2
GENERIC_CPU3
GENERIC_CPU4
MGOLDMONT
MGOLDMONTPLUS
MHASWELL
MICELAKE
MIVYBRIDGE
MJAGUAR
MK10
MK8SSE3
MNEHALEM
MPILEDRIVER
MROCKETLAKE
MSANDYBRIDGE
MSAPPHIRERAPIDS
MSILVERMONT
MSKYLAKE
MSKYLAKEX
MSTEAMROLLER
MTIGERLAKE
MWESTMERE
MZEN
MZEN2
MZEN3
MNATIVE_AMD
MNATIVE_INTEL
RHEL_DIFFERENCES
"

pf="
CC_OPTIMIZE_FOR_PERFORMANCE_O3
"

pfd="
"

pfm="
BACKLIGHT_DDCCI
DDCCI
TCP_CONG_BBR2
V4L2_LOOPBACK
"

pfv="
SCHED_TIMESLICE=4
"

pfy="
SCHED_BMQ
USER_NS_UNPRIVILEGED
"

SCRIPT="$(readlink -f $0)"
SCRIPT_DIR="$(dirname ${SCRIPT})"
CONFIG_DIR="${SCRIPT_DIR}/configs/fedora"
OUTPUT_DIR="${CONFIG_DIR}/generic"
DEBUG_DIR="${CONFIG_DIR}/debug"

cd "${SCRIPT_DIR}"

del(){
  for i in ${default} ${pf} ${pfm} ${pfv} ${pfy} ${zen} ${zenv} ${zeny}
  do
    if [ -e "${OUTPUT_DIR}/CONFIG_${i%%=*}" ] ;then
      rm -fv "${OUTPUT_DIR}/CONFIG_${i%%=*}"
    fi
  done
  for i in ${pfd}
  do
    if [ -e "${OUTPUT_DIR}/CONFIG_${i%%=*}" ] ;then
      rm -fv "${DEBUG_DIR}/CONFIG_${i%%=*}"
    fi
  done
}

main(){
  del
  for i in ${default} ${pf}
  do
    echo "# CONFIG_${i} is not set" > "${OUTPUT_DIR}/CONFIG_${i}"
  done
  for i in ${pfy}
  do
    echo "CONFIG_${i}=y" > "${OUTPUT_DIR}/CONFIG_${i}"
  done
  for i in ${pfm}
  do
    echo "CONFIG_${i}=m" > "${OUTPUT_DIR}/CONFIG_${i}"
  done
  for i in ${pfd}
  do
    echo "CONFIG_${i}=y" > "${DEBUG_DIR}/CONFIG_${i}"
  done
  for i in ${pfv}
  do
    echo "CONFIG_${i}" > "${OUTPUT_DIR}/CONFIG_${i%%=*}"
  done
}

if [ -w "${OUTPUT_DIR}" ] ;then
  case "$1" in
    del)
      del
      ;;
    pf)
      main
      ;;
    *)
      pf=
      pfd=
      pfm=
      pfv=
      pfy=
      main
      ;;
  esac

  ./build_configs.sh kernel-chinfo
fi
