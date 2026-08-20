%undefine _cmake_shared_libs

%global srcname10 brotli
%global srcname10_ver 1.2.0

%global commit11 156c7b75ae9b8c3b3f847acf264f17594c3859fb
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 boringssl

%global srcname12 nghttp2
%global srcname12_ver 1.63.0

%global srcname13 ngtcp2
%global srcname13_ver 1.20.0

%global srcname14 nghttp3 
%global srcname14_ver 1.15.0

%global srcname15 curl 
%global srcname15_ver curl-8_21_0

%global srcname16 zlib
%global srcname16_ver 1.3.1

%global srcname17 zstd
%global srcname17_ver 1.5.7

%global srcname18 libidn2
%global srcname18_ver 2.3.7


Name:           curl-impersonate
Version:        2.1.0
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
Source11:       https://github.com/google/%{srcname11}/archive/%{commit11}/%{srcname11}-%{commit11}.zip
Source110:      %{name}-boringssl-no-werror.patch
Source12:       https://github.com/%{srcname12}/%{srcname12}/releases/download/v%{srcname12_ver}/%{srcname12}-%{srcname12_ver}.tar.bz2
Source13:       https://github.com/%{srcname13}/%{srcname13}/releases/download/v%{srcname13_ver}/%{srcname13}-%{srcname13_ver}.tar.bz2
Source14:       https://github.com/%{srcname13}/%{srcname14}/releases/download/v%{srcname14_ver}/%{srcname14}-%{srcname14_ver}.tar.bz2
Source15:       https://github.com/%{srcname15}/%{srcname15}/archive/%{srcname15_ver}.tar.gz
Source16:       https://github.com/madler/%{srcname16}/releases/download/v%{srcname16_ver}/%{srcname16}-%{srcname16_ver}.tar.gz
Source17:       https://github.com/facebook/%{srcname17}/releases/download/v%{srcname17_ver}/%{srcname17}-%{srcname17_ver}.tar.gz
Source18:       https://ftp.gnu.org/gnu/libidn/%{srcname18}-%{srcname18_ver}.tar.gz

Patch0:         https://gitlab.archlinux.org/archlinux/packaging/packages/%{name}/-/raw/f0e407566499d479b55791fcdae3b9bdaf2fb590/no-download.patch#/%{name}-archlinux-no-download.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  golang
BuildRequires:  make
BuildRequires:  ninja-build


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

mkdir -p %{_vpath_builddir}/deps/downloads

cp -a \
  %{S:10} %{S:11} %{S:12} %{S:13} %{S:14} %{S:15} %{S:16} %{S:17} %{S:18} \
  %{_vpath_builddir}/deps/downloads

cat %{S:110} >> patches/boringssl.patch


%build
%make_build prepare-libidn2 BUILD_DIR=%{_vpath_builddir}

%cmake \
  -DCURL_CA_PATH:STRING=%{_sysconfdir}/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
%{nil}

%cmake_build

pushd %{_vpath_builddir}/deps/src
cp -p %{srcname10}/LICENSE ../../../LICENSE.brotli
cp -p %{srcname11}/LICENSE ../../../LICENSE.boringssl
cp -p %{srcname12}/COPYING ../../../COPYING.nghttp2
cp -p %{srcname13}/COPYING ../../../COPYING.ngtcp2
cp -p %{srcname14}/COPYING ../../../COPYING.nghttp3
cp -p %{srcname15}/COPYING ../../../COPYING.curl
cp -p %{srcname16}/LICENSE ../../../LICENSE.zlib
cp -p %{srcname17}/COPYING ../../../COPYING.zstd
cp -p %{srcname18}/COPYING ../../../COPYING.libidn2
popd


%install
%cmake_install

mv %{buildroot}%{_includedir}/curl %{buildroot}%{_includedir}/%{name}

rm -fv %{buildroot}%{_libdir}/*.{la,a}


%files
%license LICENSE
%license COPYING.* LICENSE.*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/curl_*

%files libs
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so


%changelog
* Thu Aug 20 2026 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-1
- 2.1.0

* Sun Jun 14 2026 Phantom X <megaphantomx at hotmail dot com> - 1.5.6-1
- Initial spec

