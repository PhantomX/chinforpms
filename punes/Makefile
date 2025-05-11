NAME = puNES
VERSION ?= ed201432b7186fed32ba8091afdeb9994295272b
SNAPSHOT ?= 1
SNAPROOT = https://github.com/punesemu/puNES
P7ZIPDIR = p7zip-17.04

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
	rm -rf $(DIRNAME)/src/extra/${P7ZIPDIR}/CPP/7zip/{Archive,Compress,Crypto,CMAKE,QMAKE}/Rar*
	rm -f $(DIRNAME)/src/extra/${P7ZIPDIR}/DOC/unRarLicense.txt
	rm -f $(DIRNAME)/src/extra/${P7ZIPDIR}/Utils/file_Codecs_Rar_so.py

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-free-${TARBALLVER}.tar.xz ${DIRNAME}
