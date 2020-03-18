#!/bin/sh
if [ $# -lt 3 ]; then echo Usage: dummylib.sh orig_lib_path dummy_lib_path mapfile; exit 1; fi
TMPDIR=`mktemp -d dummylib.sh.XXXXXX` || exit 1
F=`file -L $1`
C=
S=8
case "$F" in
  *ELF\ 64-bit*shared\ object*x86-64*) C=-m64;;
  *ELF\ 32-bit*shared\ object*80?86*) C=-m32; S=4;;
  *ELF\ 64-bit*shared\ object*PowerPC*) C=-m64;;
  *ELF\ 32-bit*shared\ object*PowerPC*) C=-m32; S=4;;
  *ELF\ 64-bit*shared\ object*cisco*) C=-m64;;
  *ELF\ 32-bit*shared\ object*cisco*) C=-m32; S=4;;
  *ELF\ 64-bit*shared\ object*IA-64*) C=;;
  *ELF\ 64-bit*shared\ object*Alpha*) C=;;
  *ELF\ 64-bit*shared\ object*390*) C=-m64;;
  *ELF\ 32-bit*shared\ object*390*) C=-m31; S=4;;
  *ELF\ 64-bit*shared\ object*SPARC*) C=-m64;;
  *ELF\ 32-bit*shared\ object*SPARC*) C=-m32; S=4;;
  *ELF\ 64-bit*shared\ object*Alpha*) C=;;
esac
readelf -Ws $1 | awk '
/\.dynsym.* contains/ { start=1 }
/^$/ { start=0 }
/  WEAK.*  UND [^@]*$/ { if (start) {
  print ".data"; print ".weak " $8; print ".balign 8"
  print ".'$S'byte " $8
} }
/  UND / { next }
/@/ { if (start) {
  fn=$8
  intfn="HACK" hack+0
  hack++
  if ($4 ~ /FUNC/) { print ".text"; size=16; print ".type " intfn ",@function" }
  else if ($4 ~ /OBJECT/) { print ".data"; size=$3; print ".type " intfn ",@object" }
  else if ($4 ~ /NOTYPE/) { print ".data"; size=$3 }
  else exit(1);
  print ".globl " intfn
  if ($5 ~ /WEAK/) { print ".weak " intfn }
  else if ($5 !~ /GLOBAL/) exit(1);
  print intfn ": .skip " size
  print ".size " intfn "," size
  print ".symver " intfn "," fn
} }
' > $TMPDIR/lib.s || exit
soname=`readelf -Wd $1 | grep SONAME | sed 's/^.*\[//;s/\].*$//'`
gcc $C -shared -Wl,-soname,$soname,-version-script,$3 \
    -o $2 $TMPDIR/lib.s -nostdlib
strip $2
rm -rf $TMPDIR
