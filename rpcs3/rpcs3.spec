%global _lto_cflags %{nil}
%undefine _hardened_build
%undefine _cmake_shared_libs

%global commit d6597038eeb36f6dbb6bb422d6a2edac63a62df6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220210
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

%global commit13 c9706bdda0ac22b9856f1aa8261e5b9e15cd20c5
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 glslang

%global commit14 6cf133697c4413dc9ae0fefefeba5f33587dff76
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 hidapi

%global commit15 4bbf90d60419ffcdc2d2f402be794b98d155f2c9
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

%bcond_with     native

%global sevenzip_ver 19.00
%global stb_ver 2.27

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/RPCS3
%global kg_url https://github.com/KhronosGroup

Name:           rpcs3
Version:        0.0.20
Release:        2%{?gver}%{?dist}
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
Source18:       %{vc_url}/llvm-mirror/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
Source19:       https://github.com/intel/%{srcname19}/archive/%{commit19}/%{srcname19}-%{shortcommit19}.tar.gz

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-Change-default-settings.patch


BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(flatbuffers)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew) >= 1.13.0
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires:  ffmpeg-devel
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

Provides:       bundled(7z) = %{sevenzip_ver}
Provides:       bundled(spirv-tools) = 0~git%{shortcommit10}
Provides:       bundled(soundtouch) = 0~git%{shortcommit11}
Provides:       bundled(asmjit) = 0~git%{shortcommit12}
Provides:       bundled(glslang) = 0~git%{shortcommit13}
Provides:       bundled(hidapi) = 0~git%{shortcommit14}
Provides:       bundled(stb) = %{stb_ver}
Provides:       bundled(wolfssl) = 0~git%{shortcommit15}
Provides:       bundled(yaml-cpp) = 0~git%{shortcommit16}
Provides:       bundled(llvm) = 0~git%{shortcommit18}

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
tar -xf %{S:18} -C llvm --strip-components 1

mkdir -p %{__cmake_builddir}/3rdparty/llvm_build/ittapi
tar -xf %{S:19} -C %{__cmake_builddir}/3rdparty/llvm_build/ittapi --strip-components 1

sed -e 's|${GIT_EXECUTABLE}|true|g' \
  -i llvm/lib/ExecutionEngine/IntelJITEvents/CMakeLists.txt

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

%build

%cmake \
%if 0%{with native}
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=ON \
%else
  -DUSE_NATIVE_INSTRUCTIONS:BOOL=OFF \
%endif
  -DUSE_FAUDIO:BOOL=OFF \
  -DUSE_DISCORD_RPC:BOOL=OFF \
  -DUSE_SYSTEM_FLATBUFFERS:BOOL=ON \
  -DUSE_SYSTEM_CURL:BOOL=ON \
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
  -DUSE_SYSTEM_LIBPNG:BOOL=ON \
  -DUSE_SYSTEM_LIBUSB:BOOL=ON \
  -DUSE_SYSTEM_PUGIXML:BOOL=ON \
  -DUSE_SYSTEM_XXHASH:BOOL=ON \
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
* Thu Feb 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.20-2.20220210gitd659703
- Bump

* Wed Feb 09 2022 Phantom X <megaphantomx at hotmail dot com> - 0.0.20-1.20220208gitd172b9a
- Initial spec
