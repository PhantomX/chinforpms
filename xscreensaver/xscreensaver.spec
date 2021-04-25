%define name          xscreensaver

%define mainversion   5.45
%define beta_ver      %{nil}


%define modular_conf  1
%define split_getimage   0
%if 0%{?fedora} >= 14
%define split_getimage   1
%endif

%define fedora_rel    100

%global use_clang_as_cc 0
%global use_clang_analyze 0
%global use_cppcheck   0
%global use_gcc_strict_sanitize 0
%global use_gcc_trap_on_sanitize 0
%global use_gcc_analyzer 0
%undefine extrarel

%global flagrel %{nil}
%if 0%{?use_cppcheck} >= 1
%global flagrel %{flagrel}.cppcheck
%endif
%if 0%{?use_gcc_strict_sanitize} >= 1
%global flagrel %{flagrel}.san
%endif


# EPEL6
%{!?__git:%define __git git}

%if 0%{?fedora}
%define default_text  %{_sysconfdir}/fedora-release
%else
%define default_text  %{_sysconfdir}/system-release
%endif
%define default_URL   http://planet.fedoraproject.org/rss20.xml

%define pam_ver       0.80-7
%define autoconf_ver  2.53

%define update_po     1
%define build_tests   0

%global support_setcap 0
%if 0%{?fedora} >= 31
# TODO write selinux policy for selinux-policy-mls 
# (currently works with selinux-policy-targeted)
#%%global support_setcap 1
%endif
# enable xscreensaver-systemd for F-33
%global  support_systemd 0
%if 0%{?fedora} >= 33
%global  support_systemd 1
%endif

%undefine        _changelog_trimtime


Summary:         X screen saver and locker
Name:            %{name}
Version:         %{mainversion}
Release:         %{fedora_rel}%{flagrel}%{?dist}%{?extrarel}
Epoch:           1
License:         MIT
URL:             http://www.jwz.org/xscreensaver/
Source0:         http://www.jwz.org/xscreensaver/xscreensaver-%{mainversion}%{?beta_ver}.tar.gz
%if %{modular_conf}
Source10:        update-xscreensaver-hacks
%endif
Source11:        xscreensaver-autostart
Source12:        xscreensaver-autostart.desktop
# wrapper script for switching user (bug 1878730)
Source13:        xscreensaver-newlogin-wrapper
##
## Patches
##
# bug 129335
Patch1:          xscreensaver-5.45-0001-barcode-glsnake-sanitize-the-names-of-modes.patch
## Patches already sent to the upsteam
## Patches which must be discussed with upstream
# See bug 472061
Patch21:         xscreensaver-5.35-webcollage-default-nonet.patch
# Patch to compile driver/test-xdpms
Patch52:         xscreensaver-5.44-0002-Patch-to-compile-driver-test-xdpms.patch
# 
# misc: kill gcc warn_unused_result warnings
Patch3607:       xscreensaver-5.36-0007-misc-kill-gcc-warn_unused_result-warnings.patch
# open new window for man when using gnome-terminal
Patch4261:       xscreensaver-5.42-0061-open-new-window-for-man-when-using-gnome-terminal.patch
# test-password.c: add skel definition for clientmessage_response
Patch4501:      xscreensaver-5.45-1001-test-password.c-add-skel-definition-for-clientmessa.patch
# asm6502.c/immediate: readd free() call accidentally removed during gcc warnings fix
Patch4502:      xscreensaver-5.45-0002-asm6502.c-immediate-readd-free-call-accidentally-rem.patch
# beats/draw_beats: avoid integer overflow by multiplication
Patch4503:      xscreensaver-5.45-0003-beats-draw_beats-avoid-integer-overflow-by-multiplic.patch
#
# gcc warning cleanup
# Some cppcheck cleanup
#
# Debugging patch
# Not apply by default
# XIO: print C backtrace on error
Patch13501:      xscreensaver-5.35-0101-XIO-print-C-backtrace-on-error.patch
#
# Patches end
Requires:        xscreensaver-base = %{epoch}:%{version}-%{release}
Requires:        xscreensaver-extras = %{epoch}:%{version}-%{release}
Requires:        xscreensaver-gl-extras = %{epoch}:%{version}-%{release}

%package base
Summary:         A minimal installation of xscreensaver

