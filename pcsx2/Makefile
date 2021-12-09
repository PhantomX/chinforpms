NAME = pcsx2
VERSION ?= 94c6814be8a471de6c1f59bf73689b473aafc039
SNAPSHOT ?= 1
SANITIZE ?= 1

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
	rm -f ${NAME}-${TARBALLVER}.tar.gz
	rm -f ${NAME}-${TARBALLVER}.tar.xz
	rm -f ${NAME}-clean-${TARBALLVER}.tar.xz

clone: clean
	curl --location -O https://github.com/PCSX2/${NAME}/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
ifeq ($(SANITIZE),1)
	mv $(DIRNAME)/3rdparty/include $(DIRNAME)/
	mv $(DIRNAME)/3rdparty/jpgd $(DIRNAME)/
	mv $(DIRNAME)/3rdparty/xbyak $(DIRNAME)/
	rm -rf $(DIRNAME)/3rdparty/*
	mv $(DIRNAME)/include $(DIRNAME)/3rdparty/
	mv $(DIRNAME)/jpgd $(DIRNAME)/3rdparty/
	mv $(DIRNAME)/xbyak $(DIRNAME)/3rdparty/
	rm -rf $(DIRNAME)/tools
	rm -f  $(DIRNAME)/common/src/Utilities/x86/MemcpyFast.cpp
	rm -rf .git
endif

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-clean-${TARBALLVER}.tar.xz ${DIRNAME}
