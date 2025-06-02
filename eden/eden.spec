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

%global commit fb3988a78a54b4a75090594a6d374ba819e0afcb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250531
%bcond_without snapshot

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

%global commit110 7b08d83418f628b800dfac1c9a16c3f59036fbad
%global shortcommit10 %(c=%{commit110}; echo ${c:0:7})
%global srcname110 mcl

%global commit111 e59d30b7b12e1d04cc2fc9c6219e35bda447c17e
%global shortcommit111 %(c=%{commit111}; echo ${c:0:7})
%global srcname111 unordered_dense

%global commit112 0b2432ced0884fd152b471d97ecf0258ff4d859f
%global shortcommit12 %(c=%{commit112}; echo ${c:0:7})
%global srcname112 zycore-c

%global commit113 bffbb610cfea643b98e87658b9058382f7522807
%global shortcommit113 %(c=%{commit113}; echo ${c:0:7})
%global srcname113 zydis

%global commit12 05973d8aeb1a4d12f59aadfb86d20decadba82d1
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 VulkanMemoryAllocator

%global commit15 3f17b2af6784bfa2c5aa5dbb8e0e74a607dd8b3b
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 SPIRV-Headers

%global commit16 a609330e4c6374f741d3b369269f7848255e1954
%global shortcommit16 %(c=%{commit16}; echo ${c:0:6})
%global srcname16 cpp-httplib

%global commit17 10ef5735d842b31025f1257ae78899f50a40fb14
%global shortcommit17 %(c=%{commit17}; echo ${c:0:6})
%global srcname17 cpp-jwt

%global commit20 16ce126a87c5f130cde8b8dce73b38952a19f085
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 tz

%global commit21 9c1294eaddb88cb0e044c675ccae059a85fc9c6c
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 FFmpeg

%global commit23 0456900fadde4b07c84760eadea4ccc9f948fe28
%global shortcommit23 %(c=%{commit23}; echo ${c:0:7})
%global srcname23 boost-headers

%global fmt_ver 11.0.2
%global glad_ver 0.1.29
%global nxtzdb_ver 221202
%global stbdxt_ver 1.12
%global vkh_ver 1.3.246
%{?with_qt6:%global qt_ver 6}%{!?with_qt6:%global qt_ver 5}

%global vc_url   https://git.eden-emu.dev/eden-emu

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%else
%global shortcommit 0
%endif

%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           eden
Version:        0.0.2.27334
Release:        1%{?dist}
Summary:        A NX Emulator

License:        GPL-2.0-or-later AND MIT AND Apache-2.0 WITH LLVM-exception AND MPL-2.0 AND BSL-1.0%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_mbedtls: AND (Apache-2.0 OR GPL-2.0-or-later)}
URL:            https://eden-emulator.github.io

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

%if %{without dynarmic}
Source110:      https://github.com/azahar-emu/%{srcname110}/archive/%{commit110}.tar.gz#/%{srcname110}-%{shortcommit110}.tar.gz
Source111:      https://github.com/Lizzie841/%{srcname111}/archive/%{commit111}/%{srcname11}-%{shortcommit111}.tar.gz
Source112:      https://github.com/zyantific/%{srcname112}/archive/%{commit112}.tar.gz#/%{srcname112}-%{shortcommit112}.tar.gz
Source113:      https://github.com/zyantific/%{srcname113}/archive/%{commit113}.tar.gz#/%{srcname113}-%{shortcommit113}.tar.gz
%endif
%if %{without vma}
Source12:       https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit21}.tar.gz
%endif
Source15:       https://github.com/KhronosGroup/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%if %{with webservice}
Source16:       https://github.com/yhirose/%{srcname16}/archive/%{commit16}.tar.gz#/%{srcname16}-%{shortcommit16}.tar.gz
Source17:       https://github.com/arun11299/%{srcname17}/archive/%{commit17}.tar.gz#/%{srcname17}-%{shortcommit17}.tar.gz
%endif
Source20:       https://github.com/eggert/%{srcname20}/archive/%{commit20}/%{srcname20}-%{shortcommit20}.tar.gz
%if %{without ffmpeg}
Source21:       https://github.com/FFmpeg/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
%endif
%if %{without fmt}
Source22:       https://github.com/fmtlib/fmt/archive/%{fmt_ver}/fmt-%{fmt_ver}.tar.gz
%endif
Source23:       https://github.com/boostorg/headers/archive/%{commit23}.tar.gz#/%{srcname23}-%{shortcommit23}.tar.gz


