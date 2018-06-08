%global commit d771b6612534ab8bf518a556d0303df43d1e0a12
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20161228
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           c-vtapi
Version:        0.1
Release:        1%{?gver}%{?dist}
Summary:        VirusTotal C API library

License:        ASL 2.0 
URL:            https://www.virustotal.com/
%if 0%{?with_snapshot}
Source0:        https://github.com/VirusTotal/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/VirusTotal/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
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
%if 0%{?with_snapshot}
# README.md is a broken symlink
%setup -T -c
tar xvf %{SOURCE0} --exclude=README.md --strip-components=1
%else
%autosetup -n %{name}-%{version}
%endif

autoreconf -ivf

%build
%configure \
  --includedir=%{_includedir}/%{name} \
  --disable-static \
  --disable-silent-rules \
  --disable-doxygen-ps \
  --disable-doxygen-pdf \
  --disable-examples
%make_build


%install
%make_install

find %{buildroot} -type f -name '*.la' -print -delete


%files
%license COPYING
%doc AUTHORS README
%{_libdir}/libcvtapi.so.*

%files devel
%license COPYING
%doc AUTHORS README
%{_libdir}/libcvtapi.so
%{_includedir}/%{name}


%changelog
* Thu Aug 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1-1.20161228gitd771b66
- Initial spec
