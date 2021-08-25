%global commit 0b2ed4b3eada8f9b3f730443b94971f5365813b5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210809
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname  parallel-rdp-standalone

Name:           mupen64plus-video-parallel
Version:        0
Release:        0.1%{?gver}%{?dist}
Summary:        paraLLEl-RDP video plugin for Mupen64Plus emulator

License:        MIT
URL:            https://github.com/loganmc10/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mupen64plus-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  vulkan-headers
Requires:       mupen64plus%{?_isa} >= 2.5.9
Requires:       mupen64plus-rsp-parallel%{?_isa} >= 0-0.1

%description
This is a the paraLLEl-RDP video plugin for Mupen64Plus emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

rm -rf parallel-rdp-standalone/vulkan-headers

sed \
  -e 's|../mupen64plus-core/src/api|%{_includedir}/mupen64plus|g' \
  -i CMakeLists.txt


%build
%cmake \
  -DENABLE_IPO:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_libdir}/mupen64plus/
install -pm0755 %{__cmake_builddir}/%{name}.so %{buildroot}%{_libdir}/mupen64plus/


%files
%license LICENSE
%doc README.md
%{_libdir}/mupen64plus/%{name}.so


%changelog
* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.1.20210809git0b2ed4b
- Initial spec
