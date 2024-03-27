Name:           lzlib
Version:        1.14
Release:        1%{?dist}
Summary:        A compression library for the lzip file format

License:        GPL-2.0-or-later
URL:            http://www.nongnu.org/lzip/%{name}.html

Source0:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz.sig

BuildRequires:  gcc
BuildRequires:  make


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
%set_build_flags
%configure \
  --disable-static \
  --enable-shared \
  --disable-ldconfig \
  CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" \
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
* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.14-1
- 1.14

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.13-1
- 1.13

* Sun Jan 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1.12-1
- 1.12

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.11-1
- Initial spec
