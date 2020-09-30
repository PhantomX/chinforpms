%undefine _hardened_build
# Disable LTO
%define _lto_cflags %{nil}

%global commit bf71ae00220265749cc6af1e1e81f5b287891e0a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200520
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global winecommonver 5.14

%global pkgname wine-nine-standalone

Name:           wine-nine
Version:        0.7
Release:        1%{?gver}%{?dist}
Summary:        Wine D3D9 interface library for Mesa's Gallium Nine statetracker

Epoch:          2

License:        LGPLv2+
URL:            https://github.com/iXit/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        ninewinecfg
Source2:        wineninecfg

Source100:      wine-ninecfg.desktop

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(d3d)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-dri2)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xproto)
BuildRequires:  wine-devel

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Requires:       libglvnd-egl%{?_isa}
Requires:       libglvnd-glx%{?_isa}
Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-libd3d%{?_isa}
Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       ninewinecfg.exe.so%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d9-nine.dll.so%{?_isa} = %{?epoch:%{epoch}:}%{version}

%description
%{summary} and tool to setting it.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

sed -e "/strip =/s|=.*|= 'true'|g" -i tools/cross-wine*.in

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

TEMP_CFLAGS="`mesonarray "${TEMP_CFLAGS}"`"
TEMP_LDFLAGS="`mesonarray "%{build_ldflags}"`"

sed \
  -e "/^c_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^c_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
  -i tools/cross-wine*.in

./bootstrap.sh

%build
export WINEPREFIX="$(pwd)/%{_target_platform}/wine-build"

meson \
  --cross-file tools/cross-wine%{__isa_bits} \
  --buildtype "release" \
  %{_target_platform}

%ninja_build -C %{_target_platform}


%install
mkdir -p %{buildroot}/%{_libdir}/wine
mkdir -p %{buildroot}/%{_libdir}/wine/fakedlls

install -pm0755 %{_target_platform}/ninewinecfg/ninewinecfg.exe.so \
  %{buildroot}/%{_libdir}/wine/ninewinecfg.exe.so
install -pm0755 %{_target_platform}/ninewinecfg/ninewinecfg.exe.fake \
  %{buildroot}/%{_libdir}/wine/fakedlls/ninewinecfg.exe

install -pm0755 %{_target_platform}/d3d9-nine/d3d9-nine.dll.so \
  %{buildroot}/%{_libdir}/wine/d3d9-nine.dll.so
install -pm0755 %{_target_platform}/d3d9-nine/d3d9-nine.dll.fake \
  %{buildroot}/%{_libdir}/wine/fakedlls/d3d9-nine.dll

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:1} %{buildroot}/%{_bindir}/ninewinecfg
install -pm0755 %{S:2} %{buildroot}/%{_bindir}/wineninecfg

mkdir -p %{buildroot}%{_datadir}/applications
# install desktop file
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{S:100}


%files
%doc README.rst
%license LICENSE
%{_bindir}/ninewinecfg
%{_bindir}/wineninecfg
%{_libdir}/wine/d3d9-nine.dll.so
%{_libdir}/wine/ninewinecfg.exe.so
%{_libdir}/wine/fakedlls/d3d9-nine.dll
%{_libdir}/wine/fakedlls/ninewinecfg.exe
%{_datadir}/applications/wine-ninecfg.desktop


%changelog
* Wed Aug 19 2020 Phantom X <megaphantomx at hotmail dot com> - 2:0.7-1
- 0.7

* Sat Aug 15 2020 Phantom X <megaphantomx at hotmail dot com> - 2:0.6-1
- 0.6

* Wed Aug 05 2020 Phantom X <megaphantomx at hotmail dot com> - 2:0.6-0.3.20200520gitbf71ae0
- New snapshot
- Experimental fix to work with wine 5.14

* Sat Apr 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 2:0.6-0.2.20191210git6eda08e
- Fix winepath EOL on script

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 2:0.6-0.1.20191210git6eda08e
- New snapshot

* Wed Sep 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.5-1
- 0.5

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.5-0.3.20190420git5a9da8f
- Fix obsoletes

* Mon Apr 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.5-0.1.20190420git5a9da8f
- New snapshot
- Remove meson fix
- Bump minimal wine version

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.4-1
- 0.4

* Fri Mar 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.4-0.2.20190312git30992a8
- New snapshot
- Set WINEPREFIX
- Temporary fix for meson 0.50

* Tue Feb 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.4-0.1.20190225giteeeb350
- New snapshot

* Sat Feb 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.3-0.1.20190216gite55dcab
- New snapshot
- Install official fake dlls

* Sun Feb 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:0.2-1
- 0.2.0.0 final
- Update urls

* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.2.0.0-2.20190121git13e9b40
- New snapshot

* Tue Jan 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.2.0.0-1.20190115gitacc17f4
- New snapshot

* Mon Jan 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.1.0.0-2.20190107git136dca6
- Fix fake dll module name

* Mon Jan 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.1.0.0-1.20190107git136dca6
- Change to Nine Standalone

* Sat Dec 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.0_2-2
- Add upstream patches

* Sun Mar 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.0_2-1
- 3.0_2

* Fri Jan 26 2018 Phantom X <megaphantomx at bol dot com dot br>
- 3.0_1

* Wed Nov 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0_3-2
- Fix desktop file

* Tue Nov 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0_3-1
- Initial spec
