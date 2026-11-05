NAME = 7zip
VERSION ?= 26.05

TARBALLVER = $(shell echo $(VERSION) | tr -d \. )
TARBALL = 7z$(TARBALLVER)-src.tar.xz
TARBALL_CLEAN = $(NAME)-free-$(VERSION).tar.xz

DIRNAME = ${NAME}-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f $(TARBALL)
	rm -f $(TARBALL_CLEAN)

clone: clean
	curl --location -O https://github.com/ip7z/7zip/releases/download/$(VERSION)/$(TARBALL)
	mkdir $(DIRNAME)
	tar -xJf $(TARBALL) -C $(DIRNAME)

sanitize: clone
	chmod -Rf a+rX,u+w,g-w,o-w $(DIRNAME)
	rm -rf $(DIRNAME)/CPP/7zip/{Archive,Compress,Crypto}/Rar*
	rm -f $(DIRNAME)/DOC/unRarLicense.txt

archive: clone sanitize
	tar --numeric-owner -cJf $(TARBALL_CLEAN) $(DIRNAME)
