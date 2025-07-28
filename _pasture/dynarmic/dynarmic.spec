%undefine _hardened_build

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%bcond native 0
# Enable system zydis
%bcond zydis 0

%global commit a002730d68e0d700c80d11d7083d14dbc5df0977
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250702
%bcond snapshot 1


%global commit10 7b08d83418f628b800dfac1c9a16c3f59036fbad
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 mcl

%global commit11 e59d30b7b12e1d04cc2fc9c6219e35bda447c17e
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 unordered_dense

%global commit12 7ad36e52110b39cfb62b47bfdb6def94ac531309
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 zycore-c

%global commit13 6372690e30389a94db65ece2d8a1f0a2310475ed
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 zydis

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global zydis_ver 4.1.1

%global vc_url   https://git.eden-emu.dev/eden-emu

%global pkgname eden

Name:           dynarmic
Version:        6.7.0
Release:        7%{?dist}
Summary:        An ARM dynamic recompiler

License:        0BSD AND MIT
URL:            https://git.eden-emu.dev/eden-emu/%{name}

%if %{with snapshot}
Source0:        %{vc_url}/%{pkgname}/archive/%{commit}.tar.gz#/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{pkgname}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Source10:       https://github.com/azahar-emu/%{srcname10}/archive/%{commit10}.tar.gz#/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       https://github.com/Lizzie841/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       https://github.com/zyantific/%{srcname12}/archive/%{commit12}.tar.gz#/%{srcname12}-%{shortcommit12}.tar.gz
Source13:       https://github.com/zyantific/%{srcname13}/archive/%{commit13}.tar.gz#/%{srcname13}-%{shortcommit13}.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  boost-devel >= 1.57
BuildRequires:  pkgconfig(fmt) >= 9
BuildRequires:  cmake(xbyak) >= 7
%if %{with zydis}
BuildRequires:  cmake(zydis) >= %{zydis_ver}
%else
Provides:       bundled(zydis) = 0~git%{?shortcommit13}
%endif

Provides:       bundled(mcl) = 0~git%{?shortcommit10}
Provides:       bundled(unordered_dense) = 0~git%{?shortcommit11}


%description
A dynamic recompiler for ARM.


%package devel
Summary:        Header files for developing programs with %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
libmpd-devel is a sub-package which contains header files for developing
with %{name}.


%prep
%autosetup %{?with_snapshot:-n %{pkgname}} -N -p1
pushd externals/dynarmic
%autopatch -M 500 -p1

tar -xf %{S:10} -C externals/mcl --strip-components 1
tar -xf %{S:11} -C externals/unordered_dense --strip-components 1

%if %{with zydis}
sed \
  -e '/find_/s|Zydis|zydis|g' \
  -i CMakeLists.txt CMakeModules/dynarmicConfig.cmake.in
%else
tar -xf %{S:12} -C externals/zycore-c --strip-components 1
tar -xf %{S:13} -C externals/zydis --strip-components 1
sed \
  -e '/find_/s|Zydis|zydis_DISABLED|g' \
  -i CMakeLists.txt CMakeModules/dynarmicConfig.cmake.in
cp -p externals/zycore-c/LICENSE LICENSE.zycore-c
cp -p externals/zydis/LICENSE LICENSE.zydis
%endif

cp -p externals/mcl/LICENSE LICENSE.mcl
cp -p externals/unordered_dense/LICENSE LICENSE.unordered_dense

%if 0%{with native}
sed -e '/-mtune=core2/d' -i CMakeLists.txt
%else
sed -e '/DYNARMIC_CXX_FLAGS/s|-mtune=core2|-march=x86-64-v2|' -i CMakeLists.txt
%endif
popd

%build
%global xbyak_flags -DXBYAK_STRICT_CHECK_MEM_REG_SIZE=0
export CFLAGS+=" %{xbyak_flags}"
export CXXFLAGS+=" %{xbyak_flags}"
pushd externals/dynarmic
%cmake \
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_IGNORE_ASSERTS:BOOL=ON \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
  -DDYNARMIC_TESTS:BOOL=OFF \
%{nil}

%cmake_build
popd


%install
pushd externals/dynarmic
%cmake_install
popd


%files
%license externals/dynarmic/LICENSE.*
%doc externals/dynarmic/README.md
%{_libdir}/lib%{name}.so.*

%files devel
%license externals/dynarmic/LICENSE.*
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so


%changelog
* Mon May 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.7.0-3.20250517git9baf5ad
- Change to eden fork

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

