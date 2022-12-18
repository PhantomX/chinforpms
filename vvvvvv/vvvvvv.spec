# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global commit c177f456f4c7cce7be964eabe945daed13b8d7b6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221211

%global with_systinyxml 0

%global commit2 5601b8272a6850b7c5d693dd0c0e16da50be8d8d
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 lodepng

%global commit3 6925c1067de2c9e39d626bcba84db0113f8395f2
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 physfs

%global commit4 e45d9d16d430a3f5d3eee9fe40d5e194e1e5e63a
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 tinyxml2

%global commit5 22.09.01
%global srcname5 FAudio

%global gver .%{date}git%{shortcommit}

%global pkgname VVVVVV

Name:           vvvvvv
Version:        2.4
Release:        7%{?gver}%{?dist}
Summary:        2D puzzle platform video game

# 3rd-party modules licensing:
# * S1 (lodepng) - zlib -- static dependency;
# * S2 (utf8cpp) - Boost -- static dependency;
# * S3 (tinyxml2) - zlib -- static dependency, if with_systinyxml 0;
License:        VVVVVV

URL:            https://github.com/TerryCavanagh/%{pkgname}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{pkgname}.png
Source2:        https://github.com/lvandeve/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/icculus/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/leethomason/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/FNA-XNA/FAudio/archive/%{commit5}/%{srcname5}-%{commit5}.tar.gz

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
%if 0%{?with_systinyxml}
BuildRequires:  pkgconfig(tinyxml2) >= 8.0
%endif
BuildRequires:  utf8cpp-devel

Requires:       vvvvvv-data >= 2.1
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(lodepng) = 0~git%{shortcommit2}
#Provides:       bundled(physfs) = 0~git%%{shortcommit3}
%if !0%{?with_systinyxml}
Provides:       bundled(tinyxml2) = 0~git%{shortcommit4}
%endif


%description
%{pkgname} is a %{summary}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

tar -xf %{S:2} -C third_party/lodepng --strip-components 1
tar -xf %{S:3} -C third_party/physfs \*/extras --strip-components 1

%if !%{?with_systinyxml}
tar -xf %{S:4} -C third_party/tinyxml2 --strip-components 1
sed \
  -e '/\..\/third_party\/lodepng$/a..\/third_party\/tinyxml2' \
  -e '/find_package(utf8cpp CONFIG)/aadd_library(tinyxml2-static STATIC ${XML2_SRC})' \
  -e '/target_link_libraries/s| tinyxml2 | tinyxml2-static |g' \
  -i desktop_version/CMakeLists.txt
cp -p third_party/tinyxml2/LICENSE.txt LICENSE.tinyxml2
%endif

tar -xf %{S:5} -C third_party/FAudio \*/src/stb\*.h --strip-components 1

cp -p third_party/lodepng/LICENSE LICENSE.lodepng

cp -p desktop_version/README.md README_desktop.md

sed \
  -e 's|find_package(Git)|find_package(Git_disabled)|g' \
  -e '/CMAKE_BUILD_WITH_INSTALL_RPATH/d' \
  -e '/CMAKE_INSTALL_RPATH/d' \
  -i desktop_version/CMakeLists.txt


echo 'ADD_DEFINITIONS(-DINTERIM_COMMIT="%{shortcommit}")' >> desktop_version/CMakeLists.txt
echo 'ADD_DEFINITIONS(-DCOMMIT_DATE="%{date}")' >> desktop_version/CMakeLists.txt

sed -e 's|_RPM_DATA_DIR_|%{_datadir}|g' -i desktop_version/src/FileSystemUtils.cpp


%build

%cmake \
  -S desktop_version \
  -DBUNDLE_DEPENDENCIES:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/%{pkgname} %{buildroot}%{_bindir}/%{pkgname}

mkdir -p %{buildroot}%{_datadir}/%{pkgname}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{pkgname}.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=%{pkgname}
Comment=Explore one simple game mechanic: you can't jump - instead, reverse your own gravity at the press of a button.
Icon=%{pkgname}
Exec=%{pkgname}
Categories=Game;
EOF

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


%changelog
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
