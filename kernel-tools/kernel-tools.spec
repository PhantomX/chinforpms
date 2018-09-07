# Much of this is borrowed from the original kernel.spec
# It needs a bunch of the macros for rawhide vs. not-rawhide builds.

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1
%global baserelease 500
%global fedora_build %{baserelease}

%global buildid .chinfo

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%global base_sublevel 18

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%global stable_update 6
# Set rpm version accordingly
%if 0%{?stable_update}
%global stablerev %{stable_update}
%global stable_base %{stable_update}
%endif
%global rpmversion 4.%{base_sublevel}.%{stable_update}

## The not-released-kernel case ##
%else
# The next upstream release sublevel (base_sublevel+1)
%global upstream_sublevel %(echo $((%{base_sublevel} + 1)))
# The rc snapshot level
%global rcrev 0
# Set rpm version accordingly
%global rpmversion 4.%{upstream_sublevel}.0
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
%global kversion 4.%{base_sublevel}
%global KVERREL %{version}-%{release}.%{_target_cpu}

%global _debuginfo_subpackages 1
%undefine _include_gdb_index
%undefine _include_minidebuginfo

# perf needs this
%undefine _strict_symbol_defs_build

BuildRequires: kmod, patch, bash, tar, git
BuildRequires: bzip2, xz, findutils, gzip, m4, perl-interpreter, perl(Carp), perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: zlib-devel binutils-devel newt-devel python2-devel python2-docutils perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel glibc-devel glibc-static python3-devel
BuildRequires: asciidoc xmlto
%ifnarch s390x %{arm}
BuildRequires: numactl-devel
%endif
BuildRequires: pciutils-devel gettext ncurses-devel
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
BuildRequires: rpm-build, elfutils
%{?systemd_requires}
BuildRequires: systemd

Source0: https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-%{kversion}.tar.xz

# Sources for kernel-tools
Source2000: cpupower.service
Source2001: cpupower.config

# Here should be only the patches up to the upstream canonical Linus tree.

# For a stable release kernel
%if 0%{?stable_base}
Source5000: https://cdn.kernel.org/pub/linux/kernel/v4.x/patch-4.%{base_sublevel}.%{stable_base}.xz
%else
# non-released_kernel case
# These are automagically defined by the rcrev value set up
# near the top of this spec file.
%if 0%{?rcrev}
Source5000: patch-4.%{upstream_sublevel}-rc%{rcrev}.xz
%endif
%endif

# ongoing complaint, full discussion delayed until ksummit/plumbers
Patch0: 0001-iio-Use-event-header-from-kernel-tree.patch

# rpmlint cleanup
Patch1: 0001-perf-Remove-FSF-address.patch
Patch3: 0001-tools-include-Sync-vmx.h-header-for-FSF-removal.patch
Patch4: 0001-tools-lib-Remove-FSF-address.patch
Patch6: 0002-perf-Don-t-make-sourced-script-executable.patch
Patch8: 0001-Switch-to-python3.patch

# Extra

### openSUSE patches - http://kernel.opensuse.org/cgit/kernel-source/

#global opensuse_url https://kernel.opensuse.org/cgit/kernel-source/plain/patches.suse
%global opensuse_id 70ab8aebd252bd951d6916a76c8dc34ee09f9cdc
%global opensuse_url https://github.com/openSUSE/kernel-source/raw/%{opensuse_id}/patches.suse

Patch1000: %{opensuse_url}/perf_timechart_fix_zero_timestamps.patch#/openSUSE-perf_timechart_fix_zero_timestamps.patch

Name: kernel-tools
Summary: Assortment of tools for the Linux kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: kernel-tools-libs = %{version}-%{release}
%description -n kernel-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.


%package -n perf
Summary: Performance monitoring for the Linux kernel
License: GPLv2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%global python_perf_sum Python bindings for apps which will manipulate perf events
%global python_perf_desc A Python module that permits applications \
written in the Python programming language to use the interface \
to manipulate perf events.

%package -n python2-perf
Summary: %{python_perf_sum}
%{?python_provide:%python_provide python2-perf}
%description -n python2-perf
%{python_perf_desc}

%package -n python3-perf
Summary: %{python_perf_sum}
%{?python_provide:%python_provide python3-perf}
%description -n python3-perf
%{python_perf_desc}

