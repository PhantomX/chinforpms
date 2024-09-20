%global commit 71eb6e50adf0b4e6c7fcb426791bd3e72eae5a2b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240217
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global binname OpenJazz

Name:           openjazz
Version:        20240919
Release:        1%{?dist}
Summary:        A re-implemetantion of a known platform game engine

License:        GPL-2.0-or-later AND MIT
URL:            http://www.alister.eu/jazz/oj/

%global vc_url  https://github.com/AlisterT/%{name}
%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  asciidoctor
BuildRequires:  pkgconfig(sdl2)
Requires:       hicolor-icon-theme

Provides:       bundled(argparse) = 0~git
Provides:       bundled(miniz) = 0~git
Provides:       bundled(psmplug) = 0~git
Provides:       bundled(scale2x) = 0~git


%description
%{summary}.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p0


%build
%cmake

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_datadir}/pixmaps


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license COPYING licenses.txt
%doc README.md
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man6/%{binname}.6*


%changelog
* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 20240919-1
- 20240919

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 20231028-1.20240217git71eb6e5
- 20231028

* Tue Dec 01 2020 Phantom X <megaphantomx at hotmail dot com> - 20171024-4.20200422gitb8bb914
- Bump

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 20171024-3.20190505git030119c
- Bump

* Thu Nov 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 20171024-2.20180913git61a24c6
- New snapshot
- Drop desktop file, now installed by default
- Add manpage. BR: perl-podlators

* Mon Mar 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 20171024-1.20180219gitaf172ec
- Initial spec
