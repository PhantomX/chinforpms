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
KERNELPKGNAME="kernel${VARIANT}"
PKGLOC="${KERNELPKGNAME}-headers"
HEADERSSPEC="${PKGLOC}.spec"
CURRENTDIR="$(pwd)"


if [ ! -f "$PKGLOC/${HEADERSSPEC}" ]; then
	echo "Missing checkout of kernel${VARIANT}-headers in $PKGLOC"
	exit 1
fi
# Kernel version information taken from kernel.spec and change to prepared sources directory
SPECRPMVERSION="$(grep "%define specrpmversion" ${KERNELSPEC}| cut -d ' ' -f 3)"
TARBALL_RELEASE="$(echo ${SPECRPMVERSION} | cut -d'.' -f-2)"
BASERELEASE="$(grep "%define baserelease" ${KERNELSPEC} | cut -d ' ' -f 3)"
BUILDID="$(grep "^%global buildid" ${KERNELSPEC}| cut -d ' ' -f 3)"
SRCVERSION="${BASERELEASE}${BUILDID}${VARIANTID}"
# shellcheck disable=SC1083
cd "$(rpm -E %{_builddir})/kernel-$TARBALL_RELEASE/linux-$SPECRPMVERSION-${SRCVERSION}.fc"*/
KVER="${SPECRPMVERSION}-${SRCVERSION}"

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

TARBALL="$CURRENTDIR/$PKGLOC/${PKGLOC}-$KVER.tar.xz"
pushd "$headers_dir"
	tar -Jcf "$TARBALL" -- *
popd

echo wrote "$TARBALL"

# Update kernel-headers.spec
cd "$CURRENTDIR/$PKGLOC"/

SPECRPMVERSION=$SPECRPMVERSION perl -p -i -e 's|%define specrpmversion.*|%define specrpmversion $ENV{"SPECRPMVERSION"}|' ${HEADERSSPEC}
BASERELEASE=$((BASERELEASE-1))
BASERELEASE=${BASERELEASE} perl -p -i -e 's|%define baserelease.*|%define baserelease $ENV{"BASERELEASE"}|' ${HEADERSSPEC}

rpmdev-bumpspec -c "$SPECRPMVERSION" ${HEADERSSPEC}

echo "Modified $CURRENTDIR/$PKGLOC/${KERNELSPEC}"
echo "Don't forget to upload the sources"
