%global         majorminor 1.0

#global gitrel     140
#global gitcommit  4ca3a22b6b33ad8be4383063e76f79c4d346535d
#global shortcommit %%(c=%{gitcommit}; echo ${c:0:5})

%global sanitize 0

%global pkgname gst-plugins-ugly

Name:           gstreamer1-plugins-ugly-free
Version:        1.18.4
Release:        100%{?dist}
Summary:        GStreamer streaming media framework "ugly" plugins

License:        LGPLv2+ and LGPLv2
URL:            http://gstreamer.freedesktop.org/

%if 0%{sanitize}
%if 0%{?gitrel}
Source0:        https://gitlab.freedesktop.org/gstreamer/%{pkgname}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        http://gstreamer.freedesktop.org/src/%{pkgname}/%{pkgname}-%{version}.tar.xz
%endif
%else
# Use Makefile to download
%if 0%{?gitrel}
Source0:        %{pkgname}-free-%{shortcommit}.tar.xz
%else
Source0:        %{pkgname}-free-%{version}.tar.xz
%endif
%endif
Source1:        Makefile

BuildRequires:  meson >= 0.48.0
BuildRequires:  gcc

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  check
BuildRequires:  gettext-devel

BuildRequires:  liba52-devel
BuildRequires:  libcdio-devel
BuildRequires:  libdvdread-devel
BuildRequires:  libmpeg2-devel

# when mpeg2dec was moved here from -ugly
Conflicts:      gstreamer1-plugins-ugly < 1.16.0-2

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins whose license is not fully compatible with LGPL.

%package devel
Summary:        Development files for the GStreamer media framework "ugly" plug-ins
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer1-plugins-base-devel


%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins whose license
is not fully compatible with LGPL.


%prep
%setup -q -n gst-plugins-ugly-%{version}
%if 0%{?gitrel}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

%if 0%{sanitize}
  for plugin in \
    asfdemux dvdlpcmdec dvdsub realmedia
  do
    rm -rf ext/$plugin
    rm -rf gst/$plugin
  done
%endif

%build
# libsidplay was removed as obsolete, not forbidden
%meson \
    -D package-name='chinforpms GStreamer-plugins-ugly package' \
    -D package-origin='https://copr.fedorainfracloud.org/coprs/phantomx/chinforpms' \
    -D doc=disabled \
    -D amrnb=disabled -D amrwbdec=disabled -D sidplay=disabled \
    -D x264=disabled -D asfdemux=disabled -D dvdlpcmdec=disabled \
    -D dvdsub=disabled -D realmedia=disabled

%meson_build

%install
%meson_install

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_datadir}/appdata
cat > %{buildroot}%{_datadir}/appdata/gstreamer-ugly-free.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-ugly-free</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Extra</name>
  <summary>Multimedia playback for CD, DVD, and MP3</summary>
  <description>
    <p>
      This addon includes several additional codecs that have good quality and
      correct functionality, but whose license is not fully compatible with LGPL.
    </p>
    <p>
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <keywords>
    <keyword>CD</keyword>
    <keyword>DVD</keyword>
    <keyword>MP3</keyword>
  </keywords>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang gst-plugins-ugly-%{majorminor}
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%files -f gst-plugins-ugly-%{majorminor}.lang
%license COPYING
%doc AUTHORS README REQUIREMENTS

%{_datadir}/appdata/*.appdata.xml

# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstxingmux.so

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgsta52dec.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdio.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdread.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2dec.so

%if 0
%files devel
%doc %{_datadir}/gtk-doc/html/gst-plugins-ugly-plugins-%{majorminor}
%endif

%changelog
* Sun Apr 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.18.4-100
- Fedora 33 build

* Tue Mar 16 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.4-1
- Update to 1.18.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.2-1
- Update to 1.18.2

* Fri Oct 30 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.1-1
- Update to 1.18.1

* Sat Oct 17 2020 Dominik Mierzejewski <rpm@greysector.net> - 1.18.0-2
- rebuild for libdvdread-6.1 ABI bump

* Tue Sep 8 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.0-1
- Update to 1.18.0

* Fri Aug 21 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.90-1
- Update to 1.17.90

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 6 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.2-1
- Update to 1.17.2

* Mon Jun 22 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.1-1
- Update to 1.17.1

* Mon Mar 30 2020 Adrian Reber <adrian@lisas.de> - 1.16.2-3
- Rebuilt for new libcdio (2.1.0)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 2 2020 Wim Taymans <wtaymans@redhat.com> - 1.16.2-1
- Update to 1.16.2

* Fri Nov 15 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.16.1-2
- rebuild for libdvdread ABI bump

* Tue Sep 24 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.1-1
- Update to 1.16.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.16.0-3
- Conflicts: gstreamer1-plugins-ugly < 1.16.0-2

* Mon May 13 2019 Yaakov Selkowitz <yselkowi@redhat.com> - 1.16.0-2
- Enable mpeg2dec plugin (#1709470)

* Tue Apr 23 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.0-1
- Update to 1.16.0

* Fri Mar 01 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.2-1
- Update to 1.15.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.1-1
- Update to 1.15.1

* Wed Oct 03 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.4-1
- Update to 1.14.4

* Tue Sep 18 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.3-1
- Update to 1.14.3

* Mon Jul 23 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.2-1
- Update to 1.14.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-3
- rebuild (#1581325) to update Provides

* Tue May 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.1-2
- rebuild (file)

* Mon May 21 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-1
- Update to 1.14.1

* Tue Mar 20 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Wed Mar 14 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.91-1
- Update to 1.13.91

* Mon Mar 05 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.90-1
- Update to 1.13.90

* Tue Feb 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-2
- drop Obsoletes/Provides: -mpg123 (moved to -good)

* Thu Feb 22 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.1-1
- Update to 1.13.1
- mp3 plugins moved to -good

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Adrian Reber <adrian@lisas.de> - 1.12.4-3
- Rebuilt for new libcdio (2.0.0)

* Sun Jan 14 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.4-2
- Enable twolame plugin (#1534289)

* Mon Dec 11 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.4-1
- Update to 1.12.4
- Add autoconf and friends to BuildRequires

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.3-1
- Update to 1.12.3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.2-1
- Update to 1.12.2

* Tue Jun 20 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Thu May 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.0-3
- Enable LAME plugin (#1450108)

* Thu May 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.0-2
- Update to 1.12.0

* Thu May 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.10.4-2
- Initial Fedora spec file
