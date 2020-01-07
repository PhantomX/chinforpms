NAME = dolphin
VERSION ?= f35f4f2bf06eefe20ee3338a84b82aa30fe20e3a
SNAPSHOT ?= 1
EXTERNALS = cubeb curl discord-rpc ed25519 enet ffmpeg gettext gtest hidapi libiconv-1.14 libpng libusb LZO mbedtls miniupnpc OpenAL pugixml Qt SFML MoltenVK XAudio2_7 xxhash zlib

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
