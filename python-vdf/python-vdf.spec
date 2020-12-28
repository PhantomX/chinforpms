%global pkgname vdf

Name:           python-%{pkgname}
Version:        3.3
Release:        1%{?dist}
Summary:        Library for working with Valve's VDF text format

License:        MIT
URL:            https://github.com/ValvePython/vdf
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz


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
* Mon Dec 28 2020 Phantom X <megaphantomx at hotmail dot com> - 3.3-1
- 3.3

* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.2-2
- Upstream patch

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2-1
- Initial spec
