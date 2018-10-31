Name:           libxspf
Version:        1.2.0
Release:        1%{?dist}
Summary:        XSPF playlist handling library

License:        BSD
URL:            http://libspiff.sourceforge.net/
Source0:        https://downloads.sourceforge.net/libspiff/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(expat) >= 1.95.8
BuildRequires:  pkgconfig(liburiparser) >= 0.7.2


%description
libxspf (formerly called libSpiff) brings XSPF playlist reading and
writing support to your C++ application.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig(expat)

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup

sed -e '\|#include <climits>|a#include <unistd.h> // getcwd' \
  -i examples/read/read.cpp

sed \
  -e 's|/lib\b|/%{_lib}|g' \
  -i configure

%build
%configure \
  --disable-static \
  --disable-test \
  --disable-doc

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install

%make_install
find %{buildroot} -name '*.la' -delete


%files
%license COPYING
%doc AUTHORS
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%{_includedir}/xspf
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.2.0-1
- Initial spec
