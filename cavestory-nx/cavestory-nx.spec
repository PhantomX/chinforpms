Name:           cavestory-nx
Version:        1.3.0
Release:        1%{?dist}
Summary:        A side-action adventure game

License:        BSD
URL:            https://gitlab.com/coringao/%{name}
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Source1:        %{name}.appdata.xml

BuildRequires:  cmake
BuildRequires:  ImageMagick
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  pkgconfig(zlib)
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme


%package        data
Summary:        Data files of %{name}
License:        CCmark
BuildArch:      noarch

%description data
Data files of %{name}.


%description
Cave Story NX is a nostalgic side-action adventure game to jump and shoot,
using the modified NXEngine-evo engine.


%prep
%autosetup -p1

mv data/%{name}.6 .

sed -e 's|/usr/share/games/cavestory-nx/data/|%{_datadir}/%{name}/|g' \
  -i src/ResourceManager.cpp

%build
%cmake \
  -B %{__cmake_builddir} \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr data/* %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_mandir}/man6
install -pm0644 %{name}.6 %{buildroot}%{_mandir}/man6/

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=Cave Story NX
Type=Application
Comment=Side-action adventure game
Exec=%{name}
Icon=%{name}
Terminal=false
Categories=Game;ActionGame;
EOF

for res in 16 22 24 32 36 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert data/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license LICENSE
%doc CHANGELOG
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man6/*.6*
%{_metainfodir}/*.xml


%files data
%license LICENSE
%{_datadir}/%{name}/


%changelog
* Fri Mar 22 2019 Phantom X  <megaphantomx at bol dot com dot br> - 1.3.0-1
- Initial spec
