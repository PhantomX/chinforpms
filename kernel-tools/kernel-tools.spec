# Much of this is borrowed from the original kernel.spec
# It needs a bunch of the macros for rawhide vs. not-rawhide builds.

# The kernel tools build with -ggdb3 which seems to interact badly with LTO
# causing various errors with references to discarded sections and symbol
# type errors from the LTO plugin.  Until those issues are addressed
# disable LTO
%global _lto_cflags %{nil}
%global __brp_strip_lto /usr/bin/true

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1
%global baserelease 500
%global fedora_build %{baserelease}

#global buildid .chinfo

%global opensuse_id 6d1d0389ca8e0089bb088a35ae097df2d87df746

%define major_ver 5

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%global base_sublevel 19

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%global stable_update 7
# Set rpm version accordingly
%if 0%{?stable_update}
%global stablerev %{stable_update}
%global stable_base %{stable_update}
%endif
%global rpmversion %{major_ver}.%{base_sublevel}.%{stable_update}

## The not-released-kernel case ##
%else
# The next upstream release sublevel (base_sublevel+1)
%global upstream_sublevel %(echo $((%{base_sublevel} + 1)))
# The rc snapshot level
%global rcrev 0
# Set rpm version accordingly
%global rpmversion %{major_ver}.%{upstream_sublevel}.0
%endif
# Nb: The above rcrev values automagically define Patch00 and Patch01 below.

# pkg_release is what we'll fill in for the rpm Release: field
%if 0%{?released_kernel}

%global pkg_release %{fedora_build}%{?buildid}%{?dist}

%else

# non-released_kernel
%if 0%{?rcrev}
%global rctag .rc%rcrev
%else
%global rctag .rc0
%endif
%global gittag .git0
%global pkg_release 0%{?rctag}%{?gittag}.%{fedora_build}%{?buildid}%{?dist}

%endif

# The kernel tarball/base version
%global kversion %{major_ver}.%{base_sublevel}
%global KVERREL %{version}-%{release}.%{_target_cpu}

# perf needs this
%undefine _strict_symbol_defs_build

Name:           kernel-tools
Summary:        Assortment of tools for the Linux kernel
License:        GPLv2
URL:            http://www.kernel.org/
Version:        %{rpmversion}
Release:        %{pkg_release}

Source0: https://cdn.kernel.org/pub/linux/kernel/v%{major_ver}.x/linux-%{kversion}.tar.xz

# Sources for kernel-tools
Source2000: cpupower.service
Source2001: cpupower.config

# Here should be only the patches up to the upstream canonical Linus tree.

# For a stable release kernel
%if 0%{?stable_base}
Source5000: https://cdn.kernel.org/pub/linux/kernel/v%{major_ver}.x/patch-%{major_ver}.%{base_sublevel}.%{stable_base}.xz
%else
# non-released_kernel case
# These are automagically defined by the rcrev value set up
# near the top of this spec file.
%if 0%{?rcrev}
Source5000: patch-%{major_ver}.%{upstream_sublevel}-rc%{rcrev}.xz
%endif
%endif

# rpmlint cleanup
Patch6: 0002-perf-Don-t-make-sourced-script-executable.patch


# Extra

### openSUSE patches - http://kernel.opensuse.org/cgit/kernel-source/

#global opensuse_url https://kernel.opensuse.org/cgit/kernel-source/plain/patches.suse
%global opensuse_url https://github.com/openSUSE/kernel-source/raw/%{opensuse_id}/patches.suse

Provides:       cpupowerutils = 1:009-0.6.p1
Obsoletes:      cpupowerutils < 1:009-0.6.p1
Provides:       cpufreq-utils = 1:009-0.6.p1
Provides:       cpufrequtils = 1:009-0.6.p1
Obsoletes:      cpufreq-utils < 1:009-0.6.p1
Obsoletes:      cpufrequtils < 1:009-0.6.p1
Obsoletes:      cpuspeed < 1:1.5-16
Requires:       kernel-tools-libs = %{version}-%{release}

