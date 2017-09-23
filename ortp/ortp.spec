Name:           ortp
Version:        1.0.2
Release:        101.chinfo%{?dist}
Summary:        A C library implementing the RTP protocol (RFC3550)
Epoch:          1

Group:          System Environment/Libraries
License:        LGPLv2+ and VSL
URL:            http://www.linphone.org/eng/documentation/dev/ortp.html
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  perl-Carp
BuildRequires:  pkgconfig(bctoolbox)


%description
oRTP is a C library that implements RTP (RFC3550).

%package        devel
Summary:        Development libraries for ortp
Group:          Development/Libraries
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig
Requires:       pkgconfig(bctoolbox)

%description    devel
Libraries and headers required to develop software with ortp.

%prep
%autosetup -n %{name}-%{version}-0

sed \
  -e 's|${prefix}/lib)|%{_libdir})|g' \
  -e 's|"-Werror" ||g' \
  -i CMakeLists.txt

%{__perl} -pi.dot  -e 's/^(HAVE_DOT\s+=)\s+NO$/\1 YES/;s/^(CALL_GRAPH\s+=)\s+NO$/\1 YES/;s/^(CALLER_GRAPH\s+=)\s+NO$/\1 YES/' ortp.doxygen.in

%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
  -DENABLE_TESTS:BOOL=OFF

%make_build

%install
%make_install -C builddir

rm -f builddir/doc/html/html.tar
rm -rf %{buildroot}%{_datadir}/doc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS README.md
%license COPYING
%{_libdir}/libortp.so.*

%files devel
%doc builddir/doc/html
%{_includedir}/%{name}
%{_libdir}/libortp.so
%{_libdir}/pkgconfig/ortp.pc
%{_datadir}/oRTP/cmake/*.cmake

%changelog
* Fri Sep 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.2-102.chinfo
- cmake and fixes for it

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-100.chinfo
- 1.0.2

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:1.0.1-1.chinfo
- 1.0.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Tom Callaway <spot@fedoraproject.org> - 1:0.23.0-1
- update to 0.23.0

* Fri Nov 14 2014 Tom Callaway <spot@fedoraproject.org> - 1:0.22.0-5
- rebuild for new libsrtp

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul  7 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.22.0-0
- ortp-0.22.0

* Sat Mar 23 2013 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.20.0-5
- autoreconf in %%prep (#926292)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Alexey Kurov <nucleo@fedoraproject.org> - 1:0.20.0-2
- ortp-0.20.0
- BR: libzrtpcpp-devel for F17+

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.18.0-1
- ortp-0.18.0
- drop patches for issues fixed in upstream (retval and unused vars)

* Tue Sep 27 2011 Dan Horák <dan[at]danny.cz> - 1:0.16.5-2
- fix another gcc warning and move all fixes to one patch

* Fri Sep  2 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.16.5-1
- ortp-0.16.5
- add BR: libsrtp-devel openssl-devel

* Tue Mar 15 2011 Karsten Hopp <karsten@redhat.com> 0.16.1-3.1
- fix build error (unused variable)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep  2 2010 Dan Horák <dan[at]danny.cz> - 1:0.16.1-2
- fix "ignoring return value" warning

* Mon Nov 30 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1:0.16.1-1
- Updated to 0.16.1, removed old patch
- removed autotool calls, and using install -p

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.5.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.14.2-0.4.20080211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.14.2-0.3.20080211
- fix license tag
- epoch bump to fix pre-release versioning

* Thu Feb 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.2-0.20080211.2%{?dist}
- Update to 0.14.2 snapshot

* Tue Feb  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.2
- Apply patch to remove -Werror from the build (for PPC).

* Fri Feb  1 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.14.1-0.20080123.1
- Update to 0.14.1 (using CVS snapshot until official release is available).

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.13.1-4
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-2
- Fix URL

* Mon Apr 23 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-1
- Update to 0.13.1
- BR doxygen and graphviz for building documentation

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.0-1
- Update to 0.13.0
- ortp-devel BR pkgconfig
- Add ldconfig scriptlets

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.12.0-1
- Update to 0.12.0

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-2
- Bring back -Werror patch (needed for building on PPC)

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-1
- Update to 0.11.0
- Remove ortp-0.8.1-Werror.patch

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-3
- Bump release and rebuild

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-2
- Rebuild for Fedora Extras 5

* Tue Jan  3 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-1
- Upstream update

* Thu Dec 22 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-2
- Added ortp.pc to -devel

* Sat Dec  3 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.1-1
- Upstream update

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-6
- Fix a typo in Requires on -devel

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-5
- Add missing Requires on -devel

* Sun Nov 13 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.0-4
- Split from linphone
