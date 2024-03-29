%global vc_url https://github.com/smplayer-dev/%{name}

Name:           smtube
Version:        21.10.0
Release:        100%{?dist}
Summary:        YouTube browser for SMPlayer
Epoch:          1

License:        GPL-2.0-or-later
URL:            http://www.smtube.org
%dnl Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source0:        %{vc_url}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

# Do not spam .xsession-errors
Patch1:         0001-Do-not-spam-xsession-errors.patch

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  qt5-linguist
Requires:       (smplayer or mplayer or mpv or vlc or dragon or totem)
Requires:       (youtube-dlp or youtube-dl)
Requires:       hicolor-icon-theme

%{?_qt5_version:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}

%description
This is a YouTube browser for SMPlayer. You can browse, search
and play YouTube videos.

%prep
%autosetup -p1

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

%find_lang %{name} --with-qt


%files -f %{name}.lang
%license Copying.txt
%doc Readme.txt README.md Release_notes.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%dir %{_datadir}/%{name}/


%changelog
* Wed Oct 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.10.0-100
- 21.10.0
- R: youtube-dlp

* Sat Aug 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.7.0-100
- 21.7.0

* Thu Jun 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.6.0-100
- 20.6.0
- R: youtube-dl
- Cleanup BRs

* Sat Feb 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.1.0-100
- 20.1.0

* Mon Jun 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.6.0-100
- 19.6.0

* Mon Jun 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:18.11.0-101
- Upstream patch for yt

* Fri Nov 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.11.0-100.chinfo
- 18.11.0

* Sat Apr 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.9.0-100.chinfo
- 18.9.0

* Sat Apr 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.3.0-100.chinfo
- 18.3.0

* Sun Jan 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-100.chinfo
- Initial spec, borrowed from RPMFusion smplayer spec
