NAME = pcsx2
VERSION ?= 7187b883b07cf5d89ee63b22ed19dd907df5e83d
SNAPSHOT ?= 1
SANITIZE ?= 1
PLUGINS = CDVDiso CDVDisoEFP CDVDlinuz CDVDolio CDVDpeops dev9ghzdrk PeopsSPU2 SSSPSXPAD USBqemu xpad zerogs zerospu2

ifeq ($(SNAPSHOT),1)
	TARBALLVER = $(shell echo ${VERSION} | cut -c-7 )
	DLSTR = ${VERSION}
else
	TARBALLVER = ${VERSION}
	DLSTR = v${VERSION}
endif

DIRNAME = ${NAME}-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f ${NAME}-${TARBALLVER}.tar.xz

clone: clean
	curl --location -O https://github.com/PCSX2/pcsx2/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz
	rm -f ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
ifeq ($(SANITIZE),1)
	mv $(DIRNAME)/3rdparty/include $(DIRNAME)/
	rm -rf $(DIRNAME)/3rdparty/*
	mv $(DIRNAME)/include $(DIRNAME)/3rdparty/
	rm -rf $(DIRNAME)/tools
	$(foreach var,$(PLUGINS),rm -rf $(DIRNAME)/plugins/$(var);)
	rm -rf $(DIRNAME)/unfree
	rm -rf $(DIRNAME)/plugins/GSdx/baseclasses
	rm -f  $(DIRNAME)/plugins/zzogl-pg/opengl/Win32/aviUtil.h
	rm -f  $(DIRNAME)/common/src/Utilities/x86/MemcpyFast.cpp
	rm -rf .git
endif

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-${TARBALLVER}.tar.xz ${DIRNAME}
