Name:           steamtinkerlaunch
Version:        2.4.1
Release:        1%{?dist}
Summary:        Wrapper script for Steam custom launch options

License:        GPLv3
URL:            https://github.com/frostworx/steamtinkerlaunch

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       bash
Requires:       git
Requires:       wget
Requires:       wmctrl
Requires:       xdotool
# xprop, xwininfo
Requires:       xorg-x11-utils
# xrandr
Requires:       xorg-x11-server-utils
Requires:       unzip
Requires:       yad >= 7.0
Recommends:     zenity
Recommends:     boxtron
Recommends:     cabextract
Recommends:     gameconqueror
Recommends:     gamemode
Recommends:     gamescope
Recommends:     libnotify
Recommends:     mangohud
Recommends:     net-tools
Recommends:     nyrna
Recommends:     replay-sorcery
Recommends:     scummvm
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
install -pm0755 stl %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/stl
cp -r categories lang misc regs tweaks %{buildroot}%{_datadir}/stl/


%files
%license LICENSE
%doc README.md
%{_bindir}/stl
%{_datadir}/stl

%changelog
* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 2.4.1-1
- Initial spec
