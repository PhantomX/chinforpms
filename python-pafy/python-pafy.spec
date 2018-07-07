%global pkgname pafy

Name:           python-%{pkgname}
Version:        0.5.4
Release:        1%{?dist}
Summary:        Python library to download YouTube content and retrieve metadata

License:        LGPLv3
URL:            https://github.com/mps-youtube/pafy
Source0:        %{url}/archive/v%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  youtube-dl


%description
Pafy a Python library to download YouTube content and retrieve metadata


%package     -n python3-%{pkgname}
Summary:        Python 3 library to download YouTube content and retrieve metadata

Requires:       youtube-dl

%{?python_provide:%python_provide python3-%{pkgname}}
Provides:       pafy = %{version}-%{release}

%description -n python3-%{pkgname}
%{summary}.


%package     -n ytdl
Summary:        YouTube Download Tool from pafy library

Requires:       python3-%{pkgname}

%description -n ytdl
%{summary}.

This is the from pafy library Download Tool.


%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build


%install
%py3_install


%files -n python3-%{pkgname}
%license GPLv3 LICENSE
%doc AUTHORS README.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*-*.egg-info


%files -n ytdl
%license GPLv3 LICENSE
%doc AUTHORS README.rst
%{_bindir}/ytdl


%changelog
* Fri Jul 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.5.4-1
- First spec
