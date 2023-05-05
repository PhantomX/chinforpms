%global commit 90b9f4538d0bf1af2816bb7e094ec323ff104e66
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211001
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%global srcver %{commit}
%else
%global srcver %{version}
%endif

Summary:        Qt6 - Configuration Tool
Name:           qt6ct
Version:        0.8
Release:        102%{?dist}

License:        BSD-2-Clause
Url:            https://github.com/trialuser02/qt6ct

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.xz
%endif
Source1:        README.gtk3
Source2:        60-%{name}.sh

Patch0:         0001-gtk3-dialogs.patch

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
%setup -q -c

cp -a %{name}-%{srcver} %{name}-%{srcver}-gtk3

pushd %{name}-%{srcver}-gtk3

cp -a COPYING AUTHORS ChangeLog README ../

%patch -P 0 -p1 -b.gtk3
popd

cp -p %{S:1} .
cp -p %{S:2} .


%build
pushd %{name}-%{srcver}
lrelease-qt6 src/qt6ct/translations/*.ts
%{qmake_qt6}

%make_build
popd

pushd %{name}-%{srcver}-gtk3
lrelease-qt6 src/qt6ct/translations/*.ts
%{qmake_qt6}

ln -sf ../../../%{name}-%{version}/src/qt6ct-common/libqt6ct-common.so src/qt6ct-common/
%make_build sub-src-qt6ct-all
popd

%install
make install -C %{name}-%{srcver}-gtk3/src/qt6ct INSTALL_ROOT=%{buildroot}
mv %{buildroot}%{_bindir}/%{name}{,-gtk3}

make install -C %{name}-%{srcver} INSTALL_ROOT=%{buildroot}

rm -fv %{buildroot}%{_libdir}/lib%{name}-common.so

mkdir -p %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d
install -pm0755 60-%{name}.sh \
  %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/60-%{name}.sh

sed -e '/^Name/s|$| - GTK3|g' %{buildroot}/%{_datadir}/applications/%{name}.desktop \
  > %{buildroot}/%{_datadir}/applications/%{name}-gtk3.desktop

desktop-file-edit \
  --set-key="Exec" \
  --set-value="%{name}-gtk3" \
  %{buildroot}/%{_datadir}/applications/%{name}-gtk3.desktop


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%doc AUTHORS README ChangeLog README.gtk3
%license COPYING
%{_bindir}/%{name}*
%{_libdir}/lib%{name}-common.so.*
%{_qt6_plugindir}/platformthemes/libqt6ct.so
%{_qt6_plugindir}/styles/libqt6ct-style.so
%{_datadir}/applications/%{name}*.desktop
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/colors/
%{_datadir}/%{name}/colors/*.conf
%dir %{_datadir}/%{name}/qss/
%{_datadir}/%{name}/qss/*.qss
%{_sysconfdir}/X11/xinit/xinitrc.d/60-%{name}.sh


%changelog
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
