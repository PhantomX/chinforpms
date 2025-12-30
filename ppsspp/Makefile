NAME = ppsspp-ffmpeg
VERSION ?= ee9265e96ae0b9175bc59aefd43d6e29ac35f3b7

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
