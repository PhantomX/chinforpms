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
%bcond rpm_macros 0

%if %{without rpm_macros}
%global __required_ksyms_requires %{nil}
%global __provided_ksyms_provides %{nil}
%endif

# Option to enable compiling with clang instead of gcc.
%bcond toolchain_clang 0

%if %{with toolchain_clang}
%global toolchain clang
%endif

# Compile the kernel with LTO (only supported when building with clang).
%bcond clang_lto 0

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
%define uname_suffix() %{lua:
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
%define uname_variant() %{lua:
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

# RHEL/CentOS specific .SBAT entries
%if 0%{?centos}
%global sbat_suffix centos
%else
%if 0%{?fedora}
%global sbat_suffix fedora
%else
%global sbat_suffix rhel
%endif
%endif

# Sign modules on all arches
%global signmodules 1

# Add additional rhel certificates to system trusted keys.
%global rhelkeys 1

# Compress modules only for architectures that build modules
%ifarch noarch
%global zipmodules 0
%else
%global zipmodules 1
%endif

# Default compression algorithm
%global compression xz
%global compression_flags --compress --check=crc32 --lzma2=dict=1MiB
%global compext xz

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
# Include Automotive files
%global include_automotive 0
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
%define specrpmversion 6.17.2
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

%global opensuse_id 35e9a22dd3a2f788def4839f3615d957f802e678
%global tkg_id 3ccc607fb2ab85af03711898954c6216ae7303fd
%global vhba_ver 20250329

%global ark_url https://gitlab.com/cki-project/kernel-ark/-/commit
%global kernel_url https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/patch
%global pf_url https://codeberg.org/pf-kernel/linux/commit
%global tkg_url https://github.com/Frogging-Family/linux-tkg/raw/%{tkg_id}/linux-tkg-patches
%global vhba_url https://downloads.sourceforge.net/cdemu
%global zen_url https://github.com/zen-kernel/zen-kernel

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
# we default reatime builds to off for fedora and on for rhel/centos/eln
%if 0%{?fedora}
# kernel-rt (x86_64 and aarch64 only PREEMPT_RT enabled kernel)
%define with_realtime  %{?_with_realtime:1} %{?!_with_realtime:0}
# kernel-rt-64k (aarch64 RT kernel with 64K page_size)
%define with_realtime_arm64_64k %{?_with_realtime_arm64_64k:1} %{?!_with_realtime_arm64_64k:0}
%else
# kernel-rt (x86_64 and aarch64 only PREEMPT_RT enabled kernel)
%define with_realtime  %{?_without_realtime:0} %{?!_without_realtime:1}
# kernel-rt-64k (aarch64 RT kernel with 64K page_size)
%define with_realtime_arm64_64k %{?_without_realtime_arm64_64k: 0} %{?!_without_realtime_arm64_64k:1}
%endif
# kernel-automotive (x86_64 and aarch64 with PREEMPT_RT enabled - currently off by default)
%define with_automotive %{?_with_automotive:1} %{?!_with_automotive:0}

# Supported variants
#            with_base with_debug    with_gcov
# up         X         X             X
# zfcpdump   X                       X
# arm64_16k  X         X             X
# arm64_64k  X         X             X
# realtime   X         X             X
# automotive X         X             X

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
# ynl
%define with_ynl      %{?_without_ynl:0} %{?!_without_ynl:1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo:0} %{?!_without_debuginfo:1}
# kernel-abi-stablelists
%define with_kernel_abi_stablelists %{?_without_kernel_abi_whitelists:0} %{?!_without_kernel_abi_whitelists:1}
%define with_kernel_abi_stablelists 0
# internal samples and selftests
%define with_selftests %{?_without_selftests:0} %{?!_without_selftests:1}
%define with_selftests 0
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
# Only build the automotive variant of the kernel (--with automotiveonly):
%define with_automotiveonly %{?_with_automotiveonly:1} %{?!_with_automotiveonly:0}
# Build the automotive kernel (--with automotive_build), this builds base variant with automotive config/options:
%define with_automotive_build %{?_with_automotive_build:1} %{?!_with_automotive_build:0}
# Only build the tools package
%define with_toolsonly %{?_with_toolsonly:1} %{?!_with_toolsonly:0}
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

# Want to build a vanilla kernel build without any non-upstream patches?
%define with_vanilla %{?_with_vanilla:1} %{?!_with_vanilla:0}

%ifarch x86_64 aarch64 riscv64
%define with_efiuki %{?_without_efiuki:0} %{?!_without_efiuki:1}
%else
%define with_efiuki 0
%endif

### CPU optimizations
### with native take precedence, next is tune, then one set in kernel-local-cpu-generic
# Use kernel-local-cpu-native (CONFIG_MNATIVE=y)
%global with_native  %{?_with_native:1} %{?!_with_native:0}

# Use kernel-local-cpu-tune
%global with_tune %{?_with_tune:1} %{?!_with_tune:0}

%if 0%{?fedora}
# Kernel headers are being split out into a separate package
%define with_headers 0
%define with_cross_headers 0
# no stablelist
%define with_kernel_abi_stablelists 0
%define with_arm64_64k 0
%define with_automotive 0
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
%global clang_make_opts HOSTCC=clang CC=clang LLVM_IAS=%{llvm_ias} LLVM=1
%global make_opts %{make_opts} %{clang_make_opts}
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
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%endif

# if requested, only build debug kernel
%if %{with_dbgonly}
%define with_base 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%endif

# if requested, only build realtime kernel
%if %{with_rtonly}
%define with_realtime 1
%define with_realtime_arm64_64k 1
%define with_automotive 0
%define with_up 0
%define with_debug 0
%define with_debuginfo 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_headers 0
%define with_efiuki 0
%define with_zfcpdump 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%endif

# if requested, only build the automotive variant of the kernel
%if %{with_automotiveonly}
%define with_automotive 1
%define with_realtime 0
%define with_up 0
%define with_debug 0
%define with_debuginfo 0
%define with_vdso_install 0
%define with_selftests 1
%endif

# if requested, build kernel-automotive
%if %{with_automotive_build}
%define with_automotive 1
%define with_selftests 1
%endif

# if requested, only build tools
%if %{with_toolsonly}
%define with_tools 1
%define with_up 0
%define with_base 0
%define with_debug 0
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_automotive 0
%define with_cross_headers 0
%define with_doc 0
%define with_selftests 0
%define with_headers 0
%define with_efiuki 0
%define with_zfcpdump 0
%define with_vdso_install 0
%define with_kabichk 0
%define with_kabidwchk 0
%define with_kabidw_base 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_vdso_install 0
%define with_configchecks 0
%endif

# RT and Automotive kernels are only built on x86_64 and aarch64
%ifnarch x86_64 aarch64
%define with_realtime 0
%define with_automotive 0
%endif

%if %{with_automotive}
# overrides compression algorithms for automotive
%global compression zstd
%global compression_flags --rm
%global compext zst

# automotive does not support the following variants
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_efiuki 0
%define with_doc 0
%define with_headers 0
%define with_cross_headers 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kabichk 0
%define with_kernel_abi_stablelists 0
%define with_kabidw_base 0
%define signkernel 0
%define signmodules 1
%define rhelkeys 0
%endif


%if %{zipmodules}
%global zipsed -e 's/\.ko$/\.ko.%compext/'
# for parallel xz processes, replace with 1 to go back to single process
%endif

# turn off kABI DUP check and DWARF-based check if kABI check is disabled
%if !%{with_kabichk}
%define with_kabidupchk 0
%define with_kabidwchk 0
%endif

%if %{with_vdso_install}
%define use_vdso 1
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
%define with_automotive 0
%define with_headers 0
%define with_cross_headers 0
%define with_tools 0
%define with_perf 0
%define with_libperf 0
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
%define with_realtime_arm64_64k 0
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

%ifarch riscv64
%define asmarch riscv
%define hdrarch riscv
%define make_target vmlinuz.efi
%define kernel_image arch/riscv/boot/vmlinuz.efi
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
%define with_realtime_arm64_64k 0
%define with_automotive 0

%define with_debuginfo 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_selftests 0
%define _enable_debug_packages 0
%endif

# Architectures we build tools/cpupower on
%if 0%{?fedora}
%define cpupowerarchs %{ix86} x86_64 ppc64le aarch64 riscv64
%else
%define cpupowerarchs i686 x86_64 ppc64le aarch64 riscv64
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
%if %{with_automotive} && %{with_base} && !%{with_automotive_build}
%define with_automotive_base 1
%else
%define with_automotive_base 0
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
%if %{with_realtime_arm64_64k} && %{with_base}
%define with_realtime_arm64_64k_base 1
%else
%define with_realtime_arm64_64k_base 0
%endif

#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  coreutils, systemd >= 203-2, /usr/bin/kernel-install
%define initrd_prereq  dracut >= 027


Name: %{package_name}
License: ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-2-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR CDDL-1.0) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND ((GPL-2.0-only WITH Linux-syscall-note) OR MIT) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR MIT) AND 0BSD AND BSD-2-Clause AND (BSD-2-Clause OR Apache-2.0) AND BSD-3-Clause AND BSD-3-Clause-Clear AND CC0-1.0 AND GFDL-1.1-no-invariants-or-later AND GPL-1.0-or-later AND (GPL-1.0-or-later OR BSD-3-Clause) AND (GPL-1.0-or-later WITH Linux-syscall-note) AND GPL-2.0-only AND (GPL-2.0-only OR Apache-2.0) AND (GPL-2.0-only OR BSD-2-Clause) AND (GPL-2.0-only OR BSD-3-Clause) AND (GPL-2.0-only OR CDDL-1.0) AND (GPL-2.0-only OR GFDL-1.1-no-invariants-or-later) AND (GPL-2.0-only OR GFDL-1.2-no-invariants-only) AND (GPL-2.0-only OR GFDL-1.2-no-invariants-or-later) AND (GPL-2.0-only WITH Linux-syscall-note) AND GPL-2.0-or-later AND (GPL-2.0-or-later OR BSD-2-Clause) AND (GPL-2.0-or-later OR BSD-3-Clause) AND (GPL-2.0-or-later OR CC-BY-4.0) AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND ISC AND LGPL-2.0-or-later AND (LGPL-2.0-or-later OR BSD-2-Clause) AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND LGPL-2.1-only AND (LGPL-2.1-only OR BSD-2-Clause) AND (LGPL-2.1-only WITH Linux-syscall-note) AND LGPL-2.1-or-later AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND (Linux-OpenIB OR GPL-2.0-only) AND (Linux-OpenIB OR GPL-2.0-only OR BSD-2-Clause) AND Linux-man-pages-copyleft AND MIT AND (MIT OR Apache-2.0) AND (MIT OR GPL-2.0-only) AND (MIT OR GPL-2.0-or-later) AND (MIT OR LGPL-2.1-only) AND (MPL-1.1 OR GPL-2.0-only) AND (X11 OR GPL-2.0-only) AND (X11 OR GPL-2.0-or-later) AND Zlib AND (copyleft-next-0.3.1 OR GPL-2.0-or-later)
URL: https://www.kernel.org/
Version: %{specrpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
%if 0%{?fedora}
ExclusiveArch: noarch x86_64 s390x aarch64 ppc64le riscv64
%else
ExclusiveArch: noarch i386 i686 x86_64 s390x aarch64 ppc64le riscv64
%endif
ExclusiveOS: Linux
%ifnarch %{nobuildarches}
Requires: %{name}-core-uname-r = %{KVERREL}
Requires: %{name}-modules-uname-r = %{KVERREL}
Requires: %{name}-modules-core-uname-r = %{KVERREL}
Requires: ((%{name}-modules-extra-uname-r = %{KVERREL}) if %{name}-modules-extra-matched)
Provides: installonlypkg(kernel)
%endif


#
# List the packages used during the kernel build
#
BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk, %compression
# Kernel EFI/Compression set by CONFIG_KERNEL_ZSTD
%ifarch x86_64 aarch64 riscv64
BuildRequires: zstd
%endif
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: rust, rust-src, bindgen, rustfmt, clippy
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: kernel-rpm-macros
# glibc-static is required for a consistent build environment (specifically
# CONFIG_CC_CAN_LINK_STATIC=y).
BuildRequires: glibc-static
%if %{with_headers} || %{with_cross_headers}
BuildRequires: rsync
%endif
%if %{with_doc}
BuildRequires: xmlto, asciidoc, python3-sphinx, python3-sphinx_rtd_theme
%endif
%if %{with_sparse}
BuildRequires: sparse
%endif
%if %{with_perf}
BuildRequires: zlib-devel binutils-devel newt-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel python3-setuptools
BuildRequires: java-devel
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
BuildRequires: libbpf-devel
BuildRequires: bpftool
BuildRequires: clang

%ifarch %{cpupowerarchs}
# For libcpupower bindings
BuildRequires: swig
%endif

%ifnarch s390x
BuildRequires: pciutils-devel
%endif
%ifarch i686 x86_64
BuildRequires: libnl3-devel
%endif
%endif

%if %{with_tools} && %{with_ynl}
BuildRequires: python3-pyyaml python3-jsonschema python3-pip python3-setuptools >= 61
BuildRequires: (python3-wheel if python3-setuptools < 70)
%endif

BuildRequires: openssl-devel

%if %{with_selftests}
BuildRequires: clang llvm-devel fuse-devel zlib-devel binutils-devel python3-docutils python3-jsonschema
%ifarch x86_64 riscv64
BuildRequires: lld
%endif
BuildRequires: libcap-devel libcap-ng-devel rsync libmnl-devel libxml2-devel
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
%ifarch x86_64 aarch64 riscv64
BuildRequires: nss-tools
BuildRequires: pesign >= 0.10-4
%endif
%endif
%endif

%if %{with_cross}
BuildRequires: binutils-%{_build_arch}-linux-gnu, gcc-%{_build_arch}-linux-gnu
%define cross_opts CROSS_COMPILE=%{_build_arch}-linux-gnu-
%define __strip %{_build_arch}-linux-gnu-strip

%if 0%{?fedora} && 0%{?fedora} <= 41
# Work around find-debuginfo for cross builds.
# find-debuginfo doesn't support any of CROSS options (RHEL-21797),
# and since debugedit > 5.0-16.el10, or since commit
#   dfe1f7ff30f4 ("find-debuginfo.sh: Exit with real exit status in parallel jobs")
# it now aborts on failure and build fails.
# debugedit-5.1-5 in F42 added support to override tools with target versions.
%undefine _include_gdb_index
%endif

%if 0%{?rhel}%{?centos}
%ifarch riscv64
# Temporary workaround to avoid using find-debuginfo and gdb.minimal.
# The current c10s version of gdb-minimal (14.2-4.el10) crashes when given some
# riscv64 kernel modules (see RHEL-91586). Not building the gdb index avoids
# breaking CI for now.
%undefine _include_gdb_index
%endif
%endif
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
# For UKI kernel cmdline addons
BuildRequires: systemd-ukify
# For TPM operations in UKI initramfs
BuildRequires: tpm2-tools
# For UKI sb cert
%if 0%{?rhel}%{?centos} && !0%{?eln}
%if 0%{?centos}
BuildRequires: centos-sb-certs >= 9.0-23
%else
BuildRequires: redhat-sb-certs >= 9.4-0.1
%endif
%endif
%endif

%if 0%{?released_kernel}
Source0: https://cdn.kernel.org/pub/linux/kernel/v%{kversion}.x/linux-%{tarfile_release}.tar.xz
%else
Source0: https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms-kernel/%{name}/linux-%{tarfile_release}.tar.xz/%{src_hash}/linux-%{tarfile_release}.tar.xz
%endif

Source1: Makefile.rhelver

Source10: redhatsecurebootca5.cer
Source13: redhatsecureboot501.cer

%if %{signkernel}
# Name of the packaged file containing signing key
%ifarch ppc64le
%define signing_key_filename kernel-signing-ppc.cer
%endif
%ifarch s390x
%define signing_key_filename kernel-signing-s390.cer
%endif

# Fedora/ELN pesign macro expects to see these cert file names, see:
# https://github.com/rhboot/pesign/blob/main/src/pesign-rpmbuild-helper.in#L216
%if 0%{?fedora}%{?eln}
%define pesign_name_0 redhatsecureboot501
%define secureboot_ca_0 %{SOURCE10}
%define secureboot_key_0 %{SOURCE13}
%endif

# RHEL/centos certs come from system-sb-certs
%if 0%{?rhel} && !0%{?eln}
%define secureboot_ca_0 %{_datadir}/pki/sb-certs/secureboot-ca-%{_arch}.cer
%define secureboot_key_0 %{_datadir}/pki/sb-certs/secureboot-kernel-%{_arch}.cer

%if 0%{?centos}
%define pesign_name_0 centossecureboot201
%else
%ifarch x86_64 aarch64
%define pesign_name_0 redhatsecureboot501
%endif
%ifarch s390x
%define pesign_name_0 redhatsecureboot302
%endif
%ifarch ppc64le
%define pesign_name_0 redhatsecureboot701
%endif
%endif
# rhel && !eln
%endif

# signkernel
%endif

Source20: mod-denylist.sh
Source21: mod-sign.sh
Source22: filtermods.py

%define modsign_cmd %{SOURCE21}

%if 0%{?include_rhel}
Source24: %{name}-aarch64-rhel.config
Source25: %{name}-aarch64-debug-rhel.config

Source27: %{name}-ppc64le-rhel.config
Source28: %{name}-ppc64le-debug-rhel.config
Source29: %{name}-s390x-rhel.config
Source30: %{name}-s390x-debug-rhel.config
Source31: %{name}-s390x-zfcpdump-rhel.config
Source32: %{name}-x86_64-rhel.config
Source33: %{name}-x86_64-debug-rhel.config
# ARM64 64K page-size kernel config
Source42: %{name}-aarch64-64k-rhel.config
Source43: %{name}-aarch64-64k-debug-rhel.config

Source44: %{name}-riscv64-rhel.config
Source45: %{name}-riscv64-debug-rhel.config
%endif

%if %{include_rhel} || %{include_automotive}
Source23: x509.genkey.rhel
Source34: def_variants.yaml.rhel
Source41: x509.genkey.centos
%endif

%if 0%{?include_fedora}
Source50: x509.genkey.fedora

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
Source700: %{name}-riscv64-fedora.config
Source701: %{name}-riscv64-debug-fedora.config

Source62: def_variants.yaml.fedora
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

Source83: uki.sbat.template
Source84: uki-addons.sbat.template
Source85: kernel.sbat.template

Source86: dracut-virt.conf

Source87: flavors

Source151: uki_create_addons.py
Source152: uki_addons.json

Source100: rheldup3.x509
Source101: rhelkpatch1.x509
Source102: nvidiagpuoot001.x509
Source103: rhelimaca1.x509
Source104: rhelima.x509
Source105: rhelima_centos.x509
Source106: fedoraimaca.x509

%if 0%{?fedora}%{?eln}
%define ima_ca_cert %{SOURCE106}
%endif

%if 0%{?rhel} && !0%{?eln}
%define ima_ca_cert %{SOURCE103}
# rhel && !eln
%endif

%if 0%{?centos}
%define ima_signing_cert %{SOURCE105}
%else
%define ima_signing_cert %{SOURCE104}
%endif

%define ima_cert_name ima.cer

Source200: check-kabi

Source201: Module.kabi_aarch64
Source202: Module.kabi_ppc64le
Source203: Module.kabi_s390x
Source204: Module.kabi_x86_64
Source205: Module.kabi_riscv64

Source210: Module.kabi_dup_aarch64
Source211: Module.kabi_dup_ppc64le
Source212: Module.kabi_dup_s390x
Source213: Module.kabi_dup_x86_64
Source214: Module.kabi_dup_riscv64


%if %{with_kernel_abi_stablelists}
Source300: kernel-abi-stablelists-%{kabiversion}.tar.xz
%endif
%if %{with_kabidw_base}
Source301: kernel-kabi-dw-%{kabiversion}.tar.xz
%endif

%if 0%{include_rt}
%if 0%{include_rhel}
Source474: %{name}-aarch64-rt-rhel.config
Source475: %{name}-aarch64-rt-debug-rhel.config
Source476: %{name}-aarch64-rt-64k-rhel.config
Source477: %{name}-aarch64-rt-64k-debug-rhel.config
Source478: %{name}-x86_64-rt-rhel.config
Source479: %{name}-x86_64-rt-debug-rhel.config
%endif
%if 0%{include_fedora}
Source480: %{name}-aarch64-rt-fedora.config
Source481: %{name}-aarch64-rt-debug-fedora.config
Source482: %{name}-aarch64-rt-64k-fedora.config
Source483: %{name}-aarch64-rt-64k-debug-fedora.config
Source484: %{name}-x86_64-rt-fedora.config
Source485: %{name}-x86_64-rt-debug-fedora.config
Source486: %{name}-riscv64-rt-fedora.config
Source487: %{name}-riscv64-rt-debug-fedora.config
%endif
%endif

%if %{include_automotive}
%if %{with_automotive_build}
Source488: %{name}-aarch64-rhel.config
Source489: %{name}-aarch64-debug-rhel.config
Source490: %{name}-x86_64-rhel.config
Source491: %{name}-x86_64-debug-rhel.config
%else
Source488: %{name}-aarch64-automotive-rhel.config
Source489: %{name}-aarch64-automotive-debug-rhel.config
Source490: %{name}-x86_64-automotive-rhel.config
Source491: %{name}-x86_64-automotive-debug-rhel.config
%endif
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

# Extra CPU optimization settings
Source3011: kernel-local-cpu-tune
Source3012: kernel-local-cpu-native
Source3013: kernel-local-cpu-generic

Source4000: README.rst
Source4001: rpminspect.yaml
Source4002: gating.yaml

Source6020: %{vhba_url}/vhba-module/vhba-module-%{vhba_ver}.tar.xz

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

%global patchwork_url https://patchwork.kernel.org
%global patchwork_xdg_url https://patchwork.freedesktop.org/patch
# https://patchwork.kernel.org/patch/10045863
Patch2000: radeon_dp_aux_transfer_native-74-callbacks-suppressed.patch
Patch2001: %{zen_url}/commit/be12070350a151ffb964c562e58983b16962df6d.patch#/zen-v%{patchversion}-sauce-be12070.patch
Patch2002: %{zen_url}/commit/69f73106b713eb0f9afe85b73d37dc439b69ca17.patch#/zen-v%{patchversion}-sauce-69f7310.patch

# Add native cpu gcc optimization support
Patch6000: %{pf_url}/9da6f120250f0b29564aa803cbeb5e9a0eca30dd.patch#/pf-cb-9da6f12.patch
Patch6001: 0001-kbuild-support-native-optimization.patch

Patch6010: 0001-block-elevator-default-blk-mq-to-bfq.patch
Patch6011: 0001-drivers-input-joystick-xpad-remove-dev_warn-nagging.patch

Patch6020: 0001-ZEN-Add-VHBA-driver.patch

%if 0%{?post_factum}
# archlinux
Patch6950:  %{pf_url}/18915da65f0520434ba2fa7e8ddbc17090320a9f.patch#/pf-cb-18915da.patch
# kbuild (7000)
# bbr3
Patch7050:  %{pf_url}/1c91634fce827f78ab54c06e233311a8068b46fd.patch#/pf-cb-1c91634.patch
# zstd
# v4l2loopback
Patch7230:  %{pf_url}/9abe2205879f04b447248d930bfb6bb84ee25328.patch#/pf-cb-9abe220.patch
# cpuidle
Patch7240:  %{pf_url}/93f653636155138ce3f470b33f92dc4616ae8c05.patch#/pf-cb-93f6536.patch
# fixes (7400)
Patch7400:  %{pf_url}/7cc275cc2a38a4725dd93f9fb73d7854b17b46ff.patch#/pf-cb-7cc275c.patch
Patch7401:  %{pf_url}/709cd7c62c197090898da295d216a858ad785f50.patch#/pf-cb-709cd7c.patch
Patch7402:  %{pf_url}/46364c9c832db0bf1c9404230aa560752c387871.patch#/pf-cb-46364c9.patch
Patch7403:  %{pf_url}/000abae353808c5e5978a151117d7f32cc16d071.patch#/pf-cb-000abae.patch
Patch7404:  %{pf_url}/3c83fd094c4ae5f98f95637bd7e041fe485df236.patch#/pf-cb-3c83fd0.patch
Patch7405:  %{pf_url}/951200b32a0c00508717b46b69cacd65826c6520.patch#/pf-cb-951200b.patch
Patch7406:  %{pf_url}/4e7d8c3edbb2eb90f2ebba3d210578be0b007526.patch#/pf-cb-4e7d8c3.patch
Patch7407:  %{pf_url}/446769bb8b85476d250448d5b33930ce36cd66f5.patch#/pf-cb-446769b.patch
Patch7408:  %{pf_url}/06fbbbb72a5dd3442c780d8e601db7c402e5a699.patch#/pf-cb-06fbbbb.patch
Patch7409:  %{pf_url}/da4cb55e9e241559953aa77356a4c137358555bf.patch#/pf-cb-da4cb55.patch
Patch7410:  %{pf_url}/65fa14558b16a7333e0ff4298502c7d24ad1bd22.patch#/pf-cb-65fa145.patch
Patch7411:  %{pf_url}/d62502647bf40bd53322ddef125add2e19f66807.patch#/pf-cb-d625026.patch
Patch7412:  %{pf_url}/bba68687796b236461ae50d3c4692093f1af995f.patch#/pf-cb-bba6868.patch
Patch7413:  %{pf_url}/23be44d561660c7ef6de0d40fd68585ebc64fbb2.patch#/pf-cb-23be44d.patch
Patch7414:  %{pf_url}/afe901eee25f5a3dea3ed545242c8c2b17529e68.patch#/pf-cb-afe901e.patch
Patch7415:  %{pf_url}/77877cbec72d8cc822eda5e86ac802eb688270ea.patch#/pf-cb-77877cb.patch
Patch7416:  %{pf_url}/e4191a13976744ae698aa61f74f6269b3fb33bfb.patch#/pf-cb-e4191a1.patch
Patch7417:  %{pf_url}/8d5fb83e8ead7fac078a11cf2df1152723915bac.patch#/pf-cb-8d5fb83.patch
Patch7418:  %{pf_url}/1193b11e68dde16872264e45e7916248ba0c87f0.patch#/pf-cb-1193b11.patch
Patch7419:  %{pf_url}/6ae26b16820c1dbaf3959122af2434c005b200db.patch#/pf-cb-6ae26b1.patch
Patch7420:  %{pf_url}/9a9b8c28a7451c86b4641b1a3d0bc58bbedcea51.patch#/pf-cb-9a9b8c2.patch
Patch7421:  %{pf_url}/56e83788c9dae75a9a34243a195c615a6be8cfd1.patch#/pf-cb-56e8378.patch
Patch7422:  %{pf_url}/1db1af3290ddc1be5f3015e8ed5de0f4d7a1fa31.patch#/pf-cb-1db1af3.patch
Patch7423:  %{pf_url}/51a91acb9ce9c73e84aba89d8de92299d40767e6.patch#/pf-cb-51a91ac.patch
Patch7424:  %{pf_url}/ece56c81fe7414f646f98ed2304ca2f19ba29747.patch#/pf-cb-ece56c8.patch
Patch7425:  %{pf_url}/75193fa37fe3d340f4873c292b4933421c85f3b1.patch#/pf-cb-75193fa.patch
Patch7426:  %{pf_url}/abd3d59138178f198c50417db44fb5e7bafc9009.patch#/pf-cb-abd3d59.patch
Patch7427:  %{pf_url}/47e0ca9725f97be3f7cedbfe6cc22d68840f9321.patch#/pf-cb-47e0ca9.patch
Patch7428:  %{pf_url}/4720611f15c2a2516fc9f9248bed318647579635.patch#/pf-cb-4720611.patch
Patch7429:  %{pf_url}/f975cd1f86861bd343245aa855c6e6e720c5c27a.patch#/pf-cb-f975cd1.patch
Patch7430:  %{pf_url}/3c78f92356c71dc1bb47de6c07c60d8c27411ec0.patch#/pf-cb-3c78f92.patch
Patch7431:  %{pf_url}/a240b3fe3a6a13a73f262cdab489cc4aa1daf3ba.patch#/pf-cb-a240b3f.patch

%endif

# END OF PATCH DEFINITIONS

%endif


%description
The %{package_name} meta package

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#    %%kernel_reqprovconf [-o] <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
# -o: Skips main "Provides" that would satisfy general kernel requirements that
#     special-purpose kernels shouldn't include.
#     For example, used for zfcpdump-core to *not* provide kernel-core. (BZ 2027654)
#
%define kernel_reqprovconf(o) \
%if %{-o:0}%{!-o:1}\
Provides: kernel = %{specversion}-%{pkg_release}\
Provides: %{name} = %{specversion}-%{pkg_release}\
%endif\
Provides: %{name}-%{_target_cpu} = %{specrpmversion}-%{pkg_release}%{uname_suffix %{?1}}\
Provides: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
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

%if %{with_headers}
%package headers
Summary: Header files for the Linux kernel for use by glibc
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if 0%{?gemini}
Provides: %{name}-headers = %{specversion}-%{release}
Obsoletes: kernel-headers < %{specversion}-%{release}
%endif
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.
%endif

%if %{with_cross_headers}
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
%endif

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
Summary: Development files for the perf library from kernel source
Requires: libperf = %{version}-%{release}
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
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_libdir}/libperf.so.*(\.debug)?|XXX' -o libperf-debuginfo.list}
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
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_bindir}/bootconfig(\.debug)?|.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|.*%%{_bindir}/turbostat(\.debug)?|.*%%{_bindir}/x86_energy_perf_policy(\.debug)?|.*%%{_bindir}/tmon(\.debug)?|.*%%{_bindir}/lsgpio(\.debug)?|.*%%{_bindir}/gpio-hammer(\.debug)?|.*%%{_bindir}/gpio-event-mon(\.debug)?|.*%%{_bindir}/gpio-watch(\.debug)?|.*%%{_bindir}/iio_event_monitor(\.debug)?|.*%%{_bindir}/iio_generic_buffer(\.debug)?|.*%%{_bindir}/lsiio(\.debug)?|.*%%{_bindir}/intel-speed-select(\.debug)?|.*%%{_bindir}/page_owner_sort(\.debug)?|.*%%{_bindir}/slabinfo(\.debug)?|.*%%{_sbindir}/intel_sdsi(\.debug)?|XXX' -o kernel-tools-debuginfo.list}

