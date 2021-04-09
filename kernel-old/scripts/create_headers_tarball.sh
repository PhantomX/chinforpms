#!/bin/bash
#
# This script is aimed at generating the headers from the kernel sources.
# You should have a checkout of kernel-headers inside the kernel directory 'fedpkg clone kernel-headers'
# You will need to prep the kernel sources with 'make prep' or 'fedpkg prep' before running this script
#
# Author: Herton R. Krzesinski <herton@redhat.com>
# Author: Justin M. Forbes <jforbes@redhat.com>

set -e

# Location of kernel-headers checkout
CURRENTDIR=`pwd`
PKGLOC='kernel-headers'

if [ ! -f $PKGLOC/kernel-headers.spec ]; then
	echo "Missing checkout of kernel-headers in $PKGLOC"
	exit 1
fi

# Kernel version information taken from kernel.spec and change to prepared sources directory
MAJORVER='5'
RELEASED=`grep "%global released_kernel" kernel.spec| cut -d ' ' -f 3`
BASERELEASE=`grep "%global baserelease" kernel.spec| cut -d ' ' -f 3`
BASE=`grep "%define base_sublevel" kernel.spec| cut -d ' ' -f 3`
STABLE=`grep "%define stable_update" kernel.spec| cut -d ' ' -f 3`
RC=`grep "%global rcrev" kernel.spec| cut -d ' ' -f 3`
GITREV=`grep "%define gitrev" kernel.spec| cut -d ' ' -f 3`
BUILDID=`grep "^%global buildid" kernel.spec| cut -d ' ' -f 3`
if [ $RELEASED -eq 0 ]; then
	cd "$(rpm -E %{_builddir})"/kernel-$MAJORVER.$BASE.fc??
	NEWBASE=$(($BASE+1))
	KVER=$MAJORVER.$NEWBASE.0-0.rc$RC.git$GITREV.$BASERELEASE$BUILDID
	cd linux-$MAJORVER.$NEWBASE.0-0.rc$RC.git$GITREV.$BASERELEASE$BUILDID.fc*/
else
	cd "$(rpm -E %{_builddir})"/kernel-$MAJORVER.$BASE.fc??/linux-$MAJORVER.$BASE.$STABLE-$BASERELEASE$BUILDID.fc*/
	KVER=$MAJORVER.$BASE.$STABLE-$BASERELEASE$BUILDID
fi

# ARCH_LIST below has the default list of supported architectures
# (the architectures names may be different from rpm, you list here the
# names of arch/<arch> directories in the kernel sources)
ARCH_LIST="arm arm64 powerpc s390 x86"

headers_dir=$(mktemp -d)
trap 'rm -rf "$headers_dir"' SIGHUP SIGINT SIGTERM EXIT

archs=${ARCH_LIST:-$(ls arch)}
echo $archs

# Upstream rmeoved the headers_install_all target so do it manually
for arch in $archs; do
	mkdir $headers_dir/arch-$arch
	make ARCH=$arch INSTALL_HDR_PATH=$headers_dir/arch-$arch KBUILD_HEADERS=install headers_install
done
find $headers_dir \
	\( -name .install -o -name .check -o \
	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

TARBALL=$CURRENTDIR/$PKGLOC/kernel-headers-$KVER.tar.xz
pushd $headers_dir
	tar -Jcf $TARBALL *
popd

echo wrote $TARBALL

# Update kernel-headers.spec
cd $CURRENTDIR/$PKGLOC/

BASE=$BASE perl -p -i -e 's|%define base_sublevel.*|%define base_sublevel $ENV{'BASE'}|' kernel-headers.spec
BASERELEASE=$(($BASERELEASE-1))
BASERELEASE=$BASERELEASE perl -p -i -e 's|%global baserelease.*|%global baserelease $ENV{'BASERELEASE'}|' kernel-headers.spec

if [ $RELEASED -eq 0 ]; then
	[ -n "$BUILDID" ] && sed -i -e 's/^# define buildid .local/%define buildid '$BUILDID'/' kernel-headers.spec
	RC=$RC perl -p -i -e 's|%global rcrev.*|%global rcrev $ENV{'RC'}|' kernel-headers.spec
	GITREV=$GITREV perl -p -i -e 's|%define gitrev.*|%define gitrev $ENV{'GITREV'}|' kernel-headers.spec
	rpmdev-bumpspec -c "Linux v$MAJORVER.$NEWBASE-rc$RC.git$GITREV" kernel-headers.spec
else
	STABLE=$STABLE perl -p -i -e 's|%define stable_update.*|%define stable_update $ENV{'STABLE'}|' kernel-headers.spec
	rpmdev-bumpspec -c "$MAJORVER.$BASE.$STABLE" kernel-headers.spec
fi
echo "Modified $CURRENTDIR/$PKGLOC/kernel-headers.spec"
echo "Don't forget to upload the sources"
