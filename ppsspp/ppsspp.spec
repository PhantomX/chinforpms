# https://github.com/hrydgard/ppsspp/issues/13312
%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond_without clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 3a41bd846f432b3aee9302992916a9b84c3dc7a7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250522
%bcond_without snapshot

# Enable Qt build
%bcond_with qt
# Enable EGL/GLESV2
%bcond_with egl

# Enable system ffmpeg
%bcond_with ffmpeg
%global bundleffmpegver 3.0.2
# Use smaller ffmpeg tarball, with binaries removed beforehand (use Makefile to download)
%bcond_without smallffmpeg
%bcond_with miniupnpc
%bcond_with local

%global commit1 9776332f720c854ef26f325a0cf9e32c02115a9c
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{name}-debugger

%global commit2 82049cca2e4c1516ed00a77b502a21f91b7843f4
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-ffmpeg

%global commit3 cbe88474ec196370161032a3863ec65050f70ba4
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 ffmpeg-gas-preprocessor

%global commit4 a8d71f0f279eb0d30ecf6af51473b66ae0cf8e8d
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 armips

%global commit5 fd4ffc1632db7b4e763bd28ffa6fc9d761cf3587
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 cpu_features

%global commit6 77551c429f86c0e077f26552b7c1c0f12a9f235e
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 glslang

%global commit7 4212eef67ed0ca048cb726a6767185504e7695e5
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 SPIRV-Cross

%global commit8 3f1c185ab414e764c694b8171d1c4d8c5c437517
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 filesystem

%global commit9 4697f97f3dd355ececf4066acd7a51e121a6bf1a
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 rcheevos

%global commit10 be392bf6949adeeabad5082aa79d12aacbda781f
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 OpenXR-SDK

%global commit11 27d13ca9beeb5541f5fbf11959dced03dac39972
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 miniupnp

%global commit12 f3271af11ab8591164b871e36520a7210964f3f6
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 ppsspp-lua

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%global vercommit %(c=%{commit}; echo ${c:0:10})
%endif

%global vc_url  https://github.com/hrydgard

%global jpgc_ver 1.05
%global vma_ver 3.3.0

%if %{with qt}
%global binname PPSSPPQt
%else
%global binname PPSSPPSDL
%endif

%global sver %%(echo %{version} | cut -d. -f-3)
%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           ppsspp
Version:        1.18.1.1976
Release:        100%{?dist}
Summary:        A PSP emulator
Epoch:          1

License:        BSD-3-Clause-Modification AND GPL-2.0-or-later AND Apache-2.0 AND MIT%{!?with_ffmpeg: AND GPL-3.0-or-later} AND WTFPL
URL:            http://www.ppsspp.org/

%if %{without snapshot}
Source0:        %{vc_url}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
%else
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        https://github.com/unknownbrackets/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%if %{without ffmpeg}
%if %{with smallffmpeg}
Source2:        %{srcname2}-nobin-%{shortcommit2}.tar.xz
%else
Source2:        %{vc_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
%endif
Source3:        https://github.com/FFmpeg/gas-preprocessor/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%endif
Source4:        https://github.com/Kingcom/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/google/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/KhronosGroup/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/KhronosGroup/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        https://github.com/Kingcom/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        https://github.com/RetroAchievements/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       https://github.com/KhronosGroup/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%if %{without miniupnpc}
Source11:       https://github.com/miniupnp/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%endif
Source12:       %{vc_url}/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
%endif
Source100:       %{name}.appdata.xml
Source101:       %{name}-qt.appdata.xml
Source102:       Makefile

Patch0:         0001-Disable-check-for-new-versions.patch
Patch2:         0001-Set-pulseaudio-application-name.patch
Patch3:         0001-Use-system-libraries.patch
Patch4:         0001-Use-system-vulkan-headers.patch
Patch5:         0001-tools-cmake-fixes.patch
Patch6:         0001-UI-tweak-some-font-scale-to-desktop-view.patch
%if %{with local}
Patch499:       0001-Local-changes.patch
%endif
Patch501:       0001-glslang-gcc-15-build-fix.patch

%if %{without ffmpeg}
ExclusiveArch:  %{ix86} x86_64 %{arm} %{mips32}
%endif
# https://github.com/hrydgard/ppsspp/issues/8823
ExcludeArch: %{power64}

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
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  ffmpeg-devel
%else
Provides:       bundled(ffmpeg) = %{bundleffmpegver}
%endif
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
%if %{with egl}
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
%else
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libglvnd)
%endif
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(libpng) >= 1.6
BuildRequires:  pkgconfig(libxxhash) >= 0.8.0
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(libzstd) >= 1.4.9
%if %{with miniupnpc}
BuildRequires:  pkgconfig(miniupnpc) >= 2.1
%else
Provides:       bundled(miniupnpc) = 0~git%{shortcommit11}
%endif
BuildRequires:  pkgconfig(RapidJSON)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(snappy)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers >= 1.3.236
%if %{with qt}
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5OpenGL)
%else
Requires:       (zenity or qarma or kdialog)
%endif

