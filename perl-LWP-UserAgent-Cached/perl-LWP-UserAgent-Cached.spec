%global pkgname LWP-UserAgent-Cached

Name:           perl-%{pkgname}
Version:        0.08
Release:        1%{?dist}
Summary:        LWP::UserAgent with simple caching mechanism

License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/%{pkgname}

Source0:        https://cpan.metacpan.org/authors/id/O/OL/OLEG/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(LWP::UserAgent)
# Tests
BuildRequires:  perl(Test::More) >= 0.88
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
LWP::UserAgent::Cached is yet another LWP::UserAgent subclass with cache
support. It stores cache in the files on local filesystem and if response
already available in the cache returns it instead of making HTTP request.


%prep
%autosetup -n %{pkgname}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build


%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


%check
make test


%files
%doc README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Sat Dec 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0.08-1
- Initial spec

