%global pkgname rename

Name:           perl-%{pkgname}
Version:        1.9
Release:        1%{?dist}
Summary:        Renames multiple files using Perl regular expressions

License:        (GPL+ or Artistic) and (GPLv2+ or Artistic) and BSD and Public Domain and UCD
URL:            http://search.cpan.org/dist/rename/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEDERST/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
# Remove "BuildRequires:  perl-devel" for noarch packages (unneeded)
BuildRequires:  perl-devel
BuildRequires:  perl-generators
# Correct for lots of packages, other common choices include eg. Module::Build
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
%{summary}.

%prep
%autosetup -n %{pkgname}-%{version}


%build
# Remove OPTIMIZE=... from noarch packages (unneeded)
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
%make_build


%install

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
# Remove the next line from noarch packages (unneeded)
find %{buildroot} -type f -name '*.bs' -a -size 0 -delete
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
* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.9-1
- Initial spec
