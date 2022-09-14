%global soversion 0

Name:           libdeflate
Version:        1.14
Release:        1%{?dist}
Summary:        Heavily optimized library for compression and decompression

License:        MIT
URL:            https://github.com/ebiggers/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(zlib)

%description
%{name} is a library for fast, whole-buffer DEFLATE-based compression and
decompression.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        progs
Summary:        Command-line programs distributed with %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    progs
%{name} is a library for fast, whole-buffer DEFLATE-based compression and
decompression.

This package contais command-line programs distributed with it.


%prep
%autosetup -p1

# Disable unneeded rebuild when make settings changes
sed \
  -e 's|^.build-config:|disabled_build-config:|g' \
  -e 's|\.build-config||g' \
  -i Makefile


%build
%set_build_flags
%make_build USE_SHARED_LIB=1
%make_build USE_SHARED_LIB=1 test_programs


%install
%make_install USE_SHARED_LIB=1 \
  PREFIX=%{_prefix} BINDIR=%{_bindir} INCDIR=%{_includedir} LIBDIR=%{_libdir}

pushd %{buildroot}%{_libdir}
mv %{name}.so.%{soversion} %{name}.so.%{version}
ln -sf %{name}.so.%{soversion} %{name}.so
popd

rm -f %{buildroot}%{_libdir}/*.a

%check
%make_build check


%files
%license COPYING
%doc README.md NEWS.md
%{_libdir}/%{name}.so.*

%files devel
%license COPYING
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files progs
%license COPYING
%{_bindir}/%{name}-*zip


%changelog
* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1.14-1
- 1.14

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.10-1
- 1.10

* Thu Sep 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.8-1
- Initial spec
