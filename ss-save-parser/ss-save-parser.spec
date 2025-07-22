%global commit 06922280e79cf19956654413d40e06448a738f23
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210723
%bcond snapshot 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global binname SS_Backup_RAM_Parser

Name:           ss-save-parser
Version:        0.9.9
Release:        1%{?dist}
Summary:        Parser for Sega Saturn images of various save media

License:        GPL-2.0-only
URL:            https://github.com/hitomi2500/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  gcc-g++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)


%description
This is a QT-based parser for Sega Saturn RAM Backup (aka Power Memory),
Internal RAM, and possibly other media images. It can load/save/show image's
content and extract/insert/delete single saves in a customizable way.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed 's/\r//' -i README.md

cat > %{binname}.desktop <<EOF
[Desktop Entry]
Name=SS Backup RAM Parser
Comment=Parser for Sega Saturn images
Exec=%{binname}
Terminal=false
Icon=%{binname}
Type=Application
Categories=Qt;Game;
EOF

magick masqurin_highwizard.xpm %{binname}.png

sed -e '/^QMAKE_LFLAGS/d' -i %{binname}.pro

%build
%{qmake_qt5} %{binname}.pro
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{binname} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{binname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
install -pm0644 %{binname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{binname}.png

for res in 16 22 24 32 36 48 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick %{binname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{binname}.png
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{binname}.*


%changelog
* Mon Aug 12 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9.9-1
- Initial spec