Patch10:        0001-Use-system-libraries.patch
Patch12:        0001-Bundled-fmt-support.patch
Patch14:        0001-Fix-48e86d6.patch

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
BuildRequires:  lld
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  llvm-devel >= 19.1.3
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  boost-devel >= 1.83.0
%if %{with tests}
BuildRequires:  pkgconfig(catch2) >= 2.13.7
%endif
BuildRequires:  cmake(cubeb)
%if %{with dynarmic}
BuildRequires:  cmake(dynarmic) >= 6.7.0
%else
Provides:       bundled(dynarmic) = 0~git%{?shortcommit11}
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
Provides:       bundled(ffmpeg) = 0~git%{?shortcommit21}
%endif
BuildRequires:  pkgconfig(libenet) >= 1.3
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libzstd) >= 1.5.0
%if %{with mbedtls}
BuildRequires:  mbedtls >= 2.6.10
%else
Provides:       bundled(mbedtls) = 0~gitacdc937
%endif
BuildRequires:  pkgconfig(nlohmann_json) >= 3.8.0
BuildRequires:  pkgconfig(opus) >= 1.3
BuildRequires:  pkgconfig(sdl2) >= 2.32.0
%if %{with qt}
BuildRequires:  cmake(Qt%{qt_ver}Core)
BuildRequires:  cmake(Qt%{qt_ver}DBus)
BuildRequires:  cmake(Qt%{qt_ver}Gui)
%dnl BuildRequires:  cmake(Qt%{qt_ver}LinguistTools)
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
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
BuildRequires:  cmake(VulkanUtilityLibraries) >= %{vkh_ver}
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= 3.1.0
%else
Provides:       bundled(VulkanMemoryAllocator) = 0~git%{shortcommit12}
%endif
BuildRequires:  cmake(xbyak) >= 7
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(microprofile) = 0~git
%ifarch aarch64
Provides:       bundled(oaknut) = 0~git9d09110
%endif
Provides:       bundled(sirit) = 0~git6e6d792
Provides:       bundled(simpleini) = 0~git382ddbb
%if %{with webservice}
Provides:       bundled(cpp-httplib) = 0~git%{?shortcommit16}
Provides:       bundled(cpp-jwt) = 0~git%{?shortcommit17}
%endif
Provides:       bundled(stb_dxt) = %{stbdxt_ver}
Provides:       bundled(tzdb_to_nx) = ~git9792969

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
  breakpad cubeb/* discord-rpc enet ffmpeg/ffmpeg/* gamemode getopt inih \
  libadrenotools libressl libusb oboe opus/opus/* SDL vcpkg Vulkan-Headers xbyak
%ifarch x86_64
rm -rf oaknut sse2neon
%endif
%if %{with mbedtls}
rm -rf mbedtls
%endif

%if %{with dynarmic}
rm -rf dynarmic
%else
tar -xf %{S:110} -C dynarmic/externals/mcl --strip-components 1
tar -xf %{S:111} -C dynarmic/externals/unordered_dense --strip-components 1
tar -xf %{S:112} -C dynarmic/externals/zycore --strip-components 1
tar -xf %{S:113} -C dynarmic/externals/zydis --strip-components 1
sed -e '/find_package/s|dynarmic|\0_DISABLED|g' -i ../CMakeLists.txt
sed \
  -e '/-pedantic-errors/d' \
  -i dynarmic/CMakeLists.txt
sed \
  -e '/find_/s|Zydis|zydis_DISABLED|g' \
  -i dynarmic/CMakeLists.txt dynarmic/CMakeModules/dynarmicConfig.cmake.in
%endif
%if %{without vma}
mkdir -p VulkanMemoryAllocator
tar -xf %{S:12} -C VulkanMemoryAllocator --strip-components 1
%endif
tar -xf %{S:15} -C sirit/externals/SPIRV-Headers --strip-components 1
%if %{with webservice}
tar -xf %{S:16} -C cpp-httplib --strip-components 1
tar -xf %{S:17} -C cpp-jwt --strip-components 1
%endif
tar -xf %{S:20} -C nx_tzdb/tzdb_to_nx/externals/tz/tz --strip-components 1
%if %{without ffmpeg}
tar -xf %{S:21} -C ffmpeg/ffmpeg --strip-components 1
%endif
%if %{without fmt}
mkdir -p fmt
tar -xf %{S:22} -C fmt --strip-components 1
sed \
  -e '/^find_package(fmt/s|REQUIRED||' \
  -e 's|^find_package(fmt|\0_DISABLED|' \
  -i ../CMakeLists.txt
%endif
tar -xf %{S:23} -C boost-headers --strip-components 1

%if %{without mbedtls}
sed \
  -e '/find_package/s|MBEDTLS|\0_DISABLED|g' \
  -i CMakeLists.txt
%endif

popd

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

sed -e '/find_packages/s|Git|\0_DISABLED|g' -i CMakeModules/GenerateSCMRev.cmake

sed \
  -e 's|@GIT_REV@|%{commit}|g' \
  -e 's|@GIT_BRANCH@|main|g' \
  -e 's|@GIT_DESC@|%{shortcommit}|g' \
  -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
  -e 's|@BUILD_DATE@|%(date +%F)|g' \
  -e 's|@TITLE_BAR_FORMAT_IDLE@|%{name} %{?with_snapshot:v%{version}-%{shortcommit}}%{!?with_snapshot:%{version}}|g' \
  -e 's,@TITLE_BAR_FORMAT_RUNNING@,%{name} %{?with_snapshot:v%{version}-%{shortcommit}}%{!?with_snapshot:%{version}} | {3},g' \
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

%if %{with clang}
echo 'set_target_properties(yuzu PROPERTIES INTERPROCEDURAL_OPTIMIZATION true)' \
  >> src/yuzu/CMakeLists.txt <<EOF
%endif


%build
%global xbyak_flags -DXBYAK_STRICT_CHECK_MEM_REG_SIZE=0
export CFLAGS+=" %{xbyak_flags}"
export CXXFLAGS+=" -fpermissive %{xbyak_flags}"
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DYUZU_ENABLE_LTO:BOOL=ON \
%if %{with qt}
  -DYUZU_USE_BUNDLED_QT:BOOL=OFF \
  -DENABLE_QT_TRANSLATION:BOOL=OFF \
  -DENABLE_QT_UPDATE_CHECKER:BOOL=OFF \
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

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE.txt externals/LICENSE.*
%doc README.md
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-room


%if %{with qt}
%files qt
%license LICENSE.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml
%{_metainfodir}/%{name}.metainfo.xml
%endif


%changelog
* Mon May 19 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.2.27303-1.20250519git3cad73d
- Initial spec
