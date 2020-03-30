%global use_x11_tests 1

Name:           perl-Gtk3
Version:        0.037
Release:        1%{?dist}
Summary:        Perl interface to the 3.x series of the GTK+ toolkit

License:        LGPLv2+
URL:            https://metacpan.org/release/Gtk3

Source0:        https://cpan.metacpan.org/authors/id/X/XA/XAOC/Gtk3-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  findutils
BuildRequires:  gtk3
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(Cairo::GObject) >= 1.000
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Glib::Object::Introspection version for
# Glib::Object::Introspection:convert_flags_to_sv(), CPAN RT#122761
BuildRequires:  perl(Glib::Object::Introspection) >= 0.043
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
# Tests
# Config used only on FreeBSD
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Glib)
BuildRequires:  perl(Glib::Object::Subclass)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
%if %{use_x11_tests}
# X11 tests:
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  font(:lang=en)
%endif
Requires:       gtk3 >= 3.24.14
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Cairo::GObject) >= 1.000
# Glib::Object::Introspection version for
# Glib::Object::Introspection:convert_flags_to_sv(), CPAN RT#122761
Requires:       perl(Glib::Object::Introspection) >= 0.043
Requires:       perl(POSIX)

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Cairo::GObject|Glib::Object::Introspection)\\)$

%description
The Gtk3 module allows a Perl developer to use the GTK+ graphical user
interface library. Find out more about GTK+ at <http://www.gtk.org/>.

%prep
%autosetup -n Gtk3-%{version} -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%if %{use_x11_tests}
    xvfb-run -a make test
%else
    make test
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc NEWS README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Mar 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.037-1
- 0.037

* Wed Feb 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.036-3
- Remove fix for https://gitlab.gnome.org/GNOME/gtk/issues/1077, gnomebz#634823

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.036-1
- 0.036 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.035-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.035-2
- Perl 5.30 rebuild

* Tue May 28 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.035-1
- 0.35 bump

* Fri Feb 15 2019 Daniel P. Berrangé <berrange@redhat.com> - 0.034-6
- Re-enable tests skipped from previous build

* Tue Feb 12 2019 Daniel P. Berrange <berrange@redhat.com> - 0.034-5
- Fix for GdkPixdata gir split (rhbz #1675630)
- Temporarily disable tests broken by rhbz #1676474

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.034-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.034-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.034-2
- Perl 5.28 rebuild

* Tue Jun 05 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.034-1
- 0.034 bump

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 10 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.033-1
- 0.033 bump

* Thu Aug 10 2017 Petr Pisar <ppisar@redhat.com> - 0.032-2
- Correct minimal Glib::Object::Introspection version (CPAN RT#122761)

* Thu Aug 10 2017 Petr Pisar <ppisar@redhat.com> - 0.032-1
- 0.032 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.030-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.030-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.030-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.030-1
- 0.030 bump

* Mon Oct 03 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.029-1
- 0.029 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.026-3
- Perl 5.24 rebuild

* Thu May 05 2016 Petr Pisar <ppisar@redhat.com> - 0.026-2
- Adjust tests to gtk3-3.21.1 (bug #1332962)

* Fri Apr 01 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.026-1
- 0.026 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.025-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.025-1
- 0.025 bump

* Fri Sep 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.023-1
- 0.023 bump

* Mon Jul 13 2015 Petr Pisar <ppisar@redhat.com> - 0.022-1
- 0.022 bump

* Wed Jun 17 2015 Daniel P. Berrange <berrange@redhat.com> - 0.021-1
- Update to 0.021 release

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.019-2
- Perl 5.22 rebuild

* Wed Dec 03 2014 Petr Pisar <ppisar@redhat.com> - 0.019-1
- 0.019 bump

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.017-3
- Perl 5.20 rebuild

* Tue Aug 12 2014 Petr Pisar <ppisar@redhat.com> - 0.017-2
- Run X11 tests using xvfb-run (bug #1129395)

* Wed Aug 06 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.017-1
- 0.017 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 10 2013 Daniel P. Berrange <berrange@redhat.com> - 0.015-1
- Update to 0.015 release (rhbz #1021207)

* Tue Oct  1 2013 Daniel P. Berrange <berrange@redhat.com> - 0.013-1
- Update to 0.013 release (rhbz #1003379)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.009-2
- Perl 5.18 rebuild

* Fri Feb 15 2013 Daniel P. Berrange <berrange@redhat.com> - 0.009-1
- Update to 0.009 release (rhbz #829260)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Daniel P. Berrange <berrange@redhat.com> - 0.008-1
- Update to 0.008 release (rhbz #829260)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Daniel P. Berrange <berrange@redhat.com> - 0.007-1
- Update to 0.007 release (rhbz #829260)

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.006-2
- Perl 5.16 rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.006-1
- 0.006 bump

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.005-2
- Perl 5.16 rebuild

* Mon Apr 23 2012 Daniel P. Berrange <berrange@redhat.com> - 0.005-1
- Update to 0.005 release

* Mon Mar 19 2012 Daniel P. Berrange <berrange@redhat.com> - 0.004-1
- Update to 0.004 release

* Wed Feb  8 2012 Daniel P. Berrange <berrange@redhat.com> - 0.003-2
- Add Cairo::GObject BR

* Mon Jan 30 2012 Daniel P. Berrange <berrange@redhat.com> - 0.003-1
- Update to 0.003 release (rhbz #785532)

* Thu Jan  5 2012 Daniel P. Berrange <berrange@redhat.com> - 0.002-2
- Use xvfb to run test suite
- Fix capitalization of GTK+
- Remove dist.ini & perl-Gtk3.doap
- Remove defattr from files section
- Add missing BuildRequires for test suite
- Add trailing / into URIs

* Thu Dec 15 2011 Daniel P. Berrange <berrange@redhat.com> - 0.002-1
- Update to 0.002 release

* Mon Nov 28 2011 Daniel P. Berrange <berrange@redhat.com> - 0.001-2
- Add Test::More BR
- Disable overrides.t test (rt #72773)
- Comment about running test without $DISPLAY available

* Fri Nov 04 2011 Daniel P Berrange <berrange@redhat.com> 0.001-1
- Specfile autogenerated by cpanspec 1.78.
