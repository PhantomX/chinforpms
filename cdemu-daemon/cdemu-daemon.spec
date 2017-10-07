Name:           cdemu-daemon
Version:        3.1.0
Release:        2%{?dist}
Summary:        CDEmu daemon

License:        GPLv2
URL:            http://sourceforge.net/projects/cdemu
Source:         http://downloads.sourceforge.net/cdemu/%{name}-%{version}.tar.bz2


BuildRequires:  cmake
BuildRequires:  pkgconfig(ao)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libmirage)
BuildRequires:  intltool

Requires:       vhba

%description
CDEmu daemon implements the user-space part of virtual CD/DVD-ROM device
used by CDEmu, a CD/DVD-ROM device emulator for Linux. It receives packet
commands from VHBA kernel module, processes them and passes resulting data
back to the kernel. It also provides D-Bus interface for controlling virtual
devices.

%prep
%autosetup

%build
mkdir build
pushd build

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DSESSION_BUS_SERVICE:BOOL=ON \
  -DSYSTEM_BUS_SERVICE:BOOL=OFF

%make_build

popd

%install
%make_install -C build

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README ChangeLog
%doc %{_mandir}/man8/*
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/dbus-1/services/*

%changelog
* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.1.0-2
- chinforpms release

* Sat Jun 10 2017 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.1.0-1
- Updated to 3.1.0

* Sun Oct  9 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.5-1
- Updated to 3.0.5

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.4-2
- Fixed rpmlint errors and warnings

* Mon Dec 21 2015 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.4-1
- Updated to 3.0.4

* Sat Nov 21 2015 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.3-1
- Updated to 3.0.3

* Sun Sep 28 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.2-1
- Updated to 3.0.2

* Fri Jul 25 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-1
- Updated to 3.0.1

* Sun Jun 29 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.0-1
- Updated to 3.0.0

* Thu Sep 19 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.1-1
- Updated to 2.1.1

* Fri Jun  7 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.0-1
- Updated to 2.1.0

* Mon Dec 24 2012 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.0.0-1
- RPM release for new version
