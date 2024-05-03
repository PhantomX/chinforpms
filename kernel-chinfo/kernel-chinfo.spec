# All Global changes to build and install go here.
# Per the below section about __spec_install_pre, any rpm
# environment changes that affect %%install need to go
# here before the %%install macro is pre-built.

# Disable frame pointers
%undefine _include_frame_pointers

# Disable LTO in userspace packages.
%global _lto_cflags %{nil}

# Speep up packaging, no rpaths to search here
%global __brp_check_rpaths %{nil}

# Disable some extractors from kernel-rpm-macros, speed up packaging, but no ksyms provides
%bcond_with rpm_macros

%if %{without rpm_macros}
%global __required_ksyms_requires %{nil}
%global __provided_ksyms_provides %{nil}
%endif

# Option to enable compiling with clang instead of gcc.
%bcond_with toolchain_clang

%if %{with toolchain_clang}
%global toolchain clang
%endif

# Compile the kernel with LTO (only supported when building with clang).
%bcond_with clang_lto

%if %{with clang_lto} && %{without toolchain_clang}
%{error:clang_lto requires --with toolchain_clang}
%endif

# RPM macros strip everything in BUILDROOT, either with __strip
# or find-debuginfo.sh. Make use of __spec_install_post override
# and save/restore binaries we want to package as unstripped.
%define buildroot_unstripped %{_builddir}/root_unstripped
%define buildroot_save_unstripped() \
(cd %{buildroot}; cp -rav --parents -t %{buildroot_unstripped}/ %1 || true) \
%{nil}
%define __restore_unstripped_root_post \
    echo "Restoring unstripped artefacts %{buildroot_unstripped} -> %{buildroot}" \
    cp -rav %{buildroot_unstripped}/. %{buildroot}/ \
%{nil}

# The kernel's %%install section is special
# Normally the %%install section starts by cleaning up the BUILD_ROOT
# like so:
#
# %%__spec_install_pre %%{___build_pre}\
#     [ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "${RPM_BUILD_ROOT}"\
#     mkdir -p `dirname "$RPM_BUILD_ROOT"`\
#     mkdir "$RPM_BUILD_ROOT"\
# %%{nil}
#
# But because of kernel variants, the %%build section, specifically
# BuildKernel(), moves each variant to its final destination as the
# variant is built.  This violates the expectation of the %%install
# section.  As a result we snapshot the current env variables and
# purposely leave out the removal section.  All global wide changes
# should be added above this line otherwise the %%install section
# will not see them.
%global __spec_install_pre %{___build_pre}

# Replace '-' with '_' where needed so that variants can use '-' in
# their name.
%define uname_suffix %{lua:
	local flavour = rpm.expand('%{?1:+%{1}}')
	flavour = flavour:gsub('-', '_')
	if flavour ~= '' then
		print(flavour)
	end
}

# This returns the main kernel tied to a debug variant. For example,
# kernel-debug is the debug version of kernel, so we return an empty
# string. However, kernel-64k-debug is the debug version of kernel-64k,
# in this case we need to return "64k", and so on. This is used in
# macros below where we need this for some uname based requires.
%define uname_variant %{lua:
	local flavour = rpm.expand('%{?1:%{1}}')
	_, _, main, sub = flavour:find("(%w+)-(.*)")
	if main then
		print("+" .. main)
	end
}

# At the time of this writing (2019-03), RHEL8 packages use w2.xzdio
# compression for rpms (xz, level 2).
# Kernel has several large (hundreds of mbytes) rpms, they take ~5 mins
# to compress by single-threaded xz. Switch to threaded compression,
# and from level 2 to 3 to keep compressed sizes close to "w2" results.
#
# NB: if default compression in /usr/lib/rpm/redhat/macros ever changes,
# this one might need tweaking (e.g. if default changes to w3.xzdio,
# change below to w4T.xzdio):
#
# This is disabled on i686 as it triggers oom errors

%ifnarch i686
%define _binary_payload w3T.xzdio
%endif

Summary: The Linux kernel

%if 0%{?fedora}
%define secure_boot_arch x86_64
%else
%define secure_boot_arch x86_64 aarch64 s390x ppc64le
%endif

# Signing for secure boot authentication
%ifarch %{secure_boot_arch}
%global signkernel 1
%else
%global signkernel 0
%endif

# Sign modules on all arches
%global signmodules 1

# Compress modules only for architectures that build modules
%ifarch noarch
%global zipmodules 0
%else
%global zipmodules 1
%endif

# Default compression algorithm
%global compression xz
%global compression_flags --compress
%global compext xz
%if %{zipmodules}
%global zipsed -e 's/\.ko$/\.ko.%compext/'
%endif


#global buildid .chinfo

%global variant -chinfo
%global variantid  %{lua:variantid = string.gsub(rpm.expand("%{?variant}"), "-", "."); print(variantid)}

%if 0%{?fedora}
%define primary_target fedora
%else
%define primary_target rhel
%endif

#
# genspec.sh variables
#

# kernel package name
%global package_name kernel%{?variant}
%global gemini 0
%if "0%{?variant}" != "0"
%global gemini 1
%endif
# Include Fedora files
%global include_fedora 1
# Include RHEL files
%global include_rhel 0
# Include RT files
%global include_rt 0
# Provide Patchlist.changelog file
%global patchlist_changelog 0

# Set released_kernel to 1 when the upstream source tarball contains a
#  kernel release. (This includes prepatch or "rc" releases.)
# Set released_kernel to 0 when the upstream source tarball contains an
#  unreleased kernel development snapshot.
%global released_kernel 1

# Set debugbuildsenabled to 1 to build separate base and debug kernels
#  (on supported architectures). The kernel-debug-* subpackages will
#  contain the debug kernel.
# Set debugbuildsenabled to 0 to not build a separate debug kernel, but
#  to build the base kernel using the debug configuration. (Specifying
#  the --with-release option overrides this setting.)
%define debugbuildsenabled 1
# define buildid .local
%define specrpmversion 6.8.9
%define specversion %{specrpmversion}
%define patchversion %(echo %{specversion} | cut -d'.' -f-2)
%define baserelease 500
%define pkgrelease %{baserelease}
%define kversion %(echo %{specversion} | cut -d'.' -f1)
%define tarfile_release %(echo %{specversion} | cut -d'.' -f-2)
# This is needed to do merge window version magic
%define patchlevel %(echo %{specversion} | cut -d'.' -f2)
%define stable_update %(echo %{specversion} | cut -d'.' -f3)
# This allows pkg_release to have configurable %%{?dist} tag
%define specrelease %{pkgrelease}%{?buildid}%{?variantid}%{?dist}
# This defines the kabi tarball version
%define kabiversion %{specversion}
%global src_hash 00000000000000000000000000000000

# If this variable is set to 1, a bpf selftests build failure will cause a
# fatal kernel package build error
%define selftests_must_build 0

#
# End of genspec.sh variables
#

%define pkg_release %{specrelease}

%global tkg 0
%global post_factum 1

%global opensuse_id a2ed3b547600e8f01fb4b40b4b623835d9672199
%global tkg_id 3ccc607fb2ab85af03711898954c6216ae7303fd

%global ark_url https://gitlab.com/cki-project/kernel-ark/-/commit
%global kernel_url https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/patch
%global pf_url https://codeberg.org/pf-kernel/linux/commit
%global tkg_url https://github.com/Frogging-Family/linux-tkg/raw/%{tkg_id}/linux-tkg-patches

# libexec dir is not used by the linker, so the shared object there
# should not be exported to RPM provides
%global __provides_exclude_from ^%{_libexecdir}/kselftests

# The following build options are (mostly) enabled by default, but may become
# enabled/disabled by later architecture-specific checks.
# Where disabled by default, they can be enabled by using --with <opt> in the
# rpmbuild command, or by forcing these values to 1.
# Where enabled by default, they can be disabled by using --without <opt> in
# the rpmbuild command, or by forcing these values to 0.
#
# standard kernel
%define with_up        %{?_without_up:0} %{?!_without_up:1}
# build the base variants
%define with_base      %{?_without_base:0} %{?!_without_base:1}
# build also debug variants
%define with_debug     %{?_without_debug:0} %{?!_without_debug:1}
%define with_debug     0
# kernel-zfcpdump (s390 specific kernel for zfcpdump)
%define with_zfcpdump  %{?_without_zfcpdump:0} %{?!_without_zfcpdump:1}
# kernel-16k (aarch64 kernel with 16K page_size)
%define with_arm64_16k %{?_with_arm64_16k: 0} %{?!_with_arm64_16k: 1}
# kernel-64k (aarch64 kernel with 64K page_size)
%define with_arm64_64k %{?_without_arm64_64k:0} %{?!_without_arm64_64k:1}
# kernel-rt (x86_64 and aarch64 only PREEMPT_RT enabled kernel)
%define with_realtime  %{?_with_realtime:1} %{?!_with_realtime:0}

# Supported variants
#            with_base with_debug    with_gcov
# up         X         X             X
# zfcpdump   X                       X
# arm64_16k  X         X             X
# arm64_64k  X         X             X
# realtime   X         X             X

# kernel-doc
%define with_doc       %{?_without_doc:0} %{?!_without_doc:1}
# kernel-headers
%define with_headers   %{?_without_headers:0} %{?!_without_headers:1}
%define with_cross_headers   %{?_without_cross_headers:0} %{?!_without_cross_headers:1}
# perf
%define with_perf      %{?_without_perf:0} %{?!_without_perf:1}
# libperf
%define with_libperf   %{?_without_libperf:0} %{?!_without_libperf:1}
# tools
%define with_tools     %{?_without_tools:0} %{?!_without_tools:1}
# bpftool
%define with_bpftool   %{?_without_bpftool:0} %{?!_without_bpftool:1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo:0} %{?!_without_debuginfo:1}
# kernel-abi-stablelists
%define with_kernel_abi_stablelists %{?_without_kernel_abi_whitelists:0} %{?!_without_kernel_abi_whitelists:1}
%define with_kernel_abi_stablelists 0
# internal samples and selftests
%define with_selftests %{?_without_selftests:0} %{?!_without_selftests:1}
#
# Additional options for user-friendly one-off kernel building:
#
# Only build the base kernel (--with baseonly):
%define with_baseonly  %{?_with_baseonly:1} %{?!_with_baseonly:0}
# Only build the debug variants (--with dbgonly):
%define with_dbgonly   %{?_with_dbgonly:1} %{?!_with_dbgonly:0}
%define with_dbgonly   0
# Only build the realtime kernel (--with rtonly):
%define with_rtonly    %{?_with_rtonly:1} %{?!_with_rtonly:0}
# Control whether we perform a compat. check against published ABI.
%define with_kabichk   %{?_without_kabichk:0} %{?!_without_kabichk:1}
# Temporarily disable kabi checks until RC.
%define with_kabichk 0
# Control whether we perform a compat. check against DUP ABI.
%define with_kabidupchk %{?_with_kabidupchk:1} %{?!_with_kabidupchk:0}
#
# Control whether to run an extensive DWARF based kABI check.
# Note that this option needs to have baseline setup in SOURCE300.
%define with_kabidwchk %{?_without_kabidwchk:0} %{?!_without_kabidwchk:1}
%define with_kabidw_base %{?_with_kabidw_base:1} %{?!_with_kabidw_base:0}
#
# Control whether to install the vdso directories.
%define with_vdso_install %{?_without_vdso_install:0} %{?!_without_vdso_install:1}
#
# should we do C=1 builds with sparse
%define with_sparse    %{?_with_sparse:1} %{?!_with_sparse:0}
#
# Cross compile requested?
%define with_cross    %{?_with_cross:1} %{?!_with_cross:0}
#
# build a release kernel on rawhide
%define with_release   %{?_with_release:1} %{?!_with_release:0}

# verbose build, i.e. no silent rules and V=1
%define with_verbose %{?_with_verbose:1} %{?!_with_verbose:0}

#
# check for mismatched config options
%define with_configchecks %{?_without_configchecks:0} %{?!_without_configchecks:1}

#
# gcov support
%define with_gcov %{?_with_gcov:1}%{?!_with_gcov:0}

#
# ipa_clone support
%define with_ipaclones %{?_without_ipaclones:0} %{?!_without_ipaclones:1}

# Want to build a vanilla kernel build without any non-upstream patches?
%define with_vanilla %{?_with_vanilla:1} %{?!_with_vanilla:0}

%ifarch x86_64 aarch64
%define with_efiuki %{?_without_efiuki:0} %{?!_without_efiuki:1}
%else
%define with_efiuki 0
%endif

### CPU optimizations
### with native take precedence, next is generic, then one set in kernel-local-cpu
# Use kernel-local-cpu-native (CONFIG_MNATIVE=y)
%global with_native  %{?_with_native:1} %{?!_with_native:0}

# Use kernel-local-cpu-generic (CONFIG_GENERIC_CPU=y)
%global with_generic %{?_with_generic:1} %{?!_with_generic:0}

%if 0%{?fedora}
# Kernel headers are being split out into a separate package
%define with_headers 0
%define with_cross_headers 0
# no ipa_clone for now
%define with_ipaclones 0
# no stablelist
%define with_kernel_abi_stablelists 0
# No realtime fedora variants
%define with_realtime 0
%define with_arm64_64k 0
%endif

%if %{with_verbose}
%define make_opts V=1
%else
%define make_opts -s
%endif

%if %{with toolchain_clang}
%ifarch s390x ppc64le
%global llvm_ias 0
%else
%global llvm_ias 1
%endif
%global clang_make_opts HOSTCC=clang CC=clang LLVM_IAS=%{llvm_ias}
%if %{with clang_lto}
%global clang_make_opts %{clang_make_opts} LD=ld.lld HOSTLD=ld.lld AR=llvm-ar NM=llvm-nm HOSTAR=llvm-ar HOSTNM=llvm-nm
%endif
%global make_opts %{make_opts} %{clang_make_opts}
# clang does not support the -fdump-ipa-clones option
%global with_ipaclones 0
%endif

# turn off debug kernel and kabichk for gcov builds
%if %{with_gcov}
%define with_debug 0
%define with_kabichk 0
%define with_kabidupchk 0
%define with_kabidwchk 0
%define with_kabidw_base 0
%define with_kernel_abi_stablelists 0
%endif

# turn off kABI DWARF-based check if we're generating the base dataset
%if %{with_kabidw_base}
%define with_kabidwchk 0
%endif

# kpatch_kcflags are extra compiler flags applied to base kernel
# -fdump-ipa-clones is enabled only for base kernels on selected arches
%if %{with_ipaclones}
%ifarch x86_64 ppc64le
%define kpatch_kcflags -fdump-ipa-clones
%else
%define with_ipaclones 0
%endif
%endif

%define make_target bzImage
%define image_install_path boot

%define KVERREL %{specversion}-%{release}.%{_target_cpu}
%define KVERREL_RE %(echo %KVERREL | sed 's/+/[+]/g')
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if 0%{!?nopatches:1}
%define nopatches 0
%endif

%if %{with_vanilla}
%define nopatches 1
%endif

%if %{with_release}
%define debugbuildsenabled 1
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug
# Needed because we override almost everything involving build-ids
# and debuginfo generation. Currently we rely on the old alldebug setting.
%global _build_id_links alldebug

# if requested, only build base kernel
%if %{with_baseonly}
%define with_debug 0
%define with_realtime 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_bpftool 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_cross 0
%define with_cross_headers 0
%define with_ipaclones 0
%endif

# if requested, only build debug kernel
%if %{with_dbgonly}
%define with_base 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_bpftool 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_ipaclones 0
%endif

# if requested, only build realtime kernel
%if %{with_rtonly}
%define with_realtime 1
%define with_up 0
%define with_debug 0
%define with_debuginfo 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_bpftool 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_cross 0
%define with_cross_headers 0
%define with_ipaclones 0
%define with_headers 0
%define with_efiuki 0
%define with_zfcpdump 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%endif

# RT kernel is only built on x86_64 and aarch64
%ifnarch x86_64 aarch64
%define with_realtime 0
%endif

# turn off kABI DUP check and DWARF-based check if kABI check is disabled
%if !%{with_kabichk}
%define with_kabidupchk 0
%define with_kabidwchk 0
%endif

%if %{with_vdso_install}
%define use_vdso 1
%endif

# selftests require bpftool to be built.  If bpftools is disabled, then disable selftests
%if %{with_bpftool} == 0
%define with_selftests 0
%endif

%ifnarch noarch
%define with_kernel_abi_stablelists 0
%endif

# Overrides for generic default options

# only package docs noarch
%ifnarch noarch
%define with_doc 0
%define doc_build_fail true
%endif

%if 0%{?fedora}
# don't do debug builds on anything but aarch64 and x86_64
%ifnarch aarch64 x86_64
%define with_debug 0
%endif
%endif

%define all_configs %{name}-%{specrpmversion}-*.config

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_up 0
%define with_realtime 0
%define with_headers 0
%define with_cross_headers 0
%define with_tools 0
%define with_perf 0
%define with_libperf 0
%define with_bpftool 0
%define with_selftests 0
%define with_debug 0
%endif

# sparse blows up on ppc
%ifnarch ppc64le
%define with_sparse 0
%endif

# zfcpdump mechanism is s390 only
%ifnarch s390x
%define with_zfcpdump 0
%endif

# 16k and 64k variants only for aarch64
%ifnarch aarch64
%define with_arm64_16k 0
%define with_arm64_64k 0
%endif

%if 0%{?fedora}
# This is not for Fedora
%define with_zfcpdump 0
%endif

# Per-arch tweaks

%ifarch i686
%define asmarch x86
%define hdrarch i386
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch ppc64le
%define asmarch powerpc
%define hdrarch powerpc
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%define use_vdso 0
%endif

%ifarch s390x
%define asmarch s390
%define hdrarch s390
%define kernel_image arch/s390/boot/bzImage
%define vmlinux_decompressor arch/s390/boot/vmlinux
%endif

%ifarch aarch64
%define asmarch arm64
%define hdrarch arm64
%define make_target vmlinuz.efi
%define kernel_image arch/arm64/boot/vmlinuz.efi
%endif

