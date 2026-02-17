%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond clang 0
%if %{with clang}
%global toolchain clang
%endif

# Enable lto support
%bcond lto 1
%global _lto_cflags %{nil}
%if %{without lto}
%global _lto_cflags -fno-lto
%endif

%global with_extra_flags -O3 -Wp,-U_GLIBCXX_ASSERTIONS
%{?with_extra_flags:%global _pkg_extra_cflags %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?with_extra_flags}}
%{!?_hardened_build:%global _pkg_extra_ldflags -Wl,-z,now}

%bcond native 0
# Enable system ffmpeg
%bcond ffmpeg 1
%global bundleffmpegver 7.1.1
%bcond faudio 0
# Enable system flatbuffers
%bcond flatbuffers 1
%bcond glslang 1
%global bundleflatbuffers 23.5.26
# Enable system hidapi
%bcond hidapi 1
%global bundlehidapi 0.12.0
# Enable system llvm
%bcond llvm 1
%global bundlellvm 19.1.7
# Set to build with versioned LLVM packages
%dnl %global llvm_pkgver 16
# Enable system pugixml
%bcond pugixml 0
%global bundlepugixml 1.15.0
# Enable system rtmidi
%if 0%{?fedora} > 43
%bcond rtmidi 1
%endif
%global bundlertmidi 6.0.0
%bcond vma 1
%global bundlevma 3.3.0

# Enable system yaml-cpp (need -fexceptions support)
%bcond yamlcpp 0

%global commit b30a44c1367635af0675f61504e1ca45263655c6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20260215
%bcond snapshot 1

%global commit10 ee86beb30e4973f5feffe3ce63bfa4fbadf72f38
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 pugixml

%global commit11 3982730833b6daefe77dcfb32b5c282851640c17
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 soundtouch

%global commit12 416f7356967c1f66784dc1580fe157f9406d8bff
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 asmjit

%global commit13 fc9889c889561c5882e83819dcaffef5ed45529b
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 glslang

%global commit14 d6b2a974608dec3b76fb1e36c189f22b9cf3650c
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 hidapi

%global commit15 b077c81eb635392e694ccedbab8b644297ec0285
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 wolfssl

%global commit16 05c44fcd18074836e21e1eda9fc02b3a4a1529b5
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 yaml-cpp

%global commit17 008e03eac0ac1d5f85e16f5fcaefdda3fee75cb8
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 Fusion

%global commit18 cd89023f797900e4492da58b7bed36f702120011
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 llvm

%global commit19 c2a515bd34f37ba83c61474a04cd2bba57fde67e
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 ittapi

%global commit20 ec6367d3ba9d0d57b9d22d4b87da8144acaf428f
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 ffmpeg-core

%global commit21 edaa823d8b36a8656d7b2b9241b7d0bfe50af878
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 protobuf

%global commit22 1e5b49925aa60065db52de44c366d446a902547b
%global shortcommit22 %(c=%{commit22}; echo ${c:0:7})
%global srcname22 rtmidi

%global commit23 013ac3beddff3dbffafd5177e7972067cd2b5083
%global shortcommit23 %(c=%{commit23}; echo ${c:0:7})
%global srcname23 stb

%global commit24 1d8f600fd424278486eade7ed3e877c99f0846b1
%global shortcommit24 %(c=%{commit24}; echo ${c:0:7})
%global srcname24 VulkanMemoryAllocator

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/RPCS3
%global kg_url https://github.com/KhronosGroup

%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           rpcs3
Version:        0.0.39.18794
Release:        1%{?dist}
Summary:        PS3 emulator/debugger