%package -n rtla
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Real-Time Linux Analysis tools
Requires: libtraceevent
Requires: libtracefs
Requires: libbpf
%ifarch %{cpupowerarchs}
Requires: kernel-tools-libs = %{version}-%{release}
%endif
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

%if %{with_selftests}

%package selftests-internal
Summary: Kernel samples and selftests
Requires: binutils, bpftool, fuse-libs, iproute-tc, iputils, keyutils, nmap-ncat, python3
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

%if %{with_kernel_abi_stablelists}
%package -n %{name}-abi-stablelists
Summary: The Red Hat Enterprise Linux kernel ABI symbol stablelists
AutoReqProv: no
%description -n %{name}-abi-stablelists
The kABI package contains information pertaining to the Red Hat Enterprise
Linux kernel ABI, including lists of kernel symbols that are needed by
external Linux kernel modules, and a yum plugin to aid enforcement.
%endif

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
Provides: %{name}-devel-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Provides: %{name}-devel-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
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
Requires: %{name}-devel-uname-r = %{KVERREL}%{uname_variant %{?1}}\
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

%define kernel_modules_extra_matched_package(m) \
%package modules-extra-matched\
Summary: Meta package which requires modules-extra to be installed for all kernels.\
%description modules-extra-matched\
This meta package provides a single reference that other packages can Require to have modules-extra installed for all kernels.\
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
Provides: %{name}%{?1:-%{1}}-modules-internal-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}%{?1:-%{1}}-modules-internal = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-internal-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
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
Provides: %{name}%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}%{?1:-%{1}}-modules-extra = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-extra-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-modules-extra-uname-r = %{KVERREL}%{uname_variant %{?1}}\
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
Provides: %{name}-modules-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}-modules = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-modules-uname-r = %{KVERREL}%{uname_variant %{?1}}\
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
Provides: %{name}-modules-core-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}-modules-core = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-modules-core-uname-r = %{KVERREL}%{uname_variant %{?1}}\
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
Requires: %{name}-%{1}-core-uname-r = %{KVERREL}%{uname_suffix %{1}}\
Requires: %{name}-%{1}-modules-uname-r = %{KVERREL}%{uname_suffix %{1}}\
Requires: %{name}-%{1}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{1}}\
Requires: ((%{name}-%{1}-modules-extra-uname-r = %{KVERREL}%{uname_suffix %{1}}) if %{name}-modules-extra-matched)\
%if "%{1}" == "rt" || "%{1}" == "rt-debug" || "%{1}" == "rt-64k" || "%{1}" == "rt-64k-debug"\
Requires: realtime-setup\
%endif\
Provides: installonlypkg(kernel)\
%description %{1}\
The meta-package for the %{1} kernel\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] [-m] [-o] <subpackage>
# -m: Used with debugbuildsenabled==0 to create a "meta" debug variant that
#     depends on base variant and skips debug/internal/partner packages.
# -o: Skips main "Provides" that would satisfy general kernel requirements that
#     special-purpose kernels shouldn't include.
#
%define kernel_variant_package(n:mo) \
%package %{?1:%{1}-}core\
Summary: %{variant_summary}\
Provides: %{name}-%{?1:%{1}-}core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel)\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-core-uname-r = %{KVERREL}%{uname_variant %{?1}}\
Requires: %{name}-%{?1:%{1}-}-modules-core-uname-r = %{KVERREL}%{uname_variant %{?1}}\
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
%if %{with_efiuki} && ("%{1}" != "rt" && "%{1}" != "rt-debug" && "%{1}" != "rt-64k" && "%{1}" != "rt-64k-debug")\
%package %{?1:%{1}-}uki-virt\
Summary: %{variant_summary} unified kernel image for virtual machines\
Provides: installonlypkg(kernel)\
Provides: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): systemd >= 254-1\
Recommends: uki-direct\
%package %{?1:%{1}-}uki-virt-addons\
Summary: %{variant_summary} unified kernel image addons for virtual machines\
Provides: installonlypkg(kernel)\
Requires: %{name}%{?1:-%{1}}-uki-virt = %{specrpmversion}-%{release}\
Requires(pre): systemd >= 254-1\
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
Provides: %{name}%{?1:-%{1}}-modules-partner-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}%{?1:-%{1}}-modules-partner = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-partner-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
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

