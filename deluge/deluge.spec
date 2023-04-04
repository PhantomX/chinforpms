%global commit 5f6f65a06500e12f378e7918289e1d82954c1bd6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211123
%bcond_with snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vermm %%(echo %{version} | cut -d. -f-2)

Name:           deluge
Version:        2.1.1
Release:        100%{?dist}
Summary:        A GTK+ BitTorrent client with support for DHT, UPnP, and PEX

Epoch:          1

License:        GPLv3 with exceptions
URL:            http://deluge-torrent.org/

%if %{with snapshot}
Source0:        https://git.deluge-torrent.org/deluge/snapshot/deluge-%{commit}.tar.bz2#/deluge-%{shortcommit}.tar.bz2
%else
Source0:        http://download.deluge-torrent.org/source/%{vermm}/%{name}-%{version}.tar.xz
%endif
Source1:        %{name}-daemon-sysusers.conf

Patch0:         0001-Disable-GConf2-magnet-registering.patch
Patch1:         0001-Disable-new-release-check-by-default.patch

%global vc_url  https://git.deluge-torrent.org/deluge/patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  intltool
BuildRequires:  %{py3_dist libtorrent}
BuildRequires:  %{py3_dist wheel}
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

## add Requires to make into Meta package
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-gtk = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-images = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-console = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-web = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-daemon = %{?epoch:%{epoch}:}%{version}-%{release}


%description
Deluge is a new BitTorrent client, created using Python and GTK+. It is
intended to bring a native, full-featured client to Linux GTK+ desktop
environments such as GNOME and XFCE. It supports features such as DHT
(Distributed Hash Tables), PEX (µTorrent-compatible Peer Exchange), and UPnP
(Universal Plug-n-Play) that allow one to more easily share BitTorrent data
even from behind a router with virtually zero configuration of port-forwarding.

%package common
Summary:        Files common to Deluge sub packages
License:        GPLv3 with exceptions
Requires:       %{py3_dist pyopenssl}
Requires:       %{py3_dist chardet}
Requires:       %{py3_dist dbus-python}
Requires:       %{py3_dist pillow}
Requires:       %{py3_dist pygame}
Requires:       %{py3_dist pyxdg}
# FIXME: this must be in Fedora python3-twisted Requires, remove when it is fixed
Requires:       %{py3_dist service-identity}
Requires:       %{py3_dist setproctitle}
Requires:       %{py3_dist six}
Requires:       %{py3_dist twisted}
Requires:       %{py3_dist rencode}
Requires:       %{py3_dist zope-interface}
Requires:       %{py3_dist libtorrent}
Requires:       xdg-utils


%description common
Common files needed by the Deluge bittorrent client sub packages

%package gtk
Summary:        The gtk UI to Deluge
License:        GPLv3 with exceptions
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-images = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-daemon = %{?epoch:%{epoch}:}%{version}-%{release}
## Required for the proper ownership of icon dirs.
Requires:       hicolor-icon-theme
Requires:       gtk3
Requires:       %{py3_dist pycairo}
Requires:       %{py3_dist pygobject}
Requires:       python3-gobject
Requires:       %{py3_dist geoip}

%description gtk
Deluge bittorent client GTK graphical user interface

%package images
Summary:       Image files for deluge
License:       GPLv3 with exceptions
%description images
Data files used by the GTK and web user interface for Deluge bittorent client

%package console
Summary:       CLI to Deluge
License:       GPLv3 with exceptions
Requires:      %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      %{name}-daemon = %{?epoch:%{epoch}:}%{version}-%{release}
%description console
Deluge bittorent client command line interface

%package web
Summary:       Web interface to Deluge
License:       GPLv3 with exceptions
Requires:      python3-mako
Requires:      %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      %{name}-images = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      %{name}-daemon = %{?epoch:%{epoch}:}%{version}-%{release}

%description web
Deluge bittorent client web interface

%package daemon
Summary:       The Deluge daemon
License:       GPLv3 with exceptions
Requires:      %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
BuildRequires: systemd

%description daemon
Files for the Deluge daemon

%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

%{?with_snapshot:echo "%{version}" > RELEASE-VERSION}

