%global commit 7f2251bc1b6c8ac6b81f0cfcc6a9a4894899ee28
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200226
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global gl_url  https://gitlab.com/xboxdrv/xboxdrv
# cebtenzzre fork
%global glc_url  https://gitlab.com/cebtenzzre/xboxdrv

Name:           xboxdrv
Version:        0.8.8
Release:        108%{?gver}%{?dist}
Summary:        Userspace Xbox/Xbox360 Gamepad Driver for Linux

License:        GPLv3+
URL:            https://xboxdrv.gitlab.io

%if 0%{?with_snapshot}
Source0:        %{glc_url}/-/archive/%{commit}/%{name}-%{commit}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        https://xboxdrv.gitlab.io/%{name}-linux-%{version}.tar.bz2
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

%if !%{?with_snapshot}
# Fix 60 seconds delay
Patch1:         %{gl_url}/-/merge_requests/262.patch#/%{name}-gl-262.patch
# Fix "pure virtual function called" crash and related hang
Patch2:         xboxdrv-pr220.patch
# Don't submit transfers when controller is disconnecting
Patch3:         xboxdrv-pr221.patch
# Ensure string2btn matches btn2string's output
Patch4:         xboxdrv-pr227.patch
# https://bugs.gentoo.org/show_bug.cgi?id=594674
Patch5:         xboxdrv-0.8.8-fix-c++14.patch
Patch6:         https://github.com/xboxdrv/xboxdrv/commit/ac6ebb1228962220482ea03743cadbe18754246c.patch#/%{name}-gh-ac6ebb1.patch
# https://aur.archlinux.org/cgit/aur.git/plain/scons-py3.patch?h=xboxdrv
Patch7:         %{name}-scons-py3.patch
%endif
Patch8:         %{gl_url}/commit/3ca002d783974539f5be4e683b67a58f4cc9fce0.patch#/%{name}-gl-3ca002d.patch
# https://aur.archlinux.org/packages/xboxdrv/#comment-822087
Patch9:         0001-scons-fix-build.patch

BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(x11)
BuildRequires:  gcc-c++
BuildRequires:  scons
BuildRequires:  libusbx-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  systemd
BuildRequires:  /usr/bin/pathfix.py
Requires:       python3-dbus
%{?systemd_requires}


%description
This is a Xbox/Xbox360 gamepad driver for Linux that works in userspace.
It is an alternative to the xpad kernel driver and has support for 
Xbox1 gamepads, Xbox360 USB gamepads and Xbox360 wireless gamepads, 
both first and third party.

%prep
%autosetup -n %{name}-%{?gver:%{commit}}%{!?gver:linux-%{version}} -p1

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" \
  examples/responsecurve-generator.py \
  xboxdrvctl


%build
scons %{?_smp_mflags} \
 CC=gcc \
 CXX=g++ \
 BUILD=custom \
 CCFLAGS="%{build_cflags} -Wl,-z,relro -fPIC -pie -Wl,-z,now" \
 CXXFLAGS="%{build_cxxflags} -Wl,-z,relro -fPIC -pie -Wl,-z,now" \
 CPPFLAGS=" -ansi -pedantic" \
 LINKFLAGS="%{build_ldflags} -fPIC -pie -Wl,-z,now"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

chmod 644 %{buildroot}%{_mandir}/man1/xboxdrv*
install -pm 644 doc/xboxdrv-daemon.1 %{buildroot}%{_mandir}/man1

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


%changelog
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
