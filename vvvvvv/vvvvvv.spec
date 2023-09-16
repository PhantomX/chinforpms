# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global commit d741b3aa27d9288cc1dc61eb5f6d72c97f90fce3
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230914

%bcond_without systinyxml

%global commit2 18964554bc769255401942e0e6dfd09f2fab2093
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 lodepng

%global commit3 0d4e9aac4575744ddaae56b146f1be19f064f0e5
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 physfs

%global commit4 e45d9d16d430a3f5d3eee9fe40d5e194e1e5e63a
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 tinyxml2

%global commit6 dedf70e0a769bc52a17a36da840d96770fc26d12
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 c-hashmap

%global commit5 23.09
%global srcname5 FAudio

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname VVVVVV

Name:           vvvvvv
Version:        2.4
Release:        11%{?dist}
Summary:        2D puzzle platform video game

# 3rd-party modules licensing:
# * S1 (lodepng) - Zlib -- static dependency;
# * S4 (tinyxml2) - zlib -- static dependency, if with_systinyxml 0;
# * S6 (c-hashmap) - BSD-3-Clause -- static dependency, if with_systinyxml 0;
License:        VVVVVV AND Zlib AND BSD-3-Clause

URL:            https://github.com/TerryCavanagh/%{pkgname}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{pkgname}.png
Source2:        https://github.com/lvandeve/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/icculus/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%if %{without systinyxml}
Source4:        https://github.com/leethomason/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
%endif
Source5:        https://github.com/FNA-XNA/FAudio/archive/%{commit5}/%{srcname5}-%{commit5}.tar.gz
Source6:        https://github.com/Mashpoe/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz

Patch10:        0001-System-libraries.patch
Patch11:        0001-System-data-file.patch


BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(FAudio)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(physfs)
%if %{with systinyxml}
BuildRequires:  pkgconfig(tinyxml2) >= 8.0
%endif

Requires:       vvvvvv-data >= 2.1
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(lodepng) = 0~git%{shortcommit2}
#Provides:       bundled(physfs) = 0~git%%{shortcommit3}
%if %{without systinyxml}
Provides:       bundled(tinyxml2) = 0~git%{shortcommit4}
%endif
Provides:       bundled(c-hashmap) = 0~git%{shortcommit6}

%description
%{pkgname} is a %{summary}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

tar -xf %{S:2} -C third_party/lodepng --strip-components 1
tar -xf %{S:3} -C third_party/physfs \*/extras --strip-components 1

%if %{without systinyxml}
tar -xf %{S:4} -C third_party/tinyxml2 --strip-components 1
sed \
  -e '/\..\/third_party\/lodepng$/a..\/third_party\/tinyxml2' \
  -e '/find_package(FAudio CONFIG)/iadd_library(tinyxml2-static STATIC ${XML2_SRC})' \
  -e '/target_link_libraries/s| tinyxml2 | tinyxml2-static |g' \
  -i desktop_version/CMakeLists.txt
cp -p third_party/tinyxml2/LICENSE.txt LICENSE.tinyxml2
%endif

tar -xf %{S:5} -C third_party/FAudio \*/src/stb\*.h --strip-components 1
tar -xf %{S:6} -C third_party/c-hashmap --strip-components 1

cp -p third_party/lodepng/LICENSE LICENSE.lodepng
cp -p third_party/c-hashmap/LICENSE LICENSE.c-hashmap

cp -p desktop_version/README.md README_desktop.md

sed \
  -e 's|find_package(Git)|find_package(Git_disabled)|g' \
  -e '/CMAKE_BUILD_WITH_INSTALL_RPATH/d' \
  -e '/CMAKE_INSTALL_RPATH/d' \
  -i desktop_version/CMakeLists.txt


echo 'ADD_DEFINITIONS(-DINTERIM_COMMIT="%{shortcommit}")' >> desktop_version/CMakeLists.txt
echo 'ADD_DEFINITIONS(-DCOMMIT_DATE="%{date}")' >> desktop_version/CMakeLists.txt

