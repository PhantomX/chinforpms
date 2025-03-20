# Selective LTO.
%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond_with clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit eaa9c9e3a46eb5099193b11d620ddfe96b6aec83
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250222
%bcond_without snapshot

# Enable system boost
%bcond_without boost
# Enable system dynarmic
%bcond_without dynarmic
# Enable system ffmpeg
%bcond_without ffmpeg
# Enable system fmt
%bcond_without fmt
# Enable system mbedtls (needs cmac builtin support)
%bcond_with mbedtls
# Disable Qt build
%bcond_without qt
# build with qt6 instead 5
%bcond_without qt6
# Build tests
%bcond_with tests
%bcond_without vma
# Enable webservice
%bcond_without webservice

%global commit10 c788c52156f3ef7bc7ab769cb03c110a53ac8fcb
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 VulkanMemoryAllocator

%global commit11 382ddbb4b92c0b26aa1b32cefba2002119a5b1f2
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 simpleini

%global commit12 a609330e4c6374f741d3b369269f7848255e1954
%global shortcommit12 %(c=%{commit12}; echo ${c:0:6})
%global srcname12 cpp-httplib

%global commit13 10ef5735d842b31025f1257ae78899f50a40fb14
%global shortcommit13 %(c=%{commit13}; echo ${c:0:6})
%global srcname13 cpp-jwt

%global commit14 97929690234f2b4add36b33657fe3fe09bd57dfd
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 tzdb_to_nx

%global commit140 16ce126a87c5f130cde8b8dce73b38952a19f085
%global shortcommit140 %(c=%{commit140}; echo ${c:0:7})
%global srcname140 tz

%global commit15 e0db1f51d6ddf9eb2c1314c23d063a29255b607a
%global shortcommit12 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 FFmpeg

%global fmt_ver 11.0.2
%global glad_ver 0.1.29
%global nxtzdb_ver 221202
%global stbdxt_ver 1.12
%global vkh_ver 1.3.246
%{?with_qt6:%global qt_ver 6}%{!?with_qt6:%global qt_ver 5}

%dnl %global vc_url   https://notabug.org/litucks/torzu
%global vc_url  http://vub63vv26q6v27xzv2dtcd25xumubshogm67yrpaz2rculqxs7jlfqad.onion/torzu-emu/torzu

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%else
%global shortcommit 0
%endif

%global appname onion.%{name}_emu.%{name}


%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "\\\\.", "-"); print(ver)}

Name:           torzu
Version:        2024.08.10
Release:        4%{?dist}
Summary:        A NX Emulator

License:        GPL-2.0-or-later AND MIT AND Apache-2.0 WITH LLVM-exception AND MPL-2.0%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_mbedtls: AND (Apache-2.0 OR GPL-2.0-or-later)}%{!?with_boost: AND BSL-1.0}
URL:            http://vub63vv26q6v27xzv2dtcd25xumubshogm67yrpaz2rculqxs7jlfqad.onion/torzu-emu/torzu

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{name}-%{ver}/%{name}-%{ver}.tar.gz
%endif