# Should make listnewconfig fail if there's config options
# printed out?
%if %{nopatches}
%define with_configchecks 0
%endif

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We only build kernel-headers on the following...
%if 0%{?fedora}
%define nobuildarches i386
%else
%define nobuildarches i386 i686
%endif

%ifarch %nobuildarches
# disable BuildKernel commands
%define with_up 0
%define with_debug 0
%define with_zfcpdump 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_realtime 0

%define with_debuginfo 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_bpftool 0
%define with_selftests 0
%define _enable_debug_packages 0
%endif

# Architectures we build tools/cpupower on
%if 0%{?fedora}
%define cpupowerarchs %{ix86} x86_64 ppc64le aarch64
%else
%define cpupowerarchs i686 x86_64 ppc64le aarch64
%endif

%if 0%{?use_vdso}
%define _use_vdso 1
%else
%define _use_vdso 0
%endif

# If build of debug packages is disabled, we need to know if we want to create
# meta debug packages or not, after we define with_debug for all specific cases
# above. So this must be at the end here, after all cases of with_debug or not.
%define with_debug_meta 0
%if !%{debugbuildsenabled}
%if %{with_debug}
%define with_debug_meta 1
%endif
%define with_debug 0
%endif

# short-hand for "are we building base/non-debug variants of ...?"
%if %{with_up} && %{with_base}
%define with_up_base 1
%else
%define with_up_base 0
%endif
%if %{with_realtime} && %{with_base}
%define with_realtime_base 1
%else
%define with_realtime_base 0
%endif
%if %{with_arm64_16k} && %{with_base}
%define with_arm64_16k_base 1
%else
%define with_arm64_16k_base 0
%endif
%if %{with_arm64_64k} && %{with_base}
%define with_arm64_64k_base 1
%else
%define with_arm64_64k_base 0
%endif

#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  coreutils, systemd >= 203-2, /usr/bin/kernel-install
%define initrd_prereq  dracut >= 027


Name: %{package_name}
License: ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-2-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR CDDL-1.0) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND ((GPL-2.0-only WITH Linux-syscall-note) OR MIT) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR MIT) AND BSD-2-Clause AND BSD-3-Clause AND BSD-3-Clause-Clear AND GFDL-1.1-no-invariants-or-later AND GPL-1.0-or-later AND (GPL-1.0-or-later OR BSD-3-Clause) AND (GPL-1.0-or-later WITH Linux-syscall-note) AND GPL-2.0-only AND (GPL-2.0-only OR Apache-2.0) AND (GPL-2.0-only OR BSD-2-Clause) AND (GPL-2.0-only OR BSD-3-Clause) AND (GPL-2.0-only OR CDDL-1.0) AND (GPL-2.0-only OR GFDL-1.1-no-invariants-or-later) AND (GPL-2.0-only OR GFDL-1.2-no-invariants-only) AND (GPL-2.0-only WITH Linux-syscall-note) AND GPL-2.0-or-later AND (GPL-2.0-or-later OR BSD-2-Clause) AND (GPL-2.0-or-later OR BSD-3-Clause) AND (GPL-2.0-or-later OR CC-BY-4.0) AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND ISC AND LGPL-2.0-or-later AND (LGPL-2.0-or-later OR BSD-2-Clause) AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND LGPL-2.1-only AND (LGPL-2.1-only OR BSD-2-Clause) AND (LGPL-2.1-only WITH Linux-syscall-note) AND LGPL-2.1-or-later AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND (Linux-OpenIB OR GPL-2.0-only) AND (Linux-OpenIB OR GPL-2.0-only OR BSD-2-Clause) AND Linux-man-pages-copyleft AND MIT AND (MIT OR Apache-2.0) AND (MIT OR GPL-2.0-only) AND (MIT OR GPL-2.0-or-later) AND (MIT OR LGPL-2.1-only) AND (MPL-1.1 OR GPL-2.0-only) AND (X11 OR GPL-2.0-only) AND (X11 OR GPL-2.0-or-later) AND Zlib AND (copyleft-next-0.3.1 OR GPL-2.0-or-later)
URL: https://www.kernel.org/
Version: %{specrpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
%if 0%{?fedora}
ExclusiveArch: noarch x86_64 s390x aarch64 ppc64le
%else
ExclusiveArch: noarch i386 i686 x86_64 s390x aarch64 ppc64le
%endif
ExclusiveOS: Linux
%ifnarch %{nobuildarches}
Requires: kernel-core-uname-r = %{KVERREL}
Requires: kernel-modules-uname-r = %{KVERREL}
Requires: kernel-modules-core-uname-r = %{KVERREL}
Provides: installonlypkg(kernel)
%endif


#
# List the packages used during the kernel build
#
BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk, %compression
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3-devel
BuildRequires: kernel-rpm-macros
# glibc-static is required for a consistent build environment (specifically
# CONFIG_CC_CAN_LINK_STATIC=y).
BuildRequires: glibc-static
%if %{with_headers}
BuildRequires: rsync
%endif
%if %{with_doc}
BuildRequires: xmlto, asciidoc, python3-sphinx, python3-sphinx_rtd_theme, python3-pyyaml
%endif
%if %{with_sparse}
BuildRequires: sparse
%endif
%if %{with_perf}
BuildRequires: zlib-devel binutils-devel newt-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel python3-setuptools
BuildRequires: java-devel
BuildRequires: libbpf-devel >= 0.6.0-1
BuildRequires: libbabeltrace-devel
BuildRequires: libtraceevent-devel
%ifnarch s390x
BuildRequires: numactl-devel
%endif
%ifarch aarch64
BuildRequires: opencsd-devel >= 1.0.0
%endif
%endif
%if %{with_tools}
BuildRequires: python3-docutils
BuildRequires: gettext ncurses-devel
BuildRequires: libcap-devel libcap-ng-devel
# The following are rtla requirements
BuildRequires: python3-docutils
BuildRequires: libtraceevent-devel
BuildRequires: libtracefs-devel

%ifnarch s390x
BuildRequires: pciutils-devel
%endif
%ifarch i686 x86_64
BuildRequires: libnl3-devel
%endif
%endif
%if %{with_tools} || %{signmodules} || %{signkernel}
BuildRequires: openssl-devel
%endif
%if %{with_bpftool}
BuildRequires: python3-docutils
BuildRequires: zlib-devel binutils-devel
%endif
%if %{with_selftests}
BuildRequires: clang llvm-devel fuse-devel
%ifarch x86_64
BuildRequires: lld
%endif
BuildRequires: libcap-devel libcap-ng-devel rsync libmnl-devel
BuildRequires: numactl-devel
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
BuildConflicts: rpm < 4.13.0.1-19
BuildConflicts: dwarves < 1.13
# Most of these should be enabled after more investigation
%undefine _include_minidebuginfo
%undefine _find_debuginfo_dwz_opts
%undefine _unique_build_ids
%undefine _unique_debug_names
%undefine _unique_debug_srcs
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

# Remove -q option below to provide 'extracting debug info' messages
%global _find_debuginfo_opts -r -q

%global _missing_build_ids_terminate_build 1
%global _no_recompute_build_ids 1
%endif
%if %{with_kabidwchk} || %{with_kabidw_base}
BuildRequires: kabi-dw
%endif

%if %{signkernel}%{signmodules}
BuildRequires: openssl
%if %{signkernel}
# ELN uses Fedora signing process, so exclude
%if 0%{?rhel}%{?centos} && !0%{?eln}
BuildRequires: system-sb-certs
%endif
%ifarch x86_64 aarch64
BuildRequires: nss-tools
BuildRequires: pesign >= 0.10-4
%endif
%endif
%endif

%if %{with_cross}
BuildRequires: binutils-%{_build_arch}-linux-gnu, gcc-%{_build_arch}-linux-gnu
%define cross_opts CROSS_COMPILE=%{_build_arch}-linux-gnu-
%define __strip %{_build_arch}-linux-gnu-strip
%endif

# These below are required to build man pages
%if %{with_perf}
BuildRequires: xmlto
%endif
%if %{with_perf} || %{with_tools}
BuildRequires: asciidoc
%endif

%if %{with toolchain_clang}
BuildRequires: clang
%endif

%if %{with clang_lto}
BuildRequires: llvm
BuildRequires: lld
%endif

%if %{with_efiuki}
BuildRequires: dracut
# For dracut UEFI uki binaries
BuildRequires: binutils
# For the initrd
BuildRequires: lvm2
BuildRequires: systemd-boot-unsigned
# For systemd-stub and systemd-pcrphase
BuildRequires: systemd-udev >= 252-1
# For TPM operations in UKI initramfs
BuildRequires: tpm2-tools
%endif

%if 0%{?released_kernel}
Source0: https://cdn.kernel.org/pub/linux/kernel/v%{kversion}.x/linux-%{tarfile_release}.tar.xz
%else
Source0: https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms-kernel/%{name}/linux-%{tarfile_release}.tar.xz/%{src_hash}/linux-%{tarfile_release}.tar.xz
%endif

Source1: Makefile.rhelver


# Name of the packaged file containing signing key
%ifarch ppc64le
%define signing_key_filename kernel-signing-ppc.cer
%endif
%ifarch s390x
%define signing_key_filename kernel-signing-s390.cer
%endif

%if %{?released_kernel}

Source10: redhatsecurebootca5.cer
Source11: redhatsecurebootca1.cer
Source12: redhatsecureboot501.cer
Source13: redhatsecureboot301.cer
Source14: secureboot_s390.cer
Source15: secureboot_ppc.cer

%define secureboot_ca_0 %{SOURCE10}
%define secureboot_ca_1 %{SOURCE11}
%ifarch x86_64 aarch64
%define secureboot_key_0 %{SOURCE12}
%define pesign_name_0 redhatsecureboot501
%define secureboot_key_1 %{SOURCE13}
%define pesign_name_1 redhatsecureboot301
%endif
%ifarch s390x
%define secureboot_key_0 %{SOURCE14}
%define pesign_name_0 redhatsecureboot302
%endif
%ifarch ppc64le
%define secureboot_key_0 %{SOURCE15}
%define pesign_name_0 redhatsecureboot303
%endif

# released_kernel
%else

Source10: redhatsecurebootca4.cer
Source11: redhatsecurebootca2.cer
Source12: redhatsecureboot401.cer
Source13: redhatsecureboot003.cer

%define secureboot_ca_0 %{SOURCE10}
%define secureboot_ca_1 %{SOURCE11}
%define secureboot_key_0 %{SOURCE12}
%define pesign_name_0 redhatsecureboot401
%define secureboot_key_1 %{SOURCE13}
%define pesign_name_1 redhatsecureboot003

# released_kernel
%endif

Source20: mod-denylist.sh
Source21: mod-sign.sh

%define modsign_cmd %{SOURCE21}

%if 0%{?include_rhel}
Source23: x509.genkey.rhel

Source24: %{name}-aarch64-rhel.config
Source25: %{name}-aarch64-debug-rhel.config
Source26: mod-extra.list.rhel

Source27: %{name}-ppc64le-rhel.config
Source28: %{name}-ppc64le-debug-rhel.config
Source29: %{name}-s390x-rhel.config
Source30: %{name}-s390x-debug-rhel.config
Source31: %{name}-s390x-zfcpdump-rhel.config
Source32: %{name}-x86_64-rhel.config
Source33: %{name}-x86_64-debug-rhel.config

Source34: filter-x86_64.sh.rhel
Source35: filter-aarch64.sh.rhel
Source36: filter-ppc64le.sh.rhel
Source37: filter-s390x.sh.rhel
Source38: filter-modules.sh.rhel

Source41: x509.genkey.centos
# ARM64 64K page-size kernel config
Source42: %{name}-aarch64-64k-rhel.config
Source43: %{name}-aarch64-64k-debug-rhel.config
%endif

%if 0%{?include_fedora}
Source50: x509.genkey.fedora
Source51: mod-extra.list.fedora

Source52: %{name}-aarch64-fedora.config
Source53: %{name}-aarch64-debug-fedora.config
Source54: %{name}-aarch64-16k-fedora.config
Source55: %{name}-aarch64-16k-debug-fedora.config
Source56: %{name}-ppc64le-fedora.config
Source57: %{name}-ppc64le-debug-fedora.config
Source58: %{name}-s390x-fedora.config
Source59: %{name}-s390x-debug-fedora.config
Source60: %{name}-x86_64-fedora.config
Source61: %{name}-x86_64-debug-fedora.config

Source62: filter-x86_64.sh.fedora
Source63: filter-aarch64.sh.fedora
Source64: filter-ppc64le.sh.fedora
Source65: filter-s390x.sh.fedora
Source66: filter-modules.sh.fedora
%endif

Source70: partial-kgcov-snip.config
Source71: partial-kgcov-debug-snip.config
Source72: partial-clang-snip.config
Source73: partial-clang-debug-snip.config
Source74: partial-clang_lto-x86_64-snip.config
Source75: partial-clang_lto-x86_64-debug-snip.config
Source76: partial-clang_lto-aarch64-snip.config
Source77: partial-clang_lto-aarch64-debug-snip.config
Source80: generate_all_configs.sh
Source81: process_configs.sh

Source84: mod-internal.list
Source85: mod-partner.list

Source86: dracut-virt.conf

Source87: flavors

Source100: rheldup3.x509
Source101: rhelkpatch1.x509
Source102: nvidiagpuoot001.x509

Source200: check-kabi

Source201: Module.kabi_aarch64
Source202: Module.kabi_ppc64le
Source203: Module.kabi_s390x
Source204: Module.kabi_x86_64

Source210: Module.kabi_dup_aarch64
Source211: Module.kabi_dup_ppc64le
Source212: Module.kabi_dup_s390x
Source213: Module.kabi_dup_x86_64


%if %{with_kernel_abi_stablelists}
Source300: kernel-abi-stablelists-%{kabiversion}.tar.xz
%endif
%if %{with_kabidw_base}
Source301: kernel-kabi-dw-%{kabiversion}.tar.xz
%endif

# RT specific virt module
Source400: mod-kvm.list

%if %{include_rt}
# realtime config files
Source474: %{name}-aarch64-rt-rhel.config
Source475: %{name}-aarch64-rt-debug-rhel.config
Source476: %{name}-x86_64-rt-rhel.config
Source477: %{name}-x86_64-rt-debug-rhel.config
%endif

# Sources for kernel-tools
Source2002: kvm_stat.logrotate

# Some people enjoy building customized kernels from the dist-git in Fedora and
# use this to override configuration options. One day they may all use the
# source tree, but in the mean time we carry this to support the legacy workflow
Source3000: merge.py
Source3001: kernel-local
%if 0%{patchlist_changelog}
Source3002: Patchlist.changelog
%endif

# This file is intentionally left empty in the stock kernel. Its a nicety
# added for those wanting to do custom rebuilds with altered config opts.
Source3011: kernel-local-cpu
Source3012: kernel-local-cpu-native
Source3013: kernel-local-pf
Source3014: kernel-local-cpu-generic

Source4000: README.rst
Source4001: rpminspect.yaml
Source4002: gating.yaml

# Here should be only the patches up to the upstream canonical Linus tree.

# For a stable release kernel
%if 0%{?stable_update} && 0%{?released_kernel}
%define    stable_patch_00  patch-%{specversion}.xz
Patch5000: https://cdn.kernel.org/pub/linux/kernel/v%{kversion}.x/%{stable_patch_00}
%endif

## Patches needed for building this package

## compile fixes

%if !%{nopatches}

Patch1: patch-%{patchversion}-redhat.patch

# empty final patch to facilitate testing of kernel patches
Patch999999: linux-kernel-test.patch

### Extra

### openSUSE patches - http://kernel.opensuse.org/cgit/kernel-source/

%global opensuse_url https://github.com/openSUSE/kernel-source/raw/%{opensuse_id}/patches.suse

Patch1010: %{opensuse_url}/vfs-add-super_operations-get_inode_dev#/openSUSE-vfs-add-super_operations-get_inode_dev.patch
Patch1011: %{opensuse_url}/btrfs-provide-super_operations-get_inode_dev#/openSUSE-btrfs-provide-super_operations-get_inode_dev.patch
Patch1012: %{opensuse_url}/btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch#/openSUSE-btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch
Patch1013: %{opensuse_url}/scsi-retry-alua-transition-in-progress#/openSUSE-scsi-retry-alua-transition-in-progress.patch

%global patchwork_url https://patchwork.kernel.org/patch
%global patchwork_xdg_url https://patchwork.freedesktop.org/patch
# https://patchwork.kernel.org/patch/10045863
Patch2000: radeon_dp_aux_transfer_native-74-callbacks-suppressed.patch

%if 0%{?tkg}
Patch2090: %{tkg_url}/%{patchversion}/0001-mm-Support-soft-dirty-flag-reset-for-VA-range.patch#/tkg-0001-mm-Support-soft-dirty-flag-reset-for-VA-range.patch
Patch2091: %{tkg_url}/%{patchversion}/0002-mm-Support-soft-dirty-flag-read-with-reset.patch#/tkg-0002-mm-Support-soft-dirty-flag-read-with-reset.patch
%endif

# Add additional cpu gcc optimization support
# https://github.com/graysky2/kernel_gcc_patch
%global graysky2_id c409515574bd4d69af45ad74d4e7ba7151010516
Patch6000: https://github.com/graysky2/kernel_compiler_patch/raw/%{graysky2_id}/more-uarches-for-kernel-6.8-rc4+.patch

Patch6010: 0001-block-elevator-default-blk-mq-to-bfq.patch

%if 0%{?post_factum}
# amd-pstate
Patch7001:  %{pf_url}/641e7552801c73818653ee50d6913f48245b856a.patch#/pf-cb-641e755.patch
Patch7002:  %{pf_url}/c5c351d3e348bc9be9e70d5758bd31defb03cc1d.patch#/pf-cb-c5c351d.patch
Patch7003:  %{pf_url}/ca5d8e68074f82ddebce83e03a80092d76308c6e.patch#/pf-cb-ca5d8e6.patch
Patch7004:  %{pf_url}/cc6f40b5f1d5037d99185b9d6db44eb44647b31a.patch#/pf-cb-cc6f40b.patch
Patch7005:  %{pf_url}/09c29d7bfa5ba2af29142715ba510df7600055b5.patch#/pf-cb-09c29d7.patch
Patch7006:  %{pf_url}/dee082f6177b353eff3350f48836f8f107cb44f8.patch#/pf-cb-dee082f.patch
Patch7007:  %{pf_url}/1d20d933b45e2a14c886548cc51841bbd45f10c1.patch#/pf-cb-1d20d93.patch
Patch7008:  %{pf_url}/7de6e958046bd8611e7054e0d6756e41add9aaf6.patch#/pf-cb-7de6e95.patch
Patch7009:  %{pf_url}/08cfb0e23d892b043aac2b972bb1cae423a98a3d.patch#/pf-cb-08cfb0e.patch
Patch7010:  %{pf_url}/5553679999685998f44243f007dfa8d9b645f92f.patch#/pf-cb-5553679.patch
Patch7011:  %{pf_url}/99507dc09f53c4b975cbe0e1b4b79a42ad47c8e4.patch#/pf-cb-99507dc.patch
Patch7012:  %{pf_url}/91132f11a605caf5211e93e32f06bb841bc61f6e.patch#/pf-cb-91132f1.patch
Patch7013:  %{pf_url}/16470f705c25e9f606286fc2313f3f011b48031d.patch#/pf-cb-16470f7.patch
Patch7014:  %{pf_url}/6f97d23a475a6298e145d28fd03082646c641be6.patch#/pf-cb-6f97d23.patch
Patch7015:  %{pf_url}/35f6eb6acba76baf46cbce9a908006ec763ab1c7.patch#/pf-cb-35f6eb6.patch
Patch7016:  %{pf_url}/cdce4abbb2968a438c0afb9c2d280eaa8109cf6f.patch#/pf-cb-cdce4ab.patch
Patch7017:  %{pf_url}/c8a44230ae99b7c541bc5a658c64d5f1146c45ce.patch#/pf-cb-c8a4423.patch
Patch7018:  %{pf_url}/dc33c5dbd381f342986d86b8c926c3ab757feafb.patch#/pf-cb-dc33c5d.patch
Patch7019:  %{pf_url}/9ff16d889879eea21c1b37f14e9f1fffd6d36071.patch#/pf-cb-9ff16d8.patch
Patch7020:  %{pf_url}/12e71a0895d14e9febd86fbd08b9914fea0d5e1f.patch#/pf-cb-12e71a0.patch
Patch7021:  %{pf_url}/09ad896945849fda14294735f5fef1411647908c.patch#/pf-cb-09ad896.patch
Patch7022:  %{pf_url}/86a4b05c7af435840a36d64d0356f73fbcfd363d.patch#/pf-cb-86a4b05.patch
Patch7023:  %{pf_url}/e390850be93cd4715f3babf163a011ac6c516380.patch#/pf-cb-e390850.patch
Patch7024:  %{pf_url}/9379bbed75a9f025515bb4e65dd9f7b61c141d16.patch#/pf-cb-9379bbe.patch
Patch7025:  %{pf_url}/dd56ba85f39d7ab1a7441a9eeb6b2327bb273f3a.patch#/pf-cb-dd56ba8.patch
Patch7026:  %{pf_url}/ac420ace1abc6c32aa5d142d2a9b553c4dec4df5.patch#/pf-cb-ac420ac.patch
Patch7027:  %{pf_url}/0bfd4a370e74645a0c6f3234facedc326580c9da.patch#/pf-cb-0bfd4a3.patch
Patch7028:  %{pf_url}/942c2d1ad1b5e0418870e3ed48c419321dac0630.patch#/pf-cb-942c2d1.patch
Patch7029:  %{pf_url}/3ea966004c2526cec388bf5e1918bfe774d8fb0f.patch#/pf-cb-3ea9660.patch
Patch7030:  %{pf_url}/a12286fa8a17e639044441f13647328e2c54a6ae.patch#/pf-cb-a12286f.patch
Patch7031:  %{pf_url}/bc3acabad847d3d3eca6f425093cbbf8f5f822d5.patch#/pf-cb-bc3acab.patch
Patch7032:  %{pf_url}/eafeaa077ea6356ff27144d61c74701f8fd0228d.patch#/pf-cb-eafeaa0.patch

# bbr
Patch7050:  %{pf_url}/7dd5db3e5182e5728c3fdd859d2c713335ee706a.patch#/pf-cb-7dd5db3.patch
# block
Patch7060:  %{pf_url}/e66b22c22de9257bc2c0b34326d258887a347399.patch#/pf-cb-e66b22c.patch
Patch7061:  %{pf_url}/6f98e2059e1902621baa67892148f5eac44a3978.patch#/pf-cb-6f98e20.patch
Patch7062:  %{pf_url}/46f44d5389ca3d2c8dfd7dcb3f961ab20ea914ad.patch#/pf-cb-46f44d5.patch
Patch7063:  %{pf_url}/458f213da09e768b427d7d8891bf6967f2b6e6c0.patch#/pf-cb-458f213.patch
Patch7064:  %{pf_url}/832f3d248d4d1809d0ae50065e989d2e2cf7fde3.patch#/pf-cb-832f3d2.patch
Patch7065:  %{pf_url}/1626c25ee395eab7d4f42ffda6d463bc9eaf151c.patch#/pf-cb-1626c25.patch
Patch7066:  %{pf_url}/c3c3ce96305c3374dd65dcd75e1f22998c17d7c0.patch#/pf-cb-c3c3ce9.patch
Patch7067:  %{pf_url}/d0504b7a470b4f7b1a4e71efe601adabf084f750.patch#/pf-cb-d0504b7.patch
# fixes
Patch7100:  %{pf_url}/9e943ab3c8bb617187aa696eeae5781c81e8050a.patch#/pf-cb-9e943ab.patch
Patch7101:  %{pf_url}/95f6f5d9133ed95da262ff8265ba2694b19ec2e1.patch#/pf-cb-95f6f5d.patch
Patch7102:  %{pf_url}/a218b3f2736576ba62646b1bab43edaedf9e3b70.patch#/pf-cb-a218b3f.patch
Patch7103:  %{pf_url}/79516fb573458d0bb8da5abca6edba4a48e4107a.patch#/pf-cb-79516fb.patch
Patch7105:  %{pf_url}/0f0b8ed975348b61d233d3ce0c65faaf85c1f582.patch#/pf-cb-0f0b8ed.patch
Patch7106:  %{pf_url}/50f3726f3c3ad06ae2249d216d4205e84062a4a5.patch#/pf-cb-50f3726.patch
Patch7107:  %{pf_url}/6b51f821467bf1d5234cf63b7f60ae3b606058ef.patch#/pf-cb-6b51f82.patch
Patch7108:  %{pf_url}/147fa7036b8e48e49ce88f4d4425a245c4980f46.patch#/pf-cb-147fa70.patch
Patch7109:  %{pf_url}/d5a2c4281133eb7c56285dc7444f5054d59f9259.patch#/pf-cb-d5a2c42.patch
Patch7110:  %{pf_url}/82262734c84a25000a96186bf12c495a179c5b0f.patch#/pf-cb-8226273.patch
# zstd
Patch7200:  %{pf_url}/1b8b450e0a8b6c07229f9ae7e03fbc31e5b14d7f.patch#/pf-cb-1b8b450.patch
Patch7201:  %{pf_url}/ef8fac5ecb019624f2e38cdcdb7e697873bc96e1.patch#/pf-cb-ef8fac5.patch
Patch7202:  %{pf_url}/5b59dc7236c3f4bdeb85755f1f8f81ae7545b08d.patch#/pf-cb-5b59dc7.patch
Patch7203:  %{pf_url}/9089fe4e2cb3eff89d5ad359ddcbe811a4f7af1e.patch#/pf-cb-9089fe4.patch
Patch7204:  %{pf_url}/d885d3e38500529e4df2425d206608c5cd37757c.patch#/pf-cb-d885d3e.patch
Patch7205:  %{pf_url}/91377d4a7c106b3cb98bcb674a8f4e86467ae8cb.patch#/pf-cb-91377d4.patch
Patch7206:  %{pf_url}/2216eeb4d869c393f81212145b775725fcaf9e39.patch#/pf-cb-2216eeb.patch
# ksm
Patch7220:  %{pf_url}/8d4a931c41533999c0c3a4ae4655705a65631444.patch#/pf-cb-8d4a931.patch
# v4l2loopback
Patch7230:  %{pf_url}/519ac3f772453b98143d71da4b13db626788bf7f.patch#/pf-cb-519ac3f.patch
Patch7231:  %{pf_url}/e8c31c140e168d77d52ec7290d2080d1f2dc5498.patch#/pf-cb-e8c31c1.patch
# uvcvideo
Patch7240:  %{pf_url}/07015936767a820784b39794cbad773f97e8e2f7.patch#/pf-cb-0701593.patch
Patch7241:  %{pf_url}/79c792bdfc1f2ad46d4e3a8364ff7a23ecc2bd71.patch#/pf-cb-79c792b.patch
Patch7242:  %{pf_url}/b23f715cb965b1b54a9e2dc3f88c9ef4421d58c2.patch#/pf-cb-b23f715.patch
Patch7243:  %{pf_url}/01916c357477bae685d2331d578a327393aa9dee.patch#/pf-cb-01916c3.patch
Patch7244:  %{pf_url}/d9e2c4fbda630a1503715619950f4b172975f290.patch#/pf-cb-d9e2c4f.patch
Patch7245:  %{pf_url}/5bf14c6c85ac73bfd1fd01d11337e4f8cc2de1ca.patch#/pf-cb-5bf14c6.patch
Patch7246:  %{pf_url}/884a61751d979ee9974c08a71c72e88e73bdd87e.patch#/pf-cb-884a617.patch
# aes-xts
Patch7300:  %{pf_url}/e3e25e3ad3c60ae55c0c1e8318c84b91926eb7d8.patch#/pf-cb-e3e25e3.patch
Patch7301:  %{pf_url}/c27cefb53314e868c51ea32a11e8ef26c6ccdd9e.patch#/pf-cb-c27cefb.patch
Patch7302:  %{pf_url}/ee7386a28acb97ea2229e3fad6268a6cb0ed2112.patch#/pf-cb-ee7386a.patch
Patch7303:  %{pf_url}/984e45d04d5f5d19520f2817c91155894facfca7.patch#/pf-cb-984e45d.patch
Patch7304:  %{pf_url}/703d558ecb5373cd079bfd9dd0c7f3f4d4f46ccf.patch#/pf-cb-703d558.patch
Patch7305:  %{pf_url}/5b597d0f4b148eef949a54055da95ef44e4247d0.patch#/pf-cb-5b597d0.patch
Patch7306:  %{pf_url}/68afbbe7595f8fbda4b610f3e64a1b71d54f0a9a.patch#/pf-cb-68afbbe.patch
Patch7307:  %{pf_url}/87aae2841a8f1ca5be684914746b76c47bc03e1c.patch#/pf-cb-87aae28.patch
Patch7308:  %{pf_url}/a12d00e2a783991513774f21e23c2724bfe5bd95.patch#/pf-cb-a12d00e.patch
Patch7309:  %{pf_url}/51a5ce39e960e659e146cdb9c05662b660a5bdd6.patch#/pf-cb-51a5ce3.patch
Patch7310:  %{pf_url}/5c5a0e684e41381dacff5ecb8590b3cc3b4bfe60.patch#/pf-cb-5c5a0e6.patch
Patch7311:  %{pf_url}/a38fa2dbd0079972ad3807ef315f3b324f9cfa85.patch#/pf-cb-a38fa2d.patch
Patch7312:  %{pf_url}/83cfebbe9ea9c65e5983a932ab9dc5c6d6c610e0.patch#/pf-cb-83cfebb.patch
Patch7313:  %{pf_url}/a16b17a1e14cf6ddba6c036f2d59dc392c33fbcf.patch#/pf-cb-a16b17a.patch
Patch7314:  %{pf_url}/6d032ba8824f28e4dbb0c43b0dd47dfb7067795b.patch#/pf-cb-6d032ba.patch
Patch7315:  %{pf_url}/a0a37b16a97db57aebd0c5935a6b333029403890.patch#/pf-cb-a0a37b1.patch
Patch7316:  %{pf_url}/c2f4dc5836ec304caa229a2c054b93b890d4ff6e.patch#/pf-cb-c2f4dc5.patch
Patch7317:  %{pf_url}/8832b4473470f70d14c9d6534234de50a95f3f1a.patch#/pf-cb-8832b44.patch
Patch7318:  %{pf_url}/b3ab662d27ff006898d2b982537205d51ed24263.patch#/pf-cb-b3ab662.patch
Patch7319:  %{pf_url}/b1c075117f9379a5a31405f5b13d716810b7c6db.patch#/pf-cb-b1c0751.patch
Patch7320:  %{pf_url}/0785a849e46f66328efe02280f588b7417c13c9f.patch#/pf-cb-0785a84.patch

%endif

# END OF PATCH DEFINITIONS

%endif


%description
The kernel meta package

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#    %%kernel_reqprovconf [-o] <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
#
%define kernel_reqprovconf(o) \
%if %{-o:0}%{!-o:1}\
Provides: %{name} = %{specversion}-%{pkg_release}\
%endif\
Provides: %{name}-%{_target_cpu} = %{specrpmversion}-%{pkg_release}%{uname_suffix %{?1:+%{1}}}\
Provides: kernel-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(pre): ((linux-firmware >= 20150904-56.git6ebf5d57) if linux-firmware)\
Recommends: linux-firmware\
Requires(preun): systemd >= 200\
Conflicts: xfsprogs < 4.3.0-1\
Conflicts: xorg-x11-drv-vmmouse < 13.0.99\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}


