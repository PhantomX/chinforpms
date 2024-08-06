%global commit 871913da6a4b132b567d7b65c509600363c0041e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 202406718
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url https://github.com/GPUOpen-LibrariesAndSDKs/%{name}

Summary:        Easy to integrate Vulkan memory allocation library
Name:           VulkanMemoryAllocator
Version:        3.1.0
Release:        100%{?dist}
Epoch:          1

License:        MIT
URL:            https://gpuopen.com/vulkan-memory-allocator/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

BuildArch:      noarch
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

%description
The Vulkan Memory Allocator (VMA) library provides a simple and easy to
integrate API to help you allocate memory for Vulkan buffer and image storage.

%package devel
Summary:        The Vulkan Memory Allocator development package
Requires:       vulkan-headers
Obsoletes:      %{name} < %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The Vulkan Memory Allocator development package.

%package doc
Summary:        The Vulkan Memory Allocator documentation package
BuildArch:      noarch

%description doc
The Vulkan Memory Allocator documentation package.

%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

#We don't need this :)
rm -f bin/*.exe
#Delete pre-generated docs (we will regenerate):
rm -rf docs/html
sed -e '/\/doc\//d' -i CMakeLists.txt

%build
%cmake \
  -G Ninja \
  -DVMA_BUILD_DOCUMENTATION:BOOL=ON \
%{nil}

%cmake_build

%install
%cmake_install


%files devel
%license LICENSE.txt
%doc README.md
%{_includedir}/vk_mem_alloc.h
%{_datadir}/cmake/%{name}


%files doc
%doc docs/gfx docs/html


%changelog
* Mon Aug 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1:3.1.0-100
- 3.1.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 06 2023 Jeremy Newton <Jeremy.Newton@amd.com> - 3.0.1-3
- Disable 32bit x86

* Fri Oct 06 2023 Jeremy Newton <Jeremy.Newton@amd.com> - 3.0.1-2
- Move documentation to doc subpackage

* Fri Oct 06 2023 Jeremy Newton <Jeremy.Newton@amd.com> - 3.0.1-1
- Initial Package
