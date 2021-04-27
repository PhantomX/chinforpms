%global commit 6c6a795438c4f4b6afe972a049fe02c36b3a952d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210423
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global _legacy_common_support 1

Name:           ueberzug
Version:        18.1.8
Release:        1%{?gver}%{?dist}
Summary:        A cli util which allows to display images in combination with X11 

License:        GPLv3
URL:            https://github.com/seebye/ueberzug

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist attrs}
BuildRequires:  %{py3_dist docopt}
BuildRequires:  %{py3_dist pillow}
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xres)

Provides:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Überzug is a command line util which allows to draw images on terminals by
using child windows.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}*.egg-info

%changelog
* Mon Apr 26 2021 Phantom X <megaphantomx at hotmail dot com> - 18.1.8-1.20210423git6c6a795
- Initial spec
