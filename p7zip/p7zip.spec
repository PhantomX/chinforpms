%global commit 79aac5226bdad25efda22095445ad7c4e0d9a06f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210328
%bcond_with snapshot

%if 0%{?rhel} && ! 0%{?epel}
%bcond_with gui
%else
%bcond_with gui
%endif
%global sanitize 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           p7zip
Version:        17.04
Release:        100%{?dist}
Summary:        Very high compression ratio file archiver

# Files under C/Compress/Lzma/ are dual LGPL or CPL
License:        LGPL-2.1-only and (LGPL-2.1-or-later OR CPL-1.0) AND GPL-2.0-only
URL:            http://p7zip.sourceforge.net/

%if 0%{sanitize}
%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
%else
# Use Makefile to download
%if %{with snapshot}
Source0:        %{name}-free-%{shortcommit}.tar.xz
%else
Source0:        %{name}-free-%{version}.tar.xz
%endif
%endif
Source1:        Makefile

Patch0:         0001-cmake-remove-rar.patch
Patch1:         0001-Add-exec-on-wrappers.patch
# from Debian
Patch4:         p7zip-manpages.patch
Patch7:         05-hardening-flags.patch
# Revert to fix zip extraction
Patch10:        0001-Revert-commit-c104127.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
%if %{with gui}
# for 7zG GUI
BuildRequires:  wxGTK3-devel
BuildRequires:  kde-filesystem
%endif
%ifarch %{ix86}
BuildRequires:  nasm
%endif
%ifarch x86_64
BuildRequires:  yasm
%endif

%description
p7zip is a port of 7za.exe for Unix. 7-Zip is a file archiver with a very high
compression ratio. The original version can be found at http://www.7-zip.org/.


%package plugins
Summary:        Additional plugins for p7zip
%if !%{with gui}
Obsoletes:      %{name}-gui < %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description plugins
Additional plugins that can be used with 7z to extend its abilities.
This package contains also a virtual file system for Midnight Commander.

%if %{with gui}
%package gui
Summary:        7zG - 7-Zip GUI version
Requires:       kde-filesystem
Requires:       p7zip-plugins

%description gui
7zG is a gui provide by p7zip and it is now in beta stage.
Also add some context menus for KDE4.
This package is *experimental*.
%endif

%package        doc
Summary:        Manual documentation and contrib directory
BuildArch:      noarch

%description    doc
This package contains the p7zip manual documentation and some code
contributions.

%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

%if 0%{sanitize}
  rm -rf CPP/7zip/{Archive,Compress,Crypto,CMAKE,QMAKE}/Rar*
  rm -f DOC/unRarLicense.txt
  rm -f Utils/file_Codecs_Rar_so.py
%endif

# move license files
mv DOC/License.txt DOC/copying.txt .

cp -p C/fast-lzma2/COPYING COPYING.fast-lzma2
cp -p C/zstd/COPYING COPYING.zstd

