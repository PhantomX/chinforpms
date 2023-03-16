%global commit 528c69bf5ef616f4319c62b6aed34cd0c59a48c9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230212
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global zopfli_ver 1.0.3

Name:           maxcso
Version:        1.13.0
Release:        5%{?gver}%{?dist}
Summary:        Fast cso compressor

# maxcso - ISC
# 7-zip and p7zip - LGPLv2
# Zopfli - Apache 2.0
License:        ISC AND LGPL-2.1-or-later AND Apache-2.0
URL:            https://github.com/unknownbrackets/%{name}

%if 0%{?with_snapshot}
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
BuildRequires:  pkgconfig(lzmasdk-c)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  cmake(zopfli) >= %{zopfli_ver}


%description
A fast ISO to CSO compression program for use with PSP and PS2 emulators, which
uses multiple algorithms for best compression ratio.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

rm -rf lz4 libdeflate libuv zlib zopfli


%build
%set_build_flags
%make_build SYSTEM_LIBDEFLATE=1 SYSTEM_ZOPFLI=1 PREFIX=%{_prefix}


%install
%make_install SYSTEM_LIBDEFLATE=1 SYSTEM_ZOPFLI=1 PREFIX=%{_prefix}


%files
%license LICENSE.md
%doc README*.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
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