%if %{without vma}
Source10:        https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%endif
Source11:        https://github.com/brofield/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%if %{with webservice}
Source12:        https://github.com/yhirose/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
Source13:        https://github.com/arun11299/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%endif
Source14:        https://github.com/lat9nq/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
Source140:       https://github.com/eggert/%{srcname140}/archive/%{commit140}/%{srcname140}-%{shortcommit140}.tar.gz
%if %{without ffmpeg}
Source15:       https://github.com/FFmpeg/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%endif
%if %{without fmt}
Source16:        https://github.com/fmtlib/fmt/archive/%{fmt_ver}/fmt-%{fmt_ver}.tar.gz
%endif

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-boost-build-fix.patch
Patch12:        0001-Fix-48e86d6.patch

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  llvm-devel >= 17.0.2
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
%if %{with boost}
BuildRequires:  boost-devel >= 1.79.0
%endif
%if %{with tests}
BuildRequires:  pkgconfig(catch2) >= 2.13.7
%endif
BuildRequires:  cmake(cubeb)
%if %{with dynarmic}
BuildRequires:  cmake(dynarmic) >= 6.7.0
%else
BuildRequires:  cmake(tsl-robin-map)
Provides:       bundled(dynarmic) = 0~git%{?shortcommit1}
%endif
BuildRequires:  pkgconfig(gamemode) >= 1.7
BuildRequires:  glslang
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libbrotlienc)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
%if %{with fmt}
BuildRequires:  cmake(fmt) >= 11
%else
Provides:       bundled(fmt) = %{fmt_ver}
%endif
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  ffmpeg-devel
%else
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(x11)
Provides:       bundled(ffmpeg) = 0~git%{?shortcommit15}
%endif
BuildRequires:  pkgconfig(libenet) >= 1.3
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libzstd) >= 1.5.0
%if %{with mbedtls}
BuildRequires:  mbedtls >= 2.6.10
%else
Provides:       bundled(mbedtls) = 0~git
%endif
BuildRequires:  pkgconfig(nlohmann_json) >= 3.8.0
BuildRequires:  pkgconfig(opus) >= 1.3
BuildRequires:  pkgconfig(sdl2) >= 2.28.2
%if %{with qt}
BuildRequires:  cmake(Qt%{qt_ver}Core)
BuildRequires:  cmake(Qt%{qt_ver}DBus)
BuildRequires:  cmake(Qt%{qt_ver}Gui)
BuildRequires:  cmake(Qt%{qt_ver}LinguistTools)
BuildRequires:  cmake(Qt%{qt_ver}Multimedia)
BuildRequires:  cmake(Qt%{qt_ver}OpenGL)
BuildRequires:  cmake(Qt%{qt_ver}WebEngineCore)
BuildRequires:  cmake(Qt%{qt_ver}WebEngineWidgets)
BuildRequires:  cmake(Qt%{qt_ver}Widgets)
BuildRequires:  qt%{qt_ver}-qtbase-private-devel
%if %{with qt6}
BuildRequires:  cmake(Qt%{qt_ver}OpenGL)
BuildRequires:  cmake(Qt%{qt_ver}OpenGLWidgets)
%endif
%endif
BuildRequires:  cmake(SPIRV-Headers)
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
BuildRequires:  cmake(VulkanUtilityLibraries) >= %{vkh_ver}
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= 3.1.0
%else
Provides:       bundled(VulkanMemoryAllocator) = 0~git%{shortcommit10}
%endif
BuildRequires:  cmake(xbyak) >= 7
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(microprofile) = 0~git
Provides:       bundled(sirit) = 0~git
Provides:       bundled(simpleini) = 0~git%{?shortcommit11}
%if %{with webservice}
Provides:       bundled(cpp-httplib) = 0~git%{?shortcommit12}
Provides:       bundled(cpp-jwt) = 0~git%{?shortcommit713}
%endif
Provides:       bundled(stb_dxt) = %{stbdxt_ver}
Provides:       bundled(tzdb_to_nx) = ~git%{?shortcommit140}

Obsoletes:      yuzu < 9999


%description
%{name} is an open-source NX emulator written in C++.


%package qt
Summary:        A NX Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme
Obsoletes:      yuzu-qt < 9999

%description qt
%{name} is an open-source NX emulator written in C++.

This is the Qt frontend.


%prep
%autosetup -n %{name} -N -p1
%autopatch -M 499 -p1

