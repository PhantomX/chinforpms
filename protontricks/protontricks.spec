Name:           protontricks
Version:        1.2.4
Release:        1%{?dist}
Summary:        A simple wrapper that does winetricks things for Proton enabled games

License:        GPLv3
URL:            https://github.com/Matoking/protontricks
Source0:        https://github.com/Matoking/protontricks/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-vdf
Requires:       winetricks
Suggests:       zenity


%description
%{summary}.


%prep
%autosetup -p1


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
* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.4-1
- Initial spec