BuildRequires: kmod, patch, bash, tar, git-core
BuildRequires: bzip2, xz, findutils, gzip, m4, perl-interpreter, perl(Carp), perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: zlib-devel binutils-devel newt-devel python3-docutils perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel glibc-devel glibc-headers glibc-static python3-devel java-devel
BuildRequires: asciidoc libxslt-devel xmlto libcap-devel
BuildRequires: openssl-devel libbabeltrace-devel
BuildRequires: libtracefs-devel libtraceevent-devel
BuildRequires: libbpf-devel
BuildRequires: clang llvm
# Used to mangle unversioned shebangs to be Python 3
BuildRequires: /usr/bin/pathfix.py
%ifnarch s390x %{arm}
BuildRequires: numactl-devel
%endif
%ifarch aarch64
BuildRequires: opencsd-devel >= 1.0.0
%endif
%ifarch i686 x86_64
BuildRequires: libnl3-devel
%endif
BuildRequires: pciutils-devel gettext ncurses-devel
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
BuildRequires: rpm-build, elfutils
%{?systemd_requires}
BuildRequires: systemd

%description
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package -n perf
Summary:        Performance monitoring for the Linux kernel
License:        GPLv2

%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%global python_perf_sum Python bindings for apps which will manipulate perf events
%global python_perf_desc A Python module that permits applications \
written in the Python programming language to use the interface \
to manipulate perf events.

%package -n python3-perf
Summary: %{python_perf_sum}
%{?python_provide:%python_provide python3-perf}

%description -n python3-perf
%{python_perf_desc}

%package -n kernel-tools-libs
Summary:        Libraries for the kernels-tools
License:        GPLv2

%description -n kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package -n kernel-tools-libs-devel
Summary:        Assortment of tools for the Linux kernel
License:        GPLv2
Requires:       kernel-tools = %{version}-%{release}
Provides:       cpupowerutils-devel = 1:009-0.6.p1
Obsoletes:      cpupowerutils-devel < 1:009-0.6.p1
Requires:       kernel-tools-libs = %{version}-%{release}
Provides:       kernel-tools-devel

%description -n kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package -n bpftool
Summary:        Inspection and simple manipulation of eBPF programs and maps
License:        GPLv2

%description -n bpftool
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%package -n libperf
Summary: The perf library from kernel source
License: GPLv2
%description -n libperf
This package contains the kernel source perf library.

%package -n libperf-devel
Summary: Developement files for the perf library from kernel source
License: GPLv2
%description -n libperf-devel
This package includes libraries and header files needed for development
of applications which use perf library from kernel source.

%package -n rtla
Summary: RTLA: Real-Time Linux Analysis tools 
License: GPLv2
%description -n rtla
The rtla tool is a meta-tool that includes a set of commands that
aims to analyze the real-time properties of Linux. But, instead of
testing Linux as a black box, rtla leverages kernel tracing
capabilities to provide precise information about the properties
and root causes of unexpected results.


%prep
%setup -q -n kernel-%{kversion}%{?dist} -c

cd linux-%{kversion}

# This is for patching either an -rc or stable
%if 0%{?rcrev}
    xzcat %{SOURCE5000} | patch -p1 -F1 -s
%endif

%if 0%{?stable_base}
    xzcat %{SOURCE5000} | patch -p1 -F1 -s
%endif

%patch6 -p1

# END OF PATCH APPLICATIONS