%if 0%{?use_clang_analyze} >= 1
BuildRequires:   clang-analyzer
BuildRequires:   clang
%endif
%if 0%{?use_clang_as_cc}
BuildRequires:   clang
%endif
%if 0%{?use_cppcheck}
BuildRequires:   cppcheck
%endif
%if 0%{?use_gcc_strict_sanitize}
BuildRequires:   libasan
BuildRequires:   libubsan
%endif
BuildRequires:   git
BuildRequires:   autoconf
BuildRequires:   automake
BuildRequires:   intltool
BuildRequires:   bc
BuildRequires:   desktop-file-utils
BuildRequires:   gawk
BuildRequires:   gettext
BuildRequires:   libtool
BuildRequires:   pam-devel > %{pam_ver}
BuildRequires:   sed
# Use pseudo symlink
# BuildRequires:   xdg-utils
BuildRequires:   xorg-x11-proto-devel
# extrusioni
%if 0%{?fedora} >= 13
BuildRequires:   libgle-devel
%endif
BuildRequires:   libX11-devel
BuildRequires:   libXScrnSaver-devel
BuildRequires:   libXext-devel
# From xscreensaver 5.12, write explicitly
BuildRequires:   libXi-devel
BuildRequires:   libXinerama-devel
BuildRequires:   libXmu-devel
# xscreensaver 5.39: check if the following can be removed
BuildRequires:   libXpm-devel
# xscreensaver 5.39
BuildRequires:   libpng-devel
# Write explicitly
BuildRequires:   libXrandr-devel
BuildRequires:   libXt-devel
# libXxf86misc removed from F-31
#BuildRequires:   libXxf86misc-devel
BuildRequires:   libXxf86vm-devel
# XScreenSaver 5.31
BuildRequires:   libXft-devel
BuildRequires:   gtk2-devel
# Write explicitly below, especially
# for F-23 gdk_pixbuf package splitting
BuildRequires:   pkgconfig(gdk-pixbuf-2.0)
BuildRequires:   pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:   libjpeg-devel
BuildRequires:   libglade2-devel
%if 0%{?support_setcap} >= 1
BuildRequires:   pkgconfig(libcap)
%endif
# From F-33, enable systemd support
%if 0%{?support_systemd} >= 1
BuildRequires:   pkgconfig(libsystemd)
%endif
%if 0%{?fedora}
BuildRequires:   %{default_text}
%endif
# For https://fedoraproject.org/wiki/Packaging:Perl#Build_Dependencies
# https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
# For --with-login-manager option
%if 0%{?fedora} >= 14
# Use pseudo symlink, not writing BR: gdm
#BuildRequires:   gdm
%endif
Requires:        %{_sysconfdir}/pam.d/system-auth
Requires:        pam > %{pam_ver}
# For xdg-open
Requires:        xdg-utils
%if ! %{split_getimage}
Requires:        appres
%endif
Requires:        xorg-x11-fonts-ISO8859-1-100dpi
# For switch user wrapper
Requires:        %{_bindir}/pidof
%if 0%{?build_tests} < 1
# Obsoletes but not Provides
Obsoletes:       xscreeensaver-tests < %{epoch}:%{version}-%{release}
%endif

%package extras-base
Summary:         A base package for screensavers
%if 0%{?fedora} < 19
Requires:        %{name}-base = %{epoch}:%{version}-%{release}
%endif
Requires:        appres

%package extras
Summary:         An enhanced set of screensavers
%if 0%{?fedora} >= 19
# Does not available on EPEL7
BuildRequires:   desktop-backgrounds-basic
%else
BuildRequires:	   gnome-backgrounds
%endif
Requires:        %{name}-base = %{epoch}:%{version}-%{release}
%if %{split_getimage}
Requires:        %{name}-extras-base = %{epoch}:%{version}-%{release}
%endif

%package gl-base
Summary:         A base package for screensavers that require OpenGL
Requires:        %{name}-base = %{epoch}:%{version}-%{release}

%package gl-extras
Summary:         An enhanced set of screensavers that require OpenGL
Provides:        xscreensaver-gl = %{epoch}:%{version}-%{release}
Obsoletes:       xscreensaver-gl <= 1:5.00
BuildRequires:   libGL-devel
BuildRequires:   libGLU-devel
%if %{modular_conf}
Requires:        %{name}-gl-base = %{epoch}:%{version}-%{release}
%else
Requires:        %{name}-base = %{epoch}:%{version}-%{release}
%endif
%if %{split_getimage}
Requires:        %{name}-extras-base = %{epoch}:%{version}-%{release}
%endif

%package extras-gss
Summary:         Desktop files of extras for other screensaver
Requires:        %{name}-extras = %{epoch}:%{version}-%{release}

%package gl-extras-gss
Summary:         Desktop files of gl-extras for other screensaver
Requires:        %{name}-gl-extras = %{epoch}:%{version}-%{release}

%package tests
Summary:         Test programs related to XScreenSaver
Requires:        %{name}-base = %{epoch}:%{version}-%{release}

%package clang-analyze
Summary:         Clang analyze result log

%package cppcheck
Summary:         cppcheck result log


%description
A modular screen saver and locker for the X Window System.
More than 200 display modes are included in this package.

This is a metapackage for installing all default packages
related to XScreenSaver.

%description -l fr
Un économiseur d'écran modulaire pour le système X Window.
Plus de 200 modes d'affichages sont inclus dans ce paquet.

This is a metapackage for installing all default packages
related to XScreenSaver.

%description base
A modular screen saver and locker for the X Window System.
This package contains the bare minimum needed to blank and
lock your screen.  The graphical display modes are the
"xscreensaver-extras" and "xscreensaver-gl-extras" packages.

%description -l fr base 
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient le minimum vital pour éteindre et verouiller
votre écran. Les modes d'affichages graphiques sont inclus
dans les paquets "xscreensaver-extras" et "xscreensaver-gl-extras".

%description extras-base
This package contains common files to make screensaver hacks
work for XScreenSaver.

%description extras
A modular screen saver and locker for the X Window System.
This package contains a variety of graphical screen savers for
your mind-numbing, ambition-eroding, time-wasting, hypnotized
viewing pleasure.

%description -l fr extras
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient une pléthore d'économiseurs d'écran graphiques
pour votre plaisir des yeux.

%description gl-base
A modular screen saver and locker for the X Window System.
This package contains minimal files to make screensaver hacks
that require OpenGL work for XScreenSaver.

