%global commit c8ff5b40ce457693be55260ab3101056c172295a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220210
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global volk_ver 185

%global pkgname  parallel-rdp-standalone

Name:           mupen64plus-video-parallel
Version:        0
Release:        0.2%{?gver}%{?dist}
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

Provides:      bundled(volk) = %{volk_ver}


%description
This is a the paraLLEl-RDP video plugin for Mupen64Plus emulator.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

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
* Mon Feb 14 2022 Phantom X <megaphantomx at hotmail dot com> - 0-0.2.20220210gitc8ff5b4
- Last snapshot

* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.1.20210809git0b2ed4b
- Initial spec
