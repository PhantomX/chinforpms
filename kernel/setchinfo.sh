#!/bin/bash

# This scripts sets extra files with configs for external patchsets
# del parameter deletes all the files
# pf parameter for post_factum patchset
# zen parameter for zen patchset
# nothing for Graysky cpu patch

# 20200618

set -e

default="
MBARCELONA
MBOBCAT
MBROADWELL
MBULLDOZER
MCANNONLAKE
MCASCADELAKE
MCOOPERLAKE
MEXCAVATOR
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
MSANDYBRIDGE
MSILVERMONT
MSKYLAKE
MSKYLAKEX
MSTEAMROLLER
MTIGERLAKE
MWESTMERE
MZEN
MZEN2
MNATIVE
"

pf="
CC_OPTIMIZE_HARDER
CC_OPTIMIZE_FOR_PERFORMANCE_O3
KERNEL_ZSTD
INITRAMFS_COMPRESSION_ZSTD
"

pfd="
"

pfv="
SCHED_TIMESLICE=4
"

pfy="
RD_ZSTD
SCHED_BMQ
STACKPROTECTOR_STRONG
USER_NS_UNPRIVILEGED
"

zen="
CC_OPTIMIZE_HARDER
RQ_NONE
RQ_MC
RQ_SMP
DEFAULT_BFQ_SQ
VHBA
LOGO_ZEN_CLUT224
LOGO_OLDZEN_CLUT224
LOGO_ARCH_CLUT224
LOGO_GENTOO_CLUT224
LOGO_EXHERBO_CLUT224
LOGO_SLACKWARE_CLUT224
LOGO_DEBIAN_CLUT224
LOGO_FEDORAGLOSSY_CLUT224
LOGO_TITS_CLUT224
LOGO_BSD_CLUT224
LOGO_FBSD_CLUT224
TP_SMAPI
"

zenv="
NR_TTY_DEVICES=63
"

zeny="
ZEN_INTERACTIVE
SCHED_MUQSS
SMT_NICE
RQ_SMT
IOSCHED_BFQ_SQ
BFQ_SQ_GROUP_IOSCHED
MQ_IOSCHED_BFQ
MQ_BFQ_GROUP_IOSCHED
LOGO_RANDOM
LOGO_FEDORASIMPLE_CLUT224
USER_NS_UNPRIVILEGED
"

SCRIPT="$(readlink -f $0)"
SCRIPT_DIR="$(dirname ${SCRIPT})"
CONFIG_DIR="${SCRIPT_DIR}/configs/fedora"
OUTPUT_DIR="${CONFIG_DIR}/generic"
DEBUG_DIR="${CONFIG_DIR}/debug"

cd "${SCRIPT_DIR}"

del(){
  for i in ${default} ${pf} ${pfv} ${pfy} ${zen} ${zenv} ${zeny}
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
  for i in ${default} ${pf} ${zen}
  do
    echo "# CONFIG_${i} is not set" > "${OUTPUT_DIR}/CONFIG_${i}"
  done
  for i in ${pfy} ${zeny}
  do
    echo "CONFIG_${i}=y" > "${OUTPUT_DIR}/CONFIG_${i}"
  done
  for i in ${pfd}
  do
    echo "CONFIG_${i}=y" > "${DEBUG_DIR}/CONFIG_${i}"
  done
  for i in ${pfv} ${zenv}
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
      zen=
      zeny=
      zenv=
      main
      ;;
    zen)
      pf=
      pfv=
      pfy=
      main
      ;;
    *)
      zen=
      zeny=
      zenv=
      pf=
      pfv=
      pfy=
      main
      ;;
  esac

  ./build_configs.sh
fi
