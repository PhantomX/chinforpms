# Build tests
%bcond_with tests

Name:           oaknut
Version:        2.0.2
Release:        1%{?dist}
Summary:        Yet another AArch64 emitter

Epoch:          1

License:        MIT
URL:            https://github.com/merryhime/%{name}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
%if %{with tests}
BuildRequires:  pkgconfig(catch2) >= 3
%endif


%description
A C++20 assembler for AArch64 (ARMv8.0 to ARMv8.2).
Oaknut is a header-only library that allows one to dynamically assemble code
in-memory at runtime.

%package devel
Summary:        Yet another AArch64 emitter
Provides:       oaknut-static = %{version}-%{release}

%description devel
A C++20 assembler for AArch64 (ARMv8.0 to ARMv8.2).
Oaknut is a header-only library that allows one to dynamically assemble code
in-memory at runtime.


%prep
%autosetup -p1

%build
%cmake \
  %{!?with_tests:-DBUILD_TESTING:BOOL=OFF} \
%{nil}

%cmake_build


%install
%cmake_install


%files devel
%doc README.md
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}


%changelog
* Fri Feb 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.2-1
- Initial spec

