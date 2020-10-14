%global pkgname pyotp
%global vc_url  https://github.com/pyauth/%{pkgname}

Name:           python-%{pkgname}
Version:        2.4.0
Release:        1%{?dist}
Summary:        Python library for generating and verifying one-time passwords

License:        MIT
URL:            https://pyotp.readthedocs.io/

Source0:        %{vc_url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}

%global _description\
PyOTP is a Python 3 library for generating and verifying one-time passwords. It\
can be used to implement two-factor (2FA) or multi-factor (MFA) authentication\
methods in web applications and in other systems that require users to log in.

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
%doc README.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}*-*.egg-info


%changelog
* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 2.4.0-1
- Initial spec
