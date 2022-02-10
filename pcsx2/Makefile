NAME = pcsx2
VERSION ?= af648334d1d8503d2853c93b18dec7b9932ef1f3
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
	mkdir $(DIRNAME)/3rdparty-temp
	mv $(DIRNAME)/3rdparty/include $(DIRNAME)/3rdparty-temp/
	mv $(DIRNAME)/3rdparty/glad $(DIRNAME)/3rdparty-temp/
	mv $(DIRNAME)/3rdparty/glslang $(DIRNAME)/3rdparty-temp/
	mv $(DIRNAME)/3rdparty/imgui $(DIRNAME)/3rdparty-temp/
	mv $(DIRNAME)/3rdparty/jpgd $(DIRNAME)/3rdparty-temp/
	mv $(DIRNAME)/3rdparty/rapidyaml $(DIRNAME)/3rdparty-temp/
	mv $(DIRNAME)/3rdparty/simpleini $(DIRNAME)/3rdparty-temp/
	mv $(DIRNAME)/3rdparty/xbyak $(DIRNAME)/3rdparty-temp/
	rm -rf $(DIRNAME)/3rdparty/*
	mv $(DIRNAME)/3rdparty-temp/* $(DIRNAME)/3rdparty/
	rmdir $(DIRNAME)/3rdparty-temp/
	rm -rf $(DIRNAME)/tools
	rm -f  $(DIRNAME)/common/src/Utilities/x86/MemcpyFast.cpp
	rm -rf .git
endif

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-clean-${TARBALLVER}.tar.xz ${DIRNAME}
