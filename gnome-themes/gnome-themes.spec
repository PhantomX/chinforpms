%global majorminor %%(echo %{version} | cut -d. -f1-2)

Name:           gnome-themes
Version:        2.32.0
Release:        22%{?dist}
Summary:        Themes for GNOME

License:        LGPL-2.1-only AND GPL-2.0-only
URL:            http://download.gnome.org/sources/gnome-themes

#VCS: git:git://git.gnome.org/gnome-themes
Source:         %{url}/%{majorminor}/%{name}-%{version}.tar.bz2

BuildArch:      noarch

Requires:       gtk2-engines
Requires:       gnome-icon-theme

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  intltool
BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  libtool
BuildRequires:  gettext
BuildRequires:  gtk2-engines-devel
BuildRequires:  icon-naming-utils

%description
The gnome-themes package contains a collection of desktop themes for GNOME.
These themes can change the appearance of application widgets, icons, window
borders, cursors, etc.

%package legacy
Summary: Old names for icons in gnome-themes
Requires: %{name} = %{version}-%{release}

%description legacy
This package contains symlinks to make the icons in gnome-themes
available under old names.

%prep
%autosetup

%build
%configure
%make_build


%install
%make_install

# Clearlooks gtk theme is in gtk2-engines
rm -rf %{buildroot}%{_datadir}/themes/Clearlooks/gtk-2.0
rm -f %{buildroot}%{_datadir}/themes/ThinIce/README.html
rm -f %{buildroot}%{_datadir}/themes/ThinIce/ICON.png
# Remove the test theme
rm -rf %{buildroot}%{_datadir}/themes/ClearlooksTest/

# Accessibility themes are now in gnome-themes-standard
rm -rf %{buildroot}%{_datadir}/themes/HighContrast/
rm -rf %{buildroot}%{_datadir}/themes/HighContrastInverse/
rm -rf %{buildroot}%{_datadir}/themes/HighContrastLargePrint/
rm -rf %{buildroot}%{_datadir}/themes/HighContrastLargePrintInverse
rm -rf %{buildroot}%{_datadir}/themes/LowContrast/
rm -rf %{buildroot}%{_datadir}/themes/LowContrastLargePrint
rm -rf %{buildroot}%{_datadir}/themes/Inverted/
rm -rf %{buildroot}%{_datadir}/themes/LargePrint
rm -rf %{buildroot}%{_datadir}/icons/HighContrast/
rm -rf %{buildroot}%{_datadir}/icons/HighContrastInverse/
rm -rf %{buildroot}%{_datadir}/icons/HighContrastLargePrint/
rm -rf %{buildroot}%{_datadir}/icons/HighContrastLargePrintInverse/
rm -rf %{buildroot}%{_datadir}/icons/HighContrast-SVG/
rm -rf %{buildroot}%{_datadir}/icons/LargePrint/

# add legacy symlinks
for size in 16x16 22x22 24x24 32x32 48x48 256x256; do
  for context in actions apps devices places status; do
    (cd %{buildroot}%{_datadir}/icons/Mist/$size
     icon-name-mapping -c $context)
  done
done

