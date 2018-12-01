Name:           bctoolbox
Version:        0.6.0
Release:        4%{?dist}
Summary:        Utilities library used by Belledonne Communications softwares

License:        GPLv2
URL:            https://www.linphone.org
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
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
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DENABLE_TESTS_COMPONENT:BOOL=OFF \
  -DENABLE_MBEDTLS:BOOL=ON \
  -DENABLE_POLARSSL:BOOL=OFF

%make_build

popd

%install

%make_install -C %{_target_platform}


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
%{_datadir}/%{name}/cmake/*.in


%changelog
* Mon Oct 15 2018 Phantom X - 0.6.0-4
- New mbedtls

* Tue May 29 2018 Phantom X - 0.6.0-3
- New mbedtls

* Thu Mar 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.6.0-2
- Bump for new mbedtls

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.6.0-1
- 0.6.0

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.5.1-1
- Initial spec
