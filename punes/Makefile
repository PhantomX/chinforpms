NAME = puNES
VERSION ?= b1758ec26a3d6da10abf50dc184fa837236c5f61
SNAPSHOT ?= 1
SNAPROOT = https://github.com/punesemu/puNES
7ZIPDIR = 7z2500

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
	rm -f ${NAME}-free-${TARBALLVER}.tar.xz

clone: clean
	curl --location -O ${SNAPROOT}/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
	rm -rf $(DIRNAME)/src/extra/${7ZIPDIR}/CPP/7zip/{Archive,Compress,Crypto}/Rar*
	rm -f $(DIRNAME)/src/extra/${7ZIPDIR}/DOC/unRarLicense.txt

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-free-${TARBALLVER}.tar.xz ${DIRNAME}