%package doc
Summary: Various documentation bits found in the kernel source
Group: Documentation
%description doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.


%package headers
Summary: Header files for the Linux kernel for use by glibc
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if 0%{?gemini}
Obsoletes: kernel-headers < %{specversion}-%{release}
Provides: %{name}-headers = %{specversion}-%{release}
%endif
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc
%if 0%{?gemini}
Provides: kernel-cross-headers = %{specversion}-%{release}
Obsoletes: kernel-cross-headers < %{specversion}
%endif
%description cross-headers
Kernel-cross-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
cross-glibc package.


%package debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by %{name}-debuginfo packages
Provides: installonlypkg(kernel)
%description debuginfo-common-%{_target_cpu}
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.

%if %{with_perf}
%package -n perf
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Performance monitoring for the Linux kernel
Requires: bzip2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%package -n perf-debuginfo
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Debug information for package perf
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{specrpmversion}-%{release}
AutoReqProv: no
%description -n perf-debuginfo
This package provides debug information for the perf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_bindir}/perf(\.debug)?|.*%%{_libexecdir}/perf-core/.*|.*%%{_libdir}/libperf-jvmti.so(\.debug)?|XXX' -o perf-debuginfo.list}

%package -n python3-perf
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Python bindings for apps which will manipulate perf events
%description -n python3-perf
The python3-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.

%package -n python3-perf-debuginfo
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Debug information for package perf python bindings
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{specrpmversion}-%{release}
AutoReqProv: no
%description -n python3-perf-debuginfo
This package provides debug information for the perf python bindings.

# the python_sitearch macro should already be defined from above
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{python3_sitearch}/perf.*so(\.debug)?|XXX' -o python3-perf-debuginfo.list}

# with_perf
%endif

%if %{with_libperf}
%package -n libperf
Summary: The perf library from kernel source
%description -n libperf
This package contains the kernel source perf library.

%package -n libperf-devel
Summary: Developement files for the perf library from kernel source
%description -n libperf-devel
This package includes libraries and header files needed for development
of applications which use perf library from kernel source.

%package -n libperf-debuginfo
Summary: Debug information for package libperf
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n libperf-debuginfo
This package provides debug information for the libperf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_libdir}/libperf.so(\.debug)?|XXX' -o libperf-debuginfo.list}
# with_libperf
%endif

%if %{with_tools}
%package -n kernel-tools
Summary: Assortment of tools for the Linux kernel
%ifarch %{cpupowerarchs}
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: kernel-tools-libs = %{specrpmversion}-%{release}
%endif
%define __requires_exclude ^%{_bindir}/python
%description -n kernel-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package -n kernel-tools-libs
Summary: Libraries for the kernels-tools
%description -n kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package -n kernel-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
Requires: kernel-tools = %{version}-%{release}
%ifarch %{cpupowerarchs}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
%endif
Requires: kernel-tools-libs = %{version}-%{release}
Provides: kernel-tools-devel
%description -n kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package -n kernel-tools-debuginfo
Summary: Debug information for package kernel-tools
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n kernel-tools-debuginfo
This package provides debug information for package kernel-tools.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|.*%%{_bindir}/turbostat(\.debug)?|.*%%{_bindir}/x86_energy_perf_policy(\.debug)?|.*%%{_bindir}/tmon(\.debug)?|.*%%{_bindir}/lsgpio(\.debug)?|.*%%{_bindir}/gpio-hammer(\.debug)?|.*%%{_bindir}/gpio-event-mon(\.debug)?|.*%%{_bindir}/gpio-watch(\.debug)?|.*%%{_bindir}/iio_event_monitor(\.debug)?|.*%%{_bindir}/iio_generic_buffer(\.debug)?|.*%%{_bindir}/lsiio(\.debug)?|.*%%{_bindir}/intel-speed-select(\.debug)?|.*%%{_bindir}/page_owner_sort(\.debug)?|.*%%{_bindir}/slabinfo(\.debug)?|.*%%{_sbindir}/intel_sdsi(\.debug)?|XXX' -o kernel-tools-debuginfo.list}

%package -n rtla
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Real-Time Linux Analysis tools
Requires: libtraceevent
Requires: libtracefs
%description -n rtla
The rtla meta-tool includes a set of commands that aims to analyze
the real-time properties of Linux. Instead of testing Linux as a black box,
rtla leverages kernel tracing capabilities to provide precise information
about the properties and root causes of unexpected results.

%package -n rv
Summary: RV: Runtime Verification
%description -n rv
Runtime Verification (RV) is a lightweight (yet rigorous) method that
complements classical exhaustive verification techniques (such as model
checking and theorem proving) with a more practical approach for
complex systems.
The rv tool is the interface for a collection of monitors that aim
analysing the logical and timing behavior of Linux.

