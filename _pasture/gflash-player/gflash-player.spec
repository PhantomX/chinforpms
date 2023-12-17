# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global binname gflashplayer

Name:           gflash-player
Version:        32.0.0.465
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
# dlopen
# libasound.so.2
Requires:       alsa-lib%{?_isa}
# libcurl.so.4
Requires:       libcurl%{?_isa}
# libvdpau.so.1
Requires:       libvdpau%{?_isa}
# libpulse.so.0
Requires:       pulseaudio-libs%{?_isa}
# libudev.so.1
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

cat > %{binname}.desktop <<'EOF'
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


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 flashplayer %{buildroot}%{_bindir}/%{binname}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{binname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 %{S:1} \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{binname}.png

for res in 16 22 24 32 36 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{S:1} -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{binname}.png
done

install -pm0644 %{S:2} %{buildroot}%{_datadir}/icons/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license license.pdf LGPL/*.txt
%{_bindir}/%{binname}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/*.xpm
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Thu Dec 10 2020 - 32.0.0.465-1
- 32.0.0.465

* Wed Sep 30 2020 - 32.0.0.433-1
- 32.0.0.433

* Tue Jul 14 2020 - 32.0.0.403-1
- 32.0.0.403

* Thu Mar 19 2020 - 32.0.0.344-1
- 32.0.0.344

* Thu Nov 21 2019 - 32.0.0.293-1
- 32.0.0.293

* Mon Aug 19 2019 - 32.0.0.238-1
- 32.0.0.238

* Fri Feb 15 2019 - 32.0.0.142-1
- 32.0.0.142

* Wed Nov 21 2018 - 31.0.0.108-1
- 31.0.0.153
- Document explicit Requires

* Fri Sep 14 2018 - 31.0.0.108-1
- 31.0.0.108

* Fri Jun 08 2018 - 30.0.0.113-1
- 30.0.0.113

* Sat May 19 2018 - 29.0.0.171-1
- Initial spec
