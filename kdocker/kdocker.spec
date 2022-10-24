%global project KDocker

%global _bashcompletiondir %(pkg-config --variable=completionsdir bash-completion)

Name:           kdocker
Summary:        Dock any application in the system tray
Version:        5.4
Release:        1%{?dist}

License:        GPLv2+
URL:            https://github.com/user-none/%{project}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  qtsingleapplication-qt5-devel
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xpm)

Requires:       hicolor-icon-theme


%description
%{project} will help you dock any application in the system tray. This means you
can dock OpenOffice, XMMS, Firefox, Thunderbolt, Eclipse, anything! Just point
and click. Works for LXQT/KDE and GTK/GNOME (In fact it should work for most
modern window managers that support NET WM Specification for instance).

All you need to do is start %{project} and select an application using the mouse
and lo! the application gets docked into the system tray. The application can
also be made to disappear from the task bar.


%prep
%autosetup -n %{project}-%{?gver:%{commit}}%{!?gver:%{version}} -p1
# unbundle qtsingleapplication
rm -fr 3rdparty

sed \
  -e 's|/usr/share/appdata|%{_metainfodir}|g' \
  -e 's|/etc/bash_completion.d|%{_bashcompletiondir}|g' \
  -i %{name}.pro

sed \
  -e '/\<icon.*cached/d' \
  -e '/\<screenshot\>\<\/screenshot\>/d' \
  -i helpers/appdata/%{name}.appdata.xml


%build
%qmake_qt5 SYSTEMQTSA=1

%{make_build}


%install
make install INSTALL_ROOT=%{buildroot}

install -m644 -p -D helpers/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

desktop-file-edit \
  --add-category="Qt" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license COPYING
%doc AUTHORS BUGS CREDITS ChangeLog README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_bashcompletiondir}/%{name}*
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Sun Oct 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.4-1
- 5.4

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Apr 04 2020 Raphael Groner <projects.rg@smart.ms> - 5.3-1
- new version

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Sep 01 2018 Raphael Groner <projects.rg@smart.ms> - 5.2-2
- fix changelog

* Sat Sep 01 2018 Raphael Groner <projects.rg@smart.ms> - 5.2-1
- new version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.1-1
- kdocker-5.1 (#1546587)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.0-10
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Sep 26 2015 Raphael Groner <projects.rg@smart.ms> - 5.0-4
- rebuild for Qt5.5

* Mon Jul 20 2015 Raphael Groner <projects.rg@smart.ms> - 5.0-3
- bump for rebuild cause of important fixes in qtsingleapplication

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Raphael Groner <projects.rg@smart.ms> - 5.0-1
- bump to version 5.0
- build for Qt5 where applicable (currently F22+ only)
- add special BR: pkgconfig(Qt5X11Extras)
- remove future man patch cause included now in new upstream version
- remove dedicated datadir folder, not provided any more from latest upstream
- include appdata file
- make files section to be more generical

* Tue May 05 2015 Raphael Groner <projects.rg at smart.ms> - 4.9-4
- update changelog with my correct e-mail address

* Fri May 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 4.9-3
- %%build: use SYSTEMQTSA=1 instead of CONFIG+=qtsingleapplication
- Qt5 support not ready yet

* Fri May 01 2015 Raphael Groner <projects.rg at smart.ms> - 4.9-2
- build for Qt5 (where applicable)

* Sat Mar 28 2015 Raphael Groner <projects.rg at smart.ms> - 4.9-1
- upstream moved to GitHub
- new version v4.9
- still use Qt4
- but support for Qt5 conflicts with our qtsingleapplication R: qt4 (rhbz#1206841)
- remove help2man in favor of upstream manpage

* Wed Feb 25 2015 Raphael Groner <projects.rg at smart.ms> - 4.8-2
- fix review issues

* Sun Feb 22 2015 Raphael Groner <projects.rg at smart.ms> - 4.8-1
- unretire package
- new upstream release v4.8

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 25 2010 Thomas Janssen <thomasj@fedoraproject.org> 4.3-2
- added BRs

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3-1
- kdocker-4.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 02 2008 Rex Dieter <rdieter@fedoraproject.org> 1.3-11
- BR: qt3-devel

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-10
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.3-9
- License: GPLv2+
- respin (BuildID)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.3-8
- fc6 respin

* Wed May 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.3-7
- rework -paths patch

* Fri Apr 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.3-6
- --vendor=""

* Fri Mar 10 2006 Rex Dieter <rexdieer[AT]users.sf.net> 1.3-5
- build failure, useless -debuginfo (#180103)

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 
- fc5: gcc/glibc respin

* Sat Jan 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.3-4
- .desktop: fix path to app-icon (#178531)

* Tue Nov 01 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.3-3
- remove dup'd docs
- %%lang'ify i18n bits

* Mon Oct 31 2005 Rex Dieter 1.3-2
- use desktop-file-install 

* Mon Oct 31 2005 Rex Dieter 1.3-1
- cleanup for Extras

* Tue Feb 15 2005 Rex Dieter 1.3-0.1
- 1.3 (first try)
