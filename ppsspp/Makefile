NAME = ppsspp-ffmpeg
VERSION ?= a94f3e6fa89e6ac5763e6b9d23ab3c4a72bbcd6c

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
	curl --location -O https://github.com/hrydgard/${NAME}/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
	rm -rf $(DIRNAME)/*/*/include
	rm -rf $(DIRNAME)/*/*/lib
	rm -rf $(DIRNAME)/wiiu

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-nobin-${TARBALLVER}.tar.xz ${DIRNAME}
