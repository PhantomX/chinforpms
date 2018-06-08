%global gitcommitid a76094bc69dc0cfab7f02ae0270c09175196f902
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global with_snapshot 0

Name:           fluxbox-chinfo-menu
Version:        5.0.1
Release:        1%{?dist}
Summary:        Menu generator for Fluxbox based on XDG

License:        GPLv3
URL:            https://github.com/PhantomX/fluxbox-chinfo-menu
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gettext
Requires:       fluxbox
Requires:       gettext
Requires:       xdgmenumaker >= 1.4
Requires:       xorg-x11-apps

%description
%{summary}.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{gitcommitid}
%else
%autosetup -n %{name}-%{version} -p0
%endif

%build
mkdir _build
pushd _build

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON
%make_build

popd

%install
%make_install -C _build

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc ChangeLog README
%{_bindir}/%{name}
%{_bindir}/fluxbox-dm-helper
%{_datadir}/%{name}


%changelog
* Wed Jun 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.0.1-1
- 5.0.1

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-2
- BR: gettext

* Sun Jan 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-1
- New release.

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 4.1.1-1
- Initial spec.