%description gl-extras
A modular screen saver and locker for the X Window System.
This package contains a variety of OpenGL-based (3D) screen
savers for your mind-numbing, ambition-eroding, time-wasting,
hypnotized viewing pleasure.

%description -l fr gl-extras
Un économiseur d'écran modulaire pour le système X Window.
Ce paquet contient une pléthore d'économiseurs d'écran basés sur OpenGL (3D)
pour votre plaisir des yeux.

%description extras-gss
This package contains desktop files of extras screensavers
for other screensaver compatibility.

%description gl-extras-gss
This package contains desktop files of gl-extras screensavers
for other screensaver compatibility.

%description tests
This package contains some test programs to debug XScreenSaver.

%description clang-analyze
This package contains Clang analyze result of XScreenSaver.

%description cppcheck
This package contains cppcheck result of XScreenSaver.


%prep
%setup -q -n %{name}-%{mainversion}%{?beta_ver}

cat > .gitignore <<EOF
configure
config.guess
config.sub
aclocal.m4
config.h.in
OSX
EOF

# Firstly clean this
rm -f driver/XScreenSaver_ad.h

# chmod
find . -name \*.c -exec chmod ugo-x {} \;

%__git init
%__git config user.email "xscreensaver-owner@fedoraproject.org"
%__git config user.name "XScreenSaver owners"
%__git add .
%__git commit -m "base" -q

%__cat %PATCH1 | %__git am
%__cat %PATCH21 | %__git am
%__cat %PATCH52 | %__git am

#%%__cat %PATCH3607 | %__git am
%__cat %PATCH4261 | %__git am

%__cat %PATCH4501 | %__git am
%__cat %PATCH4502 | %__git am
%__cat %PATCH4503 | %__git am

#%%__cat %PATCH13501 | %%__git am

change_option(){
   set +x
   ADFILE=$1
   if [ ! -f ${ADFILE}.opts ] ; then
      cp -p $ADFILE ${ADFILE}.opts
   fi
   shift

   for ARG in "$@" ; do
      TYPE=`echo $ARG | sed -e 's|=.*$||'`
      VALUE=`echo $ARG | sed -e 's|^.*=||'`

      eval sed -i \
         -e \'s\|\^\\\(\\\*$TYPE\:\[ \\t\]\[ \\t\]\*\\\)\[\^ \\t\]\.\*\$\|\\1$VALUE\|\' \
         $ADFILE
   done
   set -x
}

silence_hack(){
   set +x
   ADFILE=$1
   if [ ! -f ${ADFILE}.hack ] ; then
      cp -p $ADFILE ${ADFILE}.hack
   fi
   shift

   for hack in "$@" ; do
      eval sed -i \
         -e \'\/\^\[ \\t\]\[ \\t\]\*$hack\/s\|\^\|-\|g\' \
         -e \'s\|\^@GL_\.\*@.*\\\(GL\:\[ \\t\]\[ \\t\]\*$hack\\\)\|-\\t\\1\|g\' \
         $ADFILE
   done
   set -x
}

%global PATCH_desc \
# change some files to UTF-8
for f in \
   driver/XScreenSaver.ad.in \
   hacks/glx/sproingies.man \
   ; do
   iconv -f ISO-8859-1 -t UTF-8 $f > $f.tmp || cp -p $f $f.tmp
   touch -r $f $f.tmp
   mv $f.tmp $f
done
%__git commit -m "%PATCH_desc" -a

%global PATCH_desc \
# Change some options \
# For grabDesktopImages, lock, see bug 126809
change_option driver/XScreenSaver.ad.in \
   captureStderr=False \
   passwdTimeout=0:00:15 \
   grabDesktopImages=False \
   lock=True \
   splash=False \
   ignoreUninstalledPrograms=True \
   textProgram=fortune\ -s \
%if 0%{?fedora} >= 12
   textURL=%{default_URL}
%endif
%__git commit -m "%PATCH_desc" -a

# peepers: 5.39: too scary (mtasaka)
# headroom: 5.45: too scary (mtasaka)
%global PATCH_desc \
# Disable the following hacks by default \
# (disable, not remove)
silence_hack driver/XScreenSaver.ad.in \
   bsod flag \
   peepers \
   headroom \
   %{nil}
%__git commit -m "%PATCH_desc" -a

%global PATCH_desc \
# Record time, EVR
eval sed -i.ver \
   -e \'s\|version \[45\]\.\[0-9a-z\]\[0-9a-z\]\*\|version %{version}-`echo \
      %{release} | sed -e '/IGNORE THIS/s|\.[a-z][a-z0-9].*$||'`\|\' \
      driver/XScreenSaver.ad.in

eval sed -i.date \
   -e \'s\|\[0-9\].\*-.\*-20\[0-9\]\[0-9\]\|`LANG=C LC_ALL=C date -u +'%%d-%%b-%%Y'`\|g\' \
   driver/XScreenSaver.ad.in

eval sed -i.ver \
   -e \'s\|\(\[0-9\].\*-.\*-20\[0-9\]\[0-9\]\)\|\(`LANG=C LC_ALL=C \
      date -u +'%%d-%%b-%%Y'`\)\|g\' \
   -e \'s\|\\\(5.\[0-9\]\[0-9\]\\\)[a-z]\[0-9\]\[0-9\]\*\|\\\1\|\' \
   -e \'s\|5.\[0-9\]\[0-9\]\|%{version}-`echo %{release} | \
      sed -e '/IGNORE THIS/s|\.[a-zA-Z][a-zA-Z0-9].*$||'`\|\' \
   utils/version.h
