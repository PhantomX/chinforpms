# Static only package
%global debug_package %{nil}

%global commit 51743dfd01dff6179e2d8f7095729caa4e2222e9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250510
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname tdlib

Name:           tde2e
Version:        1.8.49
Release:        1%{?dist}
Summary:        Cross-platform library for building Telegram clients

License:        BSL-1.0
URL:            https://github.com/tdlib/td

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  gperf
BuildRequires:  gperftools-devel
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)

# Building with default settings require at least 16 GB of free RAM.
# Builds on ARM and other low-memory architectures are failing.
ExclusiveArch: x86_64 aarch64


%description
tde2e (Telegram Database library) is a cross-platform library for
building Telegram clients. It can be easily used from almost any
programming language.


%package devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig(openssl)
Requires:       pkgconfig(zlib)


%description devel
%{summary}.


%prep
%autosetup -n td-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

sed -e 's/"DEFAULT"/"PROFILE=SYSTEM"/g' -i tdnet/td/net/SslStream.cpp

sed \
  -e 's|-L\\"${DIRECTORY_NAME}\\" ||g' \
  -e 's|-L\\"${PKGCONFIG_LIBDIR}\\" ||g' \
  -i CMake/GeneratePkgConfig.cmake


%build
%cmake -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DTD_ENABLE_JNI:BOOL=OFF \
  -DTD_ENABLE_DOTNET:BOOL=OFF \
  -DTD_E2E_ONLY:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_libdir}/lib{,%{name}-}tdutils.a

sed \
  -e 's|libtdutils.a|lib%{name}-tdutils.a|g' \
  -i %{buildroot}%{_libdir}/cmake/%{name}/tde2eStaticTargets-release.cmake

sed -e 's|tdutils|%{name}-tdutils|g' -i %{buildroot}%{_libdir}/pkgconfig/*.pc

mv %{buildroot}%{_libdir}/pkgconfig/{,%{name}-}tdutils.pc


%files devel
%license LICENSE_1_0.txt
%doc README.md CHANGELOG.md
%{_includedir}/td/e2e
%{_libdir}/lib%{name}*.a
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}*.pc


%changelog
* Tue May 13 2025 Phantom X <megaphantomx at hotmail dot com> - 1.8.49-1.20250510git51743df
- Initial spec