# Mangle /usr/bin/python shebangs to /usr/bin/python3
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tools/ tools/perf/scripts/python/*.py scripts/clang-tools

sed -e 's|-O6|-O2|g' -i tools/lib/{api,subcmd}/Makefile tools/perf/Makefile.config

###
### build
###
%build
cd linux-%{kversion}

%ifarch aarch64
%global perf_build_extra_opts CORESIGHT=1
%endif

%global perf_make \
  make %{?make_opts} EXTRA_CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" %{?cross_opts} -C tools/perf V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 LIBBPF_DYNAMIC=1 LIBTRACEEVENT_DYNAMIC=1 %{?perf_build_extra_opts} prefix=%{_prefix} PYTHON=%{__python3}
# perf
# make sure check-headers.sh is executable
chmod +x tools/perf/check-headers.sh
%{perf_make} JOBS=%{_smp_build_ncpus} all

%global tools_make \
  CFLAGS="${CFLAGS}" LDFLAGS="${LDFLAGS}" make %{?make_opts}

# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%{tools_make} %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    %{tools_make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    %{tools_make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch %{ix86} x86_64
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
   %{tools_make} CFLAGS="${CFLAGS}"
   popd
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
pushd tools/tracing/rtla
%{tools_make}
popd

%global bpftool_make \
  make EXTRA_CFLAGS="${CFLAGS}" EXTRA_LDFLAGS="${LDFLAGS}" DESTDIR=%{buildroot} V=1

pushd tools/bpf/bpftool
%{bpftool_make}
popd
pushd tools/lib/perf
make V=1 prefix=%{_prefix} libdir=%{_libdir}
popd

# Build the docs
pushd tools/kvm/kvm_stat/
%make_build man
popd
pushd tools/perf/Documentation/
%make_build man
popd

###
### install
###

%install
export LD=ld.bfd

cd linux-%{kversion}

# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=%{buildroot} lib=%{_lib} install-bin
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace

# For both of the below, yes, this should be using a macro but right now
# it's hard coded and we don't actually want it anyway right now.
# Whoever wants examples can fix it up!

# remove examples
rm -rf %{buildroot}/usr/lib*/perf/examples
# remove the stray header file that somehow got packaged in examples
rm -rf %{buildroot}/usr/lib*/perf/include/bpf/

