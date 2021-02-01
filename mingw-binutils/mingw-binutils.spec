%global run_testsuite 1

Name:           mingw-binutils
Version:        2.34
Release:        100%{?dist}
Summary:        Cross-compiled version of binutils for Win32 and Win64 environments

License:        GPLv2+ and LGPLv2+ and GPLv3+ and LGPLv3+

URL:            http://www.gnu.org/software/binutils/
Source0:        http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2

### Patches from native package

# Unneeded, mingw does not have lib64
# Patch01: binutils-2.20.51.0.2-libtool-lib64.patch

# Purpose:  Appends a RHEL or Fedora release string to the generic binutils
#           version string.
# Lifetime: Permanent.  This is a RHEL/Fedora specific patch.
Patch02: binutils-2.25-version.patch

# Purpose:  Exports the demangle.h header file (associated with the libiberty
#           sources) with the binutils-devel rpm.
# Lifetime: Permanent.  This is a RHEL/Fedora specific patch.
Patch03: binutils-export-demangle.h.patch

# Purpose:  Disables the check in the BFD library's bfd.h header file that
#           config.h has been included before the bfd.h header.  See BZ
#           #845084 for more details.
# Lifetime: Permanent - but it should not be.  The bfd.h header defines
#           various types that are dependent upon configuration options, so
#           the order of inclusion is important.
# FIXME:    It would be better if the packages using the bfd.h header were
#           fixed so that they do include the header files in the correct
#           order.
Patch04: binutils-2.22.52.0.4-no-config-h-check.patch

# Purpose:  Include the filename concerned in readelf error messages.  This
#           makes readelf's output more helpful when it is run on multiple
#           input files.
# Lifetime: Permanent.  This patch changes the format of readelf's output,
#           making it better (IMHO) but also potentially breaking tools that
#           depend upon readelf's current format.  Hence it remains a local
#           patch.
Patch05: binutils-2.29-filename-in-error-messages.patch

# Unneeded, affects ELF only
# Patch06: binutils-2.29-revert-PLT-elision.patch

# Purpose:  Changes readelf so that when it displays extra information about
#           a symbol, this information is placed at the end of the line.
# Lifetime: Permanent.
# FIXME:    The proper fix would be to update the scripts that are expecting
#           a fixed output from readelf.  But it seems that some of them are
#           no longer being maintained.
Patch07: binutils-readelf-other-sym-info.patch

# Unneeded, affects ELF only
# Patch08: binutils-2.27-aarch64-ifunc.patch

# Purpose:  Stop the binutils from statically linking with libstdc++.
# Lifetime: Permanent.
Patch09: binutils-do-not-link-with-static-libstdc++.patch

# Unneeded, affects ELF only
# Patch10: binutils-attach-to-group.patch

# Purpose:  Stop gold from complaining about relocs in the .gnu.build.attribute
#           section that reference symbols in discarded sections.
# Lifetime: Fixed in 2.33 (maybe)
Patch11: binutils-gold-ignore-discarded-note-relocs.patch

# Purpose:  Allow OS specific sections in section groups.
# Lifetime: Might be fixed in 2.33
Patch12: binutils-special-sections-in-groups.patch

# Purpose:  Fix linker testsuite failures.
# Lifetime: Fixed in 2.33 (possibly)
Patch13: binutils-fix-testsuite-failures.patch

# Purpose:  Stop gold from aborting when input sections with the same name
#            have different flags.
# Lifetime: Fixed in 2.35 (maybe)
Patch14: binutils-gold-mismatched-section-flags.patch

# Purpose:  Fix a potential use of an initialised field by readelf.
# Lifetime: Fixed in 2.35
Patch15: binutils-readelf-compression-header-size.patch

# Purpose:  Add a check to the GOLD linker for a corrupt input file
#            with a fuzzed section offset.
# Lifetime: Fixed in 2.35 (maybe)
Patch16: binutils-CVE-2019-1010204.patch
# Backport fix for CVE-2020-16592
# https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;h=7ecb51549ab1ec22aba5aaf34b70323cf0b8509a
Patch17: binutils_CVE-2020-16592.patch
# Backport fix for CVE-2020-16598
# https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;h=ca3f923f82a079dcf441419f4a50a50f8b4b33c2
Patch18: binutils_CVE-2020-16598.patch

