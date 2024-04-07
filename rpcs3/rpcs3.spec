%global _lto_cflags -fno-lto
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond_with     clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%bcond_with     native
# Enable system ffmpeg
%bcond_without  sysffmpeg
%global bundleffmpegver 4.2.1
# Use smaller ffmpeg tarball, with binaries removed beforehand (use Makefile to download)
%bcond_without  smallffmpeg
# Enable system flatbuffers
%bcond_without  sysflatbuffers
%global bundleflatbuffers 23.5.26
# Enable system hidapi
%bcond_without  syshidapi
%global bundlehidapi 0.12.0
# Enable system llvm
%bcond_without  sysllvm
%global bundlellvm 16.0
# Set to build with versioned LLVM packages
%dnl %global llvm_pkgver 16
# Enable system rtmidi
%if 0%{?fedora} > 41
%bcond_without  sysrtmidi
%endif
%global bundlertmidi 6.0.0

# Enable system yaml-cpp (need -fexceptions support)
%bcond_with sysyamlcpp

%global commit 517f0e1bacbb6f5dd6fac5c70196fcc82832cf0a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240405
%bcond_without snapshot

%global commit10 360d469b9eac54d6c6e20f609f9ec35e3a5380ad
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 SPIRV-Tools

%global commit11 394e1f58b23dc80599214d2e9b6a5e0dfd0bbe07
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 soundtouch

%global commit12 416f7356967c1f66784dc1580fe157f9406d8bff
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 asmjit

%global commit13 36d08c0d940cf307a23928299ef52c7970d8cee6
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 glslang

%global commit14 8b43a97a9330f8b0035439ce9e255e4be202deca
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 hidapi

%global commit15 8970ff4c34034dbb3594943d11f8c9d4c5512bd5
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 wolfssl

%global commit16 456c68f452da09d8ca84b375faa2b1397713eaba
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 yaml-cpp

%global commit17 e867c06631767a2d96424cbec530f9ee5e78180f
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 SPIRV-Headers

%global commit18 cd89023f797900e4492da58b7bed36f702120011
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 llvm

%global commit19 c2a515bd34f37ba83c61474a04cd2bba57fde67e
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 ittapi

%global commit20 9a2df87789ebfecf64d35d732e5847662fbd5520
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 ffmpeg-core

%global commit21 0100f6a5779831fa7a651e4b67ef389a8752bd9b
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 flatbuffers

%global commit22 1e5b49925aa60065db52de44c366d446a902547b
%global shortcommit22 %(c=%{commit22}; echo ${c:0:7})
%global srcname22 rtmidi

%global stb_ver 2.27

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/RPCS3
%global kg_url https://github.com/KhronosGroup

%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           rpcs3
Version:        0.0.31.16295
Release:        1%{?dist}
Summary:        PS3 emulator/debugger

