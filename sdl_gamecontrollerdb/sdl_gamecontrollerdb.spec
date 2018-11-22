%global gitcommitid 89224d5cbd85aa743d4dc7f8f197e714e21ac26e
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global date 20181120
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname SDL_GameControllerDB

Name:           sdl_gamecontrollerdb
Version:        0
Release:        3%{?gver}%{?dist}
Summary:        A database of game controller mappings

License:        zlib and MIT
URL:            https://github.com/gabomdq/SDL_GameControllerDB
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{gitcommitid}.tar.gz#/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
%endif

BuildArch:      noarch

Provides:       %{pkgname} = %{version}-%{release}


%description
SDL_GameControllerDB is a community source database of game controller mappings
to be used with SDL2 Game Controller functionality.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{gitcommitid}
%else
%autosetup -n %{pkgname}-%{version}
%endif


%build

%install
mkdir -p %{buildroot}%{_datadir}/%{pkgname}
install -pm0644 gamecontrollerdb.txt %{buildroot}%{_datadir}/%{pkgname}/
install -pm0644 data/mapping_guide.png %{buildroot}%{_datadir}/%{pkgname}/

%files
%license LICENSE
%doc README.md
%{_datadir}/%{pkgname}/gamecontrollerdb.txt
%{_datadir}/%{pkgname}/mapping_guide.png


%changelog
* Thu Nov 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20181120git89224d5
- New snapshot

* Thu Sep 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20180925git2c1b295
- New snapshot

* Fri Sep 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20180818git276431b
- Initial spec
