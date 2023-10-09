%global commit d2696b5f64c206d6f0c5b82dfb7886875cb6a52a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20141223

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           pkgtool
Version:        0
Release:        1%{?dist}
Summary:        PS3 PKG tool

License:        GPL-3.0-or-later
URL:            https://github.com/kakaroto/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

Provides:       bundled(sha1-paulej)


%description
%{summary}.


%prep
%autosetup -n %{name}-%{commit} -p1

chmod +x ./autogen.sh
NOCONFIGURE=1 ./autogen.sh


%build
%configure
%make_build

%install
%make_install


%files
%license COPYING
%{_bindir}/%{name}


%changelog
* Sun Oct 08 2023 Phantom X <megaphantomx at hotmail dot com> - 0-1.20141223gitd2696b5
- Initial spec

