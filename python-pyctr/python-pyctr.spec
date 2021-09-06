%global pkgname pyctr

Name:           python-%{pkgname}
Version:        0.5.1
Release:        1%{?dist}
Summary:        Python library to interact with Nintendo 3DS files

License:        MIT
URL:            https://github.com/ihaveamac/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pillow} >= 8.1
BuildRequires:  %{py3_dist pycryptodomex}


%global _description %{expand:
%{pkgname} is a Python library to interact with Nintendo 3DS files.}

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       %{py3_dist pycryptodomex}
Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{pkgname}
%_description


%prep
%autosetup -n %{pkgname}-%{version} -p1

%if 0%{?fedora} < 35
# Push this down for the time
sed -e 's|Pillow>=8.2|Pillow>=8.1|g' -i setup.py
%endif

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{pkgname}


%check
%{__python3} setup.py test


%files -n python3-%{pkgname} -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Sun Sep 05 2021 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-1
- 0.5.1
- Update to best packaging practices

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0.4.7-1
- 0.4.7

* Wed Jan 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.4.5-1
- Initial spec
