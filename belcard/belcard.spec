Name:           belcard
Version:        1.0.2
Release:        1%{?dist}
Summary:        C++ library to manipulate VCard standard format

License:        GPLv3
URL:            https://www.linphone.org
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(belr)


%description
%{summary}.

%package devel
Summary:        Development libraries for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description devel
%{summary}.

Development files.


%prep
%autosetup -n %{name}-%{version}-0

sed \
  -e 's|@CMAKE_INSTALL_PREFIX@|%{_prefix}|g' \
  -e 's|@PROJECT_NAME@|%{name}|g' \
  -e 's|@CMAKE_INSTALL_FULL_INCLUDEDIR@|%{_includedir}|g' \
  -e 's|@CMAKE_INSTALL_FULL_LIBDIR@|%{_libdir}|g' \
  -e '/^Libs.private:/d' \
  -e "s,@PROJECT_VERSION@,$(awk '/BELCARD VERSION/{print $3}' CMakeLists.txt),g" \
  %{name}.pc.in > %{name}.pc

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
install -pm0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_bindir}/belcard-*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.hpp
%{_datadir}/Belcard/cmake/*.cmake


%changelog
* Fri Sep 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-1
- Initial spec
