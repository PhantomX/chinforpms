NAME = gst-plugins-ugly
VERSION ?= 1.18.4
SNAPSHOT ?= 0
SANITIZE ?= 1
ALLOWED = xingmux
NOT_ALLOWED= asfdemux dvdlpcmdec dvdsub realmedia

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
	rm -f ${NAME}-${TARBALLVER}.tar.bz2
	rm -f ${NAME}-${TARBALLVER}.tar.xz
	rm -f ${NAME}-free-${TARBALLVER}.tar.xz

clone: clean
ifeq ($(SNAPSHOT),1)
	curl --location https://gitlab.freedesktop.org/gstreamer/${NAME}/-/archive/${DLSTR}/${NAME}-${DLSTR}.tar.bz2 -o ${NAME}-${TARBALLVER}.tar.bz2
	tar xf ${NAME}-${TARBALLVER}.tar.bz2
	rm -f ${NAME}-${TARBALLVER}.tar.bz2
else
	curl --location -O https://gstreamer.freedesktop.org/src/${NAME}/${NAME}-${TARBALLVER}.tar.xz
	tar xf ${NAME}-${TARBALLVER}.tar.xz
	rm -f ${NAME}-${TARBALLVER}.tar.xz
endif

sanitize: clone
ifeq ($(SANITIZE),1)
	$(foreach var,$(NOT_ALLOWED),rm -rf $(DIRNAME)/gst/$(var);)
	$(foreach var,$(NOT_ALLOWED),rm -rf $(DIRNAME)/ext/$(var);)
	rm -rf .git
endif

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-free-${TARBALLVER}.tar.xz ${DIRNAME}
