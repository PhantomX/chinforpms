%global commit 26a4b1f4963dcf7fa885994f44bd632309701a68
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200504
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           maxcso
Version:        1.12.0
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

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(zlib)


%description
A fast ISO to CSO compression program for use with PSP and PS2 emulators, which
uses multiple algorithms for best compression ratio.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

rm -rf lz4 libuv zlib

sed -e 's|-luv -llz4 -lz|$(LDFLAGS) \0|' -i Makefile


%build
%set_build_flags
%make_build PREFIX=%{_prefix}


%install
%make_install PREFIX=%{_prefix}


%files
%license LICENSE.md
%doc README*.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.12.0-1
- 1.12.0

* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.11.0-1.20200504git26a4b1f
- Initial spec
