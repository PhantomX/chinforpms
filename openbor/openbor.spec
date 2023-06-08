%define _legacy_common_support 1
%define _fortify_level 2

%global commit ab6d51d6b53c93509f997510e366d01d6e9b5b2f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230530
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/DCurrent/%{name}

%global ver %%(echo %{version} | cut -d. -f3)

Name:           openbor
Version:        3.0.6391
Release:        1%{?dist}
Summary:        2D side scrolling engine

License:        BSD-3-Clause
URL:            http://www.chronocrash.com/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{ver}/%{name}-%{ver}.tar.gz
%endif
Source10:       README.Fedora

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  yasm
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
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

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
Name=Open Beats of Rage
Comment=%{summary}.
Icon=%{name}
Exec=%{name}
Categories=ArcadeGame;Game;
EOF

sed \
  -e "s|'libpng-config --prefix'/include/libpng|%(pkg-config libpng --variable=includedir)|g" \
  -e 's| -g | |g' \
  -e 's| -Werror | |g' \
  -e '/ -O2/d' \
  -e '/addprefix -L/d' \
  -e 's|-Wl,-rpath,$(LIBRARIES)||g' \
  -e 's|@$(CC)|$(CC)|g' \
  -e '/-o $(TARGET)/s|$(CFLAGS)|\0 $(LDFLAGS)|g' \
  -i engine/Makefile

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
%make_build -C engine \
  LNXDEV=%{_bindir} BUILD_LINUX=1 GCC_TARGET=%{_target_cpu} NO_STRIP=1


%install
mkdir -p %{buildroot}%{_libexecdir}
install -pm0755 engine/OpenBOR %{buildroot}%{_libexecdir}/%{name}

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
  convert engine/resources/OpenBOR_Icon_128x128.png -strip -filter Lanczos -resize ${res}x${res} \
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
* Wed May 31 2023 Phantom X <megaphantomx at hotmail dot com> - 3.0.6391-1
- Initial spec
