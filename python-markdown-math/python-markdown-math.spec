%global pkgname pymarkups

Name:           python-markdown-math
Version:        0.7
Release:        1%{?dist}
License:        BSD
Summary:        A math extension for Python-Markdown

URL:            https://pypi.org/project/python-markdown-math
Source0:        https://github.com/mitya57/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-markdown
BuildRequires:  python3-setuptools

BuildArch:      noarch

%global _description\
This module provides a Python 2 extension adds math formulas support to\
Python-Markdown.

%description %_description

%package -n python3-markdown-math
Summary:        A math extension for Python-Markdown

Requires:       python3-docutils
Requires:       python3-markdown

%{?python_provide:%python_provide python3-markdown-math}


%description -n python3-markdown-math
This module provides a Python 3 extension adds math formulas support to
Python-Markdown.


%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test -v

%files -n python3-markdown-math
%doc changelog README.md
%license LICENSE
%{python3_sitelib}/*


%changelog
* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 0.7-1
- 0.7

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.6-1
- Initial spec
