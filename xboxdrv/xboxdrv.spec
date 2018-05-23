Name:           xboxdrv
Version:        0.8.8
Release:        100.chinfo%{?dist}
Summary:        Userspace Xbox/Xbox360 Gamepad Driver for Linux

License:        GPLv3+
URL:            http://pingus.seul.org/~grumbel/xboxdrv/
Source0:        https://github.com/xboxdrv/xboxdrv/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}-config.txt
Source3:        %{name}-daemon

# Fix 60 seconds delay
Patch1:         https://github.com/xboxdrv/xboxdrv/pull/214.patch#/xboxdrv-github-214.patch
# Fix "pure virtual function called" crash and related hang
Patch2:         https://github.com/xboxdrv/xboxdrv/pull/220.patch#/xboxdrv-github-220.patch
# Don't submit transfers when controller is disconnecting
Patch3:         https://github.com/xboxdrv/xboxdrv/pull/221.patch#/xboxdrv-github-221.patch
# Ensure string2btn matches btn2string's output
Patch4:         https://github.com/xboxdrv/xboxdrv/pull/227.patch#/xboxdrv-github-227.patch
# https://bugs.gentoo.org/show_bug.cgi?id=594674
Patch5:         xboxdrv-0.8.8-fix-c++14.patch

BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(x11)
BuildRequires:  gcc-c++
BuildRequires:  scons
%if 0%{?fedora}
BuildRequires:  libusbx-devel
BuildRequires:  boost-devel
%else
BuildRequires:  libusb1-devel
BuildRequires:  boost148-devel
%endif
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig
BuildRequires:  python2-devel
Requires:       dbus-python

%if 0%{?fedora} || 0%{?rhel} > 6
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%endif

%if 0%{?rhel} < 7
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%endif

%description
This is a Xbox/Xbox360 gamepad driver for Linux that works in userspace.
It is an alternative to the xpad kernel driver and has support for 
Xbox1 gamepads, Xbox360 USB gamepads and Xbox360 wireless gamepads, 
both first and third party.

%prep
%autosetup -p1

sed -i '1s|/usr/bin/env python|%{__python2}|' examples/responsecurve-generator.py

%build
scons \
 CC=gcc \
 CXX=g++ \
 BUILD=custom \
 CCFLAGS="%{build_cflags} -Wl,-z,relro -fPIC -pie -Wl,-z,now" \
 CXXFLAGS="%{build_cxxflags} -Wl,-z,relro -fPIC -pie -Wl,-z,now" \
 CPPFLAGS=" -ansi -pedantic" \
 LINKFLAGS="%{build_ldflags} -fPIC -pie -Wl,-z,now"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

rm -f %{buildroot}%{_bindir}/xboxdrvctl

chmod 644 %{buildroot}%{_mandir}/man1/xboxdrv*
install -pm 644 doc/xboxdrv-daemon.1 %{buildroot}%{_mandir}/man1

# Install dbus rule
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -pm 644 data/org.seul.Xboxdrv.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}.conf
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service


%files
%doc PROTOCOL NEWS AUTHORS README.md examples
%license COPYING
%{_bindir}/xboxdrv
%{_mandir}/man1/xboxdrv*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/dbus-1/system.d/org.seul.Xboxdrv.conf


%changelog
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
