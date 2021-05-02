%?mingw_package_header

#%%global snapshot_date 20160204
#%%global snapshot_rev 38410ad06264949efcb331f7a63575c6be31c5e4
#%%global snapshot_rev_short %%(echo %%snapshot_rev | cut -c1-6)
#%%global branch trunk

#%%global pre rc2

# Run the testsuite
%global enable_tests 0

Name:           mingw-winpthreads
Version:        8.0.0
Release:        103%{?dist}
Summary:        MinGW pthread library

# The main license of winpthreads is MIT, but parts of this library
# are derived from the "Posix Threads library for Microsoft Windows"
# http://locklessinc.com/articles/pthreads_on_windows/
License:        MIT and BSD
URL:            http://mingw-w64.sourceforge.net/
%if 0%{?snapshot_date}
# To regenerate a snapshot:
# Use your regular webbrowser to open https://sourceforge.net/p/mingw-w64/mingw-w64/ci/%{snapshot_rev}/tarball
# This triggers the SourceForge instructure to generate a snapshot
# After that you can pull in the archive with:
# spectool -g mingw-headers.spec
Source0:        http://sourceforge.net/code-snapshots/git/m/mi/mingw-w64/mingw-w64.git/mingw-w64-mingw-w64-%{snapshot_rev}.zip
%else
Source0:        http://downloads.sourceforge.net/mingw-w64/mingw-w64-v%{version}%{?pre:-%{pre}}.tar.bz2
%endif

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw64-gcc-c++
BuildRequires:  make

%if 0%{?enable_tests}
BuildRequires:  wine-wow
%endif


%description
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.

# Win32
%package -n mingw32-winpthreads
Summary:        MinGW pthread library for the win32 target
Obsoletes:      mingw32-pthreads < 2.8.0-25.20110511cvs
Provides:       mingw32-pthreads = 2.8.0-25.20110511cvs
Conflicts:      mingw32-headers < 2.0.999-0.22.trunk.20130428

%description -n mingw32-winpthreads
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.

%package -n mingw32-winpthreads-static
Summary:        Static version of the MinGW Windows pthreads library
Requires:       mingw32-winpthreads = %{version}-%{release}
Obsoletes:      mingw32-pthreads-static < 2.8.0-25.20110511cvs
Provides:       mingw32-pthreads-static = 2.8.0-25.20110511cvs

%description -n mingw32-winpthreads-static
Static version of the MinGW Windows pthreads library.

# Win64
%package -n mingw64-winpthreads
Summary:        MinGW pthread library for the win64 target
Obsoletes:      mingw64-pthreads < 2.8.0-25.20110511cvs
Provides:       mingw64-pthreads = 2.8.0-25.20110511cvs
Conflicts:      mingw64-headers < 2.0.999-0.22.trunk.20130428

%description -n mingw64-winpthreads
The POSIX 1003.1-2001 standard defines an application programming
interface (API) for writing multithreaded applications. This interface
is known more commonly as pthreads. A good number of modern operating
systems include a threading library of some kind: Solaris (UI)
threads, Win32 threads, DCE threads, DECthreads, or any of the draft
revisions of the pthreads standard. The trend is that most of these
systems are slowly adopting the pthreads standard API, with
application developers following suit to reduce porting woes.

Win32 does not, and is unlikely to ever, support pthreads
natively. This project seeks to provide a freely available and
high-quality solution to this problem.

%package -n mingw64-winpthreads-static
Summary:        Static version of the MinGW Windows pthreads library
Requires:       mingw64-winpthreads = %{version}-%{release}
Obsoletes:      mingw64-pthreads-static < 2.8.0-25.20110511cvs
Provides:       mingw64-pthreads-static = 2.8.0-25.20110511cvs

%description -n mingw64-winpthreads-static
Static version of the MinGW Windows pthreads library.


%?mingw_debug_package


%prep
%if 0%{?snapshot_date}
rm -rf mingw-w64-v%{version}
mkdir mingw-w64-v%{version}
cd mingw-w64-v%{version}
unzip %{S:0}
%autosetup -p1 -D -T -n mingw-w64-v%{version}/mingw-w64-mingw-w64-%{snapshot_rev}
%else
%autosetup -p1 -n mingw-w64-v%{version}%{?pre:-%{pre}}
%endif


%build
pushd mingw-w64-libraries/winpthreads
    %mingw_configure
    %mingw_make %{?smp_mflags}
popd


%if 0%{?enable_tests}

%check
# Prepare a wine prefix
export WINEPREFIX=/tmp/wine-winpthreads
mkdir $WINEPREFIX
winecfg || :

# Run the tests
pushd mingw-w64-libraries/winpthreads
    %mingw_make check -k || :
popd

# Clean up the wine prefix
wineserver --kill || :
rm -rf /tmp/wine-winpthreads

%endif


%install
pushd mingw-w64-libraries/winpthreads
    %mingw_make install DESTDIR=$RPM_BUILD_ROOT
popd

# Drop all .la files
find $RPM_BUILD_ROOT -name "*.la" -delete


# Win32
%files -n mingw32-winpthreads
%license COPYING
%{mingw32_bindir}/libwinpthread-1.dll
%{mingw32_libdir}/libwinpthread.dll.a
%{mingw32_libdir}/libpthread.dll.a
%{mingw32_includedir}/pthread.h
%{mingw32_includedir}/pthread_compat.h
%{mingw32_includedir}/pthread_signal.h
%{mingw32_includedir}/pthread_time.h
%{mingw32_includedir}/pthread_unistd.h
%{mingw32_includedir}/sched.h
%{mingw32_includedir}/semaphore.h

