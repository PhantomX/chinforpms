%global srcname pyctr

Name:           python-%{srcname}
Version:        0.7.5
Release:        1%{?dist}
Summary:        Python library to interact with Nintendo 3DS files

License:        MIT
URL:            https://github.com/ihaveamac/%{srcname}

Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pillow} >= 8.1
BuildRequires:  %{py3_dist pycryptodomex}


%global _description %{expand:
%{srcname} is a Python library to interact with Nintendo 3DS files.}

%description %_description

%package     -n python3-%{srcname}
Summary:        %{summary}
Requires:       %{py3_dist pycryptodomex}
Provides:       %{srcname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{srcname}
%_description


%prep
%autosetup -n %{srcname}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{srcname}


%check
%{__python3} setup.py test


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
* Sat Mar 16 2024 Phantom X <megaphantomx at hotmail dot com> - 0.7.5-1
- 0.7.5

* Sun Sep 05 2021 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-1
- 0.5.1
- Update to best packaging practices

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0.4.7-1
- 0.4.7

* Wed Jan 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.4.5-1
- Initial spec
