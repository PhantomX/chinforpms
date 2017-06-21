Name:           bzrtp
Version:        1.0.5
Release:        1%{?dist}
Summary:        Opensource implementation of ZRTP keys exchange protocol

Group:          System Environment/Libraries
License:        GPLv2
URL:            https://www.linphone.org
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(libxml-2.0)


%description
%{summary}.

%package devel
Summary:        Development libraries for bzrtp
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description devel
%{summary}.

Development files.


%prep
%autosetup

autoreconf -ivf

%build
%configure \
  --disable-tests \
  --disable-silent-rules \
  --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

find %{buildroot} -name '*.la' -delete

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


%changelog
* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.5-1
- Initial spec
