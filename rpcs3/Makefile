NAME = ffmpeg-core
VERSION ?= 10d0ebc0b8c7c4f0b242c9998c8bdc4e55bb5067

TARBALLVER = $(shell echo ${VERSION} | cut -c-7 )
DLSTR = ${VERSION}

DIRNAME = ${NAME}-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f ${NAME}-${TARBALLVER}.tar.gz
	rm -f ${NAME}-${TARBALLVER}.tar.xz
	rm -f ${NAME}-clean-${TARBALLVER}.tar.xz

clone: clean
	curl --location -O https://github.com/RPCS3/${NAME}/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
	rm -rf $(DIRNAME)/linux/*/*
	rm -rf $(DIRNAME)/macos/*/*
	rm -rf $(DIRNAME)/windows/*/*

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-nobin-${TARBALLVER}.tar.xz ${DIRNAME}
