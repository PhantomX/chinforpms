Name:           plzip
Version:        1.10
Release:        1%{?dist}
Summary:        Multi-threaded compressor using the lzip file format

License:        GPLv2+
URL:            http://www.nongnu.org/lzip/%{name}.html

Source0:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/%{name}/%{name}-%{version}.tar.gz.sig

BuildRequires:  gcc-c++
BuildRequires:  lzlib-devel
BuildRequires:  make


%description
Plzip is a massively parallel (multi-threaded) implementation of lzip.


%prep
%autosetup -p1


%build
%set_build_flags
%configure CXXFLAGS="${CXXFLAGS}" LDFLAGS="${LDFLAGS}"
%make_build


%install
%make_install

rm -f %{buildroot}%{_infodir}/dir


%check
make check


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_infodir}/%{name}.info*
%{_mandir}/man1/%{name}.1*


%changelog
* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.10-1
- 1.10

* Sun Jan 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1.9-1
- 1.9

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.8-1
- Initial spec
