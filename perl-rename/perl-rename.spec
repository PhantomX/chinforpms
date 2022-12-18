%global pkgname rename

Name:           perl-%{pkgname}
Version:        1.12
Release:        1%{?dist}
Summary:        Renames multiple files using Perl regular expressions

License:        (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/rename

Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEDERST/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
%{summary}.

%prep
%autosetup -n %{pkgname}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build


%install

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


mv %{buildroot}%{_bindir}/%{pkgname} %{buildroot}%{_bindir}/p%{pkgname}
ln -s p%{pkgname} %{buildroot}%{_bindir}/%{name}

mv %{buildroot}%{_mandir}/man1/rename.1 %{buildroot}%{_mandir}/man1/p%{pkgname}.1
ln -s p%{pkgname}.1 %{buildroot}%{_mandir}/man1/%{name}.1


%files
%doc README.md
%{_bindir}/p%{pkgname}
%{_bindir}/%{name}
%{_mandir}/man1/*.1*


%changelog
* Sat Dec 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.12-1
- 1.12

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.11-1
- 1.11

* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.9-1
- Initial spec
