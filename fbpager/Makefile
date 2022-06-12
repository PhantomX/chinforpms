NAME = fbpager
VERSION ?= 8e0927e6365ef295bab9a6037e0647cb9cc57fb2
SNAPSHOT ?= 1
SNAPROOT = git://git.fluxbox.org/${NAME}.git
SNAPTREE ?= master

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
	rm -f ${NAME}-${TARBALLVER}.tar.xz

clone: clean
	git clone ${SNAPROOT} ${DIRNAME}

archive: clone
	cd ${DIRNAME} && git archive --format=tar --prefix=${NAME}-${VERSION}/ ${SNAPTREE} | xz -9 > ../${NAME}-${TARBALLVER}.tar.xz
