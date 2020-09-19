%global pkgname yoyo-migrations

Name:           python-%{pkgname}
Version:        6.1.0
Release:        1%{?dist}
Summary:        Database migrations with SQL

License:        ASL 2.0
URL:            https://ollycope.com/software/yoyo/latest/

Source0:        https://files.pythonhosted.org/packages/source/y/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-iniherit
BuildRequires:  python3-text-unidecode
Requires:       python3-iniherit
Requires:       python3-text-unidecode


%global _description\
Yoyo is a database schema migration tool. Migrations are written as SQL files\
or Python scripts that define a list of migration steps.

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}

%description -n python3-%{pkgname}
%_description


%prep
%autosetup -n %{pkgname}-%{version} -p1

chmod -x *.rst *.txt

%build
%{__python3} setup.py build


%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}


%check
#{__python3} setup.py test


%files
%files -n python3-%{pkgname}
%license LICENSE.txt
%doc README.rst
%{_bindir}/yoyo*
%{python3_sitelib}/yoyo
%{python3_sitelib}/*-*.egg-info


%changelog
* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- Initial spec
