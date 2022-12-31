%global debpatchver 6+deb10u1

Name:           xcftools
Version:        1.0.7
Release:        20%{?dist}
Summary:        Command-line tools for extracting information from XCF files

License:        LicenseRef-Fedora-Public-Domain
URL:            http://henning.makholm.net/software

Source0:        http://henning.makholm.net/%{name}/%{name}-%{version}.tar.gz
Source1:        https://deb.debian.org/debian/pool/main/x/%{name}/%{name}_%{version}-%{debpatchver}.debian.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  pkgconfig(libpng)
BuildRequires:  perl-generators

Requires:       xdg-utils

#patches
Patch0:         fix_sed_replacement_error.patch
Patch1:         xcftools-aarch64.patch

%description
Xcftools is a set of fast command-line tools for extracting information from
the Gimp's native file format XCF. The tools are designed to allow efficient
use of layered XCF files as sources in a build system that use 'make' and
similar tools to manage automatic processing of the graphics.
These tools work independently of the Gimp engine and do not require
the Gimp to even be installed.

%prep
%autosetup -p1 -a 1
sed -e '/remove_strip/d' -i debian/patches/series
for i in $(<debian/patches/series);do
  patch -p1 -F1 -s -i debian/patches/$i
done

# To avoid strip before install (that will generate an empty debuginfo)
sed -i -e '/strip=/d' Makefile.in

%build

%configure
%make_build

cd manpo
# Convert to utf-8
for file in xcf2png.da.1 xcf2pnm.da.1 xcfinfo.da.1 xcfview.da.1 ; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file &&  touch -r $file $file.new &&  mv $file.new $file
done


%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1/
%make_install

%find_lang %{name}


%files -f %{name}.lang
%doc README
%{_bindir}/xcfview
%{_bindir}/xcfinfo
%{_bindir}/xcf2pnm
%{_bindir}/xcf2png
%{_mandir}/man?/xcfview.1.gz
%{_mandir}/man?/xcfinfo.1.gz
%{_mandir}/man?/xcf2pnm.1.gz
%{_mandir}/man?/xcf2png.1.gz
%{_mandir}/da/man?/xcfview.1.gz
%{_mandir}/da/man?/xcfinfo.1.gz
%{_mandir}/da/man?/xcf2pnm.1.gz
%{_mandir}/da/man?/xcf2png.1.gz


%changelog
* Sat Mar 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.7-20
- Apply Debian fixes

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.0.7-9
- Perl 5.18 rebuild

* Mon Apr 08 2013 Jaromir Capik <jcapik@redhat.com> - 1.0.7-8
- aarch64 support (#926753)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 20 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.0.7-5
- Rebuild

* Sat Feb 18 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.0.7-4
- Apply patch to fix bash substitution error. The program_transform_name macro
- becomes s&^&& instead of s,x,x after running rpmbuild's configure. Problem seems
- to be with passing --program-prefix= 
- Enumerate the list of binaries and man pages

* Sun Feb 12 2012 Lakshmi Narasimhan T V <lakshminaras2002@gmail.com> - 1.0.7-3
- Reviving the package. Remove buildroot, and clean.
- Apply patch to fix reference to obsoleted PNG Null macros. 

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 22 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> 1.0.7-1
- Initital build
