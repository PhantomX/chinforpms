NAME = p7zip
VERSION ?= 79aac5226bdad25efda22095445ad7c4e0d9a06f
SNAPSHOT ?= 1

ifeq ($(SNAPSHOT),1)
	TARBALLVER = $(shell echo ${VERSION} | cut -c-7 )
	DLSTR = ${VERSION}
else
	TARBALLVER = ${VERSION}
	DLSTR = ${VERSION}
endif

DIRNAME = ${NAME}-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f ${NAME}-${TARBALLVER}.tar.xz

clone: clean
	curl --location -O https://github.com/jinfeihan57/p7zip/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz
	rm -f ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
	rm -rf $(DIRNAME)/CPP/7zip/{Archive,Compress,Crypto,CMAKE,QMAKE}/Rar*
	rm -f $(DIRNAME)/DOC/unRarLicense.txt
	rm -f $(DIRNAME)/Utils/file_Codecs_Rar_so.py

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-${TARBALLVER}.tar.xz ${DIRNAME}
