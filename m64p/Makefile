NAME = m64p
VERSION ?= 85d0d3f79d01309829d2c052e0c6f8e301775e32
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
	curl --location -O https://github.com/loganmc10/${NAME}/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
ifeq ($(SANITIZE),1)
	rm -f $(DIRNAME)/*.exe
	rm -rf $(DIRNAME)/mupen64plus-core
	rm -rf $(DIRNAME)/parallel-rdp-standalone
	rm -rf $(DIRNAME)/parallel-rsp
	rm -f $(DIRNAME)/mupen64plus-gui/discord/*.{dylib,so,dll}
	rm -f $(DIRNAME)/mupen64plus-input-qt/vosk/*.{dylib,so,dll}
	rm -rf .git
endif

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-clean-${TARBALLVER}.tar.xz ${DIRNAME}
