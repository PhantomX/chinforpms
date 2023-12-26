# Selective LTO.
%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond_without clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 2d08d3dc9495135f5488f74cd7a1849b99d12d0a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220308
%bcond_with snapshot

%global commit10 c9706bdda0ac22b9856f1aa8261e5b9e15cd20c5
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 glslang

%global commit11 8afec6c55e3a0f72368a5a085203bab1b8828ffb
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 rcheevos

%global commit12 9f4c61a31435a7a90a314fc68aeb386c92a09c0f
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 Vulkan-Headers

%global commit13 5cfd28d476c6859617878f951931b8ce7d36b9df
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 fmt

%bcond_with     native
# Enable system fmt
%bcond_with fmt
# Enable system soundtouch (needs no exception)
%bcond_with soundtouch
%bcond_without  vulkan

%global appbin %{name}-qt
%global appres PCSX2

%global perms_pcsx2 %caps(cap_net_admin,cap_net_raw+eip)

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global glad_ver 0.1.25
%global gsl_ver 4.0.0
%global imgui_ver 1.88
%global jpgc_ver 1.05
%global simpleini_ver 4.17
%global soundtouch_ver 2.3.1
%global xxhash_ver 0.8.1

Name:           pcsx2
Version:        1.7.5332
Release:        1%{?dist}
Summary:        A Sony Playstation2 emulator

License:        GPL-3.0-only AND LGPL-3.0-or-later AND MIT%{!?with_soundtouch: AND LGPL-2.1}
URL:            https://github.com/PCSX2/pcsx2

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source10:       https://github.com/KhronosGroup/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       https://github.com/RetroAchievements/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%if %{without vulkan}
Source12:       https://github.com/KhronosGroup/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
%endif
%if %{without fmt}
Source13:       https://github.com/fmtlib/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%endif

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Set-datadir-to-RPM-packaging.patch
Patch2:         0001-common-build-as-static.patch
Patch3:         0001-glad-build-as-static.patch
Patch4:         0001-glslang-build-as-static.patch
Patch5:         0001-imgui-build-as-static.patch
Patch6:         0001-simpleini-build-as-static.patch
Patch7:         0001-Qt-do-not-set-a-default-theme.patch
Patch8:         0001-cubeb-always-set-same-audiostream-name.patch
Patch10:        0001-Lower-the-SDL2-requirement-a-bit.patch
Patch11:        0001-Fix-translation-names.patch

ExclusiveArch:  x86_64

%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  cmake(FastFloat)
%if %{with fmt}
BuildRequires:  pkgconfig(fmt) >= 10.1.1
%else
Provides:       bundled(fmt) = 0~git%{shortcommit13}
%endif
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(libbacktrace)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(libcpuinfo)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsparsehash)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzip) >= 1.8.0
BuildRequires:  pkgconfig(libzstd) >= 1.4.5
BuildRequires:  libzip-tools
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  cmake(RapidJSON)
BuildRequires:  cmake(ryml) >= 0.4.1
BuildRequires:  cmake(Qt6Core) >= 6.6
BuildRequires:  cmake(Qt6CoreTools)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6GuiTools)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6WidgetsTools)
BuildRequires:  qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires:  pkgconfig(sdl2) >= 2.0.22
%if %{with soundtouch}
BuildRequires:  cmake(SoundTouch)
%else
Provides:       bundled(soundtouch) = %{soundtouch_ver}
%endif
BuildRequires:  cmake(WebP)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  cmake(xbyak)
BuildRequires:  pkgconfig(zlib)
%if %{with vulkan}
BuildRequires:  cmake(VulkanHeaders) >= 1.3.272
%endif
BuildRequires:  fonts-rpm-macros
BuildRequires:  gettext
BuildRequires:  libaio-devel
BuildRequires:  perl-interpreter

Requires:       pcsx2_patches
Requires:       joystick
Requires:       google-roboto-fonts
Requires:       google-roboto-mono-fonts
Requires:       hicolor-icon-theme
Requires:       libGL%{?_isa}
Requires:       libwayland-egl%{?_isa}
Requires:       sdl_gamecontrollerdb >= 0-42
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(gsl) = %{gsl_ver}
Provides:       bundled(glslang) = 0~git%{shortcommit10}
Provides:       bundled(imgui) = %{imgui_ver}
Provides:       bundled(jpeg-compressor) = %{jpgc_ver}
Provides:       bundled(rcheevos) = 0~git%{shortcommit11}
Provides:       bundled(simpleini) = %{simpleini_ver}
Provides:       bundled(xxhash) = %{xxhash_ver}
%dnl Provides:       bundled(zydis) = 0~git