License:        GPL-2.0-only AND GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0
URL:            https://rpcs3.net/

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source10:       %{kg_url}/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       %{vc_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       %{vc_url}/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
Source13:       %{kg_url}/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%if %{without syshidapi}
Source14:       %{vc_url}/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
%endif
Source15:       https://github.com/wolfSSL/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%if %{without sysyamlcpp}
Source16:       %{vc_url}/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
%endif
Source17:       %{kg_url}/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%if %{without sysllvm}
Source18:       https://github.com/llvm/llvm-project/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
%endif
Source19:       https://github.com/intel/%{srcname19}/archive/%{commit19}/%{srcname19}-%{shortcommit19}.tar.gz
%if %{without sysffmpeg}
%if %{with smallffmpeg}
Source20:       %{srcname20}-nobin-%{shortcommit20}.tar.xz
%else
Source20:       %{vc_url}/%{srcname20}/archive/%{commit20}/%{srcname20}-%{shortcommit20}.tar.gz
%endif
%endif
%if %{without sysflatbuffers}
Source21:       https://github.com/google/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
%endif
%if %{without sysrtmidi}
Source22:       https://github.com/thestk/%{srcname22}/archive/%{commit22}/%{srcname22}-%{shortcommit22}.tar.gz
%endif
Source99:       Makefile

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-Change-default-settings.patch
Patch12:        0001-Disable-auto-updater.patch
Patch13:        0001-Use-system-SDL_GameControllerDB.patch

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang%{?llvm_pkgver}
BuildRequires:  llvm%{?llvm_pkgver}
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  cmake(cubeb)
BuildRequires:  cmake(FAudio)
%if %{with sysllvm}
BuildRequires:  llvm%{?llvm_pkgver}-devel >= %{bundlellvm}
%else
Provides:       bundled(llvm) = %{bundlellvm}~git%{shortcommit18}
%endif
%if %{with sysflatbuffers}
BuildRequires:  pkgconfig(flatbuffers) >= %{bundleflatbuffers}
BuildRequires:  flatbuffers-compiler >= %{bundleflatbuffers}
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew) >= 1.13.0
%if %{with sysffmpeg}
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
Provides:       bundled(ffmpeg) = %{bundleffmpegver}~git%{shortcommit20}
%endif
BuildRequires:  pkgconfig(libudev)
%if %{with syshidapi}
BuildRequires:  pkgconfig(hidapi-hidraw) >= %{bundlehidapi}
%else
Provides:       bundled(hidapi) = %{bundlehidapi}~git%{shortcommit14}
%endif
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  cmake(miniupnpc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(pugixml)
%if %{with sysrtmidi}
BuildRequires:  pkgconfig(rtmidi) >= %{bundlertmidi}
%else
BuildRequires:  pkgconfig(alsa)
Provides:       bundled(rtmidi) = %{bundlertmidi}~git%{shortcommit22}
%endif
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(tinfo)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(x11)
%if %{with sysyamlcpp}
BuildRequires:  cmake(yaml-cpp)
%else
Provides:       bundled(yaml-cpp) = 0~git%{shortcommit16}
%endif
BuildRequires:  pkgconfig(zlib)
BuildRequires:  cmake(VulkanHeaders) >= 1.3.240

BuildRequires:  cmake(Qt6Core) >= 6.4.0
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

Provides:       bundled(spirv-tools) = 0~git%{shortcommit10}
Provides:       bundled(soundtouch) = 0~git%{shortcommit11}
Provides:       bundled(asmjit) = 0~git%{shortcommit12}
Provides:       bundled(glslang) = 0~git%{shortcommit13}
Provides:       bundled(stb) = %{stb_ver}
Provides:       bundled(wolfssl) = 0~git%{shortcommit15}

%description
RPCS3 is a multi-platform open-source Sony PlayStation 3 emulator and debugger
written in C++.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -N -p1
%autopatch -M 499 -p1

pushd 3rdparty
rm -rf \
  7z/src cubeb discord-rpc/*/ FAudio libsdl-org libusb miniupnp \
  MoltenVK OpenAL/libs pugixml XAudio2Redist xxHash

tar -xf %{S:10} -C SPIRV/SPIRV-Tools --strip-components 1
tar -xf %{S:11} -C SoundTouch/soundtouch --strip-components 1
tar -xf %{S:12} -C asmjit/asmjit --strip-components 1
tar -xf %{S:13} -C glslang/glslang --strip-components 1
tar -xf %{S:15} -C wolfssl/wolfssl --strip-components 1
tar -xf %{S:17} -C SPIRV/SPIRV-Headers --strip-components 1

cp -p stblib/LICENSE LICENSE.stb
cp -p asmjit/asmjit/LICENSE.md LICENSE.asmjit.md
cp -p glslang/glslang/LICENSE.txt LICENSE.glslang
cp -p SoundTouch/soundtouch/COPYING.TXT LICENSE.soundtouch
cp -p SPIRV/SPIRV-Tools/LICENSE LICENSE.SPIRV-Tools
cp -p wolfssl/wolfssl/LICENSING LICENSE.wolfssl
popd

%if %{without sysllvm}
tar -xf %{S:18} -C 3rdparty/llvm/llvm --strip-components 1

mkdir ittapi
tar -xf %{S:19} -C ittapi --strip-components 1
mkdir -p %{__cmake_builddir}/3rdparty/llvm_build
ln -s ../../../ittapi %{__cmake_builddir}/3rdparty/llvm_build/ittapi

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

%if %{without sysffmpeg}
tar -xf %{S:20} -C 3rdparty/ffmpeg --strip-components 1

cp -p 3rdparty/ffmpeg/LICENSE.md 3rdparty/LICENSE.ffmpeg.md

sed -e 's|${FFMPEG_LIB_SWRESAMPLE}|\0 va va-drm va-x11|g' -i 3rdparty/CMakeLists.txt

pushd 3rdparty/ffmpeg
rm -rf linux/*/*
rm -rf macos/*/*
rm -rf windows/*/*

sed \
  -e '/^ARCH=/s|=.*|=%{_target_cpu}|g' \
  -e 's|disable-yasm|\0 --enable-vaapi --enable-hwaccel=h264_vaapi|g' \
  -e 's|disable-everything|\0 --disable-debug --disable-stripping|g' \
  -e '/make install/d' \
  -i linux_*.sh

popd
%else
rm -rf 3rdparty/ffmpeg
%endif

%if %{without syshidapi}
tar -xf %{S:14} -C 3rdparty/hidapi/hidapi --strip-components 1
cp -p 3rdparty/hidapi/hidapi/LICENSE.txt 3rdparty/LICENSE.hidapi
sed -e 's|hidapi_FOUND|hidapi_DISABLED|g' -i 3rdparty/CMakeLists.txt
%else
rm -rf 3rdparty/hidapi
%endif

%if %{without sysflatbuffers}
tar -xf %{S:21} -C 3rdparty/flatbuffers --strip-components 1
cp -p 3rdparty/flatbuffers/LICENSE.txt 3rdparty/LICENSE.flatbuffers
%else
rm -rf 3rdparty/flatbuffers
%endif

%if %{without sysyamlcpp}
tar -xf %{S:16} -C 3rdparty/yaml-cpp/yaml-cpp --strip-components 1
cp -p 3rdparty/yaml-cpp/yaml-cpp/LICENSE 3rdparty/LICENSE.yaml-cpp
sed -e 's|yaml-cpp_FOUND|yaml-cpp_DISABLED|g' -i 3rdparty/CMakeLists.txt
%else
rm -rf 3rdparty/yaml-cpp
%endif

%if %{without sysrtmidi}
tar -xf %{S:22} -C 3rdparty/rtmidi/rtmidi --strip-components 1
cp -p 3rdparty/rtmidi/rtmidi/LICENSE 3rdparty/LICENSE.rtmidi
sed -e 's|rtmidi_FOUND|rtmidi_DISABLED|g' -i 3rdparty/CMakeLists.txt
%else
rm -rf 3rdparty/rtmidi
%endif

sed \
  -e '/find_packages/s|Git|\0_DISABLED|g' \
  -e '/RPCS3_GIT_VERSION/s|local_build|%{sbuild}%{?with_snapshot:-%{shortcommit}}|g' \
  -e '/RPCS3_GIT_BRANCH/s|local_build|master|g' \
  -e '/RPCS3_GIT_FULL_BRANCH/s|local_build|local_build|g' \
  -i %{name}/git-version.cmake

sed -e 's| -Werror||g' -i 3rdparty/wolfssl/wolfssl/CMakeLists.txt

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' -i rpcs3/Input/sdl_pad_handler.cpp


%build
%set_build_flags

%if %{without sysffmpeg}
pushd 3rdparty/ffmpeg
sed \
  -e "/extra-cflags/s|-O3|$CFLAGS|g" \
  -i linux_*.sh
./linux_x86-64.sh
%make_build
make install
mv linux/x86_64/lib/*.a linux/x86_64/
popd
%endif

%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
%if 0%{with native}
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=ON \
%else
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=OFF \
%endif
  -DWITH_LLVM:BOOL=ON \
%if %{without sysllvm}
  -DBUILD_LLVM:BOOL=ON \
%endif
  -DUSE_SYSTEM_FAUDIO:BOOL=ON \
  -DUSE_DISCORD_RPC:BOOL=OFF \
%if %{with sysflatbuffers}
  -DUSE_SYSTEM_FLATBUFFERS:BOOL=ON \
%endif
  -DUSE_SYSTEM_CURL:BOOL=ON \
%if %{with sysffmpeg}
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
%endif
  -DUSE_SYSTEM_LIBPNG:BOOL=ON \
  -DUSE_SYSTEM_LIBUSB:BOOL=ON \
  -DUSE_SYSTEM_PUGIXML:BOOL=ON \
  -DUSE_SDL:BOOL=ON \
  -DUSE_SYSTEM_SDL:BOOL=ON \
  -DUSE_SYSTEM_XXHASH:BOOL=ON \
  -DSPIRV_WERROR:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 ./%{__cmake_builddir}/bin/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -rp ./%{__cmake_builddir}/bin/{git,GuiConfigs,Icons} \
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
