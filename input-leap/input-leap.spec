%global commit 8efd4dd66301d6748801848b7bc39a9b4ed34627
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250226
%bcond snapshot 1

%bcond qt 1
# build with qt6 instead 5
%bcond qt6 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%{?with_qt6:%global qt_ver 6}%{!?with_qt6:%global qt_ver 5}
%global appname io.github.input_leap.input-leap

Name:           input-leap
Version:        3.0.2
Release:        2%{?dist}
Summary:        Keyboard and mouse sharing solution

License:        GPL-2.0-only
URL:            https://github.com/%{name}/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(avahi-compat-libdns_sd)
BuildRequires:  cmake(ghc_filesystem)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
%if %{with qt}
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cmake(Qt%{qt_ver}Core)
BuildRequires:  cmake(Qt%{qt_ver}Gui)
BuildRequires:  cmake(Qt%{qt_ver}LinguistTools)
BuildRequires:  cmake(Qt%{qt_ver}Network)
BuildRequires:  cmake(Qt%{qt_ver}Widgets)
%if %{with qt6}
BuildRequires:  cmake(Qt6Core5Compat)
%endif
Requires:       hicolor-icon-theme
%endif

%description
Input Leap allows you to share one mouse and keyboard between multiple
computers.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed \
  -e '/include (CheckIncludeFiles)/i\    set(CMAKE_AR "/usr/bin/gcc-ar")' \
  -e '/include (CheckIncludeFiles)/i\    set(CMAKE_RANLIB "/usr/bin/gcc-ranlib")' \
  -e '/gulrak-filesystem/d' \
  -i CMakeLists.txt

sed \
  -e 's|EQUAL 8 OR|EQUAL 7 OR|g' \
  -e 's|\.b${INPUTLEAP_BUILD_NUMBER}||g' \
  -e 's|-${INPUTLEAP_VERSION_STAGE}||g' \
  -i cmake/Version.cmake


%build
%{cmake3} \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%if %{without qt}
  -DINPUTLEAP_BUILD_GUI:BOOL=OFF \
%else
  -DQT_DEFAULT_MAJOR_VERSION:STRING=%{qt_ver} \
%endif
  -DINPUTLEAP_USE_EXTERNAL_GTEST:BOOL=ON \
%if %{with snapshot}
  -DINPUTLEAP_VERSION_STAGE:STRING=snapshot \
  -DINPUTLEAP_REVISION="%{shortcommit}" \
  -DINPUTLEAP_BUILD_NUMBER="%{shortcommit}" \
%else
  -DINPUTLEAP_VERSION_STAGE:STRING=stable \
%endif
%{nil}

%cmake_build


%install
%cmake_install

%check
%if %{with qt}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml
%endif


%files
%license LICENSE
%doc README.md doc/%{name}.conf.example*
%{_bindir}/%{name}c
%{_bindir}/%{name}s
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*.1*
%if %{with qt}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/%{appname}.appdata.xml
%endif


%changelog
* Sat Nov 23 2024 Phantom X <megaphantomx at hotmail dot com> - 3.0.2-1.20241111git2641bc5
- 3.0.2

* Tue Feb 27 2024 Phantom X <megaphantomx at hotmail dot com> - 2.4.0-3.20240226git6cfeacd
- Qt 6

* Fri Feb 17 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4.0-1.20230130git68aac94
- Initial spec
