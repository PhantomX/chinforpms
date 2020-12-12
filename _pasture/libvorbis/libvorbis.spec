Name:           libvorbis
Summary:        The Vorbis General Audio Compression Codec
Version:        1.3.7
Release:        100%{?dist}

Epoch:          2

License:        BSD

URL:            https://www.xiph.org/
Source:         https://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  pkgconfig(ogg) >= 1.0

# https://ao-yumi.github.io/aotuv_web/index.html
# https://freac.org
Patch10:        https://freac.org/patches/%{name}-1.3.7-aotuv-b6.03.patch
Patch11:        https://freac.org/patches/%{name}-1.3.7-aotuv-b6.03-lancer.patch
Patch12:        0001-sharedbook-Revert-memory-leak-fix-to-please-Lancer-o.patch

%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates.

The libvorbis package contains runtime libraries for use in programs
that support Ogg Vorbis.


%package devel
Summary:        Development tools for Vorbis applications
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The libvorbis-devel package contains the header files and documentation
needed to develop applications with Ogg Vorbis.

%package devel-docs
Summary:        Documentation for developing Vorbis applications
Requires:       %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description devel-docs
Documentation for developing applications with libvorbis.


%prep
%autosetup -p1

sed -i "s|-O20|%{build_cflags}|" configure
sed -i "s/-ffast-math//" configure
sed -i "s/-mcpu=750//" configure


%build
%configure \
  --disable-static \
  --disable-silent-rules \
%{nil}

%make_build


%install
%make_install docdir=%{_pkgdocdir}

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la

%check
make check


%files
%doc AUTHORS
%license COPYING
%{_libdir}/libvorbis.so.*
%{_libdir}/libvorbisfile.so.*
%{_libdir}/libvorbisenc.so.*

%files devel
%{_includedir}/vorbis
%{_libdir}/libvorbis.so
%{_libdir}/libvorbisfile.so
%{_libdir}/libvorbisenc.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/vorbis.m4

