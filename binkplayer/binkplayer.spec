# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global pkgname BinkLinuxPlayer
%if %{__isa_bits} == 64
%global binbits 64
%endif

Name:           binkplayer
Version:        2025.01
Release:        1%{?dist}
Summary:        Bink Video Player

License:        Free for no-commercial use, no modification permitted
URL:            http://www.radgametools.com/bnkmain.htm
Source0:        http://www.radgametools.com/down/Bink/%{pkgname}.7z#/%{pkgname}-%{version}.7z
Source1:        LICENSE
Source2:        http://www.radgametools.com/images/bink.jpg

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  p7zip
Requires:       hicolor-icon-theme


%description
Bink player to play Bink files (or compiled Bink EXE files) from the
command line.


%prep
%autosetup -c

RVER="$(strings BinkPlayer%{?binbits} | grep -F 'Bink Video V' |awk '{print $4}' | cut -d'/' -f1 )"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch. You have ${RVER} in %{S:0} instead %{version} "
  echo "Edit Version and try again"
  exit 1
fi

cp -p %{S:1} .

convert \
  %{S:2} -resize 96x96 \
  -background white -gravity center -extent 96x96 %{name}.png

cat > %{name}.desktop <<'EOF'
[Desktop Entry]
Name=Bink Player
Comment=Play BINK video files
Exec=%{name}
Icon=%{name}
MimeType=video/x-binkvideo;
Terminal=false
Type=Application
Categories=AudioVideo;
NoDisplay=true
EOF


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 BinkPlayer%{?binbits} %{buildroot}%{_bindir}/%{name}

chrpath --delete %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
install -pm0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/

for res in 16 22 24 32 48 64 72 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick %{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
# Mime file modified from https://aur.archlinux.org/packages/binkplayer
cat >> %{buildroot}%{_datadir}/mime/packages/%{name}.xml <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="video/x-binkvideo">
    <comment>Bink Video File</comment>
    <generic-icon name="video-x-generic"/>
    <glob pattern="*.bk2"/>
    <glob pattern="*.bik"/>
  </mime-type>
</mime-info>
EOF


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/mime/packages/*.xml


%changelog
* Wed Mar 19 2025 - 2025.01-1
- 2025.01

* Thu Sep 19 2024 - 2024.05-1
- 2024.05

* Sat Sep 16 2023 - 2023.08-1
- 2023.08

* Thu Jul 28 2022 - 2022.05-1
- 2022.05

* Tue Apr 05 2022 - 2022.03-1
- 2022.03

* Mon Apr 19 2021 - 2021.03-1
- 2021.03

* Wed Sep 30 2020 - 2020.09-1
- 2020.09

* Thu Mar 19 2020 - 2.7i-2
- BR: p7zip

* Tue Sep  4 2018 - 2.7d-1
- Initial spec
