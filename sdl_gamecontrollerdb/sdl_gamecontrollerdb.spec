%global commit 40e3a34962e4edf6730bd941efdba89d0a95229a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190131
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname SDL_GameControllerDB

Name:           sdl_gamecontrollerdb
Version:        0
Release:        5%{?gver}%{?dist}
Summary:        A database of game controller mappings

License:        zlib and MIT
URL:            https://github.com/gabomdq/SDL_GameControllerDB
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  python3-devel

Provides:       %{pkgname} = %{version}-%{release}


%description
SDL_GameControllerDB is a community source database of game controller mappings
to be used with SDL2 Game Controller functionality.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit}
%else
%autosetup -n %{pkgname}-%{version}
%endif

sed -e '1s|/usr/bin/env python$|%{__python3}|' -i check.py


%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 check.py %{buildroot}%{_bindir}/gamecontrollerdb-check

mkdir -p %{buildroot}%{_datadir}/%{pkgname}
install -pm0644 gamecontrollerdb.txt %{buildroot}%{_datadir}/%{pkgname}/
install -pm0644 data/mapping_guide.png %{buildroot}%{_datadir}/%{pkgname}/

%files
%license LICENSE
%doc README.md
%{_bindir}/gamecontrollerdb-check
%{_datadir}/%{pkgname}/gamecontrollerdb.txt
%{_datadir}/%{pkgname}/mapping_guide.png


%changelog
* Fri Feb 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-5.20190131git40e3a34
- New snapshot

* Wed Dec 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-4.20181201git04ebce5
- New snapshot
- Install check script

* Thu Nov 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20181120git89224d5
- New snapshot

* Thu Sep 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20180925git2c1b295
- New snapshot

* Fri Sep 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20180818git276431b
- Initial spec
