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

%global commit 6cdaf3355901c74f79b40104db054f41b58176d8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230319
%bcond_with snapshot

%bcond_without ea
%if %{without ea}
%global with_mainline 1
%endif

# Enable system boost
%bcond_without boost
# Enable system dynarmic
%bcond_without dynarmic
# Enable system mbedtls (needs cmac builtin support)
%bcond_with mbedtls
# Disable Qt build
%bcond_without qt
# Build tests
%bcond_with tests

%global commit1 07c614f91b0af5335e1f9c0653c2d75e7b5f53bd
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dynarmic

%global commit2 9b0fc3e7b02afe97895eb3e945fe800c3a7485ac
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 VulkanMemoryAllocator

%global commit3 ab75463999f4f3291976b079d42d52ee91eebf3f
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 sirit

%global commit5 c214f6f2d1a7253bb0e9f195c2dc5b0659dc99ef
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%global commit6 6d963fbe8d415399d65e94db7910bbd22fe3741c
%global shortcommit6 %(c=%{commit6}; echo ${c:0:6})
%global srcname6 cpp-httplib

%global commit7 e12ef06218596b52d9b5d6e1639484866a8e7067
%global shortcommit7 %(c=%{commit7}; echo ${c:0:6})
%global srcname7 cpp-jwt

%global commit8 8c88150ca139e06aa2aae8349df8292a88148ea1
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 mbedtls

%global commit9 212afa2394a74226dcf1b7996a570aae17debb69
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 tzdb_to_nx

%global commit10 ce4d77644d2793027bb27f095dec7b530edcd947
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 tz

%global glad_ver 0.1.29
%global nxtzdb_ver 230404
%global stbdxt_ver 1.12
%global vkh_ver 1.3.246

%global vcm_url   https://github.com/yuzu-emu
%global vcea_url  https://github.com/pineappleEA
%global ext_url  %{vcm_url}

%if %{with ea}
%global vc_version 3832
%global vc_name pineapple-src
%global vc_tarball EA
%global vc_url  %{vcea_url}
%global repo ea
%else
%global vc_name %{name}
%if 0%{?with_mainline}
%global vc_version 1501
%global vc_name %{name}-mainline
%global vc_tarball mainline-0
%global vc_url  %{vcm_url}
%global repo mainline
%endif
%endif

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%else
%global shortcommit 0
%endif
%global dist %{?repo:.%{repo}}%{?dist}

%global appname org.yuzu_emu.%{name}


Name:           yuzu
Version:        %{vc_version}
Release:        1%{?dist}
Summary:        A Nintendo Switch Emulator

License:        GPL-2.0-or-later AND MIT AND Apache-2.0 WITH LLVM-exception AND MPL-2.0%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_mbedtls: AND (Apache-2.0 OR GPL-2.0-or-later)}%{!?with_boost: AND BSL-1.0}
URL:            https://yuzu-emu.org

