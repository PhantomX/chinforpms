#!/usr/bin/sh
OOO_ARCH=$(uname -m)
case $OOO_ARCH in
	x86_64 | s390x | sparc64 | aarch64)
		OOO_LIB_DIR="/usr/lib64"
		SECONDARY_LIB_DIR="/usr/lib"
		;;
	* )
		OOO_LIB_DIR="/usr/lib"
		SECONDARY_LIB_DIR="/usr/lib64"
		;;
esac
if [ ! -x $OOO_LIB_DIR/BRAND/program/LAUNCHER ]; then
    OOO_LIB_DIR="$SECONDARY_LIB_DIR"
fi
exec $OOO_LIB_DIR/BRAND/program/LAUNCHER "$@"
