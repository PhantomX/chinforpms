# Selective LTO.
%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond clang 0
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit c609389ec1e1744a5d024c5c6811cc7cea1ba113
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250730
%bcond snapshot 1

# Enable system dynarmic
%bcond dynarmic 0
# Enable system ffmpeg
%bcond ffmpeg 1
# Use stable ffmpeg
%bcond ffmpeg_st 1
# Enable system fmt
%bcond fmt 1
# Enable system mbedtls (needs cmac builtin support)
%bcond mbedtls 0
# Disable Qt build
%bcond qt 1
# build with qt6 instead 5
%bcond qt6 1
# Build tests
%bcond tests 0
%bcond vma 1
%bcond xbyak 0
# Enable webservice
%bcond webservice 1

%global commit111 e59d30b7b12e1d04cc2fc9c6219e35bda447c17e
%global shortcommit111 %(c=%{commit111}; echo ${c:0:7})
%global srcname111 unordered_dense

%global commit112 75a36c45ae1ad382b0f4e0ede0af84c11ee69928
%global shortcommit112 %(c=%{commit112}; echo ${c:0:7})
%global srcname112 zycore-c

%global commit113 c2d2bab0255e53a7c3e9b615f4eb69449eb942df
%global shortcommit113 %(c=%{commit113}; echo ${c:0:7})
%global srcname113 zydis

%global commit12 05973d8aeb1a4d12f59aadfb86d20decadba82d1
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 VulkanMemoryAllocator

%global commit13 4e44f4614ddbf038f2a6296f5b906d5c72691e0f
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 xbyak

%global commit15 3f17b2af6784bfa2c5aa5dbb8e0e74a607dd8b3b
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 SPIRV-Headers

%global commit16 ca5fe354fb83194bc72a676c4cc4136fca5316d0
%global shortcommit16 %(c=%{commit16}; echo ${c:0:6})
%global srcname16 cpp-httplib

%global commit17 a54fa08a3bc929ce16cd84264bb0653e548955f9
%global shortcommit17 %(c=%{commit17}; echo ${c:0:6})
%global srcname17 cpp-jwt

%global commit20 344c99fc75006e6529df42b2a205c8f40bac4e46
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 tz

%global commit21 9c1294eaddb88cb0e044c675ccae059a85fc9c6c
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 FFmpeg

%global commit23 0456900fadde4b07c84760eadea4ccc9f948fe28
%global shortcommit23 %(c=%{commit23}; echo ${c:0:7})
%global srcname23 boost-headers

%global ffmpeg_ver 7.1.1
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

%global appname org.%{name}_emu.%{name}

%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           eden
Version:        0.0.3~rc2.27538
Release:        1%{?dist}
Summary:        A NX Emulator

License:        GPL-2.0-or-later AND MIT AND Apache-2.0 WITH LLVM-exception AND MPL-2.0 AND BSL-1.0%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_xbyak: AND BSD-3-Clause}%{!?with_mbedtls: AND (Apache-2.0 OR GPL-2.0-or-later)}
URL:            https://eden-emulator.github.io

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

%if %{without dynarmic}
Source111:      https://github.com/Lizzie841/%{srcname111}/archive/%{commit111}/%{srcname111}-%{shortcommit111}.tar.gz
Source112:      https://github.com/zyantific/%{srcname112}/archive/%{commit112}/%{srcname112}-%{shortcommit112}.tar.gz
Source113:      https://github.com/zyantific/%{srcname113}/archive/%{commit113}/%{srcname113}-%{shortcommit113}.tar.gz
%endif
%if %{without vma}
Source12:       https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit21}.tar.gz
%endif
%if %{without xbyak}
Source13:       https://github.com/Lizzie841/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%endif
%dnl Source15:       https://github.com/KhronosGroup/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%if %{with webservice}
Source16:       https://github.com/yhirose/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
Source17:       https://github.com/arun11299/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%endif
Source20:       https://github.com/eggert/%{srcname20}/archive/%{commit20}/%{srcname20}-%{shortcommit20}.tar.gz
%if %{without ffmpeg}
%if %{without ffmpeg_st}
Source21:       https://github.com/FFmpeg/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
%else
Source21:      https://ffmpeg.org/releases/ffmpeg-%{ffmpeg_ver}.tar.xz
%endif
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
Provides:       bundled(dynarmic) = 0~git%{?shortcommit}
%endif
BuildRequires:  pkgconfig(gamemode) >= 1.7
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
BuildRequires:  autoconf
BuildRequires:  nasm
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(x11)
%if %{without ffmpeg_st}
Provides:       bundled(ffmpeg) = 0~git%{?shortcommit21}
%else
Provides:       bundled(ffmpeg) = %{ffmpeg_ver}
%endif
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
BuildRequires:  pkgconfig(quazip1-qt6)
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
BuildRequires:  cmake(glslang)
BuildRequires:  cmake(SPIRV-Tools)
BuildRequires:  spirv-headers-devel
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
BuildRequires:  cmake(VulkanUtilityLibraries) >= %{vkh_ver}
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= 3.1.0
%else
Provides:       bundled(VulkanMemoryAllocator) = 0~git%{shortcommit12}
%endif
%if %{with xbyak}
BuildRequires:  cmake(xbyak) >= 7
%else
Provides:       bundled(xbyak) = 0~git%{?shortcommit13}
%endif
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


%description
%{name} is an open-source NX emulator written in C++.


%package qt
Summary:        A NX Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
%{name} is an open-source NX emulator written in C++.

This is the Qt frontend.


%prep
%autosetup -n %{name} -N -p1
%autopatch -M 499 -p1

rm -rf src/yuzu/externals

