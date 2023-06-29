NAME = 7zip
VERSION ?= 23.01

TARBALLVER = $(shell echo ${VERSION} | tr -d \. )

DIRNAME = ${NAME}-${VERSION}

all: archive

clean:
	rm -rf $(DIRNAME)/
	rm -f 7z${TARBALLVER}-src.7z
	rm -f ${NAME}-free-${TARBALLVER}.tar.xz

clone: clean
	curl --location -O https://7-zip.org/a/7z${TARBALLVER}-src.7z
	7z x -o$(DIRNAME) 7z${TARBALLVER}-src.7z

sanitize: clone
	chmod -Rf a+rX,u+w,g-w,o-w $(DIRNAME)
	rm -rf $(DIRNAME)/CPP/7zip/{Archive,Compress,Crypto}/Rar*
	rm -f $(DIRNAME)/DOC/unRarLicense.txt

archive: clone sanitize
	tar --numeric-owner -cJf ${NAME}-free-${VERSION}.tar.xz ${DIRNAME}
