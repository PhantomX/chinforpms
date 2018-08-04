#!/bin/bash
#
# This script is aimed at generating the headers from the kernel sources.
# Please do a git checkout of the kernel sources, or run until %prep step of
# kernel rpm build. Then go into the directory with the sources, and run this
# script
#
# Author: Herton R. Krzesinski <herton@redhat.com>

# ARCH_LIST below has the default list of supported architectures
# (the architectures names may be different from rpm, you list here the
# names of arch/<arch> directories in the kernel sources)
ARCH_LIST="arm arm64 powerpc s390 x86"

# If the kernel Makefile doesn't contain enough information for the tarball
# release, you can specify the release of the package so it'll be included
# in the name of the created tarball
TB_RELEASE="1"

# If kernel Makefile has the package release number, you can specify the name of
# Makefile variable here.
MAKE_RELEASE=""

# Extra string (usually dist tag) that goes into the tarball name
EXTRA=""

while [ ! -z "$1" ]; do
	opt="$1"
	case $opt in
		--arch-list|-a)
			ARCH_LIST="$2"
			shift
			;;
		--extra|-e)
			EXTRA="$2"
			shift
			;;
		--make-release|-m)
			MAKE_RELEASE=$2
			shift
			;;
		--release|-r)
			TB_RELEASE=$2
			shift
			;;
		*)
			echo "Unknown option ($1) to $0"
			exit
			;;
	esac
	shift
done

KVERSION=$(cat Makefile | sed -ne '/^VERSION\ =\ /{s///;p;q}')
KPATCHLEVEL=$(cat Makefile | sed -ne '/^PATCHLEVEL\ =\ /{s///;p;q}')
KSUBLEVEL=$(cat Makefile | sed -ne '/^SUBLEVEL\ =\ /{s///;p;q}')
TB_VERSION=$KVERSION.$KPATCHLEVEL.$KSUBLEVEL
if [ -z "$TB_RELEASE" ]; then
	KEXTRAVERSION=$(cat Makefile | sed -ne '/^EXTRAVERSION\ =\ /{s///;p;q}')
	DISTRO_RELEASE=""
	if [ -n "$MAKE_RELEASE" ]; then
		DISTRO_RELEASE=.$(cat Makefile | sed -ne "/^$MAKE_RELEASE\ =\ /{s///;p;q}")
	fi
	if [ -n "$KEXTRAVERSION" ]; then
		KEXTRAVERSION=$(echo $KEXTRAVERSION | sed -e s/-/./)
		TB_RELEASE=0$KEXTRAVERSION$DISTRO_RELEASE$EXTRA
	else
		TB_RELEASE=$DISTRO_RELEASE$EXTRA
	fi
fi

headers_dir=$(mktemp -d)
trap 'rm -rf "$headers_dir"' SIGHUP SIGINT SIGTERM EXIT

make HDR_ARCH_LIST="$ARCH_LIST" INSTALL_HDR_PATH=$headers_dir headers_install_all
find $headers_dir \
	\( -name .install -o -name .check -o \
	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

TARBALL=$PWD/kernel-headers-$TB_VERSION-$TB_RELEASE.tar.xz
pushd $headers_dir
	tar -Jcf $TARBALL *
popd

echo wrote $TARBALL
