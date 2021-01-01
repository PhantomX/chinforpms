%global xfceversion %%(echo %{version} | cut -d. -f1-2)

# Disabled, no GTK3 panel support
%global with_xfce4panel 0

Name:           orage
Version:        4.12.1
Release:        100%{?dist}
Summary:        Time-managing application for Xfce4

License:        GPLv2+
URL:            http://www.xfce.org/

Source0:        http://archive.xfce.org/src/apps/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2

Patch0:         %{name}-%{version}-libical3.patch

#VCS: git:git://git.xfce.org/apps/orage
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.14.0
BuildRequires:  pkgconfig(libnotify) >= 0.3.2
BuildRequires:  pkgconfig(libical) >= 0.43
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.34
BuildRequires:  pkgconfig(popt)
BuildRequires:  gettext
BuildRequires:  intltool >= 0.31
BuildRequires:  desktop-file-utils
Requires:       dbus

%if 0%{?with_xfce4panel}
BuildRequires:  pkgconfig(libxfce4panel-1.0) >= 4.6.0
Requires:       xfce4-panel
%endif

Provides:       xfcalendar = %{version}-%{release}
Obsoletes:      xfcalendar <= 4.2.3-3.fc6

%description
Orage provides a calendar which integrates nicely into the Xfce Desktop 
Environment. It is highly configurable and supports alerts based on dates. 
It warns you with popup or audio alarm. As it is an application for every 
day use it launches itself in the background as a daemon and can be accessed 
using the Orage Clock plugin for the panel. 

%prep
%autosetup -p1


%build
export CFLAGS="%{build_cflags} -I/usr/include/libical"
%configure \
  --disable-static \
  --enable-libical \
%if !0%{?with_xfce4panel}
  --disable-libxfce4panel \
%endif
%{nil}

%make_build


%install
%make_install

%find_lang %{name}

desktop-file-edit \
  %{buildroot}%{_datadir}/applications/xfcalendar.desktop

desktop-file-edit \
  --remove-category Application \
  %{buildroot}%{_datadir}/applications/globaltime.desktop

# remove unneeded .la file
rm -f %{buildroot}%{_libdir}/xfce4/panel/plugins/liborageclock.la

