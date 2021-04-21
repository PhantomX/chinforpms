%global pkgname pyctr

Name:           python-%{pkgname}
Version:        0.4.7
Release:        1%{?dist}
Summary:        Python library to interact with Nintendo 3DS files

License:        MIT
URL:            https://github.com/ihaveamac/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pycryptodomex}


%global _description\
%{pkgname} is a Python library to interact with Nintendo 3DS files.

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       %{py3_dist pycryptodomex}
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
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}*-*.egg-info


%changelog
* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0.4.7-1
- 0.4.7

* Wed Jan 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.4.5-1
- Initial spec