License: %{shrink:
    GPL-2.0-only AND
    GPL-2.0-or-later AND
    LGPL-2.1-or-later AND
    MIT AND BSD-3-Clause AND
    GPL-3.0-or-later
}
URL:            https://rpcs3.net/

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
%if %{without pugixml}
Source10:       https://github.com/zeux/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%endif
Source11:       %{vc_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       %{vc_url}/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
%if %{without glslang}
Source13:       %{kg_url}/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%endif
%if %{without hidapi}
Source14:       https://github.com/libusb/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
%endif
Source15:       https://github.com/wolfSSL/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%if %{without yamlcpp}
Source16:       %{vc_url}/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
%endif
Source17:       https://github.com/xioTechnologies/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%if %{without llvm}
Source18:       https://github.com/llvm/llvm-project/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
%endif
Source19:       https://github.com/intel/%{srcname19}/archive/%{commit19}/%{srcname19}-%{shortcommit19}.tar.gz
%if %{without ffmpeg}
Source20:       %{vc_url}/%{srcname20}/archive/%{commit20}/%{srcname20}-%{shortcommit20}.tar.gz
Source200:      https://ffmpeg.org/releases/ffmpeg-%{bundleffmpegver}.tar.xz
Source201:      ffmpeg-linux_x86-64.sh
%endif
Source21:       https://github.com/protocolbuffers/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
%if %{without rtmidi}
Source22:       https://github.com/thestk/%{srcname22}/archive/%{commit22}/%{srcname22}-%{shortcommit22}.tar.gz
%endif
Source23:       https://github.com/nothings/%{srcname23}/archive/%{commit23}/%{srcname23}-%{shortcommit23}.tar.gz
%if %{without vma}
Source24:       https://github.com/Megamouse/%{srcname24}/archive/%{commit24}/%{srcname24}-%{shortcommit24}.tar.gz
%endif
Source99:       Makefile

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-Change-default-settings.patch
Patch12:        0001-Disable-auto-updater.patch
Patch13:        0001-Use-system-SDL_GameControllerDB.patch
Patch500:       0001-Disable-ffmpeg-download.patch

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang%{?llvm_pkgver}
BuildRequires:  llvm%{?llvm_pkgver}
BuildRequires:  lld%{?llvm_pkgver}
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  cmake(absl)
BuildRequires:  cmake(cubeb)
%if %{with faudio}
BuildRequires:  cmake(FAudio)
%endif
%if %{with llvm}
BuildRequires:  llvm%{?llvm_pkgver}-devel >= %{bundlellvm}
%else
Provides:       bundled(llvm) = %{bundlellvm}~git%{shortcommit18}
%endif
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gamemode)
%if %{with glslang}
BuildRequires:  cmake(glslang) >= 15.3.0
%else
Provides:       bundled(glslang) = git~0%{shortcommit13}
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew) >= 1.13.0
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec) >= %{bundleffmpegver}
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  ffmpeg-devel >= %{bundleffmpegver}
%else
BuildRequires:  make
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
Provides:       bundled(ffmpeg) = %{bundleffmpegver}
%endif
BuildRequires:  pkgconfig(libudev)
%if %{with hidapi}
BuildRequires:  pkgconfig(hidapi-hidraw) >= %{bundlehidapi}
%else
Provides:       bundled(hidapi) = %{bundlehidapi}~git%{shortcommit14}
%endif
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  cmake(miniupnpc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  cmake(OpenCV)
%if %{with pugixml}
BuildRequires:  pkgconfig(pugixml) >= %{bundlepugixml}
%else
Provides:       bundled(pugixml) = %{bundlepugixml}
%endif
%if %{with rtmidi}
BuildRequires:  pkgconfig(rtmidi) >= %{bundlertmidi}
%else
BuildRequires:  pkgconfig(alsa)
Provides:       bundled(rtmidi) = %{bundlertmidi}~git%{shortcommit22}
%endif
BuildRequires:  cmake(SDL3) >= 3.4.0
BuildRequires:  pkgconfig(tinfo)
BuildRequires:  cmake(VulkanHeaders) >= 1.3.240
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= %{bundlevma}
%else
Provides:       bundled(VulkanMemoryAllocator) = %{bundlevma}~git%{shortcommit24}
%endif
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(x11)
%if %{with yamlcpp}
BuildRequires:  cmake(yaml-cpp)
%else
Provides:       bundled(yaml-cpp) = 0~git%{shortcommit16}
%endif
BuildRequires:  pkgconfig(zlib)

BuildRequires:  cmake(Qt6Core) >= 6.8.0
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6MultimediaWidgets)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Requires:       libGL%{?_isa}
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(soundtouch) = 0~git%{shortcommit11}
Provides:       bundled(asmjit) = 0~git%{shortcommit12}
Provides:       bundled(Fusion) = 0~git%{shortcommit17}
Provides:       bundled(protobuf) = 0~git%{shortcommit21}
Provides:       bundled(stb) = 0~git%{shortcommit23}
Provides:       bundled(wolfssl) = 0~git%{shortcommit15}

%description
RPCS3 is a multi-platform open-source Sony PlayStation 3 emulator and debugger
written in C++.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -N -p1
%autopatch -M 499 -p1

