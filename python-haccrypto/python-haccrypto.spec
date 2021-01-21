%global pkgname haccrypto

Name:           python-%{pkgname}
Version:        0.1.0
Release:        1%{?dist}
Summary:        Nintendo Switch XTSN crypto for Python

License:        MIT
URL:            https://github.com/luigoalma/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz


BuildRequires:  python3-devel


%global _description\
%{pkgname} is the Nintendo Switch XTSN crypto for Python.

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}
Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

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
%license LICENSE.md
%doc README.md
%{python3_sitearch}/%{pkgname}
%{python3_sitearch}/%{pkgname}*-*.egg-info


%changelog
* Wed Jan 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1.0-1
- Initial spec
