%global with_yubikey  %{?_with_yubikey: 1} %{?!_with_yubikey: 0}

Name:           keepassxc
Version:        2.2.3
Release:        100.chinfo%{?dist}
Summary:        Cross-platform password manager
Epoch:          1

License:        Boost and BSD and CC0 and GPLv3 and LGPLv2 and LGPLv2+ and LGPLv3+ and Public Domain
URL:            https://keepassxc.org/
Source0:        https://github.com/keepassxreboot/%{name}/releases/download/%{version}/%{name}-%{version}-src.tar.xz
Patch1:         https://github.com/keepassxreboot/keepassxc/commit/4cfa687a3f56ba49f113161fb3a522b7493bfb17.patch#/Fixed-typo-in-XML-tag.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  pkgconfig(Qt5Core) >= 5.2
BuildRequires:  pkgconfig(Qt5Concurrent) >= 5.2
BuildRequires:  pkgconfig(Qt5Network) >= 5.2
BuildRequires:  pkgconfig(Qt5Test) >= 5.2
BuildRequires:  pkgconfig(Qt5Widgets) >= 5.2
BuildRequires:  pkgconfig(Qt5X11Extras) >= 5.2
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  qt5-linguist
%if %{with_yubikey}
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

# get rid of icon tag in appdata file
# icon tag is not allowed in desktop appdata file
sed -i '/\<icon/d' share/linux/org.%{name}.appdata.xml

%build
mkdir build
pushd build
%cmake .. \
  -DCMAKE_BUILD_TYPE=release \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DWITH_TESTS:BOOL=OFF \
  -DWITH_XC_HTTP:BOOL=ON \
  -DWITH_XC_AUTOTYPE:BOOL=ON \
%if %{with_yubikey}
  -DWITH_XC_YUBIKEY:BOOL=ON
%else
  -DWITH_XC_YUBIKEY:BOOL=OFF
%endif

%make_build

popd

%install

%make_install -C build
 
desktop-file-edit \
  --add-mime-type="application/x-keepass" \
  --add-mime-type="application/x-keepassxc" \
  %{buildroot}%{_datadir}/applications/org.%{name}.desktop

#install appdata files
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/org.%{name}.appdata.xml

%find_lang keepassx --with-qt

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  touch --no-create %{_datadir}/mime/packages &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f keepassx.lang
%license COPYING LICENSE*
%doc CHANGELOG README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/wordlists
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/*/*%{name}*
%{_datadir}/metainfo/*.appdata.xml


%changelog
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
