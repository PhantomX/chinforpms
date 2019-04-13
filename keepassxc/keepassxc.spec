%bcond_with yubikey

Name:           keepassxc
Version:        2.4.1
Release:        100%{?dist}
Summary:        Cross-platform password manager
Epoch:          1

License:        Boost and BSD and CC0 and GPLv3 and LGPLv2 and LGPLv2+ and LGPLv3+ and Public Domain
URL:            https://keepassxc.org/
Source0:        https://github.com/keepassxreboot/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  libgcrypt-devel >= 1.7.0
BuildRequires:  libgpg-error-devel
BuildRequires:  pkgconfig(libargon2)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Core) >= 5.2
BuildRequires:  pkgconfig(Qt5Concurrent) >= 5.2
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
%autosetup -p1

sed -e '/mandb -q/d' -i src/cli/CMakeLists.txt

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DCMAKE_BUILD_TYPE=release \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DKEEPASSXC_BUILD_TYPE:STRING=Release \
  -DWITH_TESTS:BOOL=OFF \
  -DWITH_XC_NETWORKING:BOOL=ON \
  -DWITH_XC_AUTOTYPE:BOOL=ON \
  -DWITH_XC_SSHAGENT:BOOL=ON \
  -DWITH_XC_YUBIKEY:BOOL=%{?_with_yubikey:ON}%{!?_with_yubikey:OFF} \
  -DWITH_XC_UPDATECHECK:BOOL=OFF \
%{nil}

%make_build

popd

%install

%make_install -C %{_target_platform}

desktop-file-edit \
  --add-mime-type="application/x-keepass" \
  --add-mime-type="application/x-keepassxc" \
  %{buildroot}%{_datadir}/applications/org.%{name}.KeePassXC.desktop

#install appdata files
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.%{name}.KeePassXC.appdata.xml

%find_lang keepassx --with-qt

%files -f keepassx.lang
%license COPYING LICENSE*
%doc CHANGELOG README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/wizard
%{_datadir}/%{name}/wordlists
%{_datadir}/applications/*.desktop
%{_datadir}/man/man1/*.1*
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/*/*%{name}*
%{_metainfodir}/*.appdata.xml


%changelog
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
