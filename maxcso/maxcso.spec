%global commit 961f232cf99d546b2b7e704c0ecf3fc5bea52221
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240126
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global zopfli_ver 1.0.3

Name:           maxcso
Version:        1.13.0
Release:        7%{?dist}
Summary:        Fast cso compressor

# maxcso - ISC
# 7-zip and p7zip - LGPLv2
# Zopfli - Apache 2.0
License:        ISC AND LGPL-2.1-or-later AND Apache-2.0
URL:            https://github.com/unknownbrackets/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Use-system-libraries.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libdeflate-devel
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  cmake(zopfli) >= %{zopfli_ver}


%description
A fast ISO to CSO compression program for use with PSP and PS2 emulators, which
uses multiple algorithms for best compression ratio.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

rm -rf lz4 libdeflate libuv zlib zopfli


%build
%make_build USE_EXTERNAL_LIBDEFLATE=1 USE_EXTERNAL_ZOPFLI=1 PREFIX=%{_prefix}


%install
%make_install USE_EXTERNAL_LIBDEFLATE=1 USE_EXTERNAL_ZOPFLI=1 PREFIX=%{_prefix}


%files
%license LICENSE.md
%doc README*.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 1.13.0-7.20240126git961f232
- Rework external libraries fix

* Sat Dec 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1.13.0-3.20211208gita4b6f86
- Bump

* Thu Sep 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.13.0-2.20210704git26353b5
- Last snapshot
- System libdeflate

* Sun Jul 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.13.0-1.20210624gitec1b360
- 1.13.0
- System zopfli

* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.12.0-1
- 1.12.0

* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.11.0-1.20200504git26a4b1f
- Initial spec
