VERSION ?= 19.0.6
SANITIZE ?= 1

DIRNAME = mesa-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f mesa-${VERSION}.tar.xz

clone: clean
	curl -O https://mesa.freedesktop.org/archive/mesa-${VERSION}.tar.xz
	tar xf mesa-${VERSION}.tar.xz

sanitize: clone vl_mpeg12_decoder.c vl_decoder.c
ifeq ($(SANITIZE),1)
	cat < vl_mpeg12_decoder.c > $(DIRNAME)/src/gallium/auxiliary/vl/vl_mpeg12_decoder.c
	cat < vl_decoder.c > $(DIRNAME)/src/gallium/auxiliary/vl/vl_decoder.c
endif

archive: clone sanitize
	tar cJf ${DIRNAME}.tar.xz ${DIRNAME}
