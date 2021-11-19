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
%global baserelease 501
%global fedora_build %{baserelease}

%define major_ver 5

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%define base_sublevel 15

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%define stable_update 3
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
* Fri Nov 19 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.3-501.chinfo
- 5.15.3

* Fri Nov 19 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.3-500.chinfo
- 5.15.3

* Fri Nov 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.2-500.chinfo
- 5.15.2

* Sat Nov 06 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.1-500.chinfo
- 5.15.1

* Mon Nov 01 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.0-500.chinfo
- 5.15.0

* Wed Oct 27 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.15-500.chinfo
- 5.14.15

* Wed Oct 20 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.14-500.chinfo
- 5.14.14

* Sun Oct 17 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.13-500.chinfo
- 5.14.13

* Wed Oct 13 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.12-500.chinfo
- 5.14.12

* Sat Oct 09 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.11-500.chinfo
- 5.14.11

* Thu Oct 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.10-500.chinfo
- 5.14.10

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.9-500.chinfo
- 5.14.9

* Sun Sep 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.8-500.chinfo
- 5.14.8

* Wed Sep 22 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.7-500.chinfo
- 5.14.7

* Sat Sep 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.6-500.chinfo
- 5.14.6

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.5-500.chinfo
- 5.14.5

* Wed Sep 15 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.4-500.chinfo
- 5.14.4

* Sun Sep 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.3-500.chinfo
- 5.14.3

* Fri Sep 10 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.2-500.chinfo
- 5.14.2

* Fri Sep 03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.1-500.chinfo
- 5.14.1

* Wed Sep 01 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.0-501.chinfo
- 5.14.0

* Tue Aug 31 2021 Phantom X <megaphantomx at hotmail dot com> - 5.14.0-500.chinfo
- 5.14.0

* Thu Aug 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.13-500.chinfo
- 5.13.13

* Wed Aug 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.12-500.chinfo
- 5.13.12

* Tue Aug 17 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.11-500.chinfo
- 5.13.11

* Thu Aug 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.10-500.chinfo
- 5.13.10

* Sun Aug 08 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.9-500.chinfo
- 5.13.9

* Wed Aug 04 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.8-500.chinfo
- 5.13.8

* Sat Jul 31 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.7-500.chinfo
- 5.13.7

* Wed Jul 28 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.6-500.chinfo
- 5.13.6

* Sun Jul 25 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.5-500.chinfo
- 5.13.5

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.4-500.chinfo
- 5.13.4

* Mon Jul 19 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.3-500.chinfo
- 5.13.3

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.2-500.chinfo
- 5.13.2

* Wed Jul 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.1-500.chinfo
- 5.13.1
- Fix variant use

* Tue Jun 29 2021 Phantom X <megaphantomx at hotmail dot com> - 5.13.0-500.chinfo
- 5.13.0

* Fri Jun 25 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.13-501.chinfo
- 5.12.13

* Wed Jun 23 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.13-500.chinfo
- 5.12.13

* Fri Jun 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.12-500.chinfo
- 5.12.12

* Wed Jun 16 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.11-500.chinfo
- 5.12.11

* Thu Jun 10 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.10-500.chinfo
- 5.12.10

* Thu Jun 03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.9-500.chinfo
- 5.12.9

* Fri May 28 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.8-500.chinfo
- 5.12.8

* Wed May 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.7-500.chinfo
- 5.12.7

* Sat May 22 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.6-500.chinfo
- 5.12.6

* Thu May 20 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.5-501.chinfo
- 5.12.5

* Wed May 19 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.5-500.chinfo
- 5.12.5

* Fri May 14 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.4-500.chinfo
- 5.12.4

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.3-500.chinfo
- 5.12.3

* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.2-500.chinfo
- 5.12.2

* Sun May 02 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.1-500.chinfo
- 5.12.1

* Mon Apr 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.0-500.chinfo
- 5.12.0

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.16-500.chinfo
- 5.11.16

* Sun Apr 18 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.15-501.chinfo
- 5.11.15

* Fri Apr 16 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.15-500.chinfo
- 5.11.15

* Wed Apr 14 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.14-500.chinfo
- 5.11.14

* Sat Apr 10 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.13-500.chinfo
- 5.11.13

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.12-501.chinfo
- 5.11.12

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.12-500.chinfo
- 5.11.12

* Tue Mar 30 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.11-500.chinfo
- 5.11.11

* Thu Mar 25 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.10-500.chinfo
- 5.11.10

* Wed Mar 24 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.9-500.chinfo
- 5.11.9

