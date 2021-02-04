%global commit 4006ea97161254026c22c345d03c264bdce87f30
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20201105
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global appname io.github.%{name}.%{name}

Name:           antimicrox
Version:        3.1.4
Release:        100%{?gver}%{?dist}
Summary:        Graphical program used to map keyboard buttons and mouse controls to a gamepad

License:        GPLv3+
URL:            https://github.com/AntiMicroX/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

ExcludeArch:    %{arm}

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5Core) >= 5.8
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  pkgconfig(sdl2) >= 2.0.6
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  gettext
BuildRequires:  itstool
BuildRequires:  libappstream-glib
Requires:       hicolor-icon-theme

Provides:       antimicroX = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       AntiMicroX = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description
antimicroX is a graphical program used to map keyboard keys and mouse controls
to a gamepad. This program is useful for playing PC games using a gamepad that
do not have any form of built-in gamepad support.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

find src -type f \( -name "*.cpp" -o -name "*.h" \) -exec chmod -x {} ';'

sed \
  -e '/\/doc\/%{name}/d' \
  -i CMakeLists.txt

cp -f src/images/48x48/%{appname}.png src/images/48-apps-%{name}_trayicon.png
cp -f src/images/48x48/%{appname}.png src/images/breeze_themed/48-apps-%{name}_trayicon.png

%build
%cmake \
  -DWITH_X11:BOOL=ON \
  -DWITH_XTEST:BOOL=ON \
  -DWITH_UINPUT:BOOL=ON \
  -DAPPDATA:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

rm -f %{buildroot}%{_datadir}/%{name}/CHANGELOG.md

rm -rf %{buildroot}%{_includedir}

%find_lang %{name} --with-qt

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/%{appname}.desktop


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


%changelog
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
