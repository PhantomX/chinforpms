%global _suffix 246


Summary: A GNU collection of binary utilities
Name: compat-binutils%{?_with_debug:-debug}
# Note - a version number of X.XX is an offical upstream GNU Binutils release.
# A version number of X.XX.50 is a snapshot of the upstream development sources.
# A version number of X.XX.90 is a pre-release snapshot.
# The variable %%{source} (see below) should be set to indicate which of these
# origins is being used.
Version: 2.46.1
Release: 1%{?dist}
License: GPL-3.0-or-later AND (GPL-3.0-or-later WITH Bison-exception-2.2) AND (LGPL-2.0-or-later WITH GCC-exception-2.0) AND BSD-3-Clause AND GFDL-1.3-or-later AND GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later
URL: https://sourceware.org/binutils

#---Start of Configure Options-----------------------------------------------

# The binutils can be built with the following parameters to change
#  the default behaviour:

# --with    bootstrap    Build with minimal dependencies.
# --with    clang        Force building with CLANG instead of GCC.
# --with    crossbuilds  Build cross targeted versions of the binutils as well as natives.
# --with    debug        Build without optimizations and without splitting the debuginfo into a separate file.
# --without debuginfod   Disable support for debuginfod.
# --without systemzlib   Use the binutils version of zlib.  Default is to use the system version.
# --without testsuite    Do not run the testsuite.  Default is to run it.
# --without xxhash       Do not link against the xxhash library.
# --without zstd         Do not link against the zstd library.

# Other configuration options can be set by modifying the following defines.

# Create shared libraries.
%define enable_shared 0

# Create deterministic archives (ie ones without timestamps).
# Default is off because of BZ 1195883.
%define enable_deterministic_archives 0

# Generate a warning when linking creates an executable stack
%define warn_for_executable_stacks 1

# Generate a warning when linking creates a segment with read, write and execute permissions
%define warn_for_rwx_segments 1

# Turn the above warnings into errors.
# Only effective if the warnings are enabled.
# Disabled by default because this is now handled by a macro in redhat-rpm-config.
%define error_for_executable_stacks 0
%define error_for_rwx_segments 0

# Enable support for GCC LTO compilation.
# Disable if it is necessary to work around bugs in LTO.
%define enable_lto 1

# Enable support for generating new dtags in the linker
# Disable if it is necessary to use RPATH instead.
# Currently enabled for Fedora, disabled for RHEL.
%if 0%{?fedora} != 0
%define enable_new_dtags 1
%else
%define enable_new_dtags 0
%endif

# Enable the compression of debug sections as default behaviour of the
# assembler and linker.  This option is disabled for now.  The assembler and
# linker have command line options to override the default behaviour.
%define default_compress_debug 0

# Default to read-only-relocations (relro) in shared binaries.
# This is enabled as a security feature.
%define default_relro 1

# Enable the default generation of GNU Build notes by the assembler.
# This option is disabled as it has turned out to be problematic for the i686
# architecture, although the exact reason has not been determined.  (See
# BZ 1572485).  It also breaks building EFI binaries on AArch64, as these
# cannot have relocations against absolute symbols.
%define default_generate_notes 0

# Enable thread support in the GOLD linker (if it is being built).  This is
# particularly important if plugins to the linker intend to use threads
# themselves.  See BZ 1636479 for more details.  This option is made
# configurable in case there is ever a need to disable thread support.
%define enable_threading 1

# Enable the use of separate code and data segments.  Whilst potentially
# useful from a security point of view, it is problematic from a file
# size point of view.  So for now, only enable it for the i686, x86_64
# and riscv64 architectures as these are the ones that have the most
# potential vulnerability.
%ifarch %{ix86} x86_64 riscv64
%define enable_separate_code 1
%else
%define enable_separate_code 0
%endif

# Enable the creation of relocations against the contents of read-only
# sections (such as .text).  This is a security vulnerability, so it is
# disabled here by default.
# Note - the upstream GNU Binutils sources enable the generation of this
# kind of relocation by default, so this is a difference between Ferdora
# and upstream.
%define enable_textrel 0