Requires:       vulkan-loader%{?_isa}
Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(armips) = 0~git%{shortcommit4}
Provides:       bundled(basisu_transcoder)
Provides:       bundled(cityhash)
Provides:       bundled(cpu_features) = 0~git%{shortcommit5}
Provides:       bundled(gason)
Provides:       bundled(glslang) = 0~git%{shortcommit6}
Provides:       bundled(jpeg-compressor) = %{jpgc_ver}
Provides:       bundled(libkirk)
Provides:       bundled(rcheevos) = 0~git%{shortcommit9}
Provides:       bundled(sfmt19937)
Provides:       bundled(sha1-reichl)
Provides:       bundled(spirv-cross) = 0~git%{shortcommit7}
Provides:       bundled(vma) = %{vma_ver}
Provides:       bundled(xbrz)

Provides:       %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs < %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       %{name}-qt = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-qt < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-sdl = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-sdl < %{?epoch:%{epoch}:}%{version}-%{release}


%description
PPSSPP is a PSP emulator written in C++. It translates PSP CPU instructions
directly into optimized x86, x64, ARM or ARM64 machine code, using JIT
recompilers (dynarecs).


%package        data
Summary:        Data files of %{name}
BuildArch:      noarch
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       google-roboto-condensed-fonts
Requires:       sdl_gamecontrollerdb

%description data
Data files of %{name}.


%package        tools
Summary:        Additional tools files for %{name}

%description tools
Additional tools files for %{name}.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -N -p1
%autopatch -M 500 -p1

%if %{with snapshot}
tar -xf %{SOURCE1} -C assets/debugger --strip-components 1
%if %{without ffmpeg}
tar -xf %{SOURCE2} -C ffmpeg --strip-components 1
tar -xf %{SOURCE3} -C ffmpeg/gas-preprocessor --strip-components 1
%endif
tar -xf %{SOURCE4} -C ext/armips --strip-components 1
tar -xf %{SOURCE5} -C ext/cpu_features --strip-components 1
tar -xf %{SOURCE6} -C ext/glslang --strip-components 1
%patch -P 501 -p1
tar -xf %{SOURCE7} -C ext/SPIRV-Cross --strip-components 1
tar -xf %{SOURCE8} -C ext/armips/ext/filesystem --strip-components 1
tar -xf %{SOURCE9} -C ext/rcheevos --strip-components 1
tar -xf %{SOURCE10} -C ext/OpenXR-SDK --strip-components 1
tar -xf %{SOURCE12} -C ext/lua --strip-components 1
%endif

