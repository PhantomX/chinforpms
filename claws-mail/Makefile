NAME = claws-mail
VERSION ?= 1608444ca48f8db3ec731805d330a5b13b05a6a3
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