find -name '*~' -delete

sed -e "s|'closure-compiler', 'closure'|'closure_disabled'|g" -i minify_web_js.py


%build
%py3_build

%install
%py3_install

mkdir -p %{buildroot}%{_unitdir}/%{name}-{daemon,web}.service.d
install -m644 packaging/systemd/deluged.service %{buildroot}%{_unitdir}/%{name}-daemon.service
install -m644 packaging/systemd/deluge-web.service %{buildroot}%{_unitdir}/%{name}-web.service
install -m644 packaging/systemd/user.conf %{buildroot}%{_unitdir}/%{name}-daemon.service.d/
install -m644 packaging/systemd/user.conf %{buildroot}%{_unitdir}/%{name}-web.service.d/

install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}-daemon.conf

mkdir -p %{buildroot}%{_userunitdir}
install -m644 packaging/systemd/user/deluged.service %{buildroot}%{_userunitdir}/%{name}-daemon.service
install -m644 packaging/systemd/user/deluge-web.service %{buildroot}%{_userunitdir}/%{name}-web.service

mkdir -p %{buildroot}/var/lib/%{name}

## NOTE: The lang files should REEEAALLLY be in a standard place such as
##       /usr/share/locale or similar. It'd make things so much nicer for
##       the packaging. :O
## A bit of sed magic to mark the translation files with %%lang, taken from
## find-lang.sh (part of the rpm-build package) and tweaked somewhat. We
## cannot (unfortunately) call find-lang directly since it's not on a
## "$PREFIX/share/locale/"-ish directory tree.

