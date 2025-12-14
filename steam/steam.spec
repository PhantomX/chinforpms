# Binary package, no debuginfo should be generated
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global appstream_id com.valvesoftware.Steam

%global udev_id e2971e45063f6b327ccedbf18e168bda6749155c

# If firewalld macro is not defined, define it here:
%{!?firewalld_reload:%global firewalld_reload test -f /usr/bin/firewall-cmd && firewall-cmd --reload --quiet || :}

Name:           steam
Version:        1.0.0.85
Epoch:          1
Release:        100%{?dist}
Summary:        Installer for the Steam software distribution service

# Redistribution and repackaging for Linux is allowed, see license file. udev rules are MIT.
License:        LicenseRef-Steam-License-Agreement AND MIT
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        https://repo.steampowered.com/%{name}/archive/beta/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source5:        README.Fedora

# Ghost touches in Big Picture mode:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist

# Input devices seen as joysticks:
Source6:        https://github.com/denilsonsa/udev-joystick-blacklist/raw/a1ace571823be5979c135e9cb8e9ae103c7641ac/after_kernel_4_9/51-these-are-not-joysticks-rm.rules

# Configure limits in systemd
Source7:        01-steam.conf

# Newer UDEV rules
Source10:       https://github.com/ValveSoftware/steam-devices/raw/%{udev_id}/60-steam-input.rules
Source11:       https://github.com/ValveSoftware/steam-devices/raw/%{udev_id}/60-steam-vr.rules

# Do not install desktop file in lib/steam, do not install apt sources
Patch0:         %{name}-makefile.patch
# Do not try to copy steam.desktop to the user's desktop from lib/steam
Patch1:         %{name}-no-icon-on-desktop.patch


BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  systemd

BuildRequires:  libappstream-glib

# Required to run the initial setup
Requires:       tar
Requires:       zenity

# Most games use OpenGL, some games already use Vulkan. Vulkan is also required
# for Steam Play to run Windows games through emulation. i686 version of these
# packages are necessary even on x86_64 systems for running 32bit games. Pull in
# native arch drivers as well, by not specifying _isa macro, native arch
# packages are preferred. This will make sure people have all necessary drivers
# for both i686 and x86_64 games.
Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-dri-drivers
Requires:       mesa-vulkan-drivers%{?_isa}
Requires:       mesa-vulkan-drivers
Requires:       vulkan-loader%{?_isa}
Requires:       vulkan-loader

# Minimum requirements for starting the steam client using system libraries
Requires:       alsa-lib%{?_isa}
Requires:       fontconfig%{?_isa}
Requires:       gtk2%{?_isa}
Requires:       libICE%{?_isa}
Requires:       libnsl%{?_isa}
Requires:       libxcrypt-compat%{?_isa}
Requires:       libpng12%{?_isa}
Requires:       libXext%{?_isa}
Requires:       libXinerama%{?_isa}
Requires:       libXtst%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       mesa-libGL%{?_isa} >= 17.2.2-2
Requires:       NetworkManager-libnm%{?_isa}
Requires:       nss%{?_isa}
Requires:       pulseaudio-libs%{?_isa}
Requires:       SDL2%{?_isa}

# Required for sending out crash reports to Valve
Requires:       libcurl%{?_isa}

# Workaround for mesa-libGL dependency bug:
# https://bugzilla.redhat.com/show_bug.cgi?id=1168475
Requires:       systemd-libs%{?_isa}

# Required for the firewall rules
# http://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem

# Required for hardware encoding/decoding during Remote Play (intel/radeon/amdgpu/nouveau)
Requires:       libva%{?_isa}
Requires:       libvdpau%{?_isa}

# Required for having a functioning menu on the tray icon
Requires:       libdbusmenu-gtk3%{?_isa} >= 16.04.0

# Required by Feral interactive games
Requires:       libatomic%{?_isa}

# Required by Shank
Requires:       (alsa-plugins-pulseaudio%{?_isa} if pulseaudio)
Requires:       (pipewire-alsa%{?_isa} if pipewire)

Recommends:     gamemode
Recommends:     gamemode%{?_isa}
Recommends:     (gnome-shell-extension-gamemode if gnome-shell)
Recommends:     (gnome-shell-extension-appindicator if gnome-shell)

# Proton uses xdg-desktop-portal to open URLs from inside a container
Requires:       xdg-desktop-portal
Recommends:     (xdg-desktop-portal-gtk if gnome-shell)
Recommends:     (xdg-desktop-portal-kde if kwin)

# Prevent log spam when these are not pulled in as dependencies of full desktops
Recommends:     dbus-x11
Recommends:     xdg-user-dirs

