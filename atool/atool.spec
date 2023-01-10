Name:           atool
Version:        0.39.0
Release:        100%{?dist}
Summary:        A perl script for managing file archives of various types

License:        GPL-3.0-only
URL:            http://www.nongnu.org/atool/

Source0:        http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.gz

# zstd support by solsTiCe d'Hiver
Patch0:         https://github.com/solsticedhiver/atool/commit/7008abf6f88094062eba205cb54fe6dbc4f556b8.patch#/%{name}-gh-zstd-1.patch
Patch1:         https://github.com/solsticedhiver/atool/compare/d33619f67ea02b6121db443177542e3c3f431d5e...e8b18a2fec4b1274b7e7c6a036e367956344e5c8.diff#/%{name}-gh-zstd-2.patch

BuildArch:      noarch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  perl-generators

%description
atool is a script for managing file archives of various types.

It includes aunpack (to extract archives), apack (to create archives),
als (to list files), acat (to extract files to the standard output),
etc.

atool relies on external programs to handle the archives.
It determines the archive types using file extensions whenever possible,
with a fallback on 'file'.

It includes support for tarballs, gzip, bzip, bzip2, lzop, lzma, pkzip, rar,
ace, arj, rpm, cpio, arc, 7z, alzip, zstd.

%prep
%autosetup -p1

# Convert to UTF-8 while keeping the original timestamp
iconv -f iso8859-1 -t utf-8 NEWS -o tmp
touch -r NEWS tmp
mv -f tmp NEWS
chmod 0644 NEWS

autoreconf -ivf


%build
%configure
%make_build


%install
make install DESTDIR=%{buildroot}

%files
%license COPYING
%doc NEWS README* TODO AUTHORS COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 0.39.0-100
- Fix license
- Add zstd support by solsTiCe d'Hiver

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.39.0-3
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.39.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Elder Marco <eldermarco@fedoraproject.org> - 0.39.0-1
- Update to 0.39.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Pierre Carrier <prc@redhat.com> 0.37.0-1
- Initial packaging
