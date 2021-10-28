%undefine _cmake_shared_libs
#global _lto_cflags -fno-lto

%global with_sysvulkan 0

%global commit 48ddebd82e1029876661010bd6c81f49c45f4182
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211025
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/stenzek/%{name}

%global glad_ver 0.1.33
%global imgui_ver 1.81
%global md5_ver 1.6
%global stb_ver 2.25

Name:           duckstation
Version:        0.1
Release:        44%{?gver}%{?dist}
Summary:        A Sony PlayStation (PSX) emulator

Url:            https://www.duckstation.org
License:        GPLv3

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        org.%{name}.DuckStation.metainfo.xml

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Set-datadir-to-RPM-packaging.patch
Patch2:         0001-Fix-translation-names.patch
Patch3:         0001-cubeb-always-set-same-audiostream-name.patch
Patch4:         0001-Hotkeys-audio-volume-step-by-5.patch
Patch5:         0001-Revert-Qt-Make-dark-fusion-the-default-theme.patch


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
BuildRequires:  cmake(RapidJSON)
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(libcurl)
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
BuildRequires:  vulkan-headers
%if 0%{?with_sysvulkan}
BuildRequires:  pkgconfig(glslang) >= 11.0.0
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools
BuildRequires:  pkgconfig(SPIRV-Tools)
%else
Provides:       bundled(glslang) = git~0
Provides:       bundled(spirv-tools) = 0~git
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  hicolor-icon-theme

Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa}
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(imgui) = %{imgui_ver}
Provides:       bundled(md5-deutsch) = %{md5_ver}
Provides:       bundled(rcheevos) = 0~git
Provides:       bundled(simpleini)
Provides:       bundled(stb) = %{stb_ver}
Provides:       bundled(xbyak)


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
  cubeb discord-rpc libchdr libFLAC libsamplerate lzma minizip msvc \
  rapidjson tinyxml2 vulkan-loader/include/vulkan xxhash zlib

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
  -DENABLE_CHEEVOS:BOOL=ON \
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
  extras//linux-desktop-files/%{name}-qt.desktop

for res in 16 32 48 64 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 extras/icons/icon-${res}px.png ${dir}/%{name}-qt.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/org.%{name}.DuckStation.metainfo.xml

%find_lang %{name}-qt --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-qt.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/*.metainfo.xml


%files -f %{name}-qt.lang
%doc README.md
%license LICENSE dep/LICENSE.* dep/COPYRIGHT.*
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}-qt.*
%{_metainfodir}/*.metainfo.xml


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
* Tue Oct 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-44.20211025git48ddebd
- Update

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-43.20211001gita7096f0
- Last snapshot
- Disable sysvulkan

* Sun Sep 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-42.20210925git8864b48
- Bump

* Sat Sep 18 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-41.20210915gitbacd834
- Last snapshot

* Fri Sep 10 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-40.20210910gite12474a
- Update

* Sun Aug 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-39.20210824gitbbcf1c6
- Bump

* Mon Aug 23 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-38.20210822git4848c72
- Update

* Tue Aug 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-37.20210817git1824197
- New one

* Mon Aug 09 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-36.20210807git4d0968a
- Bump

* Fri Jul 30 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-35.20210723git7f88cd5
- Update

* Fri Jul 23 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-34.20210723git7f88cd5
- Last snapshot

* Sun Jul 18 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-33.20210717gitd519ba3
- Bump

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-32.20210713gitc2c204c
- Update

* Fri Jul 09 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-31.20210709git7caa5c0
- Bump

* Sat Jul 03 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-30.20210703gitb4092a5
- Last snapshot

* Mon Jun 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-29.20210621git9d26a85
- Update
- Enable rcheevos support

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-28.20210611git9d36ce7
- Bump

* Wed Jun 09 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-27.20210609git44da133
- Bump

* Sat Jun 05 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-26.20210605gite118b54
- Bump

* Tue Jun 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-25.20210601git8b57c24
- Update

* Fri May 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-24.20210526git56c0825
- Update

* Tue May 25 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-23.20210524git350bae7
- Rebump

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-22.20210521git4436cd5
- Bump
- Remove libcue BR

* Tue May 18 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-21.20210518gitfd7f88f
- Update

* Mon May 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-20.20210516gitfce3ca0
- Update

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-19.20210512gitf2cf8d2
- Latest snapshot

* Sat May 08 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-18.20210508gitd9151ce
- Update

* Wed May 05 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-17.20210504gitd3fea7b
- Bump

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-16.20210501git20747d2
- Bump

* Tue Apr 27 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-15.20210427gitf1310bf
- Latest snapshot

* Sat Apr 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-14.20210424git844c8e9
- Update

* Thu Apr 22 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-13.20210422git8f821c7
- Daily

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-12.20210421git9652e3c
- Bump

* Sun Apr 18 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-11.20210418gitc79d93f
- New snapshot
- BR: rapidjson

* Wed Apr 14 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-10.20210414git88618bd
- Update

* Mon Apr 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-9.20210412git62718b3
- Bump

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-8.20210407gitfc9d276
- Update

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
