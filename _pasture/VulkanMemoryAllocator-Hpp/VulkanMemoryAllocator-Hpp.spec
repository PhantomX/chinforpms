%global commit 5e2b0bebc2f03bc255a1754d4dba135f5971eda8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250108
%bcond snapshot 0

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vma_ver 3.3.0

%global ver %%(echo %{version} | cut -d. -f-3)
%global xver %%(echo %{version} | cut -d. -f4)

Summary:        C++ bindings for VulkanMemoryAllocator
Name:           VulkanMemoryAllocator-Hpp
Version:        3.3.0.3
Release:        1%{?dist}

License:        Apache-2.0
URL:            https://github.com/YaaZ/%{name}

%if "%{xver}" == ""
%global verx 1
%endif

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{ver}%{!?verx:+%{?xver}}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  cmake(VulkanHeaders)
BuildRequires:  VulkanMemoryAllocator-devel >= %{vma_ver}

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
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}%{!?verx:-%{?xver}}} -p1

sed -e '/^add_subdirectory(VulkanMemoryAllocator)/d' -i CMakeLists.txt


%build
%cmake \
  -G Ninja \
  -DVMA_HPP_ENABLE_INSTALL:BOOL=ON \
  -DVMA_HPP_SAMPLES_BUILD:BOOL=OFF \
  -DVMA_HPP_INPUT_HEADER:FILEPATH=%{_includedir}/vk_mem_alloc.h \
  -DFETCHCONTENT_SOURCE_DIR_VULKAN:STRING="@" \
%{nil}

%cmake_build

%install
%cmake_install


%files devel
%license LICENSE
%doc README.md
%{_includedir}/vk*.cppm
%{_includedir}/vk*.hpp
%{_datadir}/cmake/%{name}


%changelog
* Fri Mar 20 2026 Phantom X <megaphantomx at hotmail dot com> - 3.3.0-1
- 3.3.0

* Thu Sep 18 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.1-2
- Remove ValidationFailedEXTError

* Tue Apr 08 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.1-1
- 3.2.1

* Thu Jan 09 2025 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-2.20250108git5e2b0be.20250108git5e2b0be
- 1.4 headers support

* Wed Aug 07 2024 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-1
- Initial spec

