%global commit 826990b48f41d77e1280f5fa51082ed2f5115ddf
%global shortcommit %(c=%{commit}; echo ${c:0:12})
%global date 20190416

%global gver .%{date}hg%{shortcommit}

Name:           purple-rocketchat
Version:        0.9
Release:        1%{?gver}%{?dist}
Summary:        Rocket.Chat Plugin for libpurple

License:        GPLv3
URL:            https://bitbucket.org/EionRobb/%{name}

Source0:        %{url}/get/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libmarkdown)
BuildRequires:  pkgconfig(purple)


%description
purple-rocketchat adds support for Rocket.Chat to libpurple clients.


%prep
%autosetup -n EionRobb-%{name}-%{shortcommit} -p1

%build
%set_build_flags
export CFLAGS+=" -DROCKETCHAT_PLUGIN_VERSION=\\\"%{version}-%{release}\\\""
%make_build


%install
%make_install


%files
%license LICENSE
%doc README.md
%{_libdir}/purple-2/librocketchat.so
%{_datadir}/pixmaps/pidgin/protocols/*/rocketchat.*


%changelog
* Thu Jul 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.8-1.20190416git826990b48f41
- Initial spec
