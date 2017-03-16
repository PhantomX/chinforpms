Name:           keepassxc
Version:        2.1.3
Release:        1%{?dist}
Summary:        Cross-platform password manager
Group:          User Interface/Desktops

License:        GPLv2 or GPLv3
URL:            https://keepassxc.org/
Source0:        https://github.com/keepassxreboot/%{name}/releases/download/%{version}/%{name}-%{version}-src.tar.xz

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
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
Requires:       hicolor-icon-theme
Requires(post): desktop-file-utils shared-mime-info
Requires(postun): desktop-file-utils gtk-update-icon-cache shared-mime-info
Requires(posttrans): gtk-update-icon-cache shared-mime-info

%description
eePassXC is a community fork of KeePassX, a native cross-platform
port of KeePass Password Safe, with the goal to extend and improve it
with new features and bugfixes to provide a feature-rich, fully
cross-platform and modern open-source password manager.
 
%prep
%autosetup

%build
mkdir build
pushd build
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DWITH_TESTS:BOOL=OFF \
  -DWITH_XC_HTTP:BOOL=ON \
  -DWITH_XC_AUTOTYPE:BOOL=ON
 
%make_build

popd

%install

%make_install -C build
 
desktop-file-edit \
  --add-mime-type="application/x-keepass" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
 
%find_lang keepassx --with-qt

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :
update-desktop-database &>/dev/null ||:
 
%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  touch --no-create %{_datadir}/mime/packages &>/dev/null || :
  update-mime-database %{_datadir}/mime &>/dev/null || :
fi
update-desktop-database &>/dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &>/dev/null || :

%files -f keepassx.lang
%license COPYING LICENSE*
%doc CHANGELOG README.md
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/icons
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/*/*

 
%changelog
* Thu Mar 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1.3-1
- Initial spec