%global commit d2780b67263a45143feaf08c05caa78b112c5d07
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250319
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           xboxdrv
Version:        0.8.14
Release:        1%{?dist}
Summary:        Userspace Xbox/Xbox360 Gamepad Driver for Linux

License:        GPL-3.0-or-later
URL:            https://github.com/xiota/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Source1:        %{name}.service
Source2:        %{name}-config.txt
# Better dbus support
# https://gist.github.com/saik0/11225735
Source3:        org.seul.Xboxdrv.conf
Source4:        org.seul.Xboxdrv.service
# Borrowed and modified from Lutris
Source5:        org.seul.xboxdrvctl.policy
Source6:        org.seul.xboxdrv.policy
# Gentoo
Source7:        %{name}.udev-rules

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3-devel
BuildRequires:  systemd
Requires:       python3-dbus
%{?systemd_requires}


%description
This is a Xbox/Xbox360 gamepad driver for Linux that works in userspace.
It is an alternative to the xpad kernel driver and has support for 
Xbox1 gamepads, Xbox360 USB gamepads and Xbox360 wireless gamepads, 
both first and third party.

%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

%py3_shebang_fix \
  examples/responsecurve-generator.py \
  xboxdrvctl

sed \
  -e "/find_program/s|'python'|'%{__python3}'|" \
  -i meson.build


%build
%meson
%meson_build

%install
%meson_install

rm -rf %{buildroot}%{_sysconfdir}/*
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_libdir}

# Install dbus rule
mkdir -p %{buildroot}%{_datadir}/dbus-1/system.d
install -pm 644 %{S:3} %{buildroot}%{_datadir}/dbus-1/system.d/

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -pm 644 %{S:2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -D -m 644 %{S:1} %{buildroot}%{_unitdir}/%{name}.service

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
install -pm0644 %{S:4} %{buildroot}%{_datadir}/dbus-1/system-services/

mkdir -p %{buildroot}%{_datadir}/polkit-1/actions
install -pm0644 %{S:5} %{S:6} %{buildroot}%{_datadir}/polkit-1/actions/

mkdir -p %{buildroot}%{_udevrulesdir}
install -pm0644 %{S:7} %{buildroot}%{_udevrulesdir}/99-xbox-controller.rules


%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service


%files
%doc PROTOCOL NEWS AUTHORS README.md examples
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}ctl
%{_mandir}/man1/%{name}*
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/*.policy
%{_udevrulesdir}/99-xbox-controller.rules


%changelog
* Sun Jul 20 2025 Phantom X <megaphantomx at hotmail dot com> - 0.8.14-1.20250319gitd2780b6
- 0.8.14

* Thu Oct 10 2024 Phantom X <megaphantomx at hotmail dot com> - 0.8.13-1
- 0.8.13
- udev rules from Gentoo

* Mon Oct 07 2024 Phantom X <megaphantomx at hotmail dot com> - 0.8.12-1
- 0.8.12 xiota fork
- meson build
- Boost removed

* Sun Feb 11 2024 Phantom X <megaphantomx at hotmail dot com> - 0.8.8-109.20200922gitc3cf3fe
- zerojay fork

* Tue Feb 08 2022 Phantom X <megaphantomx at hotmail dot com> - 0.8.8-108
- Return to official fork

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0.8.8-107.20200226git7f2251b
- Fix build with new scons

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 0.8.8-106.20200226git7f2251b
- Fix systemd unit

* Thu Feb 27 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-105.20200226git7f2251b
- Cebtenzzre fork
- Hardened systemd unit

* Sat Jan 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-104
- python3

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-103
- Patch to fix build with python3 scons, from AUR

* Mon Sep 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-102.chinfo
- Update URLs to gitlab
- Update files to proper dbus support
- Readd xboxdrvctl
- %%{_sysconfdir}/xboxdrv
- polkit policy
- _smp_mflags

* Wed Sep 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-101.chinfo
- Upstream fix

* Wed Jan 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-100.chinfo
- Add some pull requests from github
- Patch to fix c++14

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.8.8-3
- Rebuilt for Boost 1.63

* Wed Mar 16 2016 Antonio Trande <sagitter@fedoraproject.org> - 0.8.8-2
- Made xboxdrv.conf file and moved into /etc
- Fix init script for EPEL6

* Sat Mar 05 2016 Antonio Trande <sagitter@fedoraproject.org> - 0.8.8-1
- Update to release 0.8.8
- Patched for old kernels (EPEL6)
- Fixed systemd service file
- Added init script
- Added custom dbus rule

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 0.8.5-14
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.8.5-13
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.8.5-11
- rebuild for Boost 1.58

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.8.5-9
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.8.5-8
- Rebuild for boost 1.57.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.8.5-5
- Rebuild for boost 1.55.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.8.5-3
- Rebuild for boost 1.54.0

* Tue Jun 04 2013 Marcel Wysocki <maci@satgnu.net> - 0.8.5-2
- spec cleanups
- fix man page permission

* Sun May 26 2013 Marcel Wysocki <maci@satgnu.net> - 0.8.5-1
- initial fedora port