rm -rf ext/glew/GL
rm -rf ext/{glew,rapidjson,snappy}/*.{c,cpp,h}
rm -rf ext/{discord-rpc,libchr,libpng,libzip,openxr/{android,stub},vulkan,zlib,zstd}*
rm -f ext/xxhash.*
rm -rf MoltenVK/*

find ext Core -type f \( -name '*.c*' -o -name '*.h*' -o -name '*.y' \) -exec chmod -x {} ';'

%if %{with ffmpeg}
rm -rf ffmpeg
%else
cp -p ffmpeg/LICENSE.md ext/LICENSE.ffmpeg.md
%endif
pushd ext
cp -p armips/LICENSE.txt LICENSE.armips
cp -p cityhash/COPYING COPYING.cityhash
cp -p cpu_features/LICENSE LICENSE.cpu_features
cp -p gason/LICENSE LICENSE.gason
cp -p glslang/LICENSE.txt LICENSE.glslang
cp -p rcheevos/LICENSE LICENSE.rcheevos
cp -p SPIRV-Cross/LICENSE LICENSE.SPIRV-Cross
cp -p udis86/LICENSE LICENSE.udis86
cp -p OpenXR-SDK/LICENSE LICENSE.OpenXR-SDK
cp -p portable-file-dialogs/COPYING COPYING.pfd
popd

%if %{with miniupnpc}
rm -rf ext/miniupnp
%else
tar -xf %{SOURCE11} -C ext/miniupnp --strip-components 1
cp ext/miniupnp/LICENSE ext/LICENSE.miniupnp
%endif

sed -i \
%if %{with snapshot}
  -e '/set(GIT_VERSION\b /s|".*"|"v%{sver}-%{sbuild}-g%{vercommit}"|g' \
%else
  -e '/set(GIT_VERSION\b /s|".*"|"v%{sver}"|g' \
%endif
  -e '/find_package/s|Git|\0_disabled|g' \
  -i git-version.cmake

sed \
  -e 's|"unknown"|"%{shortcommit7}"|' \
  -e 's| unknown | %{shortcommit7} |' \
  -e 's|GIT_FOUND|GIT_FOUND_DISABLED|g' \
  -i ext/SPIRV-Cross/CMakeLists.txt

sed \
  -e '/Wno-deprecated-register/d' \
  -e '/Wno-tautological-pointer-compare/d' \
  -i CMakeLists.txt

sed \
  -e 's| -O2 | |g' \
  -i CMakeLists.txt

sed \
  -e 's|"-O2"|""|g' \
  -i CMakeLists.txt

sed \
  -e 's| -O3 | |g' \
  -i ext/armips/ext/tinyformat/Makefile

%if %{without ffmpeg}
pushd ffmpeg
sed \
  -e '/^ARCH=/s|=.*|=%{_target_cpu}|g' \
  -e '/--extra-cflags/i\    --cc="${CC:-gcc}" \\' \
  -e 's|disable-everything|\0 --disable-debug --disable-stripping|g' \
  -e '/make install/d' \
  -i linux_*.sh

sed -e "s|_cflags_speed='.*'|_cflags_speed=''|g" -i configure

rm -rf */*/include
rm -rf */*/lib
rm -rf wiiu

popd
%endif

sed \
  -e "s|_RPM_LIBCOMMON_|$(pwd)/%{_vpath_builddir}/lib/libCommon.a|g" \
  -i ext/native/tools/CMakeLists.txt


%build
pushd ext/native/tools
%cmake \
  -G Ninja \
%{nil}

popd

%if %{without ffmpeg}
pushd ffmpeg
sed \
  -e "/extra-cflags/s|-O3|$CFLAGS|g" \
  -i linux_*.sh
%ifarch x86_64
./linux_x86-64.sh
%endif
%ifarch %{ix86}
./linux_x86.sh
%endif
%ifarch %{arm}
./linux_arm.sh
%endif
%ifarch %{mips32}
./linux_mips32.sh
%endif
%make_build
make install
popd
%endif

%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
%if %{with egl}
  -DUSING_EGL:BOOL=ON \
  -DUSING_GLES2:BOOL=ON \
%endif
  -DOpenGL_GL_PREFERENCE=GLVND \
%if %{with ffmpeg}
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
%endif
  -DUSE_SYSTEM_LIBPNG:BOOL=ON \
  -DUSE_SYSTEM_LIBZIP:BOOL=ON \
%if %{with miniupnpc}
  -DUSE_SYSTEM_MINIUPNPC:BOOL=ON \
%endif
  -DUSE_SYSTEM_LIBSDL2:BOOL=ON \
  -DUSE_SYSTEM_SNAPPY:BOOL=ON \
  -DUSE_SYSTEM_ZSTD:BOOL=ON \
  -DUSE_DISCORD:BOOL=OFF \
  -DUSE_WAYLAND_WSI:BOOL=ON \
  -DUSING_X11_VULKAN:BOOL=ON \
  -DENABLE_HLSL:BOOL=OFF \
  -DENABLE_GLSLANG_BINARIES:BOOL=OFF \
%ifarch %{ix86}
  -DX86:BOOL=ON \
%endif
%ifarch %{arm} aarch64
  -DARM:BOOL=ON \
%endif
%ifarch armv7l armv7hl armv7hnl
  -DARMV7:BOOL=ON \
%endif
%ifarch x86_64
  -DX86_64:BOOL=ON \
%endif
  -DBUILD_TESTING:BOOL=OFF \
  -DHEADLESS:BOOL=OFF \
%if %{with qt}
  -DUSING_QT_UI:BOOL=ON \
%endif
%{nil}

%cmake_build

pushd ext/native/tools
%cmake_build
popd


%install
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}

install -pm0755 ext/native/tools/%{_vpath_builddir}/build/{atlastool,zimtool} \
  %{buildroot}%{_bindir}/

rm -f %{buildroot}%{_datadir}/%{name}/assets/gamecontrollerdb.txt
ln -sf ../../SDL_GameControllerDB/gamecontrollerdb.txt \
  %{buildroot}%{_datadir}/%{name}/assets/gamecontrollerdb.txt

rm -f %{buildroot}%{_datadir}/%{name}/assets/Roboto-Condensed.ttf
ln -sf ../../fonts/google-roboto/RobotoCondensed-Regular.ttf \
  %{buildroot}%{_datadir}/%{name}/assets/Roboto-Condensed.ttf

%if %{with qt}
  install -pm 644 Qt/languages/*.ts %{buildroot}%{_datadir}/%{name}/assets/lang/
%endif

desktop-file-edit \
%if %{with qt}
  --set-name="PPSSPP (Qt)" \
%else
  --set-name="PPSSPP (SDL)" \
%endif
  --set-key="Exec" \
  --set-value="%{binname}" \
  --set-key="StartupNotify" \
  --set-value="false" \
  --set-key="StartupWMClass" \
  --set-value="%{binname}" \
  --remove-key="MimeType" \
  %{buildroot}%{_datadir}/applications/%{binname}.desktop

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 \
%if %{with qt}
  %{S:101} \
%else
  %{S:100} \
%endif
  %{buildroot}%{_metainfodir}/%{binname}.appdata.xml


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/%{binname}.appdata.xml


%files
%license LICENSE.TXT ext/{COPYING,LICENSE}.*
%doc README.md
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop
%{_metainfodir}/%{binname}.appdata.xml


%files data
%doc README.md
%license LICENSE.TXT
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml


%files tools
%doc ext/native/tools/README.txt
%license LICENSE.TXT
%{_bindir}/atlastool
%{_bindir}/zimtool


%changelog
* Fri May 23 2025 Phantom X <megaphantomx at hotmail dot com> - 1:1.18.1.1976-100.20250522git3a41bd8
- Use official binary names

* Wed Nov 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1:1.18.1-100.20241106git2891f63
- 1.18.1

* Tue Feb 13 2024 Phantom X <megaphantomx at hotmail dot com> - 1:1.17.1-100.20240212gitf3635c4
- 1.17.1

* Mon Jan 29 2024 Phantom X <megaphantomx at hotmail dot com> - 1:1.17-100.20240128git9401fab
- 1.17

* Sat Oct 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.16.6-100.20231013git1e6142d
- 1.16.6

* Thu Sep 28 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.16.5-100
- 1.16.5

* Sun Sep 24 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.16.3-100.20230923gitc4ad324
- 1.16.3

* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.16.1-100.20230916gitb6515ef
- 1.16.1

* Sun Sep 10 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.16.0-100.20230909gitd4365c6
- 1.16.0

* Fri May 26 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.15.4-100.20230525gitf291959
- 1.15.4

* Sun May 07 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.15.3-100.20230507git97ea555
- 1.15.3

* Wed May 03 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.15.1-100.20230503git03bf19c
- 1.15.1

* Tue Mar 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.14.4-104.20230314gitc31b4be
- Patch to change font scaling
- R: sdl_gamecontrollerdb

* Tue Jan 03 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.14.4-100
- 1.14.4

* Sun Dec 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.14-100
- 1.14

* Sun Nov 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.13.2-103.20221120git5efa2e2
- %%cmake_install

* Sun Sep 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.13.2-100.20220911gita6c9546
- 1.13.2

* Sat Aug 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.13.1-100.20220820gitad59fe0
- 1.13.1

* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.13-100.20220727gitad59fe0
- 1.13

* Sun Jul 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-115.20220628git4196928
- Bump

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-114.20220617git31aca54
- Bump

* Sun May 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-113.20220522git017f71a
- Update

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-112.20220426gitcf9c3e8
- Bump

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-111.20220324git6f04f52
- Last snapshot

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-110.20220313git97bc7a1
- Bump

* Mon Feb 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-109.20220224git3bfab63
- Bump

* Sat Jan 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-108.20220121git54d63cc
- Update

* Sun Jan 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-107.20220109git2d7a7fd
- Last snapshot

* Wed Dec 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-106.20211221gitcc76762
- Bump

* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-105.20211208git3e5ba24
- Update
- Add tools package

* Sat Dec 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-104.20211204git4b5d703
- Bump

* Thu Dec 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-103.20211202git676ed6c
- Last snapshot

* Tue Nov 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-102.20211123gitc7bba9b
- Update

* Sun Nov 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-101.20211107git4d38905
- Bump

* Thu Oct 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.3-100.20211026git030bfb1
- 1.12.3

* Tue Oct 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.12.2-100.20211011gitbb64c17
- 1.12.2

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-120.20211001git5ccbe12
- Last snapshot
- Added debugger tarball

* Sat Sep 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-119.20210918gitd944c25
- Last snapshot

* Thu Aug 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-118.20210825git714578a
- Last snapshot

* Wed Aug 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-117.20210811git5de47c6
- Update

* Thu Jul 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-116.20210722git868f5f6
- Bump
- Remove lang submodules, now in mainline

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-115.20210712git11957dd
- Update

* Wed Jul 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-114.20210707git752fdc9
- Last snapshot

* Wed Jun 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-113.20210622git8e9b012
- Update

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-112.20210610git39f4790
- Bump

* Sat May 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-111.20210528gitecc2f62
- Bump

* Tue May 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-110.20210517gitbac74b4
- Last snapshot
- Remove CHD patch

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-109.20210512gite725edd
- Update

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-108.20210501git630f071
- Bump

* Sat Apr 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-107.20210424gitfd2ff87
- Update

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-106.20210419gitbbdb4f7
- Last snapshot

* Sun Apr 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-105.20210417git036efc2
- Bump
- Added libzstd to system libraries patch
- BR: libzstd

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-104.20210407git28065c1
- Update

* Wed Mar 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-103.20210323gita37ea1e
- Add experimental CHD support from SleepyMan

* Mon Mar 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-102.20210308git1cfaa9f
- Bump to fix custom textures crashes

* Fri Mar 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-101.20210305git71707b5
- Bump to remove revert

* Wed Mar 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-100.20210303gitbd87a76
- 1.11.3

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.2-100.20210228git0fb655a
- 1.11.2

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.1-100.20210211gitd1c4b86
- 1.11.1

* Sat Jan 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-118.20210130gitc84ddaa
- New snapshot

* Thu Jan 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-117.20210106git1ee7faa
- Bump

* Wed Dec 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-116.20201223gitb403853
- Update

* Tue Dec 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-115.20201214gitafaff2e
- New snapshot

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-114.20201125git6e2447d
- Bump

* Sun Nov 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-113.20201115gite1f56b1
- Update

* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-112.20201110git0510101
- Bump

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-111.20201030gitf3c05cb
- New snapshot

* Sat Oct 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-110.20201023git254c316
- Update

* Mon Oct 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-109.20201011git615e07f
- Bump

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-108.20201002git5c9b7bb
- New snapshot

* Sat Sep 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-107.20200919git7ed1ade
- Bump

* Tue Sep 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-106.20200914git68735b4
- New snapshot

* Mon Sep 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-105.20200907gitfcaef64
- Bump

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-104.20200905git5f1e3b2
- New snapshot

* Sat Aug 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-103.20200828gitcb3ed8f
- Bump
- BR: libxxhash

* Tue Aug 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-102.20200825git3574a35
- New snapshot

* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-101.20200805git937042b
- Bump
- BR: vulkan-headers

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-100.20200726git2af805d
- 1.10.3
- BR: miniupnc
- Enable system snappy for real

* Sun Jul 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.2-100.20200710gite667421
- 1.10.2

* Sat Jun 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.0-100.20200627git401df20
- 1.10.0

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.4-110.20200620gitb879b43
- New snapshot

* Sun Jun 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-109.20200607gitba06c87
- Bump

* Sun May 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-108.20200517gitfdd0b37
- New snapshot

* Wed Apr 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-107.20200421git134c9cf
- Bump

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-106.20200220git7d13d2e
- New snapshot

* Tue Feb 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-105.20200225git4602f89
- Bump

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-104.20200127gita9302c4
- New snapshot

* Sun Jan 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-103.20200105git6d8ddb7
- New snapshot

* Wed Dec 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-102.20191217git608d716
- New snapshot

* Mon Nov 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-101.20191118git1439421
- New snapshot

* Fri Oct 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-100.201901025git86de0a4
- New snapshot

* Fri Sep 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.2-100.20190927git9e7625c
- New snapshot

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-109.20190919git5a53570
- New snapshot

* Sun Sep 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-108.20190904git2439c3e
- New snapshot

* Sat Aug 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-107.20190824git0889013
- New snapshot

* Thu Aug 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-106.20190815git3356f94
- New snapshot

* Sat Jul 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-105.20190718git37a97e7
- New snapshot

* Thu Jun 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-104.20190618git53e8263
- New snapshot

* Sun Jun 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-103.20190602git816abce
- New snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-102.20190502git709c9dc
- New snapshot

* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-101.20190410git54e102c
- New snapshot

* Mon Mar 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-100.20190318gitb004852
- New snapshot

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.5-4.20190302git7c7d276
- New snapshot

* Thu Feb 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.7.5-3.20190207gitbff58d0
- New snapshot

* Wed Jan 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.7.5-2.20190102git12e54ba
- New snapshot

* Mon Dec 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.5-1.20181210gitb282d83
- New snapshot
- Borrow some from RPMFusion
- Split data package

* Sat Nov 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.2-1.20181113git04708fe
- New snapshot
- USE_DISCORD=OFF

* Sat Oct 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-6.20181027gitcaa506b
- New snapshot

* Tue Oct 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-5.20181009git3189385
- New snapshot
- Provides ppsspp-data to not crash with RPMFusion package

* Sat Sep 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-4.20180907gitfd6c314
- New snapshot
- Dropped unneeded GL wrapper. Mesa 8.2 sets proper compat now.

* Fri Aug 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-3.20180515gitec5b0c2
- New snapshot

* Tue Jul 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-2.20180717git9be6b22
- New snapshot

* Fri Jun 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-1.20180620git06340bf
- New snapshot, 1.6.3

* Thu May 31 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.2-1.20180531gitcae79bf
- New snapshot, 1.6.2
- BR: glew
- BR: wayland-devel
- Set default OpenGL provider to libglvnd

* Sat May 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-5.20180510gitd10d57b
- New snapshot
- Appdata

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-4.20180414gitfb377b0
- New snapshot

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-3.20180406gitca0fb77
- New snapshot

* Sat Mar 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-2.20180308git0ed3dea
- New snapshot

* Wed Mar 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-1.20180305git90dbd9a
- New snapshot
- BR: gcc-c++
- Remove obsolete scriptlets

* Sun Feb 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.4-14.20180211git4e5fb6e
- New snapshot
- USE_SYSTEM_LIBZIP

* Mon Jan 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.4-13.20180108git6224260
- New snapshot

* Thu Dec 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-12.20171214gitc55847a
- New snapshot

* Tue Nov 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-11.20171107gitca3be18
- New snapshot

* Fri Oct 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-10.20171013gited602a3
- New snapshot

* Sat Sep 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-9.20170825gitd36fdd6
- New snapshot

* Sun Aug 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-8.20170825git4938ab7
- New snapshot

* Thu Jul 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-7.20170727gitf8213a9
- New snapshot

* Sat Jul 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-6.20170613gita9f70d1
- New snapshot

* Fri Jun 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-5.20170613git3249d81
- New snapshot

* Tue Jun 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-4.20170613gitdd23588
- New snapshot
- R: google-roboto-condensed-fonts

* Fri May 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-3.20170519git66dc0ea
- New snapshot

* Sat Apr 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-2.20170422git2c6161c
- New snapshot

* Sun Apr 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1.20170402git4ea01be
- New snapshot

* Sat Mar 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-7.20170318git24cfb73
- New snapshot

* Mon Mar 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-6.20170306git9f17c7f
- New snapshot
- Fix forgotten GIT_VERSION

* Sun Mar 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-5.20170305git042d09a
- New snapshot
- Update GIT_VERSION again

* Fri Feb 03 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-4.20170203git48934df
- New snapshot
- Build proper ffmpeg static libraries instead using distributed binary ones
- Set ExclusiveArch if building with bundled ffmpeg

* Sat Jan 28 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-3.20170128git14d2bf5
- New snapshot
- Fix assets/gamecontrollerdb.txt loading
- Better GIT_VERSION display
- Wrapper to export Mesa GL to 3.3COMPAT

* Thu Dec 29 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.3-2.20161227gitad04f97
- Option to build with ugly bundled ffmpeg binary.
- https://github.com/hrydgard/ppsspp/issues/9026
- System png.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
