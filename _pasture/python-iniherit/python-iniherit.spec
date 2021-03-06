%global pkgname iniherit

Name:           python-%{pkgname}
Version:        0.3.9
Release:        2%{?dist}
Summary:        A ConfigParser subclass with file-specified inheritance

License:        MIT
URL:            https://github.com/cadithealth/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
#BuildRequires:  %%{py3_dist coverage}
#BuildRequires:  %%{py3_dist nose}
BuildRequires:  %{py3_dist six}


%global _description\
%{pkgname} is a ConfigParser subclass with file-specified inheritance.

%description %_description

%package     -n python3-%{pkgname}
Summary:        %{summary}
Requires:       %{py3_dist six}
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
#{__python3} setup.py test


%files
%files -n python3-%{pkgname}
%license LICENSE.txt
%doc README.rst
%{_bindir}/%{pkgname}
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/%{pkgname}*-*.egg-info


%changelog
* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 0.3.9-2
- Fix requires

* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.3.9-1
- Initial spec
