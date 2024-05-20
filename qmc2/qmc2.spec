%global commit f8b478a8fad5b51a6ed1a0a02da9f5ff470b0042
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240324
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%if %{with snapshot}
%global git_rev v%{version}g%{shortcommit}
%else
%global git_rev 0
%endif

%global pkgname qmc2-mame-fe
%global vc_url https://github.com/qmc2/%{pkgname}

Name:           qmc2
Version:        0.244
Release:        101%{?dist}
Summary:        M.A.M.E. Catalog / Launcher II

#PDF.js is ASL 2.0
#data/js/pdfjs/web/l10n.js is MIT
#everything else is GPLv2
License:        GPL-2.0-only AND Apache-2.0 AND MIT
URL:            http://qmc2.batcom-it.net

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

#Fedora-specific configuration
Patch1:         %{name}-ini.patch

Patch10:        0001-system-minizip-fix.patch
Patch11:        0001-use-system-lzma-sdk.patch

BuildRequires:  make
BuildRequires:  desktop-file-utils
%if %{defined fedora} && 0%{?fedora} >= 40
BuildRequires:  minizip-ng-compat-devel
%else
BuildRequires:  minizip-ng-devel
%endif
BuildRequires:  rsync
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(lzmasdk-c) >= 23.01
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5MultimediaWidgets)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5ScriptTools)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5WebEngineWidgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(xmu)
Provides:       PDF.js = 3f320f0b

%description
A Qt based multi-platform GUI front-end for MAME.


%package -n qchdman
Summary:        Qt CHDMAN GUI
License:        GPLv2
Requires:       mame-tools

%description -n qchdman
A stand-alone graphical user interface / front-end to chdman


%package arcade
Summary:        Arcade QMC2 GUI
License:        GPLv2

%description arcade
A QML-based standalone graphical arcade mode binary which utilizes the cached
data of qmc2 to quickly display and launch emulators and get you "straight into
the games"


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

#ensure system minizip and zlib are used
rm -rf src/minizip
rm -rf src/zlib
rm -rf src/lzma

#fix opening documentation from the menu
sed -i s@doc/html/@doc/@ src/qmc2main.cpp

sed \
  -e 's|egrep|grep -E|g' \
  -i scripts/{generate-option-lists,os-detect,sdl-*}.sh


%build
%set_build_flags
%make_build QMAKE=%{_qt5_qmake} \
  DISTCFG=1 CC_FLAGS="$CFLAGS" CXX_FLAGS="$CXXFLAGS -I%{_includedir}/minizip" \
  L_FLAGS="$LDFLAGS" SYSTEM_MINIZIP=1 SYSTEM_SEVENZIP=1 SYSTEM_ZLIB=1 LIBARCHIVE=1 \
  CTIME=0 GITVERSION=true GIT_REV=%{git_rev}
%make_build arcade QMAKE=%{_qt5_qmake} \
  DISTCFG=1 CC_FLAGS="$CFLAGS" CXX_FLAGS="$CXXFLAGS -I%{_includedir}/minizip" \
  L_FLAGS="$LDFLAGS" SYSTEM_MINIZIP=1 SYSTEM_SEVENZIP=1 SYSTEM_ZLIB=1 LIBARCHIVE=1 \
  CTIME=0 GITVERSION=true GIT_REV=%{git_rev}
%make_build qchdman QMAKE=%{_qt5_qmake} \
  DISTCFG=1 CXX_FLAGS="$CXXFLAGS -I%{_includedir}/minizip" L_FLAGS="$LDFLAGS" \
  CTIME=0 GITVERSION=true GIT_REV=%{git_rev}
%make_build doc QMAKE=%{_qt5_qmake} DISTCFG=1 CTIME=0 GITVERSION=true GIT_REV=%{git_rev}


%install
make install DESTDIR=%{buildroot} QMAKE=%{_qt5_qmake} \
  DISTCFG=1 PREFIX=%{_prefix} \
  QT_TRANSLATION=../../qt5/translations

make arcade-install DESTDIR=%{buildroot} \
  QMAKE=%{_qt5_qmake} DISTCFG=1 PREFIX=%{_prefix} \
  QT_TRANSLATION=../../qt5/translations

