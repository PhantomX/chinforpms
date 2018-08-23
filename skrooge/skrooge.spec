Name:    skrooge
Summary: Personal finances manager
Version: 2.15.0
Release: 100.chinfo%{?dist}

License: GPLv2+
URL:     http://skrooge.org
Source0: http://download.kde.org/stable/skrooge/skrooge-%{version}.tar.xz

## upstream patches

BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: grantlee-qt5-devel
BuildRequires: kf5-kactivities-devel
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kcompletion-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdelibs4support-devel
BuildRequires: kf5-kdesignerplugin-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifyconfig-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-krunner-devel
BuildRequires: kf5-kwallet-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-rpm-macros
BuildRequires: cmake(KF5DesignerPlugin)
BuildRequires: libappstream-glib
BuildRequires: pkgconfig(qca2-qt5)
BuildRequires: pkgconfig(libofx)
BuildRequires: pkgconfig(Qt5Designer)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5WebKitWidgets)
# I think due to custom sqlcipher plugin -- rex
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(sqlcipher)


Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: qca-qt5-ossl%{?_isa}

# drop prior needless -devel pkg
Obsoletes: skrooge-devel < 2.0.0

%description
%{name} is a personal finances manager,
aiming at being simple and intuitive.
It allows you to keep track of your expenses and incomes,
categorize them, and build reports of them.

%package libs
Summary: Runtime libraries for %{name}
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.


%prep
%autosetup -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. \
  -DCMAKE_BUILD_TYPE:STRING="Release"
popd

%make_build -C %{_target_platform}


%install
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}

%find_lang %{name} --with-html

## unpackaged files
rm -fv %{buildroot}%{_kf5_libdir}/lib*.so


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf5_metainfodir}/org.kde.skrooge.appdata.xml
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.skrooge.desktop


%files -f %{name}.lang
%doc AUTHORS CHANGELOG README
%license COPYING
%{_kf5_sysconfdir}/xdg/skrooge_monthly.knsrc
%{_kf5_sysconfdir}/xdg/skrooge_unit.knsrc
%{_kf5_bindir}/skrooge*
%{_kf5_metainfodir}/org.kde.skrooge.appdata.xml
%{_kf5_datadir}/applications/org.kde.skrooge.desktop
%{_kf5_datadir}/skrooge/
%{_kf5_datadir}/mime/packages/x-skg.xml
%{_kf5_datadir}/icons/breeze/*/*/*
%{_kf5_datadir}/icons/breeze-dark/*/*/*
%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/config.kcfg/skg*.kcfg
%{_kf5_datadir}/knotifications5/skrooge.notifyrc
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/kxmlgui5/skg*/
%{_kf5_datadir}/kxmlgui5/skrooge_*/