%if %{with_realtime_arm64_64k_base}
%define variant_summary The Linux PREEMPT_RT kernel compiled for 64k pagesize usage
%kernel_variant_package rt-64k
%description rt-64k-core
The kernel package contains a variant of the ARM64 Linux PREEMPT_RT kernel using
a 64K page size.
%endif

%if %{with_realtime_arm64_64k} && %{with_debug}
%define variant_summary The Linux PREEMPT_RT kernel compiled with extra debugging enabled
%if !%{debugbuildsenabled}
%kernel_variant_package -m rt-64k-debug
%else
%kernel_variant_package rt-64k-debug
%endif
%description rt-64k-debug-core
The debug kernel package contains a variant of the ARM64 Linux PREEMPT_RT kernel using
a 64K page size.
This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_debug} && %{with_automotive} && !%{with_automotive_build}
%define variant_summary The Linux Automotive kernel compiled with extra debugging enabled
%kernel_variant_package automotive-debug
%description automotive-debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_automotive_base}
%define variant_summary The Linux kernel compiled with PREEMPT_RT enabled
%kernel_variant_package automotive
%description automotive-core
This package includes a version of the Linux kernel compiled with the
PREEMPT_RT real-time preemption support, targeted for Automotive platforms
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

%description debug-uki-virt-addons
Prebuilt debug unified kernel image addons for virtual machines.
%endif

%if %{with_up_base} && %{with_efiuki}
%description uki-virt
Prebuilt default unified kernel image for virtual machines.

