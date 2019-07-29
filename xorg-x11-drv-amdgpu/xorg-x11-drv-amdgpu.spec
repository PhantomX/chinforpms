%global pkgname xf86-video-amdgpu
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers

%global commit 87f41ace4920fd2069794211683659eb25b025a6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190705
%global with_snapshot 1

# Xorg cannot load hardened build
%undefine _hardened_build

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           xorg-x11-drv-amdgpu
Version:        19.0.1
Release:        102%{?gver}%{?dist}

Summary:        AMD GPU video driver
License:        MIT

URL:            https://www.x.org/wiki
%if 0%{?with_snapshot}
Source0:        https://gitlab.freedesktop.org/xorg/driver/%{pkgname}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        https://www.x.org/pub/individual/driver/%{pkgname}-%{version}.tar.bz2
%endif

ExcludeArch:    s390 s390x

BuildRequires:  python2
BuildRequires:  xorg-x11-server-devel
BuildRequires:  pkgconfig(gbm) >= 10.6
BuildRequires:  libdrm-devel
BuildRequires:  kernel-headers
BuildRequires:  automake autoconf libtool pkgconfig
BuildRequires:  xorg-x11-util-macros
BuildRequires:  libudev-devel
BuildRequires:  xorg-x11-glamor-devel

Requires:       Xorg %(xserver-sdk-abi-requires ansic)
Requires:       Xorg %(xserver-sdk-abi-requires videodrv)
Requires:       libdrm >= 2.4.76

%description
X.Org X11 AMDGPU driver

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

%build
%if 0%{?with_snapshot}
autoreconf -fiv
%endif
%configure --disable-static --enable-glamor
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files
%{driverdir}/amdgpu_drv.so
%{_datadir}/X11/xorg.conf.d/10-amdgpu.conf
%{_mandir}/man4/amdgpu.4*


%changelog
* Wed Jul 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-102.20190705git87f41ac
- New snapshot

* Tue Jul 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-101.20190509git7d3fef7
- Update to latest snapshot

* Tue Mar 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-100
- 19.0.1

* Thu Mar 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.0-100
- 19.0.0

* Wed Jan 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-100.20190124git9045fb3
- Update to latest snapshot

* Sun Sep 16 2018 Christopher Atherton <the8lack8ox@gmail.com> - 18.1.0-1
- Update to 18.1.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 18.0.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Apr 02 2018 Adam Jackson <ajax@redhat.com> - 18.0.1-2
- Rebuild for xserver 1.20

* Thu Mar 15 2018 Christopher Atherton <the8lack8ox@gmail.com> - 18.0.1-1
- Update to 18.0.1

* Wed Mar 07 2018 Christopher Atherton <the8lack8ox@gmail.com> - 18.0.0-1
- Update to 18.0.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 08 2017 Christopher Atherton <the8lack8ox@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 16 2017 poma <poma@gmail.com> 1.3.0-1
- Update to 1.3.0

* Mon Nov 21 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.2.0-1
- Update to latest release

* Thu Sep 29 2016 Hans de Goede <hdegoede@redhat.com> 1.1.2-3
- Update to latest git master for use with xserver-1.19
- Rebuild against xserver-1.19

* Sat Sep 24 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.2-2
- Use upstream provided xorg.conf file

* Sat Sep 17 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.2-1
- Update to latest release

* Thu Sep 15 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.1-1
- Update to latest release

* Sun Sep 04 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.0-6
- Add BuildRequires on mesa-libgbm-devel

* Sun Sep 04 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.0-5
- Disable hardened build

* Sun Sep 04 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.0-4
- Use buildroot macro not RPM_BUILD_ROOT variable
- Replace /usr/share with _datadir
- Enable hardened build

* Sat Sep 03 2016 Christopher Atherton <the8lack8ox@gmail.cmo> 1.1.0-3
- Require libdrm equal to or later than 2.4.63

* Sat Sep 03 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.0-2
- Fixed ExcludeArch typo
- Add URL for source
- Use --force with autoreconf
- Use make_build macro
- Removed explicit libdrm dependency

* Sat Sep 03 2016 Christopher Atherton <the8lack8ox@gmail.com> 1.1.0-1
- Initial spec
