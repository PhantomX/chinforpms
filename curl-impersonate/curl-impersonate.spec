%global srcname10 brotli
%global srcname10_ver 1.2.0

%global commit11 673e61fc215b178a90c0e67858bbf162c8158993
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 boringssl

%global srcname12 nghttp2
%global srcname12_ver 1.63.0

%global srcname13 ngtcp2
%global srcname13_ver 1.20.0

%global srcname14 nghttp3 
%global srcname14_ver 1.15.0

%global srcname15 curl 
%global srcname15_ver curl-8_15_0

%global srcname16 zlib
%global srcname16_ver 1.3.1

%global srcname17 zstd
%global srcname17_ver 1.5.6

%global srcname18 libunistring
%global srcname18_ver 1.1

%global srcname19 libidn2
%global srcname19_ver 2.3.7


Name:           curl-impersonate
Version:        1.5.6
Release:        1%{?dist}
Summary:        A build of curl that impersonates four major browsers

License:        %{shrink:
    MIT AND
    Apache-2.0 AND
    curl AND
    zlib AND
    BSD-3-Clause OR GPL-2.0-only AND
    GPL-2.0-or-later OR LGPL-3.0-or-later AND
    (GPL-2.0-or-later OR LGPL-3.0-or-later) AND GPL-3.0-or-later
}
URL:            https://github.com/lexiforest/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Source10:       https://github.com/google/%{srcname10}/archive/v%{srcname10_ver}/%{srcname10}-%{srcname10_ver}.tar.gz
Source11:       https://github.com/google/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       https://github.com/%{srcname12}/%{srcname12}/releases/download/v%{srcname12_ver}/%{srcname12}-%{srcname12_ver}.tar.bz2
Source13:       https://github.com/%{srcname13}/%{srcname13}/releases/download/v%{srcname13_ver}/%{srcname13}-%{srcname13_ver}.tar.bz2
Source14:       https://github.com/%{srcname13}/%{srcname14}/releases/download/v%{srcname14_ver}/%{srcname14}-%{srcname14_ver}.tar.bz2
Source15:       https://github.com/%{srcname15}/%{srcname15}/archive/%{srcname15_ver}.tar.gz
Source16:       https://github.com/madler/%{srcname16}/releases/download/v%{srcname16_ver}/%{srcname16}-%{srcname16_ver}.tar.gz
Source17:       https://github.com/facebook/%{srcname17}/releases/download/v%{srcname17_ver}/%{srcname17}-%{srcname17_ver}.tar.gz
Source18:       https://ftp.gnu.org/gnu/%{srcname18}/%{srcname18}-%{srcname18_ver}.tar.gz
Source19:       https://ftp.gnu.org/gnu/libidn/%{srcname19}-%{srcname19_ver}.tar.gz

Patch0:         https://gitlab.archlinux.org/archlinux/packaging/packages/%{name}/-/raw/7b58fd367130c71b607c9c06a820215be08a7998/no-download.patch#/%{name}-archlinux-no-download.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make


%description
A special build of curl that can impersonate the four major browsers: Chrome,
Edge, Safari and Firefox. curl-impersonate is able to perform TLS and HTTP
handshakes that are identical to that of a real browser.


%package libs
Summary:        %{summary} library
Provides:       bundled(srcname10) = %{?srcname10_ver}
Provides:       bundled(srcname11) = 0~git%{?shortcommit11}
Provides:       bundled(srcname12) = %{?srcname12_ver}
Provides:       bundled(srcname13) = %{?srcname13_ver}
Provides:       bundled(srcname14) = %{?srcname14_ver}
Provides:       bundled(srcname15) = %{?srcname15_ver}
Provides:       bundled(srcname16) = %{?srcname16_ver}
Provides:       bundled(srcname17) = %{?srcname17_ver}
Provides:       bundled(srcname18) = %{?srcname18_ver}
Provides:       bundled(srcname19) = %{?srcname19_ver}

%description libs
The %{name}-libs package contains the dynamic libraries needed for %{name} and
applications.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1

tar -xf %{S:10}
tar -xf %{S:11}
tar -xf %{S:12}
tar -xf %{S:13}
tar -xf %{S:14}
tar -xf %{S:15}
mv %{srcname15}-%{srcname15_ver} %{srcname15_ver}
tar -xf %{S:16}
tar -xf %{S:17}
tar -xf %{S:18}
tar -xf %{S:19}

cp -p %{srcname10}-%{srcname10_ver}/LICENSE LICENSE.brotli
cp -p %{srcname11}-%{commit11}/LICENSE LICENSE.boringssl
cp -p %{srcname12}-%{srcname12_ver}/COPYING COPYING.nghttp2
cp -p %{srcname13}-%{srcname13_ver}/COPYING COPYING.ngtcp2
cp -p %{srcname14}-%{srcname14_ver}/COPYING COPYING.nghttp3
cp -p %{srcname15_ver}/COPYING COPYING.curl
cp -p %{srcname16}-%{srcname16_ver}/LICENSE LICENSE.zlib
cp -p %{srcname17}-%{srcname17_ver}/COPYING COPYING.zstd
cp -p %{srcname18}-%{srcname18_ver}/COPYING COPYING.libunistring
cp -p %{srcname19}-%{srcname19_ver}/COPYING COPYING.libidn2

autoreconf -ivf


%build
%configure \
  --with-ca-bundle=%{_sysconfdir}/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
%{nil}

%make_build build -j1


%install
%make_install

if [ "%{_prefix}/lib" != "%{_libdir}" ] ;then
  mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
fi
mv %{buildroot}%{_includedir}/curl %{buildroot}%{_includedir}/%{name}

rm -f %{buildroot}%{_bindir}/%{name}-config
rm -fv %{buildroot}%{_libdir}/*.{la,a}


%files
%license LICENSE
%license COPYING.* LICENSE.*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/curl_*
%{_bindir}/w%{name}

%files libs
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so


%changelog
* Sun Jun 14 2026 Phantom X <megaphantomx at hotmail dot com> - 1.5.6-1
- Initial spec