%if %{with snapshot}
Source0:        %{vc_url}/%{vc_name}/archive/%{commit}/%{vc_name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{vc_name}/archive/%{vc_tarball}-%{version}/%{vc_name}-%{version}.tar.gz
%endif

%dnl %if %{without ea}
%if %{without dynarmic}
Source1:        https://github.com/MerryMage/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%endif
Source2:        https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{ext_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source5:        https://github.com/KhronosGroup/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/yhirose/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/arun11299/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
%if !%{with mbedtls}
Source8:        %{ext_url}/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
%endif
Source9:        https://github.com/lat9nq/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       https://github.com/eggert/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%dnl %endif

Source20:       https://api.yuzu-emu.org/gamedb#/compatibility_list.json

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-Revert-CMakeLists-Require-a-minimum-of-boost-1.79.0.patch
Patch12:        0001-Disable-telemetry-initial-dialog.patch
Patch13:        0001-appstream-validate.patch
Patch14:        0001-boost-build-fix.patch
Patch15:        0001-Lower-the-SDL2-requirement-a-bit.patch

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
BuildRequires:  llvm
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
%if %{with boost}
BuildRequires:  boost-devel >= 1.76.0
%endif
%if %{with tests}
BuildRequires:  pkgconfig(catch2) >= 2.13.7
%endif
BuildRequires:  cmake(cubeb)
%if %{with dynarmic}
BuildRequires:  cmake(dynarmic) >= 6.4.7
%else
BuildRequires:  cmake(tsl-robin-map)
Provides:       bundled(dynarmic) = 0~git%{?shortcommit1}
%endif
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(fmt) >= 9
BuildRequires:  pkgconfig(INIReader)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  ffmpeg-devel
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
BuildRequires:  pkgconfig(sdl2)
%if %{with qt}
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5WebEngineCore)
BuildRequires:  pkgconfig(Qt5WebEngineWidgets)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  qt5-linguist
%endif
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
BuildRequires:  cmake(xbyak)
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(microprofile)
Provides:       bundled(vma) = ~git%{?shortcommit2}
Provides:       bundled(sirit) = 0~git%{?shortcommit4}
Provides:       bundled(cpp-httplib) = 0~git%{?shortcommit6}
Provides:       bundled(cpp-jwt) = 0~git%{?shortcommit7}
Provides:       bundled(stb_dxt) = %{stbdxt_ver}
Provides:       bundled(tzdb_to_nx) = ~git%{?shortcommit9}

%if "%{?repo}"
Provides:       %{name}%{?repo:-%{repo}}%{?_isa} = %{version}-%{release}
%endif

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
%autosetup -n %{vc_name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{vc_tarball}-%{version}} -N -p1

%if %{with ea}
pushd externals
rm -rf cubeb/* discord-rpc enet ffmpeg/ffmpeg/* inih libressl libusb opus/opus/* SDL vcpkg Vulkan-Headers xbyak
%if %{with mbedtls}
rm -rf mbedtls
%endif
popd
find \( -name '*.c*' -or -name '*.h*' -or -name '*.cmake' \) -exec sed -i 's/\r$//' {} \;
find \( -name '*.qrc' -or -name '*.qss' -or -name '*.theme' -or -name '*.ts' \) -exec sed -i 's/\r$//' {} \;
find \( -name '*.desktop' -or -name '*.txt' -or -name '*.xml' \) -exec sed -i 's/\r$//' {} \;
find \( -iname '*license*' -or -iname '*README*' \) -exec sed -i 's/\r$//' {} \;
%endif
%if %{without dynarmic}
tar -xf %{S:1} -C externals/dynarmic --strip-components 1
rm -rf externals/dynarmic/externals/{catch,fmt,robin-map,xbyak}
sed -e '/find_package/s|dynarmic|\0_DISABLED|g' -i CMakeLists.txt
%endif
mkdir -p externals/VulkanMemoryAllocator
tar -xf %{S:2} -C externals/VulkanMemoryAllocator --strip-components 1
tar -xf %{S:3} -C externals/sirit --strip-components 1
tar -xf %{S:5} -C externals/sirit/externals/SPIRV-Headers --strip-components 1
tar -xf %{S:6} -C externals/cpp-httplib --strip-components 1
tar -xf %{S:7} -C externals/cpp-jwt --strip-components 1
%if %{without mbedtls}
tar -xf %{S:8} -C externals/mbedtls --strip-components 1
%endif
mkdir externals/nx_tzdb/tzdb_to_nx
tar -xf %{S:9} -C externals/nx_tzdb/tzdb_to_nx --strip-components 1
tar -xf %{S:10} -C externals/nx_tzdb/tzdb_to_nx/externals/tz/tz --strip-components 1

%autopatch -p1

find . -type f -exec chmod -x {} ';'
find . -type f -name '*.sh' -exec chmod +x {} ';'

pushd externals
cp -p cpp-httplib/LICENSE LICENSE.cpp-httplib
cp -p cpp-jwt/LICENSE LICENSE.cpp-jwt
%if %{without dynarmic}
%cp -p dynarmic/LICENSE.txt LICENSE.dynarmic
%endif
cp -p FidelityFX-FSR/license.txt LICENSE.FidelityFX-FSR
%if %{without mbedtls}
cp -p mbedtls/LICENSE LICENSE.mbedtls
%endif
cp -p nx_tzdb/tzdb_to_nx/LICENSE LICENSE.tzdb_to_nx
cp -p sirit/LICENSE.txt LICENSE.sirit
cp -p VulkanMemoryAllocator/LICENSE.txt LICENSE.vma
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
%if 0%{?with_ea}
  -e 's|@TITLE_BAR_FORMAT_IDLE@|yuzu Early Access %{version}|g' \
  -e 's,@TITLE_BAR_FORMAT_RUNNING@,yuzu Early Access %{version} | {3},g' \
%endif
  -i src/common/scm_rev.cpp.in

sed \
  -e 's|GIT_PROGRAM git|GIT_PROGRAM true|g' \
  -e 's|${TZ_COMMIT_TIME}|1680663527|g' \
  -e 's|${TZDB_VERSION}|nxtzdb_ver|g' \
  -i externals/nx_tzdb/tzdb_to_nx/src/tzdb/CMakeLists.txt

# https://github.com/pineappleEA/pineapple-src/issues/80
rm -f src/core/network/network.h

sed -e 's|-Wno-attributes|\0 -Wno-error=array-bounds|' -i src/CMakeLists.txt

cp -f %{S:20} dist/compatibility_list/


%build
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  %{!?with_clang:-DYUZU_ENABLE_LTO:BOOL=ON} \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%else
  -DENABLE_QT:BOOL=OFF \
%endif
  -DYUZU_CHECK_SUBMODULES:BOOL=OFF \
  -DYUZU_ROOM:BOOL=ON \
  -DYUZU_USE_FASTER_LD:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_SDL2:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_VULKAN_HEADERS:BOOL=OFF \
  -DYUZU_USE_BUNDLED_FFMPEG:BOOL=OFF \
  -DYUZU_USE_BUNDLED_LIBUSB:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPUS:BOOL=OFF \
  -DYUZU_USE_QT_WEB_ENGINE:BOOL=ON \
  %{!?with_tests:-DYUZU_TESTS:BOOL=OFF} \
  -DENABLE_WEB_SERVICE:BOOL=ON \
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
%license LICENSE.txt externals/LICENSE.*
%doc README.md
%{_bindir}/%{name}-cmd
%{_bindir}/%{name}-room
%dnl %{_mandir}/man6/%{name}.6*


%if %{with qt}
%files qt
%license LICENSE.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{appname}.xml
%{_metainfodir}/%{appname}.metainfo.xml
%dnl %{_mandir}/man6/%{name}-qt.6*
%endif


%changelog
* Mon Apr 03 2023 Phantom X <megaphantomx at hotmail dot com> - 3497-1.ea
- Build with gcc again

* Fri Mar 24 2023 Phantom X <megaphantomx at hotmail dot com> - 3472-1.ea
- 3472 ea
- Tag release support

* Fri Mar 17 2023 Phantom X <megaphantomx at hotmail dot com> - 3459-1.20230315git7ddcf90.ea
- clang optional support
- R: ninja-build

* Tue Dec 06 2022 Phantom X <megaphantomx at hotmail dot com> - 3188-1.20221205git4a88ba8.ea
- System dynarmic, inih and xbyak

* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 3118-1.20221113gite49dd26.ea
- Enable WebEngine applet

* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 2897-1.20220811git7ce78aa
- 2897 ea

* Sun Aug 07 2022 Phantom X <megaphantomx at hotmail dot com> - 2890-1.20220805git3f64006
- 2890 ea

* Sat Jul 30 2022 Phantom X <megaphantomx at hotmail dot com> - 2877-1.20220730git7b69f77
- 2877 ea
- BR: libenet

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 2836-1.20220715git2a98837
- 2836 ea

* Sun Jul 03 2022 Phantom X <megaphantomx at hotmail dot com> - 2814-1.20220630gitad70366
- 2814 ea

* Thu Jun 30 2022 Phantom X <megaphantomx at hotmail dot com> - 2806-1.20220630gitad70366
- 2806 ea

* Wed Jun 15 2022 Phantom X <megaphantomx at hotmail dot com> - 2787-1.20220615gitca4f54b
- 2787 ea

* Thu Jun 09 2022 Phantom X <megaphantomx at hotmail dot com> - 2764-1.20220608git43bf9ef
- 2764 ea

* Sun May 29 2022 Phantom X <megaphantomx at hotmail dot com> - 2743-1.20220529git5dfc24a
- 2743 ea

* Sat May 07 2022 Phantom X <megaphantomx at hotmail dot com> - 2721-1.20220507git226e463
- 2721 ea

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 2706-1.20220419git8aa17b7
- 2706 ea

* Wed Apr 20 2022 Phantom X <megaphantomx at hotmail dot com> - 2687-1.20220416git8aa17b7
- 2687 ea

* Sat Apr 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2682-1.20220416git2a9a838
- 2682 ea

* Sun Apr 10 2022 Phantom X <megaphantomx at hotmail dot com> - 2665-1.20220409git7a13d2c
- 2665 ea

* Tue Apr 05 2022 Phantom X <megaphantomx at hotmail dot com> - 2645-1.20220404gitcea32b5
- 2645 ea

* Mon Apr 04 2022 Phantom X <megaphantomx at hotmail dot com> - 2644-1.20220404gitcea32b5
- 2644 ea
- SoundTouch is not needed anymore

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 2552-2.20220315git24d7346
- gcc 12 build fixes

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2552-1.20220315git24d7346
- 2552 ea

* Sun Mar 13 2022 Phantom X <megaphantomx at hotmail dot com> - 2545-1.20220313gitb98acbe
- 2545 ea

* Sun Mar 06 2022 Phantom X <megaphantomx at hotmail dot com> - 2528-1.20220306git8667d19
- 2528 ea

* Mon Feb 28 2022 Phantom X <megaphantomx at hotmail dot com> - 2520-1.20220228gita1e50a2
- 2520 ea

* Tue Feb 22 2022 Phantom X <megaphantomx at hotmail dot com> - 2503-1.20220222git566fc94
- 2503 ea

* Tue Feb 15 2022 Phantom X <megaphantomx at hotmail dot com> - 2493-1.20220215git3b47515
- 2493 early access

* Wed Feb 09 2022 Phantom X <megaphantomx at hotmail dot com> - 912-1.20220208gitcd3dab4
- Initial spec
