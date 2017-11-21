%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global pkgname Oracle_VM_VirtualBox_Extension_Pack

%ifarch x86_64
%global parch amd64
%else
%global parch x86
%endif

Name:           VirtualBox-extpack-oracle
Version:        5.2.0
Release:        1%{?dist}
Summary:        PUEL extensions for VirtualBox

License:        PUEL
URL:            http://www.virtualbox.org/wiki/VirtualBox
Source0:        http://download.virtualbox.org/virtualbox/%{version}/%{pkgname}-%{version}.vbox-extpack

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  tar
Requires:       VirtualBox-server%{?isa} >= %{version}

%description
Support for USB 2.0 devices, VirtualBox RDP and PXE boot for Intel cards for
VirtualBox.

%prep
%autosetup -c T
tar -xzvf %{SOURCE0}


%build

%install

mkdir -p %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/%{pkgname}
cp -rp ExtPack*.* *.rom linux.%{parch} \
  %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/%{pkgname}/

%files
%license ExtPack-license.txt
%{_libdir}/virtualbox/ExtensionPacks/%{pkgname}


%changelog
* Tue Nov 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.2.0-1
- 5.2.0

* Tue Oct 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.30-1
- 5.1.30
- Do not install uneeded architecture files

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
- 5.1.16

* Wed Jan 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.14-1
- new version

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.12-1
- Initial spec.
