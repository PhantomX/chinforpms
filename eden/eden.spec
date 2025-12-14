# Selective LTO.
%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond clang 0
%if %{with clang}
%global toolchain clang
%endif

%global with_extra_flags -O3 -Wp,-U_GLIBCXX_ASSERTIONS
%{?with_extra_flags:%global _pkg_extra_cflags %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?with_extra_flags}}
%{!?_hardened_build:%global _pkg_extra_ldflags -Wl,-z,now}

%global commit 363d8610113e83e2eec972b98c62112ed639787c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20251213
%bcond snapshot 1

# Enable system ffmpeg
%bcond ffmpeg 1
# Use stable ffmpeg
%bcond ffmpeg_st 1
# Enable system fmt
%bcond fmt 1
%bcond httplib 0
# Enable system mbedtls (needs cmac builtin support)
%bcond mbedtls 1
# Disable Qt build
%bcond qt 1
# Build tests
%bcond tests 0
%bcond vma 1
%bcond xbyak 0
# Enable webservice
%bcond webservice 1

%global commit110 7b08d83418f628b800dfac1c9a16c3f59036fbad
%global shortcommit110 %(c=%{commit110}; echo ${c:0:7})
%global srcname110 mcl

%global commit111 73f3cbb237e84d483afafc743f1f14ec53e12314
%global shortcommit111 %(c=%{commit111}; echo ${c:0:7})
%global srcname111 unordered_dense

%global commit12 05973d8aeb1a4d12f59aadfb86d20decadba82d1
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 VulkanMemoryAllocator

%global commit13 4e44f4614ddbf038f2a6296f5b906d5c72691e0f
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 xbyak

%global commit16 a609330e4c6374f741d3b369269f7848255e1954
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 cpp-httplib

%global commit17 9eaea6328fae768d1cc524a27f0db6250e0a165a
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 cpp-jwt

%global commit18 c765c831e5c2a0971410692f92f7a81d6ec65ec2
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 mbedtls

%global commit180 2a3e2c5ea053c14b745dbdf41f609b1edc6a72fa
%global shortcommit180 %(c=%{commit180}; echo ${c:0:7})
%global srcname180 mbedtls-framework

%global commit19 09c21bda1dc1b578fa55f4a005d79b0afd481296
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 simpleini

%global commit20 f140d1e8c56df65993bb267603d09a5b4abd56eb
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 tzdb_to_nx

%global commit200 344c99fc75006e6529df42b2a205c8f40bac4e46
%global shortcommit200 %(c=%{commit200}; echo ${c:0:7})
%global srcname200 tz

%global commit21 9c1294eaddb88cb0e044c675ccae059a85fc9c6c
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 FFmpeg

%global commit23 95930ca8f5d144fe345a2ad7a2a7728b8c3e5cd5
%global shortcommit23 %(c=%{commit23}; echo ${c:0:7})
%global srcname23 boost-headers

%global ffmpeg_ver 7.1.1
%global fmt_ver 12.0.0
%global glad_ver 0.1.29
%global nxtzdb_ver 250725
%global stbdxt_ver 1.12
%global vkh_ver 1.3.246
%{?with_qt6:%global qt_ver 6}%{!?with_qt6:%global qt_ver 5}

%global vc_url   https://git.eden-emu.dev/eden-emu
%global gh_url   https://github.com/eden-emulator

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%else
%global shortcommit 0
%endif

%global appname dev.%{name}_emu.%{name}

%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           eden
Version:        0.0.4.28093
Release:        0.1%{?dist}
Summary:        A NX Emulator

License: %{shrink:
    GPL-2.0-or-later AND
    MIT AND Apache-2.0 AND
    Apache-2.0 WITH LLVM-exception AND
    MPL-2.0 AND
    BSL-1.0 AND ( 0BSD AND MIT )
    %{!?with_xbyak:AND BSD-3-Clause}
    %{!?with_mbedtls:AND (Apache-2.0 OR GPL-2.0-or-later)}
}
URL:            https://eden-emulator.github.io

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

Source110:      https://github.com/azahar-emu/%{srcname110}/archive/%{commit110}/%{srcname110}-%{shortcommit110}.tar.gz
Source111:      https://github.com/martinus/%{srcname111}/archive/%{commit111}/%{srcname111}-%{shortcommit111}.tar.gz
%if %{without vma}
Source12:       https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit21}.tar.gz
%endif
%if %{without xbyak}
Source13:       https://github.com/herumi/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%endif
%dnl Source14:       %{gh_url}/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
%dnl Source15:       https://github.com/KhronosGroup/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%if %{with webservice}
%if %{without httplib}
Source16:       https://github.com/yhirose/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
%endif
Source17:       https://github.com/crueter/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%endif
%if %{without mbedtls}
Source18:       https://github.com/Mbed-TLS/%{srcname18}/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
Source180:      https://github.com/Mbed-TLS/%{srcname180}/archive/%{commit180}/%{srcname180}-%{shortcommit180}.tar.gz
%endif
Source19:       https://github.com/brofield/%{srcname19}/archive/%{commit19}/%{srcname19}-%{shortcommit19}.tar.gz
Source20:       https://git.crueter.xyz/misc/%{srcname20}/archive/%{commit20}.tar.gz#/%{srcname20}-%{shortcommit20}.tar.gz
Source200:      https://github.com/eggert/%{srcname200}/archive/%{commit200}/%{srcname200}-%{shortcommit200}.tar.gz
%if %{without ffmpeg}
%if %{without ffmpeg_st}
Source21:       https://github.com/FFmpeg/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
%else
Source21:       https://ffmpeg.org/releases/ffmpeg-%{ffmpeg_ver}.tar.xz
%endif
%endif
%if %{without fmt}
Source22:       https://github.com/fmtlib/fmt/archive/%{fmt_ver}/fmt-%{fmt_ver}.tar.gz
%endif
Source23:       https://github.com/boostorg/headers/archive/%{commit23}.tar.gz#/%{srcname23}-%{shortcommit23}.tar.gz
%dnl Source24:       https://github.com/serge-sans-paille/%{srcname24}/archive/%{commit24}/%{srcname24}-%{shortcommit24}.tar.gz

