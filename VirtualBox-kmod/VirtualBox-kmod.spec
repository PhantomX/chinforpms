# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif
#akmods still generate debuginfo but have the wrong name:
#/var/cache/akmods/VirtualBox/VirtualBox-kmod-debuginfo-5.0.4-1.fc21.x86_64.rpm
#/var/cache/akmods/VirtualBox/kmod-VirtualBox-4.1.8-100.fc21.x86_64-5.0.4-1.fc21.x86_64.rpm
#and when just build akmod, debuginfo will be empty.

# In prerelease builds (such as betas), this package has the same
# major version number, while the kernel module abi is not guarranteed
# to be stable. This is so that we force the module update in sync with
# userspace.
#global prerel 106108
%global prereltag %{?prerel:-%(awk 'BEGIN {print toupper("%{prerel}")}')}

%global vboxrel 1
%global vboxreltag %{?vboxrel:-%{vboxrel}}
# Allow only root to access vboxdrv regardless of the file mode
# use only for debugging!
%bcond_without hardening
%global __arch_install_post   /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot

Name:           VirtualBox-kmod
Version:        5.2.2
#Release:        1%%{?prerel:.%%{prerel}}%%{?dist}
Release:        100.chinfo%{?dist}

Summary:        Kernel module for VirtualBox
License:        GPLv2 or CDDL
URL:            http://www.virtualbox.org/wiki/VirtualBox
# This filters out the XEN kernel, since we don't run on XEN
Source1:        VirtualBox-kmod-excludekernel-filter.txt

%global AkmodsBuildRequires %{_bindir}/kmodtool, VirtualBox-kmodsrc >= %{version}%{vboxreltag}, xz, time
BuildRequires:  %{AkmodsBuildRequires}

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  %{ix86} x86_64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} --filterfile %{SOURCE1} 2>/dev/null) }


%description
Kernel module for VirtualBox


%prep
%setup -T -c
tar --use-compress-program xz -xf %{_datadir}/%{name}-%{version}/%{name}-%{version}.tar.xz

# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} --filterfile %{SOURCE1} 2>/dev/null

# This is hardcoded in Makefiles
# Kto zisti, preco tu nefunguje %%without hardening ma u mna nanuk
%{!?with_hardening:find %{name}-%{version} -name Makefile |xargs sed 's/-DVBOX_WITH_HARDENING//' -i}

for kernel_version in %{?kernel_versions} ; do
    cp -al %{name}-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    for module in vbox{drv,guest}; do
        make VBOX_USE_INSERT_PAGE=1 %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS="${PWD}/_kmod_build_${kernel_version%%___*}/${module}"  modules
    done
    cp _kmod_build_${kernel_version%%___*}/{vboxdrv/Module.symvers,vboxnetadp}
    cp _kmod_build_${kernel_version%%___*}/{vboxdrv/Module.symvers,vboxnetflt}
    cp _kmod_build_${kernel_version%%___*}/{vboxguest/Module.symvers,vboxsf}
    cp _kmod_build_${kernel_version%%___*}/{vboxguest/Module.symvers,vboxvideo}
    for module in vbox{netadp,netflt,sf,video,pci}; do
        make VBOX_USE_INSERT_PAGE=1 %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS="${PWD}/_kmod_build_${kernel_version%%___*}/${module}"  modules
    done
done


