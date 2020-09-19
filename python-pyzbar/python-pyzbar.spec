%global pkgname pyzbar

Name:           python-%{pkgname}
Version:        0.1.8
Release:        1%{?dist}
Summary:        A ctypes-based wrapper around the zbar barcode reader

License:        MIT
URL:            https://github.com/NaturalHistoryMuseum/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-numpy
BuildRequires:  python3-pillow
BuildRequires:  zbar
Requires:       python3-pillow
Requires:       zbar


%global _description\
%{pkgname} is a ctypes-based wrapper around the zbar barcode reader.

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
%license LICENSE.txt
%doc README.rst
%{_bindir}/read_zbar*
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}*-*.egg-info


%changelog
* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.1.8-1
- Initial spec