%description uki-virt-addons
Prebuilt default unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_16k} && %{with_debug} && %{with_efiuki}
%description 16k-debug-uki-virt
Prebuilt 16k debug unified kernel image for virtual machines.

%description 16k-debug-uki-virt-addons
Prebuilt 16k debug unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_16k_base} && %{with_efiuki}
%description 16k-uki-virt
Prebuilt 16k unified kernel image for virtual machines.

%description 16k-uki-virt-addons
Prebuilt 16k unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_64k} && %{with_debug} && %{with_efiuki}
%description 64k-debug-uki-virt
Prebuilt 64k debug unified kernel image for virtual machines.

%description 64k-debug-uki-virt-addons
Prebuilt 64k debug unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_64k_base} && %{with_efiuki}
%description 64k-uki-virt
Prebuilt 64k unified kernel image for virtual machines.

%description 64k-uki-virt-addons
Prebuilt 64k unified kernel image addons for virtual machines.
%endif

%ifnarch noarch %{nobuildarches}
%kernel_modules_extra_matched_package
%endif

%define log_msg() \
  { set +x; } 2>/dev/null \
  _log_msglineno=$(grep -n %{*} %{_specdir}/%{name}.spec | grep log_msg | cut -d":" -f1) \
  echo "%{name}.spec:${_log_msglineno}: %{*}" \
  set -x

%prep
%{log_msg "Start of prep stage"}

%{log_msg "Sanity checks"}

# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_up}
%{log_msg "Cannot build --with baseonly, up build is disabled"}
exit 1
%endif
%endif

%if %{with_automotive}
%if 0%{?fedora}
%{log_msg "Cannot build automotive with a fedora baseline, must be rhel/centos/eln"}
exit 1
%endif
%endif

# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      %{log_msg "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"}
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

%setup -q -n kernel-%{tarfile_release} -c -a6020
mv linux-%{tarfile_release} linux-%{KVERREL}

cd linux-%{KVERREL}
cp -a %{SOURCE1} .

%{log_msg "Start of patch applications"}
%if !%{nopatches}

# released_kernel with possible stable updates
%if 0%{?stable_update} && 0%{?released_kernel}
# This is special because the kernel spec is hell and nothing is consistent
ApplyPatch %{PATCH5000}
%endif

ApplyOptionalPatch %{PATCH1}

ApplyOptionalPatch %{PATCH999999}

%if 0%{?post_factum}
# archlinux
ApplyPatch %{PATCH6950}
# kbuild
# bbr3
ApplyPatch %{PATCH7050}
# zstd
# v4l2loopback
ApplyPatch %{PATCH7230}
# cpuidle
ApplyPatch %{PATCH7240}
# fixes
ApplyPatch %{PATCH7400}
ApplyPatch %{PATCH7401}
ApplyPatch %{PATCH7402}
ApplyPatch %{PATCH7403}
ApplyPatch %{PATCH7404}
ApplyPatch %{PATCH7405}
ApplyPatch %{PATCH7406}
ApplyPatch %{PATCH7407}
ApplyPatch %{PATCH7408}
ApplyPatch %{PATCH7409}
ApplyPatch %{PATCH7410}
ApplyPatch %{PATCH7411}
ApplyPatch %{PATCH7412}
ApplyPatch %{PATCH7413}
ApplyPatch %{PATCH7414}
ApplyPatch %{PATCH7415}
ApplyPatch %{PATCH7416}
ApplyPatch %{PATCH7417}
ApplyPatch %{PATCH7418}
ApplyPatch %{PATCH7419}
ApplyPatch %{PATCH7420}
ApplyPatch %{PATCH7421}
ApplyPatch %{PATCH7422}
ApplyPatch %{PATCH7423}
ApplyPatch %{PATCH7424}
ApplyPatch %{PATCH7425}
ApplyPatch %{PATCH7426}
ApplyPatch %{PATCH7427}
ApplyPatch %{PATCH7428}
ApplyPatch %{PATCH7429}
ApplyPatch %{PATCH7430}
ApplyPatch %{PATCH7431}
%endif

# openSUSE
ApplyPatch %{PATCH1010}
ApplyPatch %{PATCH1011}

ApplyPatch %{PATCH2000}
ApplyPatch %{PATCH2001}
ApplyPatch %{PATCH2002}

ApplyPatch %{PATCH6000}
ApplyPatch %{PATCH6001}

ApplyPatch %{PATCH6010}
ApplyPatch %{PATCH6011}

ApplyPatch %{PATCH6020}

# END OF PATCH APPLICATIONS
%{log_msg "End of patch applications"}

%endif

# Any further pre-build tree manipulations happen here.

%{log_msg "Pre-build tree manipulations"}
chmod +x scripts/checkpatch.pl
mv COPYING COPYING-%{specrpmversion}-%{release}

cp -a ../vhba-module-%{vhba_ver}/vhba.c drivers/scsi/vhba/
sed -e 's|_RPM_VHBA_VER_|%{vhba_ver}|' -i drivers/scsi/vhba/Makefile

# on linux-next prevent scripts/setlocalversion from mucking with our version numbers
rm -f localversion-next localversion-rt

# Mangle /usr/bin/python shebangs to /usr/bin/python3
# Mangle all Python shebangs to be Python 3 explicitly
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# This fixes errors such as
# *** ERROR: ambiguous python shebang in /usr/bin/kvm_stat: #!/usr/bin/python. Change it to python3 (or python2) explicitly.
# We patch all sources below for which we got a report/error.
%{log_msg "Fixing Python shebangs..."}
%py3_shebang_fix \
    tools/kvm/kvm_stat/kvm_stat \
    scripts/show_delta \
    scripts/diffconfig \
    scripts/bloat-o-meter \
    scripts/jobserver-exec \
    tools \
    Documentation \
    scripts/clang-tools 2> /dev/null

# SBAT data
sed -e s,@KVER,%{KVERREL}, -e s,@SBAT_SUFFIX,%{sbat_suffix}, %{SOURCE83} > uki.sbat
sed -e s,@KVER,%{KVERREL}, -e s,@SBAT_SUFFIX,%{sbat_suffix}, %{SOURCE84} > uki-addons.sbat
sed -e s,@KVER,%{KVERREL}, -e s,@SBAT_SUFFIX,%{sbat_suffix}, %{SOURCE85} > kernel.sbat

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

if [ -L configs ]; then
    rm -f configs
fi
mkdir configs
cd configs

%{log_msg "Copy additional source files into buildroot"}
# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/%{name}-*.config .
cp %{SOURCE3001} .
%if %{with_native}
cat %{SOURCE3012} >> kernel-local
echo 'CONFIG_NR_CPUS=%(nproc --all)' >> kernel-local
%else
%if %{with_tune}
cat %{SOURCE3011} >> kernel-local
%else
cat %{SOURCE3013} >> kernel-local
%endif
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
%{log_msg "Collect custom defined config options"}
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
  *riscv64*) echo "riscv64" ;;
  # no arch, apply everywhere
  *) echo "" ;;
  esac
}

# Merge in any user-provided local config option changes
%{log_msg "Merge in any user-provided local config option changes"}
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

%if %{signkernel}%{signmodules}

# Add DUP and kpatch certificates to system trusted keys for RHEL
truncate -s0 ../certs/rhel.pem
%if 0%{?rhel}
%if %{rhelkeys}
%{log_msg "Add DUP and kpatch certificates to system trusted keys for RHEL"}
openssl x509 -inform der -in %{SOURCE100} -out rheldup3.pem
openssl x509 -inform der -in %{SOURCE101} -out rhelkpatch1.pem
openssl x509 -inform der -in %{SOURCE102} -out nvidiagpuoot001.pem
cat rheldup3.pem rhelkpatch1.pem nvidiagpuoot001.pem >> ../certs/rhel.pem
# rhelkeys
%endif
%if %{signkernel}
%ifarch s390x ppc64le
openssl x509 -inform der -in %{secureboot_ca_0} -out secureboot.pem
cat secureboot.pem >> ../certs/rhel.pem
%endif
%endif

# rhel
%endif

openssl x509 -inform der -in %{ima_ca_cert} -out imaca.pem
cat imaca.pem >> ../certs/rhel.pem

for i in *.config; do
  sed -i 's@CONFIG_SYSTEM_TRUSTED_KEYS=""@CONFIG_SYSTEM_TRUSTED_KEYS="certs/rhel.pem"@' $i
  sed -i 's@CONFIG_EFI_SBAT_FILE=""@CONFIG_EFI_SBAT_FILE="kernel.sbat"@' $i
done
%endif

# Adjust FIPS module name for RHEL
%if 0%{?rhel}
%{log_msg "Adjust FIPS module name for RHEL"}
for i in *.config; do
  sed -i 's/CONFIG_CRYPTO_FIPS_NAME=.*/CONFIG_CRYPTO_FIPS_NAME="Red Hat Enterprise Linux %{rhel} - Kernel Cryptographic API"/' $i
done
%endif

%{log_msg "Set process_configs.sh $OPTS"}
cp %{SOURCE81} .
OPTS="-w -n -c"
%if !%{with_configchecks}
  OPTS="$OPTS -i"
%endif
%if %{with clang_lto}
for opt in %{clang_make_opts}; do
  OPTS="$OPTS -m $opt"
done
%endif

%{log_msg "Generate redhat configs"}
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

%{log_msg "Set scripts/SOURCES targets"}
update_target=%{primary_target}
if [ "%{primary_target}" == "rhel" ]; then
: # no-op to avoid empty if-fi error
%if 0%{?centos}
  update_scripts $update_target
  %{log_msg "Updating scripts/sources to centos version"}
  update_target=centos
%endif
fi
update_scripts $update_target

%endif

%{log_msg "End of kernel config"}
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
%{log_msg "Start of build stage"}

%{log_msg "General arch build configuration"}
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
    %{log_msg "InitBuildVars for $1"}

    %{log_msg "InitBuildVars: Initialize build variables"}
    # Initialize the kernel .config file and create some variables that are
    # needed for the actual build process.

    Variant=$1

    # Pick the right kernel config file
    Config=%{name}-%{specrpmversion}-%{_target_cpu}${Variant:+-${Variant}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Variant:++${Variant}}

    KernelVer=%{specversion}-%{release}.%{_target_cpu}${Variant:++${Variant}}

    %{log_msg "InitBuildVars: Update Makefile"}
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

    %{log_msg "InitBuildVars: Copy files"}
    %{make} %{?_smp_mflags} mrproper
    cp configs/$Config .config

    %if %{signkernel}%{signmodules}
    cp configs/x509.genkey certs/.
    %endif

%if %{with_debuginfo} == 0
    sed -i 's/^\(CONFIG_DEBUG_INFO.*\)=y/# \1 is not set/' .config
%endif

    Arch=`head -1 .config | cut -b 3-`
    %{log_msg "InitBuildVars: USING ARCH=$Arch"}

    KCFLAGS="%{?kcflags}"
}

#Build bootstrap bpftool
BuildBpftool(){
    export BPFBOOTSTRAP_CFLAGS=$(echo "${CFLAGS}" | sed -r "s/\-specs=[^\ ]+\/redhat-annobin-cc1//")
    export BPFBOOTSTRAP_LDFLAGS=$(echo "${LDFLAGS}" | sed -r "s/\-specs=[^\ ]+\/redhat-annobin-cc1//")
    CFLAGS="" LDFLAGS="" make EXTRA_CFLAGS="${BPFBOOTSTRAP_CFLAGS}" EXTRA_CXXFLAGS="${BPFBOOTSTRAP_CFLAGS}" EXTRA_LDFLAGS="${BPFBOOTSTRAP_LDFLAGS}" %{?make_opts} %{?clang_make_opts} V=1 -C tools/bpf/bpftool bootstrap
}

