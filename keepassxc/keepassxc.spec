%global commit 5916a8f8dd93eb6a5de544caedd7a9d8e9a3b1ee
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220406
%bcond snapshot 0

%bcond check 0
%bcond yubikey 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global appname org.%{name}.KeePassXC

%global ver     %%(echo %{version} | tr '~' '-' | tr '_' '-')

Name:           keepassxc
Version:        2.7.10
Release:        100%{?dist}
Summary:        Cross-platform password manager
Epoch:          1

%global vc_url  https://github.com/keepassxreboot/%{name}

License:        BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND MIT AND OFL-1.1 AND LicenseRef-Fedora-Public-Domain
URL:            https://keepassxc.org/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/releases/download/%{ver}/%{name}-%{ver}-src.tar.xz
%dnl Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

# Patch0: fixes GNOME quirks on Wayland sessions
# Patch improved by pewpeww https://src.fedoraproject.org/rpms/keepassxc/pull-request/1
Patch0:         xcb.patch
%dnl Patch10:        0001-keepassxc-browser-add-Waterfox-support.patch


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  asciidoctor
BuildRequires:  pkgconfig(botan-2) >= 2.11.0
BuildRequires:  pkgconfig(libargon2)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Core) >= 5.2
BuildRequires:  pkgconfig(Qt5Concurrent) >= 5.2
BuildRequires:  pkgconfig(Qt5Gui) >= 5.2
BuildRequires:  pkgconfig(Qt5Network) >= 5.2
BuildRequires:  pkgconfig(Qt5Svg) >= 5.2
BuildRequires:  pkgconfig(Qt5Test) >= 5.2
BuildRequires:  pkgconfig(Qt5Widgets) >= 5.2
BuildRequires:  pkgconfig(Qt5X11Extras) >= 5.2
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(zlib) >= 1.2.0
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  readline-devel
%if %{defined fedora} && 0%{?fedora} >= 38 && 0%{?fedora} < 40
BuildRequires:  minizip-compat-devel
%endif
%if %{defined fedora} && 0%{?fedora} >= 40
BuildRequires:  minizip-ng-compat-devel
%endif
%if %{with yubikey}
BuildRequires:  libyubikey-devel
BuildRequires:  ykpers-devel
Provides:       bundled(ykcore)
%endif
Requires:       hicolor-icon-theme

%description
KeePassXC is a community fork of KeePassX, a native cross-platform
port of KeePass Password Safe, with the goal to extend and improve it
with new features and bugfixes to provide a feature-rich, fully
cross-platform and modern open-source password manager.
 
%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

%if %{with snapshot}
if [ ! -e .gitrev ] ;then
  echo "%{shortcommit}" > .gitrev
fi
%else
if [ ! -e .version ] ;then
  echo "%{version}" > .version
fi
%endif


%build
%cmake \
  -DCMAKE_BUILD_TYPE=release \
  -DKEEPASSXC_BUILD_TYPE:STRING=Release \
  %{!?with_check:-DWITH_TESTS:BOOL=OFF} \
  -DWITH_XC_NETWORKING:BOOL=ON \
  -DWITH_XC_AUTOTYPE:BOOL=ON \
  -DWITH_XC_BROWSER:BOOL=ON \
  -DWITH_XC_BROWSER_PASSKEYS:BOOL=ON \
  -DWITH_XC_FDOSECRETS:BOOL=ON \
  -DWITH_XC_SSHAGENT:BOOL=ON \
  -DWITH_XC_KEESHARE:BOOL=ON \
  -DWITH_XC_KEESHARE_SECURE:BOOL=ON \
  %{?with_yubikey:-DWITH_XC_YUBIKEY:BOOL=ON} \
  -DWITH_XC_UPDATECHECK:BOOL=OFF \
%{nil}

%cmake_build


%install

%cmake_install

desktop-file-edit \
  --add-mime-type="application/x-keepass" \
  --add-mime-type="application/x-keepassxc" \
  %{buildroot}%{_datadir}/applications/%{appname}.desktop

%find_lang %{name} --with-qt


%check
%if %{with check}
# 'testcli' fails with "Subprocess aborted" in Koji and local mock
%ctest --exclude-regex testcli
%endif
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml


%files -f %{name}.lang
%license COPYING LICENSE*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-proxy
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/docs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/wordlists
%{_datadir}/applications/*.desktop
%{_datadir}/man/man1/*.1*
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/*/*%{name}*
%{_metainfodir}/*.appdata.xml


%changelog
* Wed Mar 05 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.10-100
- 2.7.10

* Mon Jul 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.9-100
- 2.7.9

* Fri May 10 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.8-100
- 2.7.8

* Tue Mar 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.7-100
- 2.7.7

* Thu Aug 17 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.6-100
- 2.7.6

* Sun May 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.5-100
- 2.7.5

* Mon Oct 31 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.4-100
- 2.7.4

* Thu Oct 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.3-100
- 2.7.3

* Wed Jul 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.1-101
- Rebuild (qt5)

* Wed Apr 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.1-100
- 2.7.1

* Tue Mar 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.0-100
- 2.7.0

* Thu Mar 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.0~beta1-100
- 2.7.0-beta1
- BR: botan-2
- LTO is safe now

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.6-100
- 2.6.6

* Wed Jun 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.5-100
- 2.6.5

* Mon Feb 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.4-100
- 2.6.4

* Wed Jan 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.3-100
- 2.6.3

* Thu Oct 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.2-100
- 2.6.2

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.1-101
- Add missing BR

* Thu Aug 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.1-100
- 2.6.1

* Tue Jul 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.0-100
- 2.6.0

* Fri Apr 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.4-100
- 2.5.4

* Thu Jan 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.3-101
- Bump

* Tue Jan 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.3-100
- 2.5.3

* Sat Jan 04 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.2-100
- 2.5.2

* Tue Nov 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.1-100
- 2.5.1

* Sat Oct 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.0-100
- 2.5.0

* Tue Oct 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.4.3-101
- Conditional KeeShare support. BR: quazip-qt5-devel
- Browser support
- Waterfox support with browser

* Wed Jun 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.4.3-100
- 2.4.3

* Thu Jun 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.4.2-100
- 2.4.2
- BR: libsodium

* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.4.1-100
- 2.4.1

* Wed Mar 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.4.0-101
- Disable update check by default

* Wed Mar 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.4.0-100
- 2.4.0
- BR: Qt5Svg, libqrencode

* Thu Aug 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.3.4-100.chinfo
- 2.3.4

* Fri May 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.3.3-100.chinfo
- 2.3.3

* Tue May 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.3.2-100.chinfo
- 2.3.2

* Wed Mar 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.3.1-100.chinfo
- 2.3.1
- BR: gcc-c++
- Remove obsolete scriptlets

* Wed Feb 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.3.0-100.chinfo
- 2.3.0
- BR: libargon2
- BR: libcurl
- ssh-agent support
- Disable deprecated HTTP support and enable networking for website icons

* Fri Jan 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.2.4-100.chinfo
- 2.2.4

* Wed Dec 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.2.3-100.chinfo
- 2.2.3
- f27 sync

* Thu Oct 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.2.2-100.chinfo
- 2.2.2

* Thu Oct 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.2.1-100.chinfo
- 2.2.1

* Tue Jun 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.2.0-100.chinfo
- 2.2.0
- Conditional yubikey support

* Sun May 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1.4-100.chinfo
- Insanely high build number

* Fri Apr 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1.4-1
- 2.1.4

* Thu Mar 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1.3-1
- Initial spec