# with_tools
%endif

%if %{with_bpftool}

%if 0%{?fedora}
# bpftoolverion doesn't bump with stable updates so let's stick with
# upstream kernel version for the package name. We still get correct
# output with bpftool -V.
%define bpftoolversion  %specrpmversion
%else
%define bpftoolversion 7.4.0
%endif

%package -n bpftool
Summary: Inspection and simple manipulation of eBPF programs and maps
Version: %{bpftoolversion}
%description -n bpftool
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%package -n bpftool-debuginfo
Summary: Debug information for package bpftool
Version: %{bpftoolversion}
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{specrpmversion}-%{release}
AutoReqProv: no
%description -n bpftool-debuginfo
This package provides debug information for the bpftool package.

%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_sbindir}/bpftool(\.debug)?|XXX' -o bpftool-debuginfo.list}

# Setting "Version:" above overrides the internal {version} macro,
# need to restore it here
%define version %{specrpmversion}

# with_bpftool
%endif

%if %{with_selftests}

%package selftests-internal
Summary: Kernel samples and selftests
Requires: binutils, bpftool, iproute-tc, nmap-ncat, python3, fuse-libs, keyutils
%description selftests-internal
Kernel sample programs and selftests.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_libexecdir}/(ksamples|kselftests)/.*|XXX' -o selftests-debuginfo.list}

%define __requires_exclude ^liburandom_read.so.*$

# with_selftests
%endif

%define kernel_gcov_package() \
%package %{?1:%{1}-}gcov\
Summary: gcov graph and source files for coverage data collection.\
%description %{?1:%{1}-}gcov\
%{?1:%{1}-}gcov includes the gcov graph and source files for gcov coverage collection.\
%{nil}

%package -n %{name}-abi-stablelists
Summary: The Red Hat Enterprise Linux kernel ABI symbol stablelists
AutoReqProv: no
%description -n %{name}-abi-stablelists
The kABI package contains information pertaining to the Red Hat Enterprise
Linux kernel ABI, including lists of kernel symbols that are needed by
external Linux kernel modules, and a yum plugin to aid enforcement.

%if %{with_kabidw_base}
%package kernel-kabidw-base-internal
Summary: The baseline dataset for kABI verification using DWARF data
Group: System Environment/Kernel
AutoReqProv: no
%description kernel-kabidw-base-internal
The package contains data describing the current ABI of the Red Hat Enterprise
Linux kernel, suitable for the kabi-dw tool.
%endif

#
# This macro creates a kernel-<subpackage>-debuginfo package.
#    %%kernel_debuginfo_package <subpackage>
#
# Explanation of the find_debuginfo_opts: We build multiple kernels (debug,
# rt, 64k etc.) so the regex filters those kernels appropriately. We also
# have to package several binaries as part of kernel-devel but getting
# unique build-ids is tricky for these userspace binaries. We don't really
# care about debugging those so we just filter those out and remove it.
%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
%description %{?1:%{1}-}debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} --keep-section '.BTF' -p '.*\/usr\/src\/kernels/.*|XXX' -o ignored-debuginfo.list -p '/.*/%%{KVERREL_RE}%{?1:[+]%{1}}/.*|/.*%%{KVERREL_RE}%{?1:\+%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#    %%kernel_devel_package [-m] <subpackage> <pretty-name>
#
%define kernel_devel_package(m) \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Provides: %{name}%{?1:-%{1}}-devel-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}-devel-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
Requires(pre): findutils\
Requires: findutils\
Requires: perl-interpreter\
Requires: openssl-devel\
Requires: elfutils-libelf-devel\
Requires: bison\
Requires: flex\
Requires: make\
Requires: gcc\
%if %{-m:1}%{!-m:0}\
Requires: kernel-devel-uname-r = %{KVERREL}%{uname_variant %{?1:%{1}}}\
%endif\
Suggests: duperemove\
Suggests: hardlink\
%description %{?1:%{1}-}devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates an empty kernel-<subpackage>-devel-matched package that
# requires both the core and devel packages locked on the same version.
#	%%kernel_devel_matched_package [-m] <subpackage> <pretty-name>
#
%define kernel_devel_matched_package(m) \
%package %{?1:%{1}-}devel-matched\
Summary: Meta package to install matching core and devel packages for a given %{?2:%{2} }kernel\
Requires: %{name}%{?1:-%{1}}-devel = %{specrpmversion}-%{release}\
Requires: %{name}%{?1:-%{1}}-core = %{specrpmversion}-%{release}\
%description %{?1:%{1}-}devel-matched\
This meta package is used to install matching core and devel packages for a given %{?2:%{2} }kernel.\
%{nil}

#
# kernel-<variant>-ipaclones-internal package
#
%define kernel_ipaclones_package() \
%package %{?1:%{1}-}ipaclones-internal\
Summary: *.ipa-clones files generated by -fdump-ipa-clones for kernel%{?1:-%{1}}\
Group: System Environment/Kernel\
AutoReqProv: no\
%description %{?1:%{1}-}ipaclones-internal\
This package provides *.ipa-clones files.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-internal package.
#    %%kernel_modules_internal_package <subpackage> <pretty-name>
#
%define kernel_modules_internal_package() \
%package %{?1:%{1}-}modules-internal\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: %{name}%{?1:-%{1}}-modules-internal-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-modules-internal-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: %{name}%{?1:-%{1}}-modules-internal = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-internal-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-internal\
This package provides kernel modules for the %{?2:%{2} }kernel package for Red Hat internal usage.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-extra package.
#    %%kernel_modules_extra_package [-m] <subpackage> <pretty-name>
#
%define kernel_modules_extra_package(m) \
%package %{?1:%{1}-}modules-extra\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Provides: %{name}%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: %{name}%{?1:-%{1}}-modules-extra = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-extra-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
%if %{-m:1}%{!-m:0}\
Requires: kernel-modules-extra-uname-r = %{KVERREL}%{uname_variant %{?1:+%{1}}}\
%endif\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-extra\
This package provides less commonly used kernel modules for the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules package.
#    %%kernel_modules_package [-m] <subpackage> <pretty-name>
#
%define kernel_modules_package(m) \
%package %{?1:%{1}-}modules\
Summary: kernel modules to match the %{?2:%{2}-}core kernel\
Provides: %{name}%{?1:-%{1}}-modules-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}-modules-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: %{name}-modules = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
%if %{-m:1}%{!-m:0}\
Requires: kernel-modules-uname-r = %{KVERREL}%{uname_variant %{?1:+%{1}}}\
%endif\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules\
This package provides commonly used kernel modules for the %{?2:%{2}-}core kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-core package.
#	%%kernel_modules_core_package [-m] <subpackage> <pretty-name>
#
%define kernel_modules_core_package(m) \
%package %{?1:%{1}-}modules-core\
Summary: Core kernel modules to match the %{?2:%{2}-}core kernel\
Provides: %{name}%{?1:-%{1}}-modules-core-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}-modules-core-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: %{name}-modules-core = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
%if %{-m:1}%{!-m:0}\
Requires: kernel-modules-core-uname-r = %{KVERREL}%{uname_variant %{?1:+%{1}}}\
%endif\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-core\
This package provides essential kernel modules for the %{?2:%{2}-}core kernel package.\
%{nil}

#
# this macro creates a kernel-<subpackage> meta package.
#    %%kernel_meta_package <subpackage>
#
%define kernel_meta_package() \
%package %{1}\
summary: kernel meta-package for the %{1} kernel\
Requires: kernel-%{1}-core-uname-r = %{KVERREL}+%{uname_suffix %{1}}\
Requires: kernel-%{1}-modules-uname-r = %{KVERREL}+%{uname_suffix %{1}}\
Requires: kernel-%{1}-modules-core-uname-r = %{KVERREL}+%{uname_suffix %{1}}\
%if "%{1}" == "rt" || "%{1}" == "rt-debug"\
Requires: realtime-setup\
%endif\
Provides: installonlypkg(kernel)\
%description %{1}\
The meta-package for the %{1} kernel\
%{nil}

%if %{with_realtime}
#
# this macro creates a kernel-rt-<subpackage>-kvm package
# %%kernel_kvm_package <subpackage>
#
%define kernel_kvm_package() \
%package %{?1:%{1}-}kvm\
Summary: KVM modules for package kernel%{?1:-%{1}}\
Group: System Environment/Kernel\
Requires: kernel%{?1:-%{1}} = %{version}-%{release}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-kvm-%{_target_cpu} = %{version}-%{release}\
AutoReq: no\
%description -n kernel%{?1:-%{1}}-kvm\
This package provides KVM modules for package kernel%{?1:-%{1}}.\
%{nil}
%endif

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#    %%define variant_summary The Linux kernel compiled for <configuration>
#    %%kernel_variant_package [-n <pretty-name>] [-m] [-o] <subpackage>
#
%define kernel_variant_package(n:mo) \
%package %{?1:%{1}-}core\
Summary: %{variant_summary}\
Provides: kernel-%{?1:%{1}-}core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Provides: installonlypkg(kernel)\
%if %{-m:1}%{!-m:0}\
Requires: kernel-core-uname-r = %{KVERREL}%{uname_variant %{?1:+%{1}}}\
Requires: kernel-%{?1:%{1}-}-modules-core-uname-r = %{KVERREL}%{uname_variant %{?1:+%{1}}}\
%endif\
%{expand:%%kernel_reqprovconf %{?1:%{1}} %{-o:%{-o}}}\
%if %{?1:1} %{!?1:0} \
%{expand:%%kernel_meta_package %{?1:%{1}}}\
%endif\
%{expand:%%kernel_devel_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_devel_matched_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_modules_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_modules_core_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_modules_extra_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%if %{-m:0}%{!-m:1}\
%{expand:%%kernel_modules_internal_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%if 0%{!?fedora:1}\
%{expand:%%kernel_modules_partner_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%endif\
%{expand:%%kernel_debuginfo_package %{?1:%{1}}}\
%endif\
%if "%{1}" == "rt" || "%{1}" == "rt-debug"\
%{expand:%%kernel_kvm_package %{?1:%{1}}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%else \
%if %{with_efiuki}\
%package %{?1:%{1}-}uki-virt\
Summary: %{variant_summary} unified kernel image for virtual machines\
Provides: installonlypkg(kernel)\
Provides: kernel-%{?1:%{1}-}uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): systemd >= 254-1\
%endif\
%endif\
%if %{with_gcov}\
%{expand:%%kernel_gcov_package %{?1:%{1}}}\
%endif\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-partner package.
#	%%kernel_modules_partner_package <subpackage> <pretty-name>
#
%define kernel_modules_partner_package() \
%package %{?1:%{1}-}modules-partner\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: %{name}%{?1:-%{1}}-modules-partner-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-modules-partner-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: %{name}%{?1:-%{1}}-modules-partner = %{specrpmversion}-%{release}%{uname_suffix %{?1:+%{1}}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-partner-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
Requires: kernel%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1:+%{1}}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-partner\
This package provides kernel modules for the %{?2:%{2} }kernel package for Red Hat partners usage.\
%{nil}

# Now, each variant package.

%if %{with_zfcpdump}
%define variant_summary The Linux kernel compiled for zfcpdump usage
%kernel_variant_package -o zfcpdump
%description zfcpdump-core
The kernel package contains the Linux kernel (vmlinuz) for use by the
zfcpdump infrastructure.
# with_zfcpdump
%endif

%if %{with_arm64_16k_base}
%define variant_summary The Linux kernel compiled for 16k pagesize usage
%kernel_variant_package 16k
%description 16k-core
The kernel package contains a variant of the ARM64 Linux kernel using
a 16K page size.
%endif

%if %{with_arm64_16k} && %{with_debug}
%define variant_summary The Linux kernel compiled with extra debugging enabled
%if !%{debugbuildsenabled}
%kernel_variant_package -m 16k-debug
%else
%kernel_variant_package 16k-debug
%endif
%description 16k-debug-core
The debug kernel package contains a variant of the ARM64 Linux kernel using
a 16K page size.
This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_arm64_64k_base}
%define variant_summary The Linux kernel compiled for 64k pagesize usage
%kernel_variant_package 64k
%description 64k-core
The kernel package contains a variant of the ARM64 Linux kernel using
a 64K page size.
%endif

%if %{with_arm64_64k} && %{with_debug}
%define variant_summary The Linux kernel compiled with extra debugging enabled
%if !%{debugbuildsenabled}
%kernel_variant_package -m 64k-debug
%else
%kernel_variant_package 64k-debug
%endif
%description 64k-debug-core
The debug kernel package contains a variant of the ARM64 Linux kernel using
a 64K page size.
This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_debug} && %{with_realtime}
%define variant_summary The Linux PREEMPT_RT kernel compiled with extra debugging enabled
%kernel_variant_package rt-debug
%description rt-debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_realtime_base}
%define variant_summary The Linux kernel compiled with PREEMPT_RT enabled
%kernel_variant_package rt
%description rt-core
This package includes a version of the Linux kernel compiled with the
PREEMPT_RT real-time preemption support
%endif

%if %{with_up} && %{with_debug}
%if !%{debugbuildsenabled}
%kernel_variant_package -m debug
%else
%kernel_variant_package debug
%endif
%description debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_up_base}
# And finally the main -core package

%define variant_summary The Linux kernel
%kernel_variant_package
%description core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.
%endif

%if %{with_up} && %{with_debug} && %{with_efiuki}
%description debug-uki-virt
Prebuilt debug unified kernel image for virtual machines.
%endif

%if %{with_up_base} && %{with_efiuki}
%description uki-virt
Prebuilt default unified kernel image for virtual machines.
%endif

%if %{with_arm64_16k} && %{with_debug} && %{with_efiuki}
%description 16k-debug-uki-virt
Prebuilt 16k debug unified kernel image for virtual machines.
%endif

%if %{with_arm64_16k_base} && %{with_efiuki}
%description 16k-uki-virt
Prebuilt 16k unified kernel image for virtual machines.
%endif

%if %{with_arm64_64k} && %{with_debug} && %{with_efiuki}
%description 64k-debug-uki-virt
Prebuilt 64k debug unified kernel image for virtual machines.
%endif

%if %{with_arm64_64k_base} && %{with_efiuki}
%description 64k-uki-virt
Prebuilt 64k unified kernel image for virtual machines.
%endif

%if %{with_ipaclones}
%kernel_ipaclones_package
%endif

%prep
# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_up}
echo "Cannot build --with baseonly, up build is disabled"
exit 1
%endif
%endif

# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      echo "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"
      exit 1
    fi
  done
fi 2>/dev/null

patch_command='git --work-tree=. apply'
ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f "$patch" ]; then
    exit 1
  fi
  case "$patch" in
  *.bz2) bunzip2 < "$patch" | $patch_command ${1+"$@"} ;;
  *.gz)  gunzip  < "$patch" | $patch_command ${1+"$@"} ;;
  *.xz)  unxz    < "$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$patch" ;;
  esac
}

