Name:       psi
Version:    1.3
Release:    1.chinfo%{?dist}
Summary:    Jabber client based on Qt
License:    GPLv2+
URL:        http://psi-im.org

Source0:    http://sf.net/projects/%{name}/files/Psi/%{version}/%{name}-%{version}.tar.xz

# Language packs
Source10:   https://github.com/psi-im/psi-l10n/archive/1.3.tar.gz#/%{name}-l10n-%{version}.tar.gz

# Iconsets
Source11:   http://pkgs.fedoraproject.org/repo/pkgs/psi/emoticons-0.10.tar.gz/md5/1b4b3374c676c330c87e2ef0cd9109fa/emoticons-0.10.tar.gz
Source12:   http://pkgs.fedoraproject.org/repo/pkgs/psi/rostericons-0.10.tar.gz/md5/51386c12abbee7100f092455bfb88bf1/rostericons-0.10.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5WebKit)
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libidn)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(qca2-qt5)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  desktop-file-utils

Requires: sox
Requires: gnupg
# Required for SSL/TLS connections
Requires:       qca-qt5-ossl%{?_isa}
# Required for GnuPG encryption
Requires:       qca-qt5-gnupg%{?_isa}
Requires:       hicolor-icon-theme

# FIXME: wait for upstream to unbundle iris, rhbz#737304, https://github.com/psi-im/iris/issues/31
Provides:   bundled(iris) = 1.0.0

%description
%{name} is the premiere Instant Messaging application designed for Microsoft
Windows, Apple Mac OS X and GNU/Linux. Built upon an open protocol named
Jabber, %{name} is a fast and lightweight messaging client that utilises the best
in open source technologies. %{name} contains all the features necessary to chat,
with no bloated extras that slow your computer down. The Jabber protocol
provides gateways to other protocols as AIM, ICQ, MSN and Yahoo!.
If you want SSL support, install the qca-tls package.

%package l10n
Summary:    Language packs for %{name}
BuildArch:  noarch
Requires:   %{name} = %{version}
Obsoletes:  psi-i18n

%description -n %{name}-l10n
This package adds internationalization to %{name}.
If you want to add a translation from http://%{name}-im.org,
just put the .qm file in %{_datadir}/%{name} (you'll have to do
this as root), and restart %{name}.

%package icons
Summary:    Additional icons for %{name}
BuildArch:  noarch
Requires:   %{name} >= 0.9.1

%description -n %{name}-icons
This package contains additional icons for %{name}
There are three types of icons:
- emoticons, also known as smileys
- roster icons, to change the appearance of %{name}'s main window
- system icons, to change the rest of %{name}'s icons
More icons can be found on http://jisp.netflint.net


%prep
%autosetup -a 10
rm -rf configure configure.exe mac win32

# Remove bundled libraries
rm -fr src/libpsi/tools/zip/minizip
rm -fr iris/src/jdns

# FIXME unbundle iris
#rm -r iris

%build

mkdir -p build
pushd build

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DUSE_HUNSPELL:BOOL=ON \
  -DUSE_QT5:BOOL=ON \
  -DENABLE_WEBKIT:BOOL=ON


%make_build

popd

pushd psi-l10n-*/translations
lrelease-qt5 *.ts
popd

%install
%make_install -C build

# Install language packs
install -pm0644 psi-l10n-*/translations/*.qm %{buildroot}%{_datadir}/%{name}/

## Install iconsets
tar -xzpf %{SOURCE11} -C %{buildroot}%{_datadir}/%{name}/iconsets/emoticons/
tar -xzpf %{SOURCE12} -C %{buildroot}%{_datadir}/%{name}/iconsets/roster/

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
ln -sf ../../../../pixmaps/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

for res in 16 32 48 64 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 iconsets/system/default/logo_${res}.png \
    ${dir}/%{name}.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :


%files
%license COPYING
%doc README
%{_bindir}/%{name}
%{_datadir}/%{name}
%_datadir/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%exclude %{_datadir}/%{name}/*.qm
%exclude %{_datadir}/%{name}/iconsets/*/*.jisp

%files l10n
%{_datadir}/%{name}/%{name}_*.qm

