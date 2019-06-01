Name:           lzlib
Version:        1.11
Release:        1%{?dist}
Summary:        A compression library for the lzip file format

License:        GPLv2+
URL:            http://www.nongnu.org/lzip/%{name}.html

Source0:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz.sig

BuildRequires:  gcc


%description
Lzlib is a data compression library providing in-memory LZMA compression
and decompression functions, including integrity checking of the
decompressed data.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%configure \
  --disable-static \
  --enable-shared \
  --disable-ldconfig \
  CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}" \
%{nil}

%make_build


%install
%make_install

rm -f %{buildroot}%{_infodir}/dir


%files
%license COPYING COPYING.GPL
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/*.so.*
%{_infodir}/%{name}.info*

%files devel
%{_includedir}/%{name}.h
%{_libdir}/*.so


%changelog
* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.11-1
- Initial spec
