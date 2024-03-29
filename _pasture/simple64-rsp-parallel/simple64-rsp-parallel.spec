%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 0c3a00727fc7de28a29f1acc3d1e6ee094d5cbc8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220914
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname  parallel-rsp

Name:           simple64-rsp-parallel
Version:        0
Release:        0.4%{?gver}%{?dist}
Summary:        paraLLEl-RDP RSP plugin for Mupen64Plus/simple64 emulator

License:        (MIT or LGPLv3)
URL:            https://github.com/simple64/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        https://github.com/simple64/parallel-rdp-standalone/raw/master/README.md

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mupen64plus-devel
BuildRequires:  pkgconfig(lightning)
Requires:       mupen64plus%{?_isa} >= 2.5.9

Obsoletes:      mupen64plus-rsp-parallel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mupen64plus-rsp-parallel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
This is a the paraLLEl-RDP RSP plugin for Mupen64Plus/simple64 emulator.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

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
* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0-0.4.20220914git0c3a007
- Rename

* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 0-0.3.20220807git30f0c7a
- Bump

* Mon Feb 14 2022 Phantom X <megaphantomx at hotmail dot com> - 0-0.2.20220208gite67cee3
- Snapshot update

* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.1.20210713gita9646b2
- Initial spec
