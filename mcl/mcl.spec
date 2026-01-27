Name:           mcl
Version:        0.1.14
Release:        1%{?dist}
Summary:        merry's common library

License:        MIT
URL:            https://github.com/azahar-emu/%{name}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         0001-cmake-add-soversion.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  cmake(fmt) >= 11


%description
A collection of C++20 utilities which is common to a number of merry's projects.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%autosetup -p1


%build
%cmake \
  -G Ninja \
  -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/*.so


%changelog
* Mon Jan 26 2026 Phantom X <megaphantomx at hotmail dot com> - 0.1.14-1
- Initial spec
