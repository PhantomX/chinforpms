%global commit b88fc0130e7c9b5a8e5e86c51a69c8d3c9fd0c1b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210901
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global appname io.github.%{name}.%{name}

Name:           antimicrox
Version:        3.5.1
Release:        100%{?dist}
Summary:        Graphical program used to map keyboard buttons and mouse controls to a gamepad

License:        GPL-3.0-or-later
URL:            https://github.com/AntiMicroX/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Use-system-SDL_GameControllerDB.patch

ExcludeArch:    %{arm}

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core) >= 5.10
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(sdl2) >= 2.0.6
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  gettext
BuildRequires:  itstool
BuildRequires:  libappstream-glib
BuildRequires:  systemd
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb

Provides:       antimicroX = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       AntiMicroX = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description
antimicroX is a graphical program used to map keyboard keys and mouse controls
to a gamepad. This program is useful for playing PC games using a gamepad that
do not have any form of built-in gamepad support.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

find src -type f \( -name '*.c*' -o -name '*.h*' \) -exec chmod -x {} ';'

sed \
  -e 's|\/usr\/lib\/udev\/rules.d|%{_udevrulesdir}|g' \
  -e '/\/doc\/%{name}/d' \
  -i CMakeLists.txt

sed -e '/^SUBSYSTEM/s|$|, OPTIONS+="static_node=uinput"|' -i other/60-%{name}-uinput.rules

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' \
  -i src/sdleventreader.cpp


%build
%cmake \
  -DANTIMICROX_PKG_VERSION="%{version}-%{release}" \
  -DUSE_QT6_BY_DEFAULT=ON \
  -DWITH_X11:BOOL=ON \
  -DWITH_XTEST:BOOL=ON \
  -DWITH_UINPUT:BOOL=ON \
  -DAPPDATA:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

rm -f %{buildroot}%{_datadir}/%{name}/CHANGELOG.md
rm -f %{buildroot}%{_datadir}/%{name}/gamecontrollerdb.txt
rm -f %{buildroot}%{_datadir}/%{name}/LICENSE_SDL_GameControllerDB

rm -rf %{buildroot}%{_includedir}

%find_lang %{name} --with-qt

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop


%files -f %{name}.lang
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/translations/%{name}.qm
%{_datadir}/applications/*.desktop
%{_datadir}/icons/*/*/apps/*
%{_datadir}/mime/packages/%{appname}.xml
%{_mandir}/man1/*.1*
%{_metainfodir}/%{appname}.appdata.xml
%{_udevrulesdir}/60-%{name}-uinput.rules


%changelog
* Wed Feb 05 2025 Phantom X <megaphantomx at hotmail dot com> - 3.5.1-100
- 3.5.1
- Qt6

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 3.4.1-100
- 3.4.1

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 3.4.0-101
- BR: Qt5LinguistTools

* Sun Mar 10 2024 Phantom X <megaphantomx at hotmail dot com> - 3.4.0-100
- 3.4.0

* Sat Aug 26 2023 Phantom X <megaphantomx at hotmail dot com> - 3.3.4-100
- 3.3.4

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 3.3.3-100
- 3.3.3

* Wed Nov 16 2022 Phantom X <megaphantomx at hotmail dot com> - 3.3.1-100
- 3.3.1

* Fri Aug 19 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.5-100
- 3.2.5

* Sun Jun 12 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.4-100
- 3.2.4

* Wed Apr 27 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.3-100
- 3.2.3

* Thu Feb 24 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.2-100
- 3.2.2

* Tue Jan 04 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.1-100
- 3.2.1
- R: sdl_gamecontrollerdb

* Thu Nov 18 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-100
- 3.2.0

* Fri Sep 10 2021 Phantom X <megaphantomx at hotmail dot com> - 3.1.7-100
- 3.1.7

* Wed Sep 01 2021 Phantom X <megaphantomx at hotmail dot com> - 3.1.6-100.20210901gitb88fc01
- 3.1.6

* Sat Apr 17 2021 Phantom X <megaphantomx at hotmail dot com> - 3.1.5-100
- 3.1.5

* Wed Feb 03 2021 Phantom X <megaphantomx at hotmail dot com> - 3.1.4-100
- 3.1.4

* Sat Dec 05 2020 Phantom X <megaphantomx at hotmail dot com> - 3.1.3-100.20201105git4006ea9
- New snapshot
- libantilib removed

* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 3.1.1-100.20200917git61ce55f
- 3.1.1
- New project and files renaming

* Tue Jul 07 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0-101.20200707git80f6198
- New snapshot
- Remove icons hack

* Sun Jun 28 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0-100.20200625gitdcf23b7
- Snapshot
- Rawhide sync
- Fix icons display on interface

* Fri Jun 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.0-2
- Fix to use a better colorful tray icon

* Fri Jun 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.0-1
- Initial spec
