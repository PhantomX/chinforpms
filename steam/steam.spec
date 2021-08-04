# Binary package, no debuginfo should be generated
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global udev_id 8a3f1a0e2d208b670aafd5d65e216c71f75f1684

# If firewalld macro is not defined, define it here:
%{!?firewalld_reload:%global firewalld_reload test -f /usr/bin/firewall-cmd && firewall-cmd --reload --quiet || :}

Name:           steam
Version:        1.0.0.71
Epoch:          1
Release:        100%{?dist}
Summary:        Installer for the Steam software distribution service

# Redistribution and repackaging for Linux is allowed, see license file. udev rules are MIT.
License:        Steam License Agreement and MIT
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        http://repo.steampowered.com/%{name}/pool/%{name}/s/%{name}/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source5:        README.Fedora

# Ghost touches in Big Picture mode:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist

# Input devices seen as joysticks:
Source6:        https://github.com/denilsonsa/udev-joystick-blacklist/raw/4c23cd2044ce4ac562ede5aac500bbc9f7a0e9ca/after_kernel_4_9/51-these-are-not-joysticks-rm.rules

# Configure limits in systemd
Source7:        01-steam.conf

# Newer UDEV rules
Source10:       https://github.com/ValveSoftware/steam-devices/raw/%{udev_id}/60-steam-input.rules
Source11:       https://github.com/ValveSoftware/steam-devices/raw/%{udev_id}/60-steam-vr.rules

# Do not install desktop file in lib/steam, do not install apt sources
Patch0:         %{name}-makefile.patch
# Do not try to copy steam.desktop to the user's desktop from lib/steam
Patch1:         %{name}-no-icon-on-desktop.patch

# Create stdout logs on user directory
Patch10:         %{name}-log-stdout-to-file.patch

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  systemd

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

# Minimum requirements for starting the steam client for the first time
Requires:       alsa-lib%{?_isa}
Requires:       gtk2%{?_isa}
Requires:       libnsl%{?_isa}
Requires:       libxcrypt-compat%{?_isa}
Requires:       libpng12%{?_isa}
Requires:       libXext%{?_isa}
Requires:       libXinerama%{?_isa}
Requires:       libXtst%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       mesa-libGL%{?_isa} >= 17.2.2-2
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

# Required for hardware decoding during In-Home Streaming (intel)
%if (0%{?fedora} && 0%{?fedora} < 28)
Requires:       libva-intel-driver%{?_isa}
%else
Requires:       libva%{?_isa}
%endif

# Required for hardware decoding during In-Home Streaming (radeon/nouveau)
Requires:       libvdpau%{?_isa}

# Required for having a functioning menu on the tray icon
Requires:       libdbusmenu-gtk3%{?_isa} >= 16.04.0

# Required by Feral interactive games
Requires:       libatomic%{?_isa}

# Required by Shank
Requires:       alsa-plugins-pulseaudio%{?_isa}

Recommends:     gamemode
Recommends:     gamemode%{?_isa}
Recommends:     (gnome-shell-extension-gamemode if gnome-shell)

# Proton uses xdg-desktop-portal to open URLs from inside a container
Requires:       xdg-desktop-portal
Recommends:     (xdg-desktop-portal-gtk if gnome-shell)
Recommends:     (xdg-desktop-portal-kde if kwin)

Requires:       steam-devices = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       steam-noruntime = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      steam-noruntime < %{?epoch:%{epoch}:}%{version}-%{release}

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


%files
%{!?_licensedir:%global license %%doc}
%license COPYING steam_subscriber_agreement.txt
%doc debian/changelog README.Fedora
%{_bindir}/%{name}
%{_metainfodir}/*.metainfo.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%dir %{_prefix}/lib/systemd/system.conf.d/
%{_prefix}/lib/systemd/system.conf.d/01-steam.conf
%dir %{_prefix}/lib/systemd/user.conf.d/
%{_prefix}/lib/systemd/user.conf.d/01-steam.conf


%files devices
%{_udevrulesdir}/*


%changelog
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
