%global debug_package %{nil}

Name:           lutris
Version:        0.5.2
Epoch:          1
Release:        100%{?dist}
Summary:        Install and play any video game easily

License:        GPLv3
URL:            https://lutris.net

Source0:        https://github.com/lutris/lutris/archive/v%{version}/%{name}-%{version}.tar.gz
# Configure limits in systemd
# This should be only needed with systemd < 240
Source1:        02-%{name}.conf

Patch0:         %{name}-no-gtk-update-icon-cache.patch
Patch1:         %{name}-gamemodelib.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gtk3
BuildRequires:  python3-devel
BuildRequires:  python3-evdev
BuildRequires:  python3-gobject
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  fdupes
Requires:       hicolor-icon-theme
Requires:       cabextract
Requires:       curl
Requires:       fluidsynth
Requires:       glx-utils
Requires:       gamemode
Requires:       gnome-desktop3
Requires:       gtk3
Requires:       gvfs
Requires:       libnotify
Requires:       libstrangle
Requires:       psmisc
Requires:       p7zip
Requires:       p7zip-plugins
Requires:       pciutils
Requires:       python3-evdev
Requires:       python3-gobject-base
Requires:       python3-gobject
Requires:       python3-PyYAML
Requires:       python3-requests
Requires:       unzip
Requires:       vulkan-tools
Requires:       xorg-x11-server-Xephyr
Requires:       xorg-x11-server-utils
Requires:       webkit2gtk3
Recommends:     fluid-soundfont-gs
Recommends:     xboxdrv
Recommends:     wine
Suggests:       steam


%ifarch x86_64
Requires:       gamemode(x86-32)
Requires:       libstrangle(x86-32)
Requires:       mesa-dri-drivers(x86-32)
Requires:       mesa-vulkan-drivers(x86-32)
Requires:       vulkan-loader(x86-32)
Requires:       libglvnd-glx(x86-32)
%endif


%description
Lutris is a gaming platform for GNU/Linux. Its goal is to make
gaming on Linux as easy as possible by taking care of installing
and setting up the game for the user. The only thing you have to
do is play the game. It aims to support every game that is playable
on Linux.

%prep
%autosetup -p1


%build
%py3_build


%install
%py3_install

rm -f %{buildroot}%{_datadir}/polkit-1/actions/net.lutris.xboxdrv*

%fdupes %{buildroot}%{python3_sitelib}

desktop-file-validate %{buildroot}%{_datadir}/applications/net.lutris.Lutris.desktop

# Systemd configuration
%if 0%{?fedora} && 0%{?fedora} < 30
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
install -m 644 -p %{S:1} %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -m 644 -p %{S:1} %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
%endif


%files
%license LICENSE
%doc AUTHORS README.rst
%{_bindir}/%{name}*
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/polkit-1/actions/*.policy
%{python3_sitelib}/%{name}-*.egg-info
%{python3_sitelib}/%{name}/
%{_metainfodir}/*.appdata.xml
%if 0%{?fedora} && 0%{?fedora} < 30
%{_prefix}/lib/systemd/system.conf.d/02-%{name}.conf
%{_prefix}/lib/systemd/user.conf.d/02-%{name}.conf
%endif


%changelog
* Tue Apr 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.5.2-100
- 0.5.2

* Thu Mar 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.5.1.2-100
- 0.5.1.2

* Sat Mar 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.5.1-100
- 0.5.1

* Mon Feb 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.5.0.1-100
- 0.5.0.1
- Drop noarch, needed for better dependencies
- R: gamemode
- R: libstrangle

* Sat Feb 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.5.0-100
- 0.5.0
- Pump requirements

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.4.23-101
- systemd file descriptor limit files
- Sync NOFILE with systemd defaults

* Thu Nov 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:0.4.23-100.chinfo
- 0.4.23

* Thu Nov 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:0.4.22-1
- 0.4.22

* Mon Oct 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:0.4.21-1
- 0.4.21

* Fri Oct 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:0.4.20-1
- 0.4.20

* Mon Sep 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.4.19-5
- chinforpms cleanup

* Tue Nov 29 2016 Mathieu Comandon <strycore@gmail.com> - 0.4.3
- Ensure correct Python3 dependencies
- Set up Python macros for building (Thanks to Pharaoh_Atem on #opensuse-buildservice)

* Sat Oct 15 2016 Mathieu Comandon <strycore@gmail.com> - 0.4.0
- Update to Python 3
- Bump version to 0.4.0

* Sat Dec 12 2015 Rémi Verschelde <akien@mageia.org> - 0.3.7-2
- Remove ownership of system directories
- Spec file cleanup

* Fri Nov 27 2015 Mathieu Comandon <strycore@gmail.com> - 0.3.7-1
- Bump to version 0.3.7

* Thu Oct 30 2014 Mathieu Comandon <strycore@gmail.com> - 0.3.6-1
- Bump to version 0.3.6
- Add OpenSuse compatibility (contribution by @malkavi)

* Fri Sep 12 2014 Mathieu Comandon <strycore@gmail.com> - 0.3.5-1
- Bump version to 0.3.5

* Thu Aug 14 2014 Travis Nickles <nickles.travis@gmail.com> - 0.3.4-3
- Edited Requires to include pygobject3.

* Wed Jun 04 2014 Travis Nickles <nickles.travis@gmail.com> - 0.3.4-2
- Changed build and install step based on template generated by
  rpmdev-newspec.
- Added Requires.
- Ensure package can be built using mock.

* Tue Jun 03 2014 Travis Nickles <nickles.travis@gmail.com> - 0.3.4-1
- Initial version of the package