# don't apply patch if it's empty
ApplyOptionalPatch()
{
  local patch=$1
  shift
  if [ ! -f "$patch" ]; then
    exit 1
  fi
  local C=$(wc -l "$patch" | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch "$patch" ${1+"$@"}
  fi
}

%setup -q -n kernel-%{tarfile_release} -c
mv linux-%{tarfile_release} linux-%{KVERREL}

cd linux-%{KVERREL}
cp -a %{SOURCE1} .

%if 0%{?post_factum}
# amd-pstate
ApplyPatch %{PATCH7001}
ApplyPatch %{PATCH7002}
ApplyPatch %{PATCH7003}
ApplyPatch %{PATCH7004}
ApplyPatch %{PATCH7005}
ApplyPatch %{PATCH7006}
ApplyPatch %{PATCH7007}
ApplyPatch %{PATCH7008}
ApplyPatch %{PATCH7009}
ApplyPatch %{PATCH7010}
ApplyPatch %{PATCH7011}
ApplyPatch %{PATCH7012}
ApplyPatch %{PATCH7013}
ApplyPatch %{PATCH7014}
ApplyPatch %{PATCH7015}
ApplyPatch %{PATCH7016}
ApplyPatch %{PATCH7017}
ApplyPatch %{PATCH7018}
ApplyPatch %{PATCH7019}
ApplyPatch %{PATCH7020}
ApplyPatch %{PATCH7021}
ApplyPatch %{PATCH7022}
ApplyPatch %{PATCH7023}
ApplyPatch %{PATCH7024}
ApplyPatch %{PATCH7025}
ApplyPatch %{PATCH7026}
ApplyPatch %{PATCH7027}
ApplyPatch %{PATCH7028}
ApplyPatch %{PATCH7029}
ApplyPatch %{PATCH7030}
ApplyPatch %{PATCH7031}
ApplyPatch %{PATCH7032}
# bbr
ApplyPatch %{PATCH7050}
# block
ApplyPatch %{PATCH7060}
ApplyPatch %{PATCH7061}
ApplyPatch %{PATCH7062}
ApplyPatch %{PATCH7063}
ApplyPatch %{PATCH7064}
ApplyPatch %{PATCH7065}
ApplyPatch %{PATCH7066}
ApplyPatch %{PATCH7067}
# fixes
ApplyPatch %{PATCH7100}
ApplyPatch %{PATCH7101}
ApplyPatch %{PATCH7102}
ApplyPatch %{PATCH7103}
ApplyPatch %{PATCH7105}
ApplyPatch %{PATCH7109}
ApplyPatch %{PATCH7110}
# zstd
ApplyPatch %{PATCH7200}
ApplyPatch %{PATCH7201}
ApplyPatch %{PATCH7202}
ApplyPatch %{PATCH7203}
ApplyPatch %{PATCH7204}
ApplyPatch %{PATCH7205}
ApplyPatch %{PATCH7206}
# ksm
ApplyPatch %{PATCH7220}
# v4l2loopback
ApplyPatch %{PATCH7230}
ApplyPatch %{PATCH7231}
# uvcvideo
ApplyPatch %{PATCH7240}
ApplyPatch %{PATCH7241}
ApplyPatch %{PATCH7242}
ApplyPatch %{PATCH7243}
ApplyPatch %{PATCH7244}
ApplyPatch %{PATCH7245}
ApplyPatch %{PATCH7246}
# aes-xts
ApplyPatch %{PATCH7300}
ApplyPatch %{PATCH7301}
ApplyPatch %{PATCH7302}
ApplyPatch %{PATCH7303}
ApplyPatch %{PATCH7304}
ApplyPatch %{PATCH7305}
ApplyPatch %{PATCH7306}
ApplyPatch %{PATCH7307}
ApplyPatch %{PATCH7308}
ApplyPatch %{PATCH7309}
ApplyPatch %{PATCH7310}
ApplyPatch %{PATCH7311}
ApplyPatch %{PATCH7312}
ApplyPatch %{PATCH7313}
ApplyPatch %{PATCH7314}
ApplyPatch %{PATCH7315}
ApplyPatch %{PATCH7316}
ApplyPatch %{PATCH7317}
ApplyPatch %{PATCH7318}
ApplyPatch %{PATCH7319}
ApplyPatch %{PATCH7320}
%endif

# released_kernel with possible stable updates
%if 0%{?stable_update} && 0%{?released_kernel}
# This is special because the kernel spec is hell and nothing is consistent
ApplyPatch %{PATCH5000}
%endif

%if 0%{?post_factum}
ApplyPatch %{PATCH7106}
ApplyPatch %{PATCH7107}
ApplyPatch %{PATCH7108}
%endif

%if !%{nopatches}
ApplyOptionalPatch %{PATCH1}

ApplyOptionalPatch %{PATCH999999}

# openSUSE
ApplyPatch %{PATCH1010}
ApplyPatch %{PATCH1011}
%dnl ApplyPatch %{PATCH1012}
ApplyPatch %{PATCH1013}

ApplyPatch %{PATCH2000}

%if 0%{?tkg}
ApplyPatch %{PATCH2090}
ApplyPatch %{PATCH2091}
%endif

ApplyPatch %{PATCH6000}

ApplyPatch %{PATCH6010}

# END OF PATCH APPLICATIONS

%endif

# Any further pre-build tree manipulations happen here.

chmod +x scripts/checkpatch.pl
mv COPYING COPYING-%{specrpmversion}-%{release}

# on linux-next prevent scripts/setlocalversion from mucking with our version numbers
rm -f localversion-next

# Mangle /usr/bin/python shebangs to /usr/bin/python3
# Mangle all Python shebangs to be Python 3 explicitly
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# This fixes errors such as
# *** ERROR: ambiguous python shebang in /usr/bin/kvm_stat: #!/usr/bin/python. Change it to python3 (or python2) explicitly.
# We patch all sources below for which we got a report/error.
echo "Fixing Python shebangs..."
%py3_shebang_fix \
    tools/kvm/kvm_stat/kvm_stat \
    scripts/show_delta \
    scripts/diffconfig \
    scripts/bloat-o-meter \
    scripts/jobserver-exec \
    tools \
    Documentation \
    scripts/clang-tools 2> /dev/null

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

if [ -L configs ]; then
    rm -f configs
fi
mkdir configs
cd configs

# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/%{name}-*.config .
cp %{SOURCE3001} .
%if %{with_native}
cat %{SOURCE3012} >> kernel-local
echo 'CONFIG_NR_CPUS=%(nproc --all)' >> kernel-local
%else
%if %{with_generic}
cat %{SOURCE3014} >> kernel-local
%else
cat %{SOURCE3011} >> kernel-local
%endif
%endif

%if 0%{?post_factum}
cat %{SOURCE3013} >> kernel-local
%endif
cp %{SOURCE80} .
# merge.py
cp %{SOURCE3000} .

# kernel-local - rename and copy for partial snippet config process
cp kernel-local partial-kernel-local-snip.config
cp kernel-local partial-kernel-local-debug-snip.config
rm -f kernel-local

FLAVOR=%{primary_target} SPECPACKAGE_NAME=%{name} SPECVERSION=%{specversion} SPECRPMVERSION=%{specrpmversion} ./generate_all_configs.sh %{debugbuildsenabled}

# Collect custom defined config options
PARTIAL_CONFIGS=""
%if %{with_gcov}
PARTIAL_CONFIGS="$PARTIAL_CONFIGS %{SOURCE70} %{SOURCE71}"
%endif
%if %{with toolchain_clang}
PARTIAL_CONFIGS="$PARTIAL_CONFIGS %{SOURCE72} %{SOURCE73}"
%endif
%if %{with clang_lto}
PARTIAL_CONFIGS="$PARTIAL_CONFIGS %{SOURCE74} %{SOURCE75} %{SOURCE76} %{SOURCE77}"
%endif
PARTIAL_CONFIGS="$PARTIAL_CONFIGS partial-kernel-local-snip.config partial-kernel-local-debug-snip.config"

GetArch()
{
  case "$1" in
  *aarch64*) echo "aarch64" ;;
  *ppc64le*) echo "ppc64le" ;;
  *s390x*) echo "s390x" ;;
  *x86_64*) echo "x86_64" ;;
  # no arch, apply everywhere
  *) echo "" ;;
  esac
}

# Merge in any user-provided local config option changes
%ifnarch %nobuildarches
for i in %{all_configs}
do
  kern_arch="$(GetArch $i)"
  kern_debug="$(echo $i | grep -q debug && echo "debug" || echo "")"

  for j in $PARTIAL_CONFIGS
  do
    part_arch="$(GetArch $j)"
    part_debug="$(echo $j | grep -q debug && echo "debug" || echo "")"

    # empty arch means apply to all arches
    if [ "$part_arch" == "" -o "$part_arch" == "$kern_arch" ] && [ "$part_debug" == "$kern_debug" ]
    then
      mv $i $i.tmp
      ./merge.py $j $i.tmp > $i
    fi
  done
  rm -f $i.tmp
done
%endif

# Add DUP and kpatch certificates to system trusted keys for RHEL
%if 0%{?rhel}
%if %{signkernel}%{signmodules}
openssl x509 -inform der -in %{SOURCE100} -out rheldup3.pem
openssl x509 -inform der -in %{SOURCE101} -out rhelkpatch1.pem
openssl x509 -inform der -in %{SOURCE102} -out nvidiagpuoot001.pem
cat rheldup3.pem rhelkpatch1.pem nvidiagpuoot001.pem > ../certs/rhel.pem
%ifarch s390x ppc64le
openssl x509 -inform der -in %{secureboot_ca_0} -out secureboot.pem
cat secureboot.pem >> ../certs/rhel.pem
%endif
for i in *.config; do
  sed -i 's@CONFIG_SYSTEM_TRUSTED_KEYS=""@CONFIG_SYSTEM_TRUSTED_KEYS="certs/rhel.pem"@' $i
done
%endif
%endif

# Adjust FIPS module name for RHEL
%if 0%{?rhel}
for i in *.config; do
  sed -i 's/CONFIG_CRYPTO_FIPS_NAME=.*/CONFIG_CRYPTO_FIPS_NAME="Red Hat Enterprise Linux %{rhel} - Kernel Cryptographic API"/' $i
done
%endif

cp %{SOURCE81} .
OPTS=""
%if %{with_configchecks}
    OPTS="$OPTS -w -n -c"
%endif
%if %{with clang_lto}
for opt in %{clang_make_opts}; do
  OPTS="$OPTS -m $opt"
done
%endif

RHJOBS=%{?_smp_build_ncpus} SPECPACKAGE_NAME=%{name} ./process_configs.sh $OPTS %{specrpmversion} %{primary_target}

# We may want to override files from the primary target in case of building
# against a flavour of it (eg. centos not rhel), thus override it here if
# necessary
update_scripts() {
	TARGET="$1"

	for i in "$RPM_SOURCE_DIR"/*."$TARGET"; do
		NEW=${i%."$TARGET"}
		cp "$i" "$(basename "$NEW")"
	done
}

update_target=%{primary_target}
if [ "%{primary_target}" == "rhel" ]; then
: # no-op to avoid empty if-fi error
%if 0%{?centos}
  update_scripts $update_target
  echo "Updating scripts/sources to centos version"
  update_target=centos
%endif
fi
update_scripts $update_target

# end of kernel config
%endif

cd ..
# # End of Configs stuff

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -delete >/dev/null

# remove unnecessary SCM files
find . -name .gitignore -delete >/dev/null

cd ..

###
### build
###
%build

rm -rf %{buildroot_unstripped} || true
mkdir -p %{buildroot_unstripped}

%if %{with_sparse}
%define sparse_mflags    C=1
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

# Note we need to disable these flags for cross builds because the flags
# from redhat-rpm-config assume that host == target so target arch
# flags cause issues with the host compiler.
%if !%{with_cross}
%define build_hostcflags  %{?build_cflags}
%define build_hostldflags %{?build_ldflags}
%endif

%define make %{__make} %{?cross_opts} %{?make_opts} HOSTCFLAGS="%{?build_hostcflags}" HOSTLDFLAGS="%{?build_hostldflags}"

InitBuildVars() {
    # Initialize the kernel .config file and create some variables that are
    # needed for the actual build process.

    Variant=$1

    # Pick the right kernel config file
    Config=%{name}-%{specrpmversion}-%{_target_cpu}${Variant:+-${Variant}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Variant:++${Variant}}

    KernelVer=%{specversion}-%{release}.%{_target_cpu}${Variant:++${Variant}}

    %if 0%{?stable_update}
    # make sure SUBLEVEL is incremented on a stable release.  Sigh 3.x.
    perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{?stable_update}/" Makefile
    %endif

    # make sure EXTRAVERSION says what we want it to say
    # Trim the release if this is a CI build, since KERNELVERSION is limited to 64 characters
    ShortRel=$(perl -e "print \"%{release}\" =~ s/\.pr\.[0-9A-Fa-f]{32}//r")
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -${ShortRel}.%{_target_cpu}${Variant:++${Variant}}/" Makefile

    # if pre-rc1 devel kernel, must fix up PATCHLEVEL for our versioning scheme
    # if we are post rc1 this should match anyway so this won't matter
    perl -p -i -e 's/^PATCHLEVEL.*/PATCHLEVEL = %{patchlevel}/' Makefile

    %{make} %{?_smp_mflags} mrproper
    cp configs/$Config .config

    %if %{signkernel}%{signmodules}
    cp configs/x509.genkey certs/.
    %endif

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    KCFLAGS="%{?kcflags}"

    # add kpatch flags for base kernel
    if [ "$Variant" == "" ]; then
        KCFLAGS="$KCFLAGS%{?kpatch_kcflags: %{kpatch_kcflags}}"
    fi
}

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    DoVDSO=$3
    Variant=$4
    InstallName=${5:-vmlinuz}

    DoModules=1
    if [ "$Variant" = "zfcpdump" ]; then
        DoModules=0
    fi

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

%if %{with_gcov}
    # Make build directory unique for each variant, so that gcno symlinks
    # are also unique for each variant.
    if [ -n "$Variant" ]; then
        ln -s $(pwd) ../linux-%{KVERREL}-${Variant}
    fi
    echo "GCOV - continuing build in: $(pwd)"
    pushd ../linux-%{KVERREL}${Variant:+-${Variant}}
    pwd > ../kernel${Variant:+-${Variant}}-gcov.list
%endif

    InitBuildVars $Variant

    echo BUILDING A KERNEL FOR ${Variant} %{_target_cpu}...

    %{make} ARCH=$Arch olddefconfig >/dev/null

    # This ensures build-ids are unique to allow parallel debuginfo
    perl -p -i -e "s/^CONFIG_BUILD_SALT.*/CONFIG_BUILD_SALT=\"%{KVERREL}\"/" .config
    %{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?kernel_mflags}
    if [ $DoModules -eq 1 ]; then
    %{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} modules %{?sparse_mflags} || exit 1
    fi

    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/systemtap
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif

%ifarch aarch64
    %{make} ARCH=$Arch dtbs INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    %{make} ARCH=$Arch dtbs_install INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    cp -r $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/dtb
    find arch/$Arch/boot/dts -name '*.dtb' -type f -delete
%endif

    # Remove large intermediate files we no longer need to save space
    # (-f required for zfcpdump builds that do not enable BTF)
    rm -f vmlinux.o .tmp_vmlinux.btf

    # Start installing the results
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/config
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/System.map

    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=20

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/lib/modules/$KernelVer/zImage.stub-$KernelVer || :
    fi

    %if %{signkernel}
    if [ "$KernelImage" = vmlinux ]; then
        # We can't strip and sign $KernelImage in place, because
        # we need to preserve original vmlinux for debuginfo.
        # Use a copy for signing.
        $CopyKernel $KernelImage $KernelImage.tosign
        KernelImage=$KernelImage.tosign
        CopyKernel=cp
    fi

    SignImage=$KernelImage

    %ifarch x86_64 aarch64
    %pesign -s -i $SignImage -o vmlinuz.tmp -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
    %pesign -s -i vmlinuz.tmp -o vmlinuz.signed -a %{secureboot_ca_1} -c %{secureboot_key_1} -n %{pesign_name_1}
    rm vmlinuz.tmp 
    %endif
    %ifarch s390x ppc64le
    if [ -x /usr/bin/rpm-sign ]; then
    rpm-sign --key "%{pesign_name_0}" --lkmsign $SignImage --output vmlinuz.signed
    elif [ $DoModules -eq 1 ]; then
    chmod +x scripts/sign-file
    ./scripts/sign-file -p sha256 certs/signing_key.pem certs/signing_key.x509 $SignImage vmlinuz.signed
    else
    mv $SignImage vmlinuz.signed
    fi
    %endif

    if [ ! -s vmlinuz.signed ]; then
        echo "pesigning failed"
        exit 1
    fi
    mv vmlinuz.signed $SignImage
    # signkernel
    %endif
    $CopyKernel $KernelImage \
                $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    cp $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/$InstallName

    # hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    (cd $RPM_BUILD_ROOT/%{image_install_path} && sha512hmac $InstallName-$KernelVer) > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;
    cp $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac $RPM_BUILD_ROOT/lib/modules/$KernelVer/.vmlinuz.hmac

    if [ $DoModules -eq 1 ]; then
    # Override $(mod-fw) because we don't want it to install any firmware
    # we'll get it from the linux-firmware package and we don't want conflicts
    %{make} %{?_smp_mflags} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=
    fi

%if %{with_gcov}
    # install gcov-needed files to $BUILDROOT/$BUILD/...:
    #   gcov_info->filename is absolute path
    #   gcno references to sources can use absolute paths (e.g. in out-of-tree builds)
    #   sysfs symlink targets (set up at compile time) use absolute paths to BUILD dir
    find . \( -name '*.gcno' -o -name '*.[chS]' \) -exec install -D '{}' "$RPM_BUILD_ROOT/$(pwd)/{}" \;
%endif

    # add an a noop %%defattr statement 'cause rpm doesn't like empty file list files
    echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-ldsoconf.list
    if [ $DoVDSO -ne 0 ]; then
        %{make} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
        if [ -s ldconfig-kernel.conf ]; then
             install -D -m 444 ldconfig-kernel.conf \
                $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
         echo /etc/ld.so.conf.d/kernel-$KernelVer.conf >> ../kernel${Variant:+-${Variant}}-ldsoconf.list
        fi

        rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/vdso/.build-id
    fi

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates
    # CONFIG_KERNEL_HEADER_TEST generates some extra files in the process of
    # testing so just delete
    find . -name *.h.s -delete
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ ! -e Module.symvers ]; then
        touch Module.symvers
    fi
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi

    # create the kABI metadata for use in packaging
    # NOTENOTE: the name symvers is used by the rpm backend
    # NOTENOTE: to discover and run the /usr/lib/rpm/fileattrs/kabi.attr
    # NOTENOTE: script which dynamically adds exported kernel symbol
    # NOTENOTE: checksums to the rpm metadata provides list.
    # NOTENOTE: if you change the symvers name, update the backend too
    echo "**** GENERATING kernel ABI metadata ****"
    %compression --stdout %compression_flags < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.%compext
    cp $RPM_BUILD_ROOT/boot/symvers-$KernelVer.%compext $RPM_BUILD_ROOT/lib/modules/$KernelVer/symvers.%compext

%if %{with_kabichk}
    echo "**** kABI checking is enabled in kernel SPEC file. ****"
    chmod 0755 $RPM_SOURCE_DIR/check-kabi
    if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Variant ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Variant $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
        echo "**** NOTE: Cannot find reference Module.kabi file. ****"
    fi
%endif

%if %{with_kabidupchk}
    echo "**** kABI DUP checking is enabled in kernel SPEC file. ****"
    if [ -e $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Variant ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Variant $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
        echo "**** NOTE: Cannot find DUP reference Module.kabi file. ****"
    fi
%endif

%if %{with_kabidw_base}
    # Don't build kabi base for debug kernels
    if [ "$Variant" != "zfcpdump" -a "$Variant" != "debug" ]; then
        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf
        tar -xvf %{SOURCE301} -C $RPM_BUILD_ROOT/kabi-dwarf

        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf/stablelists
        tar -xvf %{SOURCE300} -C $RPM_BUILD_ROOT/kabi-dwarf/stablelists

        echo "**** GENERATING DWARF-based kABI baseline dataset ****"
        chmod 0755 $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh
        $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh generate \
            "$RPM_BUILD_ROOT/kabi-dwarf/stablelists/kabi-current/kabi_stablelist_%{_target_cpu}" \
            "$(pwd)" \
            "$RPM_BUILD_ROOT/kabidw-base/%{_target_cpu}${Variant:+.${Variant}}" || :

        rm -rf $RPM_BUILD_ROOT/kabi-dwarf
    fi
%endif

%if %{with_kabidwchk}
    if [ "$Variant" != "zfcpdump" ]; then
        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf
        tar -xvf %{SOURCE301} -C $RPM_BUILD_ROOT/kabi-dwarf
        if [ -d "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}" ]; then
            mkdir -p $RPM_BUILD_ROOT/kabi-dwarf/stablelists
            tar -xvf %{SOURCE300} -C $RPM_BUILD_ROOT/kabi-dwarf/stablelists

            echo "**** GENERATING DWARF-based kABI dataset ****"
            chmod 0755 $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh generate \
                "$RPM_BUILD_ROOT/kabi-dwarf/stablelists/kabi-current/kabi_stablelist_%{_target_cpu}" \
                "$(pwd)" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}.tmp" || :

            echo "**** kABI DWARF-based comparison report ****"
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh compare \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}.tmp" || :
            echo "**** End of kABI DWARF-based comparison report ****"
        else
            echo "**** Baseline dataset for kABI DWARF-BASED comparison report not found ****"
        fi

        rm -rf $RPM_BUILD_ROOT/kabi-dwarf
    fi
