#!/bin/bash

# This scripts sets extra files with configs for external patchsets
# del parameter deletes all the files
# pf parameter for post_factum patchset
# zen parameter for zen patchset
# nothing for Graysky cpu patch

# 20250420
# 6.14

set -e

default="
LONGEST_SYM_KUNIT_TEST
MALDERLAKE
MAMD_CPU_V2
MAMD_CPU_V3
MAMD_CPU_V4
MBARCELONA
MBOBCAT
MBROADWELL
MBULLDOZER
MCANNONLAKE
MCASCADELAKE
MCOOPERLAKE
MEMERALDRAPIDS
MEXCAVATOR
MGOLDMONT
MGOLDMONTPLUS
MHASWELL
MICELAKE_CLIENT
MICELAKE_SERVER
MINTEL_CPU_V2
MINTEL_CPU_V3
MINTEL_CPU_V4
MIVYBRIDGE
MJAGUAR
MK10
MK8SSE3
MMETEORLAKE
MNEHALEM
MPILEDRIVER
MRAPTORLAKE
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
MZEN4
MZEN5
MNATIVE_AMD
MNATIVE_INTEL
RHEL_DIFFERENCES
"

defaultd="
"

defaultm="
OVPN
OVPN_DCO_V2
V4L2_LOOPBACK
VHBA
"

defaultv="
X86_64_VERSION=1
"

defaulty="
CPU_IDLE_GOV_MENU
CONFIG_CPU_IDLE_GOV_TEO
USER_NS_UNPRIVILEGED
"

SCRIPT="$(readlink -f $0)"
SCRIPT_DIR="$(dirname ${SCRIPT})"
CONFIG_DIR="${SCRIPT_DIR}/configs/custom-overrides"
OUTPUT_DIR="${CONFIG_DIR}/generic"
DEBUG_DIR="${CONFIG_DIR}/debug"

cd "${SCRIPT_DIR}"

del(){
  for i in ${default} ${defaultm} ${defaulty}
  do
    if [ -n "${i}" ] && [ -e "${OUTPUT_DIR}/CONFIG_${i%%=*}" ] ;then
      rm -fv "${OUTPUT_DIR}/CONFIG_${i%%=*}"
    fi
  done
  for i in ${defaultd}
  do
    if [ -n "${i}" ] && [ -e "${OUTPUT_DIR}/CONFIG_${i%%=*}" ] ;then
      rm -fv "${DEBUG_DIR}/CONFIG_${i%%=*}"
    fi
  done
}

main(){
  del
  for i in ${default}
  do
    if [ -n "${i}" ] ;then
      echo "# CONFIG_${i} is not set" > "${OUTPUT_DIR}/CONFIG_${i}"
    fi
  done
  for i in ${defaulty}
  do
    if [ -n "${i}" ] ;then
      echo "CONFIG_${i}=y" > "${OUTPUT_DIR}/CONFIG_${i}"
    fi
  done
  for i in ${defaultm}
  do
    if [ -n "${i}" ] ;then
      echo "CONFIG_${i}=m" > "${OUTPUT_DIR}/CONFIG_${i}"
    fi
  done
  for i in ${defaultd}
  do
    if [ -n "${i}" ] ;then
      echo "CONFIG_${i}=y" > "${DEBUG_DIR}/CONFIG_${i}"
    fi
  done
  for i in ${defaultv}
  do
    if [ -n "${i}" ] ;then
      echo "CONFIG_${i}" > "${OUTPUT_DIR}/CONFIG_${i%%=*}"
    fi
  done
}

if [ -w "${OUTPUT_DIR}" ] ;then
  case "$1" in
    del)
      del
      ;;
    *)
      main
      ;;
  esac

  ./build_configs.sh kernel-chinfo
  grep -l '^# EMPTY' *.config | xargs rm -f
fi
