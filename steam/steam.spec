# Binary package, no debuginfo should be generated
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

# If firewalld macro is not defined, define it here:
%{!?firewalld_reload:%global firewalld_reload test -f /usr/bin/firewall-cmd && firewall-cmd --reload --quiet || :}

Name:           steam
Version:        1.0.0.61
Epoch:          1
Release:        103%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file
License:        Steam License Agreement
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        http://repo.steampowered.com/%{name}/pool/%{name}/s/%{name}/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source4:        %{name}.appdata.xml

# Ghost touches in Big Picture mode:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist

# Input devices seen as joysticks:
Source6:        https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/after_kernel_4_9/51-these-are-not-joysticks-rm.rules

Source10:       README.Fedora

# Updated UDEV rules
Patch0:         %{name}-udev-rules-update.patch

# Remove libstdc++ from runtime:
# https://github.com/ValveSoftware/steam-for-linux/issues/3273
Patch1: %{name}-3273.patch

# Disable desktop files installation on desktop and create logs on user directory
Patch3:         %{name}-launcher.patch

# From Arch: Set alsa SDL audiodriver if pulseaudio is not installed
Patch4:         https://git.archlinux.org/svntogit/community.git/plain/trunk/alsa_sdl_audiodriver.patch?h=packages/%{name}#/alsa_sdl_audiodriver.patch

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

Requires:       gamemode
Requires:       gamemode%{?_isa}

Provides:       steam-noruntime = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      steam-noruntime < %{?epoch:%{epoch}:}%{version}-%{release}

%description
Installer for the Steam software distribution service.
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1

sed -i 's/\r$//' %{name}.desktop
sed -i 's/\r$//' steam_subscriber_agreement.txt

cp %{SOURCE10} .

%build
# Nothing to build

%install
%make_install

rm -fr %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

