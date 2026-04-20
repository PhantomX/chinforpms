NAME = xfce-session-target
VERSION ?= 1.3.2
SNAPSHOT ?= 0
SNAPROOT = https://git.linux-help.org/infusix/${NAME}.git

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
	git clone ${SNAPROOT} ${DIRNAME}

archive: clone
	cd ${DIRNAME} && git archive --format=tar --prefix=${NAME}-${VERSION}/ ${DLSTR} | gzip -9 > ../${NAME}-${TARBALLVER}.tar.gz