# Indicate where the sources come from.
#
# Official releases come from:  https://ftp.gnu.org/gnu/binutils
# Pre releases come from:       https://sourceware.org/pub/binutils/snapshots/
#   (Even numbered pre releases include gold)
# Snapshots come from:          https://snapshots.sourceware.org/binutils/trunk/
# Tarballs are made by hand following a process outlined in this document:
#                               https://fedoraproject.org/wiki/BinutilsRawhideSync
#
# Note - the Linux Kernel binutils releases are too unstable and contain
# too many controversial patches so we stick with the official GNU version
# instead.
#
# Note - there is a confusing misnomer in the URL for the pre-release tarballs.
# They are a "snapshot" of the about to be released branch sources, rather than
# a snapshot of the mainline development sources.

%define source official-release
# %%define source even-pre-release
# %%define source odd-pre-release
# %%define source snapshot
# %%define source tarball

# For snapshots and tarballs an extension is used to indicate the commit ID.
# We need to know that so that the source extraction process will work
# correctly.  Note %%(echo) is used because you cannot directly set a
# spec variable to a hexadecimal string value.

%define commit_id %(echo "ba5838a98fb")

#----End of Configure Options------------------------------------------------

# Default: Not bootstrapping.
%bcond bootstrap 0
# Default: Not debug
%bcond debug 0
# Default: support debuginfod.
%bcond debuginfod 1
# Default: Use the system supplied version of the zlib compression library.
%bcond systemzlib 1
# Default: Always run the testsuite.
%bcond testsuite 0
# Default: Use the xxhash-devel library.
%bcond xxhash 1
# Default: Use the libztsd-devel library.
%bcond zstd 1

%bcond gold 0

# Allow the user to override the compiler used to build the binutils.
# The default build compiler is gcc if %%toolchain is not clang.
%if "%toolchain" == "clang"
%bcond_without clang
%else
%bcond_with clang
%endif

%if %{with clang}
%global toolchain clang
%else
%global toolchain gcc
%endif

# (Do not) create cross targeted versions of the binutils.
%bcond crossbuilds 0
# %%bcond_without crossbuilds

%if %{with bootstrap}
%undefine with_docs
%undefine with_testsuite
%undefine with_gprofng
%endif

%if %{with debug}
%undefine with_testsuite
%define enable_shared 0
%endif

# GprofNG currenly only supports the x86 and AArch64 architectures.
%ifnarch x86_64 aarch64
%undefine with_gprofng
%endif

# The opcodes library needs a few functions defined in the bfd
# library, but these symbols are not defined in the stub bfd .so
# that is available at link time.  (They are present in the real
# .so that is used at run time).
%undefine _strict_symbol_defs_build

# BZ 1924068.  Since applications that use the BFD library are
# required to link against the static version, ensure that it retains
# its debug informnation.
%undefine __brp_strip_static_archive

# ODD numbered upstream GNU Binutils releases do not include the sources
# for the GOLD linker, so we use a snapshot from the mainline development
# sources instead - but only for GOLD, not for the rest of the binutils.

# FIXME: Delete this once the gold linker is fully deprecated.
# %%define gold_tarball %%(echo "binutils-with-gold-2.44.50-21e608528c3")
%define gold_tarball none

#----------------------------------------------------------------------------

%if "%{source}" == "official-release"
Source0: https://ftp.gnu.org/gnu/binutils/binutils-with-gold-%{version}.tar.xz
# Source0: https://ftp.gnu.org/gnu/binutils/binutils-%%{version}.tar.xz
%elif "%{source}" == "even-pre-release"
Source0: binutils-with-gold-%{version}.tar.xz
%elif "%{source}" == "odd-pre-release"
Source0: binutils-%%{version}.tar.xz
%elif "%{source}" == "snapshot"
Source0: binutils-with-gold-%{version}-%{commit_id}.tar.gz
%elif "%{source}" == "tarball"
Source0: binutils-%{version}-%{commit_id}.tar.xz
%endif

Source1: binutils-2.19.50.0.1-output-format.sed

