%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch %{ix86}
%global parch i386
%global icd_arch i686
%else
%global parch amd64
%global icd_arch %{_arch}
%endif

%global pkgname amdgpu-pro
%global pkgdistro ubuntu-20.04

%global minsdkver 1.1.121.1
%global ver     %%(echo %{version} | sed 's/\\./-/2')

Name:           amdgpu-pro-vulkan-driver
Version:        20.20.1089974
Release:        1%{?dist}
Summary:        AMDGPU Pro Driver For Vulkan

License:        AMD GPU PRO
URL:            http://www.amd.com

# Use Makefile do download
Source0:        %{pkgname}-%{ver}-%{pkgdistro}.tar.xz
Source1:        README-chinforpms

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  patchelf

Requires:       vulkan-loader%{?_isa} >= %{minsdkver}


%description
The AMD Pro Driver for Vulkan® is an Vulkan driver for Radeon™ graphics
adapters on Linux®.


%prep
%autosetup -n %{pkgname}-%{ver}-%{pkgdistro}

mkdir %{_target_platform}
ar p vulkan-amdgpu-pro_%{ver}_%{parch}.deb data.tar.xz | tar xJ -C %{_target_platform}
rm -f *.deb

mv %{_target_platform}/usr/share/doc/vulkan-amdgpu-pro/copyright .
cp -p %{S:1} README-chinforpms

sed \
  -e 's|/opt/amdgpu-pro/lib/.*-linux-gnu/amdvlk|%{_libdir}/amdvlkpro|g' \
  -i %{_target_platform}/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd*.json

patchelf --set-soname amdvlkpro%{__isa_bits}.so \
  %{_target_platform}/opt/amdgpu-pro/lib/*-linux-gnu/amdvlk%{__isa_bits}.so


%build


%install
mkdir -p %{buildroot}%{_libdir}
install -pm0755 %{_target_platform}/opt/amdgpu-pro/lib/*-linux-gnu/amdvlk%{__isa_bits}.so \
  %{buildroot}%{_libdir}/amdvlkpro%{__isa_bits}.so

mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d
install -pm0644 %{_target_platform}/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd*.json \
  %{buildroot}%{_datadir}/vulkan/icd.d/amdpro_icd.%{icd_arch}.json

mkdir -p %{buildroot}%{_sysconfdir}/amd


%files
%license copyright
%doc README-chinforpms
%dir %{_sysconfdir}/amd
%{_datadir}/vulkan/icd.d/amdpro_icd.%{icd_arch}.json
%{_libdir}/amdvlkpro*.so


%changelog
* Sat Jun 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.20.1089974-1
- 20.20-1089974

* Sun Apr 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.10.1048554-1
- 20.10-1048554

* Wed Mar 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 19.50.1011208-1
- 19.50.1011208

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 19.50.967956-1
- 19.50.967956

* Sat Nov 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.30.855429-1
- 19.30.934563

* Thu Aug 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.30.934563-1
- Initial spec
