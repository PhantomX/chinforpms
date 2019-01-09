%global gh_url  https://github.com/BelledonneCommunications/linphone-desktop

Name:           linphoneqt
Version:        4.1.1
Release:        4%{?dist}
Summary:        Free VoIP and video softphone based on the SIP protocol

License:        GPLv2
URL:            http://www.linphone.org/
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

# Qt 5.10 and 5.11 fixes, taken from openSUSE 
Patch0:         linphoneqt-fix-cmake-i18n.patch
Patch1:         linphoneqt-force-default-style.patch
Patch2:         linphoneqt-fix-qt-5.11.patch
Patch3:         linphoneqt-qt-5.9-fix-buttons.patch


BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  bcmatroska2-devel
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(belcard)
BuildRequires:  pkgconfig(belle-sip)
BuildRequires:  pkgconfig(belr)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(linphone)
BuildRequires:  pkgconfig(Qt5)
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
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Requires:       hicolor-icon-theme

%description
Linphone is a free VoIP and video softphone based on the SIP protocol.

%prep
%autosetup -p1

echo '#define LINPHONE_QT_GIT_VERSION "%{version}-%{release}"' > src/app/gitversion.h

lrelease-qt5 assets/languages/*.ts

sed \
  -e 's|inphone|\0qt|g' \
  -i assets/linphone.desktop

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DENABLE_DBUS:BOOL=ON \
  -DENABLE_UPDATE_CHECK:BOOL=OFF

cp ../assets/languages/*.qm assets/languages/

%make_build

%install
%make_install -C %{_target_platform}

rename linphone %{name} \
  %{buildroot}%{_bindir}/linphone* \
  %{buildroot}%{_datadir}/applications/linphone.desktop \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/linphone.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-tester
%{_datadir}/applications/%{name}.desktop
%{_datadir}/linphone/*-factory
%{_datadir}/linphone/assistant/*.rc
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg


%changelog
* Tue Jan 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.1.1-4
- Qt 5.11.3 rebuild

* Tue Sep 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.1.1-3
- Qt 5.11.1 rebuild

* Tue Apr 17 2018 Phantom X - 4.1.1-2
- Patch to fix crash with Qt 5.10

* Sat Sep 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 4.1.1-1
- Initial spec
