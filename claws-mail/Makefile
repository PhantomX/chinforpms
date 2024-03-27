NAME = claws-mail
VERSION ?= 2ab815a9115fbad6b25f07c7e3b67ba1f79c4257
SNAPSHOT ?= 1
SNAPROOT = git://git.claws-mail.org/claws.git

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
	git clone --depth 1 ${SNAPROOT} ${DIRNAME}

archive: clone
	cd ${DIRNAME} && git archive --format=tar --prefix=claws-${VERSION}/ ${DLSTR} | xz -9 > ../${NAME}-${TARBALLVER}.tar.xz
