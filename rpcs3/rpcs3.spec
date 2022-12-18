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
# Enable system hidapi (disabled, bundled have modifications)
%global with_syshidapi 0
%global bundlehidapi 0.12.0

%global commit baa2768a6980a015117d3df001f33faa34e1eb57
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221217
%global with_snapshot 1

%global commit10 eb0a36633d2acf4de82588504f951ad0f2cecacb
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 SPIRV-Tools

%global commit11 83cfba67b6af80bb9bfafc0b324718c4841f2991
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 soundtouch

%global commit12 06d0badec53710a4f572cf5642881ce570c5d274
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 asmjit

%global commit13 5755de46b07e4374c05fb1081f65f7ae1f8cca81
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 glslang

%global commit14 c2aa9dd37c7b401b918fd56e18a3bac7f8f00ec2
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 hidapi

%global commit15 44f81f8bc082319cebf0e37df8470aa5748c1355
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 wolfssl

%global commit16 0b67821f307e8c6bf0eba9b6d3250e3cf1441450
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 yaml-cpp

%global commit17 85a1ed200d50660786c1a88d9166e871123cce39
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 SPIRV-Headers

%global commit18 9b52b6c39ae9f0759fbce7dd0db4b3290d6ebc56
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 llvm

%global commit19 c2a515bd34f37ba83c61474a04cd2bba57fde67e
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 ittapi

%global commit20 bf019f8c88bc64638fccef62840e935ab2689a4a
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 ffmpeg-core

%global commit21 06c5c7ed0bd987a918cf88caafb094f22cdd1721
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
Version:        0.0.25
Release:        4%{?gver}%{?dist}
Summary:        PS3 emulator/debugger

License:        GPL-2.0-only
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
%if !0%{?with_syshidapi}
Source14:       %{vc_url}/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
%endif
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
BuildRequires:  cmake(FAudio)
%if !%{with llvm_submod}
BuildRequires:  cmake(LLVM)
%endif
%if 0%{?with_sysflatbuffers}
BuildRequires:  pkgconfig(flatbuffers) >= %{bundleflatbuffers}
BuildRequires:  flatbuffers-compiler >= %{bundleflatbuffers}
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
%if 0%{?with_syshidapi}
BuildRequires:  pkgconfig(hidapi-hidraw) >= %{bundlehidapi}
%else
BuildRequires:  pkgconfig(libudev)
Provides:       bundled(hidapi) = %{bundlehidapi}
%endif
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libpng)
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

BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(spirv-tools) = 0~git%{shortcommit10}
Provides:       bundled(soundtouch) = 0~git%{shortcommit11}
Provides:       bundled(asmjit) = 0~git%{shortcommit12}
Provides:       bundled(glslang) = 0~git%{shortcommit13}
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

%if !0%{?with_syshidapi}
tar -xf %{S:14} -C 3rdparty/hidapi/hidapi --strip-components 1
cp -p 3rdparty/hidapi/hidapi/LICENSE.txt LICENSE.hidapi
sed -e 's|hidapi_FOUND|hidapi_DISABLED|g' -i 3rdparty/CMakeLists.txt
%endif

%if !0%{?with_sysflatbuffers}
tar -xf %{S:21} -C 3rdparty/flatbuffers --strip-components 1
cp -p 3rdparty/flatbuffers/LICENSE.txt 3rdparty/LICENSE.flatbuffers
%endif

pushd 3rdparty
cp -p stblib/LICENSE LICENSE.stb
cp -p asmjit/asmjit/LICENSE.md LICENSE.asmjit.md
cp -p glslang/glslang/LICENSE.txt LICENSE.glslang
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
  -e '/set(CMAKE_CXX_FLAGS/d' \
  -e '/set(CMAKE_C_FLAGS/d' \
  -i CMakeLists.txt

sed -e 's| -Werror||g' -i 3rdparty/wolfssl/wolfssl/CMakeLists.txt


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
  -DCMAKE_SKIP_RPATH:BOOL=ON \
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
  -DUSE_SYSTEM_FAUDIO:BOOL=ON \
  -DUSE_DISCORD_RPC:BOOL=OFF \
%if 0%{?with_sysflatbuffers}
  -DUSE_SYSTEM_FLATBUFFERS:BOOL=ON \
%endif
%if 0%{?with_syshidapi}
  -DHIDAPI_INCLUDEDIR:PATH=%{_includedir}/hidapi \
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
