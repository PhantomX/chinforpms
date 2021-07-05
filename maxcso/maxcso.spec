%global commit ec1b360208e566cd589ddc825a525b1ebe2185a0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210624
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global zopfli_ver 1.0.3

Name:           maxcso
Version:        1.13.0
Release:        1%{?gver}%{?dist}
Summary:        Fast cso compressor

# maxcso - ISC
# 7-zip and p7zip - LGPLv2
# Zopfli - Apache 2.0
License:        ISC and and LGPLv2 and ASL 2.0
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
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  cmake(zopfli) >= %{zopfli_ver}


%description
A fast ISO to CSO compression program for use with PSP and PS2 emulators, which
uses multiple algorithms for best compression ratio.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

rm -rf lz4 libuv zlib zopfli

sed -e 's|`pkg-config --libs|$(LDFLAGS) \0|' -i Makefile


%build
%set_build_flags
%make_build SYSTEM_ZOPFLI=1 PREFIX=%{_prefix}


%install
%make_install SYSTEM_ZOPFLI=1 PREFIX=%{_prefix}


%files
%license LICENSE.md
%doc README*.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Sun Jul 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.13.0-1.20210624gitec1b360
- 1.13.0
- System zopfli

* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.12.0-1
- 1.12.0

* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.11.0-1.20200504git26a4b1f
- Initial spec
