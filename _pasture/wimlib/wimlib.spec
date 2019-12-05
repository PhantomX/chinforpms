Name:           wimlib
Version:        1.12.0
Release:        1%{?dist}
Summary:        Windows Imaging (WIM) library

License:        GPLv3+ and CC0
URL:            https://wimlib.net

Source0:        %{url}/downloads/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(libcrypto)
# Library license can be LGPLv3+ if not linked with libntfs-3g
BuildRequires:  pkgconfig(libntfs-3g)
BuildRequires:  pkgconfig(libxml-2.0)
# For mkwinpeimg
Requires:       cabextract
Requires:       mtools
Requires:       syslinux
Requires:       /usr/bin/mkisofs


%description
%{name} is an open source, cross-platform library for creating,
extracting, and modifying Windows Imaging (WIM) archives.


%package tools
Summary:        %{summary} command line tools

%description tools
%{name} is an open source, cross-platform library for creating,
extracting, and modifying Windows Imaging (WIM) archives.

This package contains the command line tools to manipulate the archive
format.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --with-libcrypto

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

find %{buildroot} -name '*.la' -delete


%files
%license COPYING COPYING.GPLv3
%doc README
%{_libdir}/libwim.so.*

%files tools
%{_bindir}/*
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libwim.so


%changelog
* Tue Oct 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.12.0-1
- Initial spec
