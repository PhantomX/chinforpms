Name:           smtube
Version:        18.1.0
Release:        100.chinfo%{?dist}
Summary:        YouTube browser for SMPlayer

License:        GPLv2+
URL:            http://www.smtube.org
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

Patch0:         %{name}-16.3.0-system-qtsingleapplication.patch
# Do not spam .xsession-errors
Patch1:         %{name}-18.1.0-quiet.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  qt5-linguist
# for unbundle sources
BuildRequires:  qtsingleapplication-qt5-devel
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme
Recommends:     smplayer

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
This is a YouTube browser for SMPlayer. You can browse, search
and play YouTube videos.

%prep
%autosetup -p1

rm -rf src/qtsingleapplication/

sed -i 's/\r//' *.txt

%build
pushd src
%{qmake_qt5}
%make_build TRANSLATION_PATH=\\\"%{_datadir}/%{name}/translations\\\"
%{_bindir}/lrelease-qt5 %{name}.pro
popd

%install
%make_install PREFIX=%{_prefix} DOC_PATH=%{_docdir}/%{name}

rm -rf %{buildroot}%{_docdir}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license Copying.txt
%doc Changelog Readme.txt Release_notes.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}


%changelog
* Sun Jan 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-100.chinfo
- Initial spec, borrowed from RPMFusion smplayer spec