%__git commit -m "%PATCH_desc" -a

%global PATCH_desc \
# Move man entry to 6x (bug 197741)
for f in `find hacks -name Makefile.in` ; do
   sed -i.mansuf \
      -e '/^mansuffix/s|6|6x|'\
      $f
done
%__git commit -m "%PATCH_desc" -a

%global PATCH_desc \
# Search first 6x entry, next 1 entry for man pages
sed -i.manentry -e 's@man %%s@man 6x %%s 2>/dev/null || man 1 %%s @' \
   driver/XScreenSaver.ad.in
%__git commit -m "%PATCH_desc" -a

# Suppress rpmlint warnings.
# suppress about pam config (although this is 
# not the fault of xscreensaver.pam ......).
#
# From xscreensaver-5.15-10, no longer do this
%if 0
sed -i.rpmlint -n -e '1,5p' driver/xscreensaver.pam
%endif

if [ -x %{_datadir}/libtool/config.guess ]; then
  # use system-wide copy
   cp -p %{_datadir}/libtool/config.{sub,guess} .
fi

%global PATCH_desc \
# Fix for desktop-file-utils 0.14+
%if 0%{?fedora} >= 9
sed -i.icon -e 's|xscreensaver\.xpm|xscreensaver|' \
   driver/screensaver-properties.desktop.in
%endif
%__git commit -m "%PATCH_desc" -a || echo "Nothing changed"

%global PATCH_desc \
# Disable (don't build) some tests \
# apm: doesn't compile \
# mlstring: causes OOM - need check again
sed -i.test \
   -e 's|test-apm[ \t][ \t]*t|t|' \
%if 0
   -e 's|test-mlstring[ \t][ \t]*t|t|' \
%endif
   driver/Makefile.in
%__git commit -m "%PATCH_desc" -a

%global PATCH_desc \
# test-fade: give more time between fading
sed -i.delay -e 's| delay = 1| delay = 3|' driver/test-fade.c
%__git commit -m "%PATCH_desc" -a

%global PATCH_desc \
# test-grab: testing time too long, setting time 15 min -> 20 sec
sed -i.delay -e 's|60 \* 15|20|' driver/test-grab.c
%__git commit -m "%PATCH_desc" -a

aclocal
autoconf
autoheader

%build

archdir=`sh ./config.guess`
[ -d $archdir ] || mkdir $archdir
cd $archdir

# Create temporary path and symlink
rm -rf ./TMPBINDIR

# Make it sure that perl interpreter is recognized
# as /usr/bin/perl, not /bin/perl so as not to make
# /bin/perl added as rpm dependency
export PATH=/usr/bin:$PATH

mkdir TMPBINDIR
pushd TMPBINDIR/
export PATH=$(pwd):$PATH

# xdg-open
ln -sf /bin/true xdg-open
popd

# Set optflags first
%set_build_flags

# Doesn't work well when generating debuginfo...
# export CFLAGS="$(echo $CFLAGS | sed -e 's|-g |-g3 -ggdb |')"

export CFLAGS="$CFLAGS -Wno-long-long"
export CFLAGS="$CFLAGS -Wno-variadic-macros"

%if 0%{?use_clang_as_cc}
export CC=clang
export CFLAGS="$(echo $CFLAGS | sed -e 's|-fstack-protector-strong|-fstack-protector|')"
export CFLAGS="$(echo $CFLAGS | sed -e 's|-specs=[^ \t][^ \t]*||g')"
export CFLAGS="$(echo $CFLAGS | sed -e 's|-flto=auto -ffat-lto-objects |-flto |')"
export CFLAGS="$CFLAGS -Wno-gnu-statement-expression"
export LDFLAGS="$(echo $LDFLAGS | sed -e 's|-specs=[^ \t][^ \t]*||g')"
%if 0%{?fedora} >= 33
export LDFLAGS="$LDFLAGS -flto"
%endif
%endif

%if 0%{?use_gcc_strict_sanitize}
export CC="${CC} -fsanitize=address -fsanitize=undefined"
export LDFLAGS="${LDFLAGS} -pthread"
%if 0%{?use_gcc_trap_on_sanitize}
export CC="$CC -fsanitize-undefined-trap-on-error"
%endif
# Currently -fPIE binary cannot work with ASAN on kernel 4.12
# https://github.com/google/sanitizers/issues/837
export CFLAGS="$(echo $CFLAGS   | sed -e 's|-specs=[^ \t][^ \t]*hardened[^ \t][^ \t]*||g')"
export LDFLAGS="$(echo $LDFLAGS | sed -e 's|-specs=[^ \t][^ \t]*hardened[^ \t][^ \t]*||g')"
%endif

%if 0%{?use_gcc_analyzer}
export CC="${CC} -fanalyzer"
# make build log look clear
%global _smp_mflags -j1
%endif

CONFIG_OPTS="--prefix=%{_prefix} --with-pam --without-shadow --without-kerberos"
CONFIG_OPTS="$CONFIG_OPTS --without-setuid-hacks"
CONFIG_OPTS="$CONFIG_OPTS --with-text-file=%{default_text}"
CONFIG_OPTS="$CONFIG_OPTS --with-x-app-defaults=%{_datadir}/X11/app-defaults"
CONFIG_OPTS="$CONFIG_OPTS --disable-root-passwd"
CONFIG_OPTS="$CONFIG_OPTS --with-browser=xdg-open"

