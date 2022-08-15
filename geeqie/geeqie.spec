%global commit 31197b3d4f2ee55c84a2ae5c71995e2c5dad91c8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211107
%global with_snapshot 0

%bcond_with map

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/BestImageViewer/%{name}

Summary:        Image browser and viewer
Name:           geeqie
Version:        2.0.1
Release:        100%{?gver}%{?dist}

URL:            https://www.geeqie.org
License:        GPLv2+

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
%dnl Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:        %{vc_url}/releases/download/v%{version}/%{name}-%{version}.tar.xz
%endif

Patch0:         sun_path.patch


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.53.0
BuildRequires:  gettext
BuildRequires:  yelp-tools

# for /usr/bin/appstream-util
BuildRequires:  libappstream-glib

BuildRequires:  pkgconfig(ddjvuapi)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(exiv2)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libraw)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  desktop-file-utils
# For xxd
BuildRequires:  vim-common
%if %{with map}
BuildRequires:  pkgconfig(clutter-gtk-1.0)
BuildRequires:  pkgconfig(champlain-0.12)
%endif

#BuildRequires:  pkgconfig(libheif)
#BuildRequires:  pkgconfig(libffmpegthumbnailer)

# for the included plug-in scripts
Requires:       exiv2
Requires:       fbida
Requires:       ImageMagick
Requires:       perl-Image-ExifTool
Requires:       zenity


%description
Geeqie has been forked from the GQview project with the goal of picking up
development and integrating patches. It is an image viewer for browsing
through graphics files. Its many features include single click file
viewing, support for external editors, previewing images using thumbnails,
and zoom.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

echo '#!/bin/sh' > version.sh
cat >> version.sh <<'EOF'
version=$(head -1 NEWS)
set -- $version
printf '%s' "$2%{?gver:+git%{date}-%{shortcommit}}"
EOF

sed -e 's|lua5.3|lua|g' -i meson.build


%build
cflags=(
  -Wno-error=unused-variable
  -Wno-error=maybe-uninitialized
  -Wno-error=unused-function
  -Wno-error=unused-but-set-variable
  -Wno-error=parentheses
  -Wno-deprecated-declarations
)
CFLAGS="$CFLAGS ${cflags[*]}"

%meson \
  -Dgps-map=%{?with_map:enabled}%{!?with_map:disabled} \
  -Dheif=disabled \
  -Dspell=disabled \
  -Dvideothumbnailer=disabled \
  -Dgq_helpdir=%{_pkgdocdir} \
%{nil}

%meson_build


%install
mkdir -p %{buildroot}%{_pkgdocdir}/html
%meson_install

# guard against missing HTML tree
[ ! -f %{buildroot}%{_pkgdocdir}/html/index.html ] && exit 1

# We want these _docdir files in GQ_HELPDIR.
install -p -m 0644 AUTHORS COPYING NEWS README* TODO \
    %{buildroot}%{_pkgdocdir}

desktop-file-install \
    --delete-original \
    --dir %{buildroot}%{_datadir}/applications \
    --add-mime-type="image/jxl" \
    --add-mime-type="image/svg+xml-compressed;image/svg-xml;text/xml-svg" \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

sed \
  -e 's|_name>|name>|g' \
  -e 's|_summary>|summary>|g' \
  -e 's|_p>|p>|g' \
  -e 's|<_p |<p |g' \
  -i %{buildroot}%{_metainfodir}/org.geeqie.Geeqie.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.geeqie.Geeqie.appdata.xml

