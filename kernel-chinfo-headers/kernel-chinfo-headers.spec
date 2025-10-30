# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

#global buildid .chinfo

%global variant -chinfo
%global variantid  %{lua:variantid = string.gsub(rpm.expand("%{?variant}"), "-", "."); print(variantid)}

%global package_name kernel%{?variant}
%define specrpmversion 6.17.6
%define specversion %{specrpmversion}
%define patchversion %(echo %{specversion} | cut -d'.' -f-2)
%define baserelease 500
%define kversion %(echo %{specversion} | cut -d'.' -f1)
%define srcversion %{baserelease}%{?buildid}%{?variantid}

%global src_hash 00000000000000000000000000000000

%define pkg_release %{?srcversion}%{?dist}

# This package doesn't contain any binary, thus no debuginfo package is needed
%global debug_package %{nil}

Name: %{package_name}-headers
Summary: Header files for the Linux kernel for use by glibc

License: ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-2-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR CDDL-1.0) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND ((GPL-2.0-only WITH Linux-syscall-note) OR MIT) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR MIT) AND BSD-3-Clause AND (GPL-1.0-or-later WITH Linux-syscall-note) AND GPL-2.0-only AND (GPL-2.0-only WITH Linux-syscall-note) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND (LGPL-2.1-only WITH Linux-syscall-note) AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND MIT
URL: http://www.kernel.org/
Version: %{specrpmversion}
Release: %{pkg_release}
# This is a tarball with headers from the kernel, which should be created
# using create_headers_tarball.sh provided in the kernel source package.
# To create the tarball, you should go into a prepared/patched kernel sources
# directory, or git kernel source repository, and do eg.:
# For a RHEL package: (...)/create_headers_tarball.sh -m RHEL_RELEASE
# For a Fedora package: kernel/scripts/create_headers_tarball.sh -r <release number>
Source0: https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms-kernel/%{name}/%{name}-%{specrpmversion}-%{srcversion}.tar.xz/%{src_hash}/%{name}-%{specrpmversion}-%{srcversion}.tar.xz
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if "0%{?variant}"
Obsoletes: kernel-headers < %{version}-%{release}
Provides: kernel-headers = %{version}-%{release}
%endif

%description
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package -n kernel%{?variant}-cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc
%if "0%{?variant}"
Obsoletes: kernel-cross-headers < %{version}-%{release}
Provides: kernel-cross-headers = %{version}-%{release}
%endif

%description -n kernel%{?variant}-cross-headers
Kernel-cross-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
cross-glibc package.

%prep
%setup -q -c

%build

%install
# List of architectures we support and want to copy their headers
ARCH_LIST="arm arm64 powerpc riscv s390 x86"

ARCH=%_target_cpu
case $ARCH in
	armv7hl)
		ARCH=arm
		;;
	aarch64)
		ARCH=arm64
		;;
	ppc64*)
		ARCH=powerpc
		;;
	riscv64)
		ARCH=riscv
		;;
	s390x)
		ARCH=s390
		;;
	x86_64|i*86)
		ARCH=x86
		;;
esac

cd arch-$ARCH/include
mkdir -p $RPM_BUILD_ROOT%{_includedir}
cp -a asm-generic $RPM_BUILD_ROOT%{_includedir}

# Copy all the architectures we care about to their respective asm directories
for arch in $ARCH_LIST; do
	mkdir -p $RPM_BUILD_ROOT%{_prefix}/${arch}-linux-gnu/include
	cp -a asm-generic $RPM_BUILD_ROOT%{_prefix}/${arch}-linux-gnu/include/
done

# Remove what we copied already
rm -rf asm-generic

# Copy the rest of the headers over
cp -a * $RPM_BUILD_ROOT%{_includedir}/
for arch in $ARCH_LIST; do
cp -a * $RPM_BUILD_ROOT%{_prefix}/${arch}-linux-gnu/include/
done

%files
%defattr(-,root,root)
%{_includedir}/*

%files -n kernel%{?variant}-cross-headers
%defattr(-,root,root)
%{_prefix}/*-linux-gnu/*

%changelog
* Wed Oct 29 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.6-500.chinfo
- 6.17.6

* Thu Oct 23 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.5-500.chinfo
- 6.17.5

* Sun Oct 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.4-500.chinfo
- 6.17.4

* Wed Oct 15 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.3-500.chinfo
- 6.17.3

* Sun Oct 12 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.2-500.chinfo
- 6.17.2

* Mon Oct 06 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.1-500.chinfo
- 6.17.1

* Mon Sep 29 2025 Phantom X <megaphantomx at hotmail dot com> - 6.17.0-500.chinfo
- 6.17.0

* Thu Sep 25 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.9-500.chinfo
- 6.16.9

* Fri Sep 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.8-500.chinfo
- 6.16.8

* Wed Sep 17 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.7-500.chinfo
- 6.16.7

* Tue Sep 09 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.6-500.chinfo
- 6.16.6

* Thu Sep 04 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.5-500.chinfo
- 6.16.5

* Thu Aug 28 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.4-500.chinfo
- 6.16.4

* Sat Aug 23 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.3-500.chinfo
- 6.16.3

* Thu Aug 21 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.2-500.chinfo
- 6.16.2

* Tue Aug 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.16.1-501.chinfo
- 6.16.1

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

* Sun Jul 06 2025 Phantom X <megaphantomx at hotmail dot com> - 6.15.5-500.chinfo
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

* Thu May 22 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.8-500.chinfo
- 6.14.8

* Sun May 18 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.7-500.chinfo
- 6.14.7

* Fri May 09 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.6-500.chinfo
- 6.14.6

* Fri May 02 2025 Phantom X <megaphantomx at hotmail dot com> - 6.14.5-500.chinfo
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

* Sun Mar 23 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.8-500.chinfo
- 6.13.8

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.7-501.chinfo
- 6.13.7

* Thu Mar 13 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.7-500.chinfo
- 6.13.7

* Fri Mar 07 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.6-500.chinfo
- 6.13.6

* Thu Feb 27 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.5-500.chinfo
- 6.13.5

* Sat Feb 22 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.4-500.chinfo
- 6.13.4

* Mon Feb 17 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.3-500.chinfo
- 6.13.3

* Sat Feb 08 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.2-500.chinfo
- 6.13.2

* Sat Feb 01 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.1-500.chinfo
- 6.13.1

* Wed Jan 22 2025 Phantom X <megaphantomx at hotmail dot com> - 6.13.0-500.chinfo
- 6.13.0

* Sat Jan 18 2025 Phantom X <megaphantomx at hotmail dot com> - 6.12.10-500.chinfo
- 6.12.10

* Mon Jan 13 2025 Phantom X <megaphantomx at hotmail dot com> - 6.12.9-501.chinfo
- 6.12.9

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
- 6.12.0

* Tue Nov 19 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12.0-500.chinfo
- 6.12.0

* Sun Nov 17 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.9-500.chinfo
- 6.11.9

* Thu Nov 14 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.8-500.chinfo
- 6.11.8

* Fri Nov 08 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.7-500.chinfo
- 6.11.7

* Sun Nov 03 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.6-502.chinfo
- 6.11.6

* Sat Nov 02 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.6-501.chinfo
- 6.11.6

* Fri Nov 01 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.6-500.chinfo
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

* Mon Sep 16 2024 Phantom X <megaphantomx at hotmail dot com> - 6.11.0-500.chinfo
- 6.11.0
