Name:           protontricks
Version:        1.4
Release:        1%{?dist}
Summary:        A simple wrapper that does winetricks things for Proton enabled games

License:        GPLv3
URL:            https://github.com/Matoking/protontricks
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         %{url}/commit/ca4ce8f4a70192332791d33f98b70c9442ed91df.patch#/%{name}-gh-ca4ce8f.patch
Patch10:        0001-Disable-setuptools_scm-version-check.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-vdf
Requires:       winetricks
Suggests:       zenity


%description
%{summary}.


%prep
%autosetup -p1

echo "version = '%{version}'" > src/protontricks/_version.py

%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}
%{python3_sitelib}/*-*.egg-info


%changelog
* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1
- 1.4
- Remove git BR

* Sat Nov 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1
- 1.3

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.5-1
- 1.2.5

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.4-1
- Initial spec
