%global commit a9646b27c2ef399e5917735b4d84ebe93edcce39
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210713
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname  parallel-rsp

Name:           mupen64plus-rsp-parallel
Version:        0
Release:        0.1%{?gver}%{?dist}
Summary:        paraLLEl-RDP RSP plugin for Mupen64Plus emulator

License:        (MIT or LGPLv3)
URL:            https://github.com/loganmc10/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        https://github.com/loganmc10/parallel-rdp-standalone/raw/master/README.md

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mupen64plus-devel
BuildRequires:  pkgconfig(lightning)
Requires:       mupen64plus%{?_isa} >= 2.5.9

%description
This is a the paraLLEl-RDP RSP plugin for Mupen64Plus emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

cp -p %{S:1} .

sed \
  -e 's|../mupen64plus-core/src/api|%{_includedir}/mupen64plus|g' \
  -i CMakeLists.txt

sed -e 's|<lightning.h>|<lightning/lightning.h>|g' -i rsp_jit.hpp


%build
%cmake \
  -DPARALLEL_RSP_BAKED_LIGHTNING:BOOL=OFF \
  -DENABLE_IPO:BOOL=OFF \
  -DPARALLEL_RSP_DEBUG_JIT:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_libdir}/mupen64plus/
install -pm0755 %{__cmake_builddir}/%{name}.so %{buildroot}%{_libdir}/mupen64plus/


%files
%license LICENSE LICENSE.LESSER LICENSE.MIT
%doc CREDITS.txt README.md
%{_libdir}/mupen64plus/%{name}.so


%changelog
* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.1.20210713gita9646b2
- Initial spec