Patch10:        0001-Use-system-libraries.patch

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
%if %{with webservice}
%if %{with httplib}
BuildRequires:  cmake(httplib) >= 0.12
%else
Provides:       bundled(cpp-httplib) = 0~git%{?shortcommit16}
%endif
Provides:       bundled(cpp-jwt) = 0~git%{?shortcommit17}
%endif
Provides:       bundled(dynarmic) = 0~git%{?shortcommit}
BuildRequires:  cmake(frozen)
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
BuildRequires:  cmake(MbedTLS) >= 3.6.4
%else
Provides:       bundled(mbedtls) = 0~git%{?shortcommit18}
%endif
BuildRequires:  pkgconfig(nlohmann_json) >= 3.8.0
BuildRequires:  pkgconfig(opus) >= 1.3
BuildRequires:  pkgconfig(quazip1-qt6)
BuildRequires:  pkgconfig(sdl2) >= 2.32.0
%if %{with qt}
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6WebEngineCore)
BuildRequires:  cmake(Qt6WebEngineWidgets)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6OpenGLWidgets)
%endif
BuildRequires:  cmake(sirit)
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
%ifarch aarch64
Provides:       bundled(oaknut) = 0~git9d09110
%endif
Provides:       bundled(simpleini) = 0~git%{?shortcommit19}
Provides:       bundled(stb_dxt) = %{stbdxt_ver}
Provides:       bundled(tzdb_to_nx) = 0~git%{?shortcommit20}


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

mkdir -p src/dynarmic/externals/mcl
tar -xf %{S:110} -C src/dynarmic/externals/mcl --strip-components 1
%{__scm_apply_patch -p1 -q} -d src/dynarmic/externals/mcl -i ../../../../.patch/mcl/0001-assert-macro.patch
sed \
  -e '/find_package/s|mcl|\0_DISABLED|g' \
  -i src/dynarmic/CMakeLists.txt

sed \
%if %{without xbyak}
  -e '/find_/s|xbyak|xbyak_DISABLED|g' \
%endif
  -e '/-pedantic-errors/d' \
  -e '/-mtune=core2/d' \
  -i src/dynarmic/CMakeLists.txt

