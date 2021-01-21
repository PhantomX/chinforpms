%global pkgname pyfavicon

Name:           python-%{pkgname}
Version:        0.1.1
Release:        2%{?dist}
Summary:        Async favicon fetcher

License:        MIT
URL:            https://github.com/bilelmoussaoui/%{pkgname}

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist aiohttp}
BuildRequires:  %{py3_dist beautifulsoup4}
BuildRequires:  %{py3_dist coveralls}
BuildRequires:  %{py3_dist pillow}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-cov}


%global _description\
pyfavicon is an async favicon fetcher.

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       %{py3_dist aiohttp}
Requires:       %{py3_dist beautifulsoup4}
Requires:       %{py3_dist pillow}

%description -n python3-%{pkgname}
%_description


%prep
%autosetup -n %{pkgname}-%{version} -p1


%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files
%files -n python3-%{pkgname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}*-*.egg-info


%changelog
* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-2
- Fix requires

* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- Initial spec
