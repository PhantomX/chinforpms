%if 0%{?fedora} >= 40
%global build_type_safety_c 0
%endif

%global commit 28e1441f356afb9eb2538c82ebbd392c2a8686ff
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200215
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

# Build appindicator support
%bcond_with appindicator

%global vermm %%(echo %{version} | cut -d. -f-2)

%global vc_url https://github.com/DaveDavenport/%{name}

Name:           gmpc
Summary:        GNOME frontend for the MPD
Version:        11.8.90
Release:        102%{?dist}

License:        GPL-2.0-or-later
URL:            http://gmpclient.org/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://download.sarine.nl/Programs/gmpc/%{vermm}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-fix-desktop-file.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gob2 >= 2.0.0
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  make
%if %{with appindicator}
BuildRequires:  pkgconfig(appindicator3-0.1)
%endif
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libglyr)
BuildRequires:  pkgconfig(libmpd) >= 11.8.90
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xspf)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vala
%if %{with snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif

Requires:       hicolor-icon-theme
Requires:       xdg-utils

%description
Gmpc is a GNOME client for the Music Player Daemon
Features :
 * Support for loading/saving playlists.
 * File Browser
 * Browser based on ID3 information. (on artist and albums)
 * Search
 * Current playlist viewer with search.
 * ID3 information
 * Lots more

%package devel
Summary:  Development files for gmpc
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files necessary for developing gmpc plugins.

%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed -e 's/automake-1.16 /automake-1.17 \0/' -i ./autogen.sh

%{?with_snapshot:sed -e 's|`git rev-parse --short master`|%{shortcommit}|g' -i src/Makefile.am}
%{?with_snapshot:NOCONFIGURE=1 ./autogen.sh}


%build

%configure \
  --disable-shave \
%if !%{with appindicator}
  --enable-appindicator=no \
%endif
%{nil}

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Fix build error
%make_build || %make_build

%install
%make_install

mkdir -p %{buildroot}%{_metainfodir}
mv %{buildroot}%{_datadir}/appdata/* %{buildroot}%{_metainfodir}/
rm -rf %{buildroot}%{_datadir}/share/appdata

desktop-file-install \
  --remove-category GNOME \
  --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/icons/*/*/*/*
%{_mandir}/man1/*
%{_metainfodir}/%{name}.appdata.xml

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 11.8.90-102.20200215git28e1441
- Add new automake version to autogen.sh

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 11.8.90-101.20200215git28e1441
- build_type_safety_c 0

* Thu Apr 22 2021 Phantom X <megaphantomx at hotmail dot com> - 11.8.90-100.20200215git28e1441
- 11.8.90

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-24
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.8.16-17
- Remove obsolete scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Adrian Reber <adrian@lisas.de> - 11.8.16-13
- fixed "gmpc: load_list_itterate(): gmpc killed by SIGSEGV" (#1417462)

* Wed Sep 14 2016 Adrian Reber <adrian@lisas.de> - 11.8.16-12
- fixed "gmpc must not depend on webkitgtk" (#1375811)

* Tue Feb 09 2016 Adrian Reber <adrian@lisas.de> - 11.8.16-11
- fix for crash on exit (#1290929)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.16-9
- Fix F23FTBFS (RHBZ#1239534):
  - Append -DHAVE_STRNDUP=1 to CFLAGS to work-around bug in libmpd.
  - Append RPM_OPT_FLAGS to subdir CFLAGS.
- Add gmpc-awn-11.8.16-plugin.patch.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 01 2013 Adrian Reber <adrian@lisas.de> - 11.8.16-5
- added appdata file (#1034007)

* Thu Sep 26 2013 Rex Dieter <rdieter@fedoraproject.org> 11.8.16-4
- add explicit avahi build deps

* Wed Aug 07 2013 Adrian Reber <adrian@lisas.de> - 11.8.16-3
- fix #992396 (gmpc: FTBFS in rawhide)
- update URL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Adrian Reber <adrian@lisas.de> - 11.8.16-1
- updated to 11.8.16

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.20.0-5
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 11 2010 Adrian Reber <adrian@lisas.de> - 0.20.0-3
- rebuilt for new libmicrohttpd

* Sun Nov 07 2010 Adrian Reber <adrian@lisas.de> - 0.20.0-2
- rebuilt for new libnotify
- added patches for new libnotify

* Sat Jul 31 2010 Adrian Reber <adrian@lisas.de> - 0.20.0-1
- updated to 0.20.0

* Fri Jul 09 2010 Mike McGrath <mmcgrath@redhat.com> - 0.19.1-3.1
- Rebuilt to fix libwebkit-1.0.so.2 broken dep

* Fri May 07 2010 Adrian Reber <adrian@lisas.de> - 0.19.1-3
- added patch for " FTBFS gmpc-0.19.1-2.fc13: ImplicitDSOLinking" (#564660)

* Wed Nov 25 2009 Adrian Reber <adrian@lisas.de> - 0.19.1-2
- updated to 0.19.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 08 2009 Adrian Reber <adrian@lisas.de> - 0.18.0-1
- updated to 0.18.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Adrian Reber <adrian@lisas.de> - 0.16.1-1
- updated to 0.16.1

* Wed Oct 01 2008 Adrian Reber <adrian@lisas.de> - 0.15.5.0-4
- re-created patch to apply cleanly (fixes #465008)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.15.5.0-3
- Autorebuild for GCC 4.3

* Fri Feb 15 2008 Adrian Reber <adrian@lisas.de> - 0.15.5.0-2
- rebuilt for gcc43

* Sun Dec 23 2007 Adrian Reber <adrian@lisas.de> - 0.15.5.0-1
- updated to 0.15.5.0
- this should fix #242226
- added six more plugins (wikipedia, random-playlist,
  mserver, libnotify, favorites, extraplaylist)
- added BR libnotify-devel for libnotify plugin

* Sun Nov 11 2007 Adrian Reber <adrian@lisas.de> - 0.15.1-1
- update to 0.15.1
- dropped gmpc-fix-album-play-order.diff patch
- two more plugins (avahi, shout)

* Fri Aug 24 2007 Adrian Reber <adrian@lisas.de> - 0.14.0-3
- rebuilt

* Wed Jun 20 2007 Adrian Reber <adrian@lisas.de> - 0.14.0-2
- applied patch to fix album play order from David Woodhouse

* Sun Mar 25 2007 Adrian Reber <adrian@lisas.de> - 0.14.0-1
- updated to 0.14.0
- added more plugins
- fixed #233837 (gmpc-devel: unowned directory)

* Sat Dec 09 2006 Adrian Reber <adrian@lisas.de> - 0.13.0-1
- updated to 0.13.0
- created devel package for header files
- removed X-Fedora from desktop-file-install
- added some plugins and moved the plugins to %%{_libdir}/%%{name}/plugins

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.11.2-6
- BR: perl-XML-Parser

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.11.2-5
- rebuild

* Thu Mar 23 2006 Jonathan Dieter <jdieter99[AT]gmx.net> 0.11.2-4
- fix dynamic linking bug

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 0.11.2-3
- rebuild for FC5

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Nov 05 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.11.2-0.fdr.1
- initial Fedora release (from Mandrake)