%endif

    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/tracing
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/spdxcheck.py

%ifarch s390x
    # CONFIG_EXPOLINE_EXTERN=y produces arch/s390/lib/expoline/expoline.o
    # which is needed during external module build.
    if [ -f arch/s390/lib/expoline/expoline.o ]; then
      cp -a --parents arch/s390/lib/expoline/expoline.o $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
%endif

    # Files for 'make scripts' to succeed with kernel-devel.
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/security/selinux/include
    cp -a --parents security/selinux/include/classmap.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents security/selinux/include/initial_sid_to_string.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/include/tools
    cp -a --parents tools/include/tools/be_byteshift.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/tools/le_byteshift.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # Files for 'make prepare' to succeed with kernel-devel.
    cp -a --parents tools/include/linux/compiler* $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/linux/types.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/build/Build.include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/build/Build $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/build/fixdep.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/sync-check.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/bpf/resolve_btfids/main.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/bpf/resolve_btfids/Build $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    cp --parents security/selinux/include/policycap_names.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents security/selinux/include/policycap.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    cp -a --parents tools/include/asm-generic $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/linux $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/uapi/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/uapi/asm-generic $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/uapi/linux $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/vdso $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/scripts/utilities.mak $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/lib/subcmd $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/lib/*.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/*.[ch] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/Build $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/include/objtool/*.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/lib/bpf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/lib/bpf/Build $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    if [ -f tools/objtool/objtool ]; then
      cp -a tools/objtool/objtool $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
    fi
    if [ -f tools/objtool/fixdep ]; then
      cp -a tools/objtool/fixdep $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
    fi
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    if [ -f arch/%{asmarch}/kernel/module.lds ]; then
      cp -a --parents arch/%{asmarch}/kernel/module.lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +
%ifarch ppc64le
    cp -a --parents arch/powerpc/lib/crtsavres.[So] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
%ifarch aarch64
    # arch/arm64/include/asm/xen references arch/arm
    cp -a --parents arch/arm/include/asm/xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    # arch/arm64/include/asm/opcodes.h references arch/arm
    cp -a --parents arch/arm/include/asm/opcodes.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
%ifarch i686 x86_64
    # files for 'make prepare' to succeed with kernel-devel
    cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_32.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_64.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_common.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/purgatory.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/stack.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/setup-x86_64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/entry64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/ctype.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/

    cp -a --parents scripts/syscalltbl.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents scripts/syscallhdr.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/

    cp -a --parents tools/arch/x86/include/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/arch/x86/include/uapi/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/objtool/arch/x86/lib $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/arch/x86/lib/ $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/arch/x86/tools/gen-insn-attr-x86.awk $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/objtool/arch/x86/ $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

%endif
    # Clean up intermediate tools files
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +

    # Make sure the Makefile, version.h, and auto.conf have a matching
    # timestamp so that external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile \
        $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h \
        $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
    eu-readelf -n vmlinux | grep "Build ID" | awk '{print $NF}' > vmlinux.id
    cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id

    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    # (use mv + symlink instead of cp to reduce disk space requirements)
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    mv vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    ln -s $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux vmlinux
    if [ -n "%{vmlinux_decompressor}" ]; then
      eu-readelf -n  %{vmlinux_decompressor} | grep "Build ID" | awk '{print $NF}' > vmlinux.decompressor.id
      # Without build-id the build will fail. But for s390 the build-id
      # wasn't added before 5.11. In case it is missing prefer not
      # packaging the debuginfo over a build failure.
      if [ -s vmlinux.decompressor.id ]; then
        cp vmlinux.decompressor.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.decompressor.id
        cp %{vmlinux_decompressor} $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux.decompressor
      fi
    fi
%endif

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
        LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      if [ ! -z "$3" ]; then
        sed -r -e "/^($3)\$/d" -i $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      fi
    }

    collect_modules_list networking \
      'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
      'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
    collect_modules_list drm \
      'drm_open|drm_init'
    collect_modules_list modesetting \
      'drm_crtc_init'

    # detect missing or incorrect license tags
    ( find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name '*.ko' | xargs /sbin/modinfo -l | \
        grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1

    remove_depmod_files()
    {
        # remove files that will be auto generated by depmod at rpm -i time
        pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
            # in case below list needs to be extended, remember to add a
            # matching ghost entry in the files section as well
            rm -f modules.{alias,alias.bin,builtin.alias.bin,builtin.bin} \
                  modules.{dep,dep.bin,devname,softdep,symbols,symbols.bin}
        popd
    }

    remove_depmod_files

    # Identify modules in the kernel-modules-extras package
    %{SOURCE20} $RPM_BUILD_ROOT lib/modules/$KernelVer $(realpath configs/mod-extra.list)
    # Identify modules in the kernel-modules-internal package
    %{SOURCE20} $RPM_BUILD_ROOT lib/modules/$KernelVer %{SOURCE84} internal
%if 0%{!?fedora:1}
    # Identify modules in the kernel-modules-partner package
    %{SOURCE20} $RPM_BUILD_ROOT lib/modules/$KernelVer %{SOURCE85} partner
%endif
    if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" ]]; then
    # Identify modules in the kernel-rt-kvm package
        %{SOURCE20} $RPM_BUILD_ROOT lib/modules/$KernelVer %{SOURCE400} kvm
    fi

    #
    # Generate the kernel-core and kernel-modules files lists
    #

    # Copy the System.map file for depmod to use, and create a backup of the
    # full module tree so we can restore it after we're done filtering
    cp System.map $RPM_BUILD_ROOT/.
    cp configs/filter-*.sh $RPM_BUILD_ROOT/.
    pushd $RPM_BUILD_ROOT
    mkdir restore
    cp -r lib/modules/$KernelVer/* restore/.

    # don't include anything going into kernel-modules-extra in the file lists
    xargs rm -rf < mod-extra.list
    # don't include anything going into kernel-modules-internal in the file lists
    xargs rm -rf < mod-internal.list
%if 0%{!?fedora:1}
    # don't include anything going into kernel-modules-partner in the file lists
    xargs rm -rf < mod-partner.list
%endif
    if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" ]]; then
      # don't include anything going into kernel-rt-kvm in the file lists
      xargs rm -rf < mod-kvm.list
    fi

    if [ $DoModules -eq 1 ]; then
    # Find all the module files and filter them out into the core and
    # modules lists.  This actually removes anything going into -modules
    # from the dir.
    find lib/modules/$KernelVer/kernel -name *.ko | sort -n > modules.list
    ./filter-modules.sh modules.list %{_target_cpu}
    rm filter-*.sh

    # Run depmod on the resulting module tree and make sure it isn't broken
    depmod -b . -aeF ./System.map $KernelVer &> depmod.out
    if [ -s depmod.out ]; then
        echo "Depmod failure"
        cat depmod.out
        exit 1
    else
        rm depmod.out
    fi
    else
        # Ensure important files/directories exist to let the packaging succeed
        echo '%%defattr(-,-,-)' > modules.list
        echo '%%defattr(-,-,-)' > k-d.list
        mkdir -p lib/modules/$KernelVer/kernel
        # Add files usually created by make modules, needed to prevent errors
        # thrown by depmod during package installation
        touch lib/modules/$KernelVer/modules.order
        touch lib/modules/$KernelVer/modules.builtin
    fi

    if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" ]]; then
        echo "Skipping efiuki build"
    else
%if %{with_efiuki}
    popd

    KernelUnifiedImageDir="$RPM_BUILD_ROOT/lib/modules/$KernelVer"
    KernelUnifiedImage="$KernelUnifiedImageDir/$InstallName-virt.efi"

    mkdir -p $KernelUnifiedImageDir

    dracut --conf=%{SOURCE86} \
           --confdir=$(mktemp -d) \
           --verbose \
           --kver "$KernelVer" \
           --kmoddir "$RPM_BUILD_ROOT/lib/modules/$KernelVer/" \
           --logfile=$(mktemp) \
           --uefi \
           --kernel-image $(realpath $KernelImage) \
           --kernel-cmdline 'console=tty0 console=ttyS0' \
    $KernelUnifiedImage

%if %{signkernel}

    %pesign -s -i $KernelUnifiedImage -o $KernelUnifiedImage.tmp -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
    %pesign -s -i $KernelUnifiedImage.tmp -o $KernelUnifiedImage.signed -a %{secureboot_ca_1} -c %{secureboot_key_1} -n %{pesign_name_1}
    rm -f $KernelUnifiedImage.tmp

    if [ ! -s $KernelUnifiedImage.signed ]; then
      echo "pesigning failed"
      exit 1
    fi
    mv $KernelUnifiedImage.signed $KernelUnifiedImage

# signkernel
%endif

    pushd $RPM_BUILD_ROOT

# with_efiuki
%endif
    :  # in case of empty block
    fi # "$Variant" == "rt" || "$Variant" == "rt-debug"

    remove_depmod_files

    # Go back and find all of the various directories in the tree.  We use this
    # for the dir lists in kernel-core
    find lib/modules/$KernelVer/kernel -mindepth 1 -type d | sort -n > module-dirs.list

    # Cleanup
    rm System.map
    # Just "cp -r" can be very slow: here, it rewrites _existing files_
    # with open(O_TRUNC). Many filesystems synchronously wait for metadata
    # update for such file rewrites (seen in strace as final close syscall
    # taking a long time). On a rotational disk, cp was observed to take
    # more than 5 minutes on ext4 and more than 15 minutes (!) on xfs.
    # With --remove-destination, we avoid this, and copying
    # (with enough RAM to cache it) takes 5 seconds:
    cp -r --remove-destination restore/* lib/modules/$KernelVer/.
    rm -rf restore
    popd

    # Make sure the files lists start with absolute paths or rpmbuild fails.
    # Also add in the dir entries
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/k-d.list > ../kernel${Variant:+-${Variant}}-modules.list
    sed -e 's/^lib*/%dir \/lib/' %{?zipsed} $RPM_BUILD_ROOT/module-dirs.list > ../kernel${Variant:+-${Variant}}-modules-core.list
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/modules.list >> ../kernel${Variant:+-${Variant}}-modules-core.list
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/mod-extra.list >> ../kernel${Variant:+-${Variant}}-modules-extra.list
    if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" ]]; then
        sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/mod-kvm.list >> ../kernel${Variant:+-${Variant}}-kvm.list
    fi

    # Cleanup
    rm -f $RPM_BUILD_ROOT/k-d.list
    rm -f $RPM_BUILD_ROOT/modules.list
    rm -f $RPM_BUILD_ROOT/module-dirs.list
    rm -f $RPM_BUILD_ROOT/mod-extra.list
    rm -f $RPM_BUILD_ROOT/mod-internal.list
%if 0%{!?fedora:1}
    rm -f $RPM_BUILD_ROOT/mod-partner.list
%endif
    if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" ]]; then
        rm -f $RPM_BUILD_ROOT/mod-kvm.list
    fi

%if %{signmodules}
    if [ $DoModules -eq 1 ]; then
    # Save the signing keys so we can sign the modules in __modsign_install_post
    cp certs/signing_key.pem certs/signing_key.pem.sign${Variant:++${Variant}}
    cp certs/signing_key.x509 certs/signing_key.x509.sign${Variant:++${Variant}}
    fi
%endif

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir

    ln -sf ../../../src/kernels/$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # Generate vmlinux.h and put it to kernel-devel path
    # zfcpdump build does not have btf anymore
    if [ "$Variant" != "zfcpdump" ]; then
        # Build the bootstrap bpftool to generate vmlinux.h
        export BPFBOOTSTRAP_CFLAGS=$(echo "%{__global_compiler_flags}" | sed -r "s/\-specs=[^\ ]+\/redhat-annobin-cc1//")
        export BPFBOOTSTRAP_LDFLAGS=$(echo "%{__global_ldflags}" | sed -r "s/\-specs=[^\ ]+\/redhat-annobin-cc1//")
        CFLAGS="" LDFLAGS="" make EXTRA_CFLAGS="${BPFBOOTSTRAP_CFLAGS}" EXTRA_LDFLAGS="${BPFBOOTSTRAP_LDFLAGS}" %{?make_opts} %{?clang_make_opts} V=1 -C tools/bpf/bpftool bootstrap

        tools/bpf/bpftool/bootstrap/bpftool btf dump file vmlinux format c > $RPM_BUILD_ROOT/$DevelDir/vmlinux.h
    fi

    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -delete
    # prune junk from kernel-debuginfo
    find $RPM_BUILD_ROOT/usr/src/kernels -name "*.mod.c" -delete

    # Red Hat UEFI Secure Boot CA cert, which can be used to authenticate the kernel
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer
    %ifarch x86_64 aarch64
       install -m 0644 %{secureboot_ca_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca-20200609.cer
       install -m 0644 %{secureboot_ca_1} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca-20140212.cer
       ln -s kernel-signing-ca-20200609.cer $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
    %else
       install -m 0644 %{secureboot_ca_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
    %endif
    %ifarch s390x ppc64le
    if [ $DoModules -eq 1 ]; then
    if [ -x /usr/bin/rpm-sign ]; then
        install -m 0644 %{secureboot_key_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
    else
        install -m 0644 certs/signing_key.x509.sign${Variant:++${Variant}} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
        openssl x509 -in certs/signing_key.pem.sign${Variant:++${Variant}} -outform der -out $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
        chmod 0644 $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
    fi
    fi
    %endif

%if %{with_ipaclones}
    MAXPROCS=$(echo %{?_smp_mflags} | sed -n 's/-j\s*\([0-9]\+\)/\1/p')
    if [ -z "$MAXPROCS" ]; then
        MAXPROCS=1
    fi
    if [ "$Variant" == "" ]; then
        mkdir -p $RPM_BUILD_ROOT/$DevelDir-ipaclones
        find . -name '*.ipa-clones' | xargs -i{} -r -n 1 -P $MAXPROCS install -m 644 -D "{}" "$RPM_BUILD_ROOT/$DevelDir-ipaclones/{}"
    fi
%endif

%if %{with_gcov}
    popd
%endif
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd linux-%{KVERREL}


%if %{with_debug}
%if %{with_realtime}
echo "building rt-debug"
BuildKernel %make_target %kernel_image %{_use_vdso} rt-debug
%endif

%if %{with_arm64_16k}
BuildKernel %make_target %kernel_image %{_use_vdso} 16k-debug
%endif

%if %{with_arm64_64k}
BuildKernel %make_target %kernel_image %{_use_vdso} 64k-debug
%endif

%if %{with_up}
echo "building main debug package"
BuildKernel %make_target %kernel_image %{_use_vdso} debug
%endif
%endif

%if %{with_zfcpdump}
BuildKernel %make_target %kernel_image %{_use_vdso} zfcpdump
%endif

%if %{with_arm64_16k_base}
BuildKernel %make_target %kernel_image %{_use_vdso} 16k
%endif

%if %{with_arm64_64k_base}
BuildKernel %make_target %kernel_image %{_use_vdso} 64k
%endif

%if %{with_realtime_base}
BuildKernel %make_target %kernel_image %{_use_vdso} rt
%endif

%if %{with_up_base}
BuildKernel %make_target %kernel_image %{_use_vdso}
%endif

%ifnarch noarch i686 %{nobuildarches}
%if !%{with_debug} && !%{with_zfcpdump} && !%{with_up} && !%{with_arm64_16k} && !%{with_arm64_64k} && !%{with_realtime}
# If only building the user space tools, then initialize the build environment
# and some variables so that the various userspace tools can be built.
InitBuildVars
%endif
%endif

%ifarch aarch64
%global perf_build_extra_opts CORESIGHT=1
%endif
%global perf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${CFLAGS}" EXTRA_CXXFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS} -Wl,-E" %{?cross_opts} -C tools/perf V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 LIBBPF_DYNAMIC=1 LIBTRACEEVENT_DYNAMIC=1 %{?perf_build_extra_opts} prefix=%{_prefix} PYTHON=%{__python3}
%if %{with_perf}
# perf
# make sure check-headers.sh is executable
chmod +x tools/perf/check-headers.sh
%{perf_make} JOBS=%{_smp_build_ncpus} DESTDIR=$RPM_BUILD_ROOT all
%endif

%if %{with_libperf}
%global libperf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" %{?cross_opts} -C tools/lib/perf V=1
%{libperf_make} JOBS=%{_smp_build_ncpus} DESTDIR=$RPM_BUILD_ROOT
%endif

%global tools_make \
  CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" %{make} %{?make_opts}

%if %{with_tools}
sed -e 's|-O6|-O2|g' -i tools/lib/{api,subcmd}/Makefile tools/perf/Makefile.config
%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%{tools_make} %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false DEBUG=false
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    %{tools_make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   %{tools_make}
   popd
   pushd tools/power/x86/turbostat
   %{tools_make}
   popd
   pushd tools/power/x86/intel-speed-select
   %{tools_make}
   popd
   pushd tools/arch/x86/intel_sdsi
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}"
   popd
%endif
%endif
pushd tools/thermal/tmon/
%{tools_make}
popd
pushd tools/iio/
%{tools_make}
popd
pushd tools/gpio/
%{tools_make}
popd
# build VM tools
pushd tools/mm/
%{tools_make} slabinfo page_owner_sort
popd
pushd tools/verification/rv/
%{tools_make}
popd
pushd tools/tracing/rtla
%{tools_make}
popd
%endif

if [ -f $DevelDir/vmlinux.h ]; then
  RPM_VMLINUX_H=$DevelDir/vmlinux.h
fi

%if %{with_bpftool}
%global bpftool_make \
  %{__make} EXTRA_CFLAGS="${RPM_OPT_FLAGS}" EXTRA_LDFLAGS="%{__global_ldflags}" DESTDIR=$RPM_BUILD_ROOT %{?make_opts} VMLINUX_H="${RPM_VMLINUX_H}" V=1
pushd tools/bpf/bpftool
%{bpftool_make}
popd
%else
echo "bpftools disabled ... disabling selftests"
%endif

%if %{with_selftests}
# Unfortunately, samples/bpf/Makefile expects that the headers are installed
# in the source tree. We installed them previously to $RPM_BUILD_ROOT/usr
# but there's no way to tell the Makefile to take them from there.
%{make} %{?_smp_mflags} headers_install

# If we re building only tools without kernel, we need to generate config
# headers and prepare tree for modules building. The modules_prepare target
# will cover both.
if [ ! -f include/generated/autoconf.h ]; then
   %{make} %{?_smp_mflags} modules_prepare
fi

%{make} %{?_smp_mflags} ARCH=$Arch V=1 M=samples/bpf/ VMLINUX_H="${RPM_VMLINUX_H}" || true

# Prevent bpf selftests to build bpftool repeatedly:
export BPFTOOL=$(pwd)/tools/bpf/bpftool/bpftool

pushd tools/testing/selftests
# We need to install here because we need to call make with ARCH set which
# doesn't seem possible to do in the install section.
%if %{selftests_must_build}
  force_targets="FORCE_TARGETS=1"
%else
  force_targets=""
%endif

%{make} %{?_smp_mflags} ARCH=$Arch V=1 TARGETS="bpf mm livepatch net net/forwarding net/mptcp netfilter tc-testing memfd drivers/net/bonding" SKIP_TARGETS="" $force_targets INSTALL_PATH=%{buildroot}%{_libexecdir}/kselftests VMLINUX_H="${RPM_VMLINUX_H}" install

# 'make install' for bpf is broken and upstream refuses to fix it.
# Install the needed files manually.
for dir in bpf bpf/no_alu32 bpf/progs; do
	# In ARK, the rpm build continues even if some of the selftests
	# cannot be built. It's not always possible to build selftests,
	# as upstream sometimes dependens on too new llvm version or has
	# other issues. If something did not get built, just skip it.
	test -d $dir || continue
	mkdir -p %{buildroot}%{_libexecdir}/kselftests/$dir
	find $dir -maxdepth 1 -type f \( -executable -o -name '*.py' -o -name settings -o \
		-name 'btf_dump_test_case_*.c' -o -name '*.ko' -o \
		-name '*.o' -exec sh -c 'readelf -h "{}" | grep -q "^  Machine:.*BPF"' \; \) -print0 | \
	xargs -0 cp -t %{buildroot}%{_libexecdir}/kselftests/$dir || true
done
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/test_progs"
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/test_progs-no_alu32"
popd
export -n BPFTOOL
%endif

%if %{with_doc}
# Make the HTML pages.
%{__make} PYTHON=/usr/bin/python3 htmldocs || %{doc_build_fail}

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w
%endif

# Module signing (modsign)
#
# This must be run _after_ find-debuginfo.sh runs, otherwise that will strip
# the signature off of the modules.
#
# Don't sign modules for the zfcpdump variant as it is monolithic.

%define __modsign_install_post \
  if [ "%{signmodules}" -eq "1" ]; then \
    echo "Signing kernel modules ..." \
    modules_dirs="$(shopt -s nullglob; echo $RPM_BUILD_ROOT/lib/modules/%{KVERREL}*)" \
    for modules_dir in $modules_dirs; do \
        variant_suffix="${modules_dir#$RPM_BUILD_ROOT/lib/modules/%{KVERREL}}" \
        [ "$variant_suffix" == "+zfcpdump" ] && continue \
        echo "Signing modules for %{KVERREL}${variant_suffix}" \
        %{modsign_cmd} certs/signing_key.pem.sign${variant_suffix} certs/signing_key.x509.sign${variant_suffix} $modules_dir/ \
    done \
  fi \
  if [ "%{zipmodules}" -eq "1" ]; then \
    echo "Compressing kernel modules ..." \
    find $RPM_BUILD_ROOT/lib/modules/ -type f -name '*.ko' | xargs -n 16 -P%{?_smp_build_ncpus} -r %compression %compression_flags; \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}

%ifnarch noarch %{nobuildarches}
%global __debug_package 1
%files -f debugfiles.list debuginfo-common-%{_target_cpu}
%endif

%endif

# We don't want to package debuginfo for self-tests and samples but
# we have to delete them to avoid an error messages about unpackaged
# files.
# Delete the debuginfo for kernel-devel files
%define __remove_unwanted_dbginfo_install_post \
  if [ "%{with_selftests}" -ne "0" ]; then \
    rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/libexec/ksamples; \
    rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/libexec/kselftests; \
  fi \
  rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/src; \
%{nil}

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__remove_unwanted_dbginfo_install_post}\
  %{__restore_unstripped_root_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd linux-%{KVERREL}

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}

# copy the source over
mkdir -p $docdir
tar -h -f - --exclude=man --exclude='.*' -c Documentation | tar xf - -C $docdir

# with_doc
%endif

# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

%if %{with_headers}
# Install kernel headers
%{__make} ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

%endif

%if %{with_cross_headers}
HDR_ARCH_LIST='arm64 powerpc s390 x86'
mkdir -p $RPM_BUILD_ROOT/usr/tmp-headers

for arch in $HDR_ARCH_LIST; do
    mkdir $RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch}
    %{__make} ARCH=${arch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch} headers_install