%install
for kernel_version in %{?kernel_versions}; do
    install -d %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install _kmod_build_${kernel_version%%___*}/*/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done

%{?akmod_install}


%check
# If we built modules, check if it was everything the kmodsrc package provided
MODS=$(find $(ls -d %{buildroot}%{_prefix}/lib/modules/* |head -n1) -name '*.ko' -exec basename '{}' \; |wc -l)
DIRS=$(ls %{name}-%{version} |wc -l)
[ $MODS = $DIRS ] || [ $MODS = 0 ]


%changelog
* Fri Nov 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.2.2-100.chinfo
- 5.2.2

* Tue Nov 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.2.0-101.chinfo
- Readd and update linux 4.14 patch

* Tue Nov 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.2.0-100.chinfo
- 5.2.0

* Tue Oct 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.30-100.chinfo
- 5.1.30

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.28-101.chinfo
- Sync with RPMfusion

* Thu Sep 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.28-100.chinfo
- 5.1.28

* Thu Jul 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.26-100.chinfo
- 5.1.26

* Tue Jul 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.24-100.chinfo
- 5.1.24
- Sync with RPMfusion

* Thu Jul 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.22-101.chinfo
- RPMFusion sync

* Sat Apr 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.22-1.chinfo
- 5.1.22

* Tue Apr 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.20-1.chinfo
- 5.1.20

* Wed Mar 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.18-1.chinfo
- 5.1.18

* Thu Mar 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.16-1.chinfo
- 5.1.16

* Wed Jan 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.14-1.chinfo
- 5.1.14

* Sat Jan 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.12-1.chinfo
- 5.1.12

* Tue Nov 22 2016 Sérgio Basto <sergio@serjux.com> - 5.1.10-1
- New upstream vesion, 5.1.10

* Tue Oct 18 2016 Sérgio Basto <sergio@serjux.com> - 5.1.8-1
- Update VBox to 5.1.8

* Tue Sep 13 2016 Sérgio Basto <sergio@serjux.com> - 5.1.6-1
- Update VBox to 5.1.6

* Sat Sep 10 2016 Sérgio Basto <sergio@serjux.com> - 5.1.4-3
- Force use VirtualBox-kmodsrc >= 5.1.4-4, with fix for 4.8.0-rc5

* Wed Sep 07 2016 Sérgio Basto <sergio@serjux.com> - 5.1.4-2
- Force use VirtualBox-kmodsrc >= 5.1.4-3

* Tue Sep 06 2016 Sérgio Basto <sergio@serjux.com> - 5.1.4-1
- Update VBox to 5.1.4

* Mon Jul 18 2016 Sérgio Basto <sergio@serjux.com> - 5.0.26-1
- Update to 5.0.26

* Thu Jul 07 2016 Sérgio Basto <sergio@serjux.com> - 5.0.24-2
- Build only akmods

* Wed Jun 29 2016 Sérgio Basto <sergio@serjux.com> - 5.0.24-1
- Update VirtualBox to 5.0.24
- No more obsolete VirtualBox-OSE , simplify snippets

* Fri Jun 24 2016 Sérgio Basto <sergio@serjux.com> - 5.0.22-1
- Update to 5.0.22

* Sat Apr 23 2016 Sérgio Basto <sergio@serjux.com> - 5.0.18-1
- Update to 5.0.18

* Sun Mar 20 2016 Sérgio Basto <sergio@serjux.com> - 5.0.17-1.106108
- Update to 5.0.17

* Mon Mar 14 2016 Sérgio Basto <sergio@serjux.com> - 5.0.16-2
- Force use of VirtualBox-kmodsrc-5.0.16-3

* Sat Mar 05 2016 Sérgio Basto <sergio@serjux.com> - 5.0.16-1
- Building akmod for VirtualBox 5.0.16

* Wed Jan 20 2016 Sérgio Basto <sergio@serjux.com> - 5.0.14-1
- Building akmod for VirtualBox 5.0.14

* Tue Dec 22 2015 Sérgio Basto <sergio@serjux.com> - 5.0.12-1
- Building akmod for VirtualBox-5.0.12

* Thu Nov 12 2015 Sérgio Basto <sergio@serjux.com> - 5.0.10-1
- Building akmod for VirtualBox-5.0.10

* Thu Oct 22 2015 Sérgio Basto <sergio@serjux.com> - 5.0.8-1
- Update to VirtualBox-5.0.8

* Mon Oct 05 2015 Sérgio Basto <sergio@serjux.com> - 5.0.6-1
- Update to VirtualBox-5.0.6

* Fri Sep 25 2015 Sérgio Basto <sergio@serjux.com> - 5.0.4-2
- no debuginfo, if we, just build akmod, debuginfo will be empty.

* Thu Sep 24 2015 Sérgio Basto <sergio@serjux.com> - 5.0.4-1
- Update to 5.0.4, just build akmod.

* Fri Jul 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.30-1.2
- Rebuilt for kernel

* Thu Jul 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.30-1.1
- Rebuilt for kernel

* Wed Jul 15 2015 Sérgio Basto <sergio@serjux.com> - 4.3.30-1
- New upstream release (4.3.30), build akmods.
- Invert logic of conditional build, just to have more logic.

* Thu Jul 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.28-1.6
- Rebuilt for kernel

* Sun Jun 28 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.28-1.5
- Rebuilt for kernel

* Wed Jun 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.28-1.4
- Rebuilt for kernel

* Tue Jun 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.28-1.3
- Rebuilt for kernel

* Sun May 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.28-1.2
- Rebuilt for kernel

* Wed May 20 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.28-1.1
- Rebuilt for kernel

* Wed May 13 2015 Sérgio Basto <sergio@serjux.com> - 4.3.28-1
- New upstream release (4.3.28), build akmods.

* Wed May 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.26-2.2
- Rebuilt for kernel

* Sat May 09 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.26-2.1
- Rebuilt for kernel

* Tue May 05 2015 Sérgio Basto <sergio@serjux.com> - 4.3.26-2
- Rebuild for newest VirtualBox-kmodsrc and build a new akmod .

* Sat May 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.26-1.6
- Rebuilt for kernel

* Wed Apr 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.26-1.5
- Rebuilt for kernel

* Wed Apr 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.26-1.4
- Rebuilt for kernel

* Mon Mar 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.26-1.3
- Rebuilt for kernel

* Fri Mar 27 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.26-1.1
- Rebuilt for kernel

* Tue Mar 24 2015 Leigh Scott <leigh123linux@googlemail.com> - 4.3.26-1
- New upstream release.

* Mon Mar 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.8
- Rebuilt for kernel

* Sat Mar 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.7
- Rebuilt for kernel

* Tue Mar 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.6
- Rebuilt for kernel

* Fri Mar 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.5
- Rebuilt for kernel

* Sat Feb 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.4
- Rebuilt for kernel

* Sun Feb 08 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.3
- Rebuilt for kernel

* Wed Feb 04 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.2
- Rebuilt for kernel

* Mon Feb 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-4.1
- Rebuilt for kernel

* Mon Jan 26 2015 Leigh Scott <leigh123linux@googlemail.com> - 4.3.20-4
- fix build issue

* Thu Jan 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-3.5
- Bump

* Wed Jan 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-2.5
- Rebuilt for kernel

* Sat Jan 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-2.3
- Rebuilt for kernel

* Sun Dec 21 2014 Sérgio Basto <sergio@serjux.com> - 4.3.20-2.3
- s/$RPM_BUILD_ROOT/%{buildroot}/g.

* Fri Dec 19 2014 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-2.2
- Rebuilt for kernel

* Sun Dec 14 2014 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-2.1
- Rebuilt for kernel

* Fri Dec 05 2014 Nicolas Chauvet <kwizart@gmail.com> - 4.3.20-2
- Rebuilt for f21 final kernel

* Sun Nov 23 2014 Sérgio Basto <sergio@serjux.com> - 4.3.20-1
- New upstream release and just build akmods for devel.

* Sun Oct 12 2014 Sérgio Basto <sergio@serjux.com> - 4.3.18-1
- New upstream release and just build akmods for devel.

* Thu Sep 11 2014 Sérgio Basto <sergio@serjux.com> - 4.3.16-1
- New upstream release and just build akmods for devel.

* Fri Jul 25 2014 Sérgio Basto <sergio@serjux.com> - 4.3.14-1
- New upstream release and just build akmods for rawhide/F21.

* Sun May 18 2014 Sérgio Basto <sergio@serjux.com> - 4.3.12-1
- New upstream release and just build akmods for rawhide.

* Fri May 02 2014 Sérgio Basto <sergio@serjux.com> - 4.3.10-2
- Rebuild for new x11-xorg-server

* Mon Mar 31 2014 Sérgio Basto <sergio@serjux.com> - 4.3.10-1
- New upstream release and just build akmods for rawhide

* Fri Mar 14 2014 Sérgio Basto <sergio@serjux.com> - 4.3.8-1
- New upstream release and just build akmods for rawhide

* Wed Dec 25 2013 Sérgio Basto <sergio@serjux.com> - 4.3.6-2
- Rebuild for newest VirtualBox-kmodsrc and just build akmods for rawhide.

* Thu Dec 19 2013 Sérgio Basto <sergio@serjux.com> - 4.3.6-1
- New upstream release.

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.3.4-4
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.3.4-3
- Rebuilt for f20 final kernel

* Sat Nov 30 2013 Sérgio Basto <sergio@serjux.com> - 4.3.4-1
- New upstream release.

* Sat Nov 02 2013 Sérgio Basto <sergio@serjux.com> - 4.3.2-1
- New upstream release.

* Wed Oct 30 2013 Sérgio Basto <sergio@serjux.com> - 4.3.0-2
- Don't disable hardening which create /dev/vboxdrvu .

* Mon Oct 28 2013 Sérgio Basto <sergio@serjux.com> - 4.3.0-1
- New upstream release.

* Sun Sep 29 2013 Sérgio Basto <sergio@serjux.com> - 4.2.18-2
- Build with patch Additions/linux: fix shared folders for Linux 3.11

* Thu Sep 26 2013 Sérgio Basto <sergio@serjux.com> - 4.2.18-1
- New upstream release.

* Sun Sep 01 2013 Sérgio Basto <sergio@serjux.com> - 4.2.16-2
- Build akmods with src patched for kernel 3.11

* Sat Jul 06 2013 Sérgio Basto <sergio@serjux.com> - 4.2.16-1
- New upstream release.

* Sat Jun 29 2013 Sérgio Basto <sergio@serjux.com> - 4.2.14-1
- New upstream release.

* Mon Apr 15 2013 Sérgio Basto <sergio@serjux.com> - 4.2.12-1
- New upstream release.

* Sat Mar 16 2013 Sérgio Basto <sergio@serjux.com> - 4.2.10-1
- New upstream release.

* Sat Mar 02 2013 Sérgio Basto <sergio@serjux.com> - 4.2.8-1
- New upstream release.

* Tue Dec 25 2012 Sérgio Basto <sergio@serjux.com> - 4.2.6-1
- New upstream release.

* Sun Sep 23 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-2
- Build with newest VirtualBox-kmodsrc (4.2.0-3).

* Sat Sep 15 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-1
- 4.2.0 released

* Sun Sep 09 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.2.RC4
- New RC4
- Force use VirtualBox-kmodsrc >= 4.2.0-0.6

* Sat Sep 01 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.1.RC3
- New RC major upstream release.

* Thu Jun 21 2012 Sérgio Basto <sergio@serjux.com> - 4.1.18-1
- New upstream release.

* Wed Jun 13 2012 Sérgio Basto <sergio@serjux.com> - 4.1.16-2
- build with patches to kernels 3.5

* Wed May 23 2012 Sérgio Basto <sergio@serjux.com> - 4.1.16-1
- New upstream release.

* Sat May 19 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-4
- Bump a release.

* Fri May 18 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-3
- Rename to VirtualBox-kmod

* Mon May 07 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-2
- A little review.

* Fri Apr 27 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-1
- New release.

* Tue Apr 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.1.12-3
- Update for UsrMove

* Mon Apr 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.1.12-2.2
- rebuild for updated kernel

* Fri Apr 13 2012 Sérgio Basto <sergio@serjux.com> - 4.1.12-2.1
- Just build akmods

* Fri Apr 13 2012 Sérgio Basto <sergio@serjux.com> - 4.1.12-1.1
- New release

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.1.8-1.3
- rebuild for beta kernel

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.1.8-1.2
- Rebuild for UsrMove

* Fri Dec 23 2011 Sérgio Basto <sergio@serjux.com> - 4.1.8-1
- New release.

* Sun Dec 11 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-2
- rebuild for update kmodsrc.

* Sat Dec 3 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-1
- Build for new release
- added time package to AkmodsBuildRequires
- removed clean section

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1.4
- Rebuild for F-16 kernel

* Tue Nov 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1.3
- Rebuild for F-16 kernel

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1.2
- Rebuild for F-16 kernel

* Sun Oct 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1.1
- Rebuild for F-16 kernel

* Thu Sep 22 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.1.2-1
- New release
- Added vboxpci

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4.0.4-2
- rebuild for F15 release kernel

* Mon Apr 04 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.0.4-1
- New release

* Mon Feb 14 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.0.2-2
- Fix module symbol versioning

* Sat Feb 05 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.0.2-1
- New release

* Tue Jan 11 2011 Lubomir Rintel <lkundrak@v3.sk> - 3.2.10-2
- Fix build with 2.6.37

* Tue Nov 16 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.10-1
- New release

* Mon Jul 12 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.6-1
- New release

* Fri Jun 18 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.4-1
- New release

* Mon May 10 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.0-1
- Release

* Mon May 10 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.0-0.2.beta2
- Beta 2

* Thu Apr 29 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.0-0.1.beta1
- Beta

* Fri Mar 26 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.1.6-1
- New release

* Wed Feb 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.1.4-1
- New release

* Tue Jan 26 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.1.2-1
- New release

* Sun Dec 06 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.1.0-1
- stable

* Tue Nov 24 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.1.0-0.1.beta2
- Bump to beta2

* Thu Nov 12 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.1.0-0.1.beta1
- Bump to beta

* Sun Nov 01 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.10-1
- Version bump

* Wed Oct 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.8-1
- Version bump

* Mon Aug 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.6-1
- Update to 3.0.6, re-enable hardening

* Mon Aug 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-4
- Source package is now xz-compressed

* Sat Aug 15 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-2
- Make it possible to disable hardening, do so by default

* Sun Aug 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-1
- New release
- Check that we build all modules present

* Tue Aug 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.2-2
- Add netadp bmodule (Vlastimil Holer, #744)

* Sun Jul 12 2009 Jonathan Dieter <jdieter@gmail.com> - 3.0.2-1
- New release

* Fri Jul 03 2009 Jonathan Dieter <jdieter@gmail.com> - 3.0.0-1
- New release

* Thu Jul 02 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.4-2
- Enable the DRM module

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.2.4-1.1
- rebuild for final F11 kernel

* Sun May 31 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.4-1
- New release

* Sun May 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.2-1
- New release

* Sat Apr 25 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.0-1
- New release

* Fri Apr 24 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.4-2
- Fix akmod requires

* Sat Mar 14 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.4-1
- Update to 2.1.4
- Enable VBOX_USE_INSERT_PAGE (VirtualBox #3403)
- Use packed source code tarball

* Sat Jan 24 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.2-1
- Update to 2.1.2

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.0-2
- Cosmetic fixes
- Fix build of standalone akmod

* Tue Dec 30 2008 Lubomir Rintel <lkundrak@v3.sk> - 2.1.0-1
- New upstream version

* Tue Sep 02 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.6.4-2
- Use the VirtualBox-OSE build-time generated source tree

* Tue Sep 02 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.6.4-1
- New upstream version, don't build for Xen needlessly

* Sat Mar 08 2008 Till Maas <opensource till name> - 1.5.6-3
- rewrite to a kmodspec for rpmfusion

* Fri Mar 07 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.5.6-2
- Fix build by passing kernel source tree path to make

* Sun Feb 24 2008 Till Maas <opensource till name> - 1.5.6-1
- update to new version

* Sun Jan 20 2008 Till Maas <opensource till name> - 1.5.4-1
- initial spec, split out from VirtualBox-OSE spec
