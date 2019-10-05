# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

%global buildid .chinfo

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

%define major_ver 5

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%define base_sublevel 3

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%define stable_update 4
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

# pkg_release is what we'll fill in for the rpm Release: field
%if 0%{?released_kernel}

%define srcversion %{fedora_build}%{?buildid}

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

Name: kernel-headers
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
Source0: kernel-headers-%{rpmversion}-%{?srcversion}.tar.xz
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

%package -n kernel-cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc

%description -n kernel-cross-headers
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
ARCH_LIST="arm arm64 powerpc s390 x86"

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

%files -n kernel-cross-headers
%defattr(-,root,root)
%{_prefix}/*-linux-gnu/*

%changelog
* Sat Oct 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.4-500.chinfo
- 5.3.4

* Tue Oct 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.2-500.chinfo
- 5.3.2

* Mon Sep 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.1-501.chinfo
- Rebuild

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.1-500.chinfo
- 5.3.1

* Mon Sep 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.3.0-500.chinfo
- 5.3.0

* Thu Sep 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.14-501.chinfo
- Rebuild

* Tue Sep 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.14-500.chinfo
- 5.2.14

* Fri Sep 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.13-500.chinfo
- 5.2.13

* Thu Aug 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.11-500.chinfo
- 5.2.11

* Mon Aug 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.10-500.chinfo
- 5.2.10

* Fri Aug 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.9-500.chinfo
- 5.2.9

* Fri Aug 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.8-500.chinfo
- 5.2.8

* Wed Aug 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.7-501.chinfo
- 5.2.7

* Tue Aug 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.7-500.chinfo
- 5.2.7

* Sun Aug 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.6-500.chinfo
- 5.2.6

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.5-500.chinfo
- 5.2.5

* Sun Jul 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.21-500.chinfo
- 5.1.21

* Fri Jul 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.20-500.chinfo
- 5.1.20

* Sun Jul 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.19-500.chinfo
- 5.1.19

* Sun Jul 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.18-500.chinfo
- 5.1.18

* Wed Jul 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.17-500.chinfo
- 5.1.17

* Wed Jul 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.16-500.chinfo
- 5.1.16

* Tue Jun 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.15-500.chinfo
- 5.1.15

* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.14-500.chinfo
- 5.1.14

* Thu Jun 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.12-500.chinfo
- 5.1.12

* Mon Jun 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.11-500.chinfo
- 5.1.11

* Sun Jun 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.10-500.chinfo
- 5.1.10

* Tue Jun 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.9-500.chinfo
- 5.1.9

* Mon Jun 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.8-500.chinfo
- 5.1.8

* Tue Jun 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.7-500.chinfo
- 5.1.7

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.6-500.chinfo
- 5.1.6

* Sat May 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.5-500.chinfo
- 5.1.5

* Fri May 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.4-501.chinfo
- Rebuild

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.4-500.chinfo
- 5.1.4

* Thu May 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.3-500.chinfo
- 5.1.3

* Tue May 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.2-500.chinfo
- 5.1.2

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.1-500.chinfo
- 5.1.1

* Wed May 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.0-501.chinfo
- Rebuild

* Mon May 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.1.0-500.chinfo
- 5.1.0

* Sun May 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.13-500.chinfo
- 5.0.13

* Thu May 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.11-500.chinfo
- 5.0.11

* Mon Apr 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.10-500.chinfo
- 5.0.10

* Sat Apr 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.9-500.chinfo
- 5.0.9

* Wed Apr 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.8-500.chinfo
- 5.0.8

* Thu Apr 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.7-501.chinfo
- 5.0.7

* Sat Apr 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.7-500.chinfo
- 5.0.7

* Wed Apr 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.6-500.chinfo
- 5.0.6

* Tue Apr 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.5-500.chinfo
- 5.0.5

* Tue Mar 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.3-500.chinfo
- 5.0.3

* Fri Mar 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.2-500.chinfo
- 5.0.2

* Sun Mar 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.1-500.chinfo
- 5.0.1

* Fri Mar 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-502.chinfo
- Rebuild

* Mon Mar 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-500.chinfo
- 5.0.0

* Wed Feb 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.13-500.chinfo
- 4.20.13

* Sun Feb 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.12-500.chinfo
- 4.20.12

* Wed Feb 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.11-500.chinfo
- 4.20.11

* Fri Feb 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.10-500.chinfo
- 4.20.10

* Tue Feb 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.8-500.chinfo
- 4.20.8

* Wed Feb 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.7-500.chinfo
- 4.20.7

* Thu Jan 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.6-500.chinfo
- 4.20.6

* Sat Jan 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.5-500.chinfo
- 4.20.5

* Thu Jan 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.4-500.chinfo
- 4.20.4

* Thu Jan 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.3-500.chinfo
- 4.20.3

* Sun Jan 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.2-500.chinfo
- 4.20.2

* Wed Jan 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.20.1-500.chinfo
- 4.20.1

* Mon Dec 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.20.0-500.chinfo
- 4.20.0

* Fri Dec 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.12-500.chinfo
- 4.19.12

* Wed Dec 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.11-500.chinfo
- 4.19.11

* Mon Dec 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.10-500.chinfo
- 4.19.10

* Thu Dec 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.9-500.chinfo
- 4.19.9

* Wed Dec 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.8-500.chinfo
- 4.19.8

* Thu Dec 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.7-500.chinfo
- 4.19.7

* Sun Dec 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.6-500.chinfo
- 4.19.6

* Fri Nov 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.5-502.chinfo
- Rebuild

* Fri Nov 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.5-501.chinfo
- Rebuild

* Tue Nov 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.5-500.chinfo
- 4.19.5

* Sun Nov 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.4-500.chinfo
- 4.19.4

* Wed Nov 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.3-500.chinfo
- 4.19.3

* Wed Nov 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.2-500.chinfo
- 4.19.2

* Mon Nov 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.1-501.chinfo
- 4.19.1-501

* Sun Nov 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.1-500.chinfo
- 4.19.1

* Mon Oct 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.19.0-500.chinfo
- 4.19.0

* Sat Oct 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.16-500.chinfo
- 4.18.16

* Thu Oct 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.15-500.chinfo
- 4.18.15

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.14-500.chinfo
- Linux v4.18.14

* Wed Oct 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.13-500.chinfo
- 4.18.13

* Thu Oct 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.12-500.chinfo
- 4.18.12

* Sat Sep 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.11-500.chinfo
- 4.18.11

* Wed Sep 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.10-500.chinfo
- 4.18.10

* Wed Sep 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.9-500.chinfo
- 4.18.9

* Sat Sep 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.8-500.chinfo
- 4.18.8

* Sun Sep 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.18.7-500.chinfo
- 4.18.7

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

* Tue Jul 31 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.18.0-0.rc7.git0.1
- Linux v4.18-rc7

* Fri Jul 27 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.18.0-0.rc6.git3.1
- Initial package commit

* Mon Jul 23 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.18.0-0.rc6.git0.1
- Changes and updates to fit inline with current Fedora process

* Thu Jul 12 2018 Herton R. Krzesinski <herton@redhat.com> - 4.18.0-0.rc4.2
- Initial version of splitted kernel-headers package.
