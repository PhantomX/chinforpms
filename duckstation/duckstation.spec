%undefine _cmake_shared_libs
#global _lto_cflags -fno-lto

%global with_sysvulkan 1

%global commit 0313ce6aeeef95647dcc2ae049a9b0ca1009a2a4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210331
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/stenzek/%{name}

Name:           duckstation
Version:        0.1
Release:        7%{?gver}%{?dist}
Summary:        A Sony PlayStation (PSX) emulator

Url:            https://www.duckstation.org
License:        GPLv3

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Set-datadir-to-RPM-packaging.patch
Patch2:         0001-Fix-translation-names.patch
Patch3:         0001-cubeb-always-set-same-audiostream-name.patch
Patch4:         0001-Hotkeys-audio-volume-step-by-5.patch
Patch5:         0001-cubeb-set-CUBEB_STREAM_PREF_PERSIST.patch


ExclusiveArch:  x86_64 armv7l aarch64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  extra-cmake-modules
BuildRequires:  cmake(cubeb)
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Widgets)
#BuildRequires:  cmake(RapidJSON)
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(libcue)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(tinyxml2)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  minizip-compat-devel
%if 0%{?with_sysvulkan}
BuildRequires:  pkgconfig(glslang) >= 11.0.0
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  vulkan-headers
%else
Provides:       bundled(glslang) = git~0
Provides:       bundled(spirv-cross) = 0~git
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  hicolor-icon-theme

Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa}
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}


%description
A Sony PlayStation (PSX) emulator, focusing on playability, speed, and long-term
maintainability.


%package nogui
Summary:        DuckStation emulator without a graphical user interface
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

%description nogui
DuckStation emulator without a graphical user interface.


%package data
Summary:        DuckStation emulator data files
BuildArch:      noarch

%description data
This package provides the data files for duckstation.

####################################################

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

###Remove Bundled:
pushd dep
rm -rf \
  cubeb discord-rpc libcue libchdr libFLAC libsamplerate lzma minizip rapidjson \
  rcheevos tinyxml2 vulkan-loader/include/vulkan xxhash zlib

%if 0%{?with_sysvulkan}
  rm -rf glslang
%else
  sed -e 's|SPIRV-Tools|SPIRV-Tools_disabled|g' -i CMakeLists.txt
  cp -p glslang/LICENSE.txt LICENSE.glslang
%endif
cp -p imgui/LICENSE.txt LICENSE.glslang
cp -p simpleini/LICENCE.txt LICENSE.simpleini
cp -p vixl/LICENCE LICENSE.vixl
cp -p xbyak/COPYRIGHT COPYRIGHT.xbyak

popd

pushd src/%{name}-qt/translations
mv %{name}-qt_pt-br.ts %{name}-qt_pt_BR.ts
mv %{name}-qt_pt-pt.ts %{name}-qt_pt_PT.ts
mv %{name}-qt_zh-cn.ts %{name}-qt_zh_CN.ts
popd


%if 0%{?with_snapshot}
sed \
  -e 's|${HASH}|%{commit}|g' \
  -e 's|${BRANCH}|master|g' \
  -e 's|${TAG}|%{version}-%{release}|g' \
  -e 's|${DATE}|%{date}|g' \
  -i src/scmversion/gen_scmversion.sh
%endif

sed -e 's|_RPM_DATADIR_|%{_datadir}/%{name}|g' \
  -i src/duckstation-qt/qthostinterface.cpp \
  src/frontend-common/common_host_interface.cpp \
  src/frontend-common/postprocessing_chain.cpp

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' \
  -i src/frontend-common/sdl_controller_interface.cpp


%build
%cmake \
  -DUSE_WAYLAND:BOOL=ON \
  -DENABLE_CHEEVOS:BOOL=OFF \
  -DENABLE_DISCORD_PRESENCE:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/bin/%{name}-{qt,nogui} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r %{__cmake_builddir}/bin/{database,inputprofiles,resources,shaders,translations} \
  %{buildroot}%{_datadir}/%{name}/

rm -f %{buildroot}%{_datadir}/%{name}/database/gamecontrollerdb.txt

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key Terminal \
  --set-value false \
  appimage/%{name}-qt.desktop

for res in 16 32 48 64 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 appimage/icon-${res}px.png ${dir}/%{name}-qt.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name}-qt --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-qt.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/*.appdata.xml


%files -f %{name}-qt.lang
%doc README.md
%license LICENSE dep/LICENSE.* dep/COPYRIGHT.*
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-qt.*
%{_metainfodir}/*.appdata.xml


%files nogui
%doc README.md
%license LICENSE dep/LICENSE.* dep/COPYRIGHT.*
%{_bindir}/%{name}-nogui


%files data
%doc NEWS.md README.md
%license LICENSE
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/translations


%changelog
* Thu Apr 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-7.20210331git0313ce6
- Bump

* Sat Mar 27 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-6.20210327gite9aab64
- Bump

* Sun Mar 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-5.20210321git4c3d2cd
- Add missing system path

* Sat Mar 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-4.20210320gita5e316b
- Change volume hotkey steps

* Fri Mar 19 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-3.20210319git76d3028
- Enable LTO

* Tue Mar 16 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-2.20210316gitb1cf255
- Support build with system SPIRV/glslang

* Mon Mar 15 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-1.20210315gita34f0d5
- Initial spec
