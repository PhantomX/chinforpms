%undefine _cmake_shared_libs

%global commit 7ad17ae39719d3dca80ea715e88c66ce7013ccea
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220204
%global with_snapshot 1

# Enable system boost
%bcond_without boost
# Enable ffmpeg support
%bcond_with ffmpeg
# Disable Qt build
%bcond_without qt

%global commit1 a8cbfd9af4f3f3cdad6efcd067e76edec76c1338
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dynarmic

%global commit2 1e80a47dffbda813604f0913e2ad68c7054c14e4
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 inih

%global commit3 a39596358a3a5488c06554c0c15184a6af71e433
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 sirit

%global commit4 1de435ed04c8e74775804da944d176baf0ce56e2
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 xbyak

%global commit5 a3fdfe81465d57efc97cfd28ac6c8190fb31a6c8
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%undefine _hardened_build
%undefine _cmake_shared_libs

%global glad_ver 0.1.29

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/yuzu-emu

Name:           yuzu
Version:        0
Release:        0%{?gver}%{?dist}
Summary:        A Nintendo Switch Emulator

License:        GPLv2
URL:            https://yuzu-emu.org

%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        https://github.com/MerryMage/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/ReinUsesLisp/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/benhoyt/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/herumi/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/KhronosGroup/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz

Source20:       https://api.yuzu-emu.org/gamedb#/compatibility_list.json

Patch0:         0001-Use-system-libraries.patch
%if %{with boost}
Patch1:         0001-fix-system-boost-detection.patch
%endif

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  boost-devel >= 1.76.0
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(fmt) >= 8.0.1
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(liblz4)
#BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libzstd) >= 1.5.0
BuildRequires:  pkgconfig(nlohmann_json) >= 3.8.0
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(sdl2)
%if %{with qt}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  qt5-linguist
%endif
BuildRequires:  vulkan-headers
BuildRequires:  pkgconfig(zlib)

BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info

Provides:       bundled(dynarmic) = 0~git%{shortcommit1}
Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(microprofile)
Provides:       bundled(inih) = 0~git%{shortcommit2}
Provides:       bundled(xbyak) = 0~git%{shortcommit3}


%description
Yuzu is an open-source Nintendo Switch emulator written in C++.


%package qt
Summary:        A Nintendo Switch Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
Yuzu is an open-source Nintendo Switch emulator written in C++.

This is the Qt frontend.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

tar -xf %{S:1} -C externals/dynarmic --strip-components 1
tar -xf %{S:2} -C externals/inih/inih --strip-components 1
tar -xf %{S:3} -C externals/sirit --strip-components 1
tar -xf %{S:4} -C externals/xbyak --strip-components 1
tar -xf %{S:5} -C externals/sirit/externals/SPIRV-Headers --strip-components 1


sed \
  -e '/-pedantic-errors/d' \
  -i externals/dynarmic/CMakeLists.txt

%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

%if 0%{?with_snapshot}
  sed \
    -e 's|@GIT_REV@|%{commit}|g' \
    -e 's|@GIT_BRANCH@|HEAD|g' \
    -e 's|@GIT_DESC@|%{shortcommit}|g' \
    -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
    -i src/common/scm_rev.cpp.in
%endif

%build
mkdir -p dist/compatibility_list/
cp %{S:20} dist/compatibility_list/

%if 0%{?with_snapshot}
export CI=true
export TRAVIS=true
export TRAVIS_REPO_SLUG=%{name}/%{name}-nightly
export TRAVIS_TAG="%{version}-%{release}"
%endif

%cmake \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%else
  ENABLE_QT:BOOL=OFF \
%endif
  -DYUZU_USE_EXTERNAL_SDL2:BOOL=OFF \
  -DYUZU_USE_BUNDLED_FFMPEG:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPUS:BOOL=OFF \
  -DYUZU_FIX_CMAKE_BOOST:BOOL=ON \
  -DYUZU_TESTS:BOOL=OFF \
  -DENABLE_WEB_SERVICE:BOOL=OFF \
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=OFF \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

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
* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20190921git223bfc9
- New snapshot

* Wed Apr 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20190423gitb9e51f0
- Disable telemetry initial dialog
- Update version strings

* Tue Apr 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20190423gitb9e51f0
- Initial spec
