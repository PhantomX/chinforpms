NAME = amdgpu-pro
VERSION ?= 20.20-1089974
DISTRO ?= ubuntu-20.04
TARBALL = ${NAME}-${VERSION}-${DISTRO}.tar.xz
URL=https://drivers.amd.com/drivers/linux/$(TARBALL)
#URL=https://drivers.amd.com/drivers/linux/$(shell echo ${VERSION} | cut -d- -f1 )/$(TARBALL)

all: $(TARBALL)

$(TARBALL):
	wget --referer https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-20-20 -N $(URL)
