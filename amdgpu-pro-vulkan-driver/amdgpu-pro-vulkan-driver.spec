%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch x86_64
%global parch amd64
%else
%global parch i386
%endif

%global pkgname amdgpu-pro
%global pkgdistro ubuntu-18.04

Name:           amdgpu-pro-vulkan-driver
Version:        19.30.855429
Release:        1%{?dist}
Summary:        AMDGPU Pro Driver For Vulkan
License:        AMD GPU PRO
URL:            http://www.amd.com

%global ver     %(echo %{version} | sed 's/\\./-/2')
# Use Makefile do download
Source0:        %{pkgname}-%{ver}-%{pkgdistro}.tar.xz
Source1:        README-chinforpms

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  patchelf

Requires:       vulkan
Requires:       vulkan-filesystem


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
  %{buildroot}%{_datadir}/vulkan/icd.d/amdpro_icd.%{_arch}.json

mkdir -p %{buildroot}%{_sysconfdir}/amd


%files
%license copyright
%doc README-chinforpms
%dir %{_sysconfdir}/amd
%{_datadir}/vulkan/icd.d/amdpro_icd.%{_arch}.json
%{_libdir}/amdvlkpro*.so


%changelog
* Thu Aug 29 2019 Phantom X <megaphantomx at bol dot com dot br> - Tue Aug 27 2019-1
- Initial spec
