Name:           psximager
Version:        2.0
Release:        3%{?dist}
Summary:        A collection of tools for dumping PSX images

License:        GPL-2.0-only
URL:            https://github.com/cebix/psximager
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:         %{name}-cdio20.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  boost-devel
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libvcdinfo)

%description
PSXImager is a collection of tools for dumping and (pre-)mastering PlayStation 1
("PSX") CD-ROM images.

%prep
%autosetup -p0

if [ ! -r configure ]; then
  autoreconf -ivf
fi


%build
%configure
%make_build


%install
%make_install


%files
%license COPYING
%doc README
%{_bindir}/*

%changelog
* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.0-3
- libcdio 2.0 fix

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-2
- BR: automake

* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-1
- Initial spec
