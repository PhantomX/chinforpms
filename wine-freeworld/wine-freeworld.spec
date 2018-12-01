# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%global no64bit   0
#global _default_patch_fuzz 2

# build with staging-patches, see:  https://wine-staging.com/
%global stagingver 3.20
%if 0%(echo %{stagingver} | grep -q \\. ; echo $?) == 0
%global strel v
%endif

Name:           wine-freeworld
# If rc, use "~" instead "-", as ~rc1
Version:        3.20
Release:        1%{?dist}
Summary:        Wine libraries with all codecs support
Epoch:          1

License:        LGPLv2+
URL:            http://www.winehq.org/

%global ver     %{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global vermajor %(echo %{ver} | cut -d. -f1)
%if "%(echo %{ver} | cut -d. -f2 | cut -d- -f1 )" == "0"
%global verx 1
%endif
Source0:        https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz
Source10:       https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz.sign

# wine staging patches for wine-staging
Source900: https://github.com/wine-staging/wine-staging/archive/%{?strel}%{stagingver}.tar.gz#/wine-staging-%{stagingver}.tar.gz

%if !%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%else
ExclusiveArch:  %{ix86} %{arm}
%endif

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
%ifarch aarch64
BuildRequires:  clang >= 5.0
%else
BuildRequires:  gcc
%endif
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xproto)

Requires:       wine-core = %{version}
Requires:       wine-openal = %{version}
Enhances:       wine

%ifarch x86_64
Requires:       wine-freeworld(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

# x86-32 parts
%ifarch %{ix86} x86_64
Requires:       wine-core(x86-32) = %{version}
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{version}
%endif

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{version}
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{version}
%endif

Provides:       wine-xaudio2 = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       wine-xaudio2%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-xaudio2%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      wine-xaudio2 < %{?epoch:%{epoch}:}%{version}-%{release}

%description
This package adds libraries with all codecs support for wine.


%prep
%setup -q -n wine-%{ver}

# setup and apply wine-staging patches
gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

./patches/patchinstall.sh DESTDIR="`pwd`" --all

# fix parallelized build
sed -i -e 's!^loader server: libs/port libs/wine tools.*!& include!' Makefile.in

sed -i \
  -e 's|-lncurses |-lncursesw |g' \
  -e 's|"-lncurses"|"-lncursesw"|g' \
  -e 's|OpenCL/opencl.h|CL/opencl.h|g' \
  configure

%build

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo %{build_cflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

%ifarch aarch64
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
%endif

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --without-hal --with-dbus \
 --with-x \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
  --disable-tests \
  --without-capi \
  --without-cms \
  --without-coreaudio \
  --without-cups \
  --without-dbus \
  --without-freetype \
  --without-gnutls \
  --without-gsm \
  --without-gstreamer \
  --without-jpeg \
  --without-ldap \
  --without-mpg123 \
  --without-netapi  \
  --without-opencl \
  --without-osmesa \
  --without-oss  \
  --without-pcap \
  --without-png \
  --without-pulse \
  --without-sane \
  --without-sdl \
  --without-tiff \
  --without-udev \
  --without-v4l \
  --without-xinput \
  --without-xinput2 \
  --without-xml \
  --without-xslt \
  --without-zlib


make include
make %{?_smp_mflags} TARGETFLAGS="" __builddeps__

for i in 7 ;do
  make %{?_smp_mflags} TARGETFLAGS="" xaudio2_$i.dll.so -C dlls/xaudio2_$i
done


%install

for i in 7 ;do
  %makeinstall xaudio2_$i.dll.so -C dlls/xaudio2_$i \
    includedir=%{buildroot}%{_includedir}/wine \
    sysconfdir=%{buildroot}%{_sysconfdir}/wine \
    dlldir=%{buildroot}%{_libdir}/wine \
    LDCONFIG=/bin/true \
    UPDATE_DESKTOP_DATABASE=/bin/true
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING.LIB
%exclude %{_libdir}/wine/fakedlls
%{_libdir}/wine/xaudio2_7.dll.so


%changelog
* Mon Nov 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.20-1
- 3.20

* Mon Oct 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.19-1
- 3.19

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.18-1
- 3.18

* Mon Oct 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17-1
- 3.17

* Sat Sep 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.16-1
- 3.16

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.15-1
- 3.15

* Sun Aug 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.14-1
- 3.14

* Sat Jul 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:3.13-1
- 3.13
- Only build needed xaudio2_7.dll.so

* Wed Jul 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.12-2
- Conflicts

* Tue Jul 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.12-1
- Initial spec
