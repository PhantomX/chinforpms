%global pkgname VBoxGuestAdditions

Name:           VirtualBox-guest-additions-iso
Version:        5.1.24
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
