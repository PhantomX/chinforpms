%global commit 68aac94193a721e4c20512434cf6ab40a2dd89a0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230130
%global with_snapshot 1

%bcond_without qt

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           input-leap
Version:        2.4.0
Release:        1%{?gver}%{?dist}
Summary:        Keyboard and mouse sharing solution

License:        GPL-2.0-only
URL:            https://github.com/%{name}/%{name}

%if 0%{?with_snapshot}
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
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Widgets)
Requires:       hicolor-icon-theme
%endif

%description
Input Leap allows you to share one mouse and keyboard between multiple
computers.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

sed \
  -e 's|<id></id>|<id>%{name}.desktop</id>|g' \
  -e 's|barrier|%{name}|g' \
  -i res/%{name}.appdata.xml.in

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
%if %{without qt}
  -DINPUTLEAP_BUILD_GUI:BOOL=OFF \
%endif
  -DINPUTLEAP_USE_EXTERNAL_GTEST:BOOL=ON \
%if 0%{?with_snapshot}
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

desktop-file-install \
  --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  --set-name="InputLeap" \
  --set-key=Exec \
  --set-value="%{name}" \
  --set-icon="%{name}" \
  --remove-category=Utility \
  --add-category=Network \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%check
%if %{with qt}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml
%endif


%files
%license LICENSE
%doc README.md doc/%{name}.conf.example*
%{_bindir}/%{name}c
%{_bindir}/%{name}s
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*.1*
%if %{with qt}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{name}.appdata.xml
%endif


%changelog
* Fri Feb 17 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4.0-1.20230130git68aac94
- Initial spec
