Name:           ada
Version:        2.9.0
Release:        1%{?dist}
Summary:        Library for creating and reading zstd-compressed file archives

License:        Apache-2.0 AND MIT
URL:            https://github.com/ada-url/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
WHATWG-compliant and fast URL parser written in modern C++.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%cmake \
  -DBUILD_TESTING:BOOL=OFF \
  -DADA_TOOLS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license LICENSE-APACHE LICENSE-MIT
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_includedir}/%{name}*.h
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}


%changelog
* Fri Aug 02 2024 Phantom X <megaphantomx at hotmail dot com> - 2.9.0-1
- Initial spec