%if !0%{?with_xfce4panel}
rm -f %{buildroot}%{_datadir}/xfce4/panel/plugins/*.desktop
rmdir -p %{buildroot}%{_datadir}/xfce4/panel/plugins ||:
%endif


%files -f %{name}.lang
%license COPYING
%doc README ChangeLog AUTHORS
%{_bindir}/globaltime
%{_bindir}/orage
%{_bindir}/tz_convert
%{_datadir}/applications/*xfcalendar.desktop
%{_datadir}/applications/globaltime.desktop
%{_datadir}/applications/xfce-xfcalendar-settings.desktop
%{_datadir}/orage/
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/dbus-1/services/org.xfce.calendar.service
%{_datadir}/dbus-1/services/org.xfce.orage.service
%if 0%{?with_xfce4panel}
%{_datadir}/xfce4/panel/plugins/xfce4-orageclock-plugin.desktop
%{_libdir}/xfce4/panel/plugins/liborageclock.so
%endif
%{_mandir}/man1/globaltime.1.*
%{_mandir}/man1/orage.1.*
%{_mandir}/man1/tz_convert.1.*


%changelog
* Thu Dec 31 2020 Phantom X <megaphantomx at hotmail dot com> - 4.12.1-100
- Panel plugin switch, disabled

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 14 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.1-10
- Add patch to build against libical3
- Minor spec cleanup

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 4.12.1-6
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Kevin Fenzi <kevin@scrye.com> - 4.12.1-4
- Rebuild for new libical

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 4.12.1-3
- Remove no longer required AppData file

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Kevin Fenzi <kevin@scrye.com> 4.12.1-1
- Update to 4.12.1

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 4.10.0-6
- Add an AppData file for the software center

* Sat Feb 28 2015 Kevin Fenzi <kevin@scrye.com> 4.10.0-5
- Rebuild for Xfce 4.12

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4.10.0-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 11 2013 Kevin Fenzi <kevin@scrye.com> 4.10.0-1
- Update to 4.10.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Rex Dieter <rdieter@fedoraproject.org> 4.8.4-3
- rebulid (libical)

* Tue Apr 30 2013 Jon Ciesla <limburgher@gmail.com> 4.8.4-2
- Drop desktop vendor tag.

* Fri Feb 01 2013 Kevin Fenzi <kevin@scrye.com> 4.8.4-1
- Update to 4.8.4

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 15 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.3-3
- Rebuild for Xfce 4.10(pre2)

* Wed Apr 04 2012 Kevin Fenzi <kevin@scrye.com> - 4.8.3-2
- Rebuild for Xfce 4.10

* Thu Jan 05 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.3-1
- Update to 4.8.3
- Remove the icon hack, orage now ships it's own
- Drop obsolete BR on startup-notification-devel
- Add VCS key

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.2-3
- Rebuilt for glibc bug#747377

* Sun Oct 23 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-2
- Fix menu icon for globaltime (#748234)

* Tue Sep 13 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2

* Sun May 08 2011 Christoph Wickert <wickert@kolabsys.com> - 4.8.1-3
- Move xfce4-clock icons to xfce4-panel and require it

* Tue Mar 29 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-2
- Add xfce4-clock icon for globaltime (#678702)

* Sat Feb 26 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1
- Remove libnotify patch (upstreamed)
- Fix menu entries and show them not only in Xfce

* Thu Feb 17 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.0-3
- Spec file clean-up
- Update icon-cache scriptlets
- No longer require db4-devel and xfce4-dev-tools

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2 
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild 

* Thu Jan 13 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0

* Sun Jan 09 2011 Kevin Fenzi <kevin@tummy.com> - 4.7.6.13-1
- Upgrade to 2011-01-09 git snapshot

* Fri Nov 05 2010 Kevin Fenzi <kevin@tummy.com> - 4.7.5.16-3
- Add patch for new libnotify

* Mon Aug 23 2010 Ville Skyttä <ville.skytta@iki.fi> - 4.7.5.16-2
- Build with $RPM_OPT_FLAGS.

* Sat Aug 14 2010 Kevin Fenzi <kevin@tummy.com> - 4.7.5.16-1
- Update to 4.7.5.16

* Sat Feb 13 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.1-2
- Add patch to fix DSO linking. Fixes bug 564740

* Thu Sep 10 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-1
- Update to 4.6.1
- Update package deskription
- Require dbus

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sun Dec 28 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update to 4.5.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.3-1
- Update to 4.4.3
- BuildRequire intltool
- No longer BuildRequire dbh-devel
- Configure with --disable-static
- Update gtk-update-icon-cache scriptlets

* Sat Mar 01 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-3
- Modify desktop to only show in Xfce, as orage requires xfce-mcs-manager

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Update License tag

* Wed Jul  4 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-2
- Fix category in desktop file (fixes #243601)

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Thu Nov 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-2
- Add db4-devel to BuildRequires

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update 4.3.99.2

* Sun Oct 15 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-6
- xfce4-datetime-plugin is back, remove obsoletes and provides

* Sat Oct  7 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-5
- Fix Obsoletes

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-4
- Add period at the end of description. 
- Fix defattr
- Add gtk-update-icon-cache

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Bump release for devel checkin

* Sun Sep 24 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Obsolete xfce4-datetime-plugin

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Update to 4.3.99.1
- Added desktop files 

* Wed Aug 30 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-1
- Update to 4.3.90.2 and change name to orage

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3-1.fc5
- Update to 4.2.3
- Added dist tag

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Sat May  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-5.fc3
- Add missing dbh-devel buildrequires

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-4.fc4
- lowercase Release

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.FC4
- Remove unneeded la/a files

* Sun Mar 20 2005 Warren Togami <wtogami@redhat.com> - 4.2.1-2
- fix BuildRequires

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Fixed to use %%find_lang
- Removed generic INSTALL from %%doc
- Added BuildRequires for xfce-mcs-manager-devel

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-1
- Inital Fedora Extras version