# From xscreensaver 5.12, login-manager option is on by default
# For now, let's enable it on F-14 and above
pushd TMPBINDIR
# ln -sf /bin/true gdmflexiserver
install -cpm 0755 %{SOURCE13} .
CONFIG_OPTS="$CONFIG_OPTS --with-login-manager=xscreensaver-newlogin-wrapper"
popd

# Enable extrusion on F-13 and above
# CONFIG_OPTS="$CONFIG_OPTS --with-gle" # default

# Enable account type pam validation on F-18+,
# debian bug 656766
CONFIG_OPTS="$CONFIG_OPTS --enable-pam-check-account-type"

# xscreensaver 5.30
CONFIG_OPTS="$CONFIG_OPTS --with-record-animation"

%if 0%{?support_setcap}
CONFIG_OPTS="$CONFIG_OPTS --with-setcap-hacks"
%endif

%if 0%{?support_systemd}
CONFIG_OPTS="$CONFIG_OPTS --with-systemd"
%endif

# This is flaky:
# CONFIG_OPTS="$CONFIG_OPTS --with-login-manager"

%if 0%{?use_clang_analyze} >= 1
%global _configure scan-build --use-analyzer %_bindir/clang ./configure
%endif

unlink configure || :
ln -s ../configure .
%configure $CONFIG_OPTS || { cat config.log ; sleep 10 ; exit 1; }
rm -f configure

# Remove embedded build path
sed -i driver/XScreenSaver.ad -e "s|$(pwd)/TMPBINDIR/||"

%if %{update_po}
#( cd po ; make generate_potfiles_in update-po )
# ???
pushd po
  make generate_potfiles_in
  cp -p POTFILES.in ..
  # Workaround for ui file
  sed -i ../POTFILES.in POTFILES.in POTFILES \
     -e '\@-demo\.ui@s|^\([ \t]*\)\(.*\)$|\1[type: gettext/glade]\2|'
  make xscreensaver.pot srcdir=..
  ( export srcdir=.. ; make update-po )
  rm -f ../POTFILES_in
popd


( cp -p ../po/*.po po/)
( ( cd ../po ; git add *.po ; git commit -m "po regenerated" ) || true )
%endif

%if 0%{?use_clang_analyze} >= 1
%global __make scan-build  --use-analyzer %_bindir/clang -v -v -v -o clang-analyze make
mkdir clang-analyze
%endif

# Workaround for 5.39
mkdir -p hacks/images || true
if [ ! -f hacks/images/Makefile ] ; then
   cat > hacks/images/Makefile <<EOF
default:
install:
EOF
fi
# Workaround end

# From 5.45: temporary workaround for installation issue
cp -p ../driver/xscreensaver-demo.ui driver/

%if 0%{?use_clang_analyze} < 1
# Workaround for ppc64 build failure
make -C ../hacks/images -j1
for dir in \
  utils driver ../hacks/images hacks hacks/glx po
do
  %__make %{?_smp_mflags} -k \
    -C $dir \
	GMSGFMT="msgfmt --statistics"
done
%endif

# Again
%__make %{?_smp_mflags} -k

%if %{modular_conf}
# Make XScreenSavar.ad modular (bug 200881)
CONFD=xscreensaver
rm -rf $CONFD
mkdir $CONFD

# Preserve the original adfile
cp -p driver/XScreenSaver.ad $CONFD

# First split XScreenSaver.ad into 3 parts
cat driver/XScreenSaver.ad | \
   sed -n -e '1,/\*programs/p' > $CONFD/XScreenSaver.ad.header
cat driver/XScreenSaver.ad | sed -e '1,/\*programs/d' | \
   sed -n -e '1,/\\n$/p' > $CONFD/XScreenSaver.ad.hacks
cat driver/XScreenSaver.ad | sed -e '1,/\\n$/d' > $CONFD/XScreenSaver.ad.tail

# Seperate XScreenSaver.ad.hacks into each hacks
cd $CONFD
mkdir hacks.conf.d ; cp -p XScreenSaver.ad.hacks hacks.conf.d/xscreensaver.conf
cd ..

%endif

# test
# for now, build tests anyway (even if they are not to be installed)
make tests -C driver

%if 0%{?use_cppcheck} >= 1
cd ..
CPPCHECK_FLAGS=""
CPPCHECK_FLAGS="$CPPCHECK_FLAGS --enable=all --std=c89 -U__STRICT_ANSI__"
CPPCHECK_FLAGS="$CPPCHECK_FLAGS -I. -Iutils -Iutils/images -Idriver -Ihacks"
CPPCHECK_FLAGS="$CPPCHECK_FLAGS -I$archdir -I$archdir/driver -I$archdir/hacks"
CPPCHECK_FLAGS="$CPPCHECK_FLAGS -I$archdir/hacks/glx"
CPPCHECK_FLAGS="$CPPCHECK_FLAGS -I%{_includedir}"
# find stddef.h
GCC_HEADER_PATH=$(echo '#include <stddef.h>' | gcc -E - | sed -n -e 's|^.*"\(.*\)stddef\.h".*$|\1|p' | head -n 1)
CPPCHECK_FLAGS="$CPPCHECK_FLAGS -I$GCC_HEADER_PATH"
CPPCHECK_FLAGS="$CPPCHECK_FLAGS $(pkg-config --cflags gtk+-2.0 | sed -e 's|-pthread||')"
CPPCHECK_FLAGS="$CPPCHECK_FLAGS -DSTANDALONE -DHAVE_CONFIG_H -DUSE_GL"
# C default macros
CPPCHECK_FLAGS="$CPPCHECK_FLAGS -D__STDC__"

cppcheck $CPPCHECK_FLAGS . 2>&1 | tee cppcheck-result.log
cppcheck $CPPCHECK_FLAGS --check-config . 2>&1 | tee cppcheck-path-inclusion-check.log

cd $archdir
%endif

%install
archdir=`sh ./config.guess`
cd $archdir

rm -rf ${RPM_BUILD_ROOT}

# We have to make sure these directories exist,
# or nothing will be installed into them.
#
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d

make install_prefix=$RPM_BUILD_ROOT INSTALL="install -c -p" install

# Kill OnlyShowIn=GNOME; on F-11+ (bug 483495)
desktop-file-install --vendor "" --delete-original    \
   --dir $RPM_BUILD_ROOT%{_datadir}/applications         \
%if 0%{?fedora} < 11
   --add-only-show-in GNOME                              \
%endif
   --add-category    DesktopSettings                     \
%if 0
   --add-category X-Red-Hat-Base                         \
%else
   --remove-category Appearance                          \
   --remove-category AdvancedSettings                    \
   --remove-category Application                         \
%endif
   $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# This function prints a list of things that get installed.
# It does this by parsing the output of a dummy run of "make install".
list_files() {
   echo "%%defattr(-,root,root,-)"
   make -s install_prefix=${RPM_BUILD_ROOT} INSTALL=true "$@"  \
      | sed -n -e 's@.* \(/[^ ]*\)$@\1@p'                      \
      | sed    -e "s@^${RPM_BUILD_ROOT}@@"                     \
               -e "s@/[a-z][a-z]*/\.\./@/@"                    \
      | sed    -e 's@\(.*/man/.*\)@%%doc \1\*@'                      \
               -e 's@\(.*/pam\.d/\)@%%config(noreplace) \1@'    \
      | sort  \
      | uniq
}

