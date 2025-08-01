%global commit 3df20bd653ebf8fed7fe52a7988409f017958817
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20191108
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           glyr
Version:        1.0.10
Release:        1%{?dist}
Summary:        A search engine for music related metadata

License:        LGPL-3.0-only
URL:            https://github.com/sahib/glyr

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(sqlite3)


%description
Glyr is a search engine for music related metadata. It comes both in a
command-line interface tool and as a C library, both with an easy to use
interface.
The sort of metadata glyr is searching (and downloading) is usually the data
you see in your musicplayer.


%package libs
Summary:        %{summary} library
License:        LGPLv3

%description libs
The %{name}-libs package contains the dynamic libraries needed for %{name} and
applications.

%package devel
Summary:        %{summary} development files
License:        LGPLv3
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files libraries for libglyr.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed \
  -e '/GCC_ONLY_OPT/s|-s||g' \
  -e 's| -Os||g' \
  -i CMakeLists.txt

sed -e 's|-L@CMAKE_INSTALL_PREFIX@/@INSTALL_LIB_DIR@ ||g' -i libglyr.pc.in


%build
%cmake

%cmake_build


%install
%cmake_install


%files
%license COPYING
%doc AUTHORS README.textile
%{_bindir}/*

%files libs
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%license COPYING
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc


%changelog
* Thu Apr 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.10-1.20191108git3df20bd
- Initial spec
