# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

#global buildid .chinfo

%global variant -chinfo

# baserelease defines which build revision of this kernel version we're
# building.  We used to call this fedora_build, but the magical name
# baserelease is matched by the rpmdev-bumpspec tool, which you should use.
#
# NOTE: baserelease must be > 0 or bad things will happen if you switch
#       to a released kernel (released version will be < rc version)
#
# For non-released -rc kernels, this will be appended after the rcX and
# gitX tags, so a 3 here would become part of release "0.rcX.gitX.3"
#
%global baserelease 500
%global fedora_build %{baserelease}

%define major_ver 6

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%define base_sublevel 2

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%define stable_update 12
# Set rpm version accordingly
%if 0%{?stable_update}
%define stablerev %{stable_update}
%define stable_base %{stable_update}
%endif
%define rpmversion %{major_ver}.%{base_sublevel}.%{stable_update}

## The not-released-kernel case ##
%else
# The next upstream release sublevel (base_sublevel+1)
%define upstream_sublevel %(echo $((%{base_sublevel} + 1)))
# The rc snapshot level
%global rcrev 7
# The git snapshot level
%define gitrev 0
# Set rpm version accordingly
%define rpmversion %{major_ver}.%{upstream_sublevel}.0
%endif

%global variantid  %{lua:variantid = string.gsub(rpm.expand("%{?variant}"), "-", "."); print(variantid)}

# pkg_release is what we'll fill in for the rpm Release: field
%if 0%{?released_kernel}

%define srcversion %{fedora_build}%{?buildid}%{?variantid}

%else

# non-released_kernel
%if 0%{?rcrev}
%define rctag .rc%rcrev
%else
%define rctag .rc0
%endif
%if 0%{?gitrev}
%define gittag .git%gitrev
%else
%define gittag .git0
%endif
%define srcversion 0%{?rctag}%{?gittag}.%{fedora_build}%{?buildid}

%endif

%define pkg_release %{?srcversion}%{?dist}

# This package doesn't contain any binary, thus no debuginfo package is needed
%global debug_package %{nil}

Name: kernel%{?variant}-headers
Summary: Header files for the Linux kernel for use by glibc

License: GPLv2
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
# This is a tarball with headers from the kernel, which should be created
# using create_headers_tarball.sh provided in the kernel source package.
# To create the tarball, you should go into a prepared/patched kernel sources
# directory, or git kernel source repository, and do eg.:
# For a RHEL package: (...)/create_headers_tarball.sh -m RHEL_RELEASE
# For a Fedora package: kernel/scripts/create_headers_tarball.sh -r <release number>
Source0: kernel%{?variant}-headers-%{rpmversion}-%{?srcversion}.tar.xz
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

* Fri Jul 29 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.15-500.chinfo
- 5.18.15

* Sat Jul 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.14-500.chinfo
- 5.18.14

* Fri Jul 22 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.13-500.chinfo
- 5.18.13

* Mon Jul 18 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.12-500.chinfo
- 5.18.12

* Wed Jul 13 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.11-500.chinfo
- 5.18.11

* Thu Jul 07 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.10-500.chinfo
- 5.18.10

* Sat Jul 02 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.9-500.chinfo
- 5.18.9

* Wed Jun 29 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.8-500.chinfo
- 5.18.8

* Sat Jun 25 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.7-500.chinfo
- 5.18.7

* Wed Jun 22 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.6-500.chinfo
- 5.18.6

* Thu Jun 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.5-500.chinfo
- 5.18.5

* Tue Jun 14 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.4-500.chinfo
- 5.18.4

* Thu Jun 09 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.3-500.chinfo
- 5.18.3

* Mon Jun 06 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.2-500.chinfo
- 5.18.2

* Mon May 30 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.1-500.chinfo
- 5.18.1

* Mon May 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.18.0-500.chinfo
- 5.18.0

* Wed May 18 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.9-500.chinfo
- 5.17.9

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.8-500.chinfo
- 5.17.8

* Thu May 12 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.7-500.chinfo
- 5.17.7

* Mon May 09 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.6-500.chinfo
- 5.17.6

* Wed Apr 27 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.5-500.chinfo
- 5.17.5

* Wed Apr 20 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.4-500.chinfo
- 5.17.4

* Thu Apr 14 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.3-500.chinfo
- 5.17.3

* Fri Apr 08 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.2-500.chinfo
- 5.17.2

* Mon Mar 28 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.1-500.chinfo
- 5.17.1

* Mon Mar 21 2022 Phantom X <megaphantomx at hotmail dot com> - 5.17.0-500.chinfo
- 5.17.0

* Sat Mar 19 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.16-500.chinfo
- 5.16.16

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.15-500.chinfo
- 5.16.15

* Sun Mar 13 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.14-500.chinfo
- 5.16.14

* Wed Mar 09 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.13-500.chinfo
- 5.16.13

* Wed Mar 02 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.12-500.chinfo
- 5.16.12

* Wed Feb 23 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.11-500.chinfo
- 5.16.11

* Wed Feb 16 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.10-500.chinfo
- 5.16.10

* Fri Feb 11 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.9-500.chinfo
- 5.16.9

* Wed Feb 09 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.8-500.chinfo
- 5.16.8

* Sat Feb 05 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.7-500.chinfo
- 5.16.7

* Tue Feb 01 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.5-500.chinfo
- 5.16.5

* Sun Jan 30 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.4-500.chinfo
- 5.16.4

* Thu Jan 27 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.3-500.chinfo
- 5.16.3

* Thu Jan 20 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.2-500.chinfo
- 5.16.2

* Mon Jan 17 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.1-500.chinfo
- 5.16.1

* Mon Jan 10 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.0-500.chinfo
- 5.16.0
