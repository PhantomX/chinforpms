Name:           bctoolbox
Version:        0.5.1
Release:        1%{?dist}
Summary:        Utilities library used by Belledonne Communications softwares

Group:          System Environment/Libraries
License:        GPLv2
URL:            https://www.linphone.org
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  git
BuildRequires:  mbedtls-devel


%description
%{summary}.

%package devel
Summary:        Development libraries for bctoolbox
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description devel
%{summary}.

Development files.


%prep
%autosetup


%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
  -DENABLE_TESTS_COMPONENT:BOOL=OFF \
  -DENABLE_POLARSSL:BOOL=OFF

%make_build

popd

%install

%make_install -C builddir

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/*.hh
%{_datadir}/%{name}/cmake/*.cmake


%changelog
* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.5.1-1
- Initial spec