# Generate three lists of files for the three packages.
#
dd=%{_builddir}/%{name}-%{mainversion}%{?beta_ver}

# In case rpm -bi --short-circuit is tried multiple times:
rm -f $dd/*.files

(  cd hacks     ; list_files install ) >  $dd/extras.files
(  cd hacks/glx ; list_files install ) >  $dd/gl-extras.files
(  cd driver    ; list_files install ) >  $dd/base.files

%if 0%{?support_setcap} >= 1
sed -i $dd/gl-extras.files \
	-e '\@sonar$@s|^|%%attr(0755,root,root) %%caps(cap_net_raw=p)|' \
	%{nil}
%endif

# Move xscreensaver-gettext-foo, xscreensaver-text to extras-base
# (bug 668427)
%if %{split_getimage}
echo "%%defattr(-,root,root,-)" >> $dd/extras-base.files
for target in \
   /xscreensaver-getimage \
   /xscreensaver-text
do
   grep -v $target $dd/base.files > $dd/base.files.new
   grep $target $dd/base.files >> $dd/extras-base.files
   mv $dd/base.files{.new,}
done
%endif

# Move %%{_bindir}/xscreensaver-gl-helper to gl-base
# (bug 336331).
%if %{modular_conf}
echo "%%defattr(-,root,root,-)" >> $dd/gl-base.files

sed -i -e '/xscreensaver-gl-helper/d' $dd/gl-extras.files
pushd $RPM_BUILD_ROOT
for dir in `find . -name \*xscreensaver-gl-helper\*` ; do
   echo "${dir#.}" >> $dd/gl-base.files
done
popd
sed -i -e 's|^\(%{_mandir}.*\)$|\1*|' $dd/gl-base.files
%endif

%if %{modular_conf}
# Install update script
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -cpm 755 %{SOURCE10} $RPM_BUILD_ROOT%{_sbindir}
echo "%{_sbindir}/update-xscreensaver-hacks" >> $dd/base.files

# Make hack conf modular
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xscreensaver
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xscreensaver/hacks.conf.d
cp -p xscreensaver/XScreenSaver.ad* \
   $RPM_BUILD_ROOT%{_sysconfdir}/xscreensaver
cp -p xscreensaver/hacks.conf.d/xscreensaver.conf \
   $RPM_BUILD_ROOT%{_datadir}/xscreensaver/hacks.conf.d/

for adfile in xscreensaver/XScreenSaver.ad.* ; do
   filen=`basename $adfile`
   echo "%%config(noreplace) %{_sysconfdir}/xscreensaver/$filen" >> $dd/base.files
done
echo -n "%%verify(not size md5 mtime) " >> $dd/base.files
echo "%{_sysconfdir}/xscreensaver/XScreenSaver.ad" >> \
   $dd/base.files
echo "%{_datadir}/xscreensaver/hacks.conf.d/xscreensaver.conf" \
   >> $dd/base.files

# Check symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults/XScreenSaver

pushd $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults
pushd ../../../..
if [ ! $(pwd) == $RPM_BUILD_ROOT ] ; then
   echo "Possibly symlink broken"
   exit 1
fi
popd
popd

ln -sf ../../../..%{_sysconfdir}/xscreensaver/XScreenSaver.ad \
   $RPM_BUILD_ROOT%{_datadir}/X11/app-defaults/XScreenSaver

%endif

# Add documents
pushd $dd &> /dev/null
for f in README* ; do
   echo "%%doc $f" >> $dd/base.files
done
popd

# Add directory
pushd $RPM_BUILD_ROOT
for dir in `find . -type d | grep xscreensaver` ; do
   echo "%%dir ${dir#.}" >> $dd/base.files
done
popd

%find_lang %{name}
cat %{name}.lang | uniq >> $dd/base.files

# Suppress rpmlint warnings
# sanitize path in script file
for f in ${RPM_BUILD_ROOT}%{_bindir}/xscreensaver-getimage-* \
   ${RPM_BUILD_ROOT}%{_libexecdir}/xscreensaver/vidwhacker \
   ${RPM_BUILD_ROOT}%{_bindir}/xscreensaver-text ; do
   if [ -f $f ] ; then
      sed -i -e 's|%{_prefix}//bin|%{_bindir}|g' $f
   fi
done

# tests
%if %{build_tests}
echo "%%defattr(-,root,root,-)" > $dd/tests.files
cd driver
for tests in `find . -name test-\* -perm -0700` ; do
   install -cpm 0755 $tests ${RPM_BUILD_ROOT}%{_libexecdir}/xscreensaver
   echo "%{_libexecdir}/xscreensaver/$tests" >> $dd/tests.files
done
cd ..
%endif

%if 0%{?use_clang_analyze} >= 1
pushd ..
rm -rf clang-analyze
mkdir -p clang-analyze/html
cp -a $archdir/clang-analyze/*/* clang-analyze/html
popd
%endif

