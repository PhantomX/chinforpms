%define clawsolaver 0.3
%define coonsbluever 0.4

Name:           claws-mail-themes
Version:        20140629
Release:        2%{?dist}
Summary:        Claws Mail's themes

License:        GPLv3+
URL:            http://www.claws-mail.org/themes.php
Source0:        http://www.claws-mail.org/themes/%{name}-%{version}.tar.gz
Source1:        http://www.claws-mail.org/themes/png/claws-mail-theme_clawsola-%{clawsolaver}.tar.gz
Source2:        http://www.claws-mail.org/themes/png/claws-mail-theme_Coons_Blue.tar.gz

BuildArch:      noarch

Patch1:         claws-mail-theme-clawsola.patch
Patch2:         claws-mail-theme-Coons_Blue.patch

BuildRequires:  autoconf
BuildRequires:  automake
Requires:       claws-mail >= 3.14.1

%description
Claws Mail's themes.

%prep
%autosetup -p1

rm -f clawsola/*.png
rm -f Coons-Blue-*/*.png
mv Coons-Blue-* Coons-Blue-%{coonsbluever}

tar -xvf %{SOURCE1}
tar -xvf %{SOURCE2}

sed \
  -e 's|Coons-Blue-...|Coons-Blue-%{coonsbluever}|g' \
  -i configure.ac Makefile.am Coons-Blue-%{coonsbluever}/Makefile.am

touch AUTHORS ChangeLog NEWS README

autoreconf -ivf

%build
%configure
%make_build


%install
%make_install

%files
%{_datadir}/claws-mail/themes/*

%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 20140629-2
- BR: automake

* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 20140629-1
- First spec.