# Allow using Steam Runtime Launch Options
Recommends:     gobject-introspection

# Automatic loading of the ntsync module
Recommends:     ntsync-autoload

Requires:       steam-devices = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

This package contains the installer for the Steam software distribution service.


%package        devices
Summary:        Permissions required by Steam for gaming devices

%description    devices
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

This package contains the necessary permissions for gaming devices.


%prep
%autosetup -n %{name}-launcher -p1

cp %{SOURCE5} .

%build
# Nothing to build

%install
%make_install

rm -f %{buildroot}%{_bindir}/%{name}
ln -s \
  $(realpath -m --relative-to="%{_bindir}" "%{_libdir}/%{name}")/bin_steam.sh \
  %{buildroot}%{_bindir}/%{name}

rm -fr %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

mkdir -p %{buildroot}%{_udevrulesdir}/
install -m 644 -p %{SOURCE10} %{SOURCE11} %{SOURCE6} \
    %{buildroot}%{_udevrulesdir}/

desktop-file-edit \
  --remove-category="Network" \
  --remove-category="FileTransfer" \
  %{buildroot}/%{_datadir}/applications/%{name}.desktop

ln -sf ../icons/hicolor/48x48/apps/steam.png \
  %{buildroot}/%{_datadir}/pixmaps/%{name}_tray_mono.png

# Environment files
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

# Raise file descriptor limit
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/user.conf.d/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%files
%{!?_licensedir:%global license %%doc}
%license COPYING steam_subscriber_agreement.txt
%doc debian/changelog README.Fedora
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_metainfodir}/%{appstream_id}.metainfo.xml
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%dir %{_prefix}/lib/systemd/system.conf.d/
%{_prefix}/lib/systemd/system.conf.d/01-steam.conf
%dir %{_prefix}/lib/systemd/user.conf.d/
%{_prefix}/lib/systemd/user.conf.d/01-steam.conf


%files devices
%{_udevrulesdir}/*


%changelog
* Mon Oct 06 2025 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.85-100
- 1.0.0.85

* Wed Sep 17 2025 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.84-100
- 1.0.0.84

* Tue May 13 2025 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.83-100
- 1.0.0.83

* Fri Nov 29 2024 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.82-100
- 1.0.0.82

* Sat Sep 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.81-100
- 1.0.0.81

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.79-100
- 1.0.0.79

* Tue May 30 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.78-100
- 1.0.0.78

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.76-100
- 1.0.0.76

* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.75-100
- 1.0.0.75

* Thu Feb 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.74-100
- 1.0.0.74

* Fri Nov 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.73-100
- 1.0.0.73

* Tue Oct 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.72-100
- 1.0.0.72
- RPMFusion sync

* Tue Aug 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.71-100
- 1.0.0.71
- RPMFusion sync

* Sun Apr 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.70-100
- 1.0.0.70

* Sat Dec 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.68-100
- 1.0.0.68
- RPMFusion sync

* Mon Nov 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.67-100
- 1.0.0.67

* Mon Aug 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.66-100
- 1.0.0.66

* Tue Jul 14 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.64-100
- 1.0.0.64

* Mon Jun 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.63-100
- 1.0.0.63
- RPMFusion sync

* Sat May 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.62-101
- Add forgotten stdout log patch

* Thu May 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.62-100
- 1.0.0.62
- RPMFusion sync

* Sun Feb 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.61-103
- RPMFusion sync

* Sun Sep 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.61-102
- Remove unneeded firewalld file

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.61-101
- Remove limits files

* Wed Aug 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.61-100
- 1.0.0.61

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.59-101
- Update NOFILE limits

* Tue Dec 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.59-100
- 1.0.0.59
- RPMFusion sync

* Tue Oct 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.56-100.chinfo
- 1.0.0.56
- RPMFusion sync

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.54-103
- Sync with rpmfusion.

* Sun Oct 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.54-102
- Remove libtxc_dxtn requires

* Sun Jun 11 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.54-101
- Sync with rpmfusion.

* Fri Apr 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.54-100
- Sync with rpmfusion.
- Remove libstdc++ patch.
- Update udev rules.
- Update docs for hardware encoding/decoding information.

* Wed Jan 11 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.0.54-4
- Sync with rpmfusion.

* Wed Jan 04 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.0.54-3
- Patches updates.
- Disable desktop files installation on desktop.
- Create logs on user directory.
- R: SDL2
- Remove extraneous categories from desktop file.
- Use the good colorful notification icon.

* Tue Dec 13 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-2
- Re-add close functionality to X window button (#3210).
