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

%global commit dfb9f06e5c46f251e4208adf1d4861e85b1d5eea
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240418
%bcond snapshot 0

# Enable system boost
%bcond_without boost
# Enable system dynarmic
%bcond_without dynarmic
# Enable system ffmpeg
%bcond_without ffmpeg
# Enable system fmt
%bcond_with fmt
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
%bcond_without vma

%global commit1 07c614f91b0af5335e1f9c0653c2d75e7b5f53bd
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dynarmic

%global commit2 2f382df218d7e8516dee3b3caccb819a62b571a2
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 VulkanMemoryAllocator

%global commit3 795ef4d8318c7d344da99c076dd60e5580d3d5ac
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 sirit

%global commit4 382ddbb4b92c0b26aa1b32cefba2002119a5b1f2
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 simpleini

%global commit5 c214f6f2d1a7253bb0e9f195c2dc5b0659dc99ef
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%global commit6 a609330e4c6374f741d3b369269f7848255e1954
%global shortcommit6 %(c=%{commit6}; echo ${c:0:6})
%global srcname6 cpp-httplib

%global commit7 10ef5735d842b31025f1257ae78899f50a40fb14
%global shortcommit7 %(c=%{commit7}; echo ${c:0:6})
%global srcname7 cpp-jwt

%global commit8 86ed7bfaa80079a97c763a651d0b2cd8d9d59100
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 mbedtls

%global commit9 97929690234f2b4add36b33657fe3fe09bd57dfd
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 tzdb_to_nx

%global commit10 16ce126a87c5f130cde8b8dce73b38952a19f085
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 tz

%global commit11 9c1294eaddb88cb0e044c675ccae059a85fc9c6c
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 FFmpeg

%global fmt_ver 10.2.1
%global glad_ver 0.1.29
%global nxtzdb_ver 221202
%global stbdxt_ver 1.12
%global vkh_ver 1.3.246
%{?with_qt6:%global qt_ver 6}%{!?with_qt6:%global qt_ver 5}

%global vc_url   https://github.com/emuplace/sudachi.emuplace.app
%global mvc_url  https://github.com/sudachi-emu

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%else
%global shortcommit 0
%endif

%global appname org.sudachi_emu.%{name}

Name:           sudachi
Version:        1.0.15
Release:        1%{?dist}
Summary:        A NX Emulator

License:        GPL-2.0-or-later AND MIT AND Apache-2.0 WITH LLVM-exception AND MPL-2.0%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_mbedtls: AND (Apache-2.0 OR GPL-2.0-or-later)}%{!?with_boost: AND BSL-1.0}
URL:            https://sudachi.emuplace.app/

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/releases/download/v%{version}/latest.zip#/%{name}-%{version}.zip
%endif

%if %{without dynarmic}
Source1:        https://github.com/MerryMage/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%endif
%if %{without vma}
Source2:        https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
%endif
Source3:        %{mvc_url}/%{srcname3}/archive/%{commit3}.tar.gz#/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/brofield/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/KhronosGroup/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%if %{with webservice}
Source6:        https://github.com/yhirose/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/arun11299/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
%endif
%if !%{with mbedtls}
Source8:        %{mvc_url}/%{srcname8}/archive/%{commit8}.tar.gz#/%{srcname8}-%{shortcommit8}.tar.gz
%endif
Source9:        https://github.com/lat9nq/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       https://github.com/eggert/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%if %{without ffmpeg}
Source11:       https://github.com/FFmpeg/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%endif
%if %{without fmt}
Source12:        https://github.com/fmtlib/fmt/archive/%{fmt_ver}/fmt-%{fmt_ver}.tar.gz
%endif

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-boost-build-fix.patch
Patch12:        0001-Fix-48e86d6.patch
Patch13:        0001-Bundled-fmt-support.patch
Patch14:        0001-video_core-system-ffmpeg-fix.patch
Patch15:        0001-Update-for-latest-dynarmic.patch
Patch16:        0001-SDL3-fix-build.patch

ExclusiveArch:  x86_64

BuildRequires:  cmake
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
BuildRequires:  cmake(dynarmic) >= 6.6.1
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
BuildRequires:  cmake(fmt) >= 9
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
Provides:       bundled(ffmpeg) = 0~git%{?shortcommit11}
%endif
BuildRequires:  pkgconfig(libenet) >= 1.3
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libzstd) >= 1.5.0
%if %{with mbedtls}
BuildRequires:  mbedtls >= 2.6.10
%else
Provides:       bundled(mbedtls) = 0~git%{?shortcommit8}
%endif
BuildRequires:  pkgconfig(nlohmann_json) >= 3.8.0
BuildRequires:  pkgconfig(opus) >= 1.3
BuildRequires:  pkgconfig(sdl3) >= 3.2.8
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
%if %{with qt6}
BuildRequires:  cmake(Qt%{qt_ver}OpenGL)
BuildRequires:  cmake(Qt%{qt_ver}OpenGLWidgets)
%endif
%endif
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
BuildRequires:  cmake(VulkanUtilityLibraries) >= %{vkh_ver}
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= 3.1.0
%else
Provides:       bundled(VulkanMemoryAllocator) = 0~git%{shortcommit2}
%endif
BuildRequires:  cmake(xbyak) >= 7
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(microprofile) = 0~git
Provides:       bundled(sirit) = 0~git%{?shortcommit3}
Provides:       bundled(simpleini) = 0~git%{?shortcommit4}
%if %{with webservice}
Provides:       bundled(cpp-httplib) = 0~git%{?shortcommit6}
Provides:       bundled(cpp-jwt) = 0~git%{?shortcommit7}
%endif
Provides:       bundled(stb_dxt) = %{stbdxt_ver}
Provides:       bundled(tzdb_to_nx) = ~git%{?shortcommit9}