%files libs
%{_kf5_qtplugindir}/skg*.so
%{_kf5_qtplugindir}/skrooge*.so
%{_kf5_qtplugindir}/grantlee/*/grantlee_skgfilters.so
%{_kf5_qtplugindir}/sqldrivers/libskgsqlcipher.so
%{_kf5_qtplugindir}/designer/libskgbankgui*.so*
%{_kf5_qtplugindir}/designer/libskgbasegui*.so*
%{_kf5_libdir}/libskgbankgui.so.2*
%{_kf5_libdir}/libskgbankmodeler.so.2*
%{_kf5_libdir}/libskgbasegui.so.2*
%{_kf5_libdir}/libskgbasemodeler.so.2*


%changelog
* Wed Aug 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.15.0-100.chinfo
- 2.15.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.14.0-1
- skrooge-2.14.0 (#1594790)

* Thu Jun 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.13.0-3
- rebuild (qt5)

* Mon May 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.13.0-2
- rebuild (qt5)

* Tue May 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.13.0-1
- skrooge-2.13.0 (#1575967)

* Mon Apr 02 2018 Bill Nottingham <notting@splat.cc> - 2.12.0-2
- rebuild for libofx soname change

* Thu Mar 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.12.0-1
- 2.12.0 (#1553733)

* Mon Mar 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.11.0-3
- BR: gcc-c++, use %%make_build, %%check: stricter appdata check

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 2.11.0-2
- rebuild (qt5)

* Thu Feb 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.11.0-1
- 2.11.0 (#1541683)
- use %%ldconfig_scriptlets

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.10.5-4
- Remove obsolete scriptlets

* Mon Jan 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.5-3
- rebuild (qt5)

* Mon Nov 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10.5-2
- rebuild (qt5)

* Thu Nov 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10.5-1
- 2.10.5

* Mon Nov 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10.3-1
- 2.10.3

* Wed Oct 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.8.1-2
- BR: qt5-qtbase-private-devel

* Wed Aug 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.8.1-1
- update to latest release (#1365514)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.4.0-2
- add macro to support sqlcipher (disabled, ftbfs against qt 5.7.x)

* Wed Jul 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.4.0-1
- skrooge-2.4.0 (#1310483)

* Thu Feb 11 2016 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-2
- pull in some upstream fixes (kde#358315)

* Thu Feb 11 2016 Rex Dieter <rdieter@fedoraproject.org>  2.2.0-1
- skrooge-2.2.0, kf5-based

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 01 2016 Rex Dieter <rdieter@fedoraproject.org> 1.12.5-4
- drop versioned qt/kdelibs/kde-runtime deps

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> 1.12.5-3
- reset Release: tag

* Sun Jul 26 2015 maverick <siddharth.kde@gmail.com> - 1.12.5-2.1
- New Package upstream stable 1.12.5
- Fix Date in Chanelog, wrong date "Sun Nov 30"

* Sat Jul 25 2015 maverick <siddharth.kde@gmail.com> - 1.11.0-3.1
- Move qca2 to qca, as qca deprecates qca2
- Add qca-ossl as requires, to avaoid errors when saving files which are password protected

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Siddharth Sharma <siddharth.kde@gmail.com> - 1.11.0-1.1
- New Package upstream stable 1.11.0

* Fri Jan 23 2015 maverick <siddharth.kde@gmail.com> - 1.10.92-1.1
- New Package Upstream unstable 10.0.92

* Sun Nov 02 2014 Siddharth Sharma <siddharth.kde@gmail.com> - 1.10.0-1.1
- New Package Upstream 1.10.0 for bz#1116637

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Rex Dieter <rdieter@fedoraproject.org> 1.9.0-3
- optimize mimeinfo scriptlet
- BR: qtwebkit ...

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Siddharth Sharma <siddharth.kde@gmail.com> - 1.9.0-1
- New Package Upstream 1.9.0

* Tue Jan 07 2014 siddharth <siddharth.kde@gmail.com> - 1.8.0-1
- new upstream release 1.8.0

* Mon Sep 23 2013 Bill Nottingham <notting@redhat.com> - 1.7.1-4
- rebuild against new libofx

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 siddharth sharma <siddharths@fedoraproject.org> - 1.7.1-2
- Added kde-runtime as required for bz#984317

* Mon Jul 1 2013 siddharth Sharma <siddharths@fedoraproject.org> - 1.7.1-1
- new upstream release 1.7.1

* Sat Mar 16 2013 siddharth Sharma <siddharths@fedoraproject.org> - 1.6.0-2
- Fixing Compiling Error because of missing build requires

* Sat Mar 16 2013 Siddharth Sharma <siddharths@fedoraproject.org> - 1.6.0-1
- new upstream release
- Fix Packaging error for skrooge related akonadi resources

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 08 2012 Sven Lankes <sven@lank.es> - 1.3.3-1
- new upstream release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Bill Nottingham <notting@redhat.com> 1.3.0-2
- rebuild for libofx ABI bump

* Thu Apr 26 2012 Sven Lankes <sven@lank.es> 1.3.0-1
- skrooge 1.3.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Sven Lankes <sven@lank.es> 1.1.1-1
- skrooge 1.1.1

* Fri Aug 19 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-1
- 0.9.1
- -libs: track abi/sonames
- .spec cosmetics, remove deprecated items

* Wed Jun 08 2011 Sven Lankes <sven@lank.es> 0.9.0-1
- skrooge 0.9.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.8.0-1
- skrooge 0.8.0

* Tue Sep 07 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.7.3-1
- skrooge 0.7.3

* Sun Aug 08 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.7.2-1
- skrooge 0.7.2

* Mon May 17 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.7.1-1
- skrooge 0.7.1 bugfix release

* Mon Apr 26 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.7.0-1
- Skrooge 0.7.0

* Wed Feb 10 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.6.0-1
- New upstream source 0.6.0

* Thu Jan 28 2010 Rex Dieter <rdieter@fedoraproject.org> 0.5.5-2
- use %%{_kde4_version}, don't rely on kde4-config --version parsing

* Sun Dec 27 2009 Thomas Janssen <thomasj@fedoraproject.org> 0.5.5-1
- Update to new upstream release
- Corrects a lot of bugs and problems. See the CHANGELOG for details.

* Mon Nov 30 2009 Thomas Janssen <thomasj@fedoraproject.org> 0.5.4-1
- Update to new upstream version
- Corrects a lot of bugs and problems. See the changelog for details.

* Sun Nov 01 2009 Thomas Janssen <thomasj@fedoraproject.org> 0.5.3-1
- Updated to new upstream version
- Readded a -DCMAKE workaround (please keep it for now)
- Useing chmod -x to prevent spurious-executable-perm. Bug filed.

* Wed Oct 14 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.2-2
- (HTML) docs patch, use %%find_lang --with-kde
- own %%{_kde4_appsdir}/skrooge*/ dirs
- %%check: omit extraneous desktop-file-validate's

* Thu Oct 08 2009 Thomas Janssen <thomasj@fedoraproject.org> 0.5.2-1
- Changed to final 0.5.2 version
- Bugfixes, including a nasty bug where one thinks the data is gone
- added HTML documentation
- added localizations

* Tue Sep 22 2009 Thomas Janssen <thomasj@fedoraproject.org> 0.5.2-0.1.beta
- Changed to new upstream Version 0.5.2_beta (lots of bugfixes)

* Mon Sep 21 2009 Thomas Janssen <thomasj@fedoraproject.org> 0.5.1-0.5.beta
- Added -libs Requires libofx

* Mon Sep 21 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-0.4.beta
- misc cosmetics
- mime scriptlets
- move icons to hicolor
- -libs: drop dup'd docs, add min kdelibs4 dep

* Thu Sep 17 2009 Thomas Janssen <thomasj@fedoraproject.org>  0.5.1-0.3.beta
- Spec file corrections and Version correction

* Wed Sep 16 2009 Thomas Janssen <thomasj@fedoraproject.org>  0.5.1-beta2
- cleaned up desktop files

* Tue Sep 15 2009 Thomas Janssen <thomasj@fedoraproject.org>  0.5.1-beta1
- changed version to 0.5.1 beta with fixed rpmlint output

* Sun Sep 13 2009 Thomas Janssen <thomasj@fedoraproject.org>  0.5.0-2
- Fixed the spec and rpmlintoutput debuginfo-without-source

* Fri Sep 11 2009 Thomas Janssen <thomasj@fedoraproject.org>  0.5.0-1
- Initial Release 0.5.0
