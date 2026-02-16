%bcond check 0

%global pkgname libpng

Summary:        A library of functions for manipulating PNG image format files
Name:           %{pkgname}-apng
Version:        1.6.55
Release:        1%{?dist}

License:        Zlib
URL:            https://sourceforge.net/projects/%{name}/

Source0:        https://github.com/glennrp/%{pkgname}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
Source1:        pngusr.dfa

# test files regenerated with downstream zlib
Source2:        pngtest.png
Source3:        pngtest-cicp-display-p3_reencoded.png

Patch0:         %{pkgname}-multilib.patch
Patch1:         https://downloads.sourceforge.net/sourceforge/libpng-apng/%{pkgname}-%{version}-apng.patch.gz
Patch2:         0001-autoconf-libpng-apng.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(zlib)
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make

%description
The %{name} package contains a library of functions for creating and
manipulating APNG (Animated Portable Network Graphics) image format files. PNG
is a bit-mapped graphics format similar to the GIF format. PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate APNG format image
Libpng should be installed if you need to manipulate APNG format image
files.

%package devel
Summary:       Development tools for programs to manipulate APNG image format files
Requires:      %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      zlib-devel%{?_isa} pkgconfig

%description devel
The %{name}-devel package contains header files and documentation necessary
for developing programs using the APNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate APNG image format
files, you should install %{name}-devel.  You'll also need to install
the libpng package.

%package static
Summary:       Static APNG image format file library
Requires:      %{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description static
The libpng-static package contains the statically linkable version of %{name}.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.


%prep
%autosetup -n %{pkgname}-%{version} -p1

# Provide pngusr.dfa for build.
cp -p %{SOURCE1} .

# use regenerated pngtest.png as we have newer zlib that provides slightly
# better compression which makes files differ and fail the pngtest-all test
cp -p %{SOURCE2} .
cp -p %{SOURCE3} contrib/testpngs/png-3/cicp-display-p3_reencoded.png

autoreconf -ivf

%build
%configure \
  --disable-tools \
%{nil}

%make_build DFA_XTRA=pngusr.dfa

%install
%make_install

# We don't ship .la files.
rm -f %{buildroot}%{_libdir}/*.la

rm -f %{buildroot}%{_includedir}/*.h
rm -rf %{buildroot}%{_mandir}

%if 0%{?with_check}
%check
make check
%endif

%files
%license LICENSE
%{_libdir}/%{name}*.so.*

%files devel
%doc libpng-manual.txt example.c TODO CHANGES
%{_bindir}/*
%{_includedir}/%{name}*
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%files static
%{_libdir}/%{name}*.a


%changelog
* Sun Feb 15 2026 Phantom X <megaphantomx at hotmail dot com> - 1.6.55-1
- 1.6.55

* Sat Jan 31 2026 Phantom X <megaphantomx at hotmail dot com> - 1.6.54-1
- 1.6.54

* Sun Dec 07 2025 Phantom X <megaphantomx at hotmail dot com> - 1.6.53-1
- 1.6.53

* Mon Dec 01 2025 Phantom X <megaphantomx at hotmail dot com> - 1.6.51-1
- 1.6.51

* Wed Oct 08 2025 Phantom X <megaphantomx at hotmail dot com> - 1.6.50-1
- Initial spec

