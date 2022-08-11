Name:           steamtinkerlaunch
Version:        11.0
Release:        1%{?dist}
Summary:        Wrapper script for Steam custom launch options

License:        GPLv3
URL:            https://github.com/frostworx/steamtinkerlaunch

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  desktop-file-utils
Requires:       bash
Requires:       bc
Requires:       git
Requires:       wget
Requires:       wmctrl
Requires:       xdotool
Requires:       xprop
Requires:       xrandr
Requires:       xwininfo
Requires:       unzip
Requires:       yad >= 7.2
Recommends:     steam
Recommends:     boxtron
Recommends:     cabextract
Recommends:     gameconqueror
Recommends:     gamemode
Recommends:     gamescope
Recommends:     innoextract
Recommends:     jq
Recommends:     libnotify
Recommends:     mangohud
Recommends:     net-tools
Recommends:     nyrna
Recommends:     replay-sorcery
Recommends:     pev
Recommends:     scummvm
Recommends:     rsync
Recommends:     strace
Recommends:     usbutils
Recommends:     vkbasalt
Recommends:     vr-video-player
Recommends:     wine
Recommends:     winetricks
Recommends:     zenity


%description
SteamTinkerLaunch (short stl) is a Linux wrapper tool for use with the Steam
client which allows to customize and start tools and options for games quickly
on the fly.


%prep
%autosetup -p1


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r collections eval guicfgs lang misc %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  misc/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm0644 misc/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg


%changelog
* Wed Aug 10 2022 Phantom X <megaphantomx at hotmail dot com> - 11.0-1
- 11.0

* Thu Mar 03 2022 Phantom X <megaphantomx at hotmail dot com> - 9.2-1
- 9.2

* Mon Jan 17 2022 Phantom X <megaphantomx at hotmail dot com> - 9.0.1-1
- 9.0.1

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 6.15-1
- 6.15

* Thu Jun 10 2021 Phantom X <megaphantomx at hotmail dot com> - 6.8-1
- 6.8

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 4.0-1
- 4.0

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 2.4.1-1
- Initial spec
