%global commit 9750f8cfab738d0ea08ccb8d8752b95f5c09df07
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230111
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           opentyrian
Version:        2.1
Release:        8%{?gver}%{?dist}
Summary:        An arcade-style vertical scrolling shooter

License:        GPL-2.0-only
URL:            https://github.com/%{name}/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://www.camanis.net/opentyrian/releases/%{name}-%{version}-src.tar.gz
%endif

Patch0:         %{name}-wild.patch


BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_net)
Requires:       tyrian-data >= 2.1
Requires:       hicolor-icon-theme

%description
Tyrian is an arcade-style vertical scrolling shooter. The story is set
in 20,031 where you play as Trent Hawkins, a skilled fighter-pilot
employed to fight Microsol and save the galaxy.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

sed -e '/\$(docdir)/d' -i Makefile


%build
%set_build_flags
export CFLAGS+=" -pedantic -Wall -Wextra -Wno-missing-field-initializers"
%make_build \
  prefix="%{_prefix}" \
  gamesdir="%{_datadir}" \
  VCS_IDREV="(echo %{version}-%{release})" \
  STRIP=/bin/true \
%{nil}

%install
%make_install \
  prefix="%{_prefix}" \
  gamesdir="%{_datadir}" \
%{nil}

mkdir -p %{buildroot}%{_datadir}/tyrian


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc README NEWS
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%dir %{_datadir}/tyrian
%{_mandir}/man6/%{name}.6*


%changelog
* Sat Jul 18 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1-7.20200718gita874e4e
- Bump

* Tue Jul 14 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1-6.20200703git8d40433
- New snapshot from github
- Update patchset

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.1-5.20180303git24df4a4651f7
- gcc 10 fix

* Thu Apr 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.1-4.20180303git24df4a4651f7
- Add some upstream and pull requests from default branch
- Disable mouse grabbing from start

* Mon Mar 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.1-3.20180303git24df4a4651f7
- New snapshot
- Remove obsolete scriptets

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-2.20170414gitdb67cf6eb3ae
- New snapshot

* Sun Jan 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-1.20170115gitf61ceced26a3
- Initial spec
