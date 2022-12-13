#!/bin/bash

# This scripts sets extra files with configs for external patchsets
# del parameter deletes all the files
# pf parameter for post_factum patchset
# zen parameter for zen patchset
# nothing for Graysky cpu patch

# 20221212
# 6.1
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
LRNG
LRNG_COLLECTION_SIZE_32
LRNG_COLLECTION_SIZE_256
LRNG_COLLECTION_SIZE_512
LRNG_COLLECTION_SIZE_2048
LRNG_COLLECTION_SIZE_4096
LRNG_COLLECTION_SIZE_8192
LRNG_CONTINUOUS_COMPRESSION_DISABLED
LRNG_CPU
LRNG_DEV_IF
LRNG_DFLT_DRNG_CHACHA20
LRNG_DFLT_DRNG_KCAPI
LRNG_DRNG_SWITCH
LRNG_IRQ_DFLT_TIMER_ES
LRNG_SCHED_DFLT_TIMER_ES
LRNG_HWRAND_IF
LRNG_IRQ
LRNG_HASH_KCAPI
LRNG_HEALTH_TESTS
LRNG_JENT
LRNG_KCAPI_IF
LRNG_OVERSAMPLE_ENTROPY_SOURCES
LRNG_RUNTIME_ES_CONFIG
LRNG_SCHED
LRNG_SELFTEST
LRNG_SWITCHABLE_CONTINUOUS_COMPRESSION
LRNG_SWITCH_HASH
LRNG_SWITCH_DRBG
LRNG_SWITCH_DRNG
LRNG_SWITCH_DRNG_CHACHA20
LRNG_SWITCH_DRNG_KCAPI
LRNG_TESTING_MENU
"

pfd="
"

pfm="
TCP_CONG_BBR2
V4L2_LOOPBACK
"

pfv="
LRNG_CPU_ENTROPY_RATE=8
LRNG_IRQ_ENTROPY_RATE=256
LRNG_JENT_ENTROPY_RATE=16
LRNG_SCHED_ENTROPY_RATE=256
SCHED_TIMESLICE=4
"

pfy="
RANDOM_DEFAULT_IMPL
LRNG_COLLECTION_SIZE_1024
LRNG_CONTINUOUS_COMPRESSION_ENABLED
LRNG_DFLT_DRNG_DRBG
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

  ./build_configs.sh
fi