* Sat Mar 20 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.8-500.chinfo
- 5.11.8

* Wed Mar 17 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.7-500.chinfo
- 5.11.7

* Thu Mar 11 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.6-500.chinfo
- 5.11.6

* Tue Mar 09 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.5-500.chinfo
- 5.11.5

* Sun Mar 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.4-500.chinfo
- 5.11.4

* Thu Mar 04 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.3-500.chinfo
- 5.11.3

* Fri Feb 26 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.2-500.chinfo
- 5.11.2

* Tue Feb 23 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.1-500.chinfo
- 5.11.1

* Mon Feb 15 2021 Phantom X <megaphantomx at hotmail dot com> - 5.11.0-500.chinfo
- 5.11.0

* Sat Feb 13 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.16-500.chinfo
- 5.10.16

* Wed Feb 10 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.15-500.chinfo
- 5.10.15

* Sun Feb 07 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.14-500.chinfo
- 5.10.14

* Thu Feb 04 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.13-500.chinfo
- 5.10.13

* Sat Jan 30 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.12-500.chinfo
- 5.10.12

* Wed Jan 27 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.11-500.chinfo
- 5.10.11

* Sat Jan 23 16:21:53 -03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.10-500.chinfo
- 5.10.10

* Tue Jan 19 18:59:48 -03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.9-500.chinfo
- 5.10.9

* Sun Jan 17 18:33:16 -03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.8-500.chinfo
- 5.10.8

* Tue Jan 12 19:16:08 -03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.7-500.chinfo
- 5.10.7

* Sat Jan  9 15:48:23 -03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.6-500.chinfo
- 5.10.6

* Wed Jan  6 15:55:52 -03 2021 Phantom X <megaphantomx at hotmail dot com> - 5.10.5-500.chinfo
- 5.10.5

* Wed Dec 30 09:41:29 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.10.4-500.chinfo
- 5.10.4

* Sat Dec 26 13:19:23 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.10.3-500.chinfo
- 5.10.3

* Mon Dec 21 13:39:42 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.10.2-500.chinfo
- 5.10.2

* Mon Dec 14 18:31:49 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.10.1-500.chinfo
- 5.10.1

* Mon Dec 14 13:13:58 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.10.0-500.chinfo
- 5.10.0

* Fri Dec 11 11:28:56 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.14-500.chinfo
- 5.9.14

* Tue Dec 08 08:05:13 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.13-500.chinfo
- 5.9.13

* Wed Dec  2 08:16:31 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.12-500.chinfo
- 5.9.12

* Tue Nov 24 15:07:55 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.11-500.chinfo
- 5.9.11

* Sun Nov 22 10:18:31 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.10-500.chinfo
- 5.9.10

* Wed Nov 18 18:55:25 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.9-500.chinfo
- 5.9.9

* Tue Nov 10 20:02:10 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.8-500.chinfo
- 5.9.8

* Tue Nov 10 16:09:36 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.7-500.chinfo
- 5.9.7

* Thu Nov 05 20:09:30 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.6-500.chinfo
- 5.9.6

* Wed Nov  4 18:55:42 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.4-500.chinfo
- 5.9.4

* Sun Nov  1 17:21:08 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.3-500.chinfo
- 5.9.3

* Thu Oct 29 14:34:00 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.2-500.chinfo
- 5.9.2

* Sat Oct 17 17:27:38 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.1-500.chinfo
- 5.9.1

* Tue Oct 13 19:46:33 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.9.0-500.chinfo
- 5.9.0

* Wed Oct  7 14:59:04 -03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.14-500.chinfo
- 5.8.14

* Thu Oct 01 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.13-500.chinfo
- 5.8.13

* Sat Sep 26 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.12-500.chinfo
- 5.8.12

* Wed Sep 23 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.11-500.chinfo
- 5.8.11

* Thu Sep 17 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.10-500.chinfo
- 5.8.10

* Sat Sep 12 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.9-500.chinfo
- 5.8.9

* Wed Sep 09 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.8-500.chinfo
- 5.8.8

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.7-500.chinfo
- 5.8.7

* Thu Sep 03 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.6-500.chinfo
- 5.8.6

* Thu Aug 27 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.5-500.chinfo
- 5.8.5

* Wed Aug 26 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.4-500.chinfo
- 5.8.4

* Sat Aug 22 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.3-500.chinfo
- 5.8.3

* Wed Aug 19 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.2-500.chinfo
- 5.8.2

* Tue Aug 11 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.1-500.chinfo
- 5.8.1

* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 5.8.0-501.chinfo
- Bump
