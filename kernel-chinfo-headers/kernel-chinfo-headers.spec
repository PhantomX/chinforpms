# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

#global buildid .chinfo

%global variant -chinfo
%global variantid  %{lua:variantid = string.gsub(rpm.expand("%{?variant}"), "-", "."); print(variantid)}

%global package_name kernel%{?variant}
%define specrpmversion 6.11.8
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

License: GPL-2.0-only
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

* Fri Sep 13 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.10-500.chinfo
- 6.10.10

* Sun Sep 08 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.9-500.chinfo
- 6.10.9

* Fri Sep 06 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.8-501.chinfo
- 6.10.8

* Wed Sep 04 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.8-500.chinfo
- 6.10.8

* Thu Aug 29 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.7-500.chinfo
- 6.10.7

* Mon Aug 19 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.6-500.chinfo
- 6.10.6

* Sun Aug 18 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.5-500.chinfo
- 6.10.5

* Sun Aug 11 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.4-500.chinfo
- 6.10.4

* Sat Aug 03 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.3-500.chinfo
- 6.10.3

* Sun Jul 28 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.2-500.chinfo
- 6.10.2

* Wed Jul 24 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.1-500.chinfo
- 6.10.1

* Mon Jul 15 2024 Phantom X <megaphantomx at hotmail dot com> - 6.10.0-500.chinfo
- 6.10.0

* Thu Jul 11 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.9-500.chinfo
- 6.9.9

* Fri Jul 05 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.8-500.chinfo
- 6.9.8

* Thu Jun 27 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.7-500.chinfo
- 6.9.7

* Fri Jun 21 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.6-500.chinfo
- 6.9.6

* Sun Jun 16 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.5-500.chinfo
- 6.9.5

* Wed Jun 12 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.4-500.chinfo
- 6.9.4

* Thu May 30 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.3-500.chinfo
- 6.9.3

* Sat May 25 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9.2-500.chinfo
- 6.9.2

* Thu May 02 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.9-500.chinfo
- 6.8.9

* Sun Apr 28 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.8-500.chinfo
- 6.8.8

* Wed Apr 17 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.7-500.chinfo
- 6.8.7

* Sat Apr 13 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.6-500.chinfo
- 6.8.6

* Wed Apr 10 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.5-500.chinfo
- 6.8.5

* Thu Apr 04 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.4-500.chinfo
- 6.8.4

* Wed Apr 03 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.3-500.chinfo
- 6.8.3

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.2-500.chinfo
- 6.8.2

* Mon Mar 11 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8.0-500.chinfo
- 6.8.0

* Wed Mar 06 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.9-500.chinfo
- 6.7.9

* Fri Mar 01 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.7-500.chinfo
- 6.7.7

* Sat Feb 24 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.6-500.chinfo
- 6.7.6

* Fri Feb 16 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.5-500.chinfo
- 6.7.5

* Mon Feb 05 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.4-500.chinfo
- 6.7.4

* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.3-500.chinfo
- 6.7.3

* Sun Jan 28 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.2-500.chinfo
- 6.7.2

* Mon Jan 08 2024 Phantom X <megaphantomx at hotmail dot com> - 6.7.0-500.chinfo
- 6.7.0

* Fri Jan 05 2024 Phantom X <megaphantomx at hotmail dot com> - 6.6.10-500.chinfo
- 6.6.10

* Mon Jan 01 2024 Phantom X <megaphantomx at hotmail dot com> - 6.6.9-500.chinfo
- 6.6.9

* Wed Dec 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.8-500.chinfo
- 6.6.8

* Thu Dec 14 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.7-500.chinfo
- 6.6.7

* Fri Dec 08 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.5-500.chinfo
- 6.6.5

* Sun Dec 03 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.4-500.chinfo
- 6.6.4

* Tue Nov 28 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.3-500.chinfo
- 6.6.3

* Tue Nov 21 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.2-500.chinfo
- 6.6.2

* Wed Nov 08 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.1-500.chinfo
- 6.6.1

* Tue Oct 31 2023 Phantom X <megaphantomx at hotmail dot com> - 6.6.0-500.chinfo
- 6.6.0

* Wed Oct 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.9-500.chinfo
- 6.5.9

* Fri Oct 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.8-500.chinfo
- 6.5.8

* Tue Oct 10 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.7-500.chinfo
- 6.5.7

* Fri Oct 06 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.6-500.chinfo
- 6.5.6

* Sat Sep 23 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.5-500.chinfo
- 6.5.5

* Tue Sep 19 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.4-500.chinfo
- 6.5.4

* Mon Sep 18 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.3-500.chinfo
- 6.5.3

* Thu Sep 07 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.2-500.chinfo
- 6.5.2

* Sat Sep 02 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.1-500.chinfo
- 6.5.1

* Thu Aug 31 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.0-500.chinfo
- 6.5.0
