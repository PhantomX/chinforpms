%global soversion 0

Name:           libdeflate
Version:        1.17
Release:        1%{?dist}
Summary:        Heavily optimized library for compression and decompression

Epoch:          1

License:        MIT
URL:            https://github.com/ebiggers/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(zlib)

%description
%{name} is a library for fast, whole-buffer DEFLATE-based compression and
decompression.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        utils
Summary:        Command-line programs distributed with %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-progs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-progs < %{?epoch:%{epoch}:}%{version}-%{release}

%description    utils
%{name} is a library for fast, whole-buffer DEFLATE-based compression and
decompression.

This package contais command-line programs distributed with it.


%prep
%autosetup -p1


%build
%cmake \
  -DLIBDEFLATE_BUILD_STATIC_LIB:BOOL=OFF \
  -DLIBDEFLATE_USE_SHARED_LIB:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install


pushd %{buildroot}%{_libdir}
mv %{name}.so.%{soversion} %{name}.so.%{version}
ln -sf %{name}.so.%{soversion} %{name}.so
popd


%files
%license COPYING
%doc README.md NEWS.md
%{_libdir}/%{name}.so.*

%files devel
%license COPYING
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%files utils
%license COPYING
%{_bindir}/%{name}-*zip


%changelog
* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.17-1
- 1.17
- cmake

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1.14-1
- 1.14

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.10-1
- 1.10

* Thu Sep 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.8-1
- Initial spec