mkdir -p %{buildroot}%{_udevrulesdir}/
install -m 644 -p lib/udev/rules.d/* \
    %{SOURCE6} %{buildroot}%{_udevrulesdir}/

desktop-file-edit \
  --remove-category="Network" \
  --remove-category="FileTransfer" \
  %{buildroot}/%{_datadir}/applications/%{name}.desktop

ln -sf ../icons/hicolor/48x48/apps/steam.png \
  %{buildroot}/%{_datadir}/pixmaps/%{name}_tray_mono.png

# Environment files
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

# Install AppData
mkdir -p %{buildroot}%{_metainfodir}
install -p -m 0644 %{SOURCE4} %{buildroot}%{_metainfodir}/


%files
%{!?_licensedir:%global license %%doc}
%license COPYING steam_subscriber_agreement.txt
%doc README debian/changelog README.Fedora
%{_bindir}/%{name}
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%{_udevrulesdir}/*


%changelog
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

* Thu Dec 01 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-1
- Update to 1.0.0.54.
- Update udev patch.

* Wed Oct 26 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.53-1
- Update to 1.0.0.53.
- Update udev rules.

* Sat Sep 24 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.52-3
- Do not run update-desktop-database on Fedora 25+.
- Add AppStream metadata.

* Sat Aug 13 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.52-2
- Make Steam Controller usable as a gamepad (#4062).
- Update UDev rule for keyboards detected as joysticks.
- Update README.Fedora file with notes about the Steam Controller, its update
  process and update the list of devices with UDev rules.

* Fri Apr 01 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.52-1
- Update to 1.0.0.52, adds HTC Vive udev rules.
- Update patches.

* Thu Feb 25 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.51-2
- Integrate FirewallD rules (still not enabled by default).
- Add support for Nvidia Shield Controller.
- Add UDev rules for keyboards detected as joysticks:
  https://github.com/ValveSoftware/steam-for-linux/issues/3384
  https://bugzilla.kernel.org/show_bug.cgi?id=28912
  https://github.com/denilsonsa/udev-joystick-blacklist
- Update README.Fedora accordingly.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.51-1
- Update to 1.0.0.51.
- Add dependencies for In-Home Streaming decoding.
- Updated udev rules for the Steam Controller and HTC Vive VR headset.
- Update isa requirements.

* Mon May 25 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.50-2
- Add license macro.
- Add workaround for bug 3273, required for running client/games with prime:
  https://github.com/ValveSoftware/steam-for-linux/issues/3273

* Thu May 07 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.50-1
- Update to 1.0.0.50.
- Add new requirements; update README file.

* Mon Jan 12 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-4
- Flash plugin is no longer required for playing videos in the store, update
  README.Fedora.

* Thu Jan 08 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-3
- Workaround for bug 3570:
  https://github.com/ValveSoftware/steam-for-linux/issues/3570

* Tue Dec 02 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-2
- Update requirements.

* Wed Aug 27 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-1
- Update to 1.0.0.49.

* Tue Jul 29 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.48-3
- Obsolete noruntime subpackage.

* Mon Jun 23 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.48-2
- Add additional libraries required by games when skipping runtime.

* Thu Jun 19 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.48-1
- Update to 1.0.0.48.

* Thu May 15 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-4
- Update noruntime subpackage requirements.

* Mon May 05 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-3
- Add new libbz2.so requirement.

* Tue Apr 01 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-2
- Close window when clicking the x button (#3210).

* Wed Feb 12 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-1
- Update to 1.0.0.47.

* Mon Jan 06 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-6
- Make noruntime subpackage noarch.

* Mon Jan 06 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-5
- Update README.Fedora with new instructions.

* Mon Jan 06 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-4
- Create a no-runtime subpackage leaving the main package to behave as intended
  by Valve. All the Steam Runtime dependencies are against the subpackage.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-3
- Additional system libraries required by games.

* Fri Dec 20 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-2
- If STEAM_RUNTIME is not set, perform the following actions by default from the
  main commmand:
    Disable the Ubuntu runtime.
    Delete the unpacked Ubuntu runtime.
    Create the obsolete libudev.so.0.

* Wed Nov 27 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-1
- Update to 1.0.0.45.

* Thu Nov 14 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.44-1
- Update to 1.0.0.44.

* Fri Nov 08 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-9
- Disable STEAM_RUNTIME, drop all requirements and change README.Fedora. Please
  see for details:
    https://github.com/ValveSoftware/steam-for-linux/issues/2972
    https://github.com/ValveSoftware/steam-for-linux/issues/2976
    https://github.com/ValveSoftware/steam-for-linux/issues/2978

* Mon Nov 04 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-8
- Add missing mesa-dri-drivers requirement.

* Mon Oct 28 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-7
- Added libXScrnSaver to requirements.

* Wed Oct 23 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-6
- Rpmlint review fixes.

* Wed Oct 23 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-5
- Do not remove buildroot in install section.
- Update desktop database after installation/uninstallation.

* Tue Oct 22 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-4
- Added systemd build requirement for udev rules.

* Sun Oct 20 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-3
- Add alsa-plugins-pulseaudio to requirements.
- Add libappindicator to requirements to enable system tray icon.

* Thu Oct 10 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-2
- Remove requirements pulled in by other components.

* Wed Oct 09 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-1
- Update to 1.0.0.43.

* Thu Oct 03 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.42-2
- Remove rpmfusion repository dependency.

* Wed Sep 11 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.42-1
- Update to 1.0.0.42.

* Sun Sep 08 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.41-1
- Update to 1.0.0.41.

* Thu Aug 29 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.40-1
- Update to 1.0.0.40.
- Add Steam controller support.

* Sun Aug 18 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-5
- Rework requirements section.
- Add tar and zenity requirements for initial setup.

* Mon Aug 05 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-4
- Remove Fedora 17 as it is now EOL.

* Wed May 29 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-3
- Add STEAM_RUNTIME=0 to profile settings.

* Mon May 13 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-2
- Added NetworkManager requirement for STEAM_RUNTIME=0.

* Mon May 13 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-1
- Updated to 1.0.0.39.

* Thu May 09 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.38-2
- Changed Fedora 19 FLAC requirements.

* Sun Apr 28 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.38-1
- Updated to 1.0.0.38.

* Fri Apr 19 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.36-2
- Add additional libraries for starting with STEAM_RUNTIME=0.
- Added README.Fedora document with additional instructions.

* Fri Mar 15 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.36-1
- Update to 1.0.0.36.

* Mon Mar 04 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.35-1
- Updated.

* Mon Feb 25 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.34-1
- Update to 1.0.0.34.

* Thu Feb 21 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.29-2
- Added changelog to docs.

* Thu Feb 21 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.29-1
- Updated.

* Fri Feb 15 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.27-1
- Updated, used official install script.
- Removed patch.

* Mon Feb 11 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.25-1
- Updated to 1.0.0.25.
- Reworked installation for new tar package.
- Used official docs.

* Tue Jan 22 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.22-3
- Moved documents to the default document directory.
- Use internal license file instead of provided one.
- Removed STEAMSCRIPT modification, fixed in 1.0.0.22.

* Tue Jan 22 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.22-1
- Updated.

* Thu Jan 17 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.21-2
- Sorted Requires.
- Fix STEAMSCRIPT_VERSION.
- Added RPMFusion free repository as requirement for libtxc_dxtn (or nvidia drivers...).

* Thu Jan 17 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.21-1
- Updated version, patch and tarball generation for 1.0.0.21.
- Added libtxc_dxtn requirement (rpmfusion).
- Replaced steam with %%{name} where it fits.
- Removed jpeg library hack.
- Removed SDL2 requirement, is downloaded by the client.
- Replace (x86-32) with %%{_isa}.

* Tue Jan 8 2013 Tom Callaway <spot@fedoraproject.org> - 1.0.0.18-1
- update to 1.0.0.18

* Wed Nov 7 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0.14-3
- add more Requires (from downloaded bits, not packaged bits)

* Tue Nov 6 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0.14-2
- fedora specific libpng conditionalization

* Tue Nov 6 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0.14-1
- initial Fedora RPM packaging
