Name:           aisleriot
Epoch:          2
Version:        3.22.8
Release:        100%{?dist}
Summary:        A collection of card games

License:        GPLv3+ and LGPLv3+ and GFDL
URL:            https://wiki.gnome.org/Apps/Aisleriot
Source0:        http://download.gnome.org/sources/aisleriot/3.22/aisleriot-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(guile-2.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libcanberra-gtk3)
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  appdata-tools
BuildRequires:  yelp-tools
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib


%description
Aisleriot is a collection of over 80 card games programmed in scheme.

%prep
%autosetup -p1

%build
%configure \
  --with-platform=gtk-only
%make_build

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%make_install

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots %{buildroot}%{_datadir}/metainfo/sol.appdata.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/sol/a.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/sol/b.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/sol/c.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/sol/d.png 

# Omit the valgrind suppression file; only for use during development
rm %{buildroot}%{_libdir}/valgrind/aisleriot.supp

%find_lang %{name} --with-gnome

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/sol.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/sol.desktop


%files -f %{name}.lang
%doc AUTHORS
%license COPYING.GPL3 COPYING.LGPL3 COPYING.GFDL
%{_bindir}/*
%{_libdir}/aisleriot
%{_libexecdir}/aisleriot/
%{_datadir}/aisleriot
%{_datadir}/applications/sol.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/symbolic/apps/gnome-aisleriot-symbolic.svg
%{_datadir}/metainfo/sol.appdata.xml
%{_datadir}/glib-2.0/schemas/org.gnome.Patience.WindowState.gschema.xml
%{_mandir}/man6/sol.6*


%changelog
* Thu May 23 2019 Phantom X  <megaphantomx at bol dot com dot br> - 2:3.22.8-100
- --with-platform=gtk-only to remove GConf support

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 1:3.22.8-1
- Update to 3.22.8

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Kalev Lember <klember@redhat.com> - 1:3.22.7-1
- Update to 3.22.7

* Tue Sep 04 2018 Kalev Lember <klember@redhat.com> - 1:3.22.6-1
- Update to 3.22.6

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 1:3.22.5-1
- Update to 3.22.5

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.22.4-2
- Remove obsolete scriptlets

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 1:3.22.4-1
- Update to 3.22.4

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 1:3.22.3-1
- Update to 3.22.3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 1:3.22.2-1
- Update to 3.22.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 1:3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 1:3.22.0-1
- Update to 3.22.0
- Don't set group tags

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 1:3.20.2-1
- Update to 3.20.2

* Sun Mar 20 2016 Kalev Lember <klember@redhat.com> - 1:3.20.1-1
- Update to 3.20.1

* Sun Mar 20 2016 Kalev Lember <klember@redhat.com> - 1:3.20.0-1
- Update to 3.20.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Kalev Lember <klember@redhat.com> - 1:3.18.2-1
- Update to 3.18.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 1:3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 1:3.18.0-1
- Update to 3.18.0

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 1:3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.16.2-1
- Update to 3.16.2
- Include new symbolic app icon

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.16.1-1
- Update to 3.16.1

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 1:3.16.0-2
- Use better AppData screenshots

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.15.92-1
- Update to 3.15.92

* Wed Feb 18 2015 David King <amigadave@amigadave.com> - 1:3.15.0-2
- Remove unnecessary PySolGC theme path change

* Sun Feb 08 2015 David King <amigadave@amigadave.com> - 1:3.15.0-1
- Update to 3.15.0
- Set correct PySolFC card theme path
- Use license macro for COPYING.*
- Use pkgconfig for BuildRequires
- Update URL
- Update man page glob in files section

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.2-1
- Update to 3.14.2

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.1-1
- Update to 3.14.1

* Sun Sep 21 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.0-1
- Update to 3.14.0

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.13.90-1
- Update to 3.13.90

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 1:3.12.0-1
- Update to 3.12.0

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 1:3.10.2-1
- Update to 3.10.2

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 1:3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 1:3.10.0-1
- Update to 3.10.0

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.90-1
- Update to 3.9.90

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 1:3.8.0-1
- Update to 3.8.0

* Thu Mar 14 2013 Matthias Clasen <mclasen@redhat.com> - 1:3.7.91-1
- Update to 3.7.91

* Sat Feb 16 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.6.2-1
- Update to 3.6.2

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.2.3.2-2
- Update to 3.2.3.2

* Tue Apr  3 2012 Cosimo Cecchi <cosimoc@redhat.com> - 1:3.2.3.1-2
- Add an epoch to fix upgrade path from the 3.3 package we currently
  ship in F17

* Tue Apr  3 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.2.3.1-1
- Downgrade to 3.2.3.1, since >= 3.3 depends on guile 2.0 which is not
  available in Fedora yet

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1

* Wed Mar 21 2012 Richard Hughes <rhughes@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Thu Sep  8 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.1-2
- Package review feedback

* Wed Sep  7 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.1-1
- Initial packaging
