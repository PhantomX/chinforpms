Summary:        The GObject Builder
Name:           gob2
Version:        2.0.20
Release:        100%{?dist}

License:        GPL-2.0-or-later
Url:            http://www.5z.com/jirka/gob.html

Source0:        http://ftp.5z.com/pub/gob/gob2-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  flex-static
BuildRequires:  pkgconfig(glib-2.0)


%description
GOB is a simple preprocessor for making GObject objects (glib objects).
It makes objects from a single file which has inline C code so that
you don't have to edit the generated files.  Syntax is somewhat inspired
by java and yacc.  It supports generating C++ code


%prep
%autosetup

%build
%configure

%make_build


%install
%make_install


%files
%doc README AUTHORS COPYING NEWS TODO ChangeLog
%doc examples
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*

%changelog
* Thu Apr 22 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0.20-100
- 2.0.20

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.19-1
- update to version 2.0.19

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 14 2011 Jan Kaluza <jkaluza@redhat.com> - 2.0.18-1
- added upstream version 2.0.18

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 07 2010 Jan Kaluza <jkaluza@redhat.com> 2.0.17-2
- added dependency on flex-static

* Thu Aug 05 2010 Jan Kaluza <jkaluza@redhat.com> 2.0.17-1
- new upstream version 2.0.17

* Thu Dec 03 2009 Daniel Novotny <dnovotny@redhat.com> 2.0.16-4
- fixed "Source:" URL in spec (merge review: #225851)

* Tue Nov 24 2009 Daniel Novotny <dnovotny@redhat.com> 2.0.16-3
- fix #519108 class and enum names convert incorrectly in mock / koji.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel Novotny <dnovotny@redhat.com> 2.0.16-1
- new upstream version 2.0.16

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Daniel Novotny <dnovotny@redhat.com> - 2.0.15-3
- summary fix

* Wed Feb 13 2008 Tomas Smetana <tsmetana@redhat.com> - 2.0.15-2
- rebuild (gcc-4.3)

* Mon Dec 03 2007 Tomas Smetana <tsmetana@redhat.com> - 2.0.15-1
- new upstream version

* Wed Aug 29 2007 Tomas Smetana <tsmetana@redhat.com> - 2.0.14-4
- rebuild (because of BuildID)

* Mon Aug 20 2007 Tomas Smetana <tsmetana@redhat.com> - 2.0.14-3
- license tag update

* Wed Apr 18 2007 Harald Hoyer <harald@redhat.com> - 2.0.14-2
- specfile review

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.14-1.1
- rebuild

* Mon May 29 2006 Harald Hoyer <harald@redhat.com> - 2.0.14-1
- more build requires (bug #193395)
- new version 2.0.14

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.12-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.12-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Harald Hoyer <harald@redhat.com>
- version 2.0.12

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Wed Feb 09 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Mon Nov 22 2004 Harald Hoyer <harald@faro.stuttgart.redhat.com> - 2.0.11-1
- version 2.0.11

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Harald Hoyer <harald@faro.stuttgart.redhat.com> - 2.0.6-3
- BuildRequires glib2-devel (111009)

* Wed Aug  6 2003 Harald Hoyer <harald@redhat.de> 2.0.6-2
- rebuild, redhatified specfile

* Fri Sep 28 2001  George Lebl <jirka@5z.com>
- Updated for gob2

* Tue Feb 7 2000  George Lebl <jirka@5z.com>
- added %%{prefix}/share/aclocal/* to %%files

* Tue Dec 14 1999  George Lebl <jirka@5z.com>
- added the examples dir to the %%doc

* Mon Aug 16 1999  George Lebl <jirka@5z.com>
- added gob.spec.in file

