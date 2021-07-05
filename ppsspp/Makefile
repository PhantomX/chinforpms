NAME = ppsspp-ffmpeg
VERSION ?= 0b28335acea4f429ae798c5e75232e54881bf164

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
