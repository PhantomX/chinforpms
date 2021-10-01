%global commit 6c6a795438c4f4b6afe972a049fe02c36b3a952d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210423
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global _legacy_common_support 1

Name:           ueberzug
Version:        18.1.9
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

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files %{name}


%check
%{__python3} setup.py test


%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitearch}/*.so


%changelog
* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 18.1.9-1
- 18.1.9
- Update to best packaging practices

* Mon Apr 26 2021 Phantom X <megaphantomx at hotmail dot com> - 18.1.8-1.20210423git6c6a795
- Initial spec
