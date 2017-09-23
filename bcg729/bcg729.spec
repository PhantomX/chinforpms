Name:           bcg729
Version:        1.0.4
Release:        1%{?dist}
Summary:        Encoder and decoder of the ITU G729 Annex A/B speech codec library

License:        GPLv2
URL:            https://www.linphone.org
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake


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
  -e 's|@prefix@|%{_prefix}|g' \
  -e 's|@exec_prefix@|%{_exec_prefix}|g' \
  -e 's|@includedir@|%{_includedir}|g' \
  -e 's|@libdir@|%{_libdir}|g' \
  -e "s,@PACKAGE_VERSION@,$(awk '/bcg729 VERSION/{print $3}' CMakeLists.txt),g" \
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

popd

%install

%make_install -C builddir

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 lib%{name}.pc %{buildroot}%{_libdir}/pkgconfig/lib%{name}.pc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/*.h
%{_datadir}/Bcg729/cmake/*.cmake


%changelog
* Fri Sep 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.4-1
- Initial spec
