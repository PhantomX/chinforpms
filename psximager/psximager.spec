Name:           psximager
Version:        2.0
Release:        1%{?dist}
Summary:        A collection of tools for dumping PSX images

License:        GPLv2
URL:            https://github.com/cebix/psximager
Source0:        https://github.com/cebix/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libvcdinfo)

%description
PSXImager is a collection of tools for dumping and (pre-)mastering PlayStation 1
("PSX") CD-ROM images.

%prep
%autosetup

if [ ! -r configure ]; then
  autoreconf -ivf
fi


%build
%configure
%make_build


%install
rm -rf %{buildroot}
%make_install


%files
%license COPYING
%doc README
%{_bindir}/*

%changelog
* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-1
- Initial spec