%description
suyu is an open-source NX emulator written in C++.


%package qt
Summary:        A NX Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
suyu is an open-source NX emulator written in C++.

This is the Qt frontend.


%prep
%autosetup -c -N -p1

find \( -name '*.txt' -or -name '*.cmake' -or -name '*.md' -or -name '*.xml' \) -exec sed -i 's/\r$//' {} \;
find \( -name '*.desktop' -or -name '*.rules' -or -name '*.theme' \) -exec sed -i 's/\r$//' {} \;
find \( -name '*.c*' -or -name '*.h*' -or -name '*.qrc' -or -name '*.json' \) -exec sed -i 's/\r$//' {} \;

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
tar -xf %{S:1} -C externals/dynarmic --strip-components 1
rm -rf externals/dynarmic/externals/{catch,fmt,robin-map,xbyak}
sed -e '/find_package/s|dynarmic|\0_DISABLED|g' -i CMakeLists.txt
%endif
%if %{without vma}
mkdir -p externals/VulkanMemoryAllocator
tar -xf %{S:2} -C externals/VulkanMemoryAllocator --strip-components 1
%endif
tar -xf %{S:3} -C externals/sirit --strip-components 1
mkdir -p externals/simpleini
tar -xf %{S:4} -C externals/simpleini --strip-components 1
tar -xf %{S:5} -C externals/sirit/externals/SPIRV-Headers --strip-components 1
%if %{with webservice}
tar -xf %{S:6} -C externals/cpp-httplib --strip-components 1
tar -xf %{S:7} -C externals/cpp-jwt --strip-components 1
%endif
%if %{without mbedtls}
tar -xf %{S:8} -C externals/mbedtls --strip-components 1
%endif
mkdir -p externals/nx_tzdb/tzdb_to_nx
tar -xf %{S:9} -C externals/nx_tzdb/tzdb_to_nx --strip-components 1
tar -xf %{S:10} -C externals/nx_tzdb/tzdb_to_nx/externals/tz/tz --strip-components 1
%if %{without ffmpeg}
tar -xf %{S:11} -C externals/ffmpeg/ffmpeg --strip-components 1
%endif
%if %{without fmt}
mkdir -p externals/fmt
tar -xf %{S:12} -C externals/fmt --strip-components 1
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
cp -p sirit/LICENSE LICENSE.sirit
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
  -e 's|@GIT_BRANCH@|main|g' \
  -e 's|@GIT_DESC@|%{shortcommit}|g' \
  -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
  -e 's|@BUILD_DATE@|%(date +%F)|g' \
  -e 's|@TITLE_BAR_FORMAT_IDLE@|%{name} %{?with_snapshot:v%{version}-HEAD-%{shortcommit}}%{!?with_snapshot:%{version}}|g' \
  -e 's,@TITLE_BAR_FORMAT_RUNNING@,%{name} %{?with_snapshot:v%{version}-HEAD-%{shortcommit}}%{!?with_snapshot:%{version}} | {3},g' \
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

sed \
  -e 's|-Wno-attributes|\0 -Wno-error=array-bounds -Wno-error=shadow -Wno-error=unused-variable|' \
  -i src/CMakeLists.txt

sed '/create_target_directory_groups/d' -i externals/glad/CMakeLists.txt


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
  -DSUDACHI_CHECK_SUBMODULES:BOOL=OFF \
  -DSUDACHI_ENABLE_PORTABLE:BOOL=OFF \
  -DSUDACHI_ROOM:BOOL=ON \
  -DSUDACHI_USE_FASTER_LD:BOOL=OFF \
  -DSUDACHI_USE_EXTERNAL_SDL3:BOOL=OFF \
  -DSUDACHI_USE_EXTERNAL_VULKAN_HEADERS:BOOL=OFF \
  -DSUDACHI_USE_EXTERNAL_VULKAN_UTILITY_LIBRARIES:BOOL=OFF \
%if %{with ffmpeg}
  -DSUDACHI_USE_BUNDLED_FFMPEG:BOOL=OFF \
%else
  -DSUDACHI_USE_BUNDLED_FFMPEG:BOOL=ON \
%endif
  -DSUDACHI_USE_BUNDLED_LIBUSB:BOOL=OFF \
  -DSUDACHI_USE_BUNDLED_OPUS:BOOL=OFF \
  -DSUDACHI_USE_QT_WEB_ENGINE:BOOL=ON \
  %{!?with_tests:-DSUDACHI_TESTS:BOOL=OFF} \
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

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}/cmake
rm -rf %{buildroot}%{_libdir}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE.md externals/LICENSE.*
%doc README.md
%{_bindir}/%{name}-cmd
%{_bindir}/%{name}-room
%dnl %{_mandir}/man6/%{name}.6*


%if %{with qt}
%files qt
%license LICENSE.md
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{appname}.xml
%{_metainfodir}/%{appname}.metainfo.xml
%dnl %{_mandir}/man6/%{name}-qt.6*
%endif


%changelog
* Sun Apr 06 2025 - 1.0.15-1
- 1.0.15

* Tue Oct 08 2024 - 1.0.11-1
- Initial spec
