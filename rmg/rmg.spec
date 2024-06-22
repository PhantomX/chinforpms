%undefine _cmake_shared_libs

%define _fortify_level 2
%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}

%global commit 0b629a015aca5ae3cc16c2b8bd826a093e3e4891
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240612
%bcond_without snapshot

%bcond_with rust

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname RMG
%global appname com.github.Rosalie241.%{pkgname}
%global mupen64_url https://github.com/mupen64plus
%global vc_url https://github.com/Rosalie241

Name:           rmg
Version:        0.6.2
Release:        1%{?dist}
Summary:        Rosalie's Mupen GUI

License:        GPL-3.0-only AND ( MIT OR LGPL-3.0-only ) AND GPL-2.0-only AND MIT
URL:            https://github.com/Rosalie241/RMG

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch11:        0001-Use-system-SDL_GameControllerDB.patch
Patch12:        0001-use-system-lzma-sdk.patch
Patch13:        0001-RMG-Core-shared-library-fixes.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  nasm
%if %{with rust}
BuildRequires:  cargo
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(freetype2)
%if %{defined fedora} && 0%{?fedora} >= 38 && 0%{?fedora} < 40
BuildRequires:  minizip-compat-devel
%endif
%if %{defined fedora} && 0%{?fedora} >= 40
BuildRequires:  minizip-ng-compat-devel
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(lightning)
BuildRequires:  pkgconfig(lzmasdk-c) >= 23.01
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers
Requires:       dejavu-sans-fonts
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa}

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{pkgname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(mupen64plus) = 0~git
Provides:       bundled(imgui) = 0~git

%global __provides_exclude_from ^%{_libdir}/%{pkgname}/.*


%description
Rosalie's Mupen GUI is a free and open-source mupen64plus GUI written in C++.

%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -N -p1
%autopatch -M 500 -p1

mkdir LICENSEdir READMEdir

pushd Source/3rdParty

rm -rf mupen64plus-core/subprojects/minizip/
rm -rf mupen64plus-video-GLideN64/projects/msvc/
rm -rf mupen64plus-video-parallel/vulkan-headers
rm -rf discord-rpc fmt lzma SDL_GameControllerDB vosk-api

for i in mupen64plus-{core,input-raphnetraw,rsp-{cx4,hle,parallel},video-{GLideN64,parallel}} ;do
  if [ -f $i/LICENSES ] ;then
    cp -p $i/LICENSES ../../LICENSEdir/LICENSES.$i
  fi
  if [ -f $i/LICENSE ] ;then
    cp -p $i/LICENSE ../../LICENSEdir/LICENSE.$i
  fi
  if [ -f $i/LICENSE.LESSER ] ;then
    cp -p $i/LICENSE.LESSER ../../LICENSEdir/LICENSE.LESSER.$i
  fi
  if [ -f $i/LICENSE.MIT ] ;then
    cp -p $i/LICENSE.MIT ../../LICENSEdir/LICENSE.MIT.$i
  fi
done

cp -p "mupen64plus-video-angrylion-plus/MAME License.txt" ../../LICENSEdir/MAME_License.angrylion-rdp-plus.txt
cp -p imgui/LICENSE.txt ../../LICENSEdir/LICENSE.imgui

%if %{without rust}
sed -e 's| cargo|\0_disabled|g' -i CMakeLists.txt
rm -rf mupen64plus-input-gca
%endif

sed \
  -e '/find_package\(Git\)/d' \
  -e '/GIT_BRANCH/s|unknown|main|g' \
  -e '/GIT_COMMIT_HASH/s|unknown|%{shortcommit7}|g' \
  -i mupen64plus-video-angrylion-plus/git-version.cmake

rm -rf mupen64plus-rsp-parallel/lightning
sed -e '/PARALLEL_RSP_BAKED_LIGHTNING/s|ON|OFF|' -i mupen64plus-rsp-parallel/CMakeLists.txt
sed -e 's|<lightning.h>|<lightning/lightning.h>|g' -i mupen64plus-rsp-parallel/rsp_jit.hpp

popd

echo %{version}-%{release} > VERSION

sed \
  -e 's|GIT_FOUND|DIT_DISABLED|g' \
  -i CMakeLists.txt

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' -i Source/RMG-Input/main.cpp

sed -e 's|_RPMVERSION_|%{version}|g' -i Source/RMG-Core/CMakeLists.txt


%build
%cmake \
  -DPORTABLE_INSTALL:BOOL=OFF \
  -DUPDATER:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DDISCORD_RPC:BOOL=OFF \
  -DVRU:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

rm -f %{buildroot}%{_libdir}/lib%{pkgname}-Core.so

chmod +x %{buildroot}%{_libdir}/*.so*
chmod +x %{buildroot}%{_libdir}/%{pkgname}/*/*.so

ln -sf ../fonts/dejavu-sans-fonts/DejaVuSans.ttf %{buildroot}%{_datadir}/%{pkgname}/font.ttf

mkdir -p %{buildroot}%{_datadir}/%{pkgname}/Styles

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml


%files
%license LICENSE LICENSEdir/*
%doc README.md
%{_bindir}/%{pkgname}
%{_libdir}/lib%{pkgname}-Core.so.*
%{_libdir}/%{pkgname}
%{_datadir}/%{pkgname}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/%{appname}.appdata.xml


%changelog
* Sat Jun 22 2024 Phantom X <megaphantomx at hotmail dot com> - 0.6.2-1.20240612git0b629a0
- 0.6.2

* Sun May 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.9-2
- lzma-sdk rebuild

* Sun May 05 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.9-1
- 0.5.9

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.8-1
- 0.5.8

* Sun Feb 11 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.7-2.20240128git685aa59
- Rebuild (lightning)

* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.7-1.20240128git685aa59
- 0.5.7

* Thu Jan 18 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.5-1
- 0.5.5

* Sat Dec 23 2023 Phantom X <megaphantomx at hotmail dot com> - 0.5.4-1
- 0.5.4

* Fri Sep 08 2023 Phantom X <megaphantomx at hotmail dot com> - 0.5.2-1.20230828gitd0928b5
- 0.5.2

* Tue Aug 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-1.20230828gitd0928b5
- 0.5.1

* Mon Aug 14 2023 Phantom X <megaphantomx at hotmail dot com> - 0.5.0-1.20230813git558a48f
- 0.5.0

* Wed Jul 19 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.4-1
- 0.4.4

* Wed Jul 12 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.3-1
- 0.4.3

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.1-2
- lzma-sdk rebuild

* Sun Jun 25 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.1-1
- 0.4.1

* Sat May 06 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.0-1
- 0.4.0

* Sat Apr 15 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.9-1
- 0.3.9

* Sun Feb 26 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.8-1.20230225gite10ac10
- 0.3.8

* Thu Feb 23 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.7-1
- 0.3.7

* Sun Feb 19 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.6-1
- 0.3.6

* Sat Feb 18 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.5-1
- 0.3.5

* Fri Feb 10 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.3-1
- 0.3.3
- R: sdl_gamecontrollerdb

* Mon Feb 06 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.1-1
- 0.3.1

* Tue Jan 24 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.0-1
- 0.3.0

* Sat Jan 07 2023 Phantom X <megaphantomx at hotmail dot com> - 0.2.9-1
- 0.2.9

* Thu Dec 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2.7-1
- 0.2.7

* Tue Dec 20 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2.5-1
- 0.2.5

* Thu Dec 08 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2.4-1
- 0.2.4

* Sun Nov 20 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1.9-1
- 0.1.9

* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1.6-0.1.20221111git35525d1
- Initial spec

