%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

# Enable system ffmpeg
%global with_sysffmpeg 1
%global bundleffmpegver 4.2.1
# Use smaller ffmpeg tarball, with binaries removed beforehand (use Makefile to download)
%global with_smallffmpeg 1
# Enable system flatbuffers
%global with_sysflatbuffers 0
%global bundleflatbuffers 2.0.6

%global commit e0d3a3b0ed6b42351dfe610d3ad97ef2dac96196
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220425
%global with_snapshot 1

%global commit10 895927bd3f2d653f40cebab55aa6c7eabde30a86
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 SPIRV-Tools

%global commit11 83cfba67b6af80bb9bfafc0b324718c4841f2991
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 soundtouch

%global commit12 fc2a5d82f7434d7d03161275a764c051f970f41c
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 asmjit

%global commit13 9bb8cfffb0eed010e07132282c41d73064a7a609
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 glslang

%global commit14 6cf133697c4413dc9ae0fefefeba5f33587dff76
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 hidapi

%global commit15 dcaa218ed891a13d57e435b19fbbd1f6ae2d4868
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 wolfssl

%global commit16 0b67821f307e8c6bf0eba9b6d3250e3cf1441450
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 yaml-cpp

%global commit17 3fdabd0da2932c276b25b9b4a988ba134eba1aa6
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 SPIRV-Headers

%global commit18 509d31ad89676522f7121b3bb8688f7d29b7ee60
%global shortcommit18 %(c=%{commit17}; echo ${c:0:7})
%global srcname18 llvm

%global commit19 c2a515bd34f37ba83c61474a04cd2bba57fde67e
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 ittapi

%global commit20 bf019f8c88bc64638fccef62840e935ab2689a4a
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 ffmpeg-core

%global commit21 615616cb5549a34bdf288c04bc1b94bd7a65c396
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 flatbuffers

%bcond_with     clang
%bcond_with     native
# Fail with system llvm
%bcond_without  llvm_submod

%if %{with clang}
%global toolchain clang
%endif

%global stb_ver 2.27

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/RPCS3
%global kg_url https://github.com/KhronosGroup

Name:           rpcs3
Version:        0.0.21
Release:        4%{?gver}%{?dist}
Summary:        PS3 emulator/debugger

License:        GPLv2
URL:            https://rpcs3.net/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source10:       %{kg_url}/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       %{vc_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       %{vc_url}/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
Source13:       %{kg_url}/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
Source14:       %{vc_url}/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
Source15:       https://github.com/wolfSSL/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
Source16:       %{vc_url}/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
Source17:       %{kg_url}/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%if %{with llvm_submod}
Source18:       %{vc_url}/llvm-mirror/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
%endif
Source19:       https://github.com/intel/%{srcname19}/archive/%{commit19}/%{srcname19}-%{shortcommit19}.tar.gz
%if !0%{?with_sysffmpeg}
%if 0%{?with_smallffmpeg}
Source20:       %{srcname20}-nobin-%{shortcommit20}.tar.xz
%else
Source20:       %{vc_url}/%{srcname20}/archive/%{commit20}/%{srcname20}-%{shortcommit20}.tar.gz
%endif
%endif
%if !0%{?with_sysflatbuffers}
Source21:       https://github.com/google/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
%endif
Source99:       Makefile

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-Change-default-settings.patch


ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
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
BuildRequires:  cmake(cubeb)
%if !%{with llvm_submod}
BuildRequires:  cmake(LLVM)
%endif
%if 0%{?with_sysflatbuffers}
BuildRequires:  pkgconfig(flatbuffers) >= %{bundleflatbuffers}
%else
Provides:       bundled(flatbuffers) = %{bundleflatbuffers}
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew) >= 1.13.0
%if 0%{?with_sysffmpeg}
BuildRequires:  pkgconfig(libavcodec) >= %{bundleffmpegver}
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires:  ffmpeg-devel >= %{bundleffmpegver}
%endif
%else
BuildRequires:  make
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
Provides:       bundled(ffmpeg) = %{bundleffmpegver}
%endif
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(pugixml)
BuildRequires:  pkgconfig(tinfo)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers >= 1.2.198

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5MultimediaWidgets)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info

Requires:       vulkan-loader%{?_isa}

Provides:       bundled(spirv-tools) = 0~git%{shortcommit10}
Provides:       bundled(soundtouch) = 0~git%{shortcommit11}
Provides:       bundled(asmjit) = 0~git%{shortcommit12}
Provides:       bundled(glslang) = 0~git%{shortcommit13}
Provides:       bundled(hidapi) = 0~git%{shortcommit14}
Provides:       bundled(stb) = %{stb_ver}
Provides:       bundled(wolfssl) = 0~git%{shortcommit15}
Provides:       bundled(yaml-cpp) = 0~git%{shortcommit16}
%if %{with llvm_submod}
Provides:       bundled(llvm) = 0~git%{shortcommit18}
%endif

