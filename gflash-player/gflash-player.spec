%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global binname gflashplayer

Name:           gflash-player
Version:        29.0.0.171
Release:        1%{?dist}
Summary:        Adobe Flash Player Projector

License:        Non-redistributable, no modification permitted
URL:            http://get.adobe.com/flashplayer/
# https://www.adobe.com/support/flashplayer/debug_downloads.html
Source0:        https://fpdownload.macromedia.com/pub/flashplayer/updaters/%(echo %{version} | cut -d . -f1)/flash_player_sa_linux.x86_64.tar.gz#/flash_player_sa_linux_%{version}.x86_64.tar.gz
Source1:        %{binname}.png
Source2:        %{binname}128.xpm

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Requires:       alsa-lib%{?_isa}
Requires:       libcurl%{?_isa}
Requires:       libvdpau%{?_isa}
Requires:       pulseaudio-libs%{?_isa}
Requires:       systemd-libs%{?_isa}
Requires:       hicolor-icon-theme

%description
The Adobe Flash Player Projector is a freeware for viewing multimedia content
created on the Adobe Flash platform.


%prep
%autosetup -c

RVER="$(strings flashplayer |grep '^\[@LNX' | awk '{print $2}' | tr , . )"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch. You have ${RVER} in %{S:0} instead %{version} "
  echo "Edit Version and try again"
  exit 1
fi

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 flashplayer %{buildroot}%{_bindir}/%{binname}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{binname}.desktop <<EOF
[Desktop Entry]
Name=Adobe Flash Player Projector
Type=Application
Comment=Flash Movie Player
Exec=%{binname}
Icon=%{binname}
MimeType=application/x-shockwave-flash;
Terminal=false
Categories=GTK;AudioVideo;
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{S:1} \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{binname}.png

for res in 16 20 22 24 32 36 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{S:1} -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{binname}.png
done

install -pm0644 %{S:2} %{buildroot}%{_datadir}/icons/

desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license license.pdf LGPL/*.txt
%{_bindir}/%{binname}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/*.xpm
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Sat May 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 29.0.0.171-1
- Initial spec