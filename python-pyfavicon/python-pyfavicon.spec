%global pkgname pyfavicon

Name:           python-%{pkgname}
Version:        0.1.1
Release:        1%{?dist}
Summary:        Async favicon fetcher

License:        MIT
URL:            https://github.com/bilelmoussaoui/%{pkgname}

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-aiohttp
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-coveralls
BuildRequires:  python3-pillow
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
Requires:       python3-aiohttp
Requires:       python3-beautifulsoup4
Requires:       python3-pillow


%global _description\
pyfavicon is an async favicon fetcher.

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}

%description -n python3-%{pkgname}
%_description


%prep
%autosetup -n %{pkgname}-%{version} -p1


%build
%{__python3} setup.py build


%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}


%check
%{__python3} setup.py test


%files
%files -n python3-%{pkgname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}*-*.egg-info


%changelog
* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- Initial spec