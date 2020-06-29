%global commit dcf23b7e7f392c2b296bec6ea86477a790823283
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200625
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname antimicroX
%global appname com.github.juliagoda.%{pkgname}
%global libname libantilib

Name:           antimicrox
Version:        3.0
Release:        100%{?gver}%{?dist}
Summary:        Graphical program used to map keyboard buttons and mouse controls to a gamepad

License:        GPLv3+
URL:            https://github.com/juliagoda/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

ExcludeArch:    %{arm}

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  gettext
BuildRequires:  itstool
BuildRequires:  libappstream-glib
Requires:       hicolor-icon-theme

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
antimicroX is a graphical program used to map keyboard keys and mouse controls
to a gamepad. This program is useful for playing PC games using a gamepad that
do not have any form of built-in gamepad support.


%package %{libname}
Summary:        %{name} libraries
%description %{libname}
Contains library files required for running %{name}.

%package %{libname}-devel
Summary:        Development files for %{libname}
Requires:       %{name}-%{libname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description %{libname}-devel
The %{libname}-devel package contains libraries and header files for %{libname}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

find src -type f \( -name "*.cpp" -o -name "*.h" \) -exec chmod -x {} ';'

sed \
  -e '/APPEND LIBS/s|${X11_X11_LIB}|\0 xcb|' \
  -e '/\/doc\/%{pkgname}/d' \
  -i CMakeLists.txt

ln -sf %{pkgname}.png src/images/%{pkgname}_trayicon.png

# FIXME: ugly hack to display proper icons
sed \
  -e 's|QIcon(":/icons|QIcon("%{_datadir}/%{pkgname}/icons|g' \
  -i src/joytabwidget.cpp src/mainwindow.cpp src/mainsettingsdialog.cpp src/stickpushbuttongroup.cpp \
     src/keyboard/virtualkeyboardmousewidget.cpp src/dpadpushbuttongroup.cpp


%build
%cmake . -B %{_target_platform} \
  -DWITH_X11:BOOL=ON \
  -DWITH_XTEST:BOOL=ON \
  -DWITH_UINPUT:BOOL=ON \
  -DAPPDATA:BOOL=ON \
%{nil}

%make_build -C %{_target_platform}


%install
%make_install -C %{_target_platform}

rm -f %{buildroot}%{_datadir}/%{pkgname}/icons/hicolor/index.theme
rm -f %{buildroot}%{_datadir}/%{pkgname}/Changelog

%find_lang %{pkgname} --with-qt

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/%{appname}.desktop


%files -f %{pkgname}.lang
%license LICENSE
%doc Changelog README.md
%{_bindir}/%{pkgname}
%dir %{_datadir}/%{pkgname}
%dir %{_datadir}/%{pkgname}/translations
%{_datadir}/%{pkgname}/icons
%{_datadir}/%{pkgname}/images
%{_datadir}/%{pkgname}/translations/%{pkgname}.qm
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{appname}.xml
%{_mandir}/man1/*.1*
%{_metainfodir}/%{appname}.appdata.xml

%files %{libname}
%license LICENSE
%{_libdir}/%{libname}.so.1

%files %{libname}-devel
%{_includedir}/%{pkgname}
%{_libdir}/%{libname}.so


%changelog
* Sun Jun 28 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0-100.20200625gitdcf23b7
- Snapshot
- Rawhide sync
- Fix icons display on interface

* Fri Jun 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.0-2
- Fix to use a better colorful tray icon

* Fri Jun 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.0-1
- Initial spec
