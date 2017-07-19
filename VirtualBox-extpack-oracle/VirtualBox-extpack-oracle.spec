%global debug_package %{nil}
%global __strip /bin/true

%global pkgname Oracle_VM_VirtualBox_Extension_Pack

Name:           VirtualBox-extpack-oracle
Version:        5.1.24
Release:        1%{?dist}
Summary:        PUEL extensions for VirtualBox)

License:        PUEL
URL:            http://www.virtualbox.org/wiki/VirtualBox
Source0:        http://download.virtualbox.org/virtualbox/%{version}/%{pkgname}-%{version}.vbox-extpack

BuildRequires:  tar
Requires:       VirtualBox-server >= %{version}

%description
Support for USB 2.0 devices, VirtualBox RDP and PXE boot for Intel cards for
VirtualBox.

%prep
%autosetup -c T
tar -xzvf %{SOURCE0}


%build

%install

mkdir -p %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/%{pkgname}
cp -rp * \
  %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/%{pkgname}

%files
%license ExtPack-license.txt
%{_libdir}/virtualbox/ExtensionPacks/%{pkgname}


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
- 5.1.16

* Wed Jan 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.14-1
- new version

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.12-1
- Initial spec.
