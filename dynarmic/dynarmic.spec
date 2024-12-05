%undefine _hardened_build

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

# Enable system zydis
%bcond_with zydis

%global commit fa6cc2e4b2a2954f2298b6548174479c5b106c2a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240302
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global mcl_ver 0.1.12
%global zydis_ver 4.0.0

Name:           dynarmic
Version:        6.7.0
Release:        2%{?dist}
Summary:        An ARM dynamic recompiler

License:        0BSD AND MIT
URL:            https://github.com/lioncash/%{name}

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
BuildRequires:  cmake(xbyak) >= 7
%if %{with zydis}
BuildRequires:  cmake(zydis) >= %{zydis_ver}
%else
Provides:       bundled(zydis) = %{zydis_ver}
%endif

Provides:       bundled(mcl) = %{mcl_ver}


%description
A dynamic recompiler for ARM.


%package devel
Summary:        Header files for developing programs with %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
libmpd-devel is a sub-package which contains header files for developing
with %{name}.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -N -p1
%autopatch -M 500 -p1

rm -rf externals/{catch,fmt,oaknut,robin-map,xbyak}

%if %{with zydis}
rm -rf externals/{zycore,zydis}
sed \
  -e '/find_/s|Zydis|zydis|g' \
  -i CMakeLists.txt CMakeModules/dynarmicConfig.cmake.in
%else
sed \
  -e '/find_/s|Zydis|zydis_DISABLED|g' \
  -i CMakeLists.txt CMakeModules/dynarmicConfig.cmake.in
%endif


%build
%cmake \
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_IGNORE_ASSERTS:BOOL=ON \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
  -DDYNARMIC_TESTS:BOOL=OFF \
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
* Wed Dec 04 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.0-2.20240302gitfa6cc2e
- Remove the revert commit

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.0-1.20240302gitfa6cc2e
- 6.7.0

* Sun Feb 18 2024 Phantom X <megaphantomx at hotmail dot com> - 6.6.3-1.20240217git4f08226
- 6.6.3

* Fri Feb 09 2024 Phantom X <megaphantomx at hotmail dot com> - 6.6.2-1.20240206gita32e6f5
- 6.6.2

* Thu Oct 19 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.0-1
- 6.5.0
- System zydis support

* Thu Jun 08 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.8-1
- 6.4.8

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

