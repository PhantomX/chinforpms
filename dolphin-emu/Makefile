NAME = dolphin
VERSION ?= eae68194b30610c60f224c676f573de024ed3a78
SNAPSHOT ?= 1
EXTERNALS = bzip2 cubeb curl discord-rpc ed25519 enet ffmpeg gettext gtest hidapi libiconv-1.14 liblzma libpng libusb LZO mbedtls miniupnpc minizip OpenAL pugixml Qt SFML MoltenVK XAudio2_7 xxhash zlib zstd

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
	curl --location -O https://github.com/dolphin-emu/dolphin/archive/${DLSTR}/${NAME}-${TARBALLVER}.tar.gz
	tar xf ${NAME}-${TARBALLVER}.tar.gz
	rm -f ${NAME}-${TARBALLVER}.tar.gz

sanitize: clone
	$(foreach var,$(EXTERNALS),rm -rf $(DIRNAME)/Externals/$(var);)

archive: clone sanitize
	tar cJf ${NAME}-${TARBALLVER}.tar.xz ${DIRNAME}