%files -f %{name}.lang
%doc %{_pkgdocdir}/
%license COPYING
%{_bindir}/%{name}*
%{_prefix}/lib/%{name}/
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}/
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/*%{name}.desktop
%{_metainfodir}/org.geeqie.Geeqie.appdata.xml


%changelog
* Sat Aug 13 2022 Phantom X <megaphantomx at hotmail dot com> - 2.0.1-100
- 2.0.1
- meson

* Tue Apr 12 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.3-100
- 1.7.3
- Rawhide sync

* Sun Feb 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.2-100
- 1.7.2

* Mon Jan 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.1-100
- 1.7.1

* Thu Dec 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.6-102.20211107git31197b3
- Add some svg mimetypes to desktop file

* Tue Nov 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1.6-101.20211107git31197b3
- Last snapshot
- Rawhide sync

* Thu Dec  3 2020 Phantom X <megaphantomx at hotmail dot com> - 1.6-100
- 1.6
- gtk3

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4.git26c4dad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb  4 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.1-3.git26c4dad
- Update to latest git snapshot (fixes build in rawhide and other minor issues).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Matthew Miller <mattdm@fedoraproject.org> - 1.5.1-1
- new upstream release
- reenable tiff support
- don't error on the parenthesis warning (reported upstream)
- hey look: none of our patches are needed anymore!

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-9.git0004617
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.4-6
- rebuild (exiv2)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4-3
- Enable lua scripting support

* Mon Jan 01 2018 Matthew Miller <mattdm@fedoraproject.org> - 1.4-2
- hack around missing changelog (which we don't want to include
  anyway -- see below)

* Mon Jan 01 2018 Matthew Miller <mattdm@fedoraproject.org> - 1.4-1
- new upstream release
- drop exiv2 patch libstc++-copy-on-write-string -- now upstream
- add patch to relax warnings on unused-but-set variables -- see
  upstream https://github.com/BestImageViewer/geeqie/issues/566 and
  https://github.com/BestImageViewer/geeqie/issues/567
- drop ChangeLog since it's missing from the release tarball, and also we
  nominally dropped it from the package in 2008 for being "too low level"
  (see earlier rpm changelog entry)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 1.3-3
- rebuild (exiv2)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 15 2016 Matthew Miller <mattdm@fedoraproject.org> - 1.3-1
- update to new upstream 1.3 release
- remove patches integrated upstream:
    geeqie-1.1-filedata-change-notification.patch
    geeqie-1.1-large-files.patch
    geeqie-gcc6-error-about-shifting-a-signed-expression.patch
- also remove geeqie-1.0-fix-fullscreen.patch, as it hasn't been applied for
  years anyway and fullscreen seems to work
- update geeqie-bug-800350-libstc++-copy-on-write-string.diff to new version
  from Debian. Thanks, Debian!

* Sat Feb 27 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 1.2.2-3
- Add patch for #1292255

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 25 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.2-1
- Update to latest upstream release

* Wed Aug 26 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2-0.6.20150812git2b87884
- Update To Tag V1.2.1 for a few merged commit requests,
  shall also fix:
  (rhbz #1223349 patch by Sami Farin - crash for Preload next image)
  (rhbz #1231644 orientation hack makes loading image 100x slower)

- update URL to new geeqie.org

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.2-0.5.20141130gita1afabd
- rebuild (exiv2)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.20141130gita1afabd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.2-0.3.20141130gita1afabd
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 25 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2-0.2.20141130gita1afabd
- Merge Fedora appdata file as requested on devel@ list.
- Use %%license macro.

* Sun Nov 30 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2-0.1.20141130gita1afabd
- TODO: Lua support wants lua5.1.pc >= 5.1, which isn't available
  (only lua.pc 5.2.x exists).
- TODO: what's up with the aging fullscreen patch?
- Add new BUGS file to documentation.
- Drop the LCMS1 bcond.
- Some patches not needed anymore.
- Drop old conditional for desktop file vendor. 
- Update to 1.2 from gitorious including the merged LCMS2 patch (post-1.2).
  No official tarball release yet.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-21
- Retrieve a printable CMS image profile and screen profile description
  to avoid crashing g_markup (#1110073).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-19
- Don't print CMS screen profileID garbage that crashes g_markup
  (this should also fix #1051660).

* Tue May 27 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-18
- Merge fix for avoiding crash due to inexistent files in collections.
  This also replaces the history path_list patch.

* Sun Jan 26 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-17
- Merge image-overlay.c fix for handling of filenames with % in them.

* Mon Dec  9 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-16
- Add LCMS2 patch from Geeqie-devel list, fix HAVE_LCMS and build with
  lcms2-devel instead of lcms-devel.

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.1-15
- rebuild (exiv2)

* Sat Nov 16 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-14
- Conditionalize ufraw BR/R for Fedora, since it's not available with
  RHEL and EPEL and is optional at run-time.
- Drop %%defattr usage.

* Tue Aug  6 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-13
- For F-20 unversioned docdirs feature we need to build with
  configure --with-readmedir=... to override the internal GQ_HELPDIR.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun  7 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-11
- Define _hardened_build 1 to please rpm-chksec.

* Wed Feb 20 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-10
- Include config.h earlier in some files, so the large file support
  definition is available early enough for e.g. sys/stat.h
- Drop the aging Obsoletes tag for gqview.

* Fri Feb  8 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-9
- Avoid abort when opening non-existing paths from history.

* Fri Feb  1 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-8
- Drop new idle callback from file_data_send_notification() as it
  causes breakage (in the duplicate finder, for example).

* Sun Jan 27 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-7
- Check exec value for NULL in src/editors.c
- Fedora >= 19: Drop ancient "fedora" vendor prefix from desktop file.

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.1-6
- rebuild due to "jpeg8-ABI" feature drop

* Mon Dec 24 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-5
- Fix crash upon escaping from generic dialogs.

* Thu Dec 13 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-4
- Build with --disable-tiff, as the custom libtiff loader crashes
  for some images as mentioned on geeqie-devel list.

* Thu Nov 22 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-3
- Merge a patch to fix fullscreen mode.

* Sun Aug 26 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-2
- Merge bar_keywords.c master commit to fix regression.

* Tue Aug 14 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.1-1
- Fix license tag to GPLv2+ as GPL3 (only in file COPYING) had been
  added only temporarily for 1.0-alpha1.
- BR libjpeg-devel libtiff-devel
- Upgrade to 1.1 (also to reduce patch count).

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May  3 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-17
- Complete previous rebuild that failed unexpectedly because html docdir in
  buildroot had not been created (Rawhide only). Now create it explicitly
  at beginning of %%install.

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.0-16
- rebuild (exiv2)

* Fri Jan  6 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-15
- rebuild for GCC 4.7 as requested

* Sat Nov  5 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-14
- Link with --as-needed.

* Sun Oct 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-13
- Cherry-pick a few commits (from Vladimir Nadvornik, Klaus Ethgen
  and Vladislav Naumov). With the modified filelist_sort_compare_filedata
  method, Geeqie passes another stress test I've created in order
  to track down rare file_data_unref crashes.

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.0-12
- rebuild (exiv2)

* Tue Aug  9 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-11
- Patch another place where not to exif_free_fd NULL ptr (#728802).

* Fri Apr 15 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-10
- Let's see how we do with a simpler vflist_setup_iter_recursive().

* Sat Mar  5 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-9
- Patch filedata.c check_case_insensitive_ext to accept the first
  tested file name ext and not accept multiple combinations due to
  case-insensitive fs.

* Fri Mar  4 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-8.test1
- Patch filedata.c check_sidecars to avoid adding a file as its own
  sidecar. Case-insensitive sidecar file name generation may not be
  enough if a fs stat is used in conjunction with a case-insensitive fs.

* Tue Feb 22 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-8
- Fix file cache NULL pointer crash in exif-common.c (#679256).
- Patch and build with large file support.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.0-6
- rebuild (exiv2)

* Thu Sep  9 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-5
- Make gqview "Obsoletes" tag conditional: for Fedora newer than 13.

* Mon Jul 26 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-4
- Replace old gqview < 2.0.4-13 with geeqie.

* Mon May 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0-3 
- rebuild (exiv2)

* Tue Apr  6 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-2
- require exiv2, ImageMagick, fbida, ufraw, zenity for plug-in scripts
- BR gnome-doc-utils for HTML documentation (and "Help > Contents" menu)

* Fri Feb 19 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-1
- update to 1.0 final release
 
* Mon Jan 04 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.20.beta2
- rebuild (exiv2)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.19.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.18.beta2
- update to beta2 tarball
- BR intltool
- print-pagesize.patch enabled in 1.0beta2 (#222639)

* Thu May 14 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.16.beta1
- update to beta1 tarball

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.15.alpha3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.14.alpha3
- fetch src/utilops.c change from svn 1385 for metadata crash-fix

* Wed Jan 28 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.13.alpha3
- ignore .helpdir/.htmldir values in geeqierc to fix "Help"
- add --enable-lirc again to build with LIRC

* Mon Jan 26 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.12.alpha3
- update to alpha3 tarball

* Thu Jan 22 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.11.alpha2.1341svn
- update to svn 1341 for pre-alpha3 testing (image metadata features)
- drop obsolete patches remote-blank and float-layout

* Wed Dec 24 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.11.alpha2.1307svn
- update to svn 1307 for "Safe delete"

* Thu Dec 18 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.11.alpha2.1299svn
- drop desktop file Exec= invocation patch (no longer necessary)

* Thu Dec 18 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.10.alpha2.1299svn
- update to svn 1299 for new exiv2
- disable LIRC support which is broken

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.9.alpha2
- respin (exiv2)

* Tue Aug 12 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.8.alpha2
- fix float layout for --blank mode

* Mon Aug 11 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.7.alpha2
- fix options --blank and -r file:

* Thu Jul 31 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.6.alpha2
- update to 1.0alpha2 (now GPLv3)
- build with new LIRC support

* Wed Jun 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.5.alpha1 
- respin for exiv2

* Thu May  8 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.4.alpha1
- scriptlets: run update-desktop-database without path
- drop dependency on desktop-file-utils
- drop ChangeLog file as it's too low-level

* Fri Apr 25 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0-0.3.alpha1
- package GQview fork "geeqie 1.0alpha1" based on Fedora gqview.spec
- BR lcms-devel exiv2-devel
- update -desktop and -editors patch
- update spec file with more dir macros