make qchdman-install DESTDIR=%{buildroot} \
  QMAKE=%{_qt5_qmake} DISTCFG=1 PREFIX=%{_prefix} \
  QT_TRANSLATION=../../qt5/translations

make doc-install DESTDIR=%{buildroot} QMAKE=%{_qt5_qmake} DISTCFG=1 MAN_DIR=%{_mandir}

#remove docs since we are installing docs in %%doc
rm -rf %{buildroot}%{_datadir}/%{name}/doc
ln -sf "$(realpath -m --relative-to="%{_datadir}/%{name}" "%{_docdir}/%{name}")" \
  %{buildroot}%{_datadir}/%{name}/doc

#validate the desktop files
desktop-file-validate %{buildroot}%{_datadir}/applications/qmc2-sdlmame.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/qmc2-arcade.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/qchdman.desktop


%files
%doc data/doc/html/*
%license data/doc/html/us/copying.html data/js/pdfjs/LICENSE
%config(noreplace) %{_sysconfdir}/qmc2
%{_bindir}/qmc2
%{_bindir}/qmc2-sdlmame
%{_datadir}/applications/qmc2-sdlmame.desktop
%{_mandir}/man6/qmc2-main-gui.6*
%{_mandir}/man6/qmc2-sdlmame.6*
%{_mandir}/man6/qmc2.6*
%{_datadir}/qmc2

%files arcade
%license data/doc/html/us/copying.html
%{_bindir}/qmc2-arcade
%{_datadir}/applications/qmc2-arcade.desktop
%{_mandir}/man6/qmc2-arcade.6*

%files -n qchdman
%license data/doc/html/us/copying.html
%{_bindir}/qchdman
%{_datadir}/applications/qchdman.desktop
%{_mandir}/man6/qchdman.6*


%changelog
* Sun May 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.244-101.20240324gitf8b478a
- lzma-sdk rebuild

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.244-100.20230324gitf8b478a
- 0.244 snapshot

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.243-101
- lzma-sdk rebuild

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0.243-100
- 0.243
- System lzma-sdk

* Sun Apr 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0.242-100
- 0.242

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 0.195-101
- Fedora sync
- Fix qt 5.15 build

* Tue Oct 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.195-100
- Qt5
- Remove game-menus requirements

* Thu Sep 05 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.195-9
- Fix qmake detection on rawhide

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.195-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.195-7
- Fix qmake detection on rawhide

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.195-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.195-5
- Add patch migrating to the new minizip package

* Fri Sep 07 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.195-4
- Fixed qmake detection on rawhide

* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 0.195-3
- change requires to minizip-compat(-devel), rhbz#1609830, rhbz#1615381

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.195-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 09 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.195-1
- Updated to 0.195

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.192-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 02 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.192-1
- Updated to 0.192

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.187-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.187-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.187-1
- Updated to 0.187

* Sun Jun 18 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.186-1
- Updated to 0.186
- Updated the -ini patch

* Wed Feb 22 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.183-1
- Updated to 0.183
- Updated the -ini patch

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.71-1
- Updated to 0.71
- Bundled lzma-sdk is now at 16.04
- PDF.js is now at 76b4c8fa

* Thu Dec 01 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.70-1
- Updated to 0.70

* Fri Oct 28 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.69-1
- Updated to 0.69

* Fri Sep 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.68-1
- Updated to 0.68
- Updated description as per upstream suggestions
- Added libarchive support

* Sat Sep 03 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.67-1
- Updated to 0.67

* Wed Jul 27 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.66-1
- Updated to 0.66
- Dropped included patches

* Wed Jul 13 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.65-4
- Fixed warning in generated man pages
- Updated %%description spelling to front-end to silence rpmlint

* Tue Jul 12 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.65-3
- Patched to use system-wide minizip and zlib
- Added comments clarifying patches' purpuse
- Corrected the License tags
- Fixed online documentation symlink
- Added qmc2-arcade

* Fri Jul 08 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.65-2
- Fixed old changelog entries
- Tagged copying.html as %%license
- Modernised the SPEC file
- Dropped ancient Provides/Obsoletes
- Worked around lack of F25 config
- Ensured $RPM_OPT_FLAGS and $RPM_LD_FLAGS are used
- Applied some build fixes from upstream svn

* Sun Jul 03 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.65-1
- Updated to 0.65

* Wed Apr 27 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.63-1
- Updated to 0.63

* Thu Apr 07 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.62-1
- Updated to 0.62
- Updated the -ini patch

* Sat Mar 12 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.61-1
- Updated to 0.61

* Thu Jan 28 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.60-1
- Updated to 0.60

* Thu Dec 31 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.59-1
- Updated to 0.59
- Switched to SDL2

* Fri Nov 27 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.58-1
- Updated to 0.58
- Updated the URL

* Fri Oct 30 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.57-1
- Updated to 0.57
- Dropped the dat files from ini patch now that mame-data-extras is retired

* Thu Oct 01 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.56-1
- Updated to 0.56

* Sat Aug 29 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.55-1
- Updated to 0.55

* Thu Jul 30 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.54-1
- Updated to 0.54
- Dropped upstreamed patch
- Updated the -ini patch

* Tue Jul 07 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.53-1
- Updated to 0.53
- Dropped -sdlmess subpackage
- Added man pages
- Cleaned up the spec file slightly
- Updated the default configuration

* Tue Mar 31 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.50-1
- Updated to 0.50
- Switched to use history.dat instead of sysinfo.dat by default

* Thu Feb 26 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.49-1
- Updated to 0.49

* Sun Feb 01 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.48-1
- Updated to 0.48

* Sat Jan 03 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.47-1
- Updated to 0.47

* Sat Nov 29 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.46-1
- Updated to 0.46

* Sat Oct 18 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.45-1
- Updated to 0.45

* Sun Aug 03 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.44-1
- Updated to 0.44

* Sat Apr 26 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.43-1
- Updated to 0.43
- Updated the ini patch to use category.ini supplied with qmc2 by default
- Added bundled(lzma-sdk) = 9.22 to Provides

* Thu Jan 09 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.42-1
- Updated to 0.42

* Sun Nov 10 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.41-1
- Updated to 0.41

* Thu Sep 19 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.40-1
- Updated to 0.40
- cheat_file → cheatpath

* Mon Jun 17 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.39-1
- Updated to 0.39
- Added qchdman
- Fixed Source0 URL

* Sat Jan 12 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.38-1
- Updated to 0.38
- Updated the ini patch

* Fri Sep 21 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.37-1
- Updated to 0.37
- Updated the ini patch
- SDLMAME/SDLMESS have been gone for a while, so just use them internally
- Require mame/mess since the compatibility provides were dropped
- Updated summaries

* Tue May 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.36-1
- Updated to 0.36

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.35-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 06 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.35-1
- Updated to 0.35
- Updated the ini patch
- Made the inter-subpackage dependencies arch-specific

* Tue Nov 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.34-1
- Updated to 0.34 (new versioning scheme)
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Wed Jun 29 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.24.b20
- Updated to 0.2b20
- Updated the ini patch

* Sun Apr 03 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.23.b19
- Updated to 0.2b19

* Thu Jan 13 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.22.b18
- Updated to 0.2b18

* Fri Oct 22 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.21.b17
- Updated to 0.2b17
- Added Fedora 15 config

* Fri Jul 30 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.20.b16
- Updated to 0.2b16

* Sun May 16 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.19.b15
- Updated to 0.2b15
- Updated the ini template patch to include Catver.ini
- s/qt4-devel/qt-webkit-devel due to changes in qt package

* Mon Mar 15 2010 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.18.b14
- Updated to 0.2b14
- Dropped --fno-var-tracking-assignments

* Sat Jan 02 2010 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.17.b13
- Updated to 0.2b13
- Dropped the cflags patch
- Dropped the additional Fedora configs

* Sat Nov 21 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.16.b12
- Updated to 0.2b12
- Worked around RH bug 532763 for Fedora 12 and above
- Added Fedora 12 and Fedora 13 configs

* Fri Sep 11 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.15.b11
- Updated to 0.2b11
- Updated the ini patch
- Dropped F12 rawhide workaround

* Mon Jul 20 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.14.b10
- Updated to 0.2b10
- Added F12 rawhide config

* Mon Jun 08 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.13.b9
- Updated to 0.2b9

* Thu Apr 23 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.12.b8
- Updated to 0.2b8
- Updated the ini patch
- Dropped the upstreamed gcc44 patch
- Dropped the F11 Beta workaround

* Mon Mar 30 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.11.b7
- Handle the template properly
- Updated the configs for Fedora 11 Beta

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2-0.10.b7
- rebuild for new F11 features

* Mon Mar 09 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.9.b7
- Updated to 0.2b7
- Dropped the rawhide fedora-release workaround
- Overhauled for sdlmess support
- Desktop files now come with the tarball and use the shipped icon
- Updated Summary and %%description (M.A.M.E. → M.A.M.E./M.E.S.S.)
- Updated the ini patch
- Avoid installing qmc2.ini.new
- Dropped hicolor-icon-theme from Requires
- Switched to system-wide Qt translations
- No longer force Windows Qt style
- Updated the URL
- Added libXmu-devel to BuildRequires
- Added gcc-4.4 fix from SVN

* Mon Jan  5 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.8.b6
- Updated to 0.2b6
- Updated the ini patch
- Updated the rawhide fedora-relase workaround
- Added PRETTY=0 to compilation flags

* Thu Oct 16 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.7.b5
- Updated to 0.2b5

* Tue Aug 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.6.b4
- Added phonon-devel to BuildRequires
- Cleaned up BuildRequires and Requires

* Tue Aug 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.5.b4
- Updated to 0.2b4

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.2-0.4.b3
- rebuild for buildsys cflags issue

* Mon Jul  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.3.b3
- Updated to 0.2b3
- Dropped the qt4 patch, use DISTCFG instead
- Updated the ini patch to include dat files location
- Added SDL-devel to BuildRequires

* Sat May 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.2.b2
- Updated to 0.2b2
- Dropped %%{?dist} from %%changelog
- Added hyphen before version number in %%changelog

* Wed Mar 26 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.1.b1
- Updated to 0.2b1
- Dropped the ini fix since it has been merged upstream

* Sat Feb 23 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-4
- Updated the inipaths to reflect the post-0.123u1 SDLMAME configuration

* Sat Feb 23 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-3
- Replaced the previous workaround with a proper fix from upstream

* Mon Feb 11 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-2
- Updated the ini path to fix import/export feature

* Wed Feb  6 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-1
- Upstream sync

* Thu Jan 31 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-0.10.b11
- Upstream sync
- Drop backup files deletion, there are none present
- Adjusted the License tag
- Fixed the executable permissions

* Mon Jul 30 2007 XulChris <tkmame@retrogames.com> - 0.1-0.9.b10
- Upstream sync
- Remove no longer needed qt43 patch

* Mon Jul 02 2007 XulChris <tkmame@retrogames.com> - 0.1-0.8.b9
- Add patch to fix Qt-4.3 segmentation fault

* Sun Apr 22 2007 XulChris <tkmame@retrogames.com> - 0.1-0.7.b9
- Remove style from desktop file and add it to ini file instead
- Dribble Bugzilla #89

* Fri Mar 30 2007 XulChris <tkmame@retrogames.com> - 0.1-0.6.b9
- Upstream sync
- Remove no longer needed datadir patch

* Sun Mar 11 2007 XulChris <tkmame@retrogames.com> - 0.1-0.5.b8
- Update desktop category
- Include new paths in ini file
- Add patch to fix DATADIR parsing in Makefile

* Fri Feb 23 2007 XulChris <tkmame@retrogames.com> - 0.1-0.4.b8
- Upstream sync
- Update Source0 URL
- Remove patches which are now included in upstream
- Move creation of desktop file to %%prep
- Sync ini patch with new ini template

* Wed Jan 31 2007 XulChris <tkmame@retrogames.com> - 0.1-0.3.b7
- Fix ini patch

* Wed Jan 17 2007 XulChris <tkmame@retrogames.com> - 0.1-0.2.b7
- Make opengl default video mode
- Remove macros from Patch tags
- Move creation of .desktop file into %%build
- Fix Categories field in .desktop file
- Remove Version field from .desktop file
- Fix documentation

* Sun Dec 24 2006 XulChris <tkmame@retrogames.com> - 0.1-0.1.b7
- Initial Release
