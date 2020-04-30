NAME = boca
VERSION ?= 1.0.1
SANITIZE ?= 1
CLEAN_PATCH = $(NAME)-clean.patch

DIRNAME = ${NAME}-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f ${NAME}-${VERSION}.tar.xz

clone: clean
	curl --location -O https://downloads.sourceforge.net/bonkenc/${NAME}-${VERSION}.tar.gz
	tar xf ${NAME}-${VERSION}.tar.gz

sanitize: clone $(CLEAN_PATCH)
ifeq ($(SANITIZE),1)
	rm -rf $(DIRNAME)/components/decoder/aiff
	rm -rf $(DIRNAME)/components/decoder/au
	rm -rf $(DIRNAME)/components/decoder/bonk
	rm -rf $(DIRNAME)/components/decoder/cdrip
	rm -rf $(DIRNAME)/components/decoder/faad2
	rm -rf $(DIRNAME)/components/decoder/fdkaac
	rm -rf $(DIRNAME)/components/decoder/mac
	rm -rf $(DIRNAME)/components/decoder/voc
	rm -rf $(DIRNAME)/components/decoder/wave
	rm -rf $(DIRNAME)/components/decoder/wma
	rm -rf $(DIRNAME)/components/encoder/bonk
	rm -rf $(DIRNAME)/components/encoder/coreaudio
	rm -rf $(DIRNAME)/components/encoder/coreaudioconnect
	rm -rf $(DIRNAME)/components/encoder/faac
	rm -rf $(DIRNAME)/components/encoder/fdkaac
	rm -rf $(DIRNAME)/components/encoder/voaacenc
	rm -rf $(DIRNAME)/components/encoder/wave
	rm -rf $(DIRNAME)/components/encoder/wma
	cp $(CLEAN_PATCH) $(DIRNAME)/
	patch -p1 -d $(DIRNAME) -i $(CLEAN_PATCH)
	rm -f $(DIRNAME)/$(CLEAN_PATCH)
endif

archive: clone sanitize
	tar cJf ${DIRNAME}.tar.xz ${DIRNAME}
