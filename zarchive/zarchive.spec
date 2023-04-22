%global pkgname ZArchive

Name:           zarchive
Version:        0.1.2
Release:        1%{?dist}
Summary:        Library for creating and reading zstd-compressed file archives

License:        MIT-0
URL:            https://github.com/Exzap/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(libzstd)

%description
ZArchive is yet another file archive format. Think of zip, tar, 7z, etc. but
with the requirement of allowing random-access reads and supporting compression.


%package libs
Summary:        %{summary} library

%description libs
The %{name}-libs package contains the dynamic libraries needed for %{name} and
applications.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{pkgname}-%{version} -p1


%build
%cmake

%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%files libs
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Apr 21 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1.2-1
- Initial spec
