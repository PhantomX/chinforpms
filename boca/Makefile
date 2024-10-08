NAME = boca
VERSION ?= 1.0.7
SANITIZE ?= 1
CLEAN_PATCH = $(NAME)-clean.patch

DIRNAME = ${NAME}-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f ${NAME}-${VERSION}.tar.gz
	rm -f ${NAME}-${VERSION}.tar.xz
	rm -f ${NAME}-free-${VERSION}.tar.xz

clone: clean
	curl --location -O https://github.com/enzo1982/BoCA/releases/download/v${VERSION}/${NAME}-${VERSION}.tar.gz
	tar xf ${NAME}-${VERSION}.tar.gz

sanitize: clone $(CLEAN_PATCH)
ifeq ($(SANITIZE),1)
	rm -rf $(DIRNAME)/components/decoder/aiff
	rm -rf $(DIRNAME)/components/decoder/alac
	rm -rf $(DIRNAME)/components/decoder/au
	rm -rf $(DIRNAME)/components/decoder/bonk
	rm -rf $(DIRNAME)/components/decoder/cdrip
	rm -rf $(DIRNAME)/components/decoder/faad2
	rm -rf $(DIRNAME)/components/decoder/fdkaac
	rm -rf $(DIRNAME)/components/decoder/mac
	rm -rf $(DIRNAME)/components/decoder/mediafoundation
	rm -rf $(DIRNAME)/components/decoder/twinvq
	rm -rf $(DIRNAME)/components/decoder/voc
	rm -rf $(DIRNAME)/components/decoder/wave
	rm -rf $(DIRNAME)/components/decoder/winamp
	rm -rf $(DIRNAME)/components/decoder/wma
	rm -rf $(DIRNAME)/components/encoder/bonk
	rm -rf $(DIRNAME)/components/encoder/coreaudio
	rm -rf $(DIRNAME)/components/encoder/coreaudioconnect
	rm -rf $(DIRNAME)/components/encoder/faac
	rm -rf $(DIRNAME)/components/encoder/fdkaac
	rm -rf $(DIRNAME)/components/encoder/mac
	rm -rf $(DIRNAME)/components/encoder/twinvq
	rm -rf $(DIRNAME)/components/encoder/voaacenc
	rm -rf $(DIRNAME)/components/encoder/wave
	rm -rf $(DIRNAME)/components/encoder/wma
	rm -rf $(DIRNAME)/include/support/MAC
	rm -rf $(DIRNAME)/include/support/vo-aacenc
	rm -f $(DIRNAME)/include/support/faac.h
	rm -f $(DIRNAME)/include/support/faacfg.h
	rm -f $(DIRNAME)/include/support/neaacdec.h
	cp $(CLEAN_PATCH) $(DIRNAME)/
	patch -p1 -d $(DIRNAME) -i $(CLEAN_PATCH)
	rm -f $(DIRNAME)/$(CLEAN_PATCH)
endif

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-free-${VERSION}.tar.xz ${DIRNAME}
