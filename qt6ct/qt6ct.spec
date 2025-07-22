%global commit 90b9f4538d0bf1af2816bb7e094ec323ff104e66
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211001
%bcond snapshot 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%global srcver %{commit}
%else
%global srcver %{version}
%endif

Summary:        Qt6 - Configuration Tool
Name:           qt6ct
Version:        0.10
Release:        102%{?dist}

License:        BSD-2-Clause
Url:            https://www.opencode.net/trialuser/qt6ct

%if %{with snapshot}
Source0:        %{url}/-/archive/%{commit}/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2
%endif
Source2:        60-%{name}.sh

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt6-rpm-macros
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-linguist
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  desktop-file-utils
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
Requires:       qt6-qtsvg

%description
This program allows users to configure Qt6 settings (theme, font, icons, etc.)
under DE/WM without Qt integration.

%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

cp -p %{S:2} .


%build
lrelease-qt6 src/qt6ct/translations/*.ts
%{qmake_qt6}

%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}

rm -fv %{buildroot}%{_libdir}/lib%{name}-common.so

mkdir -p %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d
install -pm0755 60-%{name}.sh \
  %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/60-%{name}.sh


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%doc AUTHORS README.md ChangeLog
%license COPYING
%{_bindir}/%{name}
%{_libdir}/lib%{name}-common.so.*
%{_qt6_plugindir}/platformthemes/libqt6ct.so
%{_qt6_plugindir}/styles/libqt6ct-style.so
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/colors/
%{_datadir}/%{name}/colors/*.conf
%dir %{_datadir}/%{name}/qss/
%{_datadir}/%{name}/qss/*.qss
%{_sysconfdir}/X11/xinit/xinitrc.d/60-%{name}.sh


%changelog
* Tue Jun 10 2025 Phantom X <megaphantomx at hotmail dot com> - 0.10-102
- Rebuild (qt6)

* Fri Apr 18 2025 Phantom X <megaphantomx at hotmail dot com> - 0.10-101
- Rebuild (qt6)

* Wed Mar 05 2025 Phantom X <megaphantomx at hotmail dot com> - 0.10-100
- 0.10
- Update URL
- Drop gtk3 binary

* Wed Feb 05 2025 Phantom X <megaphantomx at hotmail dot com> - 0.9-108
- Rebuild (qt6)

* Tue Dec 10 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9-107
- Rebuild (qt6)

* Fri Nov 01 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9-106
- Rebuild (qt6)

* Thu Jul 04 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9-105
- Rebuild (qt6)

* Tue May 28 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9-104
- Rebuild (qt6)

* Fri Apr 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9-103
- Rebuild (qt6)

* Sat Feb 17 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9-102
- Rebuild (qt6)

* Wed Oct 18 2023 Phantom X <megaphantomx at hotmail dot com> - 0.9-101
- Rebuild (qt6)

* Fri Sep 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.9-100
- 0.9

* Wed Jul 26 2023 Phantom X <megaphantomx at hotmail dot com> - 0.8-105
- Rebuild (qt6)

* Fri Jul 14 2023 Phantom X <megaphantomx at hotmail dot com> - 0.8-104
- Rebuild (qt6)

* Sat May 27 2023 Phantom X <megaphantomx at hotmail dot com> - 0.8-103
- Rebuild (qt6)

* Thu May 04 2023 Phantom X <megaphantomx at hotmail dot com> - 0.8-102
- Rebuild (qt6)

* Wed Mar 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.8-101
- Rebuild (qt6)

* Sun Mar 12 2023 Phantom X <megaphantomx at hotmail dot com> - 0.8-100
- 0.8

* Sun Nov 27 2022 Phantom X <megaphantomx at hotmail dot com> - 0.7-100
- 0.7

* Thu Sep 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6-100
- 0.6

* Wed Jul 27 2022 Phantom X <megaphantomx at hotmail dot com> - 0.5-104
- Rebuild (qt6)

* Sun Jan 23 2022 Phantom X <megaphantomx at hotmail dot com> - 0.5-103
- Update xinitrc.d

* Tue Jan 18 2022 Phantom X <megaphantomx at hotmail dot com> - 0.5-102
- Add xinitrc.d script

* Thu Nov 11 2021 Phantom X <megaphantomx at hotmail dot com> - 0.5-101
- Rebuild (qt6)

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 0.5-100
- 0.5
- Install a -gtk3 binary, to set style with GTK3 dialogs and prevent some
  crashes

* Sat Aug 28 2021 Martin Gansser <martinkg@fedora.com> - 0.4-2
- Add missing desktop file validation
- Add BR desktop-file-utils

* Wed Aug 11 2021 Martin Gansser <martinkg@fedora.com> - 0.4-1
- Update to 0.4
- Fix unowned directories

* Thu Jul 01 2021 Martin Gansser <martinkg@fedora.com> - 0.3-1
- Update to 0.3

* Mon Feb 08 2021 Martin Gansser <martinkg@fedora.com> - 0.2-1
- initial Build