done

find $RPM_BUILD_ROOT/usr/tmp-headers \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

# Copy all the architectures we care about to their respective asm directories
for arch in $HDR_ARCH_LIST ; do
    mkdir -p $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include
    mv $RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch}/include/* $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include/
done

rm -rf $RPM_BUILD_ROOT/usr/tmp-headers
%endif

%if %{with_kernel_abi_stablelists}
# kabi directory
INSTALL_KABI_PATH=$RPM_BUILD_ROOT/lib/modules/
mkdir -p $INSTALL_KABI_PATH

# install kabi releases directories
tar -xvf %{SOURCE300} -C $INSTALL_KABI_PATH
# with_kernel_abi_stablelists
%endif

%if %{with_perf}
# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT lib=%{_lib} install-bin
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace

# For both of the below, yes, this should be using a macro but right now
# it's hard coded and we don't actually want it anyway right now.
# Whoever wants examples can fix it up!

# remove examples
rm -rf %{buildroot}/usr/lib/perf/examples
rm -rf %{buildroot}/usr/lib/perf/include

# python-perf extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
mkdir -p %{buildroot}/%{_mandir}/man1
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man

# remove any tracevent files, eg. its plugins still gets built and installed,
# even if we build against system's libtracevent during perf build (by setting
# LIBTRACEEVENT_DYNAMIC=1 above in perf_make macro). Those files should already
# ship with libtraceevent package.
rm -rf %{buildroot}%{_libdir}/traceevent
%endif

%if %{with_libperf}
%{libperf_make} DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} install install_headers
# This is installed on some arches and we don't want to ship it
rm -rf %{buildroot}%{_libdir}/libperf.a
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
%{make} -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
%endif
%ifarch x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/intel-speed-select
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/arch/x86/intel_sdsi
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}" DESTDIR=%{buildroot} install
   popd
%endif
pushd tools/thermal/tmon
%{tools_make} INSTALL_ROOT=%{buildroot} install
popd
pushd tools/iio
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/gpio
%{tools_make} DESTDIR=%{buildroot} install
popd
install -m644 -D %{SOURCE2002} %{buildroot}%{_sysconfdir}/logrotate.d/kvm_stat
pushd tools/kvm/kvm_stat
%{__make} INSTALL_ROOT=%{buildroot} install-tools
%{__make} INSTALL_ROOT=%{buildroot} install-man
install -m644 -D kvm_stat.service %{buildroot}%{_unitdir}/kvm_stat.service
popd
# install VM tools
pushd tools/mm/
install -m755 slabinfo %{buildroot}%{_bindir}/slabinfo
install -m755 page_owner_sort %{buildroot}%{_bindir}/page_owner_sort
popd
pushd tools/verification/rv/
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/tracing/rtla/
%{tools_make} DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_bindir}/hwnoise
rm -f %{buildroot}%{_bindir}/osnoise
rm -f %{buildroot}%{_bindir}/timerlat
(cd %{buildroot}

        ln -sf rtla ./%{_bindir}/hwnoise
        ln -sf rtla ./%{_bindir}/osnoise
        ln -sf rtla ./%{_bindir}/timerlat
)
popd
%endif

%if %{with_bpftool}
pushd tools/bpf/bpftool
%{bpftool_make} prefix=%{_prefix} bash_compdir=%{_sysconfdir}/bash_completion.d/ mandir=%{_mandir} install doc-install
popd
%endif

%if %{with_selftests}
pushd samples
install -d %{buildroot}%{_libexecdir}/ksamples
# install bpf samples
pushd bpf
install -d %{buildroot}%{_libexecdir}/ksamples/bpf
find -type f -executable -exec install -m755 {} %{buildroot}%{_libexecdir}/ksamples/bpf \;
install -m755 *.sh %{buildroot}%{_libexecdir}/ksamples/bpf
# test_lwt_bpf.sh compiles test_lwt_bpf.c when run; this works only from the
# kernel tree. Just remove it.
rm %{buildroot}%{_libexecdir}/ksamples/bpf/test_lwt_bpf.sh
install -m644 *_kern.o %{buildroot}%{_libexecdir}/ksamples/bpf || true
install -m644 tcp_bpf.readme %{buildroot}%{_libexecdir}/ksamples/bpf
popd
# install pktgen samples
pushd pktgen
install -d %{buildroot}%{_libexecdir}/ksamples/pktgen
find . -type f -executable -exec install -m755 {} %{buildroot}%{_libexecdir}/ksamples/pktgen/{} \;
find . -type f ! -executable -exec install -m644 {} %{buildroot}%{_libexecdir}/ksamples/pktgen/{} \;
popd
popd
# install mm selftests
pushd tools/testing/selftests/mm
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/mm/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/mm/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/mm/{} \;
popd
# install drivers/net/mlxsw selftests
pushd tools/testing/selftests/drivers/net/mlxsw
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
popd
# install drivers/net/netdevsim selftests
pushd tools/testing/selftests/drivers/net/netdevsim
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/netdevsim/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/netdevsim/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/netdevsim/{} \;
popd
# install drivers/net/bonding selftests
pushd tools/testing/selftests/drivers/net/bonding
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/bonding/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/bonding/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/bonding/{} \;
popd
# install net/forwarding selftests
pushd tools/testing/selftests/net/forwarding
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
popd
# install net/mptcp selftests
pushd tools/testing/selftests/net/mptcp
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/mptcp/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/mptcp/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/mptcp/{} \;
popd
# install tc-testing selftests
pushd tools/testing/selftests/tc-testing
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
popd
# install livepatch selftests
pushd tools/testing/selftests/livepatch
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/livepatch/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/livepatch/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/livepatch/{} \;
popd
# install netfilter selftests
pushd tools/testing/selftests/netfilter
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/netfilter/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/netfilter/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/netfilter/{} \;
popd

# install memfd selftests
pushd tools/testing/selftests/memfd
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
popd
%endif

###
### clean
###

###
### scripts
###

#
# This macro defines a %%post script for a kernel*-devel package.
#    %%kernel_devel_post [<subpackage>]
# Note we don't run hardlink if ostree is in use, as ostree is
# a far more sophisticated hardlink implementation.
# https://github.com/projectatomic/rpm-ostree/commit/58a79056a889be8814aa51f507b2c7a4dccee526
#
# The deletion of *.hardlink-temporary files is a temporary workaround
# for this bug in the hardlink binary (fixed in util-linux 2.38):
# https://github.com/util-linux/util-linux/issues/1602
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
drstatus=1\
if [ "$DUPEREMOVE" != "no" -a -x /usr/sbin/duperemove -a ! -e /run/ostree-booted ] \
then\
    /usr/sbin/duperemove -rd /usr/src/kernels > /dev/null 2>&1\
    drstatus=$?\
fi\
if [ "$drstatus" -ne 0 -a "$HARDLINK" != "no" -a -x /usr/bin/hardlink -a ! -e /run/ostree-booted ] \
then\
    (cd /usr/src/kernels/%{KVERREL}%{?1:+%{1}} &&\
     /usr/bin/find . -type f | while read f; do\
       hardlink -c /usr/src/kernels/*%{?dist}.*/$f $f > /dev/null\
     done;\
     /usr/bin/find /usr/src/kernels -type f -name '*.hardlink-temporary' -delete\
    )\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-extra package.
# It also defines a %%postun script that does the same thing.
#    %%kernel_modules_extra_post [<subpackage>]
#
%define kernel_modules_extra_post() \
%{expand:%%post %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-internal package.
# It also defines a %%postun script that does the same thing.
#    %%kernel_modules_internal_post [<subpackage>]
#
%define kernel_modules_internal_post() \
%{expand:%%post %{?1:%{1}-}modules-internal}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-internal}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-partner package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_modules_partner_post [<subpackage>]
#
%define kernel_modules_partner_post() \
%{expand:%%post %{?1:%{1}-}modules-partner}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-partner}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

%if %{with_realtime}
#
# This macro defines a %%post script for a kernel*-kvm package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_kvm_post [<subpackage>]
#
%define kernel_kvm_post() \
%{expand:%%post %{?1:%{1}-}kvm}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}kvm}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}
%endif

#
# This macro defines a %%post script for a kernel*-modules package.
# It also defines a %%postun script that does the same thing.
#    %%kernel_modules_post [<subpackage>]
#
%define kernel_modules_post() \
%{expand:%%post %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL}%{?1:+%{1}} ]; then\
	mkdir -p %{_localstatedir}/lib/rpm-state/%{name}\
	touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}%{?1:+%{1}}\
fi\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%posttrans %{?1:%{1}-}modules}\
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}%{?1:+%{1}} ]; then\
	rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}%{?1:+%{1}}\
	echo "Running: dracut -f --kver %{KVERREL}%{?1:+%{1}}"\
	dracut -f --kver "%{KVERREL}%{?1:+%{1}}" || exit $?\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-core package.
#	%%kernel_modules_core_post [<subpackage>]
#
%define kernel_modules_core_post() \
%{expand:%%posttrans %{?1:%{1}-}modules-core}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

# This macro defines a %%posttrans script for a kernel package.
#    %%kernel_variant_posttrans [-v <subpackage>] [-u uki-suffix]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans(v:u:) \
%{expand:%%posttrans %{?-v:%{-v*}-}%{!?-u*:core}%{?-u*:uki-%{-u*}}}\
%if 0%{!?fedora:1}\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --add-kernel %{KVERREL}%{?-v:+%{-v*}} || exit $?\
fi\
%endif\
rm -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL}%{?-v:+%{-v*}}\
/bin/kernel-install add %{KVERREL}%{?-v:+%{-v*}} /lib/modules/%{KVERREL}%{?-v:+%{-v*}}/vmlinuz%{?-u:-%{-u*}.efi} || exit $?\
if [[ ! -e "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext" ]]; then\
    ln -s "/lib/modules/%{KVERREL}%{?-v:+%{-v*}}/symvers.%compext" "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext"\
    if command -v restorecon &>/dev/null; then\
        restorecon "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext"\
    fi\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#    %%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:r:) \
%{expand:%%kernel_devel_post %{?-v*}}\
%{expand:%%kernel_modules_post %{?-v*}}\
%{expand:%%kernel_modules_core_post %{?-v*}}\
%{expand:%%kernel_modules_extra_post %{?-v*}}\
%{expand:%%kernel_modules_internal_post %{?-v*}}\
%if 0%{!?fedora:1}\
%{expand:%%kernel_modules_partner_post %{?-v*}}\
%endif\
%{expand:%%kernel_variant_posttrans %{?-v*:-v %{-v*}}}\
%{expand:%%post %{?-v*:%{-v*}-}core}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
mkdir -p %{_localstatedir}/lib/rpm-state/%{name}\
touch %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL}%{?-v:+%{-v*}}\
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#    %%kernel_variant_preun [-v <subpackage>] -u [uki-suffix]
#
%define kernel_variant_preun(v:u:) \
%{expand:%%preun %{?-v:%{-v*}-}%{!?-u*:core}%{?-u*:uki-%{-u*}}}\
/bin/kernel-install remove %{KVERREL}%{?-v:+%{-v*}} || exit $?\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --remove-kernel %{KVERREL}%{?-v:+%{-v*}} || exit $?\
fi\
%{nil}

%if %{with_up_base} && %{with_efiuki}
%kernel_variant_posttrans -u virt
%kernel_variant_preun -u virt
%endif

%if %{with_up_base}
%kernel_variant_preun
%kernel_variant_post
%endif

%if %{with_zfcpdump}
%kernel_variant_preun -v zfcpdump
%kernel_variant_post -v zfcpdump
%endif

%if %{with_up} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v debug -u virt
%kernel_variant_preun -v debug -u virt
%endif

%if %{with_up} && %{with_debug}
%kernel_variant_preun -v debug
%kernel_variant_post -v debug
%endif

%if %{with_arm64_16k_base}
%kernel_variant_preun -v 16k
%kernel_variant_post -v 16k
%endif

%if %{with_debug} && %{with_arm64_16k}
%kernel_variant_preun -v 16k-debug
%kernel_variant_post -v 16k-debug
%endif

%if %{with_arm64_16k} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v 16k-debug -u virt
%kernel_variant_preun -v 16k-debug -u virt
%endif

%if %{with_arm64_16k_base} && %{with_efiuki}
%kernel_variant_posttrans -v 16k -u virt
%kernel_variant_preun -v 16k -u virt
%endif

%if %{with_arm64_64k_base}
%kernel_variant_preun -v 64k
%kernel_variant_post -v 64k
%endif

%if %{with_debug} && %{with_arm64_64k}
%kernel_variant_preun -v 64k-debug
%kernel_variant_post -v 64k-debug
%endif

%if %{with_arm64_64k} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v 64k-debug -u virt
%kernel_variant_preun -v 64k-debug -u virt
%endif

%if %{with_arm64_64k_base} && %{with_efiuki}
%kernel_variant_posttrans -v 64k -u virt
%kernel_variant_preun -v 64k -u virt
%endif

%if %{with_realtime_base}
%kernel_variant_preun -v rt
%kernel_variant_post -v rt -r kernel
%kernel_kvm_post rt
%endif

