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
VARIANT='-chinfo'
VARIANTID="${VARIANT//-/.}"
KERNELSPEC="kernel${VARIANT}.spec"
HEADERSSPEC="kernel${VARIANT}-headers.spec"
CURRENTDIR="$(pwd)"
PKGLOC="kernel${VARIANT}-headers"

if [ ! -f "$PKGLOC/${HEADERSSPEC}" ]; then
	echo "Missing checkout of kernel${VARIANT}-headers in $PKGLOC"
	exit 1
fi

# Kernel version information taken from kernel.spec and change to prepared sources directory
MAJORVER='5'
RELEASED="$(grep "%global released_kernel" ${KERNELSPEC}| cut -d ' ' -f 3)"
BASERELEASE="$(grep "%global baserelease" ${KERNELSPEC}| cut -d ' ' -f 3)"
BASE="$(grep "%define base_sublevel" ${KERNELSPEC}| cut -d ' ' -f 3)"
STABLE="$(grep "%define stable_update" ${KERNELSPEC}| cut -d ' ' -f 3)"
RC="$(grep "%global rcrev" ${KERNELSPEC}| cut -d ' ' -f 3)"
GITREV="$(grep "%define gitrev" ${KERNELSPEC}| cut -d ' ' -f 3)"
BUILDID="$(grep "^%global buildid" ${KERNELSPEC}| cut -d ' ' -f 3)"
if [ "$RELEASED" -eq 0 ]; then
	# shellcheck disable=SC1083
	cd "$(rpm -E %{_builddir})/kernel-$MAJORVER.$BASE.fc"??
	NEWBASE=$((BASE+1))
	KVER="$MAJORVER.$NEWBASE.0-0.rc$RC.git$GITREV.${BASERELEASE}${BUILDID}${VARIANTID}"
	cd linux-"$MAJORVER.$NEWBASE.0-0.rc$RC.git$GITREV.${BASERELEASE}${BUILDID}${VARIANTID}.fc"*/
else
	# shellcheck disable=SC1083
	cd "$(rpm -E %{_builddir})/kernel-$MAJORVER.$BASE.fc"??/linux-"$MAJORVER.$BASE.$STABLE-${BASERELEASE}${BUILDID}${VARIANTID}.fc"*/
	KVER="$MAJORVER.$BASE.$STABLE-${BASERELEASE}${BUILDID}${VARIANTID}"
fi

# ARCH_LIST below has the default list of supported architectures
# (the architectures names may be different from rpm, you list here the
# names of arch/<arch> directories in the kernel sources)
ARCH_LIST="arm arm64 powerpc s390 x86"

headers_dir=$(mktemp -d)
trap 'rm -rf "$headers_dir"' SIGHUP SIGINT SIGTERM EXIT

archs=${ARCH_LIST:-$(ls arch)}
echo "$archs"

# Upstream rmeoved the headers_install_all target so do it manually
for arch in $archs; do
	mkdir "$headers_dir/arch-$arch"
	make ARCH="$arch" INSTALL_HDR_PATH="$headers_dir/arch-$arch" KBUILD_HEADERS=install headers_install
done
find "$headers_dir" \
	\( -name .install -o -name .check -o \
	-name ..install.cmd -o -name ..check.cmd \) -print0 | xargs -0 rm -f

TARBALL="$CURRENTDIR/$PKGLOC/kernel${VARIANT}-headers-$KVER.tar.xz"
pushd "$headers_dir"
	tar -Jcf "$TARBALL" -- *
popd

echo wrote "$TARBALL"

# Update kernel-headers.spec
cd "$CURRENTDIR/$PKGLOC"/

BASE=$BASE perl -p -i -e 's|%define base_sublevel.*|%define base_sublevel $ENV{"BASE"}|' ${HEADERSSPEC}
BASERELEASE=$((BASERELEASE-1))
BASERELEASE=${BASERELEASE} perl -p -i -e 's|%global baserelease.*|%global baserelease $ENV{"BASERELEASE"}|' ${HEADERSSPEC}

if [ "$RELEASED" -eq 0 ]; then
	[ -n "${BUILDID}" ] && sed -i -e "s/^# define buildid .local/%define buildid '${BUILDID}'/" ${HEADERSSPEC}
	RC=$RC perl -p -i -e 's|%global rcrev.*|%global rcrev $ENV{"RC"}|' ${HEADERSSPEC}
	GITREV=$GITREV perl -p -i -e 's|%define gitrev.*|%define gitrev $ENV{"GITREV"}|' ${HEADERSSPEC}
	rpmdev-bumpspec -c "Linux v$MAJORVER.$NEWBASE-rc$RC.git$GITREV" ${HEADERSSPEC}
else
	STABLE=$STABLE perl -p -i -e 's|%define stable_update.*|%define stable_update $ENV{"STABLE"}|' ${HEADERSSPEC}
	rpmdev-bumpspec -c "$MAJORVER.$BASE.$STABLE" ${HEADERSSPEC}
fi
echo "Modified $CURRENTDIR/$PKGLOC/${KERNELSPEC}"
echo "Don't forget to upload the sources"
