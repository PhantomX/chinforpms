NAME = MangoHud
VERSION ?= 0.6.1
SNAPSHOT ?= 0
DFSG = include/nvml.h

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
	curl --location -O https://github.com/flightlessmango/${NAME}/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz
	rm -f ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
	$(foreach var,$(DFSG),rm -rf $(DIRNAME)/$(var);)

archive: clone sanitize
	tar cJf ${NAME}-${TARBALLVER}.tar.xz ${DIRNAME}
