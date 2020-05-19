%global commit 15998df6d5c4bf8f239a05b7444dd83dd942603f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200516
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname SDL_GameControllerDB

Name:           sdl_gamecontrollerdb
Version:        0
Release:        17%{?gver}%{?dist}
Summary:        A database of game controller mappings

License:        zlib and MIT
URL:            https://github.com/gabomdq/%{pkgname}
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  /usr/bin/pathfix.py

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

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" check.py


%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 check.py %{buildroot}%{_bindir}/gamecontrollerdb-check

mkdir -p %{buildroot}%{_datadir}/%{pkgname}
install -pm0644 gamecontrollerdb.txt %{buildroot}%{_datadir}/%{pkgname}/


%files
%license LICENSE
%doc README.md
%{_bindir}/gamecontrollerdb-check
%{_datadir}/%{pkgname}/gamecontrollerdb.txt


%changelog
* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-17.20200516git15998df
- Bump

* Mon Apr 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-16.20200408gitd2bb9a5
- New snapshot

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-15.20200315gitca01c94
- New snapshot from new clone

* Wed Feb 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-14.20200219gitb01222f
- Bump

* Sun Feb 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-13.20200118gitfed28b1
- New snapshot

* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-12.20191015git8ff133d
- New snapshot

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-11.20190802gitef8542c
- New snapshot

* Sun Jul 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-10.20190719gitdca1a62
- New snapshot

* Sun Jun 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-9.20190514gitd57f564
- New snapshot

* Mon May 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-8.20190501git935f886
- New snapshot

* Thu Apr 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-7.20190402gite411d95
- New snapshot

* Sat Mar 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-6.20190307git3182bfa
- New snapshot

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