%files icons
%{_datadir}/%{name}/iconsets/*/*.jisp


%changelog
* Wed Dec 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1.chinfo
- 1.3
- Qt5 support
- cmake

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb  4 2016 Ivan Romanov <drizt@land.ru> - 0.15-17
- Fix armhfp compilation rhbz #1304549

* Fri Jan 22 2016 Rex Dieter <rdieter@fedoraproject.org> 0.15-16
- fix build flags harder (#1301086)

* Mon Jan 18 2016 Rex Dieter <rdieter@fedoraproject.org> 0.15-15
- ensure proper qmake and build flags (see also bug #1279265)

* Wed Jan  6 2016 Ivan Romanov <drizt@land.ru> - 0.15-14
- Rebuild with forgottent patch

* Wed Jan  6 2016 Ivan Romanov <drizt@land.ru> - 0.15-13
- Rebuild with new qconf
- Use external minizip
- Update qjdns patch

* Mon Nov 23 2015 Raphael Groner <projects.rg@smart.ms> - 0.15-12
- use better configure options
- modernize, restructure and cleanup for better readability

* Sun Nov 22 2015 Raphael Groner <projects.rg@smart.ms> - 0.15-11
- bump for rebuild

* Wed Oct 14 2015 Raphael Groner <projects.rg@smart.ms> - 0.15-10
- bundled(iris), rhbz#737304
- cleanup

* Thu Jul 23 2015 Raphael Groner <projects.rg@smart.ms> - 0.15-9
- bump for rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.15-7
- Rebuilt for GCC 5 C++11 ABI change

* Fri Dec 12 2014 Raphael Groner <projects.rg [AT] smart.ms> - 0.15-6
- unbundle jdns (and iris later)
- cleanup to spec

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 05 2012 Sven Lankes <sven@lank.es> - 0.15-1
- new upstream release

* Wed Sep 26 2012 Sven Lankes <sven@lank.es> - 0.15-0.2.rc3
- new upstream release

* Tue Sep 18 2012 Sven Lankes <sven@lank.es> - 0.15-0.2.rc2
- new upstream release

* Tue Aug 28 2012 Sven Lankes <sven@lank.es> 0.15-0.2.rc1
- new upstream release

* Wed Aug 22 2012 Sven Lankes <sven@lank.es> 0.15-0.1beta2
- new upstream (beta) release
- drop all patches (all upstream now)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 07 2012 Sven Lankes <sven@lank.es> 0.14-8
- fix compile with gcc 4.7.0

* Sun Nov 27 2011 Sven Lankes <sven@lank.es> 0.14-7
- Change certificate ui to use plain-text fields to avoid security
    issue with qlabel. rhbz #746877

* Wed Mar 16 2011 Rex Dieter <rdieter@fedoraproject.org> 0.14-6
- fix FTBFS (drop Requires(hint) usage)
- make qca plugin deps arched
- add arched/versioned qt4 runtime dep
- update scriptlets
- drop desktop-file-install --vendor usage (f15+)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Sven Lankes <sven@lank.es> 0.14-4
- Don't crash in chat room configuration dialog (rhbz #668850)

* Thu Apr 08 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.14-3
- disable debug, but don't break the -debuginfo pkg (rhbz#579131)

* Sun Apr 04 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.14-2
- disable debug (rhbz#579131)

* Thu Dec 03 2009 Aurelien Bompard <abompard@fedoraproject.org> -  0.14-1
- 0.14 final
- patch1 merged upstream

* Sun Nov 29 2009 Sven Lankes <sven@lank.es> 0.14-0.2.rc3
- Add (upstream) patch to make enchant spelling-suggestions work
- Remove old patches

* Sun Nov 29 2009 Sven Lankes <sven@lank.es> 0.14-0.1.rc3
- 0.14 rc3

* Mon Nov 09 2009 Aurelien Bompard <abompard@fedoraproject.org> -  0.14-0.1.rc1
- 0.14 rc1

* Tue Jul 28 2009 Aurelien Bompard <abompard@fedoraproject.org> - 0.13-1
- 0.13 final

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-0.3.rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Sven Lankes <sven@lank.es> 0.13-0.2.rc4
- 0.13 rc4

* Mon Jul 13 2009 Sven Lankes <sven@lank.es> 0.13-0.2.rc3
- 0.13 rc3
- remove qt 4.5 patch

* Sun Jul 05 2009 Sven Lankes <sven@lank.es> 0.13-0.2.rc2
- own plugin directories (bz #509683)

* Thu Jul 02 2009 Sven Lankes <sven@lank.es> 0.13-0.1.rc2
- 0.13 rc2

* Sun May 24 2009 Aurelien Bompard <abompard@fedoraproject.org> 0.13-0.1.rc1
- 0.13 rc1

* Sat Mar 28 2009 Sven Lankes <sven@lank.es> 0.12.1-2
- bump Version to avoid newer EVR in F9/F10

* Tue Mar 03 2009 Sven Lankes <sven@lank.es> 0.12.1-1
- Update to 0.12.1 (fix for CVE-2008-6393)
- add patch for qt 4.5 support

* Sun Mar 01 2009 Robert Scheck <robert@fedoraproject.org> 0.12-3
- Added missing build requirement to glib2-devel

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.12-1
- version 0.12

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.11-5
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.11-4
- Autorebuild for GCC 4.3

* Sat Nov 24 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.11-3
- Require qca-gnupg for GnuPG support

* Wed Oct 17 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.11-1
- version 0.11

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.10-5
- rebuild

* Thu Apr 13 2006 Aurelien Bompard <gauret[AT]free.fr> 0.10-4
- update translations for CS, DE, ET and VI

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.10-3
- rebuild for FC5

* Thu Jan 12 2006 Aurelien Bompard <gauret[AT]free.fr> 0.10-1
- version 0.10 final

* Tue Jan 03 2006 Aurelien Bompard <gauret[AT]free.fr> 0.10-0.3.test4
- version 0.10 test4

* Thu Nov 03 2005 Aurelien Bompard <gauret[AT]free.fr> 0.10-0.2.test3
- version 0.10 test3

* Sat Oct 15 2005 Aurelien Bompard <gauret[AT]free.fr> 0.10-0.2.test2
- version 0.10 test2
- drop patch 3 (applied upstream)
- drop icon symlink (useless)

* Thu Aug 25 2005 Aurelien Bompard <gauret[AT]free.fr> 0.10-0.1.test1
- version 0.10 test1
- spec cleanups

* Wed Jun  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.3-4
- patch it for 64-bit/GCC 4

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.9.3-3
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.3-2
- rebuilt

* Sun Jan 09 2005 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.3-1
- version 0.9.3 final

* Mon Jan 03 2005 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.3-0.fdr.0.3.test2
- version 0.9.3-test2

* Thu Nov 25 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.3-0.fdr.0.2.test1
- Drop hardcoded requirement on qca-tls, it should be a plugin

* Mon Nov 22 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.3-0.fdr.0.1.test1
- update to 0.9.3test1
- use the provided icon in the menu and drop Source1.
- add crystal iconset
- added Russian and Eesti translations

* Sat Sep 18 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.2-0.fdr.3
- add patch for typing notification
- add crystal iconset
- update translations (adding kiswahili and Eesti)

* Fri Jun 11 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.2-0.fdr.2
- split qca-tls out of this package and require it
- fix build on FC1

* Thu Jun 10 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.9.2-0.fdr.1
- version 0.9.2
- drop libgnome patch, psi now uses gnome-open
- rediffed the other patches

* Sat Feb 28 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.9
- add a patch to build with mach
- removed URLs in iconsets because the website changed
- add one iconset

* Tue Feb 17 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.8
- add a patch from Debian
- avoid stripping of binary

* Sat Feb 14 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.7
- add German (de) and Simplified Chinese (zh) translations
- Apply suggestions from Michael Schwendt :
  - BuildRequies kdelibs-devel if built --with kde
  - Drop rostericonset "neos" because it is buggy
  - Put docs in %%_datadir/psi to avoid empty about box
  - Fix source URL
  - Fix files list for FC2

* Mon Feb 09 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.6
- add Cesky (cs) and Catalan (ca) translations

* Sat Jan 31 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.5
- add polish (pl) translation.
- improve description of the i18n package

* Wed Jan 28 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.4
- add spanish (es) and svenska (se) translations.
- *really* add GNOME icon...

* Tue Jan 27 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.3
- add slovak (sk) and italian (it) translations.

* Tue Jan 20 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.2
- add GNOME icon

* Sun Jan 11 2004 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9.1-0.fdr.1
- version 0.9.1
- add jisp emoticons in a separate package (psi-icons)
- add ICONSET-HOWTO
- drop old iconsets (and thus remove buildrequires: unzip)
- add rebuild option "--without kde" to prepare for future version of psi
  which will take this into account. Right now it is ignored.

* Sat Nov 22 2003 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9-0.fdr.4
- add Requires: sox to play sound (thanks to you-know-who ;-) )
- fix date in changelog.

* Fri Nov 21 2003 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9-0.fdr.3
- Thanks to Michael Schwendt (again :-) ) :
  * exclude lang files from main package
  * preserve timestamps when possible
  * fix .desktop file
  * add ssl support

* Tue Nov 18 2003 Aurelien Bompard <gauret[AT]free.fr> - 0:0.9-0.fdr.2
- Thanks to Michael Schwendt :
  * group language packs into one subpackage.
  * added epoch=0
  * added environnement variables to ./configure
  * added BuildRequires: XFree86-devel

* Wed Nov 12 2003 Aurelien Bompard <gauret[AT]free.fr> - 0.9-0.fdr.1
- port to Fedora (from Mandrake)
