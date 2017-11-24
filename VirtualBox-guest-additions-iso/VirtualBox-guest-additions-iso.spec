%global pkgname VBoxGuestAdditions

Name:           VirtualBox-guest-additions-iso
Version:        5.2.2
Release:        1%{?dist}
Summary:        Guest additions for VirtualBox

License:        GPLv2
URL:            http://www.virtualbox.org/
Source0:        http://download.virtualbox.org/virtualbox/%{version}/%{pkgname}_%{version}.iso
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/gpl-2.0

BuildArch:      noarch

Requires:       VirtualBox-server >= %{version}

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