# Install desktop application autostart stuff
# Add OnlyShowIn=GNOME (bug 517391)
# Leave autostart stuff installed (at least useful for LXDE),
# but not show them by default for all DE
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart
install -cpm 0755 %{SOURCE11} ${RPM_BUILD_ROOT}%{_libexecdir}/
desktop-file-install \
   --vendor "" \
   --dir ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart \
   --add-only-show-in=X-NODEFAULT \
   %{SOURCE12}
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart/xscreensaver*.desktop

echo "%{_libexecdir}/xscreensaver-autostart" >> $dd/base.files
echo '%{_sysconfdir}/xdg/autostart/xscreensaver*.desktop' >> $dd/base.files

# Create desktop entry for gnome-screensaver
# bug 204944, 208560
create_desktop(){
   COMMAND=`cat $1 | sed -n -e 's|^<screen.*name=\"\([^ ][^ ]*\)\".*$|\1|p'`
# COMMAND must be full path (see bug 531151)
# Check if the command actually exists
   COMMAND=%{_libexecdir}/xscreensaver/$COMMAND
   if [ ! -x $RPM_BUILD_ROOT/$COMMAND ] ; then
      echo
      echo "WARNING:"
      echo "$COMMAND could not be found under $RPM_BUILD_ROOT"
      #exit 1
   fi
# NAME entry fix (bug 953558)
   NAME=`cat $1 | sed -n -e 's|^<screen.*_label=\"\([^\"][^\"]*\)\".*>.*$|\1|p'`
   ARG=`cat $1 | sed -n -e 's|^.*<command arg=\"\([^ ][^ ]*\)\".*$|\1|p'`
   ARG=$(echo "$ARG" | while read line ; do echo -n "$line " ; done)
   COMMENT="`cat $1 | sed -e '1,/_description/d' | \
     sed -e '/_description/q' | sed -e '/_description/d'`"
   COMMENT=$(echo "$COMMENT" | while read line ; do echo -n "$line " ; done)

# webcollage treatment
## changed to create wrapper script
%if 0
   if [ "x$COMMAND" = "xwebcollage" ] ; then
      ARG="$ARG -directory %{_datadir}/backgrounds/images"
   fi
%endif

   if [ "x$NAME" = "x" ] ; then NAME=$COMMAND ; fi

   rm -f $2
   echo "[Desktop Entry]" >> $2
#   echo "Encoding=UTF-8" >> $2
   echo "Name=$NAME" >> $2
   echo "Comment=$COMMENT" >> $2
   echo "TryExec=$COMMAND" >> $2
   echo "Exec=$COMMAND $ARG" >> $2
   echo "StartupNotify=false" >> $2
   echo "Type=Application" >> $2
   echo "Categories=GNOME;Screensaver;" >> $2
# Add OnlyShowIn (bug 953558)
   echo "OnlyShowIn=GNOME;MATE;" >> $2
}

cd $dd

SAVERDIR=%{_datadir}/applications/screensavers
mkdir -p ${RPM_BUILD_ROOT}${SAVERDIR}
echo "%%dir $SAVERDIR" >> base.files

for list in *extras.files ; do

   glist=gnome-$list
   rm -f $glist

   echo "%%defattr(-,root,root,-)" > $glist
##  move the owner of $SAVERDIR to -base
##   echo "%%dir $SAVERDIR" >> $glist

   set +x
   for xml in `cat $list | grep xml$` ; do
      file=${RPM_BUILD_ROOT}${xml}
      desktop=xscreensaver-`basename $file`
      desktop=${desktop%.xml}.desktop

      echo + create_desktop $file  ${RPM_BUILD_ROOT}${SAVERDIR}/$desktop
      create_desktop $file  ${RPM_BUILD_ROOT}${SAVERDIR}/$desktop
      echo ${SAVERDIR}/$desktop >> $glist
   done
   set -x
