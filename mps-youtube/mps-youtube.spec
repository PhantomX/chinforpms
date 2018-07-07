Name:           mps-youtube
Version:        0.2.8
Release:        1%{?dist}
Summary:        Terminal based YouTube player and downloader 

License:        GPLv3
URL:            https://github.com/%{name}/%{name}
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch0:         %{name}-noupdatecheck.patch

BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
Requires:       ytdl
Requires:       youtube-dl
Requires:       python3-pafy >= 0.4.1


%description
%{name} is Terminal based YouTube player and downloader 

%prep
%autosetup -n %{name}-%{version} -p1

%build
%py3_build


%install
%py3_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README.rst
%{_bindir}/mpsyt
%{python3_sitelib}/mps_youtube
%{python3_sitelib}/*-*.egg-info
%{_datadir}/applications/%{name}.desktop


%changelog
* Fri Jul 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.8-1
- First spec
