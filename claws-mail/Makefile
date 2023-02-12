NAME = claws-mail
VERSION ?= 8d176a20c6424d9c5c97e6866ef80795dab0909a
SNAPSHOT ?= 1
SNAPROOT = https://git.claws-mail.org/readonly/claws.git

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
	cd ${DIRNAME} && git archive --format=tar --prefix=claws-${VERSION}/ ${DLSTR} | xz -9 > ../${NAME}-${TARBALLVER}.tar.xz
