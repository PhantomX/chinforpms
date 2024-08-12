%global commit 871913da6a4b132b567d7b65c509600363c0041e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 202406718
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vma_ver 3.1.0

Summary:        C++ bindings for VulkanMemoryAllocator
Name:           VulkanMemoryAllocator-Hpp
Version:        3.1.0
Release:        1%{?dist}

License:        Apache-2.0
URL:            https://github.com/YaaZ/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-cmake-fixes.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  VulkanMemoryAllocator-devel >= %{vma_ver}
BuildRequires:  pkgconfig(vulkan)

BuildArch:      noarch
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

%description
The Vulkan Memory Allocator Hpp library provides C++ bindings for
VulkanMemoryAllocator.

%package devel
Summary:        The Vulkan Memory Allocator Hpp development package
Requires:       VulkanMemoryAllocator-devel >= %{vma_ver}
Requires:       vulkan-loader-devel
Requires:       vulkan-headers

%description devel
The Vulkan Memory Allocator Hpp development package.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1


%build
%cmake \
  -G Ninja \
%{nil}

%cmake_build

%install
%cmake_install


%files devel
%license LICENSE
%doc README.md
%{_includedir}/vk*.hpp
%{_datadir}/cmake/%{name}


%changelog
* Wed Aug 07 2024 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-1
- Initial spec

