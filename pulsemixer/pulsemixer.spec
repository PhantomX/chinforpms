%global commit 3d14c360734c0defef9a9c2206046331464e372b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190402
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           pulsemixer
Version:        1.5.1
Release:        2%{?gver}%{?dist}
Summary:        CLI and curses mixer for pulseaudio

License:        MIT
URL:            https://github.com/GeorgeFilipkin/pulsemixer
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

# Change volume step from 10 to 5
Patch0:         0001-Decrease-volume-step_big-to-5.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       pulseaudio-daemon


%description
%{summary}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif

%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}*.egg-info/


%changelog
* Tue Dec 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.5.1-2
- Requires pulseaudio-daemon

* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.5.1-1
- rebuilt

* Sun Jun 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-1
- 1.5.0

* Thu Apr 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4.0-2.20190402git3d14c36
- Update to snapshot

* Wed May 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.4.0-1
- Initial spec