%files -n mingw32-winpthreads-static
%{mingw32_libdir}/libwinpthread.a
%{mingw32_libdir}/libpthread.a

# Win64
%files -n mingw64-winpthreads
%license COPYING
%{mingw64_bindir}/libwinpthread-1.dll
%{mingw64_libdir}/libwinpthread.dll.a
%{mingw64_libdir}/libpthread.dll.a
%{mingw64_includedir}/pthread.h
%{mingw64_includedir}/pthread_compat.h
%{mingw64_includedir}/pthread_signal.h
%{mingw64_includedir}/pthread_time.h
%{mingw64_includedir}/pthread_unistd.h
%{mingw64_includedir}/sched.h
%{mingw64_includedir}/semaphore.h

%files -n mingw64-winpthreads-static
%{mingw64_libdir}/libwinpthread.a
%{mingw64_libdir}/libpthread.a


%changelog
* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 8.0.0-103
- Rebuild

* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 8.0.0-102
- Another rebuild

* Fri Jan 29 2021 Phantom X <megaphantomx at hotmail dot com> - 8.0.0-101
- Rebuild

* Wed Oct 07 2020 Phantom X <megaphantomx at hotmail dot com> - 8.0.0-100
- 8.0.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 20 2020 Sandro Mani <manisandro@gmail.com> - 7.0.0-1
- Update to 7.0.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Sandro Mani <manisandro@gmail.com> - 6.0.0-1
- Update to 6.0.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Kalev Lember <klember@redhat.com> - 5.0.4-1
- Update to 5.0.4

* Thu Jun 14 2018 Sandro Mani <manisandro@gmail.com> - 5.0.3-1
- Update to 5.0.3

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Kalev Lember <klember@redhat.com> - 5.0.2-1
- Update to 5.0.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Kalev Lember <klember@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Wed Oct 26 2016 Kalev Lember <klember@redhat.com> - 5.0.0-1
- Update to 5.0.0
- Don't set group tags
- Use license macro

* Sun Mar 27 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0-0.1.rc2
- Update to 5.0-rc2

* Thu Feb  4 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.999-0.3.trunk.git38410a.20160204
- Update to 20160204 snapshot (git rev 38410a)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.999-0.2.trunk.git5e2e73.20151224
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.999-0.1.trunk.git.5e2e73.20151224
- Update to 20151224 snapshot (git rev 5e2e73)

* Wed Aug  5 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2

* Sun Mar 29 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1

* Sat Mar 21 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0

* Sat Mar  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0-0.2.rc3
- Update to 4.0rc3

* Mon Jan 26 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0-0.1.rc1
- Update to 4.0rc1

* Mon Dec 22 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.5.trunk.git.f7337b.20141222
- Update to 20141222 snapshot (git rev f7337b)

* Tue Dec  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.4.trunk.git.dadc8f.20141209
- Update to 20141209 snapshot (git rev dadc8f)

* Wed Dec  3 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.2.trunk.git.a5c151.20141203
- Update to 20141203 snapshot (git rev a5c151)

* Fri Sep 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.1.trunk.git.b08afb.20140912
- Update to 20140912 snapshot (git rev b08afb)
- Bump version as upstream released mingw-w64 v3.2.0 recently (which is not based on the trunk branch)

* Wed Jul 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.7.trunk.gitec1ff7.20140730
- Update to 20140730 snapshot (git rev ec1ff7)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.999-0.6.trunk.git502c72.20140524
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.5.trunk.git502c72.20140524
- Update to 20140524 snapshot (git rev 502c72)
- Upstream has switched from SVN to Git

* Mon Apr  7 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.4.trunk.r6560.20140407
- Update to r6560 (20140407 snapshot)
- Fixes potential deadlock

* Mon Feb 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.3.trunk.r6497.20140224
- Update to r6497 (20140224 snapshot)

* Fri Jan 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.2.trunk.r6460.20140124
- Update to r6460 (20140124 snapshot)

* Thu Jan  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.1.trunk.r6432.20140104
- Bump version to keep working upgrade path

* Mon Jan  6 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.2.trunk.r6432.20140104
- Update to r6432 (20140104 snapshot)

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.1.trunk.r6379.20131120
- Update to r6379 (20131120 snapshot)

* Fri Sep 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.7.trunk.r6233.20130907
- Update to r6233 (20130907)
- Fixes mingw-libvirt build failure

* Fri Aug 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.6.trunk.r6069.20130810
- Update to r6069 (20130810 snapshot)

* Fri Jun 28 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.5.trunk.r5915.20130628
- Update to r5915 (20130628 snapshot)

* Sat May 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.4.trunk.20130509
- Simplified the BuildRequires
- Added a clarification for the combined license
- Added conflicts for mingw{32,64}-headers versions which also provide pthread headers

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.3.trunk.20130509
- Added -static subpackages
- Changed license to MIT and BSD

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.2.trunk.20130509
- Update to 20130509 snapshot
- Make the testsuite optional

* Mon Apr 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.1.trunk.20130429
- Update to 20130429 snapshot

* Fri Feb 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.1.20120224
- Initial package

