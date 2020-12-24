NAME = pcsx2
VERSION ?= 74336d952d7705551f0ef434067d0137ef06cf41
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
	rm -rf $(DIRNAME)/3rdparty
	rm -rf $(DIRNAME)/tools
	$(foreach var,$(PLUGINS),rm -rf $(DIRNAME)/plugins/$(var);)
	rm -rf $(DIRNAME)/unfree
	rm -rf $(DIRNAME)/plugins/GSdx/baseclasses
	rm -f  $(DIRNAME)/plugins/zzogl-pg/opengl/Win32/aviUtil.h
	rm -f  $(DIRNAME)/common/src/Utilities/x86/MemcpyFast.cpp
	rm -rf .git
endif

archive: clone sanitize
	tar cJf ${NAME}-${TARBALLVER}.tar.xz ${DIRNAME}
