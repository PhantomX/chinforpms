%global commit 960fe054ffaab7cf55722fea6094c56a8ee8f18e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230606
%bcond_without snapshot

%global commit10 95b9cb015fa17baa749c2b396b335906e1596a9e
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 expected-lite

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           cppgir
Version:        0.1.0
Release:        1%{?dist}
Summary:        GObject-Introspection C++ binding wrapper generator

License:        MIT AND BSL-1.0
URL:            https://gitlab.com/mnauw/%{name}

%if %{with snapshot}
Source0:        %{url}/-/archive/%{commit}/%{name}-%{commit}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2#/%{name}-%{version}.tar.bz2
%endif
Source10:       https://github.com/martinmoene/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  boost-devel >= 1.58
BuildRequires:  cmake(fmt)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)

Provides:       bundled(%{srcname10}) = 0~git%{shortcommit10}


%description
cppgir is a GObject-Introspection C++ binding wrapper generator. That is, it
processes .gir files derived from GObject-Introspection annotations into a set
of C++ files defining suitable namespaces, classes and other types that together
from a C++ binding.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains %{name} header files.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1
tar -xf %{S:10} -C %{srcname10} --strip-components 1
cp -p expected-lite/LICENSE.txt LICENSE-expected-lite.txt

sed -e 's| lib/cmake| %{_lib}/cmake|g' -i CMakeLists.txt


%build
%cmake \
 -DBUILD_DOC:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license LICENSE*
%doc %{_pkgdocdir}/
%{_bindir}/%{name}
%{_datadir}/%{name}

%files devel
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/*.pc


%changelog
* Wed Jun 07 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1.0-1.20230606git960fe05
- Initial spec
