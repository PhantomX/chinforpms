%global pkgname vdf

Name:           python-%{pkgname}
Version:        3.2
Release:        2%{?dist}
Summary:        Library for working with Valve's VDF text format

License:        MIT
URL:            https://github.com/ValvePython/vdf
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

Patch0:         %{url}/commit/ffbec10ae6bd6514398f67bbe2170a7e9a189349.patch#/%{name}-gh-ffbec10.patch


BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov


%description
Pure python module for (de)serialization to and from VDF that works just
like json.


%package     -n python3-%{pkgname}
Summary:        Library for working with Valve's VDF text format

%description -n python3-%{pkgname}
Pure python module for (de)serialization to and from VDF that works just
like json.


%prep
%autosetup -n %{pkgname}-%{version} -p1


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
* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.2-2
- Upstream patch

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2-1
- Initial spec