%description
A Playstation 2 emulator. Requires a dump of a real PS2 BIOS (not included).

It requires a CPU with SSE4 instructions. If your CPU does not
support this instruction set, it does not have enough horsepower to run
this emulator anyway.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

rm -rf .git

pushd 3rdparty
rm -rf \
  cpuinfo cubeb d3d12memalloc ffmpeg GL gtest libchdr libwebp \
  libpng libzip lzma qt rainterface rapidjson rapidyaml sdl2 wil \
  winpixeventruntime xbyak xz zlib zstd zydis

tar -xf %{S:10} -C glslang/glslang --strip-components 1
tar -xf %{S:11} -C rcheevos/rcheevos --strip-components 1

%if %{with fmt}
rm -rf fmt
%else
tar -xf %{S:13} -C fmt/fmt --strip-components 1
sed -e '/find_package/s|fmt|\0_DISABLED|g' -i ../cmake/SearchForStuff.cmake
cp -p fmt/fmt/LICENSE LICENSE.fmt
%endif

%if %{with soundtouch}
rm -rf soundtouch
%else
sed -e '/find_package/s|SoundTouch|\0_DISABLED|g' -i ../cmake/SearchForStuff.cmake
cp -p soundtouch/COPYING.TXT COPYING.soundtouch
%endif

%if %{without vulkan}
tar -xf %{S:12} -C vulkan-headers --strip-components 1
sed -e '/find_package/s|VulkanHeaders|\0_DISABLED|g' -i ../cmake/SearchForStuff.cmake
%endif

cp -p glslang/glslang/LICENSE.txt LICENSE.glslang
#cp -p rainterface/LICENSE LICENSE.rainterface
cp -p rcheevos/rcheevos/LICENSE LICENSE.rcheevos
cp -p simpleini/LICENCE.txt LICENSE.simpleini
%dnl cp -p zydis/LICENSE LICENSE.zydis
popd

# To remove executable bits from man, doc and icon files
chmod -x pcsx2/Docs/GPL.txt pcsx2/Docs/License.txt pcsx2/Docs/PCSX2_FAQ.md \
  pcsx2/Docs/Configuration_Guide/Configuration_Guide.md

# Remove DOS encoding errors in txt files
sed -i 's/\r//' pcsx2/Docs/GPL.txt
sed -i 's/\r//' pcsx2/Docs/License.txt

%if %{with snapshot}
sed -i \
  -e '/PCSX2_GIT_REV/s| ""| "v%{version}-git%{shortcommit}"|g' \
%else
sed -i \
  -e '/PCSX2_GIT_REV/s| ""| "v%{version}"|g' \
  -e '/PCSX2_GIT_TAG/s| ""| "v%{version}"|g' \
%endif
  cmake/Pcsx2Utils.cmake

sed -e '/DEFAULT_USE_SYSTEM_RYML/s|OFF|ON|' -i cmake/BuildParameters.cmake