%description
RPCS3 is a multi-platform open-source Sony PlayStation 3 emulator and debugger
written in C++.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

tar -xf %{S:10} -C 3rdparty/SPIRV/SPIRV-Tools --strip-components 1
tar -xf %{S:11} -C 3rdparty/SoundTouch/soundtouch --strip-components 1
tar -xf %{S:12} -C 3rdparty/asmjit/asmjit --strip-components 1
tar -xf %{S:13} -C 3rdparty/glslang/glslang --strip-components 1
tar -xf %{S:14} -C 3rdparty/hidapi/hidapi --strip-components 1
tar -xf %{S:15} -C 3rdparty/wolfssl/wolfssl --strip-components 1
tar -xf %{S:16} -C 3rdparty/yaml-cpp/yaml-cpp --strip-components 1
tar -xf %{S:17} -C 3rdparty/SPIRV/SPIRV-Headers --strip-components 1
%if %{with llvm_submod}
tar -xf %{S:18} -C llvm --strip-components 1

mkdir ittapi
tar -xf %{S:19} -C ittapi --strip-components 1
mkdir -p %{__cmake_builddir}/3rdparty/llvm_build
ln -s ../../../ittapi %{__cmake_builddir}/3rdparty/llvm_build/ittapi

sed -e 's|${GIT_EXECUTABLE}|true|g' \
  -i llvm/lib/ExecutionEngine/IntelJITEvents/CMakeLists.txt

cp -p llvm/LICENSE.TXT 3rdparty/LICENSE.llvm
%endif
%if !0%{?with_sysffmpeg}
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
%endif
%if !0%{?with_sysflatbuffers}
tar -xf %{S:21} -C 3rdparty/flatbuffers --strip-components 1
cp -p 3rdparty/flatbuffers/LICENSE.txt 3rdparty/LICENSE.flatbuffers
%endif

pushd 3rdparty
cp -p stblib/LICENSE LICENSE.stb
cp -p asmjit/asmjit/LICENSE.md LICENSE.asmjit.md
cp -p glslang/glslang/LICENSE.txt LICENSE.glslang
cp -p hidapi/hidapi/LICENSE.txt LICENSE.hidapi
cp -p SoundTouch/soundtouch/COPYING.TXT LICENSE.soundtouch
cp -p SPIRV/SPIRV-Tools/LICENSE LICENSE.SPIRV-Tools
cp -p wolfssl/wolfssl/LICENSING LICENSE.wolfssl
cp -p yaml-cpp/yaml-cpp/LICENSE LICENSE.yaml-cpp
popd

%if 0%{?with_snapshot}
  sed \
    -e '/find_packages/s|Git|\0_DISABLED|g' \
    -e '/RPCS3_GIT_VERSION/s|local_build|%{shortcommit}|g' \
    -e '/RPCS3_GIT_BRANCH/s|local_build|master|g' \
    -e '/RPCS3_GIT_FULL_BRANCH/s|local_build|local_build|g' \
    -i %{name}/git-version.cmake
%endif

# This resets RPM flags
sed \
  -e '/CMAKE_CXX_FLAGS/d' \
  -e '/CMAKE_C_FLAGS/d' \
  -i CMakeLists.txt


%build
%set_build_flags

%if !0%{?with_sysffmpeg}
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
%if %{with clang}
  -DCMAKE_C_COMPILER=%{_bindir}/clang \
  -DCMAKE_CXX_COMPILER=%{_bindir}/clang++ \
  -DCMAKE_AR=%{_bindir}/llvm-ar \
  -DCMAKE_RANLIB=%{_bindir}/llvm-ranlib \
  -DCMAKE_LINKER=%{_bindir}/llvm-ld \
  -DCMAKE_OBJDUMP=%{_bindir}/llvm-objdump \
  -DCMAKE_NM=%{_bindir}/llvm-nm \
%else
  -DCMAKE_AR=%{_bindir}/gcc-ar \
  -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
  -DCMAKE_NM=%{_bindir}/gcc-nm \
%endif
%if 0%{with native}
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=ON \
%else
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=OFF \
%endif
  -DWITH_LLVM:BOOL=ON \
%if !%{with llvm_submod}
  -DBUILD_LLVM_SUBMODULE:BOOL=OFF \
%endif
  -DUSE_FAUDIO:BOOL=OFF \
  -DUSE_DISCORD_RPC:BOOL=OFF \
%if 0%{?with_sysflatbuffers}
  -DUSE_SYSTEM_FLATBUFFERS:BOOL=ON \
%endif
  -DUSE_SYSTEM_CURL:BOOL=ON \
%if 0%{?with_sysffmpeg}
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
%endif
  -DUSE_SYSTEM_LIBPNG:BOOL=ON \
  -DUSE_SYSTEM_LIBUSB:BOOL=ON \
  -DUSE_SYSTEM_PUGIXML:BOOL=ON \
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