BuildKernel() {
    %{log_msg "BuildKernel for $4"}
    MakeTarget=$1
    KernelImage=$2
    DoVDSO=$3
    Variant=$4
    InstallName=${5:-vmlinuz}

    %{log_msg "Setup variables"}
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
    %{log_msg "Setup build directories"}
    # Make build directory unique for each variant, so that gcno symlinks
    # are also unique for each variant.
    if [ -n "$Variant" ]; then
        ln -s $(pwd) ../linux-%{KVERREL}-${Variant}
    fi
    %{log_msg "GCOV - continuing build in: $(pwd)"}
    pushd ../linux-%{KVERREL}${Variant:+-${Variant}}
    pwd > ../kernel${Variant:+-${Variant}}-gcov.list
%endif

    %{log_msg "Calling InitBuildVars for $Variant"}
    InitBuildVars $Variant

    %{log_msg "BUILDING A KERNEL FOR ${Variant} %{_target_cpu}..."}

    %{make} ARCH=$Arch olddefconfig >/dev/null

    %{log_msg "Setup build-ids"}
    # This ensures build-ids are unique to allow parallel debuginfo
    perl -p -i -e "s/^CONFIG_BUILD_SALT.*/CONFIG_BUILD_SALT=\"%{KVERREL}\"/" .config
    %{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?kernel_mflags}
    if [ $DoModules -eq 1 ]; then
    %{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} modules %{?sparse_mflags} || exit 1
    fi

    %{log_msg "Setup RPM_BUILD_ROOT directories"}
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/systemtap
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif

%ifarch aarch64 riscv64
    %{log_msg "Build dtb kernel"}
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    %{make} ARCH=$Arch dtbs INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    %{make} ARCH=$Arch dtbs_install INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    cp -r $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/dtb
    find arch/$Arch/boot/dts -name '*.dtb' -type f -delete
%endif

    %{log_msg "Cleanup temp btf files"}
    # Remove large intermediate files we no longer need to save space
    # (-f required for zfcpdump builds that do not enable BTF)
    rm -f vmlinux.o .tmp_vmlinux.btf

    %{log_msg "Install files to RPM_BUILD_ROOT"}

    # Comment out specific config settings that may use resources not available
    # to the end user so that the packaged config file can be easily reused with
    # upstream make targets
    %if %{signkernel}%{signmodules}
      sed -i -e '/^CONFIG_SYSTEM_TRUSTED_KEYS/{
        i\# The kernel was built with
        s/^/# /
        a\# We are resetting this value to facilitate local builds
        a\CONFIG_SYSTEM_TRUSTED_KEYS=""
        }' .config
    %endif

    # Start installing the results
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/config
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/System.map

    %{log_msg "Reserving 40MB in boot for initramfs"}
    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=40

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      %{log_msg "Copy zImage.stub to RPM_BUILD_ROOT"}
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/lib/modules/$KernelVer/zImage.stub-$KernelVer || :
    fi

    %if %{signkernel}
    %{log_msg "Copy kernel for signing"}
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
    %{log_msg "Sign kernel image"}
    %pesign -s -i $SignImage -o vmlinuz.signed -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
    %endif
    %ifarch s390x ppc64le
    if [ -x /usr/bin/rpm-sign ]; then
      rpm-sign --key "%{pesign_name_0}" --lkmsign $SignImage --output vmlinuz.signed
    elif [ "$DoModules" == "1" -a "%{signmodules}" == "1" ]; then
      chmod +x scripts/sign-file
      ./scripts/sign-file -p sha256 certs/signing_key.pem certs/signing_key.x509 $SignImage vmlinuz.signed
    else
      mv $SignImage vmlinuz.signed
    fi
    %endif

    if [ ! -s vmlinuz.signed ]; then
        %{log_msg "pesigning failed"}
        exit 1
    fi
    mv vmlinuz.signed $SignImage
    # signkernel
    %endif

    %{log_msg "copy signed kernel"}
    $CopyKernel $KernelImage \
                $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    cp $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/$InstallName

    # hmac sign the kernel for FIPS
    %{log_msg "hmac sign the kernel for FIPS"}
    %{log_msg "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"}
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    (cd $RPM_BUILD_ROOT/%{image_install_path} && sha512hmac $InstallName-$KernelVer) > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;
    cp $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac $RPM_BUILD_ROOT/lib/modules/$KernelVer/.vmlinuz.hmac

    if [ $DoModules -eq 1 ]; then
      %{log_msg "Install modules in RPM_BUILD_ROOT"}
      # Override $(mod-fw) because we don't want it to install any firmware
      # we'll get it from the linux-firmware package and we don't want conflicts
      %{make} %{?_smp_mflags} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=
    fi

%if %{with_gcov}
    %{log_msg "install gcov-needed files to $BUILDROOT/$BUILD/"}
    # install gcov-needed files to $BUILDROOT/$BUILD/...:
    #   gcov_info->filename is absolute path
    #   gcno references to sources can use absolute paths (e.g. in out-of-tree builds)
    #   sysfs symlink targets (set up at compile time) use absolute paths to BUILD dir
    find . \( -name '*.gcno' -o -name '*.[chS]' \) -exec install -D '{}' "$RPM_BUILD_ROOT/$(pwd)/{}" \;
%endif

    %{log_msg "Add VDSO files"}
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

    %{log_msg "Save headers/makefiles, etc. for kernel-headers"}
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
    %{log_msg "GENERATING kernel ABI metadata"}
    %compression --stdout %compression_flags < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.%compext
    cp $RPM_BUILD_ROOT/boot/symvers-$KernelVer.%compext $RPM_BUILD_ROOT/lib/modules/$KernelVer/symvers.%compext

%if %{with_kabichk}
    %{log_msg "kABI checking is enabled in kernel SPEC file."}
    chmod 0755 $RPM_SOURCE_DIR/check-kabi
    if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Variant ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Variant $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
        %{log_msg "NOTE: Cannot find reference Module.kabi file."}
    fi
%endif

%if %{with_kabidupchk}
    %{log_msg "kABI DUP checking is enabled in kernel SPEC file."}
    if [ -e $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Variant ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Variant $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
        %{log_msg "NOTE: Cannot find DUP reference Module.kabi file."}
    fi
%endif

%if %{with_kabidw_base}
    # Don't build kabi base for debug kernels
    if [ "$Variant" != "zfcpdump" -a "$Variant" != "debug" ]; then
        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf
        tar -xvf %{SOURCE301} -C $RPM_BUILD_ROOT/kabi-dwarf

        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf/stablelists
        tar -xvf %{SOURCE300} -C $RPM_BUILD_ROOT/kabi-dwarf/stablelists

        %{log_msg "GENERATING DWARF-based kABI baseline dataset"}
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

            %{log_msg "GENERATING DWARF-based kABI dataset"}
            chmod 0755 $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh generate \
                "$RPM_BUILD_ROOT/kabi-dwarf/stablelists/kabi-current/kabi_stablelist_%{_target_cpu}" \
                "$(pwd)" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}.tmp" || :

            %{log_msg "kABI DWARF-based comparison report"}
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh compare \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}.tmp" || :
            %{log_msg "End of kABI DWARF-based comparison report"}
        else
            %{log_msg "Baseline dataset for kABI DWARF-BASED comparison report not found"}
        fi

        rm -rf $RPM_BUILD_ROOT/kabi-dwarf
    fi
%endif

    %{log_msg "Cleanup Makefiles/Kconfig files"}
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
    %{log_msg "Copy expoline.o"}
    if [ -f arch/s390/lib/expoline/expoline.o ]; then
      cp -a --parents arch/s390/lib/expoline/expoline.o $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
%endif

    %{log_msg "Copy additional files for make targets"}
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
    cp --parents tools/build/fixdep.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/sync-check.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/bpf/resolve_btfids $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    cp --parents security/selinux/include/policycap_names.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents security/selinux/include/policycap.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    cp -a --parents tools/include/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
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
    if [ -d tools/arch/%{asmarch}/include ]; then
      cp -a --parents tools/arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
%ifarch aarch64
    # arch/arm64/include/asm/xen references arch/arm
    cp -a --parents arch/arm/include/asm/xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    # arch/arm64/include/asm/opcodes.h references arch/arm
    cp -a --parents arch/arm/include/asm/opcodes.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    # Cross-reference from include/perf/events/sof.h
    cp -a sound/soc/sof/sof-audio.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/sound/soc/sof
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
    %{log_msg "Clean up intermediate tools files"}
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

    %{log_msg "Copy additional files for kernel-debuginfo rpm"}
    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    # (use mv + symlink instead of cp to reduce disk space requirements)
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    mv vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    ln -s $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux vmlinux
    if [ -n "%{?vmlinux_decompressor}" ]; then
      eu-readelf -n  %{vmlinux_decompressor} | grep "Build ID" | awk '{print $NF}' > vmlinux.decompressor.id
      # Without build-id the build will fail. But for s390 the build-id
      # wasn't added before 5.11. In case it is missing prefer not
      # packaging the debuginfo over a build failure.
      if [ -s vmlinux.decompressor.id ]; then
        cp vmlinux.decompressor.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.decompressor.id
        cp %{vmlinux_decompressor} $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux.decompressor
      fi
    fi

    # build and copy the vmlinux-gdb plugin files into kernel-debuginfo
    %{make} ARCH=$Arch %{?_smp_mflags} scripts_gdb
    cp -a --parents scripts/gdb/{,linux/}*.py $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    # this should be a relative symlink (Kbuild creates an absolute one)
    ln -s scripts/gdb/vmlinux-gdb.py $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux-gdb.py
    %py_byte_compile %{python3} $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/scripts/gdb