pushd externals
rm -rf \
  cubeb/* discord-rpc enet ffmpeg/ffmpeg/* gamemode inih libressl libusb \
  opus/opus/* SDL vcpkg Vulkan-Headers xbyak
%if %{with mbedtls}
rm -rf mbedtls
%endif
popd

%if %{without dynarmic}
rm -rf externals/dynarmic/externals/{catch,fmt,robin-map,xbyak}
sed -e '/find_package/s|dynarmic|\0_DISABLED|g' -i CMakeLists.txt
%endif
%if %{without vma}
mkdir -p externals/VulkanMemoryAllocator
tar -xf %{S:10} -C externals/VulkanMemoryAllocator --strip-components 1
%endif
mkdir -p externals/simpleini
tar -xf %{S:11} -C externals/simpleini --strip-components 1
%if %{with webservice}
tar -xf %{S:12} -C externals/cpp-httplib --strip-components 1
tar -xf %{S:13} -C externals/cpp-jwt --strip-components 1
%endif
%if %{with mbedtls}
rm -rf externals/mbedtls
%endif
mkdir -p externals/nx_tzdb/tzdb_to_nx
tar -xf %{S:14} -C externals/nx_tzdb/tzdb_to_nx --strip-components 1
tar -xf %{S:140} -C externals/nx_tzdb/tzdb_to_nx/externals/tz/tz --strip-components 1
%if %{without ffmpeg}
tar -xf %{S:15} -C externals/ffmpeg/ffmpeg --strip-components 1
%endif
%if %{without fmt}
mkdir -p externals/fmt
tar -xf %{S:16} -C externals/fmt --strip-components 1
sed \
  -e '/^find_package(fmt/s|REQUIRED||' \
  -e 's|^find_package(fmt|\0_DISABLED|' \
  -i CMakeLists.txt
%endif

find . -type f -exec chmod -x {} ';'
find . -type f -name '*.sh' -exec chmod +x {} ';'

pushd externals
%if %{with webservice}
cp -p cpp-httplib/LICENSE LICENSE.cpp-httplib
cp -p cpp-jwt/LICENSE LICENSE.cpp-jwt
%endif
%if %{without dynarmic}
%cp -p dynarmic/LICENSE.txt LICENSE.dynarmic
%endif
cp -p FidelityFX-FSR/license.txt LICENSE.FidelityFX-FSR
%if %{without mbedtls}
cp -p mbedtls/LICENSE LICENSE.mbedtls
%endif
cp -p nx_tzdb/tzdb_to_nx/LICENSE LICENSE.tzdb_to_nx
cp -p simpleini/LICENCE.txt LICENSE.simpleini
cp -p sirit/LICENSE.txt LICENSE.sirit
%if %{without vma}
cp -p VulkanMemoryAllocator/LICENSE.txt LICENSE.vma
%endif
%if %{without ffmpeg}
cp -p ffmpeg/ffmpeg/COPYING.GPLv3 COPYING.ffmpeg
%endif
popd

%if %{without mbedtls}
sed \
  -e '/find_package/s|MBEDTLS|\0_DISABLED|g' \
  -i externals/CMakeLists.txt
%endif

%if %{without dynarmic}
sed \
  -e '/-pedantic-errors/d' \
  -i externals/dynarmic/CMakeLists.txt
%endif

sed -e '/find_packages/s|Git|\0_DISABLED|g' -i CMakeModules/GenerateSCMRev.cmake

sed \
  -e 's|@GIT_REV@|%{commit}|g' \
  -e 's|@GIT_BRANCH@|master|g' \
  -e 's|@GIT_DESC@|%{shortcommit}|g' \
  -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
  -e 's|@BUILD_DATE@|%(date +%F)|g' \
  -e 's|@TITLE_BAR_FORMAT_IDLE@|%{name} %{?with_snapshot:%{ver}-HEAD-%{shortcommit}}%{!?with_snapshot:%{version}}|g' \
  -e 's,@TITLE_BAR_FORMAT_RUNNING@,%{name} %{?with_snapshot:%{ver}-HEAD-%{shortcommit}}%{!?with_snapshot:%{version}} | {3},g' \
  -i src/common/scm_rev.cpp.in

sed -e '/find_program/s|GIT git|GIT cp|g' -i externals/nx_tzdb/CMakeLists.txt

sed \
  -e 's|GIT_PROGRAM git|GIT_PROGRAM true|g' \
  -e 's|${TZ_COMMIT_TIME}|1680663527|g' \
  -e 's|${TZDB_VERSION}|%{nxtzdb_ver}|g' \
  -i externals/nx_tzdb/tzdb_to_nx/src/tzdb/CMakeLists.txt

sed \
  -e 's|GIT_PROGRAM git|GIT_PROGRAM cp|g' \
  -e 's|clone --depth 1 "file://|-rp "|' \
  -i externals/nx_tzdb/tzdb_to_nx/externals/tz/CMakeLists.txt

sed -e 's|-Wno-attributes|\0 -Wno-error=array-bounds|' -i src/CMakeLists.txt

sed -e 's|yuzu|%{name}|g' \
  -i src/common/fs/fs_paths.h dist/%{appname}.{desktop,metainfo.xml}

sed -e '/\/yuzu\//!s|yuzu|%{name}|g' -i dist/languages/*.ts


%build
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  %{!?with_clang:-DSUYU_ENABLE_LTO:BOOL=ON} \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%if %{with qt6}
  -DENABLE_QT6:BOOL=ON \
%endif
%else
  -DENABLE_QT:BOOL=OFF \
%endif
  -DYUZU_CHECK_SUBMODULES:BOOL=OFF \
  -DYUZU_DOWNLOAD_TIME_ZONE_DATA:BOOL=OFF \
  -DYUZU_ENABLE_PORTABLE:BOOL=OFF \
  -DYUZU_ROOM:BOOL=ON \
  -DYUZU_USE_FASTER_LD:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_SDL2:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_VULKAN_HEADERS:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_VULKAN_UTILITY_LIBRARIES:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_VULKAN_SPIRV_TOOLS:BOOL=OFF \
%if %{with ffmpeg}
  -DYUZU_USE_BUNDLED_FFMPEG:BOOL=OFF \
%else
  -DYUZU_USE_BUNDLED_FFMPEG:BOOL=ON \
%endif
  -DYUZU_USE_BUNDLED_LIBUSB:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPUS:BOOL=OFF \
  -DYUZU_USE_QT_WEB_ENGINE:BOOL=ON \
  %{!?with_tests:-DYUZU_TESTS:BOOL=OFF} \
%if %{without webservice}
  -DENABLE_WEB_SERVICE:BOOL=OFF \
%endif
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=OFF \
%if %{without dynarmic}
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_FMT:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_ROBIN_MAP:BOOL=ON \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
  -DDYNARMIC_TESTS=OFF \
%endif
%{nil}

%cmake_build


%install
%cmake_install

rename yuzu %{name} %{buildroot}%{_bindir}/*

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}/cmake
rm -rf %{buildroot}%{_libdir}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE.txt externals/LICENSE.*
%doc README.md
%{_bindir}/%{name}-cmd
%{_bindir}/%{name}-room


%if %{with qt}
%files qt
%license LICENSE.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{appname}.xml
%{_metainfodir}/%{appname}.metainfo.xml
%endif


%changelog
* Wed Dec 04 2024 Phantom X <megaphantomx at hotmail dot com> - 2024.08.10-1.20241112gitbb142c9
- Initial spec
