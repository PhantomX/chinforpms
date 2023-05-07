%undefine _hardened_build

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 7da378033a7764f955516f75194856d87bbcd7a5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230507
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global mcl_ver 0.1.11
%global zycore_ver 1.4.1
%global zydis_ver 4.0.0

Name:           dynarmic
Version:        6.4.7
Release:        2%{?dist}
Summary:        An ARM dynamic recompiler

License:        0BSD AND MIT
URL:            https://github.com/merryhime/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  boost-devel >= 1.57
BuildRequires:  pkgconfig(fmt) >= 9
BuildRequires:  cmake(tsl-robin-map)
BuildRequires:  cmake(xbyak)

Provides:       bundled(mcl) = %{mcl_ver}
Provides:       bundled(zydis) = %{zydis_ver}
Provides:       bundled(zydis) = %{zydis_ver}


%description
A dynamic recompiler for ARM.


%package devel
Summary:        Header files for developing programs with %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
libmpd-devel is a sub-package which contains header files for developing
with %{name}.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

rm -rf externals/{catch,fmt,robin-map,xbyak}


%build
%cmake \
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_FMT:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_ROBIN_MAP:BOOL=ON \
  -DDYNARMIC_IGNORE_ASSERTS:BOOL=ON \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
  -DDYNARMIC_TESTS=OFF \
%{nil}

%cmake_build


%install
%cmake_install

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%license LICENSE.txt
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so


%changelog
* Sun May 07 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.7-1
- 6.4.7

* Mon Apr 03 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.6-1
- 6.4.6

* Tue Feb 07 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.5-1
- 6.4.5

* Wed Jan 18 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.4-1.20230117gitffc3dce
- 6.4.4

* Thu Jan 12 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.3-1.20230106git9af4b97
- 6.4.3

* Tue Dec 06 2022 Phantom X <megaphantomx at hotmail dot com> - 6.4.0-1.20211205gitec1f117
- Initial spec

