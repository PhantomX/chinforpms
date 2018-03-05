%undefine _hardened_build
%global winecommonver 3.0

Name:           wine-nine
Version:        3.0_2
Release:        1%{?dist}
Summary:        Wine D3D9 interface library for Mesa's Gallium Nine statetracker

License:        LGPL-2.0
URL:            https://github.com/iXit/wine

%global rversion %(c=%{version}; echo ${c//_/-})
Source0:        https://github.com/iXit/wine/archive/%{name}-%{rversion}.tar.gz
Source1:        ninewinecfg

Source100:      wine-ninecfg.desktop

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
BuildRequires:  desktop-file-utils
BuildRequires:  llvm-devel
BuildRequires:  pkgconfig(d3d)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xproto)

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-libd3d%{?_isa}
Requires:       libxcb%{?_isa}
Requires:       libX11%{?_isa}
Requires:       libXext%{?_isa}
Provides:       wine-nine%{?_isa} = %{version}-%{release}
Obsoletes:      wine-nine%{?_isa} < %{version}-%{release}

%ifarch x86_64
Requires:       wine-nine(x86-32) = %{version}-%{release}
%endif

Provides:       ninewinecfg.exe.so%{?_isa} = %{version}
Provides:       d3d9-nine.dll.so%{?_isa} = %{version}

%description
%{summary} and tool to setting it.

%prep
%autosetup -n wine-%{name}-%{rversion}

sed -i \
  -e 's|-lncurses |-lncursesw |g' \
  -e 's|"-lncurses"|"-lncursesw"|g' \
  -e 's|OpenCL/opencl.h|CL/opencl.h|g' \
  configure

%build

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
%if 0%{?fedora} < 26
export CFLAGS="`echo %{optflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"
%else
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
export TEMP_CFLAGS="`echo %{build_cflags} | sed -e 's/-O2/-O1/'`"
export CFLAGS="`echo $TEMP_CFLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"
%endif

export CFLAGS="$CFLAGS -DWINE_STAGING=1"

%configure \
  --sysconfdir=%{_sysconfdir}/wine \
  --x-includes=%{_includedir} --x-libraries=%{_libdir} \
  --without-hal \
  --with-x \
%ifarch x86_64 aarch64
  --enable-win64 \
%endif
  --with-d3d9-nine \
  --disable-tests \
  --without-alsa \
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
  --without-openal \
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
make %{?_smp_mflags} TARGETFLAGS="" d3d9-nine.dll.so -C dlls/d3d9-nine
make %{?_smp_mflags} TARGETFLAGS="" d3d9-nine.dll.fake -C dlls/d3d9-nine
make %{?_smp_mflags} TARGETFLAGS="" programs/ninewinecfg

%install
mkdir -p %{buildroot}/%{_libdir}/wine
mkdir -p %{buildroot}/%{_libdir}/wine/fakedlls

install -pm0755 programs/ninewinecfg/ninewinecfg.exe.so \
  %{buildroot}/%{_libdir}/wine/ninewinecfg.exe.so
install -pm0755 programs/ninewinecfg/ninewinecfg.exe.fake \
  %{buildroot}/%{_libdir}/wine/fakedlls/ninewinecfg.exe

install -pm0755 dlls/d3d9-nine/d3d9-nine.dll.so \
  %{buildroot}/%{_libdir}/wine/d3d9-nine.dll.so
install -pm0755 dlls/d3d9-nine/d3d9-nine.dll.fake \
  %{buildroot}/%{_libdir}/wine/fakedlls/d3d9-nine.dll

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:1} %{buildroot}/%{_bindir}/ninewinecfg

mkdir -p %{buildroot}%{_datadir}/applications
# install desktop file
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{S:100}

%ldconfig_scriptlets

%files
%license COPYING.LIB
%{_bindir}/ninewinecfg
%{_libdir}/wine/d3d9-nine.dll.so
%{_libdir}/wine/ninewinecfg.exe.so
%{_libdir}/wine/fakedlls/d3d9-nine.dll
%{_libdir}/wine/fakedlls/ninewinecfg.exe
%{_datadir}/applications/wine-ninecfg.desktop

%changelog
* Sun Mar 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.0_2-1
- 3.0_2

* Fri Jan 26 2018 Phantom X <megaphantomx at bol dot com dot br>
- 3.0_1

* Wed Nov 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0_3-2
- Fix desktop file

* Tue Nov 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0_3-1
- Initial spec
