%undefine _cmake_shared_libs

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}

%global commit 35525d174940281251fb33490ebb66c6223f9f3b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221111
%global with_snapshot 0

%bcond_with rust

# Hashes in Source/3rdParty/CMakeLists.txt

%global commit1 7ee312cb282a7794c62d5d284bf93151c585dd1f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 mupen64plus-core

%global commit2 39f79201baa15890c4cbae92f2215a634cc3ee6d
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 mupen64plus-rsp-cxd4

%global commit3 88093cb43499eff53d343653cddcae2132af17ef
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 mupen64plus-rsp-hle

%global commit4 cfeea3a0f89ba5bc4265acb75778e1267ed1e424
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 parallel-rsp

%global commit5 e6b23e127ca3d3b21cd715751c32deae5adccee6
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 mupen64plus-input-qt

%global commit6 86112413e98a8648edb11d199673cc24d5799af8
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 mupen64plus-input-raphnetraw

%global commit7 158e74d4ec1c818289cd19c3a05e498c3ceff758
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 angrylion-rdp-plus

%global commit8 71dcb55a398a5c4d2bdbfa9fc15b90f301f77a6b
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 GLideN64

%global commit9 2c2226517c4c8929e08ec944654867e26efe0cf5
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 parallel-rdp-standalone

%global commit10 21639fb13dfa797a7c0949ffd9bbda9a3456fc69
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 mupen64plus-input-gca

%global commit11 d7c8516a4b848c0291e3d75b627c0843f515f591
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 imgui

%if %{with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname RMG
%global appname com.github.Rosalie241.%{pkgname}
%global mupen64_url https://github.com/mupen64plus
%global vc_url https://github.com/Rosalie241

Name:           rmg
Version:        0.3.5
Release:        1%{?gver}%{?dist}
Summary:        Rosalie's Mupen GUI

License:        GPL-3.0-only AND ( MIT OR LGPL-3.0-only ) AND GPL-2.0-only AND MIT
URL:            https://github.com/Rosalie241/RMG

%if %{with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        %{mupen64_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{mupen64_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{mupen64_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        %{vc_url}/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        %{vc_url}/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/raphnet/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/ghostlydark/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        https://github.com/gonetz/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        %{vc_url}/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
%{?with_rust:Source10: https://github.com/amatho/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz}
Source11:       https://github.com/ocornut/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz

Patch10:        0001-Fix-library-path.patch
Patch11:        0001-Use-system-SDL_GameControllerDB.patch

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
BuildRequires:  minizip-compat-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(lightning)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6OpenGL)
BuildRequires:  pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers
Requires:       dejavu-sans-fonts
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa}

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{pkgname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(mupen64plus) = 0~git%{shortcommit1}
Provides:       bundled(imgui) = 0~git%{shortcommit11}

%global __provides_exclude_from ^%{_libdir}/%{pkgname}/.*


%description
Rosalie's Mupen GUI is a free and open-source mupen64plus GUI written in C++.

%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

for i in \
  %{srcname1} %{srcname2} %{srcname3} %{srcname4} %{srcname5} \
  %{srcname6} %{srcname7} %{srcname8} %{srcname9} %{srcname11}
do
  mkdir -p %{__cmake_builddir}/Source/3rdParty/$i
done

mkdir LICENSEdir READMEdir

pushd %{__cmake_builddir}/Source/3rdParty
tar -xf %{S:1} -C %{srcname1} --strip-components 1
tar -xf %{S:2} -C %{srcname2} --strip-components 1
tar -xf %{S:3} -C %{srcname3} --strip-components 1
tar -xf %{S:4} -C %{srcname4} --strip-components 1
tar -xf %{S:5} -C %{srcname5} --strip-components 1
tar -xf %{S:6} -C %{srcname6} --strip-components 1
tar -xf %{S:7} -C %{srcname7} --strip-components 1
tar -xf %{S:8} -C %{srcname8} --strip-components 1
tar -xf %{S:9} -C %{srcname9} --strip-components 1
tar -xf %{S:11} -C %{srcname11} --strip-components 1

rm -rf parallel-rdp-standalone/vulkan-headers

for i in GLideN64 %{name}-{core,{input-{qt,raphnetraw}},rsp-hle} parallel-{rdp-standalone,rsp} ;do
  if [ -f $i/LICENSES ] ;then
    cp -p $i/LICENSES ../../../LICENSEdir/LICENSES.$i
  fi
  if [ -f $i/LICENSE ] ;then
    cp -p $i/LICENSE ../../../LICENSEdir/LICENSE.$i
  fi
  if [ -f $i/LICENSE.LESSER ] ;then
    cp -p $i/LICENSE.LESSER ../../../LICENSEdir/LICENSE.LESSER.$i
  fi
  if [ -f $i/LICENSE.MIT ] ;then
    cp -p $i/LICENSE.MIT ../../../LICENSEdir/LICENSE.MIT.$i
  fi
done

cp -p "angrylion-rdp-plus/MAME License.txt" ../../../LICENSEdir/MAME_License.angrylion-rdp-plus.txt
cp -p imgui/LICENSE.txt ../../../LICENSEdir/LICENSE.imgui

ln -s angrylion-rdp-plus mupen64plus-video-angrylion-plus
ln -s GLideN64 mupen64plus-video-GLideN64
ln -s parallel-rdp-standalone mupen64plus-video-parallel
ln -s parallel-rsp mupen64plus-rsp-parallel

%if %{with rust}
mkdir -p %{srcname10}
tar -xf %{S:10} -C %{srcname10} --strip-components 1
%else
sed -e 's| cargo|\0_disabled|g' -i ../../../Source/3rdParty/CMakeLists.txt
%endif

sed \
  -e '/find_package\(Git\)/d' \
  -e '/GIT_BRANCH/s|unknown|main|g' \
  -e '/GIT_COMMIT_HASH/s|unknown|%{shortcommit7}|g' \
  -i angrylion-rdp-plus/git-version.cmake

rm -rf parallel-rsp/lightning
sed -e '/PARALLEL_RSP_BAKED_LIGHTNING/s|ON|OFF|' -i parallel-rsp/CMakeLists.txt
sed -e 's|<lightning.h>|<lightning/lightning.h>|g' -i parallel-rsp/rsp_jit.hpp

popd

sed \
  -e '/Git /d' \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} describe --tags --always|echo \"%{version}-%{release}\"|g" \
  -i CMakeLists.txt

sed -e 's|_LIBDIR_|%{?_lib}|g' -i Source/RMG-Core/Directories.cpp

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' -i Source/RMG-Input/main.cpp


%build
%cmake \
  -DNO_GIT_CLONE:BOOL=ON \
  -DPORTABLE_INSTALL:BOOL=OFF \
  -DUPDATER:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DDISCORD_RPC:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

chmod +x %{buildroot}%{_libdir}/%{pkgname}/*/*.so

ln -sf ../fonts/dejavu-sans-fonts/DejaVuSans.ttf %{buildroot}%{_datadir}/%{pkgname}/font.ttf

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml


%files
%license LICENSE LICENSEdir/*
%doc README.md
%{_bindir}/%{pkgname}
%{_libdir}/%{pkgname}
%{_datadir}/%{pkgname}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/%{appname}.appdata.xml


%changelog
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

