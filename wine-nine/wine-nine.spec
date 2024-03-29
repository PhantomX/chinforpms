%undefine _auto_set_build_flags
%define _fortify_level 0
%undefine _hardened_build
%undefine _package_note_file

# Disable LTO
%global _lto_cflags %{nil}

%global commit 27e1737950d80edee38802833786ee378c920358
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210327
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%ifarch %{ix86}
%global winearchdir i386-windows
%global winesodir i386-unix
%endif
%ifarch x86_64
%global winearchdir x86_64-windows
%global winesodir x86_64-unix
%endif

%global winecommonver 6.1

%global pkgname wine-nine-standalone

Name:           wine-nine
Version:        0.9
Release:        2%{?dist}
Summary:        Wine D3D9 interface library for Mesa's Gallium Nine statetracker

Epoch:          2

License:        LGPLv2+
URL:            https://github.com/iXit/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        ninewinecfg
Source2:        wineninecfg

Source100:      wine-ninecfg.desktop

Patch0:         %{url}/commit/95e0da48ad713fb4bc54011c96b06088fd6a0c83.patch#/%{name}-gh-95e0da4.patch

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
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

sed -e "/strip =/s|=.*|= 'true'|g" -i tools/cross-wine*.in

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=[0-9]//'` -Wno-error"

TEMP_CFLAGS="`mesonarray "${TEMP_CFLAGS}"`"
TEMP_LDFLAGS="`mesonarray "%{build_ldflags}"`"

sed \
  -e "/^c_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^c_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
  -i tools/cross-wine*.in

./bootstrap.sh

%build
export WINEPREFIX="$(pwd)/%{_vpath_builddir}/wine-build"

meson \
  --cross-file tools/cross-wine%{__isa_bits} \
  --buildtype "release" \
  %{_vpath_builddir}

%ninja_build -C %{_vpath_builddir}


%install
mkdir -p %{buildroot}%{_libdir}/wine/%{winearchdir}
mkdir -p %{buildroot}%{_libdir}/wine/%{winesodir}

install -pm0755 %{_vpath_builddir}/ninewinecfg/ninewinecfg.exe.so \
  %{buildroot}%{_libdir}/wine/%{winesodir}/ninewinecfg.exe.so
install -pm0755 %{_vpath_builddir}/ninewinecfg/ninewinecfg.exe.fake \
  %{buildroot}%{_libdir}/wine/%{winearchdir}/ninewinecfg.exe

install -pm0755 %{_vpath_builddir}/d3d9-nine/d3d9-nine.dll.so \
  %{buildroot}%{_libdir}/wine/%{winesodir}/d3d9-nine.dll.so
install -pm0644 %{_vpath_builddir}/d3d9-nine/d3d9-nine.dll.fake \
  %{buildroot}%{_libdir}/wine/%{winearchdir}/d3d9-nine.dll

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:1} %{buildroot}%{_bindir}/ninewinecfg
install -pm0755 %{S:2} %{buildroot}%{_bindir}/wineninecfg

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
%{_libdir}/wine/%{winesodir}/d3d9-nine.dll.so
%{_libdir}/wine/%{winesodir}/ninewinecfg.exe.so
%{_libdir}/wine/%{winearchdir}/d3d9-nine.dll
%{_libdir}/wine/%{winearchdir}/ninewinecfg.exe
%{_datadir}/applications/wine-ninecfg.desktop


%changelog
* Sat Mar 11 2023 Phantom X <megaphantomx at hotmail dot com> - 2:0.9-1
- 0.9

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 2:0.8-5
- Undefine _package_note_file

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 2:0.8-4
- Update script to architecture-specific library directories

* Tue Apr 27 2021 Phantom X <megaphantomx at hotmail dot com> - 2:0.8-3
- Update script to architecture-specific dll directories

* Sun Apr 25 2021 Phantom X <megaphantomx at hotmail dot com> - 2:0.8-2
- Update script

* Fri Apr 16 2021 Phantom X <megaphantomx at hotmail dot com> - 2:0.8-1
- 0.8

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 2:0.8-0.2.20210327git27e1737
- Bump

* Fri Mar 05 2021 Phantom X <megaphantomx at hotmail dot com> - 2:0.8-0.1.20210117gitbddb53a
- Snapshot for newer wine

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
