%global pkgname X11-GUITest

%global use_x11_tests 1
Name:           perl-%{pkgname}
Version:        0.28
Release:        21%{?dist}
Summary:        Provides GUI testing/interaction routines

License:        GPL-2.0-or-later
URL:            https://metacpan.org/release/%{pkgname}

Source0:        https://cpan.metacpan.org/modules/by-module/X11/%{pkgname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXt-devel
# libXi-devel is required because it contains X11/extensions/XInput.h in EL6
BuildRequires:  libXi-devel
BuildRequires:  libXtst-devel
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(vars)
%if %{use_x11_tests}
# X11 tests:
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-xinit
BuildRequires:  font(:lang=en)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This Perl package is intended to facilitate the testing of GUI applications
by means of user emulation. It can be used to test/interact with GUI
applications; which have been built upon the X library or toolkits (i.e.,
GTK+, Xt, Qt, Motif, etc.) that "wrap" the X library's functionality.

%prep
%autosetup -n %{pkgname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
%make_build

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


%check
%if %{use_x11_tests}
    xvfb-run -a make test
%else
    make test
%endif

%files
%doc Changes docs README eg ToDo
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/X11*
%{_mandir}/man3/*

%changelog
* Mon Oct 12 2020 Phantom X <megaphantomx at hotmail dot com> - 0.28-21
- Bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-17
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-14
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-10
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-5
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.28-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 David Dick <ddick@cpan.org> - 0.28-1
- Initial release
