%undefine _cmake_shared_libs
# no defined reference for "fastjmp_set"
%global _lto_cflags -fno-lto

%bcond_with clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%bcond_with nogui

# Enable system fmt
%bcond_with fmt
# Enable system soundtouch (needs no exception)
%bcond_with soundtouch
%bcond_without vulkan

%global commit d9846093c3991329c5b3cfb7ff9aba229114d581
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240206
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global appname org.%{name}.DuckStation
%global vc_url  https://github.com/stenzek/%{name}

%global glad_ver 0.1.33
%global imgui_ver 1.90.1
%global md5_ver 1.6
%global rcheevos_scommit 74860c9
%global soundtouch_ver 2.3.1
%global stb_ver 2.25

Name:           duckstation
Version:        0.1
Release:        110%{?dist}
Summary:        A Sony PlayStation (PSX) emulator

Url:            https://www.duckstation.org
License:        GPL-3.0-only AND MIT AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0 AND OFL-1.1%{!?with_soundtouch: AND LGPL-2.1}

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Set-datadir-to-RPM-packaging.patch
Patch2:         0001-Fix-translation-names.patch
Patch3:         0001-cubeb-always-set-same-audiostream-name.patch
Patch4:         0001-Hotkeys-audio-volume-step-by-5.patch
Patch5:         0001-Revert-Qt-Make-dark-fusion-the-default-theme.patch
Patch6:         0001-gamedb-missings-hashes-and-personal-additions.patch
Patch7:         0001-Disable-font-downloading.patch

ExclusiveArch:  x86_64 aarch64

%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  extra-cmake-modules
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(RapidJSON)
BuildRequires:  qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires:  pkgconfig(egl)
BuildRequires:  cmake(FastFloat)
%if %{with fmt}
BuildRequires:  pkgconfig(fmt) >= 10.1
%else
Provides:       bundled(fmt) = 10.1.1
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libbacktrace)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(libcpuinfo)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(sdl2) >= 2.30.0
%if %{with soundtouch}
BuildRequires:  pkgconfig(soundtouch)
%endif
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  cmake(WebP)
BuildRequires:  pkgconfig(x11)
BuildRequires:  cmake(xbyak)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  minizip-compat-devel
%if %{with vulkan}
BuildRequires:  cmake(VulkanHeaders) >= 1.3.239
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  libappstream-glib

Requires:       coreutils
Requires:       google-roboto-fonts
Requires:       google-roboto-mono-fonts
Requires:       google-noto-sans-jp-fonts
Requires:       google-noto-sans-kr-fonts
Requires:       google-noto-sans-sc-fonts
Requires:       hicolor-icon-theme
Requires:       libGL%{?_isa}
Requires:       libwayland-egl%{?_isa}
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa}
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}
Suggests:       qt6-qttranslations

Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(glslang) = 0~git
Provides:       bundled(imgui) = %{imgui_ver}
Provides:       bundled(md5-deutsch) = %{md5_ver}
Provides:       bundled(rainterface) = 0~git
Provides:       bundled(rcheevos) = 0~git%{rcheevos_scommit}
Provides:       bundled(simpleini) = 0~git
%if %{without soundtouch}
Provides:       bundled(soundtouch) = %{soundtouch_ver}
%endif
Provides:       bundled(stb) = %{stb_ver}
Provides:       bundled(spirv-tools) = 0~git
%dnl Provides:       bundled(zydis) = 0~git

%if %{without nogui}
Provides:       %{name}-nogui = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-nogui < %{?epoch:%{epoch}:}%{version}-%{release}
%endif


%description
A Sony PlayStation (PSX) emulator, focusing on playability, speed, and long-term
maintainability.


%if %{with nogui}
%package nogui
Summary:        DuckStation emulator without a graphical user interface
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

%description nogui
DuckStation emulator without a graphical user interface.
%endif


%package data
Summary:        DuckStation emulator data files
BuildArch:      noarch

%description data
This package provides the data files for duckstation.

####################################################

%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

###Remove Bundled:
pushd dep
rm -rf \
  cpuinfo cubeb discord-rpc gsl libchdr libFLAC lzma minizip msvc \
  rapidjson xbyak xxhash zlib zstd d3d12ma fast_float biscuit riscv-disas zydis

%if %{with fmt}
  rm -rf fmt
%else
sed -e '/find_package/s|fmt|\0_DISABLED|g' -i CMakeLists.txt
cp fmt/LICENSE.rst LICENSE.fmt.rst
%endif

%if %{with soundtouch}
rm -rf soundtouch
%else
sed -e '/pkg_search_module/s|soundtouch|\0_DISABLED|g' -i CMakeLists.txt
cp soundtouch/COPYING.TXT COPYING.soundtouch
%endif

%if %{with vulkan}
  mkdir -p ../src/vulkan
  mv vulkan/include/vulkan/vk_mem_alloc.h ../src/vulkan/
  rm -rf vulkan
%else
  sed -e '/find_package/s|VulkanHeaders|\0_DISABLED|g' -i CMakeLists.txt
%endif

cp -p glslang/LICENSE.txt LICENSE.glslang
cp -p imgui/LICENSE.txt LICENSE.imgui
cp -p rainterface/LICENSE LICENSE.rainterface
cp -p simpleini/LICENCE.txt LICENSE.simpleini
cp -p vixl/LICENCE LICENSE.vixl
%dnl cp -p zydis/LICENSE LICENSE.zydis

popd

