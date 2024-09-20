%define repo chinforpms

Name:           buildsys-build-%{repo}
Epoch:          11
Version:        41
Release:        1%{?dist}
Summary:        Tools and files used by the %{repo} buildsys 

License:        MIT
URL:            http://rpmfusion.org

Source2:        %{name}-list-kernels.sh
Source5:        %{name}-README
Source11:       %{name}-kerneldevpkgs-current

# provide this to avoid a error when generating akmods packages
Provides:       buildsys-build-%{repo}-kerneldevpkgs-akmod-%{_target_cpu}

# unneeded
%define debug_package %{nil}

%description
This package contains tools and lists of recent kernels that get used when
building kmod-packages.

%package        kerneldevpkgs-current
Summary:        Meta-package to get all current kernel-devel packages into the buildroot
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-current-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-newest-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:       %{_bindir}/kmodtool
BuildRequires:  %{_bindir}/kmodtool

# we use our own magic here to safe ourself to cut'n'paste the BR
%{expand:%(bash %{SOURCE2} --current --requires --prefix %{_sourcedir}/%{name}- 2>/dev/null)}

%description kerneldevpkgs-current
This is a meta-package used by the buildsystem to track the kernel-devel
packages for all current up-to-date kernels into the buildroot to build
kmods against them.

%files kerneldevpkgs-current
%doc .tmp/current/README

%prep
# for debugging purposes output the stuff we use during the rpm generation
bash %{SOURCE2} --current --requires --prefix %{_sourcedir}/%{name}-
sleep 2


%build
echo nothing to build


%install
rm -rf $RPM_BUILD_ROOT .tmp/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name} $RPM_BUILD_ROOT/%{_bindir} .tmp/newest .tmp/current

# install the stuff we need
install -p -m 0755 %{SOURCE2}  $RPM_BUILD_ROOT/%{_bindir}/%{name}-kerneldevpkgs
install -p -m 0644 %{SOURCE5}  .tmp/current/README
ln -s kerneldevpkgs-current $RPM_BUILD_ROOT/%{_datadir}/%{name}/kerneldevpkgs-newest
install -p -m 0644 %{SOURCE11} $RPM_BUILD_ROOT/%{_datadir}/%{name}/kerneldevpkgs-current


# adjust default-path
sed -i 's|^default_prefix=.*|default_prefix=%{_datadir}/%{name}/|'  \
 $RPM_BUILD_ROOT/%{_bindir}/%{name}-kerneldevpkgs