%if "%{gold_tarball}" != "none"
Source2: %{gold_tarball}.tar.xz
%endif

#----------------------------------------------------------------------------

# Purpose:  Use /lib64 and /usr/lib64 instead of /lib and /usr/lib in the
#           default library search path of 64-bit targets.
# Lifetime: Permanent, but it should not be.  This is a bug in the libtool
#           sources used in both binutils and gcc, (specifically the
#           libtool.m4 file).  These are based on a version released in 2009
#           (2.2.6?) rather than the latest version.  (Definitely fixed in
#           libtool version 2.4.6).
Patch01: binutils-libtool-lib64.patch

# Purpose:  Appends a RHEL or Fedora release string to the generic binutils
#           version string.
# Lifetime: Permanent.  This is a RHEL/Fedora specific patch.
Patch02: binutils-version.patch

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
Patch04: binutils-no-config-h-check.patch

# Purpose:  Disable an x86/x86_64 optimization that moves functions from the
#           PLT into the GOTPLT for faster access.  This optimization is
#           problematic for tools that want to intercept PLT entries, such
#           as ltrace and LD_AUDIT.  See BZs 1452111 and 1333481.
# Lifetime: Permanent.  But it should not be.
# FIXME:    Replace with a configure time option.
Patch05: binutils-revert-PLT-elision.patch

# Purpose:  Do not create PLT entries for AARCH64 IFUNC symbols referenced in
#           debug sections.
# Lifetime: Permanent.
# FIXME:    Find related bug.  Decide on permanency.
Patch06: binutils-2.27-aarch64-ifunc.patch

# Purpose:  Stop the binutils from statically linking with libstdc++.
# Lifetime: Permanent.
Patch07: binutils-do-not-link-with-static-libstdc++.patch

# Purpose:  Allow the binutils to be configured with any (recent) version of
#            autoconf.
# Lifetime: Fixed in 2.46 (maybe ?)
Patch08: binutils-autoconf-version.patch

# Purpose:  Stop libtool from inserting useless runpaths into binaries.
# Lifetime: Who knows.
Patch09: binutils-libtool-no-rpath.patch

# Purpose:  Fix binutils testsuite failures.
# Lifetime: Permanent, but varies with each rebase.
Patch10: binutils-testsuite-fixes.patch

# Purpose:  Fix binutils testsuite failures for the RISCV-64 target.
# Lifetime: Permanent, but varies with each rebase.
Patch11: binutils-riscv-testsuite-fixes.patch

# Purpose:  Fix the ar test of non-deterministic archives.
# Lifetime: Fixed in 2.46
Patch12: binutils-fix-ar-test.patch

# Purpose:  Fix a seg fault in the AArch64 linker when building u-boot.
# Lifetime: Fixed in 2.46
Patch13: binutils-aarch64-small-plt0.patch

# Purpose:  Fix ld testsuite failures when enable_textrel is set.
# Lifetime: Permanent.
Patch20: binutils-ld-default-z-text.patch

#----------------------------------------------------------------------------

# Purpose:  Remove the Build protected-func-2 without PIE linker tests
#            as these are currently failing.
# Lifetime: TEMPORARY - should be fixed by the 2.46 release.
Patch98: binutils-remove-ld-protected-func-2-test.patch

# Purpose:  Suppress the x86 linker's p_align-1 tests due to kernel bug on CentOS-10.
# Lifetime: TEMPORARY
Patch99: binutils-suppress-ld-align-tests.patch

#----------------------------------------------------------------------------

Provides: bundled(libiberty)

%if %{with debug}
# Define this if you want to skip the strip step and preserve debug info.
# Useful for testing.
%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}
%endif

# Perl, sed and touch are all used in the %%prep section of this spec file.
BuildRequires: autoconf, automake, perl, sed, coreutils, make

# Bison is used to generate gold/yyscript.c and ld/ldgram.c.
BuildRequires: bison

%if %{with clang}
BuildRequires: clang compiler-rt
%else
BuildRequires: gcc
%endif

%if %{without bootstrap}
BuildRequires: gettext, flex, jansson-devel
%if %{with systemzlib}
BuildRequires: zlib-devel
%endif
%endif