%if %{with_realtime} && %{with_debug}
%kernel_variant_preun -v rt-debug
%kernel_variant_post -v rt-debug
%kernel_kvm_post rt-debug
%endif

###
### file lists
###

%if %{with_headers}
%files headers
/usr/include/*
%exclude %{_includedir}/cpufreq.h
%endif

%if %{with_cross_headers}
%files cross-headers
/usr/*-linux-gnu/include/*
%endif

%if %{with_kernel_abi_stablelists}
%files -n %{name}-abi-stablelists
/lib/modules/kabi-*
%endif

%if %{with_kabidw_base}
%ifarch x86_64 s390x ppc64 ppc64le aarch64
%files %{name}-kabidw-base-internal
%defattr(-,root,root)
/kabidw-base/%{_target_cpu}/*
%endif
%endif

# only some architecture builds need kernel-doc
%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}
%endif

%if %{with_perf}
%files -n perf
%{_bindir}/perf
%{_libdir}/libperf-jvmti.so
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_datadir}/perf-core/*
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc linux-%{KVERREL}/tools/perf/Documentation/examples.txt
%{_docdir}/perf-tip/tips.txt

%files -n python3-perf
%{python3_sitearch}/*

%if %{with_debuginfo}
%files -f perf-debuginfo.list -n perf-debuginfo

%files -f python3-perf-debuginfo.list -n python3-perf-debuginfo
%endif
# with_perf
%endif

%if %{with_libperf}
%files -n libperf
%{_libdir}/libperf.so.0
%{_libdir}/libperf.so.0.0.1

%files -n libperf-devel
%{_libdir}/libperf.so
%{_libdir}/pkgconfig/libperf.pc
%{_includedir}/internal/*.h
%{_includedir}/perf/bpf_perf.h
%{_includedir}/perf/core.h
%{_includedir}/perf/cpumap.h
%{_includedir}/perf/perf_dlfilter.h
%{_includedir}/perf/event.h
%{_includedir}/perf/evlist.h
%{_includedir}/perf/evsel.h
%{_includedir}/perf/mmap.h
%{_includedir}/perf/threadmap.h
%{_mandir}/man3/libperf.3.gz
%{_mandir}/man7/libperf-counting.7.gz
%{_mandir}/man7/libperf-sampling.7.gz
%{_docdir}/libperf/examples/sampling.c
%{_docdir}/libperf/examples/counting.c
%{_docdir}/libperf/html/libperf.html
%{_docdir}/libperf/html/libperf-counting.html
%{_docdir}/libperf/html/libperf-sampling.html

%files -f libperf-debuginfo.list -n libperf-debuginfo
# with_libperf
%endif


%if %{with_tools}
%ifnarch %{cpupowerarchs}
%files -n kernel-tools
%else
%files -n kernel-tools -f cpupower.lang
%{_bindir}/cpupower
%{_datadir}/bash-completion/completions/cpupower
%ifarch x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_mandir}/man[1-8]/cpupower*
%ifarch x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%{_bindir}/intel-speed-select
%{_sbindir}/intel_sdsi
%endif
# cpupowerarchs
%endif
%{_bindir}/tmon
%{_bindir}/iio_event_monitor
%{_bindir}/iio_generic_buffer
%{_bindir}/lsiio
%{_bindir}/lsgpio
%{_bindir}/gpio-hammer
%{_bindir}/gpio-event-mon
%{_bindir}/gpio-watch
%{_mandir}/man1/kvm_stat*
%{_bindir}/kvm_stat
%{_unitdir}/kvm_stat.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kvm_stat
%{_bindir}/page_owner_sort
%{_bindir}/slabinfo

%if %{with_debuginfo}
%files -f kernel-tools-debuginfo.list -n kernel-tools-debuginfo
%endif

%ifarch %{cpupowerarchs}
%files -n kernel-tools-libs
%{_libdir}/libcpupower.so.1
%{_libdir}/libcpupower.so.0.0.1

%files -n kernel-tools-libs-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_includedir}/powercap.h
%endif

%files -n rtla
%{_bindir}/rtla
%{_bindir}/hwnoise
%{_bindir}/osnoise
%{_bindir}/timerlat
%{_mandir}/man1/rtla-hwnoise.1.gz
%{_mandir}/man1/rtla-osnoise-hist.1.gz
%{_mandir}/man1/rtla-osnoise-top.1.gz
%{_mandir}/man1/rtla-osnoise.1.gz
%{_mandir}/man1/rtla-timerlat-hist.1.gz
%{_mandir}/man1/rtla-timerlat-top.1.gz
%{_mandir}/man1/rtla-timerlat.1.gz
%{_mandir}/man1/rtla.1.gz

%files -n rv
%{_bindir}/rv
%{_mandir}/man1/rv-list.1.gz
%{_mandir}/man1/rv-mon-wip.1.gz
%{_mandir}/man1/rv-mon-wwnr.1.gz
%{_mandir}/man1/rv-mon.1.gz
%{_mandir}/man1/rv.1.gz

# with_tools
%endif

%if %{with_bpftool}
%files -n bpftool
%{_sbindir}/bpftool
%{_sysconfdir}/bash_completion.d/bpftool
%{_mandir}/man8/bpftool-cgroup.8.gz
%{_mandir}/man8/bpftool-gen.8.gz
%{_mandir}/man8/bpftool-iter.8.gz
%{_mandir}/man8/bpftool-link.8.gz
%{_mandir}/man8/bpftool-map.8.gz
%{_mandir}/man8/bpftool-prog.8.gz
%{_mandir}/man8/bpftool-perf.8.gz
%{_mandir}/man8/bpftool.8.gz
%{_mandir}/man8/bpftool-net.8.gz
%{_mandir}/man8/bpftool-feature.8.gz
%{_mandir}/man8/bpftool-btf.8.gz
%{_mandir}/man8/bpftool-struct_ops.8.gz

%if %{with_debuginfo}
%files -f bpftool-debuginfo.list -n bpftool-debuginfo
%defattr(-,root,root)
%endif
%endif

%if %{with_selftests}
%files selftests-internal
%{_libexecdir}/ksamples
%{_libexecdir}/kselftests
%endif

# empty meta-package
%if %{with_up_base}
%ifnarch %nobuildarches noarch
%files
%endif
%endif

# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#    %%kernel_variant_files [-k vmlinux] <use_vdso> <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{2}\
%{expand:%%files %{?1:-f kernel-%{?3:%{3}-}ldsoconf.list} %{?3:%{3}-}core}\
%{!?_licensedir:%global license %%doc}\
%%license linux-%{KVERREL}/COPYING-%{version}-%{release}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}\
%ghost /%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/.vmlinuz.hmac \
%ghost /%{image_install_path}/.vmlinuz-%{KVERREL}%{?3:+%{3}}.hmac \
%ifarch aarch64\
/lib/modules/%{KVERREL}%{?3:+%{3}}/dtb \
%ghost /%{image_install_path}/dtb-%{KVERREL}%{?3:+%{3}} \
%endif\
/lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
%ghost %attr(0600, root, root) /boot/System.map-%{KVERREL}%{?3:+%{3}}\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/symvers.%compext\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin*\
%ghost %attr(0600, root, root) /boot/symvers-%{KVERREL}%{?3:+%{3}}.%compext\
%ghost %attr(0600, root, root) /boot/initramfs-%{KVERREL}%{?3:+%{3}}.img\
%ghost %attr(0644, root, root) /boot/config-%{KVERREL}%{?3:+%{3}}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-core.list %{?3:%{3}-}modules-core}\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}/kernel\
/lib/modules/%{KVERREL}%{?3:+%{3}}/build\
/lib/modules/%{KVERREL}%{?3:+%{3}}/source\
/lib/modules/%{KVERREL}%{?3:+%{3}}/updates\
/lib/modules/%{KVERREL}%{?3:+%{3}}/weak-updates\
/lib/modules/%{KVERREL}%{?3:+%{3}}/systemtap\
%{_datadir}/doc/kernel-keys/%{KVERREL}%{?3:+%{3}}\
%if %{1}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/vdso\
%endif\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.block\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.drm\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.modesetting\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.networking\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.order\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.alias\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.alias.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin.alias.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.dep\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.dep.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.devname\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.softdep\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.symbols\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.symbols.bin\
%{expand:%%files -f kernel-%{?3:%{3}-}modules.list %{?3:%{3}-}modules}\
%{expand:%%files %{?3:%{3}-}devel}\
%defverify(not mtime)\
/usr/src/kernels/%{KVERREL}%{?3:+%{3}}\
%{expand:%%files %{?3:%{3}-}devel-matched}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-extra.list %{?3:%{3}-}modules-extra}\
%config(noreplace) /etc/modprobe.d/*-blacklist.conf\
%{expand:%%files %{?3:%{3}-}modules-internal}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/internal\
%if 0%{!?fedora:1}\
%{expand:%%files %{?3:%{3}-}modules-partner}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/partner\
%endif\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?3}.list %{?3:%{3}-}debuginfo}\
%endif\
%endif\
%if "%{3}" == "rt" || "%{3}" == "rt-debug"\
%{expand:%%files %{?3:%{3}-}kvm}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/kvm\
%else\
%if %{with_efiuki}\
%{expand:%%files %{?3:%{3}-}uki-virt}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
/lib/modules/%{KVERREL}%{?3:+%{3}}/symvers.%compext\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin*\
%attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi\
%ghost /%{image_install_path}/efi/EFI/Linux/%{?-k:%{-k*}}%{!?-k:*}-%{KVERREL}%{?3:+%{3}}.efi\
%endif\
%endif\
%if %{?3:1} %{!?3:0}\
%{expand:%%files %{3}}\
%endif\
%if %{with_gcov}\
%ifnarch %nobuildarches noarch\
%{expand:%%files -f kernel-%{?3:%{3}-}gcov.list %{?3:%{3}-}gcov}\
%endif\
%endif\
%endif\
%{nil}

%kernel_variant_files %{_use_vdso} %{with_up_base}
%if %{with_up}
%kernel_variant_files %{_use_vdso} %{with_debug} debug
%endif
%if %{with_arm64_16k}
%kernel_variant_files %{_use_vdso} %{with_debug} 16k-debug
%endif
%if %{with_arm64_64k}
%kernel_variant_files %{_use_vdso} %{with_debug} 64k-debug
%endif
%kernel_variant_files %{_use_vdso} %{with_realtime_base} rt
%if %{with_realtime}
%kernel_variant_files %{_use_vdso} %{with_debug} rt-debug
%endif
%if %{with_debug_meta}
%files debug
%files debug-core
%files debug-devel
%files debug-devel-matched
%files debug-modules
%files debug-modules-core
%files debug-modules-extra
%if %{with_arm64_16k}
%files 16k-debug
%files 16k-debug-core
%files 16k-debug-devel
%files 16k-debug-devel-matched
%files 16k-debug-modules
%files 16k-debug-modules-extra
%endif
%if %{with_arm64_64k}
%files 64k-debug
%files 64k-debug-core
%files 64k-debug-devel
%files 64k-debug-devel-matched
%files 64k-debug-modules
%files 64k-debug-modules-extra
%endif
%endif
%kernel_variant_files %{_use_vdso} %{with_zfcpdump} zfcpdump
%kernel_variant_files %{_use_vdso} %{with_arm64_16k_base} 16k
%kernel_variant_files %{_use_vdso} %{with_arm64_64k_base} 64k

%define kernel_variant_ipaclones(k:) \
%if %{1}\
%if %{with_ipaclones}\
%{expand:%%files %{?2:%{2}-}ipaclones-internal}\
%defattr(-,root,root)\
%defverify(not mtime)\
/usr/src/kernels/%{KVERREL}%{?2:+%{2}}-ipaclones\
%endif\
%endif\
%{nil}

%kernel_variant_ipaclones %{with_up_base}

# plz don't put in a version string unless you're going to tag
# and build.
#
#
%changelog
* Thu May 02 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.9-500.chinfo
- 6.8.9

* Sat Apr 27 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.8-500.chinfo
- 6.8.8

* Wed Apr 17 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.7-500.chinfo
- 6.8.7

* Sat Apr 13 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.6-500.chinfo
- 6.8.6

* Wed Apr 10 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.5-500.chinfo
- 6.8.5

* Thu Apr 04 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.4-500.chinfo
- 6.8.4 - pf4

* Wed Apr 03 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.3-500.chinfo
- 6.8.3 - pf4

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.2-500.chinfo
- 6.8.2 - pf3

* Mon Mar 11 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.0-500.chinfo
- 6.8.0 - pf1

* Wed Mar 06 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.9-500.chinfo
- 6.7.9 - pf8

* Fri Mar 01 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.7-500.chinfo
- 6.7.7 - pf8

* Fri Feb 23 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.6-500.chinfo
- 6.7.6 - pf7
- Rawhide sync (reenable tools packages)

* Mon Feb 05 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.5-500.chinfo
- 6.7.5 - pf7

* Mon Feb 05 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.4-500.chinfo
- 6.7.4 - pf6

* Sun Jan 28 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.2-500.chinfo
- 6.7.2 - pf4

* Mon Jan 08 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.0-500.chinfo
- 6.7.0 - pf1

* Fri Jan 05 2024 Phantom X <megaphantomx at hotmail dot com> - 6.6.10-500.chinfo
- 6.6.10 - pf6

* Mon Jan 01 2024 Phantom X <megaphantomx at hotmail dot com> - 6.6.9-500.chinfo
- 6.6.9 - pf6

* Wed Dec 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.8-500.chinfo
- 6.6.8 - pf5

* Thu Dec 14 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.7-500.chinfo
- 6.6.7 - pf5

* Fri Dec 08 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.5-500.chinfo
- 6.6.5 - pf3

* Sun Dec 03 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.4-500.chinfo
- 6.6.4 - pf3

* Tue Nov 28 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.3-500.chinfo
- 6.6.3 - pf3

* Mon Nov 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.2-500.chinfo
- 6.6.2 - pf3

* Wed Nov 08 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.1-500.chinfo
- 6.6.1 - pf2

* Tue Oct 31 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.0-500.chinfo
- 6.6.0 - pf1

* Wed Oct 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.9-500.chinfo
- 6.5.9 - pf6

* Fri Oct 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.8-500.chinfo
- 6.5.8 - pf6

* Tue Oct 10 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.7-500.chinfo
- 6.5.7 - pf5

* Fri Oct 06 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.6-500.chinfo
- 6.5.6 - pf4

* Sat Sep 23 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.5-500.chinfo
- 6.5.5 - pf3

* Tue Sep 19 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.4-500.chinfo
- 6.5.4 - pf3

* Mon Sep 18 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.3-500.chinfo
- 6.5.3 - pf3

* Thu Sep 07 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.2-500.chinfo
- 6.5.2 - pf2

* Sat Sep 02 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.1-500.chinfo
- 6.5.1 - pf2

* Thu Aug 31 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.0-500.chinfo
- 6.5.0 - pf1

* Wed Aug 23 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.12-500.chinfo
- 6.4.12 - pf6

* Wed Aug 16 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.11-500.chinfo
- 6.4.11 - pf6

* Fri Aug 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.10-500.chinfo
- 6.4.10 - pf5

* Tue Aug 08 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.9-500.chinfo
- 6.4.9 - pf5

* Thu Aug 03 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.8-500.chinfo
- 6.4.8 - pf5

* Thu Jul 27 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.7-500.chinfo
- 6.4.7 - pf4

* Mon Jul 24 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.6-500.chinfo
- 6.4.6 - pf4

* Sun Jul 23 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.5-500.chinfo
- 6.4.5 - pf4

* Wed Jul 19 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.4-500.chinfo
- 6.4.4 - pf4

* Tue Jul 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.3-500.chinfo
- 6.4.3 - pf3

* Wed Jul 05 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.2-500.chinfo
- 6.4.2 - pf2

* Tue Jul 04 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-501.chinfo
- 6.4.1 - pf2

* Sat Jul 01 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-500.chinfo
- 6.4.1 - pf1

* Mon Jun 26 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.0-500.chinfo
- 6.4.0 - pf1

* Wed Jun 21 2023  Phantom X <megaphantomx at hotmail dot com> - 6.3.9-500.chinfo
- 6.3.9 - pf6

* Wed Jun 14 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.8-500.chinfo
- 6.3.8 - pf5

* Fri Jun 09 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.7-500.chinfo
- 6.3.7 - pf5

* Mon Jun 05 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.6-500.chinfo
- 6.3.6 - pf5

* Tue May 30 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.5-500.chinfo
- 6.3.5 - pf4
- Fix kernel-rpm-macros usage

* Thu May 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.4-500.chinfo
- 6.3.4 - pf4

* Wed May 17 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.3-500.chinfo
- 6.3.3 - pf4

* Thu May 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.2-500.chinfo
- 6.3.2 - pf4

* Mon May 01 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.1-500.chinfo
- 6.3.1 - pf2

* Tue Apr 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.0-500.chinfo
- 6.3.0 - pf1
- Rawhide sync

* Thu Apr 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.12-500.chinfo
- 6.2.12 - pf6

* Thu Apr 13 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.11-500.chinfo
- 6.2.11 - pf6

* Thu Apr 06 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.10-500.chinfo
- 6.2.10 - pf5

* Thu Mar 30 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.9-500.chinfo
- 6.2.9 - pf5

* Wed Mar 22 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.8-500.chinfo
- 6.2.8 - pf5

* Fri Mar 17 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.7-500.chinfo
- 6.2.7 - pf5

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.6-500.chinfo
- 6.2.6 - pf4

* Sat Mar 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.5-500.chinfo
- 6.2.5 - pf4

* Fri Mar 10 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.3-500.chinfo
- 6.2.3 - pf4

* Fri Mar 03 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.2-500.chinfo
- 6.2.2 - pf3

* Sun Feb 26 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.1-501.chinfo
- 6.2.1 - pf2

* Sat Feb 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.1-500.chinfo
- 6.2.1 - pf2

* Mon Feb 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.0-500.chinfo
- 6.2.0 - pf1

###
# The following Emacs magic makes C-c C-e use UTC dates.
# Local Variables:
# rpm-change-log-uses-utc: t
# End:
###
