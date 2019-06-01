Name:           lunzip
Version:        1.11
Release:        1%{?dist}
Summary:        Decompressor for lzip files

License:        GPLv2+
URL:            http://www.nongnu.org/lzip/%{name}.html

Source0:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz.sig

BuildRequires:  gcc


%description
Lunzip is a decompressor for lzip files.


%prep
%autosetup -p1


%build
%configure CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}"
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
* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.11-1
- Initial spec