%package -n kernel-tools-libs
Summary: Libraries for the kernels-tools
License: GPLv2
%description -n kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package -n kernel-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
License: GPLv2
Requires: kernel-tools = %{version}-%{release}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Requires: kernel-tools-libs = %{version}-%{release}
Provides: kernel-tools-devel
%description -n kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package -n bpftool
Summary: Inspection and simple manipulation of eBPF programs and maps
License: GPLv2
%description -n bpftool
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

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

%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch8 -p1

%patch1000 -p1

# END OF PATCH APPLICATIONS

cp -a tools/perf tools/python3-perf

sed -e 's|-O6|-O2|g' -i tools/lib/{api,subcmd}/Makefile tools/perf/Makefile.config

###
### build
###
%build

cd linux-%{kversion}

%global perf_make \
  make EXTRA_CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}" %{?cross_opts} V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 NO_JVMTI=1 prefix=%{_prefix}
%global perf_python2 -C tools/perf PYTHON=%{__python2}
%global perf_python3 -C tools/python3-perf PYTHON=%{__python3}
# perf
# make sure check-headers.sh is executable
chmod +x tools/perf/check-headers.sh
chmod +x tools/python3-perf/check-headers.sh
%{perf_make} %{perf_python2} all
%{perf_make} %{perf_python3} all

# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
make %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
    pushd tools/power/cpupower/debug/i386
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch %{ix86} x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   make
   popd
   pushd tools/power/x86/turbostat
   make
   popd
%endif #turbostat/x86_energy_perf_policy
pushd tools/thermal/tmon/
make
popd
pushd tools/iio/
make
popd
pushd tools/gpio/
make
popd
pushd tools/bpf/bpftool
make
popd

# Build the docs
pushd tools/kvm/kvm_stat/
make %{?_smp_mflags} man
popd
pushd tools/perf/Documentation/
make %{?_smp_mflags} man
popd

###
### install
###

%install

cd linux-%{kversion}

# perf tool binary and supporting scripts/binaries
%{perf_make} %{perf_python2} DESTDIR=%{buildroot} lib=%{_lib} install-bin install-traceevent-plugins
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace
# remove the perf-tips
rm -rf %{buildroot}%{_docdir}/perf-tip

# For both of the below, yes, this should be using a macro but right now
# it's hard coded and we don't actually want it anyway right now.
# Whoever wants examples can fix it up!

# remove examples
rm -rf %{buildroot}/usr/lib/examples/perf
# remove the stray header file that somehow got packaged in examples
rm -rf %{buildroot}/usr/lib/include/perf/bpf/bpf.h

