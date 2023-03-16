%global commit f1cd763715e991e341d15da599d1877fd5040ce0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230130
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           c-vtapi
Version:        0.1
Release:        3%{?gver}%{?dist}
Summary:        VirusTotal C API library

License:        Apache-2.0
URL:            https://www.virustotal.com/

%global vc_url  https://github.com/VirusTotal/%{name}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(jansson)
BuildRequires:  pkgconfig(libcurl)

%package devel
Summary:        %{summary} development files
License:        Apache 2.0
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files libraries needed for
development with VirusTotal API integration.

%description
%{summary}.

%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

autoreconf -ivf

%build
%configure \
  --includedir=%{_includedir}/%{name} \
  --disable-static \
  --disable-silent-rules \
  --disable-doxygen-ps \
  --disable-doxygen-pdf \
  --disable-examples \
%{nil}

%make_build


%install
%make_install

find %{buildroot} -type f -name '*.la' -print -delete


%files
%license COPYING
%doc AUTHORS README.md
%{_libdir}/libcvtapi.so.*

%files devel
%license COPYING
%doc AUTHORS README.md
%{_libdir}/libcvtapi.so
%{_includedir}/%{name}/


%changelog
* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1-3.20230130gitf1cd763
- Update to fix README.md

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.1-2.20190710gitdae474e
- New snapshot

* Thu Aug 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1-1.20161228gitd771b66
- Initial spec