# python-perf extension
%{perf_make} DESTDIR=%{buildroot} install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
install -d %{buildroot}/%{_mandir}/man1
install -pm0644 tools/kvm/kvm_stat/kvm_stat.1 %{buildroot}/%{_mandir}/man1/
install -pm0644 tools/perf/Documentation/*.1 %{buildroot}/%{_mandir}/man1/

%{tools_make} -C tools/power/cpupower DESTDIR=%{buildroot} libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2000} %{buildroot}%{_unitdir}/cpupower.service
install -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/intel-speed-select
   %{tools_make} CFLAGS+="-D_GNU_SOURCE -Iinclude -I/usr/include/libnl3" DESTDIR=%{buildroot} install
   popd
   pushd tools/arch/x86/intel_sdsi
   %{tools_make} DESTDIR=%{buildroot} install
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
pushd tools/tracing/rtla/
%{tools_make} DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_bindir}/osnoise
rm -f %{buildroot}%{_bindir}/timerlat
(cd %{buildroot}

        ln -sf rtla ./%{_bindir}/osnoise
        ln -sf rtla ./%{_bindir}/timerlat
)
popd
pushd tools/kvm/kvm_stat
%{tools_make} INSTALL_ROOT=%{buildroot} install-tools
popd
pushd tools/bpf/bpftool
%{bpftool_make} prefix=%{_prefix} bash_compdir=%{_sysconfdir}/bash_completion.d/ mandir=%{_mandir} install doc-install
popd
pushd tools/lib/perf
make DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} V=1 install install_headers
popd

###
### scripts
###


%post
%systemd_post cpupower.service

%preun
%systemd_preun cpupower.service

%postun
%systemd_postun cpupower.service

%files -n perf
%{_bindir}/perf
%exclude %{_libdir}/traceevent
%{_libdir}/libperf-jvmti.so
%{_libexecdir}/perf-core
%{_datadir}/perf-core/
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc linux-%{kversion}/tools/perf/Documentation/examples.txt
%license linux-%{kversion}/COPYING
%{_docdir}/perf-tip/tips.txt

%files -n python3-perf
%license linux-%{kversion}/COPYING
%{python3_sitearch}/*

%files -f cpupower.lang
%{_bindir}/cpupower
%{_datadir}/bash-completion/completions/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%{_bindir}/intel-speed-select
%{_sbindir}/intel_sdsi
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
%license linux-%{kversion}/COPYING

%files libs
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.1
%license linux-%{kversion}/COPYING

%files libs-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h

%files -n bpftool
%{_sbindir}/bpftool
%{_sysconfdir}/bash_completion.d/bpftool
%{_mandir}/man8/bpftool-btf.8.gz
%{_mandir}/man8/bpftool-cgroup.8.gz
%{_mandir}/man8/bpftool-gen.8.gz
%{_mandir}/man8/bpftool-iter.8.gz
%{_mandir}/man8/bpftool-link.8.gz
%{_mandir}/man8/bpftool-map.8.gz
%{_mandir}/man8/bpftool-net.8.gz
%{_mandir}/man8/bpftool-prog.8.gz
%{_mandir}/man8/bpftool-perf.8.gz
%{_mandir}/man8/bpftool-struct_ops.8.gz
%{_mandir}/man8/bpftool-feature.8.gz
%{_mandir}/man8/bpftool.8.gz
%license linux-%{kversion}/COPYING

%files -n libperf
%{_libdir}/libperf.so.0
%{_libdir}/libperf.so.0.0.1
%license linux-%{kversion}/COPYING

%files -n libperf-devel
%{_libdir}/libperf.a
%{_libdir}/libperf.so
%{_libdir}/pkgconfig/libperf.pc
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
%license linux-%{kversion}/COPYING

%files -n rtla
%{_bindir}/rtla
%{_bindir}/osnoise
%{_bindir}/timerlat
%{_mandir}/man1/rtla-osnoise-hist.1.gz
%{_mandir}/man1/rtla-osnoise-top.1.gz
%{_mandir}/man1/rtla-osnoise.1.gz
%{_mandir}/man1/rtla-timerlat-hist.1.gz
%{_mandir}/man1/rtla-timerlat-top.1.gz
%{_mandir}/man1/rtla-timerlat.1.gz
%{_mandir}/man1/rtla.1.gz


%changelog
* Mon Sep 05 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.7-500
- 5.19.7

* Wed Aug 31 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.6-500
- 5.19.6

* Mon Aug 29 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.5-500
- 5.19.5

* Thu Aug 25 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.4-500
- 5.19.4

* Wed Aug 17 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.2-500
- 5.19.2

* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.1-500
- 5.19.1

* Mon Aug 01 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.0-500
- 5.19.0

* Fri Jul 29 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.15-500
- 5.18.15

* Sat Jul 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.14-500
- 5.18.14

* Tue Jul 12 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.11-500
- 5.18.11

* Thu Jul 07 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.10-500
- 5.18.10

* Sat Jul 02 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.9-500
- 5.18.9

* Wed Jun 29 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.8-500
- 5.18.8

* Sat Jun 25 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.7-500
- 5.18.7

* Wed Jun 22 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.6-500
- 5.18.6

* Thu Jun 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.5-500
- 5.18.5

* Tue Jun 14 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.4-500
- 5.18.4

* Thu Jun 09 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.3-500
- 5.18.3

* Mon Jun 06 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.2-500
- 5.18.2

* Mon May 30 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.1-500
- 5.18.1

* Mon May 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.0-500
- 5.18.0

* Wed May 18 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.9-500
- 5.17.9

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.8-500
- 5.17.8

* Thu May 12 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.7-500
- 5.17.7

* Mon May 09 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.6-500
- 5.17.6

* Wed Apr 27 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.5-500
- 5.17.5

* Wed Apr 20 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.4-500
- 5.17.4

* Wed Apr 13 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.3-500
- 5.17.3

* Fri Apr 08 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.2-500
- 5.17.2

* Mon Mar 28 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.1-500
- 5.17.1

* Mon Mar 21 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.0-500
- 5.17.0

* Sat Mar 19 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.16-500
- 5.16.16

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.15-500
- 5.16.15

* Sun Mar 13 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.14-500
- 5.16.14

* Tue Mar 08 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.13-500
- 5.16.13

* Wed Mar 02 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.12-500
- 5.16.12

* Wed Feb 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.11-500
- 5.16.11

* Wed Feb 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.10-500
- 5.16.10

* Fri Feb 11 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.9-500
- 5.16.9

* Sat Feb 05 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.7-500
- 5.16.7

* Tue Feb 01 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.5-500
- 5.16.5

* Sun Jan 30 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.4-500
- 5.16.4

* Thu Jan 27 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.3-500
- 5.16.3

* Thu Jan 20 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.2-500
- 5.16.2

* Sun Jan 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.1-500
- 5.16.1

* Mon Jan 10 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.0-500
- 5.16.0

* Wed Jan 05 2022 Phantom X <megaphantomx at hotmail dot com> - 5.15.13-500
- 5.15.13

* Wed Dec 29 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.12-500
- 5.15.12

* Wed Dec 22 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.11-500
- 5.15.11

* Fri Dec 17 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.10-500
- 5.15.10

* Tue Dec 14 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.8-500
- 5.15.8

* Wed Dec 08 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.7-500
- 5.15.7

* Wed Dec 01 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.6-500
- 5.15.6

* Thu Nov 25 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.5-500
- 5.15.5

* Sun Nov 21 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.4-500
- 5.15.4

* Thu Nov 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.3-500
- 5.15.3

* Fri Nov 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.2-500
- 5.15.2

* Mon Nov 01 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.0-500
- 5.15.0

* Wed Oct 27 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.15-500
- 5.14.15

* Wed Oct 20 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.14-500
- 5.14.14

* Sun Oct 17 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.13-500
- 5.14.13

* Wed Oct 13 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.12-500
- 5.14.12

* Sat Oct 09 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.11-500
- 5.14.11

* Thu Oct 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.10-500
- 5.14.10

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.9-500
- 5.14.9

* Sun Sep 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.8-500
- 5.14.8

* Wed Sep 22 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.7-500
- 5.14.7

* Sat Sep 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.6-500
- 5.14.6

* Wed Sep 15 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.4-500
- 5.14.4

* Sun Sep 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.3-500
- 5.14.3

* Wed Sep 08 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.2-500
- 5.14.2

* Tue Aug 31 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.0-500
- 5.14.0

* Thu Aug 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.13-500
- 5.13.13

* Wed Aug 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.12-500
- 5.13.12

* Sun Aug 15 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.11-500
- 5.13.11

* Thu Aug 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.10-500
- 5.13.10

* Sun Aug 08 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.9-500
- 5.13.9

* Wed Aug 04 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.8-500
- 5.13.8

* Sat Jul 31 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.7-500
- 5.13.7

* Wed Jul 28 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.6-500
- 5.13.6

* Sun Jul 25 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.5-500
- 5.13.5

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.4-500
- 5.13.4

* Mon Jul 19 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.3-500
- 5.13.3

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.2-500
- 5.13.2

* Tue Jun 29 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.0-500
- 5.13.0
- Rawhide sync

* Fri Jun 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.13-500
- 5.12.13

* Fri Jun 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.12-500
- 5.12.12

* Wed Jun 16 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.11-500
- 5.12.11

* Thu Jun 10 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.10-500
- 5.12.10

* Thu Jun 03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.9-500
- 5.12.9

* Fri May 28 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.8-500
- 5.12.8

* Wed May 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.7-500
- 5.12.7

* Sat May 22 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.6-500
- 5.12.6

* Wed May 19 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.5-500
- 5.12.5

* Fri May 14 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.4-500
- 5.12.4

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.3-500
- 5.12.3

* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.2-500
- 5.12.2

* Sun May 02 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.1-500
- 5.12.1

* Mon Apr 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.0-500
- 5.12.0