sed -e 's|_RPM_DATA_DIR_|%{_datadir}|g' -i desktop_version/src/FileSystemUtils.cpp

cat > %{pkgname}.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=%{pkgname}
Comment=Explore one simple game mechanic: you can't jump - instead, reverse your own gravity at the press of a button.
Icon=%{pkgname}
Exec=%{pkgname}
Categories=Game;
EOF


%build

%cmake \
  -S desktop_version \
  -DBUNDLE_DEPENDENCIES:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/%{pkgname} %{buildroot}%{_bindir}/%{pkgname}

mkdir -p %{buildroot}%{_datadir}/%{pkgname}/{fonts,lang}

pushd desktop_version
for f in $(find fonts lang/*/ -print | sed -e '/\.\/$/d') ; do
  if [ -d ${f} ] ; then
    install -dm 755 %{buildroot}%{_datadir}/%{pkgname}/${f}
  else
    install -pm 644 ${f} %{buildroot}%{_datadir}/%{pkgname}/${f}
  fi
done
popd

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{pkgname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -pm0644 %{S:1} \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{pkgname}.png

for res in 16 22 24 32 36 48 64 72 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{S:1} \
    -filter Lanczos -resize ${res}x${res} ${dir}/%{pkgname}.png
done

desktop-file-validate %{buildroot}%{_datadir}/applications/%{pkgname}.desktop


%files
%license LICENSE.*
%doc README.md README_desktop.md
%{_bindir}/%{pkgname}
%{_datadir}/applications/%{pkgname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{pkgname}.png
%dir %{_datadir}/%{pkgname}
%{_datadir}/%{pkgname}/fonts
%{_datadir}/%{pkgname}/lang


%changelog
* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4-11.20230914gitd741b3a
- Removed utf8cpp BR

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4-9.20230315git4398861
- Build with system tinyxml2

* Thu Feb 02 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4-8.20230202git113fbb0
- Add fonts and lang files

* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 2.4-6.20220705git8ca53fa
- Update
- BR: FAudio, instead SDL2_mixer

* Tue Mar 08 2022 - 2.4-5.20220214git9c698c0
- Bump

* Wed Dec 22 2021 - 2.4-4.20211222gitf7454ba
- Last snapshot

* Wed Nov 24 2021 - 2.4-3.20211114git6e832ca
- Update

* Mon Sep 13 2021 - 2.4-2.20210912git2991b23
- Bump

* Tue Aug 31 2021 - 2.4-1.20210831git1cbc3bd
- 2.4 snapshot

* Mon Apr 19 2021 - 2.3-8.20210418git186f36b
- Update

* Mon Mar 22 2021 - 2.3-7.20210321git0da9b50
- Bump
- Remove system libraries patch

* Fri Dec 25 2020 - 2.3-6.20201224gite3aa768
- New snapshot
- Use bundled tinyxml2 for the time
- Compiler optimizations seems good now

* Thu Oct 29 2020 - 2.3-5.20201014git70e82df
- Update

* Mon Aug 31 2020 - 2.3-4.20200825gitc29d7c7
- Bump

* Sat Jul 18 2020 - 2.3-3.20200717gitaf89c52
- New snapshot

* Fri Jun 12 2020 - 2.3-2.20200612git628eb7b
- Bump

* Fri May 15 2020 - 2.3-1.20200514gitf617b6d
- 2.3

* Sun Apr 12 2020 - 2.2-8.20200409gitd403466
- Bump

* Thu Mar 19 2020 - 2.2-7.20200315gitcfd355b
- New snapshot

* Sun Mar 01 2020 - 2.2-6.20200301git8d44d93
- Bump

* Mon Feb 03 2020 - 2.2-5.20200202gitcefc95d
- Update data files patch

* Sun Feb 02 2020 - 2.2-4.20200202git8260bb2
- Bump

* Wed Jan 15 2020 - 2.2-3.20200115git6f8d2dc
- Bump
- Patch cmake to use system libraries

* Sat Jan 11 2020 - 2.2-2.20200111git901de41
- Bump

* Fri Jan 10 2020 - 2.2-1
- Initial spec
