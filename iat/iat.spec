Name:           iat
Version:        0.1.7
Release:        1%{?dist}
Summary:        Iso9660 Analyzer Tool 

License:        GPL-2.0-or-later
URL:            http://iat.berlios.de/

Source0:        https://downloads.sourceforge.net/%{name}.berlios/%{name}-%{version}.tar.lzma

BuildRequires:  gcc
BuildRequires:  make


%description
Detects and converts DVD/CD images from BIN/MDF/PDI/CDI/NRG/B5I to ISO-9660.


%prep
%autosetup


%build
%configure
%make_build


%install
%make_install

rm -rf %{buildroot}%{_includedir}


%files
%license COPYING
%doc README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Tue Nov 12 2024 Phantom X <megaphantomx at hotmail dot com> - 0.1.7-1
- Initial spec

