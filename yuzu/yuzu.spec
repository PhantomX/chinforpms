# Disable LTO. Crash.
%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 7a13d2c502e6519d39afb434fbb4b925c7a2dd15
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220409

%global with_ea 1
%if !0%{?with_ea}
%global with_mainline 1
%endif

# Enable system boost
%bcond_without boost
# Enable system mbedtls (needs cmac builtin support)
%bcond_with mbedtls
# Disable Qt build
%bcond_without qt

%if !0%{?with_ea}
%global commit1 a8cbfd9af4f3f3cdad6efcd067e76edec76c1338
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dynarmic

%global commit2 1e80a47dffbda813604f0913e2ad68c7054c14e4
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 inih

%global commit3 a39596358a3a5488c06554c0c15184a6af71e433
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 sirit

%global commit4 c306b8e5786eeeb87b8925a8af5c3bf057ff5a90
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 xbyak

%global commit5 a3fdfe81465d57efc97cfd28ac6c8190fb31a6c8
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%global commit6 9648f950f5a8a41d18833cf4a85f5821b1bcac54
%global shortcommit6 %(c=%{commit5}; echo ${c:0:6})
%global srcname6 cpp-httplib

%global commit8 8c88150ca139e06aa2aae8349df8292a88148ea1
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 mbedtls
%endif

%global glad_ver 0.1.29

%global gver .%{date}git%{shortcommit}

%global vcm_url   https://github.com/yuzu-emu
%global vcea_url  https://github.com/pineappleEA

%if 0%{?with_ea}
%global vc_name pineapple-src
%global vc_url  %{vcea_url}
%else
%global vc_name %{name}
%if 0%{?with_mainline}
%global vc_name %{name}-mainline
%global vc_url  %{vcm_url}
%endif
%endif


Name:           yuzu
Version:        2665
Release:        1%{?gver}%{?dist}
Summary:        A Nintendo Switch Emulator

License:        GPLv2
URL:            https://yuzu-emu.org

Source0:        %{vc_url}/%{vc_name}/archive/%{commit}/%{vc_name}-%{shortcommit}.tar.gz
%if !0%{?with_ea}
Source1:        https://github.com/MerryMage/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/ReinUsesLisp/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/benhoyt/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/herumi/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/KhronosGroup/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/yhirose/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
%if !%{with mbedtls}
Source8:        %{vc_url}/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
%endif
%endif

Source20:       https://api.yuzu-emu.org/gamedb#/compatibility_list.json

Patch0:         0001-Use-system-libraries.patch
%if %{with boost}
Patch1:         0001-fix-system-boost-detection.patch
%endif
Patch2:         0001-Disable-telemetry-initial-dialog.patch
%if 0%{?with_ea}
Patch10:        0001-gcc-12-build-fix.patch
%endif

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
%if %{with boost}
BuildRequires:  boost-devel >= 1.76.0
%endif
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(fmt) >= 8.0.1
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires:  ffmpeg-devel
%endif
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libzstd) >= 1.5.0
%if %{with mbedtls}
BuildRequires:  mbedtls >= 2.6.10
%endif
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

Requires:       vulkan-loader%{?_isa}

Provides:       bundled(dynarmic) = 0~git%{?shortcommit1}
Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(microprofile)
Provides:       bundled(inih) = 0~git%{?shortcommit2}
Provides:       bundled(xbyak) = 0~git%{?shortcommit3}
Provides:       bundled(sirit) = 0~git%{?shortcommit4}
Provides:       bundled(cpp-httplib) = 0~git%{?shortcommit6}
%if !%{with mbedtls}
Provides:       bundled(mbedtls) = 0~git%{?shortcommit8}
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
%autosetup -n %{vc_name}-%{commit} -p1

%if 0%{?with_ea}
pushd externals
rm -rf cubeb/* discord-rpc ffmpeg/ffmpeg/* libressl libusb opus/opus/* SDL Vulkan-Headers
%if %{with mbedtls}
rm -rf mbedtls
%endif
popd
%else
tar -xf %{S:1} -C externals/dynarmic --strip-components 1
tar -xf %{S:2} -C externals/inih/inih --strip-components 1
tar -xf %{S:3} -C externals/sirit --strip-components 1
tar -xf %{S:4} -C externals/xbyak --strip-components 1
tar -xf %{S:5} -C externals/sirit/externals/SPIRV-Headers --strip-components 1
tar -xf %{S:6} -C externals/cpp-httplib --strip-components 1
%if !%{with mbedtls}
tar -xf %{S:8} -C externals/mbedtls --strip-components 1
%endif
%endif

find . -type f -exec chmod -x {} ';'
find . -type f -name '*.sh' -exec chmod +x {} ';'

pushd externals
cp -p cpp-httplib/LICENSE LICENSE.cpp-httplib
cp -p dynarmic/LICENSE.txt LICENSE.dynarmic
cp -p FidelityFX-FSR/license.txt LICENSE.FidelityFX-FSR
%if !%{with mbedtls}
cp -p mbedtls/LICENSE LICENSE.mbedtls
%endif
cp -p sirit/LICENSE.txt LICENSE.sirit
cp -p xbyak/COPYRIGHT COPYRIGHT.xbyak
sed -e 's/\r//' -i COPYRIGHT.xbyak
popd

%if !%{with mbedtls}
sed \
  -e '/find_package/s|MBEDTLS|\0_DISABLED|g' \
  -i externals/CMakeLists.txt
%endif

sed \
  -e '/-pedantic-errors/d' \
  -i externals/dynarmic/CMakeLists.txt

sed -e '/find_packages/s|Git|\0_DISABLED|g' -i CMakeModules/GenerateSCMRev.cmake

sed \
  -e 's|@GIT_REV@|%{commit}|g' \
  -e 's|@GIT_BRANCH@|main|g' \
  -e 's|@GIT_DESC@|%{shortcommit}|g' \
  -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
  -i src/common/scm_rev.cpp.in

%build
mkdir -p dist/compatibility_list/
cp %{S:20} dist/compatibility_list/

%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%else
  -DENABLE_QT:BOOL=OFF \
%endif
  -DYUZU_USE_EXTERNAL_SDL2:BOOL=OFF \
  -DYUZU_USE_BUNDLED_FFMPEG:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPUS:BOOL=OFF \
  -DYUZU_FIX_CMAKE_BOOST:BOOL=ON \
  -DYUZU_TESTS:BOOL=OFF \
  -DENABLE_WEB_SERVICE:BOOL=ON \
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=OFF \
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}/cmake

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license license.txt externals/{COPYING,COPYRIGHT,LICENSE}.*
%doc README.md
%{_bindir}/%{name}-cmd
%dnl %{_mandir}/man6/%{name}.6*


%if %{with qt}
%files qt
%license license.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml
%dnl %{_mandir}/man6/%{name}-qt.6*
%endif


%changelog
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
