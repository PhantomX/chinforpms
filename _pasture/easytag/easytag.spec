%global commit eb64ebd962c17ca7ab176e6963fd069685a0d209
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220808
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global majorminor %%(echo %{version} | cut -d. -f1-2)

%global vc_url https://gitlab.gnome.org/GNOME/%{name}


Name:           easytag
Version:        2.5.1
Release:        0.6%{?dist}
Summary:        Tag editor for MP3, Ogg, FLAC and other music files

Epoch:          1

License:        GPL-2.0-or-later
URL:            https://wiki.gnome.org/Apps/EasyTAG

%if %{with snapshot}
Source0:        %{vc_url}/-/archive/%{commit}/%{name}-%{commit}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        https://download.gnome.org/sources/%{name}/%{majorminor}/%{name}-%{version}.tar.xz
%endif

# https://bugzilla.gnome.org/show_bug.cgi?id=776110
# https://gitlab.gnome.org/GNOME/easytag/-/issues/8
Patch0:         %{vc_url}/-/merge_requests/8.patch#/%{name}-gl-mr8.patch

# Debian
Patch10:        01_remove-pixdata.patch

BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  id3lib-devel >= 3.7.12
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  libxslt
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(id3tag)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(wavpack)
%if %{with snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(appstream-glib)
BuildRequires:  yelp-tools
%endif
Recommends:     yelp

# Obsoleted in F37
Obsoletes:     easytag-nautilus < 2.4.3-16 

%description
EasyTAG is a utility for viewing, editing and writing the tags of MP4, MP3,
MP2, FLAC, Ogg Opus, Ogg Speex, Ogg Vorbis, MusePack and Monkey's Audio files.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

%{?with_snapshot:NOCONFIGURE=1 ./autogen.sh}


%build
%configure \
  --disable-silent-rules \
  --disable-appdata-validate \
  --disable-schemas-compile \
  --disable-nautilus-actions \
%{nil}

%make_build


%install
%make_install

find %{buildroot} -type f -name "*.la" -delete

desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.EasyTAG.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.gnome.EasyTAG.appdata.xml

%find_lang %{name} --with-gnome


%check
make check


%files -f %{name}.lang
%doc ChangeLog HACKING README THANKS TODO
%license COPYING
%{_bindir}/easytag
%{_metainfodir}/org.gnome.EasyTAG.appdata.xml
%{_datadir}/applications/org.gnome.EasyTAG.desktop
%{_datadir}/icons/hicolor/*/apps/org.gnome.EasyTAG.*
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.EasyTAG-symbolic.svg
%{_datadir}/glib-2.0/schemas/org.gnome.EasyTAG.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.EasyTAG.gschema.xml
%{_mandir}/man1/easytag.1*


%changelog
* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.1-0.5.20220418git5f41323
- Disable nautilus package

* Mon Jun 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.1-0.4.20220418git5f41323
- Bump

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.1-0.3.20210912gited74295
- Update

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.1-0.2.20210326git206bfb4
- Bump

* Tue Dec 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.1-0.1.20200504gitc903a7a
- Snapshot
- Better fix to old bug 776110

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.4.3-104
- Disable appdata validation

* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.4.3-103.chinfo
- BR: gcc-c++

* Wed Jun 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.4.3-102.chinfo
- Some upstream fixes
- Make macros
- Move appdata to new place
- Remove uneeded scriptlets

* Mon Jan 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.4.3-101.chinfo
- Apply only the right patch

* Sun Jan 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.4.3-100.chinfo
- Try to fix https://bugzilla.gnome.org/show_bug.cgi?id=776110

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 05 2016 David King <amigadave@amigadave.com> - 2.4.3-1
- Update to 2.4.3

* Mon Feb 29 2016 David King <amigadave@amigadave.com> - 2.4.2-2
- Fix crash in the load filenames dialog (#1312163)

* Sun Feb 21 2016 David King <amigadave@amigadave.com> - 2.4.2-1
- Update to 2.4.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 David King <amigadave@amigadave.com> - 2.4.1-2
- Upstream fix for file renaming

* Mon Jan 25 2016 David King <amigadave@amigadave.com> - 2.4.1-1
- Update to 2.4.1

* Fri Oct 30 2015 David King <amigadave@amigadave.com> - 2.4.0-2
- Fix crash when writing playlists (#1275064)

* Sat Aug 29 2015 David King <amigadave@amigadave.com> - 2.4.0-1
- Update to 2.4.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 David King <amigadave@amigadave.com> - 2.3.7-3
- Fix crash when failing to read FLAC headers (#1231502)

* Sun May 31 2015 David King <amigadave@amigadave.com> - 2.3.7-2
- Fix crash when changing directory (#1226671)

* Sun May 17 2015 David King <amigadave@amigadave.com> - 2.3.7-1
- Update to 2.3.7

* Mon Apr 20 2015 David King <amigadave@amigadave.com> - 2.3.6-1
- Update to 2.3.6

* Tue Mar 10 2015 David King <amigadave@amigadave.com> - 2.3.5-1
- Update to 2.3.5
- Use license macro for COPYING and COPYING.GPL3

* Fri Feb 06 2015 David King <amigadave@amigadave.com> - 2.3.4-1
- Update to 2.3.4

* Wed Dec 31 2014 David King <amigadave@amigadave.com> - 2.3.3-1
- Update to 2.3.3

* Sun Nov 30 2014 David King <amigadave@amigadave.com> - 2.3.2-1
- Update to 2.3.2

* Sat Nov 01 2014 David King <amigadave@amigadave.com> 2.3.1-1
- Update to 2.3.1
- Add new -nautilus subpackage for Nautilus extension

* Sat Sep 27 2014 David King <amigadave@amigadave.com> 2.2.4-1
- Update to 2.2.4 (#1147133)
- Fix crash when reloading the directory tree (#1121142)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 22 2014 David King <amigadave@amigadave.com> 2.2.3-1
- Update to 2.2.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 David King <amigadave@amigadave.com> 2.2.2-2
- Add fix for crash when browsing hidden directories

* Fri May 09 2014 David King <amigadave@amigadave.com> 2.2.2-1
- Update to 2.2.2

* Tue Apr 22 2014 David King <amigadave@amigadave.com> 2.2.1-1
- Update to 2.2.1
- Add hardening flags

* Sat Apr 12 2014 David King <amigadave@amigadave.com> 2.2.0-1
- Update to 2.2.0
- Use pkgconfig with BuildRequires

* Sat Mar 08 2014 David King <amigadave@amigadave.com> 2.1.10-4
- Avoid crash when saving files with unknown image types
- Avoid crash when loading filenames from a text file

* Fri Mar 07 2014 David King <amigadave@amigadave.com> 2.1.10-3
- Avoid crash when declining deletion of a file

* Mon Mar 03 2014 David King <amigadave@amigadave.com> 2.1.10-2
- Avoid crash when clicking the window close button (#1071563)

* Wed Feb 19 2014 David King <amigadave@amigadave.com> 2.1.10-1
- Update to 2.1.10
- Install AppData
- Run make check

* Fri Feb 07 2014 David King <amigadave@amigadave.com> 2.1.9-2
- Avoid crash while saving Vorbis tags
- Avoid crash when receiving invalid commandline arguments
- Avoid double unref of GFile in open handler
- Fix memory leak in log date formatting
- Fix memory leak in date parsing

* Mon Jan 06 2014 David King <amigadave@amigadave.com> 2.1.9-1
- Update to 2.1.9 (#1051759)

* Mon Jan 06 2014 David King <amigadave@amigadave.com> 2.1.8-1
- Update to 2.1.8 (#951265)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 Matthias Saou <matthias@saou.eu> 2.1.7-1
- Update to 2.1.7 final.
- Replace the ugly low-res xpm icon with a nicer png one.

* Wed Feb  8 2012 Matthias Saou <matthias@saou.eu> 2.1.7-0.1
- Update to 2.1.7 git snapshot.
- Remove upstreamed patches.
- Cosmetic spec file updates.
- Require libmp4v2 >= 1.9.1 to still get mp4 tagging support, see #620531.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.1.6-8
- Rebuild for new libpng

* Sun Feb 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.1.6-7
- Improve default settings (#675421).
- Convert README to UTF-8.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 30 2010 Matthias Saou <http://freshrpms.net/> 2.1.6-5
- Actually apply the patch to remove x-directory/normal.
- Include patch to fix empty decription with flac pictures (#559828).
- Include patch to fix load from txt feature (#562317).

* Thu Apr  8 2010 Matthias Saou <http://freshrpms.net/> 2.1.6-3
- Remove x-directory/normal from the desktop file (#451823).

* Mon Oct 19 2009 Matthias Saou <http://freshrpms.net/> 2.1.6-2
- Add libid3tag-devel BR to fix id3 tag support (#525519).
- Add speex-devel BR to support speex files.

* Sat Sep 12 2009 Matthias Saou <http://freshrpms.net/> 2.1.6-1
- Update to 2.1.6 : Development, but the latest for over a year now.
- Include upstream cddb_manual_search_fix patch.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1-5
- Autorebuild for GCC 4.3

* Mon Oct 22 2007 Matthias Saou <http://freshrpms.net/> 2.1-4
- Fix Russian comment of the desktop file (charset problem, #327331).

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 2.1-3
- Rebuild to fix wrong execmem requirement on ppc32.

* Sat Aug  4 2007 Matthias Saou <http://freshrpms.net/> 2.1-2
- Update License field.

* Tue May  8 2007 Matthias Saou <http://freshrpms.net/> 2.1-1
- Update to 2.1.

* Wed May  2 2007 Matthias Saou <http://freshrpms.net/> 2.0.2-1
- Update to 2.0.2.

* Fri Apr 20 2007 Matthias Saou <http://freshrpms.net/> 2.0.1-1
- Update to 2.0.1.
- Update id3lib patch (Makefile.mingw changes).
- Include new wavpack support.

* Thu Mar  1 2007 Matthias Saou <http://freshrpms.net/> 2.0-1
- Update to 2.0.
- Remove now included APE tag patch.
- Chmod -x all files, then +x only where needed, since nearly all are +x :-(

* Mon Feb 19 2007 Matthias Saou <http://freshrpms.net/> 1.99.13-3
- Include patch to remove APE tags when tagging MP3 files (#200507).

* Thu Feb 15 2007 Matthias Saou <http://freshrpms.net/> 1.99.13-2
- Rebuild against flac 1.1.4.
- Enable libmp4v2 since it's now part of Fedora.

* Tue Dec 12 2006 Matthias Saou <http://freshrpms.net/> 1.99.13-1
- Update to 1.99.13.
- Update id3lib patch to still apply.
- Switch away from %%makeinstall to DESTDIR method.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 1.99.12-3
- FC6 rebuild.

* Tue Jul 11 2006 Matthias Saou <http://freshrpms.net/> 1.99.12-2
- Now use "patched" tarball with the libmpg123 directory removed.
- Include patch to disable libmpg123 and use id3lib instead for mpeg headers.

* Tue Apr 11 2006 Matthias Saou <http://freshrpms.net/> 1.99.12-1
- Update to 1.99.12.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 1.99.11-2
- Release bump to drop the disttag number in FC5 build.

* Fri Dec 16 2005 Matthias Saou <http://freshrpms.net/> 1.99.11-1
- Update to 1.99.11.

* Tue Dec 13 2005 Matthias Saou <http://freshrpms.net/> 1.99.10-1
- Update to 1.99.10.

* Thu Nov  3 2005 Matthias Saou <http://freshrpms.net/> 1.99.9-1
- Update to 1.99.9.

* Mon Oct 10 2005 Matthias Saou <http://freshrpms.net/> 1.99.8-1
- Update to 1.99.8.
- Try to add MP4/AAC support, but with current faad2 it fails to compile.

* Fri Oct 29 2004 Matthias Saou <http://freshrpms.net/> 1.99.1-1
- Fork off to "unstable" 1.99.1.

* Tue Jun  1 2004 Matthias Saou <http://freshrpms.net/> 0.31-1
- Update to stable 0.31.

* Fri Mar 26 2004 Matthias Saou <http://freshrpms.net/> 0.30.2-1
- Update to unstable 0.30.2.

* Wed Mar 24 2004 Matthias Saou <http://freshrpms.net/> 0.30.1-1
- Update to unstable 0.30.1.
- Remove desktop-file-install as it's now freedesktop style.

* Thu Feb 26 2004 Matthias Saou <http://freshrpms.net/> 0.30-4d
- Added patch for 0.30d.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.30-3c
- Rebuild for Fedora Core 1.

* Thu Oct 30 2003 Matthias Saou <http://freshrpms.net/> 0.30-2c
- Added patches to update to 0.30c.

* Tue Sep  9 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.30.

* Mon Sep  1 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.29.

* Tue Jul 15 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.28.1.

* Wed Jun  4 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.28.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Thu Mar 20 2003 Matthias Saou <http://freshrpms.net/>
- Added patch to 0.27a.

* Fri Feb  7 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.27.

* Fri Jan  3 2003 Ville Skyttä <ville.skytta@iki.fi> 0.26-fr1
- Update to 0.26.

* Wed Dec 25 2002 Ville Skyttä <ville.skytta@iki.fi> 0.25b-fr1
- Update to 0.25b.
- Build with flac support.

* Thu Oct 10 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 8.0.
- New menu entry.
- Rebuild with flac support... nope, doesn't compile :-(

* Fri Sep 20 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.24.

* Fri Aug 30 2002 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup for Red Hat Linux.
- A few %%files fixes and improvements.

* Tue Dec 18 2001 Jerome Couderc <j.couderc@ifrance.com>
- Updated for (Build)Requires entries

* Sat Sep 22 2001 Jerome Couderc <j.couderc@ifrance.com>
- Updated for /etc/X11/applnk/Multimedia/easytag.desktop

* Thu Sep 20 2001 Götz Waschk <waschk@linux-mandrake.com> 0.15.1-1
- Updated for autoconf

* Fri Jun 2 2000 Jerome Couderc <j.couderc@ifrance.com>
- Updated to include po files into the rpm package

* Fri May 5 2000 Jerome Couderc <j.couderc@ifrance.com>
- Initial spec file.

