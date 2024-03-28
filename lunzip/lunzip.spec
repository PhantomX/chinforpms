Name:           lunzip
Version:        1.14
Release:        1%{?dist}
Summary:        Decompressor for lzip files

License:        GPL-2.0-or-later
URL:            http://www.nongnu.org/lzip/%{name}.html

Source0:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz.sig

BuildRequires:  gcc
BuildRequires:  make


%description
Lunzip is a decompressor for lzip files.


%prep
%autosetup -p1


%build
%configure CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
%make_build


%install
%make_install


%check
make check


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 1.14-1
- 1.14

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.13-1
- 1.13

* Sun Jan 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1.12-1
- 1.12

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.11-1
- Initial spec
