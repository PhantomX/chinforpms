Name:           liferea
Epoch:          2
Version:        1.16.14
Release:        100%{?dist}
Summary:        An RSS/RDF feed reader

License:        GPL-2.0-or-later
URL:            https://lzone.de/liferea/
Source0:        https://github.com/lwindolf/liferea/releases/download/v%{version}/liferea-%{version}.tar.bz2
Source1:        https://github.com/lwindolf/liferea/raw/068c12bbba396ed357078f9c3d69f495467f3827/js/user.js

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(girepository-2.0)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libpeas-2)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(sqlite)
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(webkit2gtk-web-extension-4.1)
BuildRequires:  xorg-x11-server-Xvfb

Requires:       libpeas-loader-python%{?_isa} >= 2
# gobject introspection dependencies
Recommends:     gstreamer1-plugins-base%{?_isa}
Recommends:     libappindicator-gtk3%{?_isa}
Recommends:     libnotify%{?_isa}
Recommends:     libsecret%{?_isa}

%description
Liferea (Linux Feed Reader) is an RSS/RDF feed reader.
It's intended to be a clone of the Windows-only FeedReader.
It can be used to maintain a list of subscribed feeds,
browse through their items, and show their contents.

%prep
%autosetup -p1 -n %{name}-%{version}

cp -p %{S:1} js/


%build
%configure \
  --disable-static \
  --disable-schemas-compile \
%{nil}

xvfb-run -- %make_build

%install
%make_install

%find_lang %{name}

# Upstream sets Version to 1.1 although the 1.1 spec says to use 1.0
desktop-file-edit --set-key=Version --set-value=1.0 %{buildroot}/%{_datadir}/applications/net.sourceforge.liferea.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/net.sourceforge.liferea.desktop

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/net.sourceforge.liferea.appdata.xml


