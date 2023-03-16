%global srcname setuptools-lint

Name:           python-%{srcname}
Version:        0.6.0
Release:        12%{?dist}
Summary:        This package expose pylint as a lint command into setup.py

License:        BSD-3-Clause
URL:            https://github.com/johnnoone/setuptools-pylint
Source0:        %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pylint

%description
This package expose pylint as a lint command into setup.py


%package     -n python3-%{srcname}
Summary:     This package expose pylint as a lint command into setup.py
Requires:    python3-pylint
%description -n python3-%{srcname}
This package expose pylint as a lint command into setup.py


%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files setuptools_lint


%check
%{__python3} setup.py test


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst NEWS.txt


%changelog
* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.0-12
- Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.6.0-10
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 11 2019 Mairi Dulaney <jdulaney@fedoraproject.org> - 0.6.0-2
- Minor tweak from package review

* Thu Apr 11 2019 Mairi Dulaney <jdulaney@fedoraproject.org> - 0.6.0-1
- Initial Packaging