# Backport fixes for CVE-2021-20197.
Patch19: binutils-gdb.git-365f5fb6d0f0da83817431a275e99e6f6babbe04.patch
Patch20: binutils-gdb.git-1a1c3b4cc17687091cff5a368bd6f13742bcfdf8.patch
Patch21: binutils-gdb.git-014cc7f849e8209623fc99264814bce7b3b6faf2.patch

# https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;h=463ec189fe9eca199edf87cda2c31efbe850390d
Patch22: binutils-bug25993.patch

### MINGW specific patches

Patch102: binutils-config.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  texinfo
BuildRequires:  zlib-devel
BuildRequires:  mingw32-filesystem >= 102
BuildRequires:  mingw64-filesystem >= 102
%if %{run_testsuite}
BuildRequires:  dejagnu
BuildRequires:  sharutils
%endif
Provides:       bundled(libiberty)
BuildRequires:	autoconf, automake


%description
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.

%package -n mingw-binutils-generic
Summary:        Utilities which are needed for both the Win32 and Win64 toolchains

%description -n mingw-binutils-generic
Utilities (like strip and objdump) which are needed for
both the Win32 and Win64 toolchains

%package -n mingw32-binutils
Summary:        Cross-compiled version of binutils for the Win32 environment
Requires:       mingw-binutils-generic = %{version}-%{release}

# NB: This must be left in.
Requires:       mingw32-filesystem >= 95

%description -n mingw32-binutils
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.

%package -n mingw64-binutils
Summary:        Cross-compiled version of binutils for the Win64 environment
Requires:       mingw-binutils-generic = %{version}-%{release}

# NB: This must be left in.
Requires:       mingw64-filesystem >= 95

%description -n mingw64-binutils
Cross compiled binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.


%prep
%autosetup -p1 -n binutils-%{version}

# See Patch02
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}


%build
# Dependencies are not set up to rebuild the configure files
# in the subdirectories.  So we just rebuild the ones we care
# about
pushd libiberty
autoconf
popd
pushd intl
autoconf
popd

# We call configure directly rather than via macros, thus if
# we are using LTO, we have to manually fix the broken configure
# scripts
[ %{_lto_cflags}x != x ] && %{_fix_broken_configure_for_lto}


mkdir build_win32
pushd build_win32
CFLAGS="%{optflags}" \
../configure \
  --build=%_build --host=%_host \
  --target=%{mingw32_target} \
  --disable-nls \
  --with-sysroot=%{mingw32_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir}

%make_build
popd

mkdir build_win64
pushd build_win64
CFLAGS="%{optflags}" \
../configure \
  --build=%_build --host=%_host \
  --target=%{mingw64_target} \
  --disable-nls \
  --with-sysroot=%{mingw64_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir}

%make_build
popd

# Create multilib versions for the tools strip, objdump nm, and objcopy
mkdir build_multilib
pushd build_multilib
CFLAGS="%{optflags}" \
../configure \
  --build=%_build --host=%_host \
  --target=%{mingw64_target} \
  --enable-targets=%{mingw64_target},%{mingw32_target} \
  --disable-nls \
  --with-sysroot=%{mingw64_sysroot} \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir}

%make_build
popd


