Name:           zycore-c
Version:        1.4.1
Release:        1%{?dist}
Summary:        Zyan Core Library for C

License:        MIT
URL:            https://github.com/zyantific/%{name}

Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

ExcludeArch:    s390x

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  pkgconfig(gtest)
BuildRequires:  doxygen

%description
%{name} is an internal library providing platform independent types, macros and a
fallback for environments without LibC.


%package        devel
Summary:        Development libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        docs
Summary:        HTML documentation for %{name}

%description    docs
Provides the documentation files for use with %{name}.


%prep
%autosetup -p1

%build
%cmake \
  -DZYCORE_BUILD_SHARED_LIB:BOOL=ON \
  -DZYCORE_BUILD_TESTS:BOOL=ON \
%{nil}

%cmake_build

%install
%cmake_install

mv %{buildroot}%{_datadir}/doc/Zycore _docs


%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/libZycore.so.*

%files devel
%{_includedir}/Zycore/
%{_libdir}/cmake/zycore/
%{_libdir}/libZycore.so

%files docs
%doc _docs/*


%changelog
* Thu Oct 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.4.1-1
- Initial spec