BuildRequires: findutils

# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{with testsuite}
# relro_test.sh uses dc which is part of the bc rpm, hence its inclusion here.
# sharutils is needed so that we can uuencode the testsuite results.
BuildRequires: dejagnu, glibc-static, sharutils, bc, libstdc++
%if %{with systemzlib}
BuildRequires: zlib-devel
%endif
%endif

%if %{with debuginfod}
BuildRequires: elfutils-debuginfod-client-devel
%endif

%if %{with xxhash}
BuildRequires: xxhash-devel
%endif

%if %{with zstd}
BuildRequires: libzstd-devel
%endif

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif

#----------------------------------------------------------------------------

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

#----------------------------------------------------------------------------

# BZ 1924068.  Since applications that use the BFD library are
# required to link against the static version, ensure that it retains
# its debug informnation.
# FIXME: Yes - this is being done twice.  I have no idea why this
# second invocation is necessary but if both are not present the
# static archives will be stripped.
%undefine __brp_strip_static_archive

#----------------------------------------------------------------------------

%prep

%if "%{gold_tarball}" != "none"

%setup -q -n binutils-%{version} -a 0

%autopatch -p1 

%elif "%{source}" == "snapshot"
%autosetup -p1 -n binutils-with-gold-%{version}-%{commit_id}
%elif "%{source}" == "official-release"
%autosetup -p1 -n binutils-with-gold-%{version}
%elif "%{source}" == "even-pre-release"
%autosetup -p1 -n binutils-with-gold-%{version}
%elif "%{source}" == "odd-pre-release"
%autosetup -p1 -n binutils-%{version}
%else
%autosetup -p1 -n binutils-%{version} 
%endif

# On ppc64 and aarch64, we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c
%if %{with gold}
sed -i -e '/common_pagesize/s/4 /64 /' gold/powerpc.cc
sed -i -e '/pagesize/s/0x1000,/0x10000,/' gold/aarch64.cc
%endif

# LTP sucks
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}

# Build libbfd.so and libopcodes.so with -Bsymbolic-functions if possible.
if gcc %{optflags} -v --help 2>&1 | grep -q -- -Bsymbolic-functions; then
sed -i -e 's/^libbfd_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' bfd/Makefile.{am,in}
sed -i -e 's/^libopcodes_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' opcodes/Makefile.{am,in}
fi

# $PACKAGE is used for the gettext catalog name.
sed -i -e 's/^ PACKAGE=/ PACKAGE=%{?cross}/' */configure

# Undo the name change to run the testsuite.
for tool in binutils gas ld
do
  sed -i -e "2aDEJATOOL = $tool" $tool/Makefile.am
  sed -i -e "s/^DEJATOOL = .*/DEJATOOL = $tool/" $tool/Makefile.in
done

# Touch the .info files so that they are newer then the .texi files and
# hence do not need to be rebuilt.  This eliminates the need for makeinfo.
# The -print is there just to confirm that the command is working.
%if %{without docs}
  find . -name *.info -print -exec touch {} \;
%else
# If we are creating the docs, touch the texi files so that the info and
# man pages will be rebuilt.
  find . -name *.texi -print -exec touch {} \;
%endif

%ifarch %{power64}
%define _target_platform %{_arch}-%{_vendor}-%{_host_os}
%endif

#----------------------------------------------------------------------------

%build

# Building is now handled by functions which allow for both native and cross
# builds.  Builds are created in their own sub-directory of the sources, which
# allows for both native and cross builds to be created at the same time.

