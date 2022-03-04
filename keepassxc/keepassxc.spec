%bcond_with keeshare
%bcond_with yubikey

%global appname org.%{name}.KeePassXC

%global ver     %%(echo %{version} | tr '~' '-' | tr '_' '-')

Name:           keepassxc
Version:        2.7.0~beta1
Release:        100%{?dist}
Summary:        Cross-platform password manager
Epoch:          1

%global vc_url  https://github.com/keepassxreboot/%{name}

License:        Boost and BSD and CC0 and GPLv3 and LGPLv2 and LGPLv2+ and LGPLv3+ and Public Domain
URL:            https://keepassxc.org/

Source0:        %{vc_url}/releases/download/%{ver}/%{name}-%{ver}-src.tar.xz

# Patch0: fixes GNOME quirks on Wayland sessions
# Patch improved by pewpeww https://src.fedoraproject.org/rpms/keepassxc/pull-request/1
Patch0:         xcb.patch
Patch10:        0001-keepassxc-browser-add-Waterfox-support.patch


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  asciidoctor
BuildRequires:  pkgconfig(botan-2)
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
%if %{with keeshare}
BuildRequires:  quazip-qt5-devel
%endif
%if %{with yubikey}
BuildRequires:  libyubikey-devel
BuildRequires:  ykpers-devel
%endif
Requires:       hicolor-icon-theme

%description
KeePassXC is a community fork of KeePassX, a native cross-platform
port of KeePass Password Safe, with the goal to extend and improve it
with new features and bugfixes to provide a feature-rich, fully
cross-platform and modern open-source password manager.
 
%prep
%autosetup -n %{name}-%{ver} -p1

%build
%cmake \
  -DCMAKE_BUILD_TYPE=release \
  -DKEEPASSXC_BUILD_TYPE:STRING=Release \
  -DWITH_TESTS:BOOL=OFF \
  -DWITH_XC_NETWORKING:BOOL=ON \
  -DWITH_XC_AUTOTYPE:BOOL=ON \
  -DWITH_XC_BROWSER:BOOL=ON \
  -DWITH_XC_FDOSECRETS:BOOL=ON \
  -DWITH_XC_SSHAGENT:BOOL=ON \
%if %{with keeshare}
  -DWITH_XC_KEESHARE:BOOL=ON \
  -DWITH_XC_KEESHARE_SECURE:BOOL=ON \
%endif
  -DWITH_XC_YUBIKEY:BOOL=%{?_with_yubikey:ON}%{!?_with_yubikey:OFF} \
  -DWITH_XC_UPDATECHECK:BOOL=OFF \
%{nil}

%cmake_build


%install

%cmake_install

desktop-file-edit \
  --add-mime-type="application/x-keepass" \
  --add-mime-type="application/x-keepassxc" \
  %{buildroot}%{_datadir}/applications/%{appname}.desktop

#install appdata files
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml

%find_lang %{name} --with-qt

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