pushd externals
rm -rf \
  ffmpeg/ffmpeg/* gamemode getopt libusb
%ifarch x86_64
rm -rf sse2neon
%endif

mkdir -p unordered-dense
tar -xf %{S:111} -C unordered-dense --strip-components 1
%if %{without vma}
mkdir -p VulkanMemoryAllocator
tar -xf %{S:12} -C VulkanMemoryAllocator --strip-components 1
%endif
%if %{without xbyak}
mkdir -p xbyak
tar -xf %{S:13} -C xbyak --strip-components 1
sed -e '/find_package/s|xbyak|\0_DISABLED|g' -i CMakeLists.txt
%endif
%if %{with webservice}
%if %{without httplib}
mkdir -p cpp-httplib
tar -xf %{S:16} -C cpp-httplib --strip-components 1
sed -e 's|zstd::libzstd|zstd::zstd|g' -i cpp-httplib/CMakeLists.txt
sed -e '/find_package/s|httplib|\0_DISABLED|g' -i ../CMakeLists.txt
%endif
mkdir -p cpp-jwt
tar -xf %{S:17} -C cpp-jwt --strip-components 1
sed -e '/find_package/s|cpp-jwt|\0_DISABLED|g' -i ../CMakeLists.txt
%endif
%if %{without mbedtls}
mkdir -p mbedtls
tar -xf %{S:18} -C mbedtls --strip-components 1
tar -xf %{S:180} -C mbedtls/framework --strip-components 1
%{__scm_apply_patch -p1 -q} -d mbedtls -i ../../.patch/mbedtls/0002-aesni-fix.patch
%{__scm_apply_patch -p1 -q} -d mbedtls -i ../../.patch/mbedtls/0003-aesni-fix.patch
sed \
  -e '/find_package/s|mbedtls|\0_DISABLED|g' \
  -i CMakeLists.txt
%endif
mkdir -p simpleini
tar -xf %{S:19} -C simpleini --strip-components 1
mkdir -p nx_tzdb/tzdb_to_nx
tar -xf %{S:20} -C nx_tzdb/tzdb_to_nx --strip-components 1
tar -xf %{S:200} -C nx_tzdb/tzdb_to_nx/externals/tz/tz --strip-components 1
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
mkdir -p boost-headers
tar -xf %{S:23} -C boost-headers --strip-components 1

popd

find . -type f -exec chmod -x {} ';'
find . -type f -name '*.sh' -exec chmod +x {} ';'

pushd externals
%if %{with webservice}
%if %{without httplib}
cp -p cpp-httplib/LICENSE LICENSE.cpp-httplib
%endif
cp -p cpp-jwt/LICENSE LICENSE.cpp-jwt
%endif
cp -p FidelityFX-FSR/license.txt LICENSE.FidelityFX-FSR
%if %{without mbedtls}
cp -p mbedtls/LICENSE LICENSE.mbedtls
%endif
cp -p nx_tzdb/tzdb_to_nx/LICENSE LICENSE.tzdb_to_nx
cp -p simpleini/LICENCE.txt LICENSE.simpleini
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

sed \
  -e '/find_program/s|GIT git|GIT cp|g' \
  -e 's|FATAL_ERROR|STATUS|g' \
  -i externals/nx_tzdb/CMakeLists.txt

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
  -e 's|-Wno-attributes|\0 -Wno-error=array-bounds -Wno-error=shadow -Wno-error=unused-variable -Wno-error=missing-declarations|' \
  -i src/CMakeLists.txt

%if %{with clang}
echo 'set_target_properties(yuzu PROPERTIES INTERPROCEDURAL_OPTIMIZATION true)' \
  >> src/yuzu/CMakeLists.txt <<EOF
%endif


%build
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DYUZU_BUILD_PRESET:STRING="none" \
  -DYUZU_SYSTEM_PROFILE:STRING="none" \
  -DYUZU_ENABLE_LTO:BOOL=ON \
%if %{with qt}
  -DYUZU_USE_BUNDLED_QT:BOOL=OFF \
  -DENABLE_QT_TRANSLATION:BOOL=ON \
  -DENABLE_UPDATE_CHECKER:BOOL=OFF \
  -DENABLE_QT6:BOOL=ON \
%else
  -DENABLE_QT:BOOL=OFF \
%endif
  -DYUZU_CHECK_SUBMODULES:BOOL=OFF \
  -DYUZU_USE_CPM:BOOL=OFF \
  -DCPM_DOWNLOAD_ALL:BOOL=OFF \
  -DYUZU_DOWNLOAD_TIME_ZONE_DATA:BOOL=OFF \
  -DYUZU_ENABLE_PORTABLE:BOOL=OFF \
  -DYUZU_ROOM:BOOL=ON \
  -DYUZU_USE_FASTER_LD:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_SDL2:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_VULKAN_SPIRV_TOOLS:BOOL=OFF \
  %{!?with_httplib:-DYUZU_USE_SYSTEM_HTTPLIB:BOOL=OFF} \
  -DYUZU_USE_EXTERNAL_VULKAN_UTILITY_LIBRARIES:BOOL=OFF \
  %{?with_ffmpeg:-DYUZU_USE_BUNDLED_FFMPEG:BOOL=OFF} \
  -DYUZU_USE_BUNDLED_LIBUSB:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPENSSL:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPUS:BOOL=OFF \
  -DYUZU_USE_QT_WEB_ENGINE:BOOL=ON \
  %{!?with_tests:-DYUZU_TESTS:BOOL=OFF} \
  %{!?with_webservice:-DENABLE_WEB_SERVICE:BOOL=OFF} \
  -DENABLE_WIFI_SCAN:BOOL=OFF \
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=OFF \
  -DDYNARMIC_ENABLE_LTO:BOOL=ON \
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_FMT:BOOL=ON \
  -DDYNARMIC_TESTS:BOOL=OFF \
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
* Wed Nov 26 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.4.28044-0.1.20251125git46239da
- 0.0.4-rc3

* Fri Nov 21 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.4.28031-0.1.20251121git7371373
- 0.0.4-rc3.test3

* Mon Nov 10 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.4.27984-0.1.20251109git4286302
- 0.0.4 rc2

* Sat Nov 08 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.4.27977-0.1.20251108git312c1cc
- rc2.test2

* Mon Oct 27 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.4.27896-0.1.20251027gitdd9cae4
- 0.0.4 test

* Sat Sep 06 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.3.27675-1.20250905git718891d
- 0.0.3

* Sat Aug 23 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.3~rc3.275617-1.20250822gita51953e
- 0.0.3-rc3

* Thu Jul 31 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.3~rc2.27538-1.20250730gitc609389
- 0.0.3-rc2

* Sun Jul 27 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.3~rc1.27522-1.20250727giteeb6876
- 0.0.3-rc1

* Sun Jun 15 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.2.27370-1.20250615gitcf00554
- Bundle ffmpeg until internal codecs is not needed

* Mon May 19 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.2.27303-1.20250519git3cad73d
- Initial spec
