%global commit 8722b970c52f2c0d8e82561477edb62a53ae9dbb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200321
%global with_snapshot 1

# Enable ffmpeg support
%bcond_with ffmpeg
# Disable Qt build
%bcond_without qt

%global commit1 15cf3caaceb21172ea42a24e595a2eb58c3ec960
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 Catch

%global commit2 f320e7d92a33ee80ae42deef79da78cfc30868af
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 cryptopp

%global commit3 4e6848d1c9e8dadc70595c15b5589f8b14aad478
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 dynarmic

%global commit4 4b8f8fac96a7819f28f4be523ca10a2d5d8aaaf2
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 fmt

%global commit5 2023872dfffb38b6a98f2c45a0eb25652aaea91f
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 inih

%global commit6 fd69de1a1b960ec296cc67d32257b0f9e2d89ac6
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 nihstro

%global commit7 060181eaf273180d3a7e87349895bd0cb6ccbf4a
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 ext-soundtouch

%global commit8 e6ea0eae656c022d7878ffabc4e016b3e6f0c536
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 teakra

%global commit9 1de435ed04c8e74775804da944d176baf0ce56e2
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 xbyak

%global commit10 31d9704fdcca0b68fb9656d4764fa0fb60e460c2
%global shortcommit10 %(c=%{commit9}; echo ${c:0:7})
%global srcname10 lodepng

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%undefine _hardened_build

%global vc_url  https://github.com/citra-emu

Name:           citra
Version:        0
Release:        7%{?gver}%{?dist}
Summary:        A Nintendo 3DS Emulator

License:        GPLv2
URL:            https://citra-emu.org

%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        https://github.com/philsquared/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/weidai11/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/MerryMage/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/fmtlib/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/benhoyt/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/neobrain/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        %{vc_url}/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        https://github.com/wwylele/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        https://github.com/herumi/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       https://github.com/lvandeve/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz

Source20:       https://api.citra-emu.org/gamedb#/compatibility_list.json

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Disable-telemetry-initial-dialog.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  boost-devel
BuildRequires:  cmake(cubeb)
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
%endif
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(sdl2)
%if %{with qt}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  qt5-linguist
%endif

BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info


%description
Citra is an experimental open-source Nintendo 3DS emulator/debugger
written in C++.


%package qt
Summary:        A Nintendo 3DS Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
Citra is an experimental open-source Nintendo 3DS emulator/debugger
written in C++.

This is the Qt frontend.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

tar -xf %{S:1} -C externals/catch --strip-components 1
tar -xf %{S:2} -C externals/cryptopp/cryptopp --strip-components 1
tar -xf %{S:3} -C externals/dynarmic --strip-components 1
tar -xf %{S:4} -C externals/fmt --strip-components 1
tar -xf %{S:5} -C externals/inih/inih --strip-components 1
tar -xf %{S:6} -C externals/nihstro --strip-components 1
tar -xf %{S:7} -C externals/soundtouch --strip-components 1
tar -xf %{S:8} -C externals/teakra --strip-components 1
tar -xf %{S:9} -C externals/xbyak --strip-components 1
tar -xf %{S:10} -C externals/lodepng/lodepng --strip-components 1

sed -e '/ENABLE_WEB_SERVICE/s|ON|OFF|g' -i CMakeLists.txt

sed -e 's|-pedantic-errors||g' -i externals/fmt/CMakeLists.txt

sed \
  -e '/-Wfatal-errors/d' \
  -e '/-pedantic-errors/d' \
  -i externals/teakra/CMakeLists.txt externals/dynarmic/CMakeLists.txt

sed -e '/^#include <exception>/a#include <system_error>' \
  -i externals/teakra/src/interpreter.h

%if 0%{?with_snapshot}
  sed \
    -e 's|@GIT_REV@|%{commit}|g' \
    -e 's|@GIT_BRANCH@|HEAD|g' \
    -e 's|@GIT_DESC@|%{shortcommit}|g' \
    -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
    -i src/common/scm_rev.cpp.in
%endif

%build
%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')

mkdir -p %{_target_platform}
pushd %{_target_platform}

mkdir -p dist/compatibility_list/
cp %{S:20} dist/compatibility_list/

%if 0%{?with_snapshot}
export CI=true
export TRAVIS=true
export TRAVIS_REPO_SLUG=%{name}/%{name}-nightly
export TRAVIS_TAG="%{version}-%{release}"
%endif

%cmake .. \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%else
  ENABLE_QT:BOOL=OFF \
%endif
%if %{with ffmpeg}
  -DENABLE_FFMPEG:BOOL=ON \
%endif
  -DENABLE_WEB_SERVICE:BOOL=OFF \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=ON \
%{nil}

%make_build

popd


%install
%make_install -C %{_target_platform}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license license.txt
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-room
%{_mandir}/man6/%{name}.6*


%if %{with qt}
%files qt
%{_bindir}/%{name}-qt
%license license.txt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man6/%{name}-qt.6*
%endif


%changelog
* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-7.20200321git8722b97
- New snapshot

* Sun Mar 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-6.20200312gitad3c464
- Bump

* Thu Feb 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-5.20200204git821a35b
- New snapshot
- libzstd

* Sun Jan 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-4.20200101git01686f7
- New snapshot
- lodepng

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20190921git223bfc9
- New snapshot

* Wed Apr 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20190423gitb9e51f0
- Disable telemetry initial dialog
- Update version strings

* Tue Apr 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20190423gitb9e51f0
- Initial spec
