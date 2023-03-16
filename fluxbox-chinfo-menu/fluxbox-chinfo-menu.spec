%global commit 0d9bd8671fa98d68912528638fdd6398d96b6aba
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           fluxbox-chinfo-menu
Version:        5.1.0
Release:        2%{?gver}%{?dist}
Summary:        Menu generator for Fluxbox based on XDG

License:        GPL-3.0-only
URL:            https://github.com/PhantomX/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gettext
Requires:       fluxbox
Requires:       gettext
Requires:       xdgmenumaker >= 1.4
Requires:       xmessage
Requires:       xterm

%description
%{summary}.

%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

%build
%cmake \
%{nil}

%cmake_build


%install
%cmake_install

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc ChangeLog README
%{_bindir}/%{name}
%{_bindir}/fluxbox-dm-helper
%{_datadir}/%{name}/


%changelog
* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 5.1.0-2
- Replace xorg-x11-apps BR with split packages

* Mon Oct 19 2020 Phantom X <megaphantomx at hotmail dot com> - 5.1.0-1
- 5.1.0

* Fri Oct 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.0.2-1
- 5.0.2

* Wed Jun 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.0.1-1
- 5.0.1

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-2
- BR: gettext

* Sun Jan 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-1
- New release.

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 4.1.1-1
- Initial spec.
