%global commit 172cf14915fd88356a9fd4e7428a596798a2e496
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230407
%bcond_without snapshot

%bcond_without kf5

# keep this in sync with phonon-backend-gstreamer
%global gstversion 1.0

%global vc_url https://invent.kde.org/multimedia/%{name}

Name:           kid3
Version:        3.9.3
Release:        100%{?dist}
Summary:        Efficient KDE ID3 tag editor
Epoch:          1

License:        GPL-2.0-or-later
URL:            https://kid3.sourceforge.net/

%if %{with snapshot}
Source0:        %{vc_url}/-/archive/%{commit}/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        https://download.kde.org/stable/%{name}/%{version}/%{name}-%{version}.tar.xz
%endif

BuildRequires:  kf5-kdelibs4support
BuildRequires:  cmake(KF5Config)
BuildRequires:  cmake(KF5ConfigWidgets)
BuildRequires:  cmake(KF5CoreAddons)
BuildRequires:  cmake(KF5DocTools)
BuildRequires:  cmake(KF5KIO)
BuildRequires:  cmake(KF5WidgetsAddons)
BuildRequires:  cmake(KF5XmlGui)
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  cmake
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5Qml)
BuildRequires:  cmake(Qt5Quick)
BuildRequires:  cmake(Qt5QuickControls2)
BuildRequires:  cmake(Qt5Svg)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Xml)
BuildRequires:  id3lib-devel
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(libchromaprint)
BuildRequires:  pkgconfig(gstreamer-%{gstversion})
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  gcc-c++
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}

%description
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio, WavPack, WMA, WAV, and AIFF files
(e.g. full albums) without typing the same information again and again
and have control over both ID3v1 and ID3v2 tags, then Kid3 is the
program you are looking for.

%package        common
Summary:        Efficient command line ID3 tag editor
Recommends:     xdg-utils

%description    common
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio, WavPack, WMA, WAV, and AIFF files
(e.g. full albums) without typing the same information again and again
and have control over both ID3v1 and ID3v2 tags, then Kid3 is the
program you are looking for.  The %{name}-common package provides Kid3
command line tool and files shared between all Kid3 variants.


%package        qt
Summary:        Efficient Qt ID3 tag editor
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}

%description    qt
If you want to easily tag multiple MP3, Ogg/Vorbis, FLAC, MPC,
MP4/AAC, MP2, Speex, TrueAudio, WavPack, WMA, WAV, and AIFF files
(e.g. full albums) without typing the same information again and again
and have control over both ID3v1 and ID3v2 tags, then Kid3 is the
program you are looking for.  The %{name}-qt package provides Kid3
built without KDE dependencies.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1


%build
# lib64 stuff: //bugzilla.redhat.com/show_bug.cgi?id=1425064
%cmake_kf5 \
%if "%{?_lib}" == "lib64"
    %{?_cmake_lib_suffix64} \
%endif
    -DWITH_GSTREAMER:BOOL=ON \
    -DWITH_GSTREAMER_VERSION=%{gstversion} \
    -DWITH_NO_MANCOMPRESS:BOOL=ON \
%{nil}

%cmake_build


%install

%cmake_install

install -dm 755 $RPM_BUILD_ROOT%{_pkgdocdir}
install -pm 644 AUTHORS ChangeLog README $RPM_BUILD_ROOT%{_pkgdocdir}

%find_lang %{name} --with-html --with-man
mv %{name}.lang %{name}-kde.lang
%find_lang %{name}-qt --with-man
%find_lang %{name}-cli --with-man
%find_lang %{name} --with-qt
cat %{name}.lang >> %{name}-cli.lang
cat <<EOF >> %{name}-cli.lang
%%dir %%{_datadir}/kid3/
%%dir %%{_datadir}/kid3/translations/
EOF


%check
appstream-util validate-relax --nonet \
    $RPM_BUILD_ROOT%{_datadir}/metainfo/*.appdata.xml

%files -f %{name}-kde.lang
%{_bindir}/kid3
%{_datadir}/metainfo/org.kde.kid3.appdata.xml
%{_datadir}/icons/hicolor/*x*/apps/kid3.png
%{_datadir}/icons/hicolor/scalable/apps/kid3.svgz
%{_datadir}/applications/org.kde.kid3.desktop
%{_datadir}/kxmlgui5/%{name}

%files common -f %{name}-cli.lang
%{_bindir}/kid3-cli
%{_libdir}/kid3/
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/kid3/qml/
%{_mandir}/man1/kid3.1*
%{_mandir}/man1/kid3-cli.1*
%license COPYING LICENSE
%{_pkgdocdir}/

%files qt -f %{name}-qt.lang
%{_bindir}/kid3-qt
%{_datadir}/metainfo/org.kde.kid3-qt.appdata.xml
%{_datadir}/applications/org.kde.kid3-qt.desktop
%{_datadir}/icons/hicolor/*x*/apps/kid3-qt.png
%{_datadir}/icons/hicolor/scalable/apps/kid3-qt.svg
%dir %{_docdir}/kid3-qt/
%lang(de) %{_docdir}/kid3-qt/kid3_de.html
%lang(en) %{_docdir}/kid3-qt/kid3_en.html
%lang(pt) %{_docdir}/kid3-qt/kid3_pt.html
%lang(ca) %{_docdir}/kid3-qt/kid3_ca.html
%lang(it) %{_docdir}/kid3-qt/kid3_it.html
%lang(nl) %{_docdir}/kid3-qt/kid3_nl.html
%lang(sv) %{_docdir}/kid3-qt/kid3_sv.html
%lang(uk) %{_docdir}/kid3-qt/kid3_uk.html
%lang(ru) %{_docdir}/kid3-qt/kid3_ru.html
%{_mandir}/man1/kid3-qt.1*


%changelog
* Sat Apr 08 2023 Phantom X <megaphantomx at hotmail dot com> - 3.9.3-100
- 3.9.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 3.9.2-2
- Rebuilt for flac 1.4.0

* Sat Aug 06 2022 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 3.9.2-1
- Update to latest upstream bugfix version: 3.9.2
