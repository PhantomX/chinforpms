%if 0%{?fedora} >= 40
%global build_type_safety_c 0
%endif

%global minor_version %%(echo %{version} | cut -d. -f1-2)
%global xfceversion 4.14

%global vc_url https://gitlab.xfce.org/panel-plugins/%{name}

Name:           xfce4-notes-plugin
Version:        1.11.2
Release:        100%{?dist}
Summary:        Notes plugin for the Xfce panel

Epoch:          1

License:        GPL-2.0-or-later
URL:            https://docs.xfce.org/panel-plugins/%{name}
Source0:        https://archive.xfce.org/src/panel-plugins/%{name}/%{minor_version}/%{name}-%{version}.tar.bz2

Patch0:         0001-Disable-automatic-autostart-settings.patch

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.22
BuildRequires:  pkgconfig(libxfce4panel-2.0) >= %{xfceversion}
BuildRequires:  pkgconfig(libxfce4ui-2) >= %{xfceversion}
BuildRequires:  pkgconfig(libxfce4util-1.0) >= %{xfceversion}
BuildRequires:  pkgconfig(libxfconf-0) >= %{xfceversion}
BuildRequires:  pkgconfig(gtksourceview-4)
BuildRequires:  gettext, intltool, desktop-file-utils
Requires:       xfce4-panel >= %{xfceversion}
Requires:       xfconf >= %{xfceversion}
Requires:       exo

%description
This plugin provides sticky notes for your desktop. You can create a note by 
clicking on the customizable icon with the middle button of your mouse, 
show/hide the notes using the left one, edit the titlebar, change the notes 
background color and much more.


%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang %{name}

desktop-file-validate \
  %{buildroot}%{_sysconfdir}/xdg/autostart/xfce4-notes-autostart.desktop
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/xfce4-notes.desktop


%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README.md
%license COPYING
%config(noreplace) %{_sysconfdir}/xdg/autostart/xfce4-notes-autostart.desktop
%{_bindir}/xfce4-notes
%{_bindir}/xfce4-popup-notes
%{_bindir}/xfce4-notes-settings
%{_libdir}/xfce4/panel/plugins/libnotes.so
%{_datadir}/applications/xfce4-notes.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/xfce4/panel/plugins/*.desktop
%{_datadir}/xfce4/notes/gtk-3.0/gtk.css


%changelog
* Sat Feb 01 2025 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.2-100
- 1.11.2

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.0-100
- 1.11.0

* Sat Mar 18 2023 Phantom X <megaphantomx at hotmail dot com> - 1.10.0-100
- 1.10.0

* Tue Aug 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1.9.0-102
- Little upstream fix

* Tue Jan 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.9.0-101
- Disable autostart automatic settings

* Tue Jan 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.9.0-100
- 1.9.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Aug 11 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 1.8.1-20
- Rebuilt (xfce 4.13)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.8.1-7
- Spec cleanup / modernization

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 24 2015 Kevin Fenzi <kevin@scrye.com> 1.8.1-1
- Update to 1.8.1

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 13 2015 Kevin Fenzi <kevin@scrye.com> 1.8.0-1
- Update to 1.8.0

* Sat Feb 28 2015 Kevin Fenzi <kevin@scrye.com> 1.7.7-12
- Rebuild for Xfce 4.12

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.7.7-11
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 15 2012 Kevin Fenzi <kevin@scrye.com> - 1.7.7-5
- Rebuild for Xfce 4.10(pre2)

* Thu Apr 05 2012 Kevin Fenzi <kevin@scrye.com> - 1.7.7-4
- Rebuild for Xfce 4.10

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.7.7-2
- Rebuild for new libpng

* Tue Feb 22 2011 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Adam Williamson <awilliam@redhat.com> - 1.7.6-2
- adjust file list for new location of plugin, remove .la file

* Wed Mar 31 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6
- Drop DSO linking patch, fixed upstream

* Mon Mar 29 2010 Mar 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.4-1
- Update to 1.7.4
- Use exo-open to open URLs (#577548)

* Sat Mar 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.3-1
- Update to 1.7.3

* Wed Feb 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.2-2
- Add patch to fix DSO linking (#565043)

* Sun Dec 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2
- New build dep: unique-devel

* Fri Sep 04 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0
- Update gtk-update-icon-cache scriptlets

* Sun Mar 01 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.4-1
- Update to 1.6.4

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.3-2
- Rebuild for Xfce 4.6 (Beta 3)
- Enable Xfconf settings dialog

* Thu Nov 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.3-1
- Update to 1.6.3
- BR intltool
- Update gtk-update-icon-cache scriptlets

* Sat May 24 2008 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6.1-2
- Autorebuild for GCC 4.3

* Sat Dec 29 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1
- BR Thunar-devel for new file system monitoring feature

* Fri Dec 07 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.0-2
- Rebuild for Xfce 4.4.2

* Sat Nov 24 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Sat Aug 25 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.1-3
- Rebuild for BuildID feature
- Update license tag

* Sat Apr 28 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.1-2
- Rebuild for Xfce 4.4.1

* Mon Jan 22 2007 Christoph Wickert <cwickert@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1 on Xfce 4.4.

* Sun Nov 26 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.4-1
- Update to 1.4.

* Thu Oct 05 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.99.1-3
- Bump release for devel checkin.

* Wed Sep 13 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.99.1-2
- Rebuild for XFCE 4.3.99.1.
- BR perl(XML::Parser).

* Thu Sep 07 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.99.1-1
- Update to 1.3.99.1.

* Mon Sep 04 2006 Christoph Wickert <cwickert@fedoraproject.org> - 1.3.90.2-1
- Update to 1.3.90.2 on XFCE 4.3.90.2.

* Mon Sep 04 2006 Christoph Wickert <cwickert@fedoraproject.org> - 0.11.1-5
- Mass rebuild for Fedora Core 6.

* Tue Apr 11 2006 Christoph Wickert <fedora wickert at arcor de> - 0.11.1-4
- Require xfce4-panel.

* Thu Feb 16 2006 Christoph Wickert <fedora wickert at arcor de> - 0.11.1-3
- Rebuild for Fedora Extras 5.

* Thu Dec 01 2005 Christoph Wickert <fedora wickert at arcor de> - 0.11.1-2
- Add libxfcegui4-devel BuildReqs.
- Fix %%defattr.

* Mon Nov 14 2005 Christoph Wickert <fedora wickert at arcor de> - 0.11.1-1
- Initial Fedora Extras version.
- Update to 0.11.1.
- disable-static instead of removing .a files.

* Fri Sep 23 2005 Christoph Wickert <fedora wickert at arcor de> - 0.10.0-2.fc4.cw
- Add libxml2 BuildReqs.

* Sat Jul 09 2005 Christoph Wickert <fedora wickert at arcor de> - 0.10.0-1.fc4.cw
- Rebuild for Core 4.

* Thu Apr 14 2005 Christoph Wickert <fedora wickert at arcor de> - 0.10.0-1.fc3.cw
- Initial RPM release.
