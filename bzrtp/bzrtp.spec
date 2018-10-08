Name:           bzrtp
Version:        1.0.6
Release:        4%{?dist}
Summary:        Opensource implementation of ZRTP keys exchange protocol

License:        GPLv2
URL:            https://www.linphone.org
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)


%description
%{summary}.

%package devel
Summary:        Development libraries for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description devel
%{summary}.

Development files.


%prep
%autosetup

sed \
  -e 's|"-Werror" ||g' \
  -i CMakeLists.txt

sed \
  -e 's|@prefix@|%{_prefix}|g' \
  -e 's|@exec_prefix@|%{_exec_prefix}|g' \
  -e 's|@includedir@|%{_includedir}|g' \
  -e 's|@libdir@|%{_libdir}|g' \
  -e "s,@PACKAGE_VERSION@,$(awk '/bzrtp VERSION/{print $3}' CMakeLists.txt),g" \
  lib%{name}.pc.in > lib%{name}.pc

%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
  -DENABLE_TESTS:BOOL=OFF

%make_build

%install
%make_install -C builddir

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 lib%{name}.pc %{buildroot}%{_libdir}/pkgconfig/lib%{name}.pc


%files
%license COPYING
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/*.h
%{_datadir}/%{name}/cmake/*.cmake


%changelog
* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0.6-4
- BR: gcc-c++

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0.6-3
- Remove -Werror

* Fri Sep 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.6-2
- cmake and fixes for it

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.6-1
- 1.0.6
- BR: sqlite3

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.5-1
- Initial spec