# we want to own the icon caches
for dir in %{buildroot}%{_datadir}/icons/*; do
  touch $dir/icon-theme.cache
done

(cd %{buildroot}%{_datadir}
 find icons/Mist -type l -and -not -name "gtk-\*" -printf "%%%%{_datadir}/%%p\n"
) > legacy.txt

%find_lang %{name}

%post
for icon_theme in Crux Mist ; do
  touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
done

%postun
if [ $1 -eq 0 ]; then
for icon_theme in Crux Mist ; do
  touch --no-create %{_datadir}/icons/${icon_theme} &> /dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done
fi

%posttrans
for icon_theme in Crux Mist ; do
  gtk-update-icon-cache %{_datadir}/icons/${icon_theme} &> /dev/null || :
done


%files -f  %{name}.lang
%{_datadir}/icons/Crux/
%{_datadir}/icons/Mist/

# themes where the gtk theme is shipped with the engine
%{_datadir}/themes/Clearlooks/*
%{_datadir}/themes/Crux/*
%{_datadir}/themes/Mist/*

# others
%{_datadir}/themes/Glider
%{_datadir}/themes/Glossy
%{_datadir}/themes/ClearlooksClassic
%{_datadir}/themes/Simple

%doc AUTHORS COPYING NEWS README

%files legacy -f legacy.txt

%changelog
* Mon Oct 12 2020 Phantom X <megaphantomx at hotmail dot com> - 2.32.0-22
- chinforpms take

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-7
- Rebuilt for glibc bug#747377

* Mon May 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.0-6
- Drop accessibility themes to avoid conflict with gnome-themes-standard
- Sync with F15

* Fri Apr 15 2011 Dennis Gilmore <dennis@ausil.us> - 2.32.0-5
- drop Requires on gtk-theme-engine-clearlooks since it no longer exists

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.32.0-3
- Don't require gtk3-engines, they don't work with gtk3 anymore

* Fri Oct 15 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.32.0-2
- Merge-review cleanup (#225840)

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> 2.32.0-1
- Update to 2.32.0

* Tue Aug 17 2010 Matthias Clasen <mclasen@redhat.com> 2.31.90-1
- Update to 2.31.90

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-1
- Update to 2.31.6

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-2
- Require gtk3-engines, so it gets into existing installs

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-1
- Update to 2.31.4

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-1
- Update to 2.31.2

* Mon May 24 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-2
- Create more symlinks
- Split off a legacy subpackage

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Update to 2.31.1

* Thu Apr 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1

* Tue Apr  6 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-3
- Fix rendering problems with metacity titlebars in Indic locales

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-2
- Add new, better Mist icons

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Wed Feb 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.29.91-2
- update/optimize icon scriptlets
- fix/sync sources/.cvsignore

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.6-1
- Update to 2.29.6

* Fri Dec  4 2009 Matthias Clasen <mclasen@redhat.com> - 2.29.2-1
- Update to 2.29.2

* Tue Oct 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-2
- Add scalable versions of the xdg folder icons to Mist

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Sun Oct 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Add xdg folder icons to Mist

* Tue Sep 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Tue Aug 10 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/gnome-themes/2.26/gnome-themes-2.26.1.news

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Mon Dec  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-2
- BR gtk2-engines-devel

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-3
- Improve description

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Update to 2.25.1

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Tue Aug  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.5-2
- fix license tag

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-2
- Fix source url

* Thu Apr 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Fri Feb 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-2
- Require gnome-icon-theme (#432715)O

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2
- Drop old Clearlooks tweaking

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1 (translation updates)

* Wed Sep 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90
- Update the license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Mon Jul  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Thu Jun  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-2
- Fix directory ownership issues

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Fri Feb 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-2
- Own the icon caches

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Sat Jan 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-3
- Re-add the Clearlooks icon theme

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Sun Nov 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-2
- Drop Clearlooks variants (#215114)

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1.1-1
- Update to 2.16.1.1

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91.1-1.fc6
- Update to 2.15.91.1

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4
- Drop the variant of the Clearlooks metacity theme
 
* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Mon Jun 12 2006 Bill Nottingham <notting@redhat.com> - 2.15.2-3
- buildreq automake, not automake17

* Wed Jun  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-2
- Fix a problem in %%post (#194323)

* Tue May 16 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Thu Feb  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-3
- Fix a warning

* Tue Feb  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-2
- Remove the hidden patch, since it causes icon themes
  to not show up in the theme capplet

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90

* Tue Dec 21 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.2-3
- Make sure the new Clearlooks metacity theme gets picked up

* Tue Dec 20 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.2-2
- Update the Clearlooks metacity theme

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.2-1
- Update to 2.13.2
- Drop upstreamed patches/sources

* Tue Oct 25 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.1-4
- Add one more a11y icon

* Mon Oct 24 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.1-3
- Improve the coverage of the stock gtk icons by the
  a11y themes.

* Wed Oct 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.1-2
- Silence %%post

* Fri Oct  5 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Fri Sep 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-2
- Fix pixmap paths
- Actually apply the redmond patch

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0
- Adjust clearlooks patch

* Mon Aug 22 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.91-2
- Remove conflicting files 

* Fri Aug 19 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.91-1
- New upstream version

* Thu Aug 10 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.90-2
- Remove uses of the redmond engine

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.90-1
- New upstream version
- Clearlooks 0.6.2

* Wed Jun 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.3-2
- noarch

* Tue Jun 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.3-1
- Update to 2.11.3 and Clearlooks 0.6.1

* Wed Apr 27 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-2
- Patch Clearlooks icon theme to inherit from bluecurve

* Tue Apr 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Thu Mar 17 2005 Matthias Clasen <mclasen@redhat.com> - 2.10.0-2
- Include Clearlooks themes, version 0.4

* Mon Mar 14 2005 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Sun Mar  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.95-2
- Fix %%post script (#146661)

* Sat Mar  5 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.95-1
- Update to 2.9.95

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.94-1
- Update to 2.9.94

* Sat Feb  5 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-3
- Silence gtk-update-icon-cache

* Fri Jan 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-2
- Prereq gtk2 since we use gtk-update-icon-cache in %%post

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-1
- update to 2.9.90
- update icon caches in %%post

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- update to 2.8.0

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92
- remove autogenerated files from hidden patch

* Fri Aug 13 2004 Alexander Larsson <alexl@redhat.com> - 2.7.90-1
- update to 2.7.90

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Apr 11 2004 Warren Togami <wtogami@redhat.com> 2.6.0-2
- BR autoconf automake14 intltool pkgconfig gtk2-devel libtool gettext

* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 2.6.0-1
- Update to 2.6.0

* Wed Mar 17 2004 Alex Larsson <alexl@redhat.com> 2.5.92-1
- update to 2.5.92
- gtk binary age changed

* Wed Mar 10 2004 Alex Larsson <alexl@redhat.com> 2.5.91-1
- update to 2.5.91

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.5.4-1
- update to 2.5.4

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jonathan Blandford <jrb@redhat.com> 2.5.3-1
- new version
- new version

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- 2.4.0

* Thu Aug 14 2003 Alexander Larsson <alexl@redhat.com> 2.3.3-1
- update to gnome 2.3

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 2.2-7
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix find_lang

* Wed Apr 16 2003 Than Ngo <than@redhat.com> 2.2-4
- make gnome-icon themes hidden in KDE

* Wed Feb 19 2003 Jonathan Blandford <jrb@redhat.com> 2.2-2
- remove a thinice file also included in gtk-engines, #84398

* Wed Feb 12 2003 Bill Nottingham <notting@redhat.com>
- fix group typo

* Tue Feb  4 2003 Jonathan Blandford <jrb@redhat.com>
- new release.  This one includes a thinice tarball.

* Thu Jan 30 2003 Jonathan Blandford <jrb@redhat.com>
- new version

* Tue Jan 28 2003 Jonathan Blandford <jrb@redhat.com>
- Initial build.