%files
%{_bindir}/*
%{_datadir}/%{name}/



%changelog
* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 11:41-1
- Bump for 41

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 11:39-2
- Bump for 40

* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 11:39-1
- Bump for 39

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 11:38-1
- Bump for 38

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 11:37-1
- Bump for 37

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 11:35-1
- Bump for 35

* Sat May 22 2021 Phantom X <megaphantomx at hotmail dot com> - 11:34-2
- Rename to buildsys-build-chinforpms

* Sat Apr 24 2021 Leigh Scott <leigh123linux@gmail.com> - 11:34-1
- rebuild for kernel 5.11.12-300.fc34

* Thu Mar 04 2021 Leigh Scott <leigh123linux@gmail.com> - 11:34-0.2
- rebuild for kernel 5.11.2-300.fc34

* Fri Aug 21 2020 Leigh Scott <leigh123linux@gmail.com> - 11:34-0.1
- Bump for 34

* Mon Feb 17 2020 Leigh Scott <leigh123linux@gmail.com> - 11:33-0.1
- Bump for 33

* Fri Aug 16 2019 Leigh Scott <leigh123linux@gmail.com> - 11:32-0.1
- Bump for 32

* Sun Mar 31 2019 Leigh Scott <leigh123linux@googlemail.com> - 10:31-0.1
- Bump for 31

* Thu Aug 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 10:30-0.1
- Bump for 30

* Mon Apr 16 2018 Nicolas Chauvet <kwizart@gmail.com> - 10:29-0.2
- rebuild for kernel 4.16.2-300.fc28

* Tue Mar 06 2018 Nicolas Chauvet <kwizart@gmail.com> - 10:28-0.1
- Bump for 29

* Mon Sep 04 2017 Nicolas Chauvet <kwizart@gmail.com> - 10:27-0.1
- bump for 27

* Sat Mar 18 2017 Nicolas Chauvet <kwizart@gmail.com> - 10:26-0.4
- rebuild for kernel 4.11.0-0.rc2.git2.2.fc26

* Sat Mar 18 2017 Nicolas Chauvet <kwizart@gmail.com> - 10:26-0.3
- rebuild for kernel 4.11.0-0.rc2.git2.2.fc26

* Sat Aug 06 2016 Nicolas Chauvet <kwizart@gmail.com> - 10:26-0.2
- Bump for 26

* Fri Jul 01 2016 Nicolas Chauvet <kwizart@gmail.com> - 10:25-0.2
- rebuild for kernel 4.6.3-300.fc24.x86_64

* Sun Jun 12 2016 Nicolas Chauvet <kwizart@gmail.com> - 10:25-0.1
- Update to 25

* Mon May 16 2016 Nicolas Chauvet <kwizart@gmail.com> - 10:24-0.2
- Bump for 24

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:23-1
- rebuild for kernel 4.2.3-300.fc23

* Fri Aug 07 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-7
- rebuild for kernel 4.1.4-200.fc22

* Wed Aug 05 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-6
- rebuild for kernel 4.1.3-200.fc22

* Wed Aug 05 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-5
- rebuild for kernel 4.1.3-201.fc22

* Wed Jul 29 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-4
- rebuild for kernel 4.1.2-200.fc22

* Fri Jul 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-3
- rebuild for kernel 4.1.3-200.fc22

* Wed Jul 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-2
- rebuild for kernel 4.0.8-300.fc22

* Mon May 25 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-1
- rebuild for kernel 4.0.4-301.fc22

* Mon May 11 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-0.2
- Rebuilt for kernel 4.0.2-300.fc22

* Tue May 05 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:22-0.1
- Bump for f22 branch

* Wed Apr 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-20
- rebuild for kernel 3.19.5-200.fc21

* Wed Apr 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-19.1
- rebuild for kernel 3.19.4-200.fc21

* Fri Apr 03 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-18.1
- Rebuilt for refresh repodata

* Sat Mar 28 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-18
- rebuild for kernel 3.19.3-200.fc21

* Fri Mar 27 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-17
- rebuild for kernel 3.19.2-201.fc21

* Mon Mar 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-16
- rebuild for kernel 3.19.2-200.fc21

* Sat Mar 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-15
- rebuild for kernel 3.19.1-201.fc21

* Tue Mar 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-14
- rebuild for kernel 3.18.9-200.fc21

* Tue Mar 03 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-13
- rebuild for kernel 3.18.8-201.fc21

* Sat Feb 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-12
- rebuild for kernel 3.18.7-200.fc21

* Sun Feb 08 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-11
- rebuild for kernel 3.18.6-200.fc21

* Wed Feb 04 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-10
- rebuild for kernel 3.18.5-201.fc21

* Sat Jan 31 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-9
- rebuild for kernel 3.18.5-200.fc21

* Wed Jan 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-8
- rebuild for kernel 3.18.3-201.fc21

* Thu Jan 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-7
- rebuild for kernel 3.18.2-200.fc21

* Sat Jan 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 10:21-6
- rebuild for kernel 3.17.8-300.fc21

* Thu Dec 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 10:21-5
- rebuild for kernel 3.17.7-300.fc21

* Sun Dec 14 2014 Nicolas Chauvet <kwizart@gmail.com> - 10:21-4
- rebuild for kernel 3.17.6-300.fc21

* Sat Dec 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 10:21-2
- rebuild for kernel 3.17.4-302.fc21

* Fri Dec 05 2014 Nicolas Chauvet <kwizart@gmail.com> - 10:21-1
- rebuild for kernel 3.17.4-301.fc21

* Fri Jul 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 10:21-0.2
- Rebuilt to test fedora branched packages

* Thu Dec 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 10:21-0.1
- Open Fedora-21/Rawhide

* Sat Dec 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 10:20-1
- Tag for F-20 GA

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 10:20-0.6
- rebuild for kernel 3.11.10-301.fc20

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 10:20-0.5
- Fix kernel variant + separator
- rebuild for kernel 3.11.10-300.fc20
- Add support for aarch64

* Sun Dec 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 10:20-0.3
- rebuild for kernel 3.11.9-300.fc20

* Thu Nov 21 2013 Nicolas Chauvet <kwizart@gmail.com> - 10:20-0.2
- Add lpae as a known kvarriant

* Thu Aug 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 10:20-0.1
- Bump for F-20

* Fri Sep 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 10:18-0.2
- Bump for secondary

* Mon Apr 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 10:18-0.1
- Build for default F-18 kernels

* Tue Jan 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 10:17-0.1
- Build for default F-17 kernels

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 10:16-5
- rebuild for kernel 3.1.0-7.fc16

* Sun Oct 30 2011 Nicolas Chauvet <kwizart@gmail.com> - 10:16-4
- rebuild for kernel 3.1.0-5.fc16

* Thu Oct 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 10:16-2
- rebuild for kernel 3.1.0-1.fc16

* Sat Oct 22 2011 Nicolas Chauvet <kwizart@gmail.com> - 10:16-1
- rebuild for kernel 3.1.0-0.rc10.git0.1.fc16

* Sat Oct 22 2011 Nicolas Chauvet <kwizart@gmail.com> - 10:16-0
- Introduce F-16

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:15-1
- rebuild for kernel 2.6.38.6-26.rc1.fc15

* Thu May 05 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-11
- rebuild for kernel 2.6.35.13-91.fc14

* Sun Apr 24 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-10
- rebuild for kernel 2.6.35.12-90.fc14

* Mon Apr 04 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-9
- rebuild for kernel 2.6.35.12-88.fc14

* Sat Feb 12 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-8
- rebuild for kernel 2.6.35.11-83.fc14

* Fri Dec 24 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-7
- rebuild for kernel 2.6.35.10-74.fc14

* Wed Dec 22 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-6
- rebuild for kernel 2.6.35.10-72.fc14

* Mon Dec 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-5
- rebuild for kernel 2.6.35.10-69.fc14

* Fri Dec 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-4
- rebuild for kernel 2.6.35.10-68.fc14

* Sun Dec 05 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-3
- rebuild for kernel 2.6.35.9-64.fc14

* Mon Nov 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-2
- rebuild for kernel 2.6.35.6-48.fc14

* Fri Oct 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:14-1
- rebuild for kernel 2.6.35.6-45.fc14

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:13-0.1
- no i586 in devel anymore, so adjust ExclusiveArch and 
  buildsys-build-rpmfusion-list-kernels.sh

* Sun Jun 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:12-0.1
- rebuild for rawhide

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.11
- rebuild for kernel 2.6.29.4-167.fc11

* Mon Apr 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.10
- use isa to make sure we get the right kernel 

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.9
- rebuild for new F11 features

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.8
- adjust for Fedora new kenrels scheme
- use a different way to generate lists

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.7
- rebuild, and just use the latest as default

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.6
- rebuild for kernel 2.6.29-0.25.rc0.git14.fc11

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.5
- rebuild for kernel 2.6.29-0.9.rc0.git4.fc11

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.4
- rebuild for kernel 2.6.28-3.fc11

* Sat Dec 27 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.3
- just track in the latest kernel

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.2
- rebuild for kernel 2.6.28-0.140.rc9.git1.fc11

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:11-0.1
- rebuild for kernel 2.6.28-0.127.rc8.git1.fc11

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.11
- rebuild for kernel 2.6.27.5-117.fc10

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.10
- rebuild for kernel 2.6.27.5-113.fc10

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.9
- rebuild for kernel 2.6.27.5-109.fc10

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.8
- rebuild for kernel 2.6.27.4-79.fc10

* Fri Nov 07 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.7
- rebuilt

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.6
- rebuild for kernel 2.6.27.4-68.fc10

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 10:10-0.5
- rebuild for kernel 2.6.27.4-47.rc3.fc10

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 10:10-0.4
- rebuild for kernel 2.6.27.3-27.rc1.fc10

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10:10-0.3
- install filterfile for ppc64

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10:10-0.2
- don't use the --buildrequires stuff, doesn't work in plague/mock
- provide compatible symlink for "newest"

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10:10-0.1
- adjust things for rawhide
-- no xen kernels anymore, so no need for the whole newest and current handling
-- just require kernels unversioned if buildsys-build-rpmfusion-kerneldevpkgs
   contains lines with "default"

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-3
- adjust output for new kernel scheme

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-2
- add epoch to provides/requires

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-1
- Build for F9 kernel

* Mon Mar 31 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2-2
- Update to latest kernels 2.6.24.4-64.fc8 2.6.21.7-3.fc8xen

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:1-2
- s/akmods/akmod/

* Wed Jan 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:1-3
- Build for rawhide
- disable kerneldevpkgs-newest and kerneldevpkgs-current packages, as we
  don't maintain them for rawhide
- add epoch for new versioning scheme

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 22-1
- Update to latest kernels 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 22-1
- Update to latest kernels 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 21-1
- Update to latest kernels 2.6.23.8-63.fc8 2.6.21-2952.fc8xen

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 20-1
- Update to latest kernels 2.6.23.1-49.fc8 2.6.21-2950.fc8xen

* Mon Oct 29 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 19-1
- Update to latest kernels 2.6.23.1-41.fc8 2.6.21-2950.fc8xen

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 18-1
- Update to latest kernels 2.6.23.1-41.fc8 2.6.21-2950.fc8xen

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-3
- don't include file with know variants and instead properly fix the script

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-2
- include file with know variants as it is needed in buildsys

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-1
- split buildsys stuff out into a seperate package
- rename to buildsys-build-rpmfusion
- add proper obsoletes
- give subpackages and files more sane names and places

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 16-2
- Update to latest kernels 2.6.23.1-35.fc8 2.6.21-2950.fc8xen

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 16-1
- Update to latest kernels 2.6.23.1-35.fc8 2.6.21-2949.fc8xen

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 15-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 14-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 13-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 12-1
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 11-1
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10-1
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9-2
- fix typo

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9-1
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8-1
- update for 2.6.23-0.224.rc9.git6.fc8

* Sun Oct 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 7-1
- update for 2.6.23-0.222.rc9.git1.fc8

* Wed Oct 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 6-1
- update for 2.6.23-0.217.rc9.git1.fc8 and 2.6.21-2947.fc8xen

* Wed Oct 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5-1
- disable --all-but-latest stuff -- does not work as expected
- rename up2date list of kernels from "latest" to "current" as latest 
  and newest are to similar in wording; asjust script as well
- kmodtool: don't provide kernel-modules, not needed anymore with
  the new stayle and hurts

* Sun Sep 09 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4-2
- fix typos in spec file and list-kernels script
- interdependencies between the two buildsys-build packages needs to be
  arch specific as well

* Sun Sep 09 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4-1
- s/latests/latest/
- update kernel lists for rawhide and test2 kernels
- make kmod-helpers-livna-list-kernels print BuildRequires for all kernels
  as well; this is not needed and will slow build a bit as it will track 
  all the kernel-devel packages in, but that way we make sure they are really
  available in the buildsys

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-4
- implement proper arch deps 

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-3
- proper list of todays rawhide-kernels

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-2
- fix typo in kmod-helpers-livna-latests-kernels

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-1
- adjust for devel

* Sat Sep 01 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2-1
- initial package