done

# Create wrapper script for webcollage to use nonet option
# by default, and rename the original webcollage
# (see bug 472061)
pushd ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}
mv -f webcollage webcollage.original

cat > webcollage <<EOF
#!/bin/sh
PATH=%{_libexecdir}/%{name}:\$PATH
exec webcollage.original \\
	-directory %{_datadir}/backgrounds/images \\
	"\$@"
EOF
chmod 0755 webcollage
echo "%%{_libexecdir}/%%{name}/webcollage.original" >> \
	$dd/extras.files

# install wrapper-script for switching user
install -cpm 0755 %{SOURCE13} ${RPM_BUILD_ROOT}%{_libexecdir}/%{name}
echo "%{_libexecdir}/%{name}/xscreensaver-newlogin-wrapper" >> $dd/base.files


# Make sure all files are readable by all, and writable only by owner.
#
chmod -R a+r,u+w,og-w ${RPM_BUILD_ROOT}

%post base
%if %{modular_conf}
%{_sbindir}/update-xscreensaver-hacks
%endif

%if 0%{?fedora} >= 18
# In the case that pam setting is edited locally by sysadmin:
if ! grep -q '^account' %{_sysconfdir}/pam.d/xscreensaver
then
    echo "Warning: %{_sysconfdir}/pam.d/xscreensaver saved as %{_sysconfdir}/pam.d/xscreensaver.rpmsave"
    cp -p %{_sysconfdir}/pam.d/xscreensaver{,.rpmsave}
    PAMFILE=%{_sysconfdir}/pam.d/xscreensaver
    echo >> $PAMFILE
    echo "# Account validation" >> $PAMFILE
    echo "account include system-auth" >> $PAMFILE
fi
%endif

exit 0

%files
%defattr(-,root,root,-)

%files -f base.files base
%defattr(-,root,root,-)

%if %{build_tests}
%files -f tests.files tests
%defattr(-,root,root,-)
%endif

%if %{split_getimage}
%files -f extras-base.files extras-base
%defattr(-,root,root,-)
%endif

%files -f extras.files extras
%defattr(-,root,root,-)

%if %{modular_conf}
%files -f gl-base.files gl-base
%defattr(-,root,root,-)
%endif

%files -f gl-extras.files gl-extras
%defattr(-,root,root,-)

%files -f gnome-extras.files extras-gss
%defattr(-,root,root,-)

%files -f gnome-gl-extras.files gl-extras-gss
%defattr(-,root,root,-)

%if 0%{?use_clang_analyze} >= 1
%files clang-analyze
%doc clang-analyze/html
%endif

%if 0%{?use_cppcheck} >= 1
%files cppcheck
%doc cppcheck-*.log
%endif

%changelog
* Sun Apr 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.45-100
- Downgrade for Fedora 34

* Thu Dec 10 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.45-1
- Update to 5.45
- asm6502.c/immediate: readd free() call accidentally removed during gcc warnings fix
- beats/draw_beats: avoid integer overflow by multiplication

* Tue Nov 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-12
- Clean up gcc10 warnings, especially for -Wstringop
- Clean up some warnings by cppcheck

* Mon Nov  9 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-11
- Another way to make LTO happy with respecting upstream advice

* Sat Nov  7 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-10
- Remove unneeded undefining to make LTO happy

* Thu Oct 22 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-9
- Fix BR for systemd: use pkgconfig(libsystemd)

* Tue Oct 20 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-8
- peepers / reset_floater : fix logic for choosing color

* Wed Oct 14 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-6
- Install experimental wrapper script for switching user (bug 1878730)

* Sat Oct  3 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-5
- FuzzyFlakesFreeFlake: avoid double free on subsequent calls
  such as when ConfigureNotify event happens (bug 1884822)

* Fri Sep 25 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-4
- Some spec file cleanup, deleting conditions for no longer supported branches
- Use %%set_build_flags
- F-33+: enable systemd integration

* Tue Jul 28 2020 Adam Jackson <ajax@redhat.com> 1:5.44-3
- Requires appres not xorg-x11-resutils

* Thu Apr 16 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-2
- ya_rand_init: avoid signed integer overflow by with recent pid_max value

* Tue Mar 24 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.44-1
- Update to 5.44
- free_gibson: fix order of freeing memory

* Sat Feb  8 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.43-5
- More fix for issues detected by gcc10 sanitizer
  - send_ping(sonar-icmp.c): keep alignment for struct timeval
  - gravitywell: restict the index accessing to colors[] buffer to the valid range

* Fri Feb  7 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.43-3
- make_job (driver/subprocs.c): check is the pointer gets to the last of string buffer correctly
  (error detected by gcc10 -sanitize=address)

* Tue Jan 28 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.43-2.1
- F-32: mass rebuild

* Tue Aug 27 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.43-2
- glhanoi: fix malloc size shortage (bug 1745794)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.43-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.43-1
- Update to 5.43

* Tue Jun 25 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.42-2
- xjack: avoid freeing string literal when window is small (bug 1723461)

* Thu Jun 20 2019 Adam Jackson <ajax@redhat.com> - 1:5.42-1.3
- Drop BuildRequires: pkgconfig(xxf86misc), X servers haven't implemented that
  extension in 10+ years.

* Fri Jun 14 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:5.42-2
- sonar: support setcap (disabled for now)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.42-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1:5.42-1.1
- Rebuilt for libcrypt.so.2 (#1666033)