# compute_global_configuration()
#   Build the CARGS variable which contains the global configuration arguments.
compute_global_configuration()
{
    CARGS="--quiet \
 --program-suffix=%{?_suffix} \
 --build=%{_target_platform} \
 --host=%{_target_platform} \
 --enable-ld \
 --enable-plugins \
 --enable-64-bit-bfd \
 --enable-default-hash-style=gnu \
 --with-bugurl=%{dist_bug_report_url}"

%if %{without bootstrap}
    CARGS="$CARGS --enable-jansson=yes"
%endif

%if %{with debuginfod}
    CARGS="$CARGS --with-debuginfod"
%endif

    CARGS="$CARGS --enable-gprofng=no"

%if %{with systemzlib}
    CARGS="$CARGS --with-system-zlib=yes"
%endif

%if %{with xxhash}
    CARGS="$CARGS --with-xxhash=yes"
%else
    CARGS="$CARGS --with-xxhash=no"
%endif

%if %{with zstd}
    CARGS="$CARGS --with-zstd=yes"
%else
    CARGS="$CARGS --with-zstd=no"
%endif

%if %{default_compress_debug}
    CARGS="$CARGS --enable-compressed-debug-sections=all"
%else
    CARGS="$CARGS --enable-compressed-debug-sections=none"
%endif

%if %{default_generate_notes}
    CARGS="$CARGS --enable-generate-build-notes=yes"
%else
    CARGS="$CARGS --enable-generate-build-notes=no"
%endif

%if %{default_relro}
    CARGS="$CARGS --enable-relro=yes"
%else
    CARGS="$CARGS --enable-relro=no"
%endif

%if %{enable_deterministic_archives}
    CARGS="$CARGS --enable-deterministic-archives"
%else
    CARGS="$CARGS --enable-deterministic-archives=no"
%endif

%if %{warn_for_executable_stacks}
    CARGS="$CARGS --enable-warn-execstack=yes"
    CARGS="$CARGS --enable-default-execstack=no"
%if %{error_for_executable_stacks}
    CARGS="$CARGS --enable-error-execstack=yes"
%endif
%else
    CARGS="$CARGS --enable-warn-execstack=no"
%endif

%if %{warn_for_rwx_segments}
    CARGS="$CARGS --enable-warn-rwx-segments=yes"
%if %{error_for_rwx_segments}
    CARGS="$CARGS --enable-error-rwx-segments=yes"
%endif
%else
    CARGS="$CARGS --enable-warn-rwx-segments=no"
%endif

%if %{enable_lto}
    CARGS="$CARGS --enable-lto"
%endif

%if %{enable_new_dtags}
    CARGS="$CARGS --enable-new-dtags --disable-rpath"
%endif

%if %{enable_separate_code}
  CARGS="$CARGS --enable-separate-code=yes"
  CARGS="$CARGS --enable-rosegment=yes"
%else
  CARGS="$CARGS --enable-separate-code=no"
  CARGS="$CARGS --enable-rosegment=no"
%endif

%if %{enable_threading}
    CARGS="$CARGS --enable-threads=yes"
%else
    CARGS="$CARGS --enable-threads=no"
%endif

%if %{enable_textrel}
    CARGS="$CARGS --enable-textrel-check=no"
%else
    CARGS="$CARGS --enable-textrel-check=error"
%endif

%if "%{source}" != "official-release"
# Since non official release tarballs are created directly from development
# sources they will have "development=true" set in the bfd/development.sh file.
# This enables -Werror by default, which is a problem because there is a
# known issue with the libiberty library:
#   libiberty/cp-demangle.c: In function 'd_demangle_callback.constprop':
#   libiberty/cp-demangle.c:6794:1: error: stack usage might be unbounded [-Werror=stack-usage=]
# So we explicitly disable werror for builds from these tarballs.
    CARGS="$CARGS --enable-werror=no"
%endif
}