%files -f %{name}.lang
%doc AUTHORS ChangeLog
%license COPYING
%{_mandir}/man1/%{name}.1*
%lang(it) %{_mandir}/it/man1/%{name}.1*
%{_bindir}/%{name}
%{_bindir}/%{name}-add-feed
%{_libdir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/metainfo/net.sourceforge.liferea.appdata.xml
%{_datadir}/applications/net.sourceforge.liferea.desktop
%{_datadir}/dbus-1/services/net.sourceforge.liferea.service
%{_datadir}/glib-2.0/schemas/net.sf.liferea.gschema.xml
%{_datadir}/GConf/gsettings/liferea.convert
%{_datadir}/icons/hicolor/16x16/apps/net.sourceforge.liferea.png
%{_datadir}/icons/hicolor/22x22/apps/net.sourceforge.liferea.png
%{_datadir}/icons/hicolor/24x24/apps/net.sourceforge.liferea.png
%{_datadir}/icons/hicolor/32x32/apps/net.sourceforge.liferea.png
%{_datadir}/icons/hicolor/48x48/apps/net.sourceforge.liferea.png
%{_datadir}/icons/hicolor/scalable/apps/net.sourceforge.liferea*.svg


%changelog
* Sat Sep 19 2026 Phantom X <megaphantomx at hotmail dot com> - 2:1.16.14-100
- 1.16.14

* Sat May  2 2026 Yanko Kaneti <yaneti@declera.com> - 1:1.16.9-1
- Update to 1.16.9

* Sun Apr 26 2026 Yanko Kaneti <yaneti@declera.com> - 1:1.16.8-1
- Update to 1.16.8

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.16.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Dec 28 2025 Yanko Kaneti <yaneti@declera.com> - 1:1.16.7-1
- Update to 1.16.7

* Fri Oct 31 2025 Yanko Kaneti <yaneti@declera.com> - 1:1.16.6-1
- Update to 1.16.6

* Thu Oct 30 2025 Yanko Kaneti <yaneti@declera.com> - 1:1.16.5-3
- Fix incomplete libpeas requirements update (#207399)
- Drop rhel conditionals for now

* Wed Oct  1 2025 Yanko Kaneti <yaneti@declera.com> - 1:1.16.5-2
- Update to wip 1.16.x to uncork f43 and rawhide
- Switch to libpeas2 and girepository-2.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 30 2024 josef radinger <cheese@nosuchhost.net> - 1:1.15.8-1
- bump version

* Mon Jul 22 2024 josef radinger <cheese@nosuchhost.net> - 1:1.15.7-1
- bump version

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 22 2024 josef radinger <cheese@nosuchhost.net> - 1:1.15.6-1
- bump version
- remove patch 0001

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Yanko Kaneti <yaneti@declera.com> - 1:1.15.4-4
- Pick an upstream fix for FTBFS with recent rawhide changes

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.15.4-2
- Clarify dependencies

* Tue Oct 24 2023 josef radinger <cheese@nosuchhost.net> - 1:1.15.4-1
- bump version
  should fix "libsoup2 and libsoup3 in the same process"-problem

* Fri Sep 22 2023 josef radinger <cheese@nosuchhost.net> - 1:1.15.3-1
- bump version

* Sun Sep 10 2023 josef radinger <cheese@nosuchhost.net> - 1:1.15.2-1
- bump version

* Sun Aug 20 2023 josef radinger <cheese@nosuchhost.net> - 1:1.15.1-2
- no current version for rhel
- webkit2gtk4.1

* Sun Aug 20 2023 josef radinger <cheese@nosuchhost.net> - 1:1.15.1-1
- bump version
- webkitgtk4 renamed to webkitgtk


* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 04 2023 josef radinger <cheese@nosuchhost.net> - 1:1.15.0-1
- bump version

* Sun Apr 16 2023 josef radinger <cheese@nosuchhost.net> - 1:1.14.5-1
- bump version

* Tue Apr 11 2023 Florian Weimer <fweimer@redhat.com> - 1:1.14.4-2
- Do not build with -std=c99

* Tue Apr 04 2023 josef radinger <cheese@nosuchhost.net> - 1:1.14.4-1
- bump version

* Sat Mar 25 2023 josef radinger <cheese@nosuchhost.net> - 1:1.14.3-1
- bump version

* Fri Mar 24 2023 josef radinger <cheese@nosuchhost.net> - 1:1.14.2-1
- bump version

* Mon Mar 13 2023 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.14.1-1
- Update to 1.14.1 (thanks to mikelo2) (#2177773)

* Thu Jan 26 2023 josef radinger <cheese@nosuchhost.net> - 1:1.14.0-1
- bump version

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 27 2022 josef radinger <cheese@nosuchhost.net> - 1:1.13.9-1
- bump version

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 09 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1:1.13.8-2
- Add Italian man file

* Fri Apr 08 2022 josef radinger <cheese@nosuchhost.net> - 1:1.13.8-1
- bump version

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 josef radinger <cheese@nosuchhost.net> - 1:1.13.7-1
- bump version

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 09 2021 josef radinger <cheese@nosuchhost.net> - 1:1.13.6-2
- add Requires on libpeas-gtk (#1732634)

* Sun May 09 2021 josef radinger <cheese@nosuchhost.net> - 1:1.13.6-1
- bump version
- remove patch0, incorporated upstream

* Mon Apr 12 2021 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.13.5-3
- Apply upstream patch to handle webkit2gtk 2.32.0 (#1946134)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 josef radinger <cheese@nosuchhost.net> - 1:1.13.5-1
- bump version

* Sat Dec 26 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.4-2
- fix specfile

* Sat Dec 26 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.4-1
- bump version
- icons have now full name

* Thu Oct 15 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.3-4
- fix build for epel7 (thanks tis)

* Sun Oct 11 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.3-3
- fix build for epel7

* Sat Oct 10 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.3-2
- drop outdated polish man-page
- metainfo instead of appdata
- add check-section

* Sat Oct 10 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.3-1
- bump version

* Tue Sep 01 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.2-1
- New development release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 12 2020 josef radinger <cheese@nosuchhost.net> - 1:1.13.1-1
- New development release

* Thu Mar  5 2020 Yanko Kaneti <yaneti@declera.com> - 1:1.13.0-1
- New development release

* Fri Jan 31 2020 Yanko Kaneti <yaneti@declera.com> - 1:1.12.7-5
- Run build under X11 to help introspection generation

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 20 2019 Yanko Kaneti <yaneti@declera.com> - 1:1.12.7-3
- Bump again for libpeas soname revert

* Tue Aug 20 2019 Yanko Kaneti <yaneti@declera.com> - 1:1.12.7-2
- Rebuild for libpeas soname bump

* Mon Aug  5 2019 Yanko Kaneti <yaneti@declera.com> - 1:1.12.7-1
- Update to 1.12.7

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec  4 2018 Yanko Kaneti <yaneti@declera.com> - 1:1.12.6-1
- Update to 1.12.6

* Fri Oct 19 2018 Yanko Kaneti <yaneti@declera.com> - 1:1.12.5-2
- Backport an upstream patch to enable plugin-installer

* Mon Sep 10 2018 Yanko Kaneti <yaneti@declera.com> - 1:1.12.5-1
- Update to 1.12.5

* Tue Jul 24 2018 Yanko Kaneti <yaneti@declera.com> - 1:1.12.4-1
- Update to 1.12.4. Drop patch

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun  9 2018 Yanko Kaneti <yaneti@declera.com> - 1:1.12.3-3
- Pull upstream fix for infinite loop -  bug 1589380

* Wed May 09 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.12.3-2
- Add a Requires on libpeas-loader-python3 to allow enabling
  the 'plugin installer' plugin

* Wed May  2 2018 Yanko Kaneti <yaneti@declera.com> - 1:1.12.3-1
- Update to 1.12.3

* Wed Mar  7 2018 Yanko Kaneti <yaneti@declera.com> - 1:1.12.2-1
- Update to 1.12.2

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.12.1-5
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Tomas Popela <tpopela@redhat.com> - 1:1.12.1-3
- Adapt to the webkitgtk4 rename

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.12.1-2
- Remove obsolete scriptlets

* Wed Dec 27 2017 Yanko Kaneti <yaneti@declera.com> - 1:1.12.1-1
- Update to 1.12.1. Drop upstream patch.

* Mon Dec  4 2017 Yanko Kaneti <yaneti@declera.com> - 1:1.12.0-2
- Pull a fix for Copy Link Location
- Use autosetup

* Fri Dec  1 2017 Yanko Kaneti <yaneti@declera.com> - 1:1.12.0-1
- Update to 1.12.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12-0.3.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12-0.2.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Yanko Kaneti <yaneti@declera.com> - 1:1.12-0.1.rc3
- Update to 1.12-rc3

* Mon Mar 20 2017 Yanko Kaneti <yaneti@declera.com> - 1:1.12-0.1.rc2
- Upgrade to 1.12-rc2. Move to webkitgtk4

* Sun Mar 19 2017 josef radinger <cheese@nosuchhost.net> - 1:1.10.19-3
- rebuild for broken dependencies

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Apr 05 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1.10.19-1
- Update to 1.10.19
- Drop backported patch

* Sat Mar 26 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1.10.18-5
- Do not rename the symbolic icon when we install it

* Mon Mar 21 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1.10.18-4
- Use the real symbolic icon

* Mon Mar 21 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 1.10.18-3
- Add symbolic icon, backported from the 1.11.xx series (#1243881)
- Use %%license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Emmanuel Seyman <emmanuel@seyman.fr> -  1:1.10.18-1
- Update to 1.10.18

* Sat Oct 31 2015 Yanko Kaneti <yaneti@declera.com> - 1:1.10.17-1
- Update to 1.10.17. Fixes various dialog UI issues with recent gtk+

* Mon Oct 26 2015 Yanko Kaneti <yaneti@declera.com> - 1:1.10.16-2
- Pick up upstream fix for pref dialog crash (#1275106)

* Sat Jun 20 2015 Yanko Kaneti <yaneti@declera.com> - 1:1.10.16-1
- Update to 1.10.16

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.10.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.10.15-1
- Update to 1.10.15
- Fix macro mentionned in changelog

* Fri Feb 27 2015 Yanko Kaneti <yaneti@declera.com> - 1:1.10.14-1
- Update to 1.10.14

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:1.10.13-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Jan 23 2015 Yanko Kaneti <yaneti@declera.com> - 1:1.10.13-1
- Update to 1.10.13
- Munge Version in the desktop file so that it passes validation

* Wed Oct 15 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.10.12-1
- Update to 1.10.12
- Disable desktop file validation

* Mon Aug 25 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.10.11-1
- Update to 1.10.11

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.10.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1:1.10.9-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.10.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Yanko Kaneti <yaneti@declera.com> - 1:1.10.9-1
- Update to 1.10.9

* Wed Mar 26 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.10.8-1
- Update to 1.10.8

* Mon Feb 24 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.10.6-1
- Update to 1.10.6 (fixes #1048499)

* Thu Jan 16 2014 Yanko Kaneti <yaneti@declera.com> - 1:1.10.5-1
- Upstream bugfix release - 1.10.5
- Source on github
- Upstream fixed installing the gsettings convert file

* Mon Jan 13 2014 Yanko Kaneti <yaneti@declera.com> - 1:1.10.4-1
- Upstream bugfix release - 1.10.4

* Tue Oct 08 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.10.3-1
- Update to 1.10.3
- Fix incorrect date in changelog

* Fri Sep 06 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.10.2-1
- Update to 1.10.2

* Sun Jul 28 2013 Yanko Kaneti <yaneti@declera.com> - 1:1.10.1-1
- New upstream bugfix release - 1.10.1
- Drop upstreamed patch

* Thu Jul 11 2013 Yanko Kaneti <yaneti@declera.com> - 1:1.10.0-1
- New major stable release - 1.10.0
- Spec rework for move to gsettings

* Tue Jun 25 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.8.15-1
- Update to 1.8.15

* Wed Jun 05 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.8.14-1
- New release - 1.8.14 
  http://sourceforge.net/p/liferea/code/ci/liferea-1_8/tree/ChangeLog

* Tue Feb 12 2013 Jon Ciesla <limburgher@gmail.com> - 1:1.8.12-2
- Drop desktop vendor tag.

* Thu Jan 10 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.8.12-1
- New bugfix upstream release - 1.8.12

* Sat Dec 29 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.8.11-1
- New bugfix upstream release - 1.8.11

* Sun Nov 04 2012 Emmanuel Seyman <emmanuel@seyman.fr> - 1:1.8.10-2
- Minor spec clean-ups

* Wed Oct 31 2012 Yanko Kaneti <yaneti@declera.com> - 1:1.8.10-1
- New upstream bugfix release - 1.8.10 - 861231, 861253

* Fri Oct  5 2012 Yanko Kaneti <yaneti@declera.com> - 1:1.8.9-1
- New upstream bugfix release - 1.8.9
- Drop upstreamed patch

* Sat Sep 29 2012 Yanko Kaneti <yaneti@declera.com> - 1:1.8.8-2
- Actually apply the Patch1 crash fix

* Fri Sep 14 2012 Yanko Kaneti <yaneti@declera.com> - 1:1.8.8-1
- New bugfix release from upstream - 1.8.8
- Add crash fix - bug 857348

* Tue Jul 31 2012 Yanko Kaneti <yaneti@declera.com> - 1:1.8.7-1
- New bugfix release from upstream - 1.8.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Yanko Kaneti <yaneti@declera.com> - 1:1.8.6-1
- New upstream bugfix release. 1.8.6

* Thu Apr 26 2012 Jon Ciesla <limburgher@gmail.com> - 1:1.8.5-1
- New upstream release, BZ 807602.

* Wed Jan 25 2012 Steven M. Parrish <smparrish@gmail.com> - 1:1.8.0-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1:1.6.5-5
- Rebuild for new libpng

* Sun Mar 27 2011 Christopher Aillon <caillon@redhat.com> - 1.6.5-4
- Rebuild against NM 0.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 16 2010 Tomas Bzatek <tbzatek@redhat.com> - 1.6.5-2
- Rebuilt against new libnotify

* Wed Oct 13 2010 Steven M. Parrish <smparrish@gmail.com> - 1.6.5-1
- New upstream release

* Mon Jul 5 2010 Steven M. Parrish <smparrish@gmail.com> - 1.6.4-1
- Fixes  Enclosures URLs with spaces do not work.
- Added  identi.ca bookmarking support.
- Fixes  Atom author URIs not markup escaped.
- Fixes  comma in link prevents launching browser
- Fixes  Broken Google Reader authentication.

* Sat Mar 27 2010 Steven M. Parrish <smparrish@gmail.com> - 1.6.3-1
- New upstream release
- Fix for 564609

* Mon Jan 25 2010 Steven M. Parrish <smparrish@gmail.com> - 1.6.2-2
- Fix Epoch issue

* Sun Jan 24 2010 Steven M. Parrish <smparrish@gmail.com> - 1.6.2-1
- New upstream release

* Sat Oct 10 2009 Steven M. Parrish <smparrish@gmail.com> - 1.6.0-1
- Add additional functionality #527873

* Wed Aug 12 2009 Steven M. Parrish <smparrish@gmail.com> - 1.6.0-0
- Final 1.6.0 release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-0.5.rc7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Steven M. Parrish <smparrish@gmail.com> 1.6.0-0.4.rc7
- Open the "Decrease/Increase Text Size" menu instead of the
- normal link menu on JavaScript links.
- Fixes SF #2787817, SF #2814022, Debian #525368:
- Work around several eggtrayicon crashes.
- Fix target="_blank" links not opening in tabs.
- Fixes a crash on some newsbin items without parents.
- Open new windows opened by Javascript in a new tab.
- Fixes crash when removing Google Reader node when update
- of one of it's subscriptions is in progress.
- Fixes SF #2789255: Crash when quitting during download.
- Reduce memory usage by only using a WebKitWebSettings for all
- the htmlviews.
- Fixes SF #2823359: Subscription -> New Source crashes
- Require WebKitGtk+ >= 1.1.10 to avoid problems with older
- versions.
- Fixes SF #2815397: Don't scale images when scaling the text.
- Fixes Debian #537295: Work around a format misdetection in
- item_set_description().
- Fixes Debian #537332: Infinite loop on 404 errors.
- Update of Arabic translation. 
- Update of Brazilian Portuguese translation.


* Tue Jun 30 2009 Steven M. Parrish <smparrish@gmail.com> 1.6.0-0.1.rc6
- Updated the example feeds. 
- Updated the social bookmarking sites. 
- Added Twitter Search support. 
- Added Identi.ca Search support. 
- Support non-RFC822 alphabetic timezones. 
- Fix favicon downloads when the feed contains a link with
- leading or trailing whitespace.
- Fixes comment feed hiding when comment feed is disabled.
- Don't use the deprecated soup_message_headers_get() function.
- More consistent tab label widths.
- Avoid having loading of other tabs cancelled when opening
- a new tab. 

* Wed Jun 24 2009 Rex Dieter <rdieter@fedoraproject.org> 1.6.0-0.3.fc5
- Obsoletes: liferea-WebKit < 1.6.0

* Tue Jun 16 2009 Steven M. Parrish <smparrish@gmail.com> 1.6.0-0.2.rc5
- fix missing BR

* Tue Jun 16 2009 Steven M. Parrish <smparrish@gmail.com> 1.6.0-0.1.rc5
- New upstream release
- Added obsolete for the old liferea-Webkit

* Tue May 26 2009 Steven M. Parrish <tuxbrewr@fedoraproject.org> 1.6.0-0.1.rc4
- New upstream release
- Drops support for xulrunner.  Now WebKit only

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> - 1.4.26-2
- Rebuild against newer gecko

* Sun Mar 08 2009 Steven M. Parrish <tuxbrewr@fedoraproject.org> 1.4.26-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Steven M. Parrish <tuxbrewr@fedoraproject.org> 1.4.23-3
- Fix missing -p1 on patch

* Fri Jan 30 2009 Steven M. Parrish <tuxbrewr@fedoraproject.org> 1.4.23-2
- Patch to fix WebKit issue in F11

* Sun Jan 11 2009 Steven M. Parrish <tuxbrewr@fedoraproject.org> 1.4.23
- New upstream release

* Sat Nov 22 2008 Steven M. Parrish <smparrish@shallowcreek.net> 1.4.22d-1
- New upstream release
- should fix #472636 #469351 #467083 #467874 #468214 

* Thu Oct 23 2008 Steven M. Parrish <smparrish@shallowcreek.net> 1.4.20-4
- Packaged the WebKit libs seperately so the default install uses
- XulRunner.  If the user wants to enable WebKit they need to 
- install the -WebKit sub-package

* Wed Oct 22 2008 Steven M. Parrish <smparrish@shallowcreek.net> 1.4.20-3
- Added support for WebKit
- Liferea will default to using Webkit, and will fallback to Xulrunner 
- if there are any initialization errors.

* Wed Oct 15 2008 Steven M. Parrish <smparrish@shallowcreek.net> 1.4.20-2
- Add missing patch file

* Wed Oct 15 2008 Steven M. Parrish <smparrish@shallowcreek.net> 1.4.20-1
- New upstream release and fix for #467083

* Thu Oct 02 2008  Steven M. Parrish <smparrish@shallowcreek.net> 1.4.19-1
- New upstream release

* Sat Aug 09 2008 Steven M. Parrish <smparrish@shallowcreek.net> - 1.4.18-1
- New upstream release

* Thu Jul 24 2008 Steven M. Parrish <smparrish@shallowcreek.net> - 1.4.17-1
- New upstream release

* Sun Jul 20 2008 Steven M. Parrish <tuxbrewr@fedoraproject.org> 1.4.16b-6
- fix missing dependencies

* Wed Jul 02 2008 Steven Parrish <smparrish@shallowcreek.net> - 1.4.16b-5
- corrected multiple segfaults.  Fixes Bug #453233

* Fri Jun 27 2008 Steven Parrish <smparrish@shallowcreek.net> - 1.4.16b-4
- removed uneeded patch files

* Fri Jun 27 2008 Steven Parrish <smparrish@shallowcreek.net> - 1.4.16b-43
- Cleaned up spec file and removed support for firefox-devel

* Thu Jun 26 2008 Steven Parrish <smparrish@shallowcreek.net> - 1.4.16b-1
- New upstream release

* Wed Jun 25 2008 Tomas Mraz <tmraz@redhat.com> - 1.4.15-6
- rebuild with new gnutls

* Thu May 15 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 1.4.15-5
- Bump version cause of my incompetence
- Change the patches from the bug should fix BZ#399541

* Thu May 15 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 1.4.15-4
- Change the gecko version

* Sun Apr 20 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 1.4.15-3
- Rebuild against xulrunner
- disable gtkhtml

* Sat Apr 19 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 1.4.15-2
- Rebuild against newer webkit

* Fri Apr 18 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 1.4.15-1
- Update to 1.4.15
- rebuilt with WebKit engine as liferea cannot be compiled with
  xulrunner (#399541)

* Mon Apr 07 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.13-2
- Rebuild for N-E-V-R issues.

* Mon Mar 17 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 1.4.13-1
- Updated to latest stable version

* Sat Feb 23 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 1.4.12-2
- Fixed fedora feed for fedora weekly news

* Wed Feb 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 1.4.12-1
- new version
- builds with gcc4.3
- added firefox-devel and xulrunner-devel for different fedora's

* Fri Feb  8 2008 Christopher Aillon <caillon@redhat.com> - 1.4.11-2
- Rebuild against newer gecko

* Thu Jan 17 2008 Brian Pepple <bpepple@fedoraproject.org> - 1.4.11-1
- Update to 1.4.11. release fixes news bin crasher. (#429021)

* Wed Dec 19 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.4.10-1
- Update to 1.4.10.
- Update feed patch.

* Sun Dec  2 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.4.9-1
- Update to 1.4.9.
- Update feed patch.

* Tue Nov 27 2007 Christopher Aillon <caillon@redhat.com> - 1.4.8-2
- Rebuild against newer gecko

* Thu Nov 22 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.4.8-1
- Update to 1.4.8.
- fixes LD_LIBRARY_PATH security bug. CVE-2006-4791

* Thu Nov 15 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.4.7-1
- Update to 1.4.7.
- Drop opml & nm patches. fixed upstream.
- Update fedora feed patch for 1.4.x.
- add BR on sqlite-devel, dbus-devel, dbus-glib-devel, libglade2-devel.
- Don't build gtkhtml2 plugin for now.

* Tue Nov  6 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.23-6
- Rebuild for new gecko libs.

* Wed Oct 31 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.23-5
- Add patch to fix opml security bug: CVE-2007-5751. (#360641)

* Wed Oct 24 2007 Jeremy Katz <katzj@redhat.com> - 1.2.23-4
- Fix build against new NetworkManager

* Tue Oct 23 2007 Jeremy Katz <katzj@redhat.com> - 1.2.23-3
- Don't build against NetworkManager as the nm-glib api seems to have changed

* Tue Oct 23 2007 Jeremy Katz <katzj@redhat.com> - 1.2.23-2
- Rebuild against new firefox

* Sat Sep  8 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.23-1
- Update to 1.2.23.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.22-1
- Update to 1.2.22.

* Thu Aug  9 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.21-2
- Rebuild against new gecko.

* Tue Aug  7 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.21-1
- Update to 1.2.21.

* Sun Aug  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.20-3
- Update license tag.

* Wed Jul 18 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.20-2
- Rebuild for new gecko-libs 1.8.1.5.

* Wed Jul 11 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.20-1
- Update to 1.2.20.

* Tue Jul  3 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.19-2
- Bump.

* Mon Jul  2 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.19-1
- Update to 1.2.19.

* Sun Jul  1 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.18-1
- Update to 1.2.18.

* Sat Jun 16 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.17-1
- Update to 1.2.17.

* Tue Jun  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.16b-1
- Update to 1.2.16b.

* Mon Jun  4 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.16-1
- Update to 1.2.16.

* Fri Jun  1 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.15b-2
- Rebuild for new gecko release.

* Fri May 18 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.15b-1
- Update to 1.2.15b.
- Drop cpu timer patch, fixed upstream.

* Sat May 12 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.10c-2
- Add patch to fix cpu from waking up frequently. (#239945)

* Thu Apr  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.10c-1
- Update to 1.2.10c.
- Update feed patch.

* Thu Mar 29 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.10b-1
- Update to 1.2.10b.

* Wed Mar 28 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.10-2
- Bump.

* Wed Mar 28 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.10-1
- Update to 1.2.10.

* Sat Mar 24 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9.

* Wed Mar 14 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8.

* Sun Mar  4 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.7-3
- Rebuild against firefox-2.0.0.1.

* Tue Feb 27 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.7-2
- Rebuild against new firefox.

* Wed Feb 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7.

* Sun Feb 11 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.6b-1
- Update to 1.2.6b.

* Thu Feb  8 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.6-1
- Update to 1.2.6.

* Mon Feb  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5.

* Sun Jan 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4.

* Wed Jan 17 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-2
- Add min. version of libxslt required.

* Wed Jan 10 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Thu Jan  4 2007 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.
- Remove *.in files that shouldn't be installed.

* Sun Dec 24 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Sat Dec 23 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-2
- Rebuild against new firefox.

* Sun Dec 17 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.
- Add scriptlets for gtk+ icon cache.
- Add BR for gnutls-devel, libnotify-devel, & NetworkManager-glib-devel.
- Add BR for perl(XML::Parser) & libxslt-devel.
- Drop BR on dbus-devel, since libnotify-devel will pull this in.
- Drop fonts patch, fixed upstream.

* Thu Dec  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.27-1
- Update to 1.0.27.

* Tue Nov 21 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.26-1
- Update to 1.0.26.
- Add patch to use document font name. (#216813)

* Sun Oct 29 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.25-3
- Actually use the correct version for firefox.

* Sun Oct 29 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.25-2
- Rebuild for new firefox.

* Fri Oct 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.25-1
- Update to 1.0.25.
- Drop X-Fedora category from desktop file.

* Thu Oct 19 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.24-1
- Update to 1.0.24.

* Thu Oct 12 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.23-3
- Add patch to add Fedora default feeds. (#209301)

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.0.23-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.23-1
- Update to 1.0.23.

* Fri Sep 15 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.22-2
- Bump firefox version to 1.5.0.7.

* Thu Aug 31 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.22-1
- Update to 1.0.22.

* Thu Aug 10 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.21-3
- Update to 1.0.21.
- Bump firefox version to 1.5.0.6.

* Mon Aug  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.20-4
- Add requires on specified version of firefox.

* Mon Aug  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.20-3
- Update to 1.0.20. (#199222)

* Mon Jul 31 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.19-3
- Update to 1.0.19.
- Build against firefox instead of mozilla. (#145752)

* Fri Jul 28 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.18-3
- Update to 1.0.18.

* Sat Jul 22 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.16-4
- Rebuild because of dbus soname change.

* Sun Jun 25 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.16-3
- Update to 1.0.16.

* Sun Jun 18 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.0.15-3
- Update to 1.0.15.
- Drop doc patch.

* Mon May 29 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.14-3
- Update to 1.0.14.
- Add patch to fix doc build.
- Drop NEWS, since it doesn't contain any useful info.

* Wed May  3 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.11-3
- Update to 1.0.11.

* Sat Apr 22 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.10-3
- Update to 1.0.10,
- Delete origianl desktop file with desktop-file-install call.
- Remove *.la, instead of excluding.

* Wed Apr  5 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.9-3
- Update to 1.0.9.

* Sat Mar 18 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.8-3
- Update to 1.0.8.
- Drop mozilla-lib64 patch, fixed upstream.

* Tue Mar 14 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.7-3
- Add patch to find mozilla on x86_64 (#185243).

* Mon Mar  6 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.7-2
- Update to 1.0.7.
- Fix gconf scriptlets.

* Sat Feb 25 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.6-2
- Update to 1.0.6.

* Thu Feb 16 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.4-4
- Remove unnecessary BR (zlib-devel & libxml2-devel).

* Mon Feb 13 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.4-3
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 10 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.4-2
- Update to 1.0.4.

* Tue Jan 31 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.3-2
- Update to 1.0.3.

* Wed Jan 25 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.2-2
- Update to 1.0.2.

* Mon Jan 16 2006 Brian Pepple <bdpepple@ameritech.net> - 1.0.1-1
- Update to 1.0.1.

* Mon Dec 26 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-4
- Dropp BR for libXdmcp-devel & libXau-devel, replace w/ libX11-devel (#176313).

* Sun Dec 25 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-3
- Add BR for libXdmcp-devel,libXau-devel, & libSM-devel.

* Fri Dec 23 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-2
- Update to 1.0.

* Sun Dec 04 2005 Luke Macken <lmacken@redhat.com> - 1.0-0.3.rc4
- Rebuild against dbus 0.60

* Fri Nov 18 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-0.2.rc4
- Update tp 1.0-RC4.

* Fri Nov  4 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-0.2.rc3
- Update to 1.0-RC3.

* Mon Oct 10 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-0.2.rc2
- Update to 1.0-RC2.

* Tue Oct  4 2005 Brian Pepple <bdpepple@ameritech.net> - 1.0-0.2.rc1
- Update to 1.0-RC1.

* Sun Sep  4 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.7b-2
- Update to 0.9.7b.

* Tue Aug 30 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.7a-2
- Update to 0.9.7a.

* Thu Aug 18 2005 Jeremy Katz <katzj@redhat.com> - 0.9.6-3
- rebuild for devel changes

* Mon Aug 15 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.6-2
- Update to 0.9.6.

* Sun Jul 31 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.5-2
- Update to 0.9.5.

* Fri Jul 22 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.4-2
- Update to 0.9.4.

* Thu Jul  7 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.3-1
- Update to 0.9.3.
- Enable dbus.
- Add dist tag.

* Thu May 12 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.2-1
- Update to 0.9.2
- Don't enable d-bus since old API is used.

* Sat Mar 12 2005 Brian Pepple <bdpepple@ameritech.net> - 0.9.1-1
- Updated to 0.9.1.
- Drop epoch: 0.

* Tue Jan 18 2005 Brian Pepple <bdpepple@gmail.com> - 0:0.9.0-0.1.b
- Updated to 0.9.0b.
- Remove seperate desktop file.

* Fri Jan 14 2005 Brian Pepple <bdpepple@gmail.com> - 0:0.9.0-0.fdr.1
- Updated to 0.9.0.

* Wed Jan 12 2005 Brian Pepple <bdpepple@gmail.com> - 0:0.6.4-0.fdr.1.b
- Updated to 0.6.4b.

* Mon Nov  1 2004 Brian Pepple <bdpepple@ameritech.net> - 0:0.6.1-0.fdr.1
- Updated to 0.6.1.
- Added %%exclude *.la
- Removed liferea-0.5.3c-fixes.patch, not needed anymore.
- Removed liferea-0.5.3b-mozillahome.patch, not needed anymore.

* Fri Sep 24 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.5.3-0.fdr.4.c
- Sync with Mozilla 1.7.3 update for FC2.

* Fri Sep 10 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.5.3-0.fdr.3.c
- Add memory leak fix + updates from 0.5.3c
  (tarball would require autoreconf).

* Fri Aug 27 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.5.3-0.fdr.2.b
- Add BR mozilla-devel to build Mozilla plugin.
- Patch liferea script to support FC1/FC2 Mozilla homes.

* Sat Aug 21 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.5.3-0.fdr.1.b
- Update to 0.5.3b (bug-fixes).
- Remove version from libxml2 requirement (2.4.1 would be sufficient).

* Thu Aug 19 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.5.3-0.fdr.1
- Update to 0.5.3.
- Add schemas un-/install in preun/post.
- Update desktop file.

* Wed Aug  4 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.5.2-0.fdr.1.c
- Add BR zlib-devel.
- Update desktop file.
- Adhere to versioning guidelines.

* Wed Aug 04 2004 Daryll Strauss <daryll@daryll.net> - 0:0.5.2c-0.fdr.1
- Updated to 0.5.2c

* Sat May 22 2004 Brian Pepple <bdpepple@ameritech.net> - 0:0.4.9-0.fdr.1
- Updated to 0.4.9
- Removed liferea_browser.patch.  Shouldn't be needed anymore.

* Thu May  6 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.8-0.fdr.1
- Updated to 0.4.8.
- Modified liferea_browser.patch to work with new version.
- Removed liferea.png that fedora.us provided, since package now supplies it's own.

* Fri Apr 30 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.7-0.fdr.5.d
- Applied browser.patch from Michael Schwendt (#1478)

* Wed Apr 28 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.7-0.fdr.4.d
- Updated to 0.4.7d.
- Removed patch, since it didn't fix browser problem.

* Fri Apr 23 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.7-0.fdr.4.c
- Add patch to use 'gnome-open %%s' instead of 'mozilla %%s'.

* Tue Apr 20 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.7-0.fdr.3.c
- Updated to 0.4.7c

* Sun Apr 11 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.7-0.fdr.3.b
- Updated to 0.4.7b
- Removed %%post/postun [#1478]

* Sun Apr 11 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.7-0.fdr.2
- Added liferea-bin to files.

* Fri Apr  2 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.7-0.fdr.1
- Updated to 0.4.7.
- Added %%post & %%postun
- Added %%{_libdir} files

* Tue Mar 30 2004 Brian Pepple <bdpepple@ameritech.net> 0:0.4.6-0.fdr.1.e
- Updated to 0.4.6e
- Added gettext build requirement

* Sun Jan 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.4.6-0.fdr.1.b
- Updated to 0.4.6b.

* Sun Nov 16 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.4.4-0.fdr.2
- BuildReq desktop-file-utils.

* Mon Nov 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.4.4-0.fdr.1
- Updated to 0.4.4.

* Thu Oct 16 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.4.3-0.fdr.1
- Updated to 0.4.3.

* Mon Oct 13 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.4.1-0.fdr.1
- Updated to 0.4.1.

* Fri Oct 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.4.0-0.fdr.1
- Updated to 0.4.0.

* Wed Oct 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.3.8-0.fdr.1
- Updated to 0.3.8.

* Tue Sep 23 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.3.7-0.fdr.3
- Correction in %%defattr.
- Improved Summary.
- Source now direct downloadable.

* Sun Sep 21 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.3.7-0.fdr.2
- epoch added to versioned req.

* Thu Sep 18 2003 Phillip Compton <pcompton[AT]proteinmedia.com> 0:0.3.7-0.fdr.1
- Initial Fedora Release.
