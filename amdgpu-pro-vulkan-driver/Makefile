NAME = amdgpu-pro
VERSION ?= 19.50-967956
DISTRO ?= ubuntu-18.04
TARBALL = ${NAME}-${VERSION}-${DISTRO}.tar.xz
URL=https://drivers.amd.com/drivers/linux/$(shell echo ${VERSION} | cut -d- -f1 )/$(TARBALL)

all: $(TARBALL)

$(TARBALL):
	wget --referer https://www.amd.com/en/support/kb/release-notes/rn-rad-lin-19-50-unified -N $(URL)