%check
%if !%{run_testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
pushd build_win32
  make -k check < /dev/null || :
  echo ====================TESTING WIN32 =========================
  cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
  echo ====================TESTING WIN32 END=====================
  for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
  do
    ln $file binutils-%{mingw32_target}-$(basename $file) || :
  done
  tar cjf binutils-%{mingw32_target}.tar.bz2 binutils-%{mingw32_target}-*.{sum,log}
  uuencode binutils-%{mingw32_target}.tar.bz2 binutils-%{mingw32_target}.tar.bz2
  rm -f binutils-%{mingw32_target}.tar.bz2 binutils-%{mingw32_target}-*.{sum,log}
popd

pushd build_win64
  make -k check < /dev/null || :
  echo ====================TESTING WIN64 =========================
  cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
  echo ====================TESTING WIN64 END=====================
  for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
  do
    ln $file binutils-%{mingw64_target}-$(basename $file) || :
  done
  tar cjf binutils-%{mingw64_target}.tar.bz2 binutils-%{mingw64_target}-*.{sum,log}
  uuencode binutils-%{mingw64_target}.tar.bz2 binutils-%{mingw64_target}.tar.bz2
  rm -f binutils-%{mingw64_target}.tar.bz2 binutils-%{mingw64_target}-*.{sum,log}
popd
%endif


%install
%mingw_make_install
make -C build_multilib DESTDIR=%{buildroot}/multilib install

# These files conflict with ordinary binutils.
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_libdir}/libiberty*

# Keep the multilib versions of the strip, objdump and objcopy commands
# We need these for the RPM integration as these tools must be able to
# both process win32 and win64 binaries
mv %{buildroot}/multilib%{_bindir}/%{mingw64_strip} %{buildroot}%{_bindir}/%{mingw_strip}
mv %{buildroot}/multilib%{_bindir}/%{mingw64_objdump} %{buildroot}%{_bindir}/%{mingw_objdump}
mv %{buildroot}/multilib%{_bindir}/%{mingw64_objcopy} %{buildroot}%{_bindir}/%{mingw_objcopy}
mv %{buildroot}/multilib%{_bindir}/%{mingw64_nm} %{buildroot}%{_bindir}/%{mingw_nm}
rm -rf %{buildroot}/multilib


