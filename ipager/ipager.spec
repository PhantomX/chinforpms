Name:           ipager
Version:        1.1.0
Release:        4%{?dist}
Summary:        A themable desktop pager for fluxbox and other WMs

License:        MIT
URL:            http://www.useperl.ru/ipager/index.en.html
Source0:        https://slackware.uk/slacky/slackware-13.0/desktop/ipager/1.1.0/src/%{name}-%{version}.tar.gz
Source1:        %{name}-CMakeLists.txt

Patch0:         0001-Add-missing-header.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(imlib2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)


%description
ipager is a simple pager.


%prep
%autosetup -p1

cp -p %{S:1} CMakeLists.txt


%build
%cmake -G Ninja

%cmake_build


%install
%cmake_install

%files
%license LICENSE
%doc README
%{_bindir}/%{name}


%changelog
* Fri Sep 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-4
- Add cmake build support

* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-3
- Remove all imlib2-config references

* Sat Oct 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-2
- Unset compiler variables to please scons bullshit

* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1.0-1
- Initial spec
