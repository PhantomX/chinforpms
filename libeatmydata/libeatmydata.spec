%global commit df7ddeb0345104f25b5b7bb154bc6a008c8c8404
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180519
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           libeatmydata
Version:        105
Release:        1%{?gver}%{?dist}
Summary:        Library and utilities designed to disable fsync and friends

License:        GPLv3

URL:            https://www.flamingspork.com/projects/%{name}

%global vc_url https://github.com/stewartsmith/%{name}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Multilib-fix.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool


%description
%{name} is a small LD_PRELOAD library designed to (transparently)
disable fsync (and friends, like open(O_SYNC)). This has two side-effects:
making software that writes data safely to disk a lot quicker and making
this software no longer crash safe.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit}
%else
%autosetup -n %{name}-%{name}-%{version}
%endif

if ! [ -x ./configure ] ;then
  autoreconf -ivf
fi


%build
%configure \
  --libdir=%{_libdir}/%{name} \
  --disable-static \
%{nil}

%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%files
%license COPYING
%doc AUTHORS README.md
%{_bindir}/eatmydata
%{_libexecdir}/eatmydata.sh
%{_libdir}/%{name}/%{name}.so


%changelog
* Thu Oct 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 105-1.20180519gitdf7ddeb
- Initial spec
