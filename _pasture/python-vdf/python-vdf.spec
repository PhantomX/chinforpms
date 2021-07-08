%global commit 2b23d5b8a74f3e1d87e69c82eca7d2eeed26b7d4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210223
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname vdf

Name:           python-%{pkgname}
Version:        3.3
Release:        2%{?gver}%{?dist}
Summary:        Library for working with Valve's VDF text format

License:        MIT
URL:            https://github.com/ValvePython/vdf

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist mock}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-cov}


%description
Pure python module for (de)serialization to and from VDF that works just
like json.


%package     -n python3-%{pkgname}
Summary:        Library for working with Valve's VDF text format

%description -n python3-%{pkgname}
Pure python module for (de)serialization to and from VDF that works just
like json.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif


%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*-*.egg-info


%changelog
* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 3.3-2.20210223git2b23d5b
- Snapshot

* Mon Dec 28 2020 Phantom X <megaphantomx at hotmail dot com> - 3.3-1
- 3.3

* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.2-2
- Upstream patch

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2-1
- Initial spec
