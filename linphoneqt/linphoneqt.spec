Name:           linphoneqt
Version:        4.1.1
Release:        1%{?dist}
Summary:        Free VoIP and video softphone based on the SIP protocol

License:        GPLv2
URL:            http://www.linphone.org/
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  bcmatroska2-devel
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(belcard)
BuildRequires:  pkgconfig(belle-sip)
BuildRequires:  pkgconfig(belr)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(linphone)
BuildRequires:  pkgconfig(Qt5Core) >= 5.9
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5QuickControls2)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  python2
BuildRequires:  python2-six
BuildRequires:  pystache
BuildRequires:  qt5-linguist
Requires:       hicolor-icon-theme

%description
Linphone is a free VoIP and video softphone based on the SIP protocol.

%prep
%autosetup

echo '#define LINPHONE_QT_GIT_VERSION "%{version}-%{release}"' > src/app/gitversion.h

lrelease-qt5 assets/languages/*.ts

sed \
  -e 's|inphone|\0qt|g' \
  -i assets/linphone.desktop

%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
  -DENABLE_DBUS:BOOL=ON \
  -DENABLE_UPDATE_CHECK:BOOL=OFF

cp ../assets/languages/*.qm assets/languages/

%make_build

%install
%make_install -C builddir

rename linphone %{name} \
  %{buildroot}%{_bindir}/linphone* \
  %{buildroot}%{_datadir}/applications/linphone.desktop \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/linphone.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-tester
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/*-factory
%{_datadir}/%{name}/assistant/*.rc
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg


%changelog
* Sat Sep 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 4.1.1-1
- Initial spec
