NAME = amdgpu-pro
VERSION ?= 19.30-934563
DISTRO ?= ubuntu-18.04
TARBALL = ${NAME}-${VERSION}-${DISTRO}.tar.xz
URL=https://drivers.amd.com/drivers/linux/$(TARBALL)

all: $(TARBALL)

$(TARBALL):
	wget --referer https://www.amd.com/en/support/kb/release-notes/rn-rad-lin-19-30-unified.aspx -N $(URL)
