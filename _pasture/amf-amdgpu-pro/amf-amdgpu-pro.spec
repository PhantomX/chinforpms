# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none

%global pkgdistro rhel/10.0
%global pkgrelease 310

%global amdenc_so_ver 1.0
%global amfrt_so_ver 1.5.0

Name:           amf-amdgpu-pro
Version:        25.20
Release:        1%{?dist}
Summary:        AMDGPU Pro Advanced Multimedia Framework

License:        LicenseRef-AMD-GPU-PRO-End-User-License-Agreement
URL:            https://github.com/GPUOpen-LibrariesAndSDKs/AMF

Source0:        https://repo.radeon.com/amf/%{version}/%{pkgdistro}/packages/main/%{_arch}/amf-amdgpu-pro-%{version}-%{pkgrelease}.x86_64.rpm
Source1:        https://repo.radeon.com/amf/%{version}/%{pkgdistro}/packages/main/%{_arch}/libamdenc-amdgpu-pro-%{version}-%{pkgrelease}.x86_64.rpm

ExclusiveArch:  x86_64

Requires:       vulkan-loader%{?_isa}
Suggests:       rocm-opencl%{?_isa}


%description
The Advanced Media Framework (AMF) SDK provides developers with optimal
access to AMD devices for multimedia processing .


%prep
%autosetup -cT

rpm2cpio %{S:0} | cpio -imdv
rpm2cpio %{S:1} | cpio -imdv

%{__strip} --strip-unneeded opt/amf/%{_lib}/libamdenc%{__isa_bits}.so.%{amdenc_so_ver}
%{__strip} --strip-unneeded opt/amf/%{_lib}/libamfrt%{__isa_bits}.so.%{amfrt_so_ver}


%build


%install
mkdir -p %{buildroot}%{_libdir}
install -pm0755 opt/amf/%{_lib}/libamdenc%{__isa_bits}.so.%{amdenc_so_ver} \
  %{buildroot}%{_libdir}/
ln -s libamdenc%{__isa_bits}.so.%{amfrt_so_ver} \
  %{buildroot}%{_libdir}/libamdenc%{__isa_bits}.so
  
install -pm0755 opt/amf/%{_lib}/libamfrt%{__isa_bits}.so.%{amfrt_so_ver} \
  %{buildroot}%{_libdir}/
ln -s libamfrt%{__isa_bits}.so.%{amfrt_so_ver} \
  %{buildroot}%{_libdir}/libamfrt%{__isa_bits}.so.1
ln -s libamfrt%{__isa_bits}.so.%{amfrt_so_ver} \
  %{buildroot}%{_libdir}/libamfrt%{__isa_bits}.so


%files
%license opt/amf/share/licenses/%{name}/AMDGPUPROEULA
%{_libdir}/libamdenc%{__isa_bits}.so*
%{_libdir}/libamfrt%{__isa_bits}.so*


%changelog
* Thu Dec 11 2025 - 25.20-1
- Initial spec