pushd 3rdparty
rm -rf \
  7zip/7zip cubeb discord-rpc/*/ FAudio libsdl-org libusb \
  MoltenVK OpenAL/libs XAudio2Redist

tar -xf %{S:11} -C SoundTouch/soundtouch --strip-components 1
cp -p SoundTouch/soundtouch/COPYING.TXT LICENSE.soundtouch
tar -xf %{S:12} -C asmjit/asmjit --strip-components 1
cp -p asmjit/asmjit/LICENSE.md LICENSE.asmjit.md
%if %{without glslang}
tar -xf %{S:13} -C glslang/glslang --strip-components 1
cp -p glslang/glslang/LICENSE.txt LICENSE.glslang
%endif
%if %{without hidapi}
tar -xf %{S:14} -C 3rdparty/hidapi/hidapi --strip-components 1
cp -p hidapi/hidapi/LICENSE.txt LICENSE.hidapi
%endif
tar -xf %{S:15} -C wolfssl/wolfssl --strip-components 1
cp -p wolfssl/wolfssl/LICENSING LICENSE.wolfssl
tar -xf %{S:17} -C fusion/fusion --strip-components 1
cp -p fusion/fusion/LICENSE.md LICENSE.fusion.md
%if %{without rtmidi}
tar -xf %{S:22} -C rtmidi/rtmidi --strip-components 1
cp -p rtmidi/rtmidi/LICENSE LICENSE.rtmidi
%endif
tar -xf %{S:23} -C stblib/stb --strip-components 1
cp -p stblib/stb/LICENSE LICENSE.stb
%if %{without vma}
tar -xf %{S:24} -C 3rdparty/GPUOpen/VulkanMemoryAllocator --strip-components 1
cp -p GPUOpen/VulkanMemoryAllocator/LICENSE.txt LICENSE.vma
%endif

popd

%if %{without llvm}
tar -xf %{S:18} -C 3rdparty/llvm/llvm --strip-components 1

mkdir ittapi
tar -xf %{S:19} -C ittapi --strip-components 1
mkdir -p %{_vpath_builddir}/3rdparty/llvm_build
ln -s ../../../ittapi %{_vpath_builddir}/3rdparty/llvm_build/ittapi

sed -e 's|${GIT_EXECUTABLE}|true|g' \
  -i 3rdparty/llvm/llvm/llvm/lib/ExecutionEngine/IntelJITEvents/CMakeLists.txt

cp -p 3rdparty/llvm/llvm/LICENSE.TXT 3rdparty/LICENSE.llvm
%else
%if 0%{?llvm_pkgver}
sed \
  -e '/CMAKE_MODULE_PATH/alist(APPEND CMAKE_PREFIX_PATH "%{_libdir}/llvm%{?llvm_pkgver}/lib/cmake")' \
  -i CMakeLists.txt
%endif
%endif

%if %{without ffmpeg}
tar -xf %{S:20} -C 3rdparty/ffmpeg --strip-components 1
%patch -P 500 -p1
rm -rf 3rdparty/ffmpeg/include/*
rm -rf 3rdparty/ffmpeg/lib/*
cp -p 3rdparty/ffmpeg/copyright 3rdparty/copyright.ffmpeg
tar -xf %{S:200} -C 3rdparty/ffmpeg/include --strip-components 1
cp -p %{S:201} 3rdparty/ffmpeg/include/

sed -e '/target_link_libraries/s|INTERFACE|\0 va va-drm va-x11 X11|g' -i 3rdparty/ffmpeg/CMakeLists.txt
sed \
  -e '/^ARCH=/s|=.*|=%{_target_cpu}|g' \
  -e '/make install/d' \
  -i 3rdparty/ffmpeg/include/ffmpeg-linux_*.sh

%else
rm -rf 3rdparty/ffmpeg
%endif

%if %{with pugixml}
rm -rf 3rdparty/pugixml
%else
tar -xf %{S:10} -C 3rdparty/pugixml --strip-components 1
cp -p 3rdparty/pugixml/LICENSE.md 3rdparty/LICENSE.pugixml.md
%endif

tar -xf %{S:21} -C 3rdparty/protobuf/protobuf --strip-components 1
cp -p 3rdparty/protobuf/protobuf/LICENSE 3rdparty/LICENSE.protobuf

%if %{without yamlcpp}
tar -xf %{S:16} -C 3rdparty/yaml-cpp/yaml-cpp --strip-components 1
cp -p 3rdparty/yaml-cpp/yaml-cpp/LICENSE 3rdparty/LICENSE.yaml-cpp
sed -e 's|yaml-cpp_FOUND|yaml-cpp_DISABLED|g' -i 3rdparty/CMakeLists.txt
%else
rm -rf 3rdparty/yaml-cpp
%endif

sed \
  -e '/find_packages/s|Git|\0_DISABLED|g' \
  -e '/RPCS3_GIT_VERSION/s|local_build|%{sbuild}%{?with_snapshot:-%{shortcommit}}|g' \
  -e '/RPCS3_GIT_BRANCH/s|local_build|master|g' \
  -e '/RPCS3_GIT_FULL_BRANCH/s|local_build|local_build|g' \
  -i %{name}/git-version.cmake

sed \
  -e '/Examples\//d' \
  -e '/Python-C/d' \
  -i 3rdparty/fusion/fusion/CMakeLists.txt

sed -e 's|3rdparty/feralinteractive/feralinteractive/lib/||' -i rpcs3/gamemode_control.cpp

sed -e '/pkg_check_modules/s|2.3.3|2.3.0|' -i 3rdparty/miniupnp/CMakeLists.txt

sed -e 's| -Werror||g' -i 3rdparty/wolfssl/wolfssl/CMakeLists.txt

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' -i rpcs3/Input/sdl_pad_handler.cpp


%build
%if %{with clang}
export CC=clang%{?llvm_pkgver:-%{llvm_pkgver}}
export CXX=clang++%{?llvm_pkgver:-%{llvm_pkgver}}
export AR=llvm-ar%{?llvm_pkgver:-%{llvm_pkgver}}
export AS=llvm-as%{?llvm_pkgver:-%{llvm_pkgver}}
export NM=llvm-nm%{?llvm_pkgver:-%{llvm_pkgver}}
export RANLIB=llvm-ranlib%{?llvm_pkgver:-%{llvm_pkgver}}
%endif

%if %{without ffmpeg}
pushd 3rdparty/ffmpeg/include
sed \
  -e "/extra-cflags/s|-O3|$CFLAGS|g" \
  -i ffmpeg-linux_*.sh
chmod +x ffmpeg-linux_*.sh
%ifarch x86_64
./ffmpeg-linux_x86-64.sh
%endif
%make_build
make install
popd
mkdir -p %{_vpath_builddir}/external/ffmpeg/lib
mv 3rdparty/ffmpeg/include/linux/x86_64/lib/*.a %{_vpath_builddir}/3rdparty/ffmpeg/lib/
%endif

%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
%if %{without lto}
  -DUSE_LTO:BOOL=OFF \
%endif
%if 0%{with native}
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=ON \
%else
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=OFF \
%endif
  -DWITH_LLVM:BOOL=ON \
%if %{without llvm}
  -DBUILD_LLVM:BOOL=ON \
%endif
%if %{with faudio}
  -DUSE_SYSTEM_FAUDIO:BOOL=ON \
%else
  -DUSE_FAUDIO:BOOL=OFF \
%endif
  -DUSE_DISCORD_RPC:BOOL=OFF \
  -DUSE_SYSTEM_PROTOBUF:BOOL=OFF \
  -DUSE_SYSTEM_CUBEB:BOOL=ON \
  -DUSE_SYSTEM_CURL:BOOL=ON \
%if %{with ffmpeg}
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
%endif
%if %{with glslang}
  -DUSE_SYSTEM_GLSLANG:BOOL=ON \
%endif
%if %{with hidapi}
  -DUSE_SYSTEM_HIDAPI:BOOL=ON \
%endif
  -DUSE_SYSTEM_LIBPNG:BOOL=ON \
  -DUSE_SYSTEM_LIBUSB:BOOL=ON \
  -DUSE_SYSTEM_MINIUPNPC:BOOL=ON \
%if %{with pugixml}
  -DUSE_SYSTEM_PUGIXML:BOOL=ON \
%endif
  -DUSE_SYSTEM_OPENCV:BOOL=ON \
%if %{with rtmidi}
  -DUSE_SYSTEM_RTMIDI:BOOL=ON \
%endif
  -DUSE_SDL:BOOL=ON \
  -DUSE_SYSTEM_SDL:BOOL=ON \
%if %{with vma}
  -DUSE_SYSTEM_VULKAN_MEMORY_ALLOCATOR:BOOL=ON \
%endif
  -DUSE_SYSTEM_WOLFSSL:BOOL=OFF \
  -DUSE_SYSTEM_ZSTD:BOOL=ON \
  -DSPIRV_WERROR:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 ./%{_vpath_builddir}/bin/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -rp ./%{_vpath_builddir}/bin/{GuiConfigs,Icons} \
  %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category="Qt" \
  %{name}/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{48x48,scalable}/apps
install -pm0644 %{name}/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install -pm0644 %{name}/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{name}/%{name}.metainfo.xml \
  %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE 3rdparty/LICENSE.*
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Thu Jan 08 2026 Phantom X <megaphantomx at hotmail dot com> - 0.0.39.18620-1.20260107git1bfd115
- 0.0.39

* Sat Oct 11 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.38.18185-1.20251010git9e49b91
- 0.0.38

* Sun Jun 01 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.37.17989-1.20250601git70faef3
- 0.0.37

* Sat Apr 05 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.36.17745-1.20250404git613212f
- 0.0.36

* Sat Mar 01 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.35.17533-1.20250228gitb266e3d
- 0.0.35

* Sun Nov 10 2024 Phantom X <megaphantomx at hotmail dot com> - 0.0.34.17098-1.20241106git2262ac1
- 0.0.34

* Wed Sep 04 2024 Phantom X <megaphantomx at hotmail dot com> - 0.0.33.16889-1.20240903git23f9eb5
- 0.0.33.16889

* Sun May 05 2024 Phantom X <megaphantomx at hotmail dot com> - 0.0.32.16416-1.20240504git0fcb0b7
- 0.0.32.16416

* Wed Mar 06 2024 Phantom X <megaphantomx at hotmail dot com> - 0.0.31.16163-1.20240304gitef8afa7
- 0.0.31

* Thu Jan 04 2024 Phantom X <megaphantomx at hotmail dot com> - 0.0.30.15910-1.20240103git2369266
- 0.0.30

* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.29.15620-1.20230912gitf398f11
- Add llvm_pkgver define to set versioned LLVM packages, when needed

* Wed Aug 02 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.29.15426-1.20230802gitd34287b
- 0.0.29.15426
- Qt6

* Wed Jun 07 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.28.15143-1.20230606git6f834e9
- Add build number to %%{version}

* Fri Jun 02 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.28-1.20230602git33558d1
- 0.0.28

* Sat Apr 08 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.27-5.20230408gitf0e36c6
- System llvm is now supported, so use it

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.27-3.20230312gitcf5346c
- gcc 13 build fix

* Thu Mar 02 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.27-1.20230301git0178b20
- 0.0.27
- BR: miniupnpc

* Sat Jan 07 2023 Phantom X <megaphantomx at hotmail dot com> - 0.0.26-1.20230107gitdf718bc
- 0.0.26

* Thu Nov 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.25-1.20221101gita00f9e4
- 0.0.25

* Sat Sep 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.24-1.20220902git64579ee
- 0.0.24

* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.23-5.20220811git7ff4509
- Trying again

* Wed Aug 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.23-4.20220801gitc75b76d
- Revert to fix crashes

* Wed Aug 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.23-3.20220803git3e923b4
- Again

* Tue Aug 02 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.23-2.20220801gitc75b76d
- Bump
- BR: FAudio

* Sun Jul 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.23-1.20220702git969b9eb
- 0.0.23

* Wed Jun 22 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.22-5.20220622git661b485
- Update

* Sun Jun 12 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.22-4.20220612gitcb2c073
- Bump

* Wed Jun 08 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.22-3.20220608git64616f1
- Update

* Wed May 18 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.22-2.20220514git2ba437b
- Bump

* Tue May 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.22-1.20220503git0786a0a
- 0.0.22

* Mon Apr 25 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.21-4.20220425gite0d3a3b
- Bump
- Reenable system ffmpeg
- Build with bundled flatbluffers

* Mon Apr 11 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.21-3.20220410git3ed5a93
- Update

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.21-2.20220329git4a86638
- Bump
- Build with bundled ffmpeg

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.21-1.20220314gitf3a325f
- 0.0.21
- Fix build flags propagation

* Thu Feb 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.20-2.20220210gitd659703
- Bump

* Wed Feb 09 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.20-1.20220208gitd172b9a
- Initial spec