chmod +x check/*.sh

sed -e 's|strip |true |g' -i install.sh

%build
pushd CPP/7zip/CMAKE/
sh ./generate.sh
popd
%ifarch %{ix86}
cp -f makefile.linux_x86_asm_gcc_4.X makefile.machine
%endif
%ifarch x86_64
cp -f makefile.linux_amd64_asm makefile.machine
%endif
%ifarch ppc ppc64
cp -f makefile.linux_any_cpu_gcc_4.X makefile.machine
%endif

%make_build all2 \
%if %{with gui}
  7zG \
%endif
    OPTFLAGS="$CFLAGS" \
    LDFLAGS="$LDFLAGS" \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}


%install
make install \
    DEST_DIR=%{buildroot} \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libexecdir}/p7zip \
    DEST_MAN=%{_mandir}

# remove redundant DOC dir
mv %{buildroot}%{_docdir}/p7zip/DOC/* %{buildroot}%{_docdir}/p7zip
rmdir %{buildroot}%{_docdir}/p7zip/DOC/

%if %{with gui}
mkdir -p %{buildroot}%{_kde4_datadir}/kde4/services/ServiceMenus/
# remove a duplicated of p7zip_compress.desktop
rm GUI/kde4/p7zip_compress2.desktop
cp GUI/kde4/*.desktop %{buildroot}%{_kde4_datadir}/kde4/services/ServiceMenus/
#fix non-executable-in-bin
chmod +x %{buildroot}%{_bindir}/p7zipForFilemanager
%endif

%check
%if ! 0%{?rhel} || 0%{?rhel} >= 7
make test
%endif
# Next test fails, because we don't have X11 envoirment ...
# Error: Unable to initialize gtk, is DISPLAY set properly?
#make test_7zG || :


%files
%{_docdir}/p7zip
%exclude  %{_docdir}/p7zip/MANUAL
%license copying.txt License.txt
%{_bindir}/7za
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7za
%{_libexecdir}/p7zip/7zCon.sfx
%{_mandir}/man1/7za.1*
%exclude %{_mandir}/man1/7zr.1*

%files plugins
%license COPYING.fast-lzma2 COPYING.zstd
%doc README.md
%{_bindir}/7z
%dir %{_libexecdir}/p7zip/
%{_libexecdir}/p7zip/7z
%{_libexecdir}/p7zip/7z.so
#{_libexecdir}/p7zip/Codecs/
#{_libexecdir}/p7zip/Formats/
%{_mandir}/man1/7z.1*

%if %{with gui}
%files gui
%{_bindir}/7zG
%{_bindir}/p7zipForFilemanager
%{_libexecdir}/p7zip/7zG
%{_libexecdir}/p7zip/Lang
%{_kde4_datadir}/kde4/services/ServiceMenus/*.desktop
%endif

%files doc
%{_docdir}/p7zip/MANUAL
%doc contrib/


%changelog
* Sun Apr 04 2021 Phantom X <megaphantomx at hotmail dot com> - 17.04-100
- 17.04

* Mon Mar 29 2021 Phantom X <megaphantomx at hotmail dot com> - 17.03-102.20210328git79aac52
- Last snapshot

* Sun Jan 10 2021 Phantom X <megaphantomx at hotmail dot com> - 17.03-101
- Fix zip extraction

* Mon Jan 04 2021 Phantom X <megaphantomx at hotmail dot com> - 17.03-100
- 17.03, maintained fork
- Added LDFLAGS
- Disable unsupported gui for the time

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 24 2019 Sérgio Basto <sergio@serjux.com> - 16.02-16
- Add gcc10-conversion.patch provide by Red Hat's compiler team

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
- https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Mon Jul 09 2018 Scott Talbert <swt@techie.net> - 16.02-12
- Rebuild with wxWidgets 3.0

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 16.02-11
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Tue Feb 06 2018 Sérgio Basto <sergio@serjux.com> - 16.02-10
- Improve security patch

* Sat Jan 27 2018 Sérgio Basto <sergio@serjux.com> - 16.02-9
- Security fix for CVE-2017-17969 (from Debian)
- Add 05-hardening-flags.patch, 09-man-update.patch, 10-drop-fm-doc.patch
  and 14-Fix-g++-warning.patch patches from Debian, very small changes
  better documentation, compile flags and compile warning.

* Wed Jan 24 2018 Sérgio Basto <sergio@serjux.com> - 16.02-8
- Add sub-package doc

* Wed Jan 24 2018 Tomas Hoger <thoger@redhat.com> - 16.02-7
- Add conditional for building with(out) GUI support.  Keep GUI enabled for
  Fedora and EPEL builds, but disabled for RHEL.
- Add missing dependency - 7zG requires 7z.so, so p7zip-gui needs to require
  p7zip-plugins.

* Sun Sep 10 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 16.02-6
- Cleanup spec

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 21 2016 Sérgio Basto <sergio@serjux.com> - 16.02-2
- Security fix for CVE-2016-9296

* Mon Jul 18 2016 Sérgio Basto <sergio@serjux.com> - 16.02-1
- Update p7zip to 16.02 and fix security issues

* Sun Mar 27 2016 Sérgio Basto <sergio@serjux.com> - 15.14.1-1
- Update to 15.14.1
- Revert 7zFM build, upstream recomends not build it
  http://sourceforge.net/p/p7zip/bugs/175/

* Thu Mar 17 2016 Sérgio Basto <sergio@serjux.com> - 15.14-2
- Fix non-executable-in-bin for p7zipForFilemanager.
- Remove p7zip_compress2.desktop to not duplicate the menu entries.
- Also build 7zFM, rebuild p7zip_15.14_src_all-norar.tar.bz2, to build 7zFM
  instead 7zFM_do_not_use.

* Tue Mar 15 2016 Sérgio Basto <sergio@serjux.com> - 15.14-1
- Update to 15.14 .
- Rebase norar_cmake.patch
- Minor improvement in snippet of documentation.
- Drop patch1, from changelog build on s390 is fixed.
- Drop p7zip-15.09-CVE-2015-1038.patch, from changelog if fixed.
- Drop upstreamed p7zip_15.09-incorrect-fsf-address.patch .
- Drop p7zip_15.09-no7zG_and_7zFM.patch, p7zip build is fixed.
- Add sub-package p7zip-gui with 7zG.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.09-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Sérgio Basto <sergio@serjux.com> - 15.09-9
- Add 02_man.patch from Debian

* Fri Jan 22 2016 Sérgio Basto <sergio@serjux.com> - 15.09-8
- Revert better solutions for "create unowned directory"

* Fri Jan 22 2016 Sérgio Basto <sergio@serjux.com> - 15.09-7
- Split incorrect-fsf-address.patch and do not pack backup files

* Fri Jan 22 2016 Sérgio Basto <sergio@serjux.com> - 15.09-6
- Stating in License.txt file that we removed non-Free unrar code
  from sources (#190277)
- Fix incorrect fsf address in the license files.
- Add p7zip_15.09-no7zG_and_7zFM.patch in a diferent patch.

* Fri Jan 22 2016 Sérgio Basto <sergio@serjux.com> - 15.09-5
- Add license tag
- better solutions for "create unowned directory" (#917366)

* Thu Dec 03 2015 Sérgio Basto <sergio@serjux.com> - 15.09-4
- Fix CVE-2015-1038 (#1179505)

* Wed Dec 02 2015 Sérgio Basto <sergio@serjux.com> - 15.09-3
- Fix build on s390 architecture (#1286992)

* Thu Nov 12 2015 Sérgio Basto <sergio@serjux.com> - 15.09-2
- fix rhbz #917366

* Thu Nov 05 2015 Sérgio Basto <sergio@serjux.com> - 15.09-1
- Update to p7zip_15.09
- Use cmake.
- Refactor norar patch.
- Deleted: p7zip_9.20.1-execstack.patch (upstreamed)
- Deleted: p7zip_9.20.1-install.patch (upstreamed)
- Deleted: p7zip_9.20.1-nostrip.patch (upstreamed)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 9.20.1-9
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Matthias Saou <matthias@saou.eu> 9.20.1-2
- Execstack patch to fix what's wanted by the yasm code (#718778).

* Tue Jul 26 2011 Matthias Saou <matthias@saou.eu> 9.20.1-1
- Update to 9.20.1 (#688564).
- Update norar, nostrip and install patches.
- Minor clean ups : Don't use trivial macros + new email address.
- Don't require the main package from the plugins package (#690551).
- Use the any_cpu_gcc_4.X makefile for ppc* since the ppc specific one is gone.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Matthias Saou <matthias@saou.eu> 9.13-1
- Update to 9.13.
- Update norar and nostrip patches.

* Tue Dec  8 2009 Matthias Saou <matthias@saou.eu> 9.04-1
- Update to 9.04.
- Update norar patch.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <matthias@saou.eu> 4.65-1
- Update to 4.65.
- Update norar patch.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Matthias Saou <matthias@saou.eu> 4.61-1
- Update to 4.61.
- Update norar patch.
- Use asm for x86 too (nasm).

* Wed Jun 18 2008 Matthias Saou <matthias@saou.eu> 4.58-1
- Update to 4.58.
- Update norar patch.
- Update install patch.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Matthias Saou <matthias@saou.eu> 4.51-3
- Rebuild for new BuildID feature.

* Thu Aug  9 2007 Matthias Saou <matthias@saou.eu> 4.51-2
- Update License field some more (LGPL+ to LGPLv2+).

* Sun Aug  5 2007 Matthias Saou <matthias@saou.eu> 4.51-1
- Update to 4.51.
- Update License field.

* Tue Jun 19 2007 Matthias Saou <matthias@saou.eu> 4.47-1
- Update to 4.47.
- Include now required patch to exclude removed Rar bits from makefiles.
- Switch to using "make install" for installation... so patch and hack.
- Use the asm makefile for x86_64, so build require yasm for it too.
- Add ppc64 to the main %%ifarch.
- Remove no longer included Codecs and Formats dirs (7z.so replaces them?).
- Remove our wrapper scripts, since the install script creates its own.

* Thu Mar  1 2007 Matthias Saou <matthias@saou.eu> 4.44-2
- Remove _smp_mflags since some builds fail with suspicious errors.

* Thu Mar  1 2007 Matthias Saou <matthias@saou.eu> 4.44-1
- Update to 4.44.

* Mon Aug 28 2006 Matthias Saou <matthias@saou.eu> 4.42-2
- FC6 rebuild.

* Thu Jun 29 2006 Matthias Saou <matthias@saou.eu> 4.42-1
- Update to 4.42.

* Tue May  2 2006 Matthias Saou <matthias@saou.eu> 4.39-1
- Update to 4.39.
- Remove no longer needed gcc 4.1 patch.
- Use the gcc_4.X makefile.
- Remove RAR licensed files and RAR license itself (#190277).

* Mon Mar  6 2006 Matthias Saou <matthias@saou.eu> 4.30-3
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <matthias@saou.eu> 4.30-2
- Rebuild for new gcc/glibc.
- Include gcc 4.1 patch for extra qualification errors.

* Mon Nov 28 2005 Matthias Saou <matthias@saou.eu> 4.30-1
- Update to 4.30.

* Thu Oct 27 2005 Matthias Saou <matthias@saou.eu> 4.29-3
- Double quote args passed inside the shell scripts, to fix #171480.

* Mon Oct 10 2005 Matthias Saou <matthias@saou.eu> 4.29-2
- Update to 4.29.

* Sun Jun 05 2005 Dag Wieers <dag@wieers.com> - 4.20-1
- Updated to release 4.20.

* Sun Apr 10 2005 Dag Wieers <dag@wieers.com> - 4.16-1
- Moved inline scripts to %%prep stage.
- Removed quotes for $@ as it should not be necessary.

* Thu Mar 17 2005 Matthias Saou <matthias@saou.eu> 4.14.01-1
- Spec file cleanup.
- Fix wrapper scripts : Double quote $@ for filenames with spaces to work.
- Move files from /usr/share to /usr/libexec.
- Various other minor changes.

* Mon Jan 24 2005 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.14.01

* Sun Jan 16 2005 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.14

* Mon Dec 20 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - added 7za script and moved SFX module to _datadir/name/ to allow 7za & 7z
   use it simultaneously
 - returned to plugins in separate package

* Sat Dec 18 2004 Charles Duffy <cduffy@spamcop.net>
 - upgraded to 4.13
 - added 7z (not just 7za) with a shell wrapper
 - added gcc-c++ to the BuildRequires list

* Sat Nov 20 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.12
 - added virtual file system for Midnight Commander

* Thu Nov 11 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - upgraded to 4.10
 - plugins support was dropped out from p7zip

* Sun Aug 29 2004 Marcin Zajączkowski <mszpak@wp.pl>
 - initial release

