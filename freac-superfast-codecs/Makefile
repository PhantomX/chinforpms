NAME = freac-superfast-codecs
VERSION ?= 1.0-pre3
SANITIZE ?= 1
CLEAN_PATCH = $(NAME)-clean.patch

DIRNAME = superfast-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f ${NAME}-${VERSION}.tar.xz

clone: clean
	curl --location -O https://github.com/enzo1982/superfast/archive/v${VERSION}/${NAME}-${VERSION}.tar.gz
	tar xf ${NAME}-${VERSION}.tar.gz

sanitize: clone $(CLEAN_PATCH)
ifeq ($(SANITIZE),1)
	rm -rf $(DIRNAME)/components/coreaudio
	rm -rf $(DIRNAME)/components/faac
	rm -rf $(DIRNAME)/components/fdkaac
	rm -rf $(DIRNAME)/components/voaacenc
	cp $(CLEAN_PATCH) $(DIRNAME)/
	patch -p1 -d $(DIRNAME) -i $(CLEAN_PATCH)
	rm -f $(DIRNAME)/$(CLEAN_PATCH)
endif

archive: clone sanitize
	tar cJf ${DIRNAME}.tar.xz ${DIRNAME}
