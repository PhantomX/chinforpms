%global commit a1ee56d0acffff2cc30080675e44c78895df2296
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20260222
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname openbor
%global vc_url  https://github.com/DCurrent/%{pkgname}

%global ver %%(echo %{version} | cut -d. -f3)

Name:           %{pkgname}4
Version:        4.0.7762
Release:        1%{?dist}
Summary:        2D side scrolling engine - version 4

License:        BSD-3-Clause
URL:            http://www.chronocrash.com/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{ver}/%{pkgname}-%{ver}.tar.gz
%endif
Source10:       README.Fedora

ExclusiveArch:  x86_64 aarch64

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  nasm
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_gfx)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme

%description
OpenBOR is a royalty free sprite-based side scrolling gaming engine. 


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

install -m644 -p %{S:10} .

cat > %{name}.sh <<'EOF'
#!/usr/bin/bash
set -e
OPENBORBIN=%{_libexecdir}/%{name}

if [[ "${XDG_DATA_HOME}" ]] ;then
  OPENBORHOME="${XDG_DATA_HOME}/%{name}"
else
  OPENBORHOME="${HOME}/.local/share/%{name}"
fi

shopt -s nullglob

mkdir -p "${OPENBORHOME}"
cd "${OPENBORHOME}"
exec "${OPENBORBIN}" "$@"
EOF

cat > %{name}.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Open Beats of Rage 4
Comment=%{summary}.
Icon=%{name}
Exec=%{name}
Categories=ArcadeGame;Game;
EOF

sed \
  -e '/ENABLE_STATIC/d' \
  -i cmake/linux.cmake

sed \
  -e 's|$VERSION_BUILD|%{ver}|g' \
%if %{with snapshot}
  -e '/read -r/d' \
  -e 's|$VERSION_COMMIT|%{shortcommit}|g' \
  -e 's|${VERSION_COMMIT}|%{shortcommit}|g' \
  -e 's|0000000|%{shortcommit}|g' \
%endif
  -i engine/version.sh

pushd engine
chmod +x ./version.sh
./version.sh
popd


%build
export CFLAGS+=" -fno-strict-aliasing"
%cmake \
  -DCMAKE_PREFIX_PATH:PATH=%{_prefix} \
  -DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
  -DBUILD_LINUX:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_libexecdir}
install -pm0755 %{_vpath_builddir}/OpenBOR %{buildroot}%{_libexecdir}/%{name}

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.sh %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop


mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -pm0644 engine/resources/OpenBOR_Icon_128x128.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick engine/resources/OpenBOR_Icon_128x128.png -strip -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license engine/LICENSE
%doc README.*
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Mon Apr 27 2026 Phantom X <megaphantomx at hotmail dot com> - 4.0.7762-1.20260222gita1ee56d
- Initial spec

