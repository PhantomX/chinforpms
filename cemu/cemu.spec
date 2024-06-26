%undefine _hardened_build
%undefine _cmake_shared_libs
%undefine _debugsource_packages

%bcond_with clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 13b90874f9934f0a79a9ab2b9c4e1288ed2e6764
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240513
%bcond_with snapshot

# Enable system fmt
%bcond_without fmt

%global commit1 f65bcf481ab34cd07d3909aab1479f409fa79f2f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 imgui

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global fmt_ver 10.2.1
%global vkh_ver 1.3.240

%global vc_url   https://github.com/cemu-project/Cemu

%global pkgname Cemu
%global appname info.%{name}.%{pkgname}

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global pat     %%(echo %%{ver} | cut -s -d- -f2)

Name:           cemu
Version:        2.0~86
Release:        1%{?dist}
Summary:        A Nintendo Wii U Emulator

License:        MPL-2.0 AND MIT AND MIT-0 AND Apache-2.0
URL:            https://cemu.info/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{ver}/%{pkgname}-%{ver}.tar.gz
%endif
Source1:        https://github.com/ocornut/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%if %{without fmt}
Source2:        https://github.com/fmtlib/fmt/archive/%{fmt_ver}/fmt-%{fmt_ver}.tar.gz
%endif

Patch10:        0001-Bundled-fmt-support.patch

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  ImageMagick
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
BuildRequires:  llvm
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  nasm
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  boost-devel
BuildRequires:  cmake(cubeb)
%if %{with fmt}
BuildRequires:  cmake(fmt) >= 9.1.0
%else
Provides:       bundled(fmt) = %{fmt_ver}
%endif
BuildRequires:  cmake(glm)
BuildRequires:  cmake(glslang)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(pugixml)
BuildRequires:  cmake(RapidJSON)
BuildRequires:  pkgconfig(sdl2) >= 2.30.0
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  wxGTK-devel >= 3.2
BuildRequires:  pkgconfig(zarchive)
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(imgui) = 0~git%{?shortcommit1}
Provides:       bundled(ih264d) = 0~git

Provides:       %{pkgname}%{?_isa} = %{version}-%{release}

%description
%{pkgname} is a software to emulate Wii U games and applications on PC.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

pushd dependencies
rm -rf cubeb DirectX_2010 discord-rpc vcpkg* Vulkan-Headers ZArchive

mkdir -p imgui
tar -xf %{S:1} -C imgui --strip-components 1
%if %{without fmt}
mkdir fmt
tar -xf %{S:2} -C fmt --strip-components 1
sed -e '/^find_package(fmt/s|9 REQUIRED|%{fmt_ver}|' -i ../CMakeLists.txt
%endif

cp -p imgui/LICENSE.txt LICENSE.imgui
cp -p ih264d/NOTICE NOTICE.ih264d
popd

%if %{with fmt}
# Fixes from https://aur.archlinux.org/packages/cemu
# unbundled fmt
sed -e '/FMT_HEADER_ONLY/d' -i src/Common/precompiled.h
%endif
# gamelist column width improvement
sed \
  -e '/InsertColumn/s/kListIconWidth/&+8/;/SetColumnWidth/s/last_col_width/&-1/' \
  -i src/gui/components/wxGameList.cpp

%if "%{pat}"
sed -e "/#define EMULATOR_VERSION_MINOR/s/[0-9]\+/%{pat}/;s/-/./" -i src/Common/version.h
%endif

sed -e '/CMAKE_INTERPROCEDURAL_OPTIMIZATION/s| ON| OFF|g' -i CMakeLists.txt


%build
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DENABLE_VCPKG:BOOL=OFF \
  -DENABLE_DISCORD_RPC:BOOL=OFF \
  -DPORTABLE:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/%{pkgname}_release %{buildroot}%{_bindir}/%{pkgname}

mkdir -p %{buildroot}%{_datadir}/%{pkgname}
cp -rp bin/{gameProfiles,resources,shaderCache} \
  %{buildroot}%{_datadir}/%{pkgname}/

mkdir -p %{buildroot}%{_datadir}/applications
install -pm644 dist/linux/%{appname}.desktop \
  %{buildroot}%{_datadir}/applications/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -pm0644 dist/linux/%{appname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{appname}.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert dist/linux/%{appname}.png \
    -filter Lanczos -resize ${res}x${res} ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 dist/linux/%{appname}.metainfo.xml %{buildroot}%{_metainfodir}/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE.txt dependencies/{LICENSE,NOTICE}.*
%doc README.md
%{_bindir}/%{pkgname}
%{_datadir}/%{pkgname}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Sun Jun 23 2024 Phantom X <megaphantomx at hotmail dot com> - 2.0~86-1
- 2.0-86

* Mon Feb 19 2024 Phantom X <megaphantomx at hotmail dot com> - 2.0~65-1.20240218git3a02490
- Add snapshot support

* Fri Apr 21 2023 Phantom X <megaphantomx at hotmail dot com> - 2.0~36-1
- Initial spec