%endif

    %{log_msg "Create modnames"}
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.
    %{log_msg "Generate a list of modules for block and networking"}
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

    %{log_msg "detect missing or incorrect license tags"}
    # detect missing or incorrect license tags
    ( find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name '*.ko' | xargs /sbin/modinfo -l | \
        grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1


    if [ $DoModules -eq 0 ]; then
        %{log_msg "Create empty files for RPM packaging"}
        # Ensure important files/directories exist to let the packaging succeed
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-core.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-extra.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-internal.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-partner.list
        mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/kernel
        # Add files usually created by make modules, needed to prevent errors
        # thrown by depmod during package installation
        touch $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.order
        touch $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.builtin
    fi

    # Copy the System.map file for depmod to use
    cp System.map $RPM_BUILD_ROOT/.

    if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" || "$Variant" == "rt-64k" || "$Variant" == "rt-64k-debug" || "$Variant" == "automotive" || "$Variant" == "automotive-debug" ]]; then
        %{log_msg "Skipping efiuki build"}
    else
%if %{with_efiuki}
        %{log_msg "Setup the EFI UKI kernel"}
	KernelUnifiedImageDir="$RPM_BUILD_ROOT/lib/modules/$KernelVer"
    	KernelUnifiedImage="$KernelUnifiedImageDir/$InstallName-virt.efi"
	KernelUnifiedInitrd="$KernelUnifiedImageDir/$InstallName-virt.img"

    mkdir -p $KernelUnifiedImageDir

    dracut --conf=%{SOURCE86} \
           --confdir=$(mktemp -d) \
           --no-hostonly \
           --verbose \
           --kver "$KernelVer" \
           --kmoddir "$RPM_BUILD_ROOT/lib/modules/$KernelVer/" \
           --logfile=$(mktemp) \
    $KernelUnifiedInitrd

  ukify build --linux $(realpath $KernelImage) --initrd $KernelUnifiedInitrd \
     --sbat @uki.sbat --os-release @/etc/os-release --uname $KernelVer \
    --cmdline 'console=tty0 console=ttyS0' --output $KernelUnifiedImage

  rm -f $KernelUnifiedInitrd

  KernelAddonsDirOut="$KernelUnifiedImage.extra.d"
  mkdir -p $KernelAddonsDirOut
  python3 %{SOURCE151} %{SOURCE152} $KernelAddonsDirOut virt %{primary_target} %{_target_cpu} @uki-addons.sbat

%if %{signkernel}
    %{log_msg "Sign the EFI UKI kernel"}
%if 0%{?fedora}%{?eln}
        %pesign -s -i $KernelUnifiedImage -o $KernelUnifiedImage.signed -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
%else
%if 0%{?centos}
        UKI_secureboot_name=centossecureboot204
%else
        UKI_secureboot_name=redhatsecureboot504
%endif
        UKI_secureboot_cert=%{_datadir}/pki/sb-certs/secureboot-uki-virt-%{_arch}.cer

        %pesign -s -i $KernelUnifiedImage -o $KernelUnifiedImage.signed -a %{secureboot_ca_0} -c $UKI_secureboot_cert -n $UKI_secureboot_name
# 0%{?fedora}%{?eln}
%endif
        if [ ! -s $KernelUnifiedImage.signed ]; then
            echo "pesigning failed"
            exit 1
        fi
        mv $KernelUnifiedImage.signed $KernelUnifiedImage

      for addon in "$KernelAddonsDirOut"/*; do
        %pesign -s -i $addon -o $addon.signed -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
        rm -f $addon
        mv $addon.signed $addon
      done

# signkernel
%endif

    # hmac sign the UKI for FIPS
    KernelUnifiedImageHMAC="$KernelUnifiedImageDir/.$InstallName-virt.efi.hmac"
    %{log_msg "hmac sign the UKI for FIPS"}
    %{log_msg "Creating hmac file: $KernelUnifiedImageHMAC"}
    (cd $KernelUnifiedImageDir && sha512hmac $InstallName-virt.efi) > $KernelUnifiedImageHMAC;

# with_efiuki
%endif
    :  # in case of empty block
    fi # "$Variant" == "rt" || "$Variant" == "rt-debug" || "$Variant" == "automotive" || "$Variant" == "automotive-debug"


    #
    # Generate the modules files lists
    #
    move_kmod_list()
    {
        local module_list="$1"
        local subdir_name="$2"

        mkdir -p "$RPM_BUILD_ROOT/lib/modules/$KernelVer/$subdir_name"

        set +x
        while read -r kmod; do
            local target_file="$RPM_BUILD_ROOT/lib/modules/$KernelVer/$subdir_name/$kmod"
            local target_dir="${target_file%/*}"
            mkdir -p "$target_dir"
            mv "$RPM_BUILD_ROOT/lib/modules/$KernelVer/kernel/$kmod" "$target_dir"
        done < <(sed -e 's|^kernel/||' "$module_list")
        set -x
    }

    create_module_file_list()
    {
        # subdirectory within /lib/modules/$KernelVer where kmods should go
        local module_subdir="$1"
        # kmod list with relative paths produced by filtermods.py
        local relative_kmod_list="$2"
        # list with absolute paths to kmods and other files to be included
        local absolute_file_list="$3"
        # if 1, this adds also all kmod directories to absolute_file_list
        local add_all_dirs="$4"
        local run_mod_deny="$5"

        if [ "$module_subdir" != "kernel" ]; then
            # move kmods into subdirs if needed (internal, partner, extra,..)
            move_kmod_list $relative_kmod_list $module_subdir
        fi

        # make kmod paths absolute
        sed -e 's|^kernel/|/lib/modules/'$KernelVer'/'$module_subdir'/|' $relative_kmod_list > $absolute_file_list

        if [ "$run_mod_deny" -eq 1 ]; then
            # run deny-mod script, this adds blacklist-* files to absolute_file_list
            %{SOURCE20} "$RPM_BUILD_ROOT" lib/modules/$KernelVer $absolute_file_list
        fi

%if %{zipmodules}
        # deny-mod script works with kmods as they are now (not compressed),
        # but if they will be we need to add compext to all
        sed -i %{?zipsed} $absolute_file_list
%endif
        # add also dir for the case when there are no kmods
        # "kernel" subdir is covered in %%files section, skip it here
        if [ "$module_subdir" != "kernel" ]; then
                echo "%dir /lib/modules/$KernelVer/$module_subdir" >> $absolute_file_list
        fi

        if [ "$add_all_dirs" -eq 1 ]; then
            (cd $RPM_BUILD_ROOT; find lib/modules/$KernelVer/kernel -mindepth 1 -type d | sort -n) > ../module-dirs.list
            sed -e 's|^lib|%dir /lib|' ../module-dirs.list >> $absolute_file_list
        fi
    }

    if [ $DoModules -eq 1 ]; then
        # save modules.dep for debugging
        cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.dep ../

        %{log_msg "Create module list files for all kernel variants"}
        variants_param=""
        if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" ]]; then
            variants_param="-r rt"
        fi
        if [[ "$Variant" == "rt-64k" || "$Variant" == "rt-64k-debug" ]]; then
            variants_param="-r rt-64k"
        fi
        if [[ "$Variant" == "automotive" || "$Variant" == "automotive-debug" ]]; then
            variants_param="-r automotive"
        fi
        # this creates ../modules-*.list output, where each kmod path is as it
        # appears in modules.dep (relative to lib/modules/$KernelVer)
        ret=0
        %{SOURCE22} -l "../filtermods-$KernelVer.log" sort -d $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.dep -c configs/def_variants.yaml $variants_param -o .. || ret=$?
        if [ $ret -ne 0 ]; then
            echo "8< --- filtermods-$KernelVer.log ---"
            cat "../filtermods-$KernelVer.log"
            echo "--- filtermods-$KernelVer.log --- >8"

            echo "8< --- modules.dep ---"
            cat $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.dep
            echo "--- modules.dep --- >8"
            exit 1
        fi

        create_module_file_list "kernel" ../modules-core.list ../kernel${Variant:+-${Variant}}-modules-core.list 1 0
        create_module_file_list "kernel" ../modules.list ../kernel${Variant:+-${Variant}}-modules.list 0 0
        create_module_file_list "internal" ../modules-internal.list ../kernel${Variant:+-${Variant}}-modules-internal.list 0 1
        create_module_file_list "kernel" ../modules-extra.list ../kernel${Variant:+-${Variant}}-modules-extra.list 0 1
%if 0%{!?fedora:1}
        create_module_file_list "partner" ../modules-partner.list ../kernel${Variant:+-${Variant}}-modules-partner.list 1 1
%endif
    fi # $DoModules -eq 1

    remove_depmod_files()
    {
        # remove files that will be auto generated by depmod at rpm -i time
        pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
            # in case below list needs to be extended, remember to add a
            # matching ghost entry in the files section as well
            rm -f modules.{alias,alias.bin,builtin.alias.bin,builtin.bin} \
                  modules.{dep,dep.bin,devname,softdep,symbols,symbols.bin,weakdep}
        popd
    }

    # Cleanup
    %{log_msg "Cleanup build files"}
    rm -f $RPM_BUILD_ROOT/System.map
    %{log_msg "Remove depmod files"}
    remove_depmod_files

%if %{with_cross}
    make -C $RPM_BUILD_ROOT/lib/modules/$KernelVer/build M=scripts clean
    make -C $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/bpf/resolve_btfids clean
    sed -i 's/REBUILD_SCRIPTS_FOR_CROSS:=0/REBUILD_SCRIPTS_FOR_CROSS:=1/' $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile
%endif

    # Move the devel headers out of the root file system
    %{log_msg "Move the devel headers to RPM_BUILD_ROOT"}
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir

    # This is going to create a broken link during the build, but we don't use
    # it after this point.  We need the link to actually point to something
    # when kernel-devel is installed, and a relative link doesn't work across
    # the F17 UsrMove feature.
    ln -sf ../../../src/kernels/$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

%if %{with_debuginfo}
    # Generate vmlinux.h and put it to kernel-devel path
    # zfcpdump build does not have btf anymore
    if [ "$Variant" != "zfcpdump" ]; then
	%{log_msg "Build the bootstrap bpftool to generate vmlinux.h"}
        # Build the bootstrap bpftool to generate vmlinux.h
        BuildBpftool
        tools/bpf/bpftool/bootstrap/bpftool btf dump file vmlinux format c > $RPM_BUILD_ROOT/$DevelDir/vmlinux.h
    fi
%endif

    %{log_msg "Cleanup kernel-devel and kernel-debuginfo files"}
    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -delete
    # prune junk from kernel-debuginfo
    find $RPM_BUILD_ROOT/usr/src/kernels -name "*.mod.c" -delete

    # Red Hat UEFI Secure Boot CA cert, which can be used to authenticate the kernel
    %{log_msg "Install certs"}
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer
%if %{signkernel}
    install -m 0644 %{secureboot_ca_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
    %ifarch s390x ppc64le
    if [ -x /usr/bin/rpm-sign ]; then
        install -m 0644 %{secureboot_key_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
    fi
    %endif
%endif

%if 0%{?rhel}
    # Red Hat IMA code-signing cert, which is used to authenticate package files
    install -m 0644 %{ima_signing_cert} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{ima_cert_name}
%endif

%if %{signmodules}
    if [ $DoModules -eq 1 ]; then
        # Save the signing keys so we can sign the modules in __modsign_install_post
        cp certs/signing_key.pem certs/signing_key.pem.sign${Variant:++${Variant}}
        cp certs/signing_key.x509 certs/signing_key.x509.sign${Variant:++${Variant}}
        %ifarch s390x ppc64le
        if [ ! -x /usr/bin/rpm-sign ]; then
            install -m 0644 certs/signing_key.x509.sign${Variant:++${Variant}} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
            openssl x509 -in certs/signing_key.pem.sign${Variant:++${Variant}} -outform der -out $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
            chmod 0644 $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
        fi
        %endif
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
BuildKernel %make_target %kernel_image %{_use_vdso} rt-debug
%endif

%if %{with_realtime_arm64_64k}
BuildKernel %make_target %kernel_image %{_use_vdso} rt-64k-debug
%endif

%if %{with_automotive} && !%{with_automotive_build}
BuildKernel %make_target %kernel_image %{_use_vdso} automotive-debug
%endif

%if %{with_arm64_16k}
BuildKernel %make_target %kernel_image %{_use_vdso} 16k-debug
%endif

%if %{with_arm64_64k}
BuildKernel %make_target %kernel_image %{_use_vdso} 64k-debug
%endif

%if %{with_up}
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

%if %{with_realtime_arm64_64k_base}
BuildKernel %make_target %kernel_image %{_use_vdso} rt-64k
%endif

%if %{with_automotive_base}
BuildKernel %make_target %kernel_image %{_use_vdso} automotive
%endif

%if %{with_up_base}
BuildKernel %make_target %kernel_image %{_use_vdso}
%endif

%ifnarch noarch i686 %{nobuildarches}
%if !%{with_debug} && !%{with_zfcpdump} && !%{with_up} && !%{with_arm64_16k} && !%{with_arm64_64k} && !%{with_realtime} && !%{with_realtime_arm64_64k} && !%{with_automotive}
# If only building the user space tools, then initialize the build environment
# and some variables so that the various userspace tools can be built.
%{log_msg "Initialize userspace tools build environment"}
InitBuildVars
# Some tests build also modules, and need Module.symvers
if ! [[ -e Module.symvers ]] && [[ -f $DevelDir/Module.symvers ]]; then
    %{log_msg "Found Module.symvers in DevelDir, copying to ."}
    cp "$DevelDir/Module.symvers" .
fi
%endif
%endif

%ifarch aarch64
%global perf_build_extra_opts CORESIGHT=1
%endif
%global perf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${CFLAGS}" EXTRA_CXXFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS} -Wl,-E" %{?cross_opts} -C tools/perf V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 LIBTRACEEVENT_DYNAMIC=1 %{?perf_build_extra_opts} prefix=%{_prefix} PYTHON=%{__python3}
%if %{with_perf}
%{log_msg "Build perf"}
# perf
# make sure check-headers.sh is executable
chmod +x tools/perf/check-headers.sh
%{perf_make} JOBS=%{_smp_build_ncpus} DESTDIR=$RPM_BUILD_ROOT all
%endif

%if %{with_libperf}
%global libperf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" %{?cross_opts} -C tools/lib/perf V=1
  %{log_msg "build libperf"}
%{libperf_make} JOBS=%{_smp_build_ncpus} DESTDIR=$RPM_BUILD_ROOT
%endif

%global tools_make \
  CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" EXTRA_CFLAGS="${CFLAGS}" %{make} %{?make_opts}

%ifarch %{cpupowerarchs}
    # link against in-tree libcpupower for idle state support
    %global rtla_make %{tools_make} LDFLAGS="${LDFLAGS} -L../../power/cpupower" INCLUDES="-I../../power/cpupower/lib"
    # Build libcpupower Python bindings
    %global libcpupower_python_bindings_make %{tools_make} LDFLAGS="-L%{buildroot}%{_libdir} -lcpupower"
%else
    %global rtla_make %{tools_make}
%endif

%if %{with_tools}
sed -e 's|-O6|-O2|g' -i tools/lib/{api,subcmd}/Makefile tools/perf/Makefile.config

%if %{with_ynl}
pushd tools/net/ynl
export PIP_CONFIG_FILE=/tmp/pip.config
cat <<EOF > $PIP_CONFIG_FILE
[install]
no-index = true
no-build-isolation = false
EOF
%{tools_make} %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
popd
%endif

%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%{log_msg "build cpupower"}
%{tools_make} %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false DEBUG=false
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    %{log_msg "build centrino-decode powernow-k8-decode"}
    %{tools_make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   %{log_msg "build x86_energy_perf_policy"}
   %{tools_make}
   popd
   pushd tools/power/x86/turbostat
   %{log_msg "build turbostat"}
   %{tools_make}
   popd
   pushd tools/power/x86/intel-speed-select
   %{log_msg "build intel-speed-select"}
   %{tools_make}
   popd
   pushd tools/arch/x86/intel_sdsi
   %{log_msg "build intel_sdsi"}
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}"
   popd
%endif
%endif
pushd tools/thermal/tmon/
%{log_msg "build tmon"}
%{tools_make}
popd
pushd tools/bootconfig/
%{log_msg "build bootconfig"}
%{tools_make}
popd
pushd tools/iio/
%{log_msg "build iio"}
%{tools_make}
popd
pushd tools/gpio/
%{log_msg "build gpio"}
%{tools_make}
popd
# build VM tools
pushd tools/mm/
%{log_msg "build slabinfo page_owner_sort"}
%{tools_make} slabinfo page_owner_sort
popd
pushd tools/verification/rv/
%{log_msg "build rv"}
%{tools_make}
popd
pushd tools/tracing/rtla
%{log_msg "build rtla"}
%{rtla_make}
popd
%endif

#set RPM_VMLINUX_H
if [ -f $RPM_BUILD_ROOT/$DevelDir/vmlinux.h ]; then
  RPM_VMLINUX_H=$RPM_BUILD_ROOT/$DevelDir/vmlinux.h
elif [ -f $DevelDir/vmlinux.h ]; then
  RPM_VMLINUX_H=$DevelDir/vmlinux.h
fi
echo "${RPM_VMLINUX_H}" > ../vmlinux_h_path

%if %{with_selftests}
%{log_msg "start build selftests"}
# Unfortunately, samples/bpf/Makefile expects that the headers are installed
# in the source tree. We installed them previously to $RPM_BUILD_ROOT/usr
# but there's no way to tell the Makefile to take them from there.
%{log_msg "install headers for selftests"}
%{make} %{?_smp_mflags} headers_install

# If we re building only tools without kernel, we need to generate config
# headers and prepare tree for modules building. The modules_prepare target
# will cover both.
if [ ! -f include/generated/autoconf.h ]; then
   %{log_msg "modules_prepare for selftests"}
   %{make} %{?_smp_mflags} modules_prepare
fi

# Build BPFtool for samples/bpf
if [ ! -f tools/bpf/bpftool/bootstrap/bpftool ]; then
  BuildBpftool
fi

%{log_msg "build samples/bpf"}
%{make} %{?_smp_mflags} EXTRA_CXXFLAGS="${CXXFLAGS}" ARCH=$Arch BPFTOOL=$(pwd)/tools/bpf/bpftool/bootstrap/bpftool V=1 M=samples/bpf/ VMLINUX_H="${RPM_VMLINUX_H}" || true

pushd tools/testing/selftests
# We need to install here because we need to call make with ARCH set which
# doesn't seem possible to do in the install section.
%if %{selftests_must_build}
  force_targets="FORCE_TARGETS=1"
%else
  force_targets=""
%endif

%{log_msg "main selftests compile"}

# Some selftests (especially bpf) do not build with source fortification.
# Since selftests are not shipped, disable source fortification for them.
%global _fortify_level_bak %{_fortify_level}
%undefine _fortify_level
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"

%{make} %{?_smp_mflags} EXTRA_CFLAGS="${CFLAGS}" ARCH=$Arch V=1 TARGETS="bpf cgroup kmod mm net net/forwarding net/mptcp net/netfilter net/packetdrill tc-testing memfd drivers/net drivers/net/hw iommu cachestat pid_namespace rlimits timens pidfd" SKIP_TARGETS="" $force_targets INSTALL_PATH=%{buildroot}%{_libexecdir}/kselftests VMLINUX_H="${RPM_VMLINUX_H}" install

# Restore the original level of source fortification
%define _fortify_level %{_fortify_level_bak}
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"

# 'make install' for bpf is broken and upstream refuses to fix it.
# Install the needed files manually.
%{log_msg "install selftests"}
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

# The urandom_read binary doesn't pass the check-rpaths check and upstream
# refuses to fix it. So, we save it to buildroot_unstripped and delete it so it
# will be hidden from check-rpaths and will automatically get restored later.
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/urandom_read"
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/no_alu32/urandom_read"
rm -f %{buildroot}/usr/libexec/kselftests/bpf/urandom_read
rm -f %{buildroot}/usr/libexec/kselftests/bpf/no_alu32/urandom_read

# Copy bpftool to kselftests so selftests is packaged with
# the full bpftool instead of bootstrap bpftool
cp ./bpf/tools/sbin/bpftool %{buildroot}%{_libexecdir}/kselftests/bpf/bpftool

popd
%{log_msg "end build selftests"}
%endif

%if %{with_doc}
%{log_msg "start install docs"}
# Make the HTML pages.
%{log_msg "build html docs"}
%{__make} PYTHON=/usr/bin/python3 htmldocs || %{doc_build_fail}

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w
%{log_msg "end install docs"}
%endif

# Module signing (modsign)
#
# This must be run _after_ find-debuginfo.sh runs, otherwise that will strip
# the signature off of the modules.
#
# Don't sign modules for the zfcpdump variant as it is monolithic.

%define __modsign_install_post \
  if [ "%{signmodules}" -eq "1" ]; then \
    %{log_msg "Signing kernel modules ..."} \
    modules_dirs="$(shopt -s nullglob; echo $RPM_BUILD_ROOT/lib/modules/%{KVERREL}*)" \
    for modules_dir in $modules_dirs; do \
        variant_suffix="${modules_dir#$RPM_BUILD_ROOT/lib/modules/%{KVERREL}}" \
        [ "$variant_suffix" == "+zfcpdump" ] && continue \
        %{log_msg "Signing modules for %{KVERREL}${variant_suffix}"} \
        %{modsign_cmd} certs/signing_key.pem.sign${variant_suffix} certs/signing_key.x509.sign${variant_suffix} $modules_dir/ \
    done \
  fi \
  if [ "%{zipmodules}" -eq "1" ]; then \
    %{log_msg "Compressing kernel modules ..."} \
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

# Make debugedit and gdb-add-index use target versions of tools
# when cross-compiling. This is supported since debugedit-5.1-5.fc42
# https://inbox.sourceware.org/debugedit/20250220153858.963312-1-mark@klomp.org/
%if %{with_cross}
%define __override_target_tools_for_debugedit \
	export OBJCOPY=%{_build_arch}-linux-gnu-objcopy \
	export NM=%{_build_arch}-linux-gnu-nm \
	export READELF=%{_build_arch}-linux-gnu-readelf \
%{nil}
%endif

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__override_target_tools_for_debugedit:%{__override_target_tools_for_debugedit}}\
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

# re-define RPM_VMLINUX_H, because it doesn't carry over from %%build
RPM_VMLINUX_H="$(cat ../vmlinux_h_path)"

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
HDR_ARCH_LIST='arm64 powerpc s390 x86 riscv'
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
%{make} -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} libexecdir=%{_libexecdir} mandir=%{_mandir} unitdir=%{_unitdir} CPUFREQ_BENCH=false install
%find_lang cpupower
mv cpupower.lang ../
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
%{log_msg "Build libcpupower Python bindings"}
pushd tools/power/cpupower/bindings/python
%{libcpupower_python_bindings_make}
%{log_msg "Install libcpupower Python bindings"}
%{make} INSTALL_DIR=$RPM_BUILD_ROOT%{python3_sitearch} install
popd
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
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}" DESTDIR=%{buildroot} BINDIR=%{_sbindir} install
   popd
%endif
pushd tools/thermal/tmon
%{tools_make} INSTALL_ROOT=%{buildroot} install
popd
pushd tools/bootconfig
%{tools_make} DESTDIR=%{buildroot} install
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
# install cgroup selftests
pushd tools/testing/selftests/cgroup
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/cgroup/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/cgroup/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/cgroup/{} \;
popd
# install drivers/net selftests
pushd tools/testing/selftests/drivers/net
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/{} \;
popd
# install drivers/net/mlxsw selftests
pushd tools/testing/selftests/drivers/net/mlxsw
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
popd
# install drivers/net/hw selftests
pushd tools/testing/selftests/drivers/net/hw
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/hw/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/hw/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/hw/{} \;
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
# install net/netfilter selftests
pushd tools/testing/selftests/net/netfilter
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/netfilter/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/netfilter/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/netfilter/{} \;
popd
# install net/packetdrill selftests
pushd tools/testing/selftests/net/packetdrill
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/packetdrill/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/packetdrill/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/packetdrill/{} \;
popd

# install memfd selftests
pushd tools/testing/selftests/memfd
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
popd
# install iommu selftests
pushd tools/testing/selftests/iommu
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/iommu/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/iommu/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/iommu/{} \;
popd
# install rlimits selftests
pushd tools/testing/selftests/rlimits
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/rlimits/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/rlimits/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/rlimits/{} \;
popd
# install pid_namespace selftests
pushd tools/testing/selftests/pid_namespace
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/pid_namespace/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/pid_namespace/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/pid_namespace/{} \;
popd
# install timens selftests
pushd tools/testing/selftests/timens
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/timens/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/timens/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/timens/{} \;
popd
# install pidfd selftests
pushd tools/testing/selftests/pidfd
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/pidfd/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/pidfd/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/pidfd/{} \;
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
%if %{with_cross}\
    echo "Building scripts and resolve_btfids"\
    env --unset=ARCH make -C /usr/src/kernels/%{KVERREL}%{?1:+%{1}} prepare_after_cross\
%endif\
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
%if !%{with_automotive}\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --add-kernel %{KVERREL}%{?-v:+%{-v*}} || exit $?\
fi\
%endif\
%endif\
rm -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL}%{?-v:+%{-v*}}\
/bin/kernel-install add %{KVERREL}%{?-v:+%{-v*}} /lib/modules/%{KVERREL}%{?-v:+%{-v*}}/vmlinuz%{?-u:-%{-u*}.efi} || exit $?\
if [[ ! -e "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext" ]]; then\
    cp "/lib/modules/%{KVERREL}%{?-v:+%{-v*}}/symvers.%compext" "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext"\
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
#	%%kernel_variant_preun [-v <subpackage>] -u [uki-suffix] -e
# Add kernel-install's --entry-type=type1|type2|all option (if supported) to limit removal
# to a specific boot entry type.
#
%define kernel_variant_preun(v:u:e) \
%{expand:%%preun %{?-v:%{-v*}-}%{!?-u*:core}%{?-u*:uki-%{-u*}}}\
entry_type=""\
%{-e: \
/bin/kernel-install --help|grep -q -- '--entry-type=' &&\
    entry_type="--entry-type %{!?-u:type1}%{?-u:type2}" \
}\
/bin/kernel-install remove %{KVERREL}%{?-v:+%{-v*}} $entry_type || exit $?\
%if !%{with_automotive}\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --remove-kernel %{KVERREL}%{?-v:+%{-v*}} || exit $?\
fi\
%endif\
%{nil}

%if %{with_up_base} && %{with_efiuki}
%kernel_variant_posttrans -u virt
%kernel_variant_preun -u virt -e
%endif

%if %{with_up_base}
%kernel_variant_preun -e
%kernel_variant_post
%endif

%if %{with_zfcpdump}
%kernel_variant_preun -v zfcpdump
%kernel_variant_post -v zfcpdump
%endif

%if %{with_up} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v debug -u virt
%kernel_variant_preun -v debug -u virt -e
%endif

%if %{with_up} && %{with_debug}
%kernel_variant_preun -v debug -e
%kernel_variant_post -v debug
%endif

%if %{with_arm64_16k_base}
%kernel_variant_preun -v 16k -e
%kernel_variant_post -v 16k
%endif

%if %{with_debug} && %{with_arm64_16k}
%kernel_variant_preun -v 16k-debug -e
%kernel_variant_post -v 16k-debug
%endif

%if %{with_arm64_16k} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v 16k-debug -u virt
%kernel_variant_preun -v 16k-debug -u virt -e
%endif

%if %{with_arm64_16k_base} && %{with_efiuki}
%kernel_variant_posttrans -v 16k -u virt
%kernel_variant_preun -v 16k -u virt -e
%endif

%if %{with_arm64_64k_base}
%kernel_variant_preun -v 64k -e
%kernel_variant_post -v 64k
%endif

%if %{with_debug} && %{with_arm64_64k}
%kernel_variant_preun -v 64k-debug -e
%kernel_variant_post -v 64k-debug
%endif

%if %{with_arm64_64k} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v 64k-debug -u virt
%kernel_variant_preun -v 64k-debug -u virt -e
%endif

%if %{with_arm64_64k_base} && %{with_efiuki}
%kernel_variant_posttrans -v 64k -u virt
%kernel_variant_preun -v 64k -u virt -e
%endif

%if %{with_realtime_base}
%kernel_variant_preun -v rt
%kernel_variant_post -v rt -r kernel
%endif

%if %{with_automotive_base}
%kernel_variant_preun -v automotive
%kernel_variant_post -v automotive -r kernel
%endif

%if %{with_realtime} && %{with_debug}
%kernel_variant_preun -v rt-debug
%kernel_variant_post -v rt-debug
%endif

%if %{with_realtime_arm64_64k_base}
%kernel_variant_preun -v rt-64k
%kernel_variant_post -v rt-64k
%kernel_kvm_post rt-64k
%endif

%if %{with_debug} && %{with_realtime_arm64_64k}
%kernel_variant_preun -v rt-64k-debug
%kernel_variant_post -v rt-64k-debug
%kernel_kvm_post rt-64k-debug
%endif

%if %{with_automotive} && %{with_debug} && !%{with_automotive_build}
%kernel_variant_preun -v automotive-debug
%kernel_variant_post -v automotive-debug
%endif

###
### file lists
###

%if %{with_headers}
%files headers
/usr/include/*
%exclude %{_includedir}/cpufreq.h
%if %{with_ynl}
%exclude %{_includedir}/ynl
%endif
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
%ifarch x86_64 s390x ppc64 ppc64le aarch64 riscv64
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
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc linux-%{KVERREL}/tools/perf/Documentation/examples.txt
%{_docdir}/perf-tip/tips.txt
%{_includedir}/perf/perf_dlfilter.h

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

%if %{with_debuginfo}
%files -f libperf-debuginfo.list -n libperf-debuginfo
%endif

# with_libperf
%endif


%if %{with_tools}
%ifnarch %{cpupowerarchs}
%files -n kernel-tools
%else
%files -n kernel-tools -f cpupower.lang
%{_bindir}/cpupower
%{_libexecdir}/cpupower
%{_unitdir}/cpupower.service
%config(noreplace) %{_sysconfdir}/cpupower-service.conf
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
%{_bindir}/bootconfig
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
%if %{with_ynl}
%{_bindir}/ynl*
%{_docdir}/ynl
%{_datadir}/ynl
%{python3_sitelib}/pyynl*
%endif

%if %{with_debuginfo}
%files -f kernel-tools-debuginfo.list -n kernel-tools-debuginfo
%endif

%files -n kernel-tools-libs
%ifarch %{cpupowerarchs}
%{_libdir}/libcpupower.so.1
%{_libdir}/libcpupower.so.1.0.1
%endif

%files -n kernel-tools-libs-devel
%ifarch %{cpupowerarchs}
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_includedir}/powercap.h
# libcpupower Python bindings
%{python3_sitearch}/_raw_pylibcpupower.so
%{python3_sitearch}/raw_pylibcpupower.py
%endif
%if %{with_ynl}
%{_libdir}/libynl*
%{_includedir}/ynl
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
%{_mandir}/man1/rv-mon-sched.1.gz
%{_mandir}/man1/rv.1.gz

# with_tools
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
%ifarch aarch64 riscv64\
/lib/modules/%{KVERREL}%{?3:+%{3}}/dtb \
%ghost /%{image_install_path}/dtb-%{KVERREL}%{?3:+%{3}} \
%endif\
/lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
%ghost /boot/System.map-%{KVERREL}%{?3:+%{3}}\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/symvers.%compext\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin*\
%ghost %attr(0644, root, root) /boot/symvers-%{KVERREL}%{?3:+%{3}}.%compext\
%ghost %attr(0600, root, root) /boot/initramfs-%{KVERREL}%{?3:+%{3}}.img\
%ghost %attr(0644, root, root) /boot/config-%{KVERREL}%{?3:+%{3}}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-core.list %{?3:%{3}-}modules-core}\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
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
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.weakdep\
%{expand:%%files -f kernel-%{?3:%{3}-}modules.list %{?3:%{3}-}modules}\
%{expand:%%files %{?3:%{3}-}devel}\
%defverify(not mtime)\
/usr/src/kernels/%{KVERREL}%{?3:+%{3}}\
%{expand:%%files %{?3:%{3}-}devel-matched}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-extra.list %{?3:%{3}-}modules-extra}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-internal.list %{?3:%{3}-}modules-internal}\
%if 0%{!?fedora:1}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-partner.list %{?3:%{3}-}modules-partner}\
%endif\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?3}.list %{?3:%{3}-}debuginfo}\
%endif\
%endif\
%if %{with_efiuki} && "%{3}" != "rt" && "%{3}" != "rt-debug" && "%{3}" != "rt-64k" && "%{3}" != "rt-64k-debug"\
%{expand:%%files %{?3:%{3}-}uki-virt}\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
/lib/modules/%{KVERREL}%{?3:+%{3}}/symvers.%compext\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin*\
%attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi\
%attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/.%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi.hmac\
%ghost /%{image_install_path}/efi/EFI/Linux/%{?-k:%{-k*}}%{!?-k:*}-%{KVERREL}%{?3:+%{3}}.efi\
%{expand:%%files %{?3:%{3}-}uki-virt-addons}\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi.extra.d/ \
/lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi.extra.d/*.addon.efi\
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
%kernel_variant_files %{_use_vdso} %{with_automotive_base} automotive
%if %{with_automotive} && !%{with_automotive_build}
%kernel_variant_files %{_use_vdso} %{with_debug} automotive-debug
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
%kernel_variant_files %{_use_vdso} %{with_realtime_arm64_64k_base} rt-64k
%if %{with_realtime_arm64_64k}
%kernel_variant_files %{_use_vdso} %{with_debug} rt-64k-debug
%endif

%ifnarch noarch %{nobuildarches}
%files modules-extra-matched
%endif

# plz don't put in a version string unless you're going to tag
# and build.
#
#
%changelog
* Sun Oct 12 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.1-500.chinfo
- 6.17.2

* Mon Oct 06 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.1-500.chinfo
- 6.17.1

* Mon Sep 29 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.0-500.chinfo
- 6.17.0

* Thu Sep 25 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.9-500.chinfo
- 6.16.9

* Fri Sep 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.8-500.chinfo
- 6.16.8

* Tue Sep 16 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.7-500.chinfo
- 6.16.7

* Tue Sep 09 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.6-500.chinfo
- 6.16.6

* Thu Sep 04 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.5-500.chinfo
- 6.16.5

* Thu Aug 28 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.4-500.chinfo
- 6.16.4

* Sat Aug 23 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.3-500.chinfo
- 6.16.3

* Wed Aug 20 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.2-500.chinfo
- 6.16.2

* Tue Aug 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.1-501.chinfo
- Assorted fixes

* Fri Aug 15 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.1-500.chinfo
- 6.16.1

* Mon Jul 28 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.0-500.chinfo
- 6.16.0

* Thu Jul 24 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.8-500.chinfo
- 6.15.8

* Thu Jul 17 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.7-500.chinfo
- 6.15.7

* Thu Jul 10 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.6-500.chinfo
- 6.15.6

* Fri Jun 27 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.5-500.chinfo
- 6.15.5

* Fri Jun 27 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.4-500.chinfo
- 6.15.4

* Thu Jun 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.3-500.chinfo
- 6.15.3

* Tue Jun 10 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.2-500.chinfo
- 6.15.2

* Thu Jun 05 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.1-500.chinfo
- 6.15.1

* Mon May 26 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.0-500.chinfo
- 6.15.0
- Remove graysky patch

* Thu May 22 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.8-500.chinfo
- 6.14.8

* Sun May 18 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.7-500.chinfo
- 6.14.7

* Fri May 02 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.6-500.chinfo
- 6.14.6

* Fri May 02 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.6-500.chinfo
- 6.14.5

* Fri Apr 25 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.4-500.chinfo
- 6.14.4

* Sun Apr 20 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.3-500.chinfo
- 6.14.3

* Thu Apr 10 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.2-500.chinfo
- 6.14.2

* Mon Apr 07 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.1-500.chinfo
- 6.14.1

* Mon Mar 24 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.0-500.chinfo
- 6.14.0

* Sat Mar 22 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.8-500.chinfo
- 6.13.8

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.7-501.chinfo
- gcc 15 fixes

* Thu Mar 13 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.7-500.chinfo
- 6.13.7

* Fri Mar 07 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.6-500.chinfo
- 6.13.6

* Thu Feb 27 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.5-500.chinfo
- 6.13.5

* Fri Feb 21 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.4-500.chinfo
- 6.13.4

* Mon Feb 17 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.3-500.chinfo
- 6.13.3

* Sat Feb 08 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.2-500.chinfo
- 6.13.2

* Sat Feb 01 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.1-500.chinfo
- 6.13.1

* Tue Jan 21 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.0-500.chinfo
- 6.13.0

* Sat Jan 18 2025 Phantom X <megaphantomx at hotmail dot com> - 6.12.10-500.chinfo
- 6.12.10

* Mon Jan 13 2025 Phantom X <megaphantomx at hotmail dot com> - 6.12.9-501.chinfo
- invlpgb (patches from Zen)

* Thu Jan 09 2025 Phantom X <megaphantomx at hotmail dot com> - 6.12.9-500.chinfo
- 6.12.9

* Thu Jan 02 2025 Phantom X <megaphantomx at hotmail dot com> - 6.12.8-500.chinfo
- 6.12.8

* Fri Dec 27 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.7-500.chinfo
- 6.12.7

* Thu Dec 19 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.6-500.chinfo
- 6.12.6

* Sat Dec 14 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.5-500.chinfo
- 6.12.5

* Mon Dec 09 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.4-500.chinfo
- 6.12.4

* Fri Dec 06 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.3-500.chinfo
- 6.12.3

* Thu Dec 05 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.2-500.chinfo
- 6.12.2

* Fri Nov 22 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.1-500.chinfo
- 6.12.1

* Wed Nov 20 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.0-501.chinfo
- Add full ntsync and vhba modules (patches from Zen)

* Mon Nov 18 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.0-500.chinfo
- 6.12.0

* Sun Nov 17 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.9-500.chinfo
- 6.11.9

* Thu Nov 14 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.8-500.chinfo
- 6.11.8

* Fri Nov 08 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.7-500.chinfo
- 6.11.7

* Sun Nov 03 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.6-502.chinfo
- btrfs fixes

* Sat Nov 02 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.6-501.chinfo
- pf patch fix

* Thu Oct 31 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.6-500.chinfo
- 6.11.6

* Tue Oct 22 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.5-500.chinfo
- 6.11.5

* Thu Oct 17 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.4-500.chinfo
- 6.11.4

* Thu Oct 10 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.3-500.chinfo
- 6.11.3

* Fri Oct 04 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.2-500.chinfo
- 6.11.2

* Mon Sep 30 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.1-500.chinfo
- 6.11.1

* Sun Sep 15 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.0-500.chinfo
- 6.11.0

###
# The following Emacs magic makes C-c C-e use UTC dates.
# Local Variables:
# rpm-change-log-uses-utc: t
# End:
###
