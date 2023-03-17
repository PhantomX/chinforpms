%global srcname haccrypto

Name:           python-%{srcname}
Version:        0.1.2
Release:        1%{?dist}
Summary:        Nintendo Switch XTSN crypto for Python

License:        MIT
URL:            https://github.com/luigoalma/%{srcname}

Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

Patch0:         0001-gcc-13-build-fix.patch

BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++


%global _description %{expand:
%{srcname} is the Nintendo Switch XTSN crypto for Python.}

%description %_description

%package     -n python3-%{srcname}
Summary:        %{summary}
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


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.md
%doc README.md


%changelog
* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1.2-1
- 0.1.2

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-2
- BR: gcc
- BR: gcc-c++

* Sun Sep 05 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- 0.1.1
- Update to best packaging practices

* Wed Jan 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1.0-1
- Initial spec