# run_target_configuration()
#    Create and configure the build tree.
#        $1 is the target architecture
#        $2 is 1 if this is a native build
#        $3 is 1 if shared libraries should be built
#
run_target_configuration()
{
    local target="$1"
    local native="$2"
    local shared="$3"
    local builddir=build-$target

    # Create a build directory
    rm -rf $builddir
    mkdir $builddir
    pushd $builddir

    echo "BUILDING the Binutils for TARGET $target (native ? $native) (shared ? $shared)"

    %set_build_flags

    # RHEL-121799: Builders may want to restrict the number of CPUs used by
    # the LTO compiler.  The normal way to do this is to set RPM_BUILD_NCPUS.
    # But this only affects the -j option passed to make.  By adding -flto=N
    # we can also restrict the number of threads used by the LTO compiler.
    export CFLAGS="$RPM_OPT_FLAGS -flto=$RPM_BUILD_NCPUS"

%ifarch %{power64}
    export CFLAGS="$CFLAGS -Wno-error"
%endif

%if %{with debug}
    %undefine _fortify_level
    export CFLAGS="$CFLAGS -O0 -ggdb2 -Wno-error"
%endif

    export CXXFLAGS="$CXXFLAGS $CFLAGS"

    # Some GNU extensions to the C11 standard are used.
    # Note set here as -std=gnu11 is not a valid G++ command line option.
    export CFLAGS="$CFLAGS -std=gnu11"

    # BZ 1541027 - include the linker flags from redhat-rpm-config as well.
    export LDFLAGS=$RPM_LD_FLAGS

%if %{enable_new_dtags}
    # Build the tools with new dtags, as well as supporting their generation by the linker.
    export LDFLAGS="$LDFLAGS -Wl,--enable-new-dtags"
%endif

    if test x$native == x1 ; then
        # Extra targets to build along with the native one.
        #
        # BZ 1920373: Enable PEP support for all targets as the PERF package's
        # testsuite expects to be able to read PE format files regardless of
        # the host's architecture.
        #
        # Also enable the BPF target so that strip will work on BPF files.
        case $target in
        s390*)
            # Note - The s390-linux target is there so that the GOLD linker will
            # build.  By default, if configured for just s390x-linux, the GOLD
            # configure system will only include support for 64-bit targets, but
            # the s390x gold backend uses both 32-bit and 64-bit templates.
            TARGS="--enable-targets=s390-linux,s390x-linux,x86_64-pep,bpf-unknown-none"
            ;;
        ia64*)
            TARGS="--enable-targets=ia64-linux,x86_64-pep,bpf-unknown-none"
            ;;
        ppc64-*)
            TARGS="--enable-targets=powerpc64le-linux,spu,x86_64-pep,bpf-unknown-none"
            ;;
        ppc64le*)
            TARGS="--enable-targets=powerpc-linux,spu,x86_64-pep,bpf-unknown-none"
            ;;
        *)
            TARGS="--enable-targets=x86_64-pep,bpf-unknown-none"
            ;;
        esac

        # Set up the sysroot and paths.
        SARGS="--with-sysroot=/ \
               --prefix=%{_prefix} \
               --libdir=%{_libdir} \
               --sysconfdir=%{_sysconfdir}"
        SARGS="$SARGS --disable-gold"
    fi
    if test x$shared == x1 ; then
        RARGS="--enable-shared"
    else
        RARGS="--disable-shared"
    fi
    
    ../configure --target=$target $CARGS $SARGS $RARGS $TARGS  || cat config.log

    popd
}

# build_target ()
#   Builds a configured set of sources.
#        $1 is the target architecture
build_target()
{
    local target="$1"
    local builddir=build-$target

    pushd $builddir

    mkdir -p gas/doc
    
    %make_build %{_smp_mflags} tooldir=%{_prefix} MAKEINFO=true all
    
    popd
}

