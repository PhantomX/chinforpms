# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global commit 1cbc3bdc7cd69757a88aa0fe80fd3ee68dd663e1
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210831

%undefine _hardened_build

%global with_systinyxml 0

%global bundlelodepngver 20191109
%global bundlephysfsver 0
%global bundletinyxml 8.0.0

%global gver .%{date}git%{shortcommit}

%global pkgname VVVVVV

Name:           vvvvvv
Version:        2.4
Release:        1%{?gver}%{?dist}
Summary:        2D puzzle platform video game

# 3rd-party modules licensing:
# * S1 (lodepng) - zlib -- static dependency;
# * S2 (utf8cpp) - Boost -- static dependency;
# * S3 (tinyxml2) - zlib -- static dependency, if with_systinyxml 0;
License:        VVVVVV

URL:            https://github.com/TerryCavanagh/%{pkgname}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{pkgname}.png

Patch11:        0001-System-data-file.patch


BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  pkgconfig(physfs)
%if 0%{?with_systinyxml}
BuildRequires:  pkgconfig(tinyxml2)
%endif
BuildRequires:  utf8cpp-devel

Requires:       vvvvvv-data >= 2.1
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(lodepng) = %{bundlelodepngver}
#Provides:       bundled(physfs) = %%{bundlephysfsver}
%if !0%{?with_systinyxml}
Provides:       bundled(tinyxml2) = %{bundletinyxml}
%endif


%description
%{pkgname} is a %{summary}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

# Make sure that we are using system ones
rm -rf third_party/physfs/
rm -rf third_party/utfcpp/
%if 0%{?with_systinyxml}
rm -rf third_party/tinyxml2/
%else
sed \
  -e '/\..\/third_party\/lodepng$/a..\/third_party\/tinyxml2' \
  -e '/find_package(utf8cpp CONFIG)/aadd_library(tinyxml2-static STATIC ${XML2_SRC})' \
  -e '/target_link_libraries/s| tinyxml2 | tinyxml2-static |g' \
  -i desktop_version/CMakeLists.txt
%endif

cp -p desktop_version/README.md README_desktop.md

sed \
  -e 's|FIND_PACKAGE(Git)|FIND_PACKAGE(Git_disabled)|g' \
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
%if 0%{?with_systinyxml}
  -DUSE_SYSTEM_TINYXML:BOOL=ON \
%endif
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
%license LICENSE.md
%doc README.md README_desktop.md
%{_bindir}/%{pkgname}
%{_datadir}/applications/%{pkgname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{pkgname}.png
%dir %{_datadir}/%{pkgname}


%changelog
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
