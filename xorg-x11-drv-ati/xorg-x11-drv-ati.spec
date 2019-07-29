%global pkgname xf86-video-ati
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers

%global commit c7ed12cb2ea76999351d7cb87877224bdc0664f0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190718
%global with_snapshot 1

%undefine _hardened_build

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Summary:   Xorg X11 ati video driver
Name:      xorg-x11-drv-ati
Version:   19.0.1
Release:   102%{?gver}%{?dist}

URL:       http://www.x.org
License:   MIT

%if 0%{?with_snapshot}
Source0:        https://gitlab.freedesktop.org/xorg/driver/%{pkgname}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        https://www.x.org/pub/individual/driver/%{pkgname}-%{version}.tar.bz2
%endif

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-devel >= 1.13
BuildRequires: pkgconfig(gbm) >= 10.6
BuildRequires: libdrm-devel >= 2.4.33-1
BuildRequires: kernel-headers >= 2.6.27-0.308
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.1.5
BuildRequires: libudev-devel
BuildRequires: xorg-x11-glamor-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: libdrm >= 2.4.36-1

%description
X.Org X11 ati video driver.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

%build
autoreconf -iv
%configure --disable-static --enable-glamor
%make_build

%install
%make_install
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%files
%{driverdir}/ati_drv.so
%{driverdir}/radeon_drv.so
%{_mandir}/man4/ati.4*
%{_mandir}/man4/radeon.4*
%{_datadir}/X11/xorg.conf.d/10-radeon.conf


%changelog
* Wed Jul 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-102.20190718gitc7ed12c
- New snapshot

* Tue Jul 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-101.20190625git33803c8
- Update to latest snapshot

* Tue Mar 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-100
- 19.0.1

* Thu Mar 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.0-100
- 19.0.0

* Tue Feb 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-101.20190128git15697ee
- Update to latest snapshot

* Sat Jan 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-100.20190109gitb1c0169
- Update to latest snapshot

* Fri Sep 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-1.chinfo
- 18.1.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 04 2018 Adam Jackson <ajax@redhat.com> - 18.0.1-1
- ati 18.0.1

* Mon Apr 02 2018 Adam Jackson <ajax@redhat.com> - 7.10.0-4
- Rebuild for xserver 1.20

* Mon Mar 19 2018 Adam Jackson <ajax@redhat.com> - 7.10.0-3
- Drop BuildRequires: python, not actually needed

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Adam Jackson <ajax@redhat.com> - 7.10.0-1
- ati 7.10.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 17 2017 Adam Jackson <ajax@redhat.com> - 7.9.0-1
- ati 7.9.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.7.1-2.20160928git3fc839ff
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 Hans de Goede <hdegoede@redhat.com> 7.7.1-1
- Update to latest git, this is the equivalent of 7.7.1 + fixes for use
  with xserver-1.19 (rhbz#1325613)
- Rebuild against xserver-1.19

* Wed May 18 2016 Dave Airlie <airlied@redhat.com> 7.7.0-1
- Update to latest git.

* Mon Feb 15 2016 Dave Airlie <airlied@redhat.com> 7.6.1-3
- update to latest git snapshot

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.1-2.20151116gitdfb5277
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Mon Nov 16 2015 Dave Airlie <airlied@redhat.com> 7.6.1-1
- 7.6.1 release git snapshot

* Wed Sep 16 2015 Dave Airlie <airlied@redhat.com> - 7.6.0-0.4.20150729git5510cd6
- 1.18 ABI rebuild

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> 7.6.0-0.3.20150729git5510cd6
- git snapshot for new ABI

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 7.6.0-0.2.20150709git95f5d09
- 1.15 ABI rebuild

* Thu Jul 09 2015 Dave Airlie <airlied@redhat.com> 7.6.0-0.1
- git snapshot of the day.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 7.5.0-4
- kill hardended builds harder

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 7.5.0-3
- kill hardended builds for X.org

* Wed Feb 11 2015 Hans de Goede <hdegoede@redhat.com> - 7.5.0-2
- xserver 1.17 ABI rebuild

* Fri Oct 10 2014 Adam Jackson <ajax@redhat.com> 7.5.0-1
- ati 7.5.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-2
- Fix FTBFS with xorg-server-1.16.0

* Wed Jul  2 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-1
- Update to 7.4.0 (rhbz#907141)

* Mon Jun 16 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-0.4.20140419git48d3dbc
- xserver 1.15.99.903 ABI rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-0.3.20140419git48d3dbc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 7.4.0-0.2.20140419git48d3dbc
- xserver 1.15.99-20140428 git snapshot ABI rebuild

* Sat Apr 19 2014 Dave Airlie <airlied@redhat.com> 7.4.0-0.1
- latest upstream git snapshot

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 7.2.0-7.20131101git3b38701
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-6.20131101git3b38701
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-5.20131101git3b38701
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-4.20131101git3b38701
- 1.15RC1 ABI rebuild

* Fri Nov 01 2013 Jerome Glisse <jglisse@redhat.com> - 7.2.0-3
- Update to lastest upstream git snapshot

* Fri Oct 25 2013 Jerome Glisse <jglisse@redhat.com> - 7.2.0-2
- Fix gnome-shell rendering issue with radeonsi

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 7.2.0-1
- ABI rebuild

* Thu Aug 29 2013 Dave Airlie <airlied@redhat.com> 7.2.0-0
- update to latest upstream release 7.2.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.0-6.20130408git6e74aacc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Jerome Glisse <jglisse@redhat.com> 7.1.0-5
- No need to patch for enabling glamor with git snapshot

* Mon Apr 08 2013 Jerome Glisse <jglisse@redhat.com> 7.1.0-4
- Git snapshot
- Enable glamor acceleration for southern island GPU

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 7.1.0-3
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 7.1.0-2
- ABI rebuild

* Tue Feb 26 2013 Adam Jackson <ajax@redhat.com> 7.1.0-1
- ati 7.1.0

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 7.0.0-0.10.20121015gitbd9e2c064
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 7.0.0-0.9.20121015gitbd9e2c064
- ABI rebuild

* Thu Nov 15 2012 Jerome Glisse <jglisse@redhat.com> 7.0.0-0.8.20121015gitbd9e2c064
- fix dri2 segfault #872536

* Mon Oct 15 2012 Dave Airlie <airlied@redhat.com> 7.0.0-0.7.20121015gitbd9e2c064
- fix issue with damage when using offload or sw cursor

* Mon Sep 10 2012 Dave Airlie <airlied@redhat.com> 7.0.0-0.6.20120910git7c7f27756
- make sure driver loads on outputless GPUs