# run_tests()
#       Test a built (but not installed) binutils.
#        $1 is the target architecture
#        $2 is 1 if this is a native build
#
run_tests()
{
    local target="$1"
    local native="$2"

    echo "TESTING the binutils FOR TARGET $target (native ? $native)"

    # Do not use %%check as it is run after %%install where libbfd.so is rebuilt
    # with -fvisibility=hidden no longer being usable in its shared form.
%if %{without testsuite}
    echo ================ $target == TESTSUITE DISABLED ====================
    return
%endif

    pushd build-$target

    # FIXME:  I have not been able to find a way to capture a "failed" return
    # value from "make check" without having it also stop the build.  So in
    # order to obtain the logs from the test runs if a check fails I have to
    # run the tests twice.  Once to generate the logs and then a second time
    # to generate the correct exit code.
    
    echo ================ $target == TEST RUN 1 =============================

    # Run the tests and accumulate the logs - but ignore failures...
    
    if test x$native == x1 ; then
        make -k check-gas check-binutils check-ld < /dev/null || :
    else
        # Do not try running linking tests for the cross-binutils.
        make -k check-gas check-binutils < /dev/null || :
    fi
    
    for f in {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
    do
        if [ -f $f ]; then
            cat $f
        fi
    done

    for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
    do
        if [ -f $file ]; then
            ln $file binutils-$target-$(basename $file) || :
        fi
    done

    tar cjf binutils-$target.tar.xz  binutils-$target-*.log
    uuencode binutils-$target.tar.xz binutils-$target.tar.xz
    rm -f binutils-$target.tar.xz    binutils-$target-*.log

    echo ================ $target == TEST RUN 2 =============================

    # Run the tests and this time fail if there are any errors.

    if test x$native == x1 ; then
        make -k check-gas check-binutils check-ld < /dev/null
        # Ignore the gold tests - they always fail
    else
        # Do not try running linking tests for the cross-binutils.
        make -k check-gas check-binutils < /dev/null
    fi

    popd
}

#----------------------------------------------------------------------------

# There is a problem with the clang+libtool+lto combination.
# The LDFLAGS containing -flto are not being passed when linking the
# libbfd.so, so the build fails.  Solution: disable LTO.
%if %{with clang}
%define enable_lto 0
%endif

%if %{with clang}
%define _with_cc_clang 1
%endif

# Disable LTO on arm due to:
# https://bugzilla.redhat.com/show_bug.cgi?id=1918924
%ifarch %{arm}
%define enable_lto 0
%endif

%if !0%{?enable_lto}
%global _lto_cflags %{nil}
%endif

compute_global_configuration

# Build the native configuration.
run_target_configuration  %{_target_platform} 1 %{enable_shared}
build_target              %{_target_platform}
run_tests                 %{_target_platform} 1 

#----------------------------------------------------------------------------

%install

# install_binutils()
#       Install the binutils.
#        $1 is the target architecture
#        $2 is 1 if this is a native build
#        $3 is 1 if shared libraries should be built
#
install_binutils()
{
    local target="$1"
    local native="$2"
    local shared="$3"

    local local_root=%{buildroot}/%{_prefix}
    local local_bindir=$local_root/bin
    local local_libdir=%{buildroot}%{_libdir}
    local local_mandir=$local_root/share/man/man1
    local local_incdir=$local_root/include
    local local_infodir=$local_root/share/info
    local local_libdir
    
    mkdir -p $local_libdir
    mkdir -p $local_incdir
    mkdir -p $local_mandir
    mkdir -p $local_infodir

    echo "INSTALLING the binutils FOR TARGET $target (native ? $native) (shared ? $shared)"

    pushd build-$target
    
    if test x$native == x1 ; then

        %make_install DESTDIR=%{buildroot} MAKEINFO=true

        # Rebuild the static libraries with -fPIC.
        # It would be nice to build the static libraries with -fno-lto so that
        # they can be used by programs that are built with a different version
        # of GCC from the one used to build the libraries, but this will trigger
        # warnings from annocheck.

        # Future: Remove libiberty together with its header file, projects should bundle it.
        %make_build -s -C libiberty clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libiberty

        # Without the hidden visibility the 3rd party shared libraries would export
        # the bfd non-stable ABI.
        %make_build -s -C bfd clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS -fvisibility=hidden" -C bfd

        %make_build -s -C opcodes clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C opcodes

        %make_build -s -C libsframe clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libsframe

        install -m 644 bfd/.libs/libbfd.a           $local_libdir
        install -m 644 libiberty/libiberty.a        $local_libdir
        install -m 644 ../include/libiberty.h       $local_incdir
        install -m 644 opcodes/.libs/libopcodes.a   $local_libdir
        install -m 644 libsframe/.libs/libsframe.a  $local_libdir

        # Remove Windows/Novell only man pages
        rm -f $local_mandir/{dlltool,nlmconv,windres,windmc}*
	rm -f $local_mandir/{addr2line,ar,as,c++filt,elfedit,gp,ld,nm,objcopy,objdump,ranlib,readelf,size,strings,strip}*
	rm -f $local_infodir/{as,bfd,binutils,ctf,gprof,ld,sframe}*
	rm -fr $local_infodir/../doc/gprofng

        # Prevent programs from linking against libbfd and libopcodes
        # dynamically, as they are changed far too often.
        rm -f $local_libdir/lib{bfd,opcodes}.so

        # Remove libtool files, which reference the .so libs
        rm -f %local_libdir/lib{bfd,opcodes}.la

        # Sanity check --enable-64-bit-bfd really works.
        grep '^#define BFD_ARCH_SIZE 64$' $local_incdir/bfd.h
        # Fix multilib conflicts of generated values by __WORDSIZE-based expressions.
%ifarch %{ix86} x86_64 ppc %{power64} s390 s390x sh3 sh4 sparc sparc64 arm
        sed -i -e '/^#include "ansidecl.h"/{p;s~^.*$~#include <bits/wordsize.h>~;}' \
            -e 's/^#define BFD_DEFAULT_TARGET_SIZE \(32\|64\) *$/#define BFD_DEFAULT_TARGET_SIZE __WORDSIZE/' \
            -e 's/^#define BFD_HOST_64BIT_LONG [01] *$/#define BFD_HOST_64BIT_LONG (__WORDSIZE == 64)/' \
            -e 's/^#define BFD_HOST_64_BIT \(long \)\?long *$/#if __WORDSIZE == 32\
#define BFD_HOST_64_BIT long long\
#else\
#define BFD_HOST_64_BIT long\
#endif/' \
            -e 's/^#define BFD_HOST_U_64_BIT unsigned \(long \)\?long *$/#define BFD_HOST_U_64_BIT unsigned BFD_HOST_64_BIT/' \
            $local_incdir/bfd.h
%endif

        touch -r ../bfd/bfd-in2.h $local_incdir/bfd.h

        # Generate .so linker scripts for dependencies; imported from glibc/Makerules:

        # This fragment of linker script gives the OUTPUT_FORMAT statement
        # for the configuration we are building.
        OUTPUT_FORMAT="\
/* Ensure this .so library will not be used by a link for a different format
   on a multi-architecture system.  */
$(gcc $CFLAGS $LDFLAGS -shared -x c /dev/null -o /dev/null -Wl,--verbose -v 2>&1 | sed -n -f "%{SOURCE1}")"

        tee $local_libdir/libbfd.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

/* The libz & libsframe dependencies are unexpected by legacy build scripts.  */
/* The libdl dependency is for plugin support.  (BZ 889134)  */
INPUT ( %{_libdir}/libbfd.a %{_libdir}/libsframe.a -liberty -lz -ldl )
EOH

        tee $local_libdir/libopcodes.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOH

        rm -fr $local_root/$target

    else # CROSS BUILDS

        local target_root=$local_root/$target
        
        %make_install DESTDIR=%{buildroot} MAKEINFO=true
    fi

    # This one comes from gcc
    rm -f $local_infodir/dir

    popd
}

#----------------------------------------------------------------------------

install_binutils %{_target_platform} 1 %{enable_shared}

ln -sf ld.bfd%{?_suffix} %{buildroot}%{_bindir}/ld%{?_suffix}

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}
rm -rf %{buildroot}%{_datadir}

# Stop check-rpaths from complaining about standard runpaths.
export QA_RPATHS=0x0003

#----------------------------------------------------------------------------

%files
%license COPYING COPYING3 COPYING3.LIB COPYING.LIB
%doc README
%{_bindir}/[!l]*%{?_suffix}
# %%verify(symlink) does not work for some reason, so using "owner" instead.
%verify(owner) %{_bindir}/ld%{?_suffix}
# %%verify(mtime) does not work, probably because of the alternatives command in the %%post stage, so using "owner" instead.  (#2277349)
%verify(owner) %{_bindir}/ld.bfd%{?_suffix}

#----------------------------------------------------------------------------
%changelog
* Fri Sep 18 2026 Phantom X <megaphantomx at hotmail dot com> - 2.46.1-1
- Initial spec, modified from Fedora binutils original

