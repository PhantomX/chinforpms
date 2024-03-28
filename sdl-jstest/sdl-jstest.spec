%global commit ae5dc5619fc1d6a26591b1e98edb81905eb891ed
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240126
%bcond_without snapshot

%global commit1 ad3e98dbc86157cce04e60343965970cb812e92e
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 tinycmmc

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/grumbel

Name:           sdl-jstest
Version:        0.2.2
Release:        2%{?dist}
Summary:        Simple SDL joystick test application for the console

License:        GPL-3.0-only
URL:            %{vc_url}/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{vc_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz

Patch0:         0001-Use-system-SDL_GameControllerDB.patch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(sdl2)
Requires:       sdl_gamecontrollerdb

Provides:       bundled(%{srcname1}) = 0~git%{shortcommit1}


%description
sdl2-jstest is a simple program that lets you find out how many
joysticks SDL2 detected on your system, how many axes, buttons,
hats and balls they have each. They also lets you test the joysticks
by displaying the events they send or by displaying their current
button, axis, hat or ball state. sdl-jstest is especially useful if
you want to test your SDL_LINUX_JOYSTICK configuration.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

tar -xf %{SOURCE1} -C external/tinycmmc --strip-components 1

%if %{with snapshot}
sed -i \
  -e '/Git REQUIRED/d' \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} describe.*$|echo \"%{version}-%{release}\"|g" \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} log.*$|echo \"%{date}\"|g" \
  CMakeLists.txt
%endif
echo %{version}-%{release} > VERSION

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' -i src/sdl2-jstest.c


%build
%cmake \
  -DBUILD_SDL_JSTEST:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/sdl*-jstest
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/sdl*-jstest.1*


%changelog
* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.2.2-1.20230913git5bc418e
- 0.2.2

* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.1-0.2.20180715gitaafbdb1
- BR: gcc-c++

* Thu Sep 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.1-0.1.20180715gitaafbdb1
- Initial spec
