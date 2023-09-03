# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

#global buildid .chinfo

%global variant -chinfo
%global variantid  %{lua:variantid = string.gsub(rpm.expand("%{?variant}"), "-", "."); print(variantid)}

%global package_name kernel%{?variant}
%define specrpmversion 6.5.1
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
* Sat Sep 02 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.1-500.chinfo
- 6.5.1

* Thu Aug 31 2023 Phantom X <megaphantomx at hotmail dot com> - 6.5.0-500.chinfo
- 6.5.0

* Wed Aug 23 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.12-500.chinfo
- 6.4.12

* Wed Aug 16 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.11-500.chinfo
- 6.4.11

* Fri Aug 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.10-500.chinfo
- 6.4.10

* Tue Aug 08 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.9-500.chinfo
- 6.4.9

* Thu Aug 03 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.8-500.chinfo
- 6.4.8

* Thu Jul 27 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.7-500.chinfo
- 6.4.7

* Mon Jul 24 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.6-500.chinfo
- 6.4.6

* Sun Jul 23 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.5-500.chinfo
- 6.4.5

* Wed Jul 19 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.4-500.chinfo
- 6.4.4

* Tue Jul 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.3-500.chinfo
- 6.4.3

* Wed Jul 05 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.2-500.chinfo
- 6.4.2

* Tue Jul 04 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-501.chinfo
- 6.4.1

* Sat Jul 01 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-500.chinfo
- 6.4.1

* Mon Jun 26 2023 Phantom X <megaphantomx at hotmail dot com> - 6.4.0-500.chinfo
- 6.4.0

* Wed Jun 21 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.9-500.chinfo
- 6.3.9

* Wed Jun 14 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.8-500.chinfo
- 6.3.8

* Fri Jun 09 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.7-500.chinfo
- 6.3.7

* Mon Jun 05 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.6-500.chinfo
- 6.3.6

* Tue May 30 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.5-500.chinfo
- 6.3.5

* Thu May 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.4-500.chinfo
- 6.3.4

* Wed May 17 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.3-500.chinfo
- 6.3.3

* Thu May 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.2-500.chinfo
- 6.3.2

* Mon May 01 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.1-500.chinfo
- 6.3.1

* Tue Apr 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.3.0-500.chinfo
- 6.3.0

* Thu Apr 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.12-500.chinfo
- 6.2.12

* Thu Apr 13 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.11-500.chinfo
- 6.2.11

* Thu Apr 06 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.10-500.chinfo
- 6.2.10

* Thu Mar 30 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.9-500.chinfo
- 6.2.9

* Wed Mar 22 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.8-500.chinfo
- 6.2.8

* Fri Mar 17 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.7-500.chinfo
- 6.2.7

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.6-500.chinfo
- 6.2.6

* Sat Mar 11 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.5-500.chinfo
- 6.2.5

* Fri Mar 10 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.3-500.chinfo
- 6.2.3

* Fri Mar 03 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.2-500.chinfo
- 6.2.2

* Sun Feb 26 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.1-501.chinfo
- 6.2.1

* Sat Feb 25 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.1-500.chinfo
- 6.2.1

* Mon Feb 20 2023 Phantom X <megaphantomx at hotmail dot com> - 6.2.0-500.chinfo
- 6.2.0

* Tue Feb 14 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.12-500.chinfo
- 6.1.12

* Thu Feb 09 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.11-500.chinfo
- 6.1.11

* Mon Feb 06 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.10-500.chinfo
- 6.1.10

* Wed Feb 01 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.9-500.chinfo
- 6.1.9

* Tue Jan 24 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.8-500.chinfo
- 6.1.8

* Wed Jan 18 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.7-500.chinfo
- 6.1.7

* Sat Jan 14 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.6-500.chinfo
- 6.1.6

* Thu Jan 12 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.5-500.chinfo
- 6.1.5

* Sat Jan 07 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.4-500.chinfo
- 6.1.4

* Wed Jan 04 2023 Phantom X <megaphantomx at hotmail dot com> - 6.1.3-500.chinfo
- 6.1.3

* Sat Dec 31 2022 Phantom X <megaphantomx at hotmail dot com> - 6.1.2-500.chinfo
- 6.1.2

* Wed Dec 21 2022 Phantom X <megaphantomx at hotmail dot com> - 6.1.1-500.chinfo
- 6.1.1

* Mon Dec 12 2022 Phantom X <megaphantomx at hotmail dot com> - 6.1.0-500.chinfo
- 6.1.0

* Fri Dec 09 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.12-500.chinfo
- 6.0.12

* Fri Dec 02 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.11-500.chinfo
- 6.0.11

* Sat Nov 26 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.10-500.chinfo
- 6.0.10

* Wed Nov 16 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.9-500.chinfo
- 6.0.9

* Thu Nov 10 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.8-500.chinfo
- 6.0.8

* Thu Nov 03 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.7-500.chinfo
- 6.0.7

* Sat Oct 29 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.6-500.chinfo
- 6.0.6

* Wed Oct 26 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.5-500.chinfo
- 6.0.5

* Fri Oct 21 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.3-500.chinfo
- 6.0.3

* Sat Oct 15 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.2-500.chinfo
- 6.0.2

* Wed Oct 12 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.1-500.chinfo
- 6.0.1

* Mon Oct 03 2022 Phantom X <megaphantomx at hotmail dot com> - 6.0.0-500.chinfo
- 6.0.0

* Wed Sep 28 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.12-500.chinfo
- 5.19.12

* Mon Sep 26 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.11-501.chinfo
- 5.19.11

* Fri Sep 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.11-500.chinfo
- 5.19.11

* Tue Sep 20 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.10-500.chinfo
- 5.19.10

* Fri Sep 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.9-500.chinfo
- 5.19.9

* Sun Sep 11 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.8-501.chinfo
- 5.19.8

* Thu Sep 08 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.8-500.chinfo
- 5.19.8

* Mon Sep 05 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.7-500.chinfo
- 5.19.7

* Wed Aug 31 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.6-500.chinfo
- 5.19.6

* Mon Aug 29 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.5-500.chinfo
- 5.19.5

* Thu Aug 25 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.4-500.chinfo
- 5.19.4

* Wed Aug 24 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.3-500.chinfo
- 5.19.3

* Wed Aug 17 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.2-500.chinfo
- 5.19.2

* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.1-500.chinfo
- 5.19.1

* Mon Aug 01 2022 Phantom X <megaphantomx at hotmail dot com> - 5.19.0-500.chinfo
- 5.19.0