rename -a - _ pcsx2-qt/Translations/*.ts
rename _ - pcsx2-qt/Translations/*.ts

sed \
  -e 's|_RPM_DATADIR_|%{_datadir}/%{appres}|g' \
  -e 's|_RPM_QTTDIR_|%{_qt6_translationdir}|g' \
  -i pcsx2/Pcsx2Config.cpp pcsx2-qt/Translations.cpp


%build

%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  %{!?with_clang:-DLTO_PCSX2_CORE:BOOL=ON} \
  -DDISABLE_BUILD_DATE:BOOL=ON \
  -DBUILD_REPLAY_LOADERS:BOOL=OFF \
  -DQT_BUILD:BOOL=ON \
  -DX11_API:BOOL=ON \
  -DWAYLAND_API:BOOL=ON \
  -DCMAKE_BUILD_STRIP:BOOL=OFF \
%if %{with native}
  -DDISABLE_ADVANCE_SIMD:BOOL=OFF \
%else
  -DDISABLE_ADVANCE_SIMD:BOOL=ON \
%endif
  -DUSE_VTUNE:BOOL=OFF \
  -DCUBEB_API:BOOL=ON \
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DENABLE_SETCAP:BOOL=OFF \
  -DENABLE_TESTS:BOOL=OFF \
  -DOpenGL_GL_PREFERENCE=GLVND \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/bin/%{appbin} %{buildroot}%{_bindir}/%{appbin}

mkdir -p %{buildroot}%{_datadir}/%{appres}
cp -r %{__cmake_builddir}/bin/{resources,translations} \
  %{buildroot}%{_datadir}/%{appres}/

rm -f %{buildroot}%{_datadir}/%{appres}/resources/game_controller_db.txt
ln -sf ../../SDL_GameControllerDB/gamecontrollerdb.txt \
  %{buildroot}%{_datadir}/%{appres}/resources/game_controller_db.txt

rm -f %{buildroot}%{_datadir}/%{appres}/resources/fonts/Roboto*
ln -sf ../../../fonts/google-roboto/Roboto-Regular.ttf \
  %{buildroot}%{_datadir}/%{appres}/resources/fonts/Roboto-Regular.ttf

ln -sf ../../../fonts/google-roboto-mono/'RobotoMono[wght].ttf' \
  %{buildroot}%{_datadir}/%{appres}/resources/fonts/RobotoMono-Medium.ttf

# Install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
ln -sf ../../../../PCSX2/resources/icons/AppIconLarge.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{appres}.png

for res in 16 22 24 32 36 48 64 72 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert bin/resources/icons/AppIconLarge.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{appres}.png
done

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{appbin}" \
  .github/workflows/scripts/linux/%{appbin}.desktop

%find_lang %{appbin} --with-qt


%files -f %{appbin}.lang
%license COPYING* 3rdparty/LICENSE.* %{!?with_soundtouch:3rdparty/COPYING*}
%doc README.md bin/docs/*.pdf
%{perms_pcsx2} %{_bindir}/%{appbin}
%{_datadir}/applications/%{appbin}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appres}.png
%dir %{_datadir}/%{appres}
%dir %{_datadir}/%{appres}/resources/
%dir %{_datadir}/%{appres}/translations/
%{_datadir}/%{appres}/resources/fonts
%{_datadir}/%{appres}/resources/fullscreenui
%{_datadir}/%{appres}/resources/icons
%{_datadir}/%{appres}/resources/shaders
%{_datadir}/%{appres}/resources/sounds
%{_datadir}/%{appres}/resources/GameIndex.yaml
%{_datadir}/%{appres}/resources/RedumpDatabase.yaml
%{_datadir}/%{appres}/resources/cover-placeholder.png
%{_datadir}/%{appres}/resources/game_controller_db.txt


%changelog
* Thu Oct 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.7.5136-1
- 1.7.5136
- BR: WebP

* Sun Sep 17 2023 Phantom X <megaphantomx at hotmail dot com> - 1.7.5025-1
- Add translations

* Tue Jan 03 2023 Phantom X <megaphantomx at hotmail dot com> - 1.7.3849-1
- Not instalable anymore, fix this

* Wed Dec 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3687-1
- 1.7.3687
- BR: xbyak

* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3348-1
- 1.7.3348
- rcheevos

* Fri Sep 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3316-1
- 1.7.3316
- BR: libcpuinfo

* Wed Sep 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3307-1
- 1.7.3307

* Wed Aug 31 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3264-1
- 1.7.3264

* Sat Aug 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3229-1
- 1.7.3229
- R: pcsx2_patches

* Fri Aug 12 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3195-1
- 1.7.3195

* Wed Jul 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3131-1
- 1.7.3131

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3079-1
- 1.7.3079

* Wed Jul 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3057-1
- 1.7.3057

* Mon Jul 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3043-1
- 1.7.3043

* Wed Jun 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3028-1
- 1.7.3028

* Thu Jun 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2991-1
- 1.7.2991
- Qt build
- Remove wrapper

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2953-1
- 1.7.2953

* Mon May 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2781-1
- 1.7.2769

* Sat May 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2715-1
- 1.7.2715

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2663-1
- 1.7.2663

* Sun Apr 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2582-1
- 1.7.2582

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2541-1
- 1.7.2541

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2465-1
- 1.7.2465

* Mon Mar 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2449-1
- 1.7.2449

* Tue Mar 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2421-1
- 1.7.2421 tag release

* Tue Feb 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-140.20220221git4e7ade8
- Update

* Thu Feb 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-139.20220216git5b6986c
- Bump

* Wed Feb 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-138.20220207gitaf64833
- Last snapshot

* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-137.20210821git94c6814
- Downgrade more

* Sun Nov 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-136.20211005git660c623
- Last snapshot that works well on potatoes

* Tue Oct 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-135.20211026git3705054
- Update

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-133.20211002git6035377
- Last snapshot

* Sat Sep 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-132.20210924git2406ae6
- Bump

* Thu Sep 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-131.20210902gitbb5bfda
- Bump
- Update SSE2 build warnings

* Sun Aug 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-130.20210821git94c6814
- Update

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-129.20210713git21908bd
- Update

* Tue Jul 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-128.20210705git6dd90ae
- Last snapshot

* Tue May 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-127.20210520gite011119
- Bump

* Sun May 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-126.20210430git6a2ed3d
- Update

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-125.20210430git5639273
- Bump

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-124.20210419git6f7890b
- Last snapshot

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-123.20210418git256afa8
- Update

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-122.20210407git05a31bd
- Bump

* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-121.20210323gitbc477e1
- Bump
- BR: libchdr, and patch to support system library

* Mon Mar 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-120.20210307gitb33321d
- Update

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-119.20210228gitf9d96f5
- New snapshot
- SSE4 is needed now by upstream, but a sse4 switch is added to maintain a SSE2
  minimal, for older CPUs that can run some not demanding games

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-118.20210212git7187b88
- Bump

* Thu Feb 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-117.20210204gitd55c611
- Update

* Wed Dec 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-114.20201223git74336d9
- New snapshot
- BR: yaml-cpp

* Sun Nov 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-113.20201128git76c98e7
- Bump

* Fri Nov 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-112.20201113git319287d
- Update
- BR: samplerate

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-111.20201030git7a2c94f
- Bump

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-110.20201021git418974a
- Bump

* Fri Oct  2 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-109.20201002git85c1aca
- New snapshot

* Sat Sep 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-108.20200919gite1ff498
- Bump

* Sat Sep 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-107.20200912git6229b20
- New snapshot

* Mon Aug 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-106.20200830git6f0011a
- New snapshot
- x86_64 support
- native switch

* Tue Aug 18 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-105.20200813git61f3258
- Bump
- EGL
- GTK3

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-104.20200729git95b5ab5
- New snapshot

* Fri Jul 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-103.20200717git30e6a7a
- Bump and test new cmake out of source macros

* Sun Jul 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-102.20200711git257f8b1
- New snapshot
- Copy game_controller_db.txt from sdl_gamecontrollerdb

* Mon Jun 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-101.20200620git297f91a
- Bump

* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.7.0-100.20200513git94e1635
- New snapshot
- Disable hardening
- Remove execstack

* Tue May 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.6.0-101.20200511git593d948
- Bump

* Thu Mar 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.6.0-100.20200229gitc43b511
- New snapshot

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-108.20200131git69ae598
- New snapshot

* Fri Dec 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-107.20191202git23174f3
- New snapshot
- PR to remove portaudio support, SDL2 do the work already
- Convert and resize icon to png

* Sun Nov 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-106.20191103git3c38087
- New snapshot

* Mon Oct 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-105.20191006gitafde59b
- New snapshot

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-104.20190917git6392f79
- New snapshot

* Sun Aug 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-103.20190818git33571dd
- New snapshot

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-102.20190517gitc6fcf0a
- New snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-101.20190502git079baae
- New snapshot

* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-100.20190411git163fd2b
- chinforpms
- New snapshot
- Make build on Fedora > 30
- Makefile to sanitize

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Sat Jul 28 2018 Sérgio Basto <sergio@serjux.com> - 1.4-10
- Try fix rfbz #4962
- Use the same SDL that wxGTK depends on (F27 SDL, F28 SDL2)

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun May 20 2018 Sérgio Basto <sergio@serjux.com> - 1.4-8
- Try fix f27 (#4775) use compat-wxGTK3-gtk2-devel
- Add BR xz-devel to dectect LibLZMA
- Remove manually-specified variables were not used by the project
- Add DISABLE_ADVANCE_SIMD=TRUE, recomended by upstream
- OpenGL_GL_PREFERENCE=GLVND to not use legacy OpenGL

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Sérgio Basto <sergio@serjux.com> - 1.4-6
- Rebuilt to fix core dump with wxWindow

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 1.4-5
- Rebuild for soundtouch 2.0.0
- Just enable compat-wxGTK3-gtk2, pcsx2 fails to detect wxGTK3
  therefore SDL2 also is disabled, intructions on
  https://github.com/PCSX2/pcsx2/wiki/Installing-on-Linux
- Enable GLSL_API and AVX
- Fix Perl builroot changes.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Sérgio Basto <sergio@serjux.com> - 1.4-2
- Add gcc6 patch

* Thu Feb 11 2016 Giles Birchley <gbirchley@blueyonder.co.uk> -1.4-1
- Build for new release 1.4
- Drop patch pcsx2-1.3.1_fedora_cflags_opts.diff - cflag options now streamlined upstream
- Add dependency for lzma-devel
- Add dependency for libICE-devel
- Remove dependency for Cg
- Remove dependency for libjpeg-turbo-devel
- Remove dependency for package glew-devel
- Add build option to retain WxWidget 2.8 -DWX28_API=TRUE
- Add build option -DGTK3_API=FALSE
- Add build option -DSDL2_API=FALSE
- Add build option -DDISABLE_ADVANCE_SIMD=TRUE
- For now, avoided specifying crosscompile (-DCMAKE_TOOLCHAIN_FILE=cmake/linux-compiler-i386-multilib.cmake) as not sure of rpmfusion guideline on this
- Binary name has been altered to PCSX2 upstream; renamed PCSX2.desktop.in, PCSX2.xpm and PCSX2.1
- Added new launcher script PCSX2-linux.sh

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.1-1
- Updated source to 1.2.1
- Updated patch1 permissions
- Source required modification to remove copyrighted files - added Source1

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.0-1
- Updated source to 1.2
- Updated patch1
- Source required modification to remove copyrighted files - added Source1

* Sat Jul 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-5
- made overlooked change suggested in rpmfusion review (#2455)
- changed requires from libGL-devel/libGLU-devel instead of mesa-libGL-devel

* Sun Jun 30 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-4
- made some minor changes suggested in rpmfusion review (#2455)
- removed backslash in cmake command
- removed pcsx2-1.1.0-fedora_cflags.diff
- replaced patch with pcsx2-1.1.0-fedora_cflags_opts.diff

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-3
- made some minor changes suggested in rpmfusion review (#2455)
- fix URL

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-2
- made some minor changes suggested in rpmfusion review (#2455):
- changed icon install permissions
- changed URL
- changed description line length
- reintroduced %%{version} macro to source0
- removed extra backslash from %%cmake
- changed line indentations so all are single space
- removed -DDOC_DIR from %%cmake
- removed extraneous remove lines

* Sun Jun 09 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-1
- changes following rpmfusion review (#2455).
- removed Group tag.
- updated source to v1.1 (linux fixes) 
- removed pcsx2-1.0.0_helpfile.diff (no longer needed).
- removed pcsx2-1.0.0_fedora_cmake.diff (Fedora<16 is no longer supported).
- removed pcsx2-1.1.0_fedora_gcc.diff as this patch is now applied in 1.1.0 source
- added Requires: hicolor-icon-theme (icons in %%{_datadir}/icons/hicolor/).
- added BuildRequires: libaio-devel (needed for 1.1.0).
- added warning about SSE2 to %%description.
- comment about 64 bit status shortened.
- version from names of docs removed (unversioned in 1.1.0).
- fixed omissions in pcsx2.xpm shebang (fix rpmlint error)
- Use %%{_docdir} instead of %%{_defaultdocdir}.
- removed some docs that were either misplaced or should not be packaged.
- removed specification of CMAKE_INSTALL_PREFIX and CMAKE_VERBOSE_MAKEFILE (%%cmake macro already sets them).
- moved %%find_lang macro to end of %%install.
- moved shell invocation to line following %%post %%postun (fix rpmlint error)

* Mon May 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-2
- further changes to comply with rpmfusion review (#2455):
- libGL-devel/libGLU-devel instead of mesa-libGL-devel
- Remove BuildRequires: libCg (redundant with Cg)
- Use %%{_prefix} instead of /usr for CMAKE install prefix
- add Gregory Hainaut's patch to fix issue with gcc 4.8, for Fedora 19 build
- Changed cmake option of DBUILD_REPLAY_LOADERS to false and changed %%files accrdingly

* Tue Mar 05 2013 Giles Birchley <gbirchey@blueyonder.co.uk>
- bleeding edge build, altered package name
- added pcsx2 as a conflict

* Mon Oct 15 2012 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-1
- Build of official 1.0.0 Release
- Significant modifications to script to comply with Fedora/RPMFusion packaging requirements
- Removed redundant BuildRequires
- Added upstream source
- Added Patch to make CFLAGS compliant
- Changed DCMAKE_BUILD_STRIP to FALSE to allow rpm debug package to be created
- Changed document destination in cmake by specifying DDOC_DIR=
- Changed language detection
- Changed icon and desktop file installation

* Tue Aug 09 2011 Danger Boy <Danger[dot] Boy [at]necac.tv.idl> - 0.9.8.4851-1
- initial build
