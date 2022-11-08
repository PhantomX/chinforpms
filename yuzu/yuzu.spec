# Disable LTO. Crash.
%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 9b08ac8a80778d5d9e84e4d29c734f62a06b39dc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221106

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

%global commit1 2d4602a6516c67d547000d4c80bcc5f74976abdd
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dynarmic

%global commit2 1e80a47dffbda813604f0913e2ad68c7054c14e4
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 inih

%global commit3 aa292d56650bc28f2b2d75973fab2e61d0136f9c
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 sirit

%global commit4 c306b8e5786eeeb87b8925a8af5c3bf057ff5a90
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 xbyak

%global commit5 a3fdfe81465d57efc97cfd28ac6c8190fb31a6c8
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%global commit6 305a7abcb9b4e9e349843c6d563212e6c1bbbf21
%global shortcommit6 %(c=%{commit6}; echo ${c:0:6})
%global srcname6 cpp-httplib

%global commit7 e12ef06218596b52d9b5d6e1639484866a8e7067
%global shortcommit7 %(c=%{commit7}; echo ${c:0:6})
%global srcname7 cpp-jwt

%global commit8 8c88150ca139e06aa2aae8349df8292a88148ea1
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 mbedtls

%global glad_ver 0.1.29

%global gver .%{date}git%{shortcommit}

%global vcm_url   https://github.com/yuzu-emu
%global vcea_url  https://github.com/pineappleEA
%global ext_url  %{vcm_url}

%if 0%{?with_ea}
%global vc_name pineapple-src
%global vc_url  %{vcea_url}
%global repo ea
%else
%global vc_name %{name}
%if 0%{?with_mainline}
%global vc_name %{name}-mainline
%global vc_url  %{vcm_url}
%global repo mainline
%endif
%endif

%global appname org.yuzu_emu.%{name}


Name:           yuzu
Version:        3097
Release:        1%{?gver}%{?repo:.%{repo}}%{?dist}
Summary:        A Nintendo Switch Emulator

License:        GPLv2
URL:            https://yuzu-emu.org

Source0:        %{vc_url}/%{vc_name}/archive/%{commit}/%{vc_name}-%{shortcommit}.tar.gz
%dnl %if !0%{?with_ea}
Source1:        https://github.com/MerryMage/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/benhoyt/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/ReinUsesLisp/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/herumi/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/KhronosGroup/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/yhirose/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/arun11299/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
%if !%{with mbedtls}
Source8:        %{ext_url}/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
%endif
%dnl %endif

Source20:       https://api.yuzu-emu.org/gamedb#/compatibility_list.json

Patch0:         0001-Use-system-libraries.patch
Patch2:         0001-Disable-telemetry-initial-dialog.patch
Patch3:         0001-appstream-validate.patch

Patch10:        0001-boost-build-fix.patch
Patch11:        0001-nvflinger.cpp-ignore-Wconversion.patch
Patch12:        0001-gcc-ignore-Wmaybe-uninitialized.patch

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
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
BuildRequires:  pkgconfig(libenet)
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

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(dynarmic) = 0~git%{?shortcommit1}
Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(microprofile)
Provides:       bundled(inih) = 0~git%{?shortcommit2}
Provides:       bundled(xbyak) = 0~git%{?shortcommit3}
Provides:       bundled(sirit) = 0~git%{?shortcommit4}
Provides:       bundled(cpp-httplib) = 0~git%{?shortcommit6}
Provides:       bundled(cpp-jwt) = 0~git%{?shortcommit7}
%if !%{with mbedtls}
Provides:       bundled(mbedtls) = 0~git%{?shortcommit8}
%endif

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
%autosetup -n %{vc_name}-%{commit} -N -p1

%if 0%{?with_ea}
pushd externals
rm -rf cubeb/* discord-rpc enet ffmpeg/ffmpeg/* libressl libusb opus/opus/* SDL vcpkg Vulkan-Headers
%if %{with mbedtls}
rm -rf mbedtls
%endif
popd
find \( -name '*.c*' -or -name '*.h*' -or -name '*.cmake' \) -exec sed -i 's/\r$//' {} \;
find \( -name '*.qrc' -or -name '*.qss' -or -name '*.theme' -or -name '*.ts' \) -exec sed -i 's/\r$//' {} \;
find \( -name '*.desktop' -or -name '*.txt' -or -name '*.xml' \) -exec sed -i 's/\r$//' {} \;
find \( -iname '*license*' -or -name '*COPYRIGHT*' -or -iname '*README*' \) -exec sed -i 's/\r$//' {} \;
%endif
tar -xf %{S:1} -C externals/dynarmic --strip-components 1
mkdir -p externals/inih/inih
tar -xf %{S:2} -C externals/inih/inih --strip-components 1
tar -xf %{S:3} -C externals/sirit --strip-components 1
tar -xf %{S:4} -C externals/xbyak --strip-components 1
tar -xf %{S:5} -C externals/sirit/externals/SPIRV-Headers --strip-components 1
tar -xf %{S:6} -C externals/cpp-httplib --strip-components 1
tar -xf %{S:7} -C externals/cpp-jwt --strip-components 1
%if !%{with mbedtls}
tar -xf %{S:8} -C externals/mbedtls --strip-components 1
%endif


%autopatch -p1

find . -type f -exec chmod -x {} ';'
find . -type f -name '*.sh' -exec chmod +x {} ';'

pushd externals
cp -p cpp-httplib/LICENSE LICENSE.cpp-httplib
cp -p cpp-jwt/LICENSE LICENSE.cpp-jwt
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

%if %{with boost}
sed \
  -e '/Boost/s|CONFIG ||g' \
  -e '/Boost/s| headers||g' \
  -i CMakeLists.txt
%endif

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

# https://github.com/pineappleEA/pineapple-src/issues/80
rm -f src/core/network/network.h

cp -f %{S:20} dist/compatibility_list/


%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%else
  -DENABLE_QT:BOOL=OFF \
%endif
  -DYUZU_CHECK_SUBMODULES:BOOL=OFF \
  -DYUZU_USE_EXTERNAL_SDL2:BOOL=OFF \
  -DYUZU_USE_BUNDLED_FFMPEG:BOOL=OFF \
  -DYUZU_USE_BUNDLED_OPUS:BOOL=OFF \
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
rm -rf %{buildroot}%{_libdir}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license license.txt externals/{COPYRIGHT,LICENSE}.*
%doc README.md
%{_bindir}/%{name}-cmd
%{_bindir}/%{name}-room
%dnl %{_mandir}/man6/%{name}.6*


%if %{with qt}
%files qt
%license license.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{appname}.xml
%{_metainfodir}/%{appname}.metainfo.xml
%dnl %{_mandir}/man6/%{name}-qt.6*
%endif


%changelog
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
