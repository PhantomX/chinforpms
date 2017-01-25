%global gitcommitid e5e8c89a313637778ac730533c2d6b9c9254da75
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global use_git 1

%if 0%{?use_git}
%global gver .git%{shortcommit}
%endif

Name:           bitlbee-facebook
Version:        1.0.0
Release:        3%{?gver}%{?dist}
Summary:        Facebook MQPP protocol module for bitlbee

License:        GPLv2
URL:            https://github.com/bitlbee/bitlbee-facebook
%if 0%{?use_git}
Source0:        https://github.com/bitlbee/%{name}/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/bitlbee/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  bitlbee-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  json-glib-devel
BuildRequires:  zlib-devel
Requires:       bitlbee

%description
%{summary}

%prep
%if 0%{?use_git}
%autosetup -n %{name}-%{gitcommitid}
%else
%autosetup -n %{name}-%{version}
%endif

sed -i -e '/\/configure/d' autogen.sh
./autogen.sh

%build
%configure --disable-silent-rules
%make_build

%install
rm -rf %{buildroot}

%make_install

find %{buildroot} -type f -name '*.la' -print -delete

%files
%license COPYING
%doc AUTHORS README
%{_libdir}/bitlbee/facebook.so

%changelog
* Sat Jan 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.0-3.gite5e8c89
- New snapshot

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.0.0-2
- rebuilt

* Sun Jun 26 2016 Phantom X
- Latest master.

* Sat Jan 23 2016 Phantom X
- 1.0.0.