pushd %{buildroot}
    find -type f -o -type l \
        | sed '
            s:%{buildroot}%{python3_sitelib}::
            s:^\.::
            s:\(.*/deluge/i18n/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:
            s:^\([^%].*\)::
            s:%lang(C) ::
            /^$/d' \
    > %{name}.lang

## Now we move that list back to our sources, so that '%%files -f' can find it
## properly.
popd && mv %{buildroot}/%{name}.lang .

mv %{buildroot}%{_datadir}/appdata %{buildroot}%{_metainfodir}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%files

%files common -f %{name}.lang
%doc CHANGELOG.md LICENSE README.md

%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info/
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/*.py*
%{python3_sitelib}/%{name}/__pycache__/
%{python3_sitelib}/%{name}/plugins
%{python3_sitelib}/%{name}/core
%dir %{python3_sitelib}/%{name}/ui
%{python3_sitelib}/%{name}/ui/*.py*
%{python3_sitelib}/%{name}/ui/__pycache__/
# includes %%name.pot too
%dir %{python3_sitelib}/%{name}/i18n
%dir %{python3_sitelib}/%{name}/i18n/*
%dir %{python3_sitelib}/%{name}/i18n/*/LC_MESSAGES
%{python3_sitelib}/%{name}/i18n/__pycache__/*
%{python3_sitelib}/%{name}/i18n/*.py


%files images
# only pixmaps dir is in data so I own it all
%{python3_sitelib}/%{name}/ui/data
# if someone decides to only install images
%dir %{python3_sitelib}/%{name}

%files gtk
%{_bindir}/%{name}
%{_bindir}/%{name}-gtk
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/*/apps/%{name}-panel.*
%{_datadir}/pixmaps/%{name}.*
%{python3_sitelib}/%{name}/ui/gtk3
%{_mandir}/man?/%{name}-gtk*
%{_mandir}/man?/%{name}.1*
%{_metainfodir}/%{name}.appdata.xml

%files console
%{_bindir}/%{name}-console
%{python3_sitelib}/%{name}/ui/console
%{_mandir}/man?/%{name}-console*

%files web
%{_bindir}/%{name}-web
%{python3_sitelib}/%{name}/ui/web
%{_mandir}/man?/%{name}-web*
%{_unitdir}/%{name}-web.service
%dir %{_unitdir}/%{name}-web.service.d
%{_unitdir}/%{name}-web.service.d/user.conf
%{_userunitdir}/%{name}-web.service

%files daemon
%{_bindir}/%{name}d
%{_sysusersdir}/%{name}-daemon.conf
%{_unitdir}/%{name}-daemon.service
%dir %{_unitdir}/%{name}-daemon.service.d
%{_unitdir}/%{name}-daemon.service.d/user.conf
%{_userunitdir}/%{name}-daemon.service
%attr(-,%{name}, %{name})/var/lib/%{name}/
%{_mandir}/man?/%{name}d*

%pre daemon
%sysusers_create_compat %{SOURCE1}

%post daemon
%systemd_post deluge-daemon.service

%post web
%systemd_post deluge-web.service

%preun daemon
%systemd_preun deluge-daemon.service

%preun web
%systemd_preun deluge-web.service

%postun daemon
%systemd_postun_with_restart deluge-daemon.service

%postun web
%systemd_postun_with_restart deluge-web.service


%changelog
* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.1-100
- 2.1.1

* Wed Jun 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.0-100
- 2.1.0

* Thu Dec 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.5-100
- 2.0.5

* Mon Dec 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.4-100
- 2.0.4

* Wed Nov 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-116.20211123git5f6f65a
- Last snapshot

* Mon Oct 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-115.20211003gitd566364
- Update

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-114.20210921git1e6cc03
- Bump

* Mon Sep 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-113.20210829git588f600
- Update

* Sun Aug 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-112.20210731git5c9378a
- Last snapshot

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-111.20210417git2e46610
- Bump

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-110.20210220git4d97075
- BR: python3-wheel

* Mon Feb 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-109.20210220git4d97075
- Update

* Tue Jan 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-108.20200430git23a48dd
- Fix python BRs
- Rawhide sync

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.0.3-107.20200430git23a48dd
- Remove closure-compiler BR

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.3-106.20200430git23a48dd
- New snapshot

* Sat Apr 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.3-105.20200425git62d8749
- Bump

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.3-104.20191128git2f1c008
- Arch fix for ngettext with python 3.8

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.3-103.20191128git2f1c008
- New snapshot
- sysusersdir support

* Thu Nov 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.3-102.20191115git5f1eada
- Snapshot

* Mon Aug 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.3-101
- Some upstream fixes

* Wed Jun 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.3-100
- 2.0.3

* Sat Jun 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.2-100
- 2.0.2
- Requirements updated for python3, gtk3
- Upstream systemd files

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 21 2018 Michael Cronenworth <mike@cchtml.com> - 1.3.15-10
- Update python dependencies for F28+ only

* Tue Mar 20 2018 Michael Cronenworth <mike@cchtml.com> - 1.3.15-9
- Update python dependencies for F28+ only

* Tue Mar 20 2018 Michael Cronenworth <mike@cchtml.com> - 1.3.15-8
- Update python dependencies for F28+ only

* Mon Mar 19 2018 Michael Cronenworth <mike@cchtml.com> - 1.3.15-7
- Fix GTK UI bug (rhbz#1558110)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.15-5
- Remove obsolete scriptlets

* Thu Jan 04 2018 Michael Cronenworth <mike@cchtml.com> - 1.3.15-4
- Update Python dependency names for new packaging standards

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Michael Cronenworth <mike@cchtml.com> - 1.3.15-2
- Fix preferences dialog

* Fri May 12 2017 Michael Cronenworth <mike@cchtml.com> - 1.3.15-1
- Update to 1.3.15

* Mon Mar 06 2017 Michael Cronenworth <mike@cchtml.com> - 1.3.14-1
- Update to 1.3.14

* Wed Feb 15 2017 Jon Ciesla <limburgher@gmail.com> - 1.3.13-4
- Fix python macros.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Michael Cronenworth <mike@cchtml.com> - 1.3.13-2
- Remove dependency on gtk for web subpackage (rhbz#1365920)

* Wed Jul 20 2016 Michael Cronenworth <mike@cchtml.com> - 1.3.13-1
- update to 1.3.13

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 11 2016 Michael Cronenworth <mike@cchtml.com> - 1.3.12-3
- Fix GTK UI bugs (rhbz#1219582 and rhbz#1223058)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 14 2015 Michael Cronenworth <mike@cchtml.com> - 1.3.12-1
- update to 1.3.12

* Fri Aug 21 2015 Michael Cronenworth <mike@cchtml.com> - 1.3.11-5
- Fix crash for non-C locales on creating torrents (rhbz#1224261)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Michael Cronenworth <mike@cchtml.com> - 1.3.11-3
- Fix unbundling attempt of rencode (rhbz#953700)

* Tue May 19 2015 Michael Cronenworth <mike@cchtml.com> - 1.3.11-2
- fix compatibility with Twisted 15 (rhbz#1221985)

* Thu Dec 18 2014 Tom Callaway <spot@fedoraproject.org> - 1.3.11-1
- update to 1.3.11

* Thu Oct 16 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.10-1
- update to 1.3.10

* Mon Oct 06 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.9-1
- upstream release 1.3.9
- http://dev.deluge-torrent.org/wiki/ReleaseNotes/1.3.9
- switch to bz2
- remove empty file
- drop old obsoletes and provides
- drop old sysv transitional changes
- switch from using systemd-units to systemd

* Sun Jul 13 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.7-1
- update to 1.3.7
- drop upstream patch to fix icon location

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.6-3
- add dependency on newly introduced python-rencode
- remove bundled copy.  resolves rhbz#953700
- add references to upstream tickets on systemd, rencode and svg icon location

* Thu May 09 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.6-2
- drop dependency on gnome-python2-gnome. resolves rhbz#961541
- drop dependency on python-simplejson
- add dependency on pygame, python-GeoIP and python-setproctitle
- fix old bogus date in changelog

* Mon Feb 25 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.6-1
- upstream release 1.3.6
- http://dev.deluge-torrent.org/wiki/ReleaseNotes/1.3.6

* Mon Feb 18 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.5-4
- Remove --vendor from desktop-file-install https://fedorahosted.org/fesco/ticket/1077

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Jon Ciesla <limburgher@gmail.com> - 1.3.5-1
- Latest upstream.
- Added rb_libtorrent-python BuildRequires to ensure use of system libtorrent.
- Migrate to systemd, BZ 790182.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.3-1
- New upstream release
- http://dev.deluge-torrent.org/wiki/ReleaseNotes/1.3.3
- Drop defattr
- Add build requires on intltool

* Mon May 30 2011 Justin Noah <justinnoah@gmail.com> - 1.3.2-1
- Update to latest upstream release
- http://dev.deluge-torrent.org/wiki/ReleaseNotes/1.3.2
- Dropped unnecessary patch concerning deluge.desktop categories
- Remove hidden files created by webui build and compression

* Mon Mar 28 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.1-5
- Add init script for the deluge daemon. Resolves rhbz#537387
- Rewrite package descriptions to be better

* Fri Feb 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.3.1-4
- Build split up packages

* Mon Jan 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.1-3
- correct posttrans snippet

* Mon Jan 10 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.1-3
- Updated as per https://bugzilla.redhat.com/show_bug.cgi?id=603906#c24

* Tue Dec 28 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.1-2
- Correct scripts
- Correct directory ownership
- add desktop file patch

* Mon Dec 27 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.1-1
- update to latest upstream release
- Moved icon update scriptlets to -images
- Moved python-mako requires to -web

* Fri Oct 29 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.0-3
- correct License and check file ownerships
- updated icon cache scriplet

* Thu Oct 28 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.0-2
- Split into sub packages #603906

* Wed Oct 13 2010 Peter Gordon <peter@thecodergeek.com> - 1.3.0-1
- Update to new upstream release (1.3.0).
- Add P2P to the .desktop file Categories list.
- Resolves: #615984 (.desktop menu entry has wrong/missing categories)

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 1.3.0-0.3.rc1
- Rebuilt for boost-1.44

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 20 2010 Peter Gordon <peter@thecodergeek.com> - 1.3.0-0.1.rc1
- Update to new upstream release candidate (1.3.0 RC1)

* Sun Mar 28 2010 Peter Gordon <peter@thecodergeek.com> - 1.2.3-1
- Update to new upstream bug-fix release (1.2.3).

* Sat Feb 27 2010 Peter Gordon <peter@thecodergeek.com> - 1.2.1-1
- Update to new upstream bug-fix release (1.2.1)
- Add python-mako dependency to fix WebUI startup crash.
- Resolves: #568845 (missing dependency to python-mako)

* Sat Jan 16 2010 Peter Gordon <peter@thecodergeek.com> - 1.2.0-1
- Update to new upstream final release (1.2.0)

* Fri Jan 08 2010 Peter Gordon <peter@thecodergeek.com> - 1.2.0-0.4.rc5
- Update to new upstream release candidate (1.2.0 RC5)

* Wed Nov 25 2009 Peter Gordon <peter@thecodergeek.com> - 1.2.0-0.3.rc4
- Update to new upstream release candidate (1.2.0 RC4)

* Wed Nov 04 2009 Peter Gordon <peter@thecodergeek.com> - 1.2.0-0.2.rc3
- Update to new upstream release candidate (1.2.0 RC3)

* Sun Oct 11 2009 Peter Gordon <peter@thecodergeek.com> - 1.2.0-0.1.rc1
- Update to new upstream release candidate (1.2.0 RC1)
- Adds Twisted dependencies, and drops the D-Bus dependency.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.9-2
- Fixed rb_libtorrent-python dependency, so as not to use the
  %%min_rblibtorrent_ver macro any more (#510264).

* Wed Jun 17 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.9-1
- Update to new upstream bug-fix release (1.1.9).
- Do not hard-code minimum rb_libtorrent version. (We're only building against
  the system rb_libtorrent for Fedora 11+, which already has the necessary
  version.)

* Wed May 27 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.8-1
- Update to new upstream release (1.1.8) for bug-fixes and some translation
  updates. Adds dependency on chardet for fixing lots of bugs with torrents
  which are not encoded as UTF-8.
- Add back the flags, in an optional -flags subpackage as per the new Flags
  policy (Package_Maintainers_Flags_Policy on the wiki).
- Add LICENSE and README to installed documentation.

* Fri May 08 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.7-2
- Rebuild for the Boost 1.39.0 update.

* Sat May 02 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.7-1
- Update to new upstream bug-fix release (1.1.7).

* Mon Apr 06 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.6-1
- Update to new upstream bug-fix release (1.1.6)
- Fix GPL version, add OpenSSL exception to License.
- Remove libtool, openssl-devel, and boost-devel BuildRequires (were only
  necessary when building the in-tarball libtorrent copy).

* Mon Mar 16 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.5-1
- Update to new upstream bug-fix release (1.1.5)
- Remove FIXME comment about parallel-compilation. We're not building the
  in-tarball libtorrent copy anymore, so no compilation (other than the python
  bytecode) happens and we no longer need to worry about this.

* Tue Mar 10 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.4-2
- Fix the installed location of the scalable (SVG) icon (#483443).
  + scalable-icon-dir.diff

* Mon Mar 09 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.4-1
- Update to new upstream bug-fix release (1.1.4)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.3-1
- Update to new upstream bug-fix release (1.1.3)

* Sun Feb 01 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.2-2
- Fix scalable icon directory ownership (#483443).

* Sat Jan 31 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.2-1
- Update to new upstream bug-fix release (1.1.2)

* Sun Jan 25 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.1-1
- Update to new upstream bug-fix release (1.1.1)

* Sun Jan 11 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.0-1
- Update to new upstream release (1.1.0 Final - yay!)
- Drop the get_tracker_host patch (fixed upstream):
  - fix-get_tracker-host-if-no-tracker.patch

* Fri Jan 09 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.0-0.4.rc3
- Do not package the country flags data.
- Resolves: #479265 (country flags should not be used in Deluge)

* Wed Jan 07 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.0-0.3.rc3
- Add patch from upstream SVN to fix an error where torrents are not shown (or
  possibly shown in "Error" states) due to a bad inet_aton call:
  + fix-get_tracker-host-if-no-tracker.patch
- Resolves: #479097 (No torrent shown in menu); thanks to Mamoru Tasaka for
  the bug report.
- Fix day of previous %%changelog entry.

* Tue Jan 06 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.0-0.2.rc3
- Update to new upstream release candidate (1.1.0 RC3)
- Build against the system rb_libtorrent instead of using the in-tarball copy
  (requires rb_libtorrent 0.14+), and adjust dependencies accordingly. Drop
  the hacked setup.py script formerly used to enable this (fixed upstream):
  - fixed-setup.py
- Make it a noarch package now that it's just python scripts and related
  data files (translations, images, etc.)

* Mon Dec 29 2008 Peter Gordon <peter@thecodergeek.com> - 1.1.0-0.1.rc2
- Update to new upstream release candidate (1.1.0 RC2)

* Thu Dec 18 2008 Petr Machata <pmachata@redhat.com> - 1.0.7-2
- Rebuild for new boost.

* Tue Dec 16 2008 Peter Gordon <peter@thecodergeek.com> - 1.0.7-1
- Update to new upstream bug-fix release (1.0.7)
- Remove CC-BY-SA license (the Tango WebUI images have been replaced by upstream).

* Mon Dec 01 2008 Peter Gordon <peter@thecodergeek.com> - 1.0.6-1
- Update to new upstream release (1.0.6)
- Adds Tango images to the WebUI data (CC-BY-SA) and some man pages.
- Properly mark translation files with %%lang.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.5-3
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.5-2
- Rebuild for Python 2.6

* Thu Nov 13 2008 Peter Gordon <peter@thecodergeek.com> - 1.0.5-1
- Update to new upstream release (1.0.5)

* Fri Oct 31 2008 Peter Gordon <peter@thecodergeek.com> - 1.0.4-1
- Update to new upstream release (1.0.4).

* Fri Oct 24 2008 Peter Gordon <peter@thecodergeek.com> - 1.0.3-1
- Update to new upstream release (1.0.3)

* Sun Oct 12 2008 Peter Gordon <peter@thecodergeek.com> - 1.0.2-1
- Update to new upstream release (1.0.2)
- Drop multithreaded boost compilation patch (fixed upstream, again).
  - mt-boost-fix.patch

* Sat Sep 27 2008 Peter Gordon <peter@thecodergeek.com> - 1.0.0-1
- Update to new upstream release (1.0.0 Final)
- Apply patch from Mamoru Tasaka to build against the multi-threaded Boost
  libraries once more:
  + mt-boost-fix.patch
- Resolves: #464151 (About 1.0.0 build failure)

* Tue Sep 16 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.09-1
- Update to new upstream release candidate (1.0.0 RC9)
- Drop mt-boost patch (fixed upstream):
  - use-mt-boost.patch

* Sun Sep 07 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.08-1
- Update to new upstream release candidate (1.0.0 RC8)
- Drop state_upgrade script from the documentation. (This is now handled
  automatically.)
- Fix version in previous %%changelog entry.

* Wed Aug 13 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.07-1
- Update to new upstream release candidate (1.0.0 RC7)
- Drop desktop file icon name hack (fixed upstream).

* Wed Aug 13 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.06-1
- Update to new upstream release candidate (1.0.0 RC6)
- Drop desktop file icon name hack (fixed upstream).

* Fri Aug 01 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.04-1
- Update to new upstream release candidate (1.0.0 RC4)

* Wed Jul 23 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.03-2
- Add setuptools runtime dependency, to fix "No module named pkg_resources"
  error messages.

* Mon Jul 21 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.03-1
- Update to new upstream release candidate (1.0.0 RC3)
- Re-add the blocklist plugin, at upstream's suggestion. (The rewrite is
  complete.)

* Tue Jul 15 2008 Peter Gordon <peter@thecodergeek.com> - 0.9.02-1
- Update to new upstream release candidate (1.0.0 RC2)
- Force building against the multithreaded Boost libs.
  + use-mt-boost.patch
- Remove python-libtorrent Obsoletes. (It's been dead for 3 releases now; and
  is just clutter.)
- Remove the blocklist plugin, at upstream's recommendation.

* Tue Jun 24 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.9.3-1
- Update to new upstream release (0.5.9.3)

* Fri May 23 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.9.1-1
- Update to new upstream release (0.5.9.1)

* Fri May 02 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.9.0-1
- Update to new upstream release (0.5.9.0)
- Drop upstreamed default-preferences patch for disabling new version
  notifications:
  - default-prefs-no-release-notifications.patch

* Tue Apr 15 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8.9-1
- Update to new upstream release (0.5.8.9)

* Wed Mar 26 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8.7-1
- Update to new upstream release (0.5.8.7)

* Mon Mar 17 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8.6-1
- Update to new upstream release (0.5.8.6)

* Fri Feb 29 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8.5-1
- Update to new upstream release (0.5.8.5)

* Sat Feb 16 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8.4-1
- Update to new upstream release (0.5.8.4)
- Rebuild for GCC 4.3

* Mon Jan 28 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8.3-1
- Update to new upstream security fix release (0.5.8.3), which includes a fix
  for a potential remotely-exploitable stack overflow with a malformed
  bencoded message.

* Sat Jan 19 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8.1-1
- Update to new upstream bugfix release (0.5.8.1)

* Wed Jan 09 2008 Peter Gordon <peter@thecodergeek.com> - 0.5.8-3
- Add runtime dependency on dbus-x11 for the dbus-launch utility. Fixes bug
  428106 (Missing BR dbus-x11).
- Bump release to 3 to maintain a proper F8->F9+ upgrade path.

* Mon Dec 31 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.8-1
- Update to new upstream release (0.5.8)
- Merge Mamoru Tasaka's no-release-notification patch into the default-prefs
  patch.

* Sat Dec 29 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.7.98-1
- Update to new upstream release candidate (0.5.8 RC2)

* Mon Dec 24 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.7.95-1
- Update to new upstream release candidate (0.5.8 RC1)
- Completely suppress updates notification (bug 299601, 426642)

* Sun Dec 09 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.7.1-2
- Add missing icon cache %%post and %%postun scriptlets.
- Add missing egg-info to the %%files list.

* Fri Dec 07 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.7.1-1
- Update to new upstream bug-fix release (0.5.7.1).
- Sort %%files list (aesthetic-only change).

* Wed Dec 05 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.7-3
- Fix previous %%changelog Version.
- Cleanup the installed .desktop file. Fixes bug 413101 (deluge fails to build
  in rawhide  bad .desktop file.)

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.5.7-2
- Rebuild for deps

* Sat Nov 24 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.7-1
- Update to new upstream release (0.5.7)

* Sat Nov 24 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.6.96-1
- Update to new upstream release candidate (0.5.7 RC2)
- Drop plugin error patch (fixed upstream):
  - plugin-not-found-OK.patch

* Sat Nov 24 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.6.95-1
- Update to new upstream release candidate (0.5.7 RC)
- Update Source0 url
- Add upstream patch to prevent dying if plugin in prefs.state is not found on
  the filesystem:
  + plugin-not-found-OK.patch

* Wed Oct 31 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.6.2-1
- Update to new upstream bug-fix release (0.5.6.2)

* Tue Oct 30 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.6.1-1
- Update to new upstream bug-fix release (0.5.6.1)
- Drop use-mt-boost build script patch (fixed upstream):
  - use-mt-boost.patch

* Sat Oct 27 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.6-1
- Update to new upstream release (0.5.6)

* Wed Oct 17 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.5.95-1
- Update to new upstream release candidate (0.5.6 RC1)

* Thu Sep 20 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.5-2
- Fix release on previous %%changelog entry.
- Disable the version update notifications by default:
  + default-prefs-no-release-notifications.patch
  (Resolves bug 299601: Deluge alerts of new versions)

* Wed Sep 12 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.5-1
- Update to new upstream release (0.5.5)

* Mon Sep 03 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.4.1.95-1
- Update to new upstream release candidate (0.5.5 RC1)

* Mon Aug 13 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.4.1-1
- Update to new upstream release (0.5.4.1)
- Build with new binutils to gain BuildID debugging goodness.

* Mon Aug 06 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.4-1
- Update to new upstream release (0.5.4)

* Fri Aug 03 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.3-2
- Update License tag (GPLv2+).
- Rebuild against new Boost libraries, adding a patch to build against the
  multi-threaded ("*-mt") libraries:
  + use-mt-boost.patch

* Wed Jul 25 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.3-1
- Update to new upstream release candidate (0.5.3)
- Drop %%ifarch invocations for 64-bit builds. The internal setup script now
  properly determines this and adds the AMD64 compiler definition if necessary.

* Fri Jul 20 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.2.90-1
- Update to new upstream release candidate (0.5.3 RC1)
- Drop stale persistence fix patch (applied upstream):
  - fix-persistence-upgrade-rhbz_247927.patch

* Wed Jul 11 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.2-2
- Add patch to fix the existence of stale persistence files by automatically
  updating the deluge.deluge module name to deluge.core, or removing them if
  empty (bug 247927):
  + fix-persistence-upgrade-rhbz_247927.patch

* Sun Jul 08 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.2-1
- Update to new upstream release (0.5.2)
- Update Summary and %%description to reflect new µTorrent-compatible Peer
  Exchange ("PEX") functionality.

* Thu Jun 07 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.0.90.2-2
- Update to new upstream release (0.5.1 Beta 2)

* Sun Apr 08 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.0-2
- Make Deluge the upgrade path of the now-orphaned python-libtorrent package.

* Mon Mar 12 2007 Peter Gordon <peter@thecodergeek.com> - 0.5.0-1
- Update to new upstream release (0.5.0).

* Mon Mar 12 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.99.2-1
- Update to new upstream release (0.5 RC2).
- Drop IndexError exception-handling fix (applied upstream):
  - delugegtk.py-fix-IndexError-exception-handling.patch
- Use the system libtool instead of the one from the sources to ensure
  that no unnecessary RPATH hacks are added to the final build.

* Wed Mar 07 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.99.1-3
- Add a patch (submitted upstream) to properly catch a thrown IndexError in
  state message updates. This should resolve the bug wherein the UI stops
  updating its details and torrent listing.
  + delugegtk.py-fix-IndexError-exception-handling.patch

* Wed Mar 07 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.99.1-2
- Drop unneeded 64bit-python_long patch; as it seems to cause more trouble than
  it's worth. Instead, pass -DAMD64 as a compiler flag on 64-bit arches.
  - 64bit-python_long patch
  (This should fix the bug where, even though torrents are active, they are not
  shown in the GtkTreeView listing.)

* Tue Mar 06 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.99.1-1
- Update to new upstream release (0.5 RC1).
- Use rewritten setup.py instead of patching it so much, since it's easier to
  maintain across version upgrades and whatnot:
  + fixed-setup.py
- Remove the setup.py patches (no longer needed, since I'm packaging my own):
  - setup.py-dont-store-the-install-dir.patch
  - setup.py-build-against-system-libtorrent.patch

* Fri Mar 02 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.90.3-1
- Update to new upstream release (0.5 Beta 3).
- Add patch to fix storing of installation directory:
  + setup.py-dont-store-the-install-dir.patch
    (to be applied after setup.py-build-against-system-libtorrent.patch)

* Sun Feb 25 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.90.2-2
- Add patch to fix 64-bit python_long type.
  +  64bit-python_long.patch

* Sat Feb 24 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.90.2-1
- Update to new upstream release (0.5 Beta 2)
- Add patch to force building against system copy of rb_libtorrent:
  + setup.py-build-against-system-libtorrent.patch
- Remove python-libtorrent and a few other dependencies that are no longer
  used.

* Fri Feb 23 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.1-6
- Fix Source0 URL.

* Wed Feb 21 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.1-5
- Make notify-python dependency conditional (FC6+ only)
- Strip the unneeded shebang lines from the plugin scripts, since they are not
  meant to be directly executed.

* Wed Feb 07 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.1-4
- Update .desktop file: Icon should not have the "-256" size suffix.
- Add Requires: notify-python
- Remove strict dependency on python 2.3+, since we're targetting FC5+
  only, which has 2.4+.

* Wed Jan 10 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.1-3
- Use install instead of the cp/find/chmod fiasco of earlier releases for
  clarity and proper permissions setting.
- Be more consistent about use of %%{name} and other macros in file naming as
  well as whitespace between sections.

* Sun Jan 07 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.1-2
- Bump python-libtorrent dependency to 0.3.0-4, which contains a fix for
  64-bit systems.

* Wed Jan 03 2007 Peter Gordon <peter@thecodergeek.com> - 0.4.1-1
- Initial packaging for Fedora Extras.
