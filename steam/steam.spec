# Binary package, no debuginfo should be generated
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global appstream_id com.valvesoftware.Steam

# If firewalld macro is not defined, define it here:
%{!?firewalld_reload:%global firewalld_reload test -f /usr/bin/firewall-cmd && firewall-cmd --reload --quiet || :}

Name:           steam
Version:        1.0.0.85
Epoch:          1
Release:        102%{?dist}
Summary:        Installer for the Steam software distribution service

# Redistribution and repackaging for Linux is allowed, see license file. udev rules are MIT.
License:        LicenseRef-Steam-License-Agreement AND MIT
URL:            http://www.steampowered.com/
ExclusiveArch:  x86_64

Source0:        https://repo.steampowered.com/%{name}/archive/beta/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source5:        README.Fedora

# Ghost touches in Big Picture mode:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist

# Configure limits in systemd
Source7:        01-steam.conf


# Do not install desktop file in lib/steam, do not install apt sources
Patch0:         %{name}-makefile.patch
# Do not try to copy steam.desktop to the user's desktop from lib/steam
Patch1:         %{name}-no-icon-on-desktop.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  systemd

# Required for the basic runtime
Requires:       glibc(x86-32)
Requires:       libdrm(x86-32)
Requires:       libglvnd-glx(x86-32)
Requires:       libnsl(x86-32)

# Required to run the initial setup
Requires:       tar
Requires:       zenity
Requires:       xz

# Required for basic gaming, also for native 32 bit games:
Requires:       mesa-dri-drivers
Requires:       mesa-dri-drivers(x86-32)
Requires:       mesa-vulkan-drivers
Requires:       mesa-vulkan-drivers(x86-32)
Requires:       vulkan-loader
Requires:       vulkan-loader(x86-32)

# Hardware stuff (permissions on devices, hardware updater, etc.):
Requires:       steam-devices

# These libraries are also part of the Ubuntu runtime at:
#   ~/.local/share/Steam/ubuntu12_32
#   ~/.local/share/Steam/ubuntu12_64
# Steam client uses the system ones if available; so override where there is a
# benefit using the native system libraries or just to match when the native 64
# bit packages are already installed.
Requires:       bzip2-libs
Requires:       bzip2-libs(x86-32)
Requires:       fontconfig
Requires:       fontconfig(x86-32)
Requires:       libICE
Requires:       libICE(x86-32)
Requires:       libnsl
Requires:       libnsl(x86-32)
Requires:       libXext
Requires:       libXext(x86-32)
Requires:       libXinerama
Requires:       libXinerama(x86-32)
Requires:       libXtst
Requires:       libXtst(x86-32)
Requires:       libva
Requires:       libva(x86-32)
Requires:       libvdpau
Requires:       libvdpau(x86-32)
Requires:       mesa-libGL
Requires:       mesa-libGL(x86-32)
Requires:       NetworkManager-libnm
Requires:       NetworkManager-libnm(x86-32)
Requires:       nss
Requires:       nss(x86-32)
Requires:       openal-soft
Requires:       openal-soft(x86-32)
Requires:       pipewire-libs
Requires:       pipewire-libs(x86-32)
Requires:       pulseaudio-libs
Requires:       pulseaudio-libs(x86-32)
%if 0%{?fedora}
Requires:       SDL3
Requires:       SDL3(x86-32)
%endif
# The client does not override only the ones linked at:
#   ~/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_32
#   ~/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_64
# At the moment of writing, the pinned ones belong to these packages:
#   gtk2
#   libcurl
#   libdbusmenu
#   libdbusmenu-gtk2
#   mesa-libGLU
# And yes, the "ubuntu12_32" directory twice above is not a typo. Windows style (system32...).

# Required for the firewall rules
# http://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem

# Required for hardware encoding/decoding during Remote Play (intel/radeon/amdgpu/nouveau)
Requires:       libva%{?_isa}
Requires:       libvdpau%{?_isa}

# Required by Feral interactive games
Requires:       libatomic
Requires:       libatomic(x86-32)

# Required by Shank
Requires:       (alsa-plugins-pulseaudio%{?_isa} if pulseaudio)

Recommends:     gamemode
Recommends:     gamemode(x86-32)
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


%description
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

This package contains the installer for the Steam software distribution service.

%package arch-transition
Summary: Transition package for migrating Steam from i686 to x86_64
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: steam = 1.0.0.85-100
Obsoletes: steam < 1.0.0.85-100
BuildArch: noarch

%description arch-transition
This package is used to migrate Steam installations from the
legacy i686 package layout to the x86_64 package layout.

It exists only to handle package replacement and dependency
changes during upgrades, and can be safely removed once the
transition is complete.

%prep
%autosetup -n %{name}-launcher -p1

cp %{SOURCE5} .

%build
# Nothing to build

%install
%make_install

rm -f %{buildroot}%{_bindir}/%{name}
ln -s \
  $(realpath -m --relative-to="%{_bindir}" "%{_prefix}/lib/%{name}")/bin_steam.sh \
  %{buildroot}%{_bindir}/%{name}

rm -fr %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

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
%{_prefix}/lib/%{name}/
%{_mandir}/man6/%{name}.*
%{_metainfodir}/%{appstream_id}.metainfo.xml
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%dir %{_prefix}/lib/systemd/system.conf.d/
%{_prefix}/lib/systemd/system.conf.d/01-steam.conf
%dir %{_prefix}/lib/systemd/user.conf.d/
%{_prefix}/lib/systemd/user.conf.d/01-steam.conf

%files arch-transition


%changelog
* Sun Jun 07 2026 Phantom X <megaphantomx at hotmail dot com> - 1:1.0.0.85-102
- RPMFusion sync

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
