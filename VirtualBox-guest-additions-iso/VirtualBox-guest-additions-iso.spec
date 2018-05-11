%global pkgname VBoxGuestAdditions

# Set to 0 for final release
%global prerel 0

Name:           VirtualBox-guest-additions-iso
Version:        5.2.12
Release:        1%{?prerel:.%{prerel}}%{?dist}
Summary:        Guest additions for VirtualBox

License:        GPLv2
URL:            http://www.virtualbox.org/
%if 0%{?prerel}
Source0:        http://www.virtualbox.org/download/testcase/%{pkgname}_%{version}-%{prerel}.iso
%else
Source0:        http://download.virtualbox.org/virtualbox/%{version}/%{pkgname}_%{version}.iso
%endif
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/gpl-2.0

BuildArch:      noarch

Requires:       VirtualBox-server >= %(echo %{version} | cut -d. -f -2)

%description
CD image containing guest additions for VirtualBox.

%prep
%autosetup -c -T

cp %{SOURCE1} .

%build


%install

mkdir -p %{buildroot}%{_datadir}/virtualbox
install -pm0644 %{SOURCE0} \
  %{buildroot}%{_datadir}/virtualbox/%{pkgname}.iso


%files
%license gpl-2.0
%{_datadir}/virtualbox/%{pkgname}.iso


%changelog
* Thu May 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.2.12-1
- 5.2.12

* Tue Apr 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.2.10-1
- 5.2.10

* Tue Feb 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.2.8-1
- 5.2.8

* Sat Jan 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.2.1-1.120326
- 5.2.7-120326

* Tue Jan 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.2.6-1
- 5.2.6

* Tue Dec 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.2.4-1
- 5.2.4

* Fri Nov 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.2.2-1
- 5.2.2

* Tue Nov 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.2.0-1
- 5.2.0

* Tue Oct 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.30-1
- 5.1.30

* Thu Sep 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.28-1
- 5.1.28

* Thu Jul 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.26-1
- 5.1.26

* Tue Jul 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.24-1
- 5.1.24

* Sat Apr 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.22-1
- 5.1.22

* Tue Apr 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.20-1
- 5.1.20

* Wed Mar 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.18-1
- 5.1.18

* Thu Mar 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.16-1
- new version

* Wed Jan 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.14-1
- new version

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.12-1
- Initial spec.