rm -f CMakeModules/FindSDL2.cmake
rm -f data/resources/fonts/*.txt

sed \
  -e '/NotoSansJP/s|\.ttf|.otf|' \
  -e '/NotoSansKR/s|\.ttf|.otf|' \
  -e '/NotoSansSC/s|\.ttf|.otf|' \
  -i src/duckstation-qt/qttranslations.cpp

pushd src/%{name}-qt/translations
rename -a - _ *.ts
rename _ - *.ts

sed -e 's|[Cc]ubed|Cubeb|g' -i %{name}-qt_pt_BR.ts
popd

sed \
  -e '/ENABLE_DISCORD_PRESENCE/s| ON| OFF|g' \
  -i CMakeLists.txt

%if %{with snapshot}
sed \
  -e 's|${HASH}|%{commit}|g' \
  -e 's|${BRANCH}|master|g' \
  -e 's|${TAG}|%{version}-%{release}|g' \
  -e 's|${DATE}|%{date}|g' \
  -i src/scmversion/gen_scmversion.sh
%endif

sed \
  -e 's|@GIT_VERSION@|%{version}-%{release}|g' \
%if %{with snapshot}
  -e 's|@GIT_DATE@|%{date}|g' \
%else
  -e 's| date="@GIT_DATE@"||g' \
%endif
  scripts/%{appname}.metainfo.xml.in > %{appname}.metainfo.xml

sed \
  -e 's|_RPM_DATADIR_|%{_datadir}/%{name}|g' \
  -e 's|_RPM_QTTDIR_|%{_qt6_translationdir}|g' \
  -i src/duckstation-qt/qt{host,translations}.cpp


%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%if %{without nogui}
  -DBUILD_NOGUI_FRONTEND:BOOL=OFF \
%endif
  -DUSE_WAYLAND:BOOL=ON \
  -DENABLE_DISCORD_PRESENCE:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/bin/%{name}-qt %{buildroot}%{_bindir}/%{name}-qt

%if 0%{?with_nogui}
install -pm0755 %{__cmake_builddir}/bin/%{name}-nogui %{buildroot}%{_bindir}/%{name}-nogui
%endif

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r %{__cmake_builddir}/bin/{resources,translations} \
  %{buildroot}%{_datadir}/%{name}/

rm -f %{buildroot}%{_datadir}/%{name}/database/gamecontrollerdb.txt
ln -sf ../../SDL_GameControllerDB/gamecontrollerdb.txt \
  %{buildroot}%{_datadir}/%{name}/resources/gamecontrollerdb.txt

rm -f %{buildroot}%{_datadir}/%{name}/resources/fonts/Roboto*
ln -sf ../../../fonts/google-roboto/Roboto-Regular.ttf \
  %{buildroot}%{_datadir}/%{name}/resources/fonts/Roboto-Regular.ttf

ln -sf ../../../fonts/google-roboto-mono/'RobotoMono[wght].ttf' \
  %{buildroot}%{_datadir}/%{name}/resources/fonts/RobotoMono-Medium.ttf

ln -sf ../../../fonts/google-noto-sans-jp-fonts/NotoSansJP-Regular.otf \
  %{buildroot}%{_datadir}/%{name}/resources/fonts/NotoSansJP-Regular.otf

ln -sf ../../../fonts/google-noto-sans-sc-fonts/NotoSansSC-Regular.otf \
  %{buildroot}%{_datadir}/%{name}/resources/fonts/NotoSansSC-Regular.otf

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  scripts/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -pm0644 scripts/%{appname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/

for res in 16 22 24 32 36 48 64 72 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert scripts/%{appname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{appname}.metainfo.xml %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml

%find_lang %{name}-qt --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/*.metainfo.xml


%files -f %{name}-qt.lang
%doc README.md
%license LICENSE dep/LICENSE.*
%{_bindir}/%{name}-qt*
%dir %{_datadir}/%{name}/translations/
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/*.metainfo.xml


%if %{with nogui}
%files nogui
%doc README.md
%license LICENSE dep/LICENSE.*
%{_bindir}/%{name}-nogui*
%endif


%files data
%doc README.md
%license LICENSE
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/resources/
%exclude %{_datadir}/%{name}/translations


%changelog
* Fri Jan 12 2024 Phantom X <megaphantomx at hotmail dot com> - 0.1-108.20240110git5d3cf93
- Add more font packages to requirements

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1-84.20230316git3bbce19
- gcc 13 build fix

* Fri Nov 25 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-76.20221123git11559c1
- Remove unneeded wrapper

* Wed Aug 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-61.20220810git4652c5f
- Bump

* Thu Aug 04 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-60.20220807git73a80d3
- Again

* Mon Aug 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-59.20220801gitefa4f53
- Update

* Wed Jul 27 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-58.20220726git5ad268f
- Update

* Sat Jul 23 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-57.20220723git2d4404c
- Bump
- Qt6
- Add wrapper to copy some files to home dir
- nogui optional switch, disabled by default

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-56.20220513git6f932c2
- Last snapshot

* Tue Apr 19 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-55.20220418git44d47e8
- Update

* Mon Apr 04 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-54.20220404git1d9075f
- Bump

* Tue Jan 11 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-53.20220110git51041e4
- rcheevos update

* Sat Jan 08 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-52.20220106git46737ac
- Bump

* Sat Dec 25 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-51.20211225gitbee5048
- Last snapshot

* Fri Dec 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-50.20211216git59cb7c0
- Update

* Fri Nov 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-49.20211125gitd55c86c
- Last one

* Thu Nov 11 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-48.20211111gitf982a2a
- Bump

* Wed Nov 10 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-47.20211110gitc54c5f1
- Update

* Sat Nov 06 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-46.20211106git946481c
- Bump

* Sun Oct 31 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-45.20211029git287b1e1
- Bump

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
