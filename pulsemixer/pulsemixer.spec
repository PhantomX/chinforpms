Name:           pulsemixer
Version:        1.4.0
Release:        1%{?dist}
Summary:        CLI and curses mixer for pulseaudio

License:        MIT
URL:            https://github.com/GeorgeFilipkin/pulsemixer
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Change volume step from 10 to 5
Patch0:         %{name}-volume-step.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       pulseaudio


%description
%{summary}.


%prep
%autosetup -p1

%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}*.egg-info/


%changelog
* Wed May 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.4.0-1
- Initial spec
