%global commit 3f3ea6eac7713aa3d36b3296058d52a7d3f0c913
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200110

%undefine _hardened_build

%global bundlelodepngver 20191109
%global bundlephysfsver 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname VVVVVV

Name:           vvvvvv
Version:        2.0
Release:        1%{?gver}%{?dist}
Summary:        2D puzzle platform video game

# 3rd-party modules licensing:
# * S1 (lodepng) - zlib -- static dependency;
# * S2 (physfs) - zlib -- static dependency;
License:        VVVVVV

URL:            https://github.com/TerryCavanagh/%{pkgname}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{pkgname}.png

Patch10:        0001-System-tinyxml.patch
Patch11:        0001-System-data-file.patch


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  pkgconfig(tinyxml)
Requires:       vvvvvv-data >= 2.1
Requires:       hicolor-icon-theme

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(lodepng) = %{bundlelodepngver}
Provides:       bundled(physfs) = %{bundlephysfsver}


%description
%{pkgname} is a %{summary}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

rm -rf desktop_version/tinyxml/*

cp -p desktop_version/README.md README_desktop.md

sed -e '/CMAKE_EXECUTABLE_SUFFIX/d' -i desktop_version/CMakeLists.txt

sed -e 's|_RPM_DATA_DIR_|%{_datadir}/%{pkgname}|g' -i desktop_version/src/FileSystemUtils.cpp


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

mkdir -p %{_target_platform}
pushd %{_target_platform}

%cmake ../desktop_version \
%{nil}

%make_build

popd


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{_target_platform}/%{name} %{buildroot}%{_bindir}/%{pkgname}

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
* Fri Jan 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.0-1
- Initial spec
