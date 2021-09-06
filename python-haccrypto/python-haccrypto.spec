%global pkgname haccrypto

Name:           python-%{pkgname}
Version:        0.1.1
Release:        1%{?dist}
Summary:        Nintendo Switch XTSN crypto for Python

License:        MIT
URL:            https://github.com/luigoalma/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz


BuildRequires:  python3-devel


%global _description %{expand:
%{pkgname} is the Nintendo Switch XTSN crypto for Python.}

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}
Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{pkgname}
%_description


%prep
%autosetup -n %{pkgname}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{pkgname}


%files -n python3-%{pkgname} -f %{pyproject_files}
%license LICENSE.md
%doc README.md


%changelog
* Sun Sep 05 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- 0.1.1
- Update to best packaging practices

* Wed Jan 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1.0-1
- Initial spec
