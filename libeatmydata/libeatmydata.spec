%global commit df7ddeb0345104f25b5b7bb154bc6a008c8c8404
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180519
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           libeatmydata
Version:        131
Release:        1%{?dist}
Summary:        Library and utilities designed to disable fsync and friends

License:        GPL-3.0-only

URL:            https://www.flamingspork.com/projects/%{name}

%global vc_url https://github.com/stewartsmith/%{name}
%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Multilib-fix.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libtool


%description
%{name} is a small LD_PRELOAD library designed to (transparently)
disable fsync (and friends, like open(O_SYNC)). This has two side-effects:
making software that writes data safely to disk a lot quicker and making
this software no longer crash safe.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

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
* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 131-1
- 131

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 130-1
- 130

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 129-1
- 129

* Thu Oct 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 105-1.20180519gitdf7ddeb
- Initial spec