%files -n mingw-binutils-generic
%license COPYING
%{_mandir}/man1/*
%{_bindir}/%{mingw_strip}
%{_bindir}/%{mingw_objdump}
%{_bindir}/%{mingw_objcopy}
%{_bindir}/%{mingw_nm}

%files -n mingw32-binutils
%{_bindir}/%{mingw32_target}-addr2line
%{_bindir}/%{mingw32_target}-ar
%{_bindir}/%{mingw32_target}-as
%{_bindir}/%{mingw32_target}-c++filt
%{_bindir}/%{mingw32_target}-dlltool
%{_bindir}/%{mingw32_target}-dllwrap
%{_bindir}/%{mingw32_target}-elfedit
%{_bindir}/%{mingw32_target}-gprof
%{_bindir}/%{mingw32_target}-ld
%{_bindir}/%{mingw32_target}-ld.bfd
%{_bindir}/%{mingw32_target}-nm
%{_bindir}/%{mingw32_target}-objcopy
%{_bindir}/%{mingw32_target}-objdump
%{_bindir}/%{mingw32_target}-ranlib
%{_bindir}/%{mingw32_target}-readelf
%{_bindir}/%{mingw32_target}-size
%{_bindir}/%{mingw32_target}-strings
%{_bindir}/%{mingw32_target}-strip
%{_bindir}/%{mingw32_target}-windmc
%{_bindir}/%{mingw32_target}-windres
%{_prefix}/%{mingw32_target}/bin/ar
%{_prefix}/%{mingw32_target}/bin/as
%{_prefix}/%{mingw32_target}/bin/dlltool
%{_prefix}/%{mingw32_target}/bin/ld
%{_prefix}/%{mingw32_target}/bin/ld.bfd
%{_prefix}/%{mingw32_target}/bin/nm
%{_prefix}/%{mingw32_target}/bin/objcopy
%{_prefix}/%{mingw32_target}/bin/objdump
%{_prefix}/%{mingw32_target}/bin/ranlib
%{_prefix}/%{mingw32_target}/bin/readelf
%{_prefix}/%{mingw32_target}/bin/strip
%{_prefix}/%{mingw32_target}/lib/ldscripts

%files -n mingw64-binutils
%{_bindir}/%{mingw64_target}-addr2line
%{_bindir}/%{mingw64_target}-ar
%{_bindir}/%{mingw64_target}-as
%{_bindir}/%{mingw64_target}-c++filt
%{_bindir}/%{mingw64_target}-dlltool
%{_bindir}/%{mingw64_target}-dllwrap
%{_bindir}/%{mingw64_target}-elfedit
%{_bindir}/%{mingw64_target}-gprof
%{_bindir}/%{mingw64_target}-ld
%{_bindir}/%{mingw64_target}-ld.bfd
%{_bindir}/%{mingw64_target}-nm
%{_bindir}/%{mingw64_target}-objcopy
%{_bindir}/%{mingw64_target}-objdump
%{_bindir}/%{mingw64_target}-ranlib
%{_bindir}/%{mingw64_target}-readelf
%{_bindir}/%{mingw64_target}-size
%{_bindir}/%{mingw64_target}-strings
%{_bindir}/%{mingw64_target}-strip
%{_bindir}/%{mingw64_target}-windmc
%{_bindir}/%{mingw64_target}-windres
%{_prefix}/%{mingw64_target}/bin/ar
%{_prefix}/%{mingw64_target}/bin/as
%{_prefix}/%{mingw64_target}/bin/dlltool
%{_prefix}/%{mingw64_target}/bin/ld
%{_prefix}/%{mingw64_target}/bin/ld.bfd
%{_prefix}/%{mingw64_target}/bin/nm
%{_prefix}/%{mingw64_target}/bin/objcopy
%{_prefix}/%{mingw64_target}/bin/objdump
%{_prefix}/%{mingw64_target}/bin/ranlib
%{_prefix}/%{mingw64_target}/bin/readelf
%{_prefix}/%{mingw64_target}/bin/strip
%{_prefix}/%{mingw64_target}/lib/ldscripts


%changelog
* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 2.34-100
- patch for binutils bug #25993

* Thu Jan 28 2021 Richard W.M. Jones <rjones@redhat.com> - 2.34-7
- Backport fixes for CVE-2021-20197.
- Bump and rebuild for s390.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Sandro Mani <manisandro@gmail.com> - 2.34-4
- Backport patches for CVE-2020-16592, CVE-2020-16598

* Wed Jul 29 2020 Sandro Mani <manisandro@gmail.com> - 2.34-3
- Fix ld --version output

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Jeff Law <law@redhat.com> - 2.34.0-2
- Fix configure tests compromised by LTO

* Fri Jun 19 2020 Sandro Mani <manisandro@gmail.com> - 2.34.0-1
- Update to 2.34.0
- Modernize spec

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 19 2019 Sandro Mani <manisandro@gmail.com> - 2.32-6
- Add binutils_24267.patch
- Drop non-relevant patches from native binutils package

* Tue Aug 13 2019 Fabiano Fidêncio <fidencio@redhat.com> - 3.32-5
- Backport all patches from native binutils package, rhbz#1740709

* Wed Aug 07 2019 Sandro Mani <manisandro@gmail.com> - 2.32-4
- Backport patch to fix "too many open files" when linking libLLVM.dll

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Sandro Mani <manisandro@gmail.com> - 2.32-1
- Update to 2.32

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 22 2018 Sandro Mani <manisandro@gmail.com> - 2.30-5
- Refresh patch for binutils bug #23061

* Wed Aug 08 2018 Sandro Mani <manisandro@gmail.com> - 2.30-4
- Backport patch for binutils bug #23061

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Sandro Mani <manisandro@gmail.com> - 2.30-2
- Backport patch for binutils bug #22762

* Thu Jun 14 2018 Sandro Mani <manisandro@gmail.com> - 2.30-1
- Update to 2.30

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 2.29.1-1
- Update to 2.29.1

* Tue Sep 19 2017 Sandro Mani <manisandro@gmail.com> - 2.29-4
- Rebuild for mingw-filesystem (for %%mingw_nm macro)

* Fri Aug 25 2017 Sandro Mani <manisandro@gmail.com> - 2.29-3
- Also build multilib version of nm

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Kalev Lember <klember@redhat.com> - 2.29-1
- Update to 2.29

* Mon Mar 06 2017 Kalev Lember <klember@redhat.com> - 2.28-1
- Update to 2.28

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 10 2016 Kalev Lember <klember@redhat.com> - 2.27-1
- Update to 2.27

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 2.26-1
- Update to 2.26

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25-1
- Update to 2.25

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.24-5
- Fix CVE-2014-8501 (RHBZ #1162578 #1162583)
- Fix CVE-2014-8502 (RHBZ #1162602)
- Fix CVE-2014-8503 (RHBZ #1162612)
- Fix CVE-2014-8504 (RHBZ #1162626)
- Fix CVE-2014-8737 (RHBZ #1162660)
- Fix CVE-2014-8738 (RHBZ #1162673)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.24-2
- Fix FTBFS against gcc 4.9

* Sat Jan 11 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.24-1
- Update to 2.24

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.52.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.52.0.1-1
- Update to 2.23.52.0.1
- Fixes FTBFS against latest texinfo
- Resolve build failure on PPC

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.51.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.51.0.5-3
- Backported patch to fix 'unexpected version string length' error in windres (RHBZ #902960)

* Tue Nov 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.51.0.5-2
- Added BR: zlib-devel to enable support for compressed debug sections

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.51.0.5-1
- Update to 2.23.51.0.5 release

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 2.22.52.0.4-2
- Provides: bundled(libiberty)

* Wed Jul 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52.0.4-1
- Update to 2.22.52.0.4 release

* Sat Jun  2 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52.0.3-1
- Update to 2.22.52.0.3 release

* Sun Apr  8 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-4
- Cleaned up unneeded %%global tags

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-3
- Made the package compliant with the new MinGW packaging guidelines
- Added win64 support
- Added a mingw-binutils-generic package containing toolchain
  utilities which can be used by both the win32 and win64 toolchains
- Enable the testsuite
- Package the license
- Fix source URL

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-2
- Renamed the source package to mingw-binutils (RHBZ #673786)
- Use mingw macros without leading underscore

* Sat Feb 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.52-1
- Update to 2.22.52 20120225 snapshot
- Bump the BR/R: mingw32-filesystem to >= 95
- Rebuild using the i686-w64-mingw32 triplet
- Dropped some obsolete configure arguments
- Temporary provide mingw-strip, mingw-objdump and mingw-objcopy
  in preparation for win32+win64 support

* Tue Jan 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22-1
- Update to 2.22
- Dropped unneeded RPM tags
- Use parallel make

* Tue May 10 2011 Kalev Lember <kalev@smartlink.ee> - 2.21-2
- Default to runtime pseudo reloc v2 now that mingw32-runtime 3.18 is in

* Thu Mar 17 2011 Kalev Lember <kalev@smartlink.ee> - 2.21-1
- Update to 2.21
- Added a patch to use runtime pseudo reloc v1 by default as the version of
  mingw32-runtime we have does not support v2.
- Don't own the /usr/i686-pc-mingw32/bin/ directory

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.51.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep  7 2010 Richard W.M. Jones <rjones@redhat.com> - 2.20.51.0.10-1
- Synchronize with Fedora native version (2.20.51.0.10).
- Note however that we are not using any Fedora patches.

* Thu May 13 2010 Kalev Lember <kalev@smartlink.ee> - 2.20.1-1
- Update to 2.20.1

* Wed Sep 16 2009 Kalev Lember <kalev@smartlink.ee> - 2.19.51.0.14-1
- Update to 2.19.51.0.14

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-4
- Switch to using upstream (GNU) binutils 2.19.1.  It's exactly the
  same as the MinGW version now.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-2
- Rebuild for mingw32-gcc 4.4

* Tue Feb 10 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-1
- New upstream version 2.19.1.

* Mon Dec 15 2008 Richard W.M. Jones <rjones@redhat.com> - 2.19-1
- New upstream version 2.19.

* Sat Nov 29 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-10
- Must runtime-require mingw32-filesystem.

* Fri Nov 21 2008 Levente Farkas <lfarkas@lfarkas.org> - 2.18.50_20080109_2-9
- BR mingw32-filesystem >= 38

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-8
- Rename mingw -> mingw32.
- BR mingw32-filesystem >= 26.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-7
- Use mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-5
- Initial RPM release, largely based on earlier work from several sources.
