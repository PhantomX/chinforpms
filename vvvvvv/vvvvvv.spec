# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global commit c29d7c7d149ccc3d5d297f2679b5a8b89e7ac910
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200825

%undefine _hardened_build

%global bundlelodepngver 20191109
%global bundlephysfsver 0

%global gver .%{date}git%{shortcommit}

%global pkgname VVVVVV

Name:           vvvvvv
Version:        2.3
Release:        4%{?gver}%{?dist}
Summary:        2D puzzle platform video game

# 3rd-party modules licensing:
# * S1 (lodepng) - zlib -- static dependency;
# * S2 (utf8cpp) - Boost -- static dependency;
License:        VVVVVV

URL:            https://github.com/TerryCavanagh/%{pkgname}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{pkgname}.png

Patch10:        0001-System-libraries.patch
Patch11:        0001-System-data-file.patch


BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  pkgconfig(physfs)
BuildRequires:  pkgconfig(tinyxml2)
Requires:       vvvvvv-data >= 2.1
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(lodepng) = %{bundlelodepngver}
#Provides:       bundled(physfs) = %%{bundlephysfsver}


%description
%{pkgname} is a %{summary}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

# Make sure that we are using system ones
rm -rf third_party/physfs/
rm -rf third_party/tinyxml2/

cp -p desktop_version/README.md README_desktop.md

sed \
  -e '/CMAKE_BUILD_WITH_INSTALL_RPATH/d' \
  -e '/CMAKE_INSTALL_RPATH/d' \
  -i desktop_version/CMakeLists.txt

sed -e 's|_RPM_DATA_DIR_|%{_datadir}|g' -i desktop_version/src/FileSystemUtils.cpp


%build

# Optimizations breaks build
export CFLAGS="$(echo %{optflags} | sed \
  -e 's/-O2\b/-O0/' \
  -e 's/-Wp,-D_FORTIFY_SOURCE=2//' \
  -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//' \
  -e 's/-fstack-protector-strong//' \
  -e 's/-fasynchronous-unwind-tables//' \
  -e 's/-fstack-clash-protection//' \
  -e 's/-fcf-protection//' \
)"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

%cmake \
  -S desktop_version \
  -DUSE_SYSTEM_PHYSFS:BOOL=ON \
  -DUSE_SYSTEM_TINYXML:BOOL=ON \
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
* Mon Aug 31 2020 Phantom X <megaphantomx at hotmail dot com> - 2.3-4.20200825gitc29d7c7
- Bump

* Sat Jul 18 2020 Phantom X <megaphantomx at hotmail dot com> - 2.3-3.20200717gitaf89c52
- New snapshot

* Fri Jun 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.3-2.20200612git628eb7b
- Bump

* Fri May 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.3-1.20200514gitf617b6d
- 2.3

* Sun Apr 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-8.20200409gitd403466
- Bump

* Thu Mar 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-7.20200315gitcfd355b
- New snapshot

* Sun Mar 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-6.20200301git8d44d93
- Bump

* Mon Feb 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-5.20200202gitcefc95d
- Update data files patch

* Sun Feb 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-4.20200202git8260bb2
- Bump

* Wed Jan 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-3.20200115git6f8d2dc
- Bump
- Patch cmake to use system libraries

* Sat Jan 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-2.20200111git901de41
- Bump

* Fri Jan 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.2-1
- Initial spec
