%global debug_package %{nil}

%global commit ad36e8b3aa62a18405e7afeb1314ad11d5bb4399
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20231208
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname volk

Name:           %{pkgname}-vulkan
Version:        1.3.273
Release:        1%{?dist}
Summary:        Meta loader for Vulkan API 

License:        MIT
URL:            https://github.com/zeux/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch10:        0001-cmake-change-namespace-to-volk_vulkan.patch
Patch11:        0001-library-set-PIC.patch

BuildRequires:  cmake3
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  cmake(VulkanHeaders) >= %{version}


%description
volk is a meta-loader for Vulkan. It allows you to dynamically load entrypoints
required to use Vulkan without linking to vulkan-1.dll or statically linking
Vulkan loader. Additionally, volk simplifies the use of Vulkan extensions by
automatically loading all associated entrypoints. Finally, volk enables loading
Vulkan entrypoints directly from the driver which can increase performance
by skipping loader dispatch overhead.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1


%build
%cmake3 \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DVOLK_INSTALL:BOOL=ON \
%{nil}

%cmake3_build


%install
%cmake3_install

%files devel
%license LICENSE.md
%{_libdir}/lib*.a
%{_includedir}/volk_vulkan/
%{_libdir}/cmake/volk_vulkan/


%changelog
* Sat Dec 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.273-1.20231208gitad36e8b
- 1.3.273

* Sat Dec 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.272-1.20231201git630309f
- Initial spec
