%global pkgname iniherit

Name:           python-%{pkgname}
Version:        0.3.9
Release:        1%{?dist}
Summary:        A ConfigParser subclass with file-specified inheritance

License:        MIT
URL:            https://github.com/cadithealth/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
#BuildRequires:  python3-coverage
#BuildRequires:  python3-nose
BuildRequires:  python3-six
Requires:       python3-six


%global _description\
%{pkgname} is a ConfigParser subclass with file-specified inheritance.

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}
Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{pkgname}
%_description


%prep
%autosetup -n %{pkgname}-%{version} -p1


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
%{_bindir}/%{pkgname}
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}*-*.egg-info


%changelog
* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.3.9-1
- Initial spec
