%global pkgname bison

Summary:        A GNU general-purpose parser generator
Name:           compat-bison-36
Version:        3.6.4
Release:        1%{?dist}

License:        GPLv3+

Source0:        https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz
Source1:        https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz.sig
# genereted from https://ftp.gnu.org/gnu/gnu-keyring.gpg via:
# curl https://ftp.gnu.org/gnu/gnu-keyring.gpg | gpg2 --import
# gpg2 --export --export-options export-minimal 7DF84374B1EE1F9764BBE25D0DDCAA3278D5264E > gpgkey-7DF84374B1EE1F9764BBE25D0DDCAA3278D5264E.gpg
Source2: gpgkey-7DF84374B1EE1F9764BBE25D0DDCAA3278D5264E.gpg

# testsuite dependency
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  flex
BuildRequires:  gnupg2

URL: http://www.gnu.org/software/%{pkgname}/
BuildRequires:  m4 >= 1.4
#java-1.7.0-openjdk-devel
Requires:       m4 >= 1.4

# bison contains a copy of gnulib.  As a copylib, gnulib was granted
# an exception that allows bundling it with other software.  For
# details, see:
# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Exceptions
Provides:       bundled(gnulib)

%description
Bison is a general purpose parser generator that converts a grammar
description for an LALR(1) context-free grammar into a C program to
parse that grammar. Bison can be used to develop a wide range of
language parsers, from ones used in simple desk calculators to complex
programming languages. Bison is upwardly compatible with Yacc, so any
correctly written Yacc grammar should work with Bison without any
changes. If you know Yacc, you shouldn't have any trouble using
Bison. You do need to be very proficient in C programming to be able
to use Bison. Bison is only needed on systems that are used for
development.

This is a compat package only for compat-gcc-32 build.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{pkgname}-%{version}

%build
%configure \
  --datadir=%{_datadir}/bison36 \
  --program-suffix=36 \
  --disable-yacc \
  --disable-nls
%make_build

%check
#make check
#make maintainer-check

%install
%make_install

# Remove unpackaged files.
rm -f %{buildroot}%{_bindir}/yacc
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_mandir}/man1/yacc*
rm -rf %{buildroot}%{_docdir}

# The distribution contains also source files.  These are used by m4
# when the target parser file is generated.
%files
%doc AUTHORS ChangeLog NEWS README THANKS TODO COPYING
%{_mandir}/*/bison*
%{_datadir}/bison36
%{_bindir}/bison36

%changelog
* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 3.6.4-1
- Initial spec, borrowed from Fedora 33 last release.