pushd externals
rm -rf \
  breakpad cubeb/* discord-rpc enet ffmpeg/ffmpeg/* gamemode getopt inih \
  libadrenotools libressl libusb oboe opus/opus/* SDL vcpkg Vulkan-Headers
%ifarch x86_64
rm -rf oaknut sse2neon
%endif
%if %{with mbedtls}
rm -rf mbedtls
%endif

%if %{with dynarmic}
rm -rf dynarmic
%else
tar -xf %{S:111} -C dynarmic/externals/unordered_dense --strip-components 1
tar -xf %{S:112} -C dynarmic/externals/zycore-c --strip-components 1
tar -xf %{S:113} -C dynarmic/externals/zydis --strip-components 1
sed -e '/find_package/s|dynarmic|\0_DISABLED|g' -i ../CMakeLists.txt
sed \
  -e '/-pedantic-errors/d' \
  -e '/-mtune=core2/d' \
  -i dynarmic/CMakeLists.txt
sed \
  -e '/find_/s|Zydis|Zydis_DISABLED|g' \
  -i dynarmic/CMakeLists.txt dynarmic/CMakeModules/dynarmicConfig.cmake.in
%endif
%if %{without vma}
mkdir -p VulkanMemoryAllocator
tar -xf %{S:12} -C VulkanMemoryAllocator --strip-components 1
%endif
%if %{without xbyak}
tar -xf %{S:13} -C xbyak --strip-components 1
sed -e '/find_package/s|xbyak|\0_DISABLED|g' -i ../CMakeLists.txt
%endif
%dnl tar -xf %{S:15} -C sirit/externals/SPIRV-Headers --strip-components 1
%if %{with webservice}
tar -xf %{S:16} -C cpp-httplib --strip-components 1
tar -xf %{S:17} -C cpp-jwt --strip-components 1
sed -e 's|zstd::libzstd|zstd::zstd|g' -i cpp-httplib/CMakeLists.txt
%endif
tar -xf %{S:20} -C nx_tzdb/tzdb_to_nx/externals/tz/tz --strip-components 1
%if %{without ffmpeg}
tar -xf %{S:21} -C ffmpeg/ffmpeg --strip-components 1
sed -e '/h264_sei.o/s|$| aom_film_grain.o|' -i ffmpeg/ffmpeg/libavcodec/Makefile
sed \
  -e 's|--disable-avdevice|\0 --arch=%{_target_cpu}|' \
  -i ffmpeg/CMakeLists.txt
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
cp -p dynarmic/LICENSE.txt LICENSE.dynarmic
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
%if %{without xbyak}
cp xbyak/COPYRIGHT LICENSE.xbyak
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
  -e 's|clone --depth=1 "file://|-rp "|' \
  -i externals/nx_tzdb/tzdb_to_nx/externals/tz/CMakeLists.txt

sed \
  -e 's|-Wno-attributes|\0 -Wno-error=array-bounds -Wno-error=shadow -Wno-error=unused-variable -Wno-error=missing-declarations|' \
  -i src/CMakeLists.txt

%if %{with clang}
echo 'set_target_properties(yuzu PROPERTIES INTERPROCEDURAL_OPTIMIZATION true)' \
  >> src/yuzu/CMakeLists.txt <<EOF
%endif


%build
%global xbyak_flags -DXBYAK_STRICT_CHECK_MEM_REG_SIZE=0
export CFLAGS+=" %{xbyak_flags}"
export CXXFLAGS+=" %{xbyak_flags}"
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DYUZU_BUILD_PRESET:STRING="none" \
  -DYUZU_SYSTEM_PROFILE:STRING="none" \
  -DYUZU_ENABLE_LTO:BOOL=ON \
%if %{with qt}
  -DYUZU_USE_BUNDLED_QT:BOOL=OFF \
  -DENABLE_QT_TRANSLATION:BOOL=OFF \
  -DENABLE_QT_UPDATE_CHECKER:BOOL=OFF \
  %{?with_qt6:-DENABLE_QT6:BOOL=ON} \
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
  -DYUZU_USE_EXTERNAL_VULKAN_SPIRV_TOOLS:BOOL=OFF \
  -DSIRIT_USE_SYSTEM_SPIRV_HEADERS:BOOL=ON \
  -DYUZU_USE_EXTERNAL_VULKAN_UTILITY_LIBRARIES:BOOL=OFF \
  %{?with_ffmpeg:-DYUZU_USE_BUNDLED_FFMPEG:BOOL=OFF} \
  -DYUZU_USE_BUNDLED_LIBUSB:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPUS:BOOL=OFF \
  -DYUZU_USE_QT_WEB_ENGINE:BOOL=ON \
  %{!?with_tests:-DYUZU_TESTS:BOOL=OFF} \
  %{!?with_webservice:-DENABLE_WEB_SERVICE:BOOL=OFF} \
  -DENABLE_WIFI_SCAN:BOOL=OFF \
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=OFF \
%if %{without dynarmic}
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_FMT:BOOL=ON \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
  -DDYNARMIC_TESTS:BOOL=OFF \
%endif
%{nil}

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}/cmake
rm -rf %{buildroot}%{_libdir}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE.txt externals/LICENSE.*
%doc README.md
%{_bindir}/%{name}-cli
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
* Thu Jul 31 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.3~rc2.27538-1.20250730gitc609389
- 0.0.3-rc2

* Sun Jul 27 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.3~rc1.27522-1.20250727giteeb6876
- 0.0.3-rc1

* Sun Jun 15 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.2.27370-1.20250615gitcf00554
- Bundle ffmpeg until internal codecs is not needed

* Mon May 19 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.2.27303-1.20250519git3cad73d
- Initial spec
