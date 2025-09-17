%global pkgname App-rename

Name:           perl-rename
Version:        1.16.3
Release:        1%{?dist}
Summary:        Renames multiple files using Perl regular expressions

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/App-rename

Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEDERST/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)

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


mv %{buildroot}%{_bindir}/rename %{buildroot}%{_bindir}/prename
ln -s prename %{buildroot}%{_bindir}/%{name}

mv %{buildroot}%{_mandir}/man1/rename.1 %{buildroot}%{_mandir}/man1/prename.1
ln -s prename.1 %{buildroot}%{_mandir}/man1/%{name}.1


%files
%doc README.md
%{_bindir}/prename
%{_bindir}/%{name}
%{perl_vendorlib}/App
%{_mandir}/man1/*.1*


%changelog
* Tue Sep 16 2025 Phantom X <megaphantomx at hotmail dot com> - 1.16.3-1
- 1.16.3

* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.14-1
- 1.14

* Sat Dec 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.12-1
- 1.12

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.11-1
- 1.11

* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.9-1
- Initial spec