# python-perf extension
%{perf_make} %{perf_python3} DESTDIR=%{buildroot} install-python_ext
%{perf_make} %{perf_python2} DESTDIR=%{buildroot} install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
install -d %{buildroot}/%{_mandir}/man1
install -pm0644 tools/kvm/kvm_stat/kvm_stat.1 %{buildroot}/%{_mandir}/man1/
install -pm0644 tools/perf/Documentation/*.1 %{buildroot}/%{_mandir}/man1/

make -C tools/power/cpupower DESTDIR=%{buildroot} libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
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
   make DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   make DESTDIR=%{buildroot} install
   popd
%endif #turbostat/x86_energy_perf_policy
pushd tools/thermal/tmon
make INSTALL_ROOT=%{buildroot} install
popd
pushd tools/iio
make DESTDIR=%{buildroot} install
popd
pushd tools/gpio
make DESTDIR=%{buildroot} install
popd
pushd tools/kvm/kvm_stat
make INSTALL_ROOT=%{buildroot} install-tools
popd
pushd tools/bpf/bpftool
make DESTDIR=%{buildroot} prefix=%{_prefix} bash_compdir=%{_sysconfdir}/bash_completion.d/ mandir=%{_mandir} install doc-install
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
%dir %{_libdir}/traceevent
%{_libdir}/traceevent/plugins/
%{_libexecdir}/perf-core
%{_datadir}/perf-core/
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc linux-%{kversion}/tools/perf/Documentation/examples.txt
%license linux-%{kversion}/COPYING

%files -n python2-perf
%license linux-%{kversion}/COPYING
%{python2_sitearch}/*

%files -n python3-perf
%license linux-%{kversion}/COPYING
%{python3_sitearch}/*

%files -f cpupower.lang
%{_bindir}/cpupower
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
%endif
%{_bindir}/tmon
%{_bindir}/iio_event_monitor
%{_bindir}/iio_generic_buffer
%{_bindir}/lsiio
%{_bindir}/lsgpio
%{_bindir}/gpio-hammer
%{_bindir}/gpio-event-mon
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
%{_mandir}/man8/bpftool-cgroup.8.gz
%{_mandir}/man8/bpftool-map.8.gz
%{_mandir}/man8/bpftool-prog.8.gz
%{_mandir}/man8/bpftool-perf.8.gz
%{_mandir}/man8/bpftool.8.gz
%license linux-%{kversion}/COPYING

%changelog
* Wed Sep 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.6-500.chinfo
- 4.18.6

* Fri Aug 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.5-500.chinfo
- 4.18.5

* Wed Aug 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.4-500.chinfo
- 4.18.4

* Sat Aug 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.3-500.chinfo
- 4.18.3

* Fri Aug 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.2-500.chinfo
- 4.18.2

* Wed Aug 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.1-500.chinfo
- 4.18.1

* Mon Aug 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.0-500.chinfo
- 4.18.0
- Rawhide sync

* Thu Aug 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.14-500.chinfo
- 4.17.14

* Mon Aug 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.13-500.chinfo
- 4.17.13

* Fri Aug 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.12-500.chinfo
- 4.17.12

* Sat Jul 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.11-500.chinfo
- 4.17.11

* Wed Jul 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.10-500.chinfo
- 4.17.10

* Sun Jul 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.9-500.chinfo
- 4.17.9

* Wed Jul 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.8-500.chinfo
- 4.17.8

* Tue Jul 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.7-500.chinfo
- 4.17.7

* Wed Jul 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.6-500.chinfo
- 4.17.6

* Sun Jul 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.5-500.chinfo
- 4.17.5

* Tue Jul 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.4-500.chinfo
- 4.17.4

* Mon Jun 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.3-500.chinfo
- 4.17.3

* Sat Jun 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.2-500.chinfo
- 4.17.2

* Mon Jun 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.1-500.chinfo
- 4.17.1

* Mon Jun 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.17.0-500.chinfo
- 4.17.0
- rawhide sync

* Wed May 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.13-500.chinfo
- 4.16.13

* Fri May 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.12-500.chinfo
- 4.16.12

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.11-500.chinfo
- 4.16.11

* Wed May 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.9-100.chinfo
- 4.16.9

* Wed May 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.8-100.chinfo
- 4.16.8

* Wed May 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.7-100.chinfo
- 4.16.7

* Sun Apr 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.6-101.chinfo
- f28 sync, bpftool

* Sun Apr 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.6-100.chinfo
- 4.16.6

* Thu Apr 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.5-100.chinfo
- 4.16.5

* Tue Apr 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.4-100.chinfo
- 4.16.4

* Thu Apr 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.3-100.chinfo
- 4.16.3

* Thu Apr 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.2-100.chinfo
- 4.16.2

* Sun Apr 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.1-100.chinfo
- 4.16.1

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.16.0-100.chinfo
- 4.16.0
- Rawhide sync

* Mon Mar 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.11-100.chinfo
- 4.15.11

* Thu Mar 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.10-100.chinfo
- 4.15.10

* Sun Mar 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.9-100.chinfo
- 4.15.9

* Fri Mar 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.8-100.chinfo
- 4.15.8

* Wed Feb 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.7-100.chinfo
- 4.15.7

* Tue Feb 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.6-100.chinfo
- 4.15.6

* Thu Feb 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.5-100.chinfo
- 4.15.5

* Sat Feb 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.4-100.chinfo
- 4.15.4

* Mon Feb 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.3-100.chinfo
- 4.15.3

* Wed Feb 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.2-100.chinfo
- 4.15.2

* Sat Feb 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.1-100.chinfo
- 4.15.1
- Apply missing patch

* Mon Jan 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.15.0-100.chinfo
- chinforpms
- openSUSE patch

* Mon Jan 29 2018 Laura Abbott <labbott@redhat.com> - 4.15.0-1
- Linux v4.15

* Tue Jan 23 2018 Laura Abbott <labbott@redhat.com> - 4.15.0-0.rc9.git0.1
- Linux 4.15-rc9

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.15.0-0.rc8.git0.2
- Rebuilt for switch to libxcrypt

* Tue Jan 16 2018 Laura Abbott <labbott@redhat.com> - 4.15.0-0.rc8.git0.1
- Linux 4.15-rc8

* Fri Jan 05 2018 Laura Abbott <labbott@redhat.com> - 4.15.0-0.rc7.git0.1
- Fork from the kernel package
