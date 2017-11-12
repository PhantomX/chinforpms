%global svn_revision 3050
%global source_hash b020875391484d0dc3ffc163ba5aaff421256b26edd1d188504a24edcbdcaa1056b975e4ee2997f49e6f085c33d546d3c043a0a20d94ff0f9e25896942bf7134

Name:           kBuild
Version:        0.1.9998
Release:        14%{?svn_revision:.r%{svn_revision}}%{?dist}
Summary:        A cross-platform build environment

License:        BSD and GPLv2+
# most tools are from NetBSD, some are from FreeBSD,
# and make and sed are from GNU
URL:            http://svn.netlabs.org/kbuild
#Generated with kBuild-snapshot.sh
Source0:        http://pkgs.fedoraproject.org/repo/pkgs/%{name}/kBuild-r%{svn_revision}.tar.gz/sha512/%{source_hash}/kBuild-r%{svn_revision}.tar.gz
Patch0:         kBuild-0.1.3-escape.patch
Patch1:         kBuild-0.1.5-pthread.patch
Patch2:         kbuild-wrong-memset.patch
Patch3:         kBuild-0.1.98-arm.patch
Patch4:         kBuild-0.1.9998-ppc64le.patch
Patch5:         kBuild-0.1.9998-aarch64.patch

BuildRequires:  byacc libacl-devel flex
BuildRequires:  bison
BuildRequires:  autoconf automake gettext-devel


%description
This is a GNU make fork with a set of scripts to simplify
complex tasks and portable versions of various UNIX tools to
ensure cross-platform portability.

It is used mainly to build VirtualBox packages for RPM Fusion
repository.


%prep
#%setup -q -n %{name}-%{version}%{?patchlevel:-%{patchlevel}}
%setup -q -n %{name}
%patch0 -p1 -b .escape
%patch1 -p1 -b .pthreads
%patch2 -p1 -b .memset
%patch3 -p1 -b .arm
%patch4 -p1 -b .ppc64le
%patch5 -p1 -b .aarch64


%build
echo KBUILD_SVN_URL := http://svn.netlabs.org/repos/kbuild/trunk  >  SvnInfo.kmk
echo KBUILD_SVN_REV := %{svn_revision} >>  SvnInfo.kmk

%define bootstrap_mflags %{_smp_mflags} \\\
        CFLAGS="%{optflags}"            \\\
        KBUILD_VERBOSE=2                \\\
        KBUILD_VERSION_PATCH=9998

%define mflags %{bootstrap_mflags}      \\\
        NIX_INSTALL_DIR=%{_prefix}      \\\
        BUILD_TYPE=release              \\\
        MY_INST_MODE=0644               \\\
        MY_INST_BIN_MODE=0755

# The bootstrap would probably not be needed if we depended on ourselves,
# yet it is not guarranteed that new versions are compilable with older
# kmk versions, so with this we are on a safer side
find -name config.log -delete
kBuild/env.sh --full make -f bootstrap.gmk %{bootstrap_mflags}
kBuild/env.sh kmk %{mflags} rebuild
#pod2man -c 'kBuild for Debian GNU/Linux' \
#  -r kBuild-$(DEB_UPSTREAM_VERSION) debian/kmk.pod > debian/kmk.1


%install
export KBUILD_VERBOSE=2
kBuild/env.sh kmk %{mflags} PATH_INS=%{buildroot} install
# These are included later in files section
rm -r %{buildroot}%{_docdir}


%files
%{_bindir}/*
%{_datadir}/*
%doc ChangeLog kBuild/doc/QuickReference*
%license COPYING kBuild/doc/COPYING-FDL-1.3


%changelog
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9998-14.r3050
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9998-13.r3050
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Sérgio Basto <sergio@serjux.com> - 0.1.9998-12.r3025
- Update kBuild to revison 3025
- Upstream already fixed these 2:
  deleted:    kBuild-0.1.9998-glob.patch
  deleted:    kbuild-PKMKCCEVALPROG.patch
- Rebased:
  modified:   kBuild-0.1.98-arm.patch
  modified:   kBuild-0.1.9998-aarch64.patch
  modified:   kBuild-0.1.9998-ppc64le.patch

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9998-11.r2814
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 06 2016 Sérgio Basto <sergio@serjux.com> - 0.1.9998-10.r2814
- Fix el6 build

* Tue Jul 26 2016 Sérgio Basto <sergio@serjux.com> - 0.1.9998-9.r2814
- add BR:bison

* Fri Apr 29 2016 Sérgio Basto <sergio@serjux.com> - 0.1.9998-8.r2814
- Update kBuild to svn rev 2814

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9998-7.r2784
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 0.1.9998-6.r2784
- Add support for aarch64 (#1291091).

* Mon Jun 22 2015 Sérgio Basto <sergio@serjux.com> - 0.1.9998-5.r2784
- Update to trunk HEAD version.
- Rework patch for glob issue.
- Add kBuild-0.1.9998-ppc64le.patch to add support for ppc64le.
- Add kbuild-wrong-memset.patch, fix one warning.
- Fix License macro.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9998-4.r2730
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9998-3.r2730
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9998-2.r2730
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Sérgio Basto <sergio@serjux.com> - 0.1.9998-1.r2730
- Update to trunk HEAD version, have a fix for gcc >= 4.7 (http://trac.netlabs.org/kbuild/ticket/112)
- Drop kBuild-0.1.5-dprintf.patch patch, upstream source also have a fix in their own way.
- add kBuild-0.1.9998-gl_.patch to fix a regression on compiling in Linux
  (http://trac.netlabs.org/kbuild/ticket/117), partially reverses changeset 2702 . 

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.1.98-6.r1
- Bulk sad and useless attempt at consistent SPEC file formatting
- Fix ARM build

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.98-5.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.98-4.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.98-3.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.98-2.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.1.98-1.r1
- Later patchset

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-7.p2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.1.5-6.p2
- Fix build
- Update to later patch level

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-6.p1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.1.5-5.p1
- Update to later patchlevel to support VirtualBox 2.2.0

* Mon Apr 13 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.1.5-4
- Fix typoes (Robert P. J. Day, #495393)
- Comment out the colliding dprintf

* Sun Mar 1 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.1.5-3
- Fix up BRs

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.1.5-1
- Update to new upstream release

* Tue Dec 30 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.1.5-0.1.20081106svn
- Update to build VirtualBox OSE 2.1.0

* Fri Sep 19 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.1.4-1
- New upstream release

* Thu Aug 28 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.1.3-2
- Add gettext-devel to BRs for autopoint

* Sun Aug 17 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.1.3-1
- New upstream version
- Install into FHS hierarchy
- Honour optflags
- No need to be arch specific

* Tue Oct 30 2007 Till Maas <opensource till name> - 0.1.0-0.3.20070627svn
- add support for x86_64
- add BR: autoconf, automake

* Wed Jun 27 2007 Till Maas <opensource till name> - 0.1.0-0.2.20070627svn
- Update to a new version
- just copy the bin files to %%{_libexecdir}, kmk install does not work

* Sun Feb 18 2007 Till Maas <opensource till name> - 0.1.0-0.1.20070218svn
- Initial spec for fedora extras
