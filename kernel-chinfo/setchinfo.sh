#!/bin/bash

# This scripts sets extra files with configs for external patchsets
# del parameter deletes all the files

# 20260209
# 6.19

set -e

default="
CPU_IDLE_GOV_MENU
MNATIVE_AMD
MNATIVE_INTEL
RHEL_DIFFERENCES
SND_INTEL_BYT_PREFER_SOF
"

defaultd="
"

defaultm="
V4L2_LOOPBACK
VHBA
"

defaultv="
SND_HDA_POWER_SAVE_DEFAULT=0
X86_64_ISA_LEVEL=1
"

defaulty="
ACPI_TABLE_UPGRADE
CPU_IDLE_GOV_TEO
DRM_AMDGPU_SI
EFI_VARS_PSTORE_DEFAULT_DISABLE
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