%files devel-docs
%{_pkgdocdir}/*
%exclude %{_pkgdocdir}/doxygen-build.stamp


%changelog
* Tue Jul 14 2020 Phantom X <megaphantomx at hotmail dot com> - 2:1.3.7-100
- 1.3.7

* Wed Jan 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:1.3.6-100
- aoTuV and Lancer optimizations
- chinforpms updates

* Tue Jul 31 2018 Adam Jackson <ajax@redhat.com> - 1.3.6-3
- Sync with git (CVE-2017-14160, CVE-2018-10392,
  CVE-2018-10393, #1516379)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 16 2018 Adam Jackson <ajax@redhat.com> - 1.3.6-1
- libvorbis 1.3.6

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.3.5-5
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 David King <amigadave@amigadave.com> - 1.3.5-1
- Update to 1.3.5 (#1197923)
- Use license macro for COPYING
- Tighten subpackage dependencies
- Use make_install and make_build macros
- Use pkgconfig for BuildRequires
- Remove unnecessary Requires from devel subpackage
- Remove obsolete Obsoletes

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.3.4-5
- Fix build for https://fedoraproject.org/wiki/Changes/Harden_All_Packages

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.4-1
- libvorbis 1.3.4

* Wed Jan 15 2014 Adam Jackson <ajax@redhat.com> 1.3.3-7
- Nuke -mcpu=750 from cflags for PPC, that plus -mcpu=power7 confuses gcc.

* Thu Aug  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3.3-6
- Install docs to %%{_pkgdocdir} where available (#993967).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:1.3.3-3
- Run test suite during build.
- Fix doc file permissions and duplicate doc dir ownership.
- rpmlint warning fixes.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Adam Jackson <ajax@redhat.com> 1.3.3-1
- libvorbis 1.3.3 (#787635)

* Wed Jan 04 2012 Jindrich Novy <jnovy@redhat.com> 1.3.2-2
- ship documentation only in -doc subpackage and only license
  in -devel (#540634) - thanks to Edward Sheldrake
- -devel-doc subpackage requires -devel

* Wed Feb 09 2011 Adam Jackson <ajax@redhat.com> 1.3.2-1
- libvorbis 1.3.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 1.3.1-2
- Include COPYING in base package too.

* Mon Mar 29 2010 Adam Jackson <ajax@redhat.com> 1.3.1-1
- libvorbis 1.3.1.  Fixes surround.

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 1.2.3-5
- libvorbis-1.2.3-add-needed.patch: Fix FTBFS from --no-add-needed

* Mon Nov 23 2009 Adam Jackson <ajax@redhat.com> 1.2.3-4
- Fix doc subpackage build (#540634)

* Mon Nov  2 2009 Jindrich Novy <jnovy@redhat.com> 1.2.3-3
- backport patches to fix CVE-2009-3379 (#531765) from upstream

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Adam Jackson <ajax@redhat.com> 1.2.3-1
- libvorbis 1.2.3

* Wed Jul 08 2009 Adam Jackson <ajax@redhat.com> 1.2.2-2
- libvorbis-1.2.2-svn16228.patch: Backport a fix from pre-1.2.3 to hopefully
  fix small sound file playback. (#505610)

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.2.2-1
- libvorbis 1.2.2

* Wed Jun 03 2009 Adam Jackson <ajax@redhat.com> 1.2.2-0.1.rc1
- libvorbis 1.2.2rc1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Caolán McNamara <caolanm@redhat.com> -1:1.2.0-6
- rebuild to get provides pkgconfig(vorbisenc)

* Sun Sep  7 2008 Hans de Goede <hdegoede@redhat.com> -1:1.2.0-5
- Fix patch fuzz build failure

* Wed May 14 2008 Jindrich Novy <jnovy@redhat.com> - 1:1.2.0-4
- fix CVE-2008-1420, CVE-2008-1419, CVE-2008-1423 (#446344)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.2.0-3
- Autorebuild for GCC 4.3

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:1.2.0-2
- Don't include Makefile's in %%doc, avoiding a multilib conflict (bz 342481)

* Mon Oct 15 2007 Behdad Esfahbod <besfahbo@redhat.com> - 1:1.2.0-1
- Update to 1.2.0
- Resolves: #250115

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1:1.1.2-4
- Rebuild for build ID

* Mon Jun 25 2007 Matthias Clasen <mclasen@redhat.com> - 1:1.1.2-3
- Fix typos in %%description (#245471)

* Thu Feb  8 2007 Matthias Clasen <mclasen@redhat.com> - 1:1.1.2-2
- Package review cleanups
- Don't ship static libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.2-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.2-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.1.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 John (J5) Palmieri <johnp@redhat.com> 1:1.1.2-1
- Update to 1.1.2

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.1-1
- Update to 1.1.1

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.0-2
- rebuild with gcc 4.0

* Wed Sep 29 2004 Colin Walters <walters@redhat.com> 1:1.1.0-1
- Update to 1.1.0
- Remove upstreamed patch libvorbis-underquoted.patch

* Wed Sep 29 2004 Warren Togami <wtogami@redhat.com> 1:1.0.1-5
- link to .pdf spec rather than ship redundant copy
- spec cleanups

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.0.1-4
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 11 2003 Bill Nottingham <notting@redhat.com> 1:1.0.1-1
- update to 1.0.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Elliot lee <sopwith@redhat.com> 1:1.0-6
- Fix #81026 by updating libvorbis-1.0-m4.patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Bill Nottingham <notting@redhat.com> 1:1.0-4
- add epochs to dependencies, to avoid 1.0rc3 >= 1.0 miscomparisons
  (#79374)
- fix vorbis.m4

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1:1.0-2
- remove unpackaged files from the buildroot
- tell configure where ogg libs are
- lib64'ize
