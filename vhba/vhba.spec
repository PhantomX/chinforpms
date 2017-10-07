%global orig_name vhba-module
%global debug_package %{nil}

Name:           vhba
Version:        20170610
Release:        100%{?dist}
Summary:        Virtual SCSI host bus adapter driver

License:        GPLv2
URL:            http://sourceforge.net/projects/cdemu
Source0:        http://downloads.sourceforge.net/cdemu/%{orig_name}/%{orig_name}-%{version}.tar.bz2
Source1:        vhba.udev
Source2:        vhba.modules

Provides:       %{name}-kmod-common = %{version}
Requires:       %{name}-kmod >= %{version}

BuildRequires:  systemd

%description
An implementation of a Virtual SCSI Host Bus Adapter (VHBA), which acts
as a low-level SCSI driver that provides a virtual SCSI adapter with one
or more virtual SCSI devices. It is part of cdemu, a CD/DVD-ROM device
emulator for linux.

%prep
%autosetup -n %{orig_name}-%{version}

%build
# Nothing to do here...

%install

# systemd module autoinsert rule
install -m644 -D %{SOURCE2} %{buildroot}%{_prefix}/lib/modules-load.d/%{name}.conf

# udev rule
install -m644 -D %{SOURCE1} %{buildroot}/%{_udevrulesdir}/69-%{name}.rules

%files
%license COPYING
%doc README AUTHORS ChangeLog
%{_prefix}/lib/modules-load.d/%{name}.conf
%{_udevrulesdir}/69-%{name}.rules

%changelog
* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170610-100
- chinforpms release

* Sat Jun 10 2017 Rok Mandeljc <rok.mandeljc@gmail.com> - 20170610-1
- Updated to 20170610

* Sun Oct  9 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 20161009-1
- Updated to 20161009

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 20140928-6
- This time really renamed the udev rule

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 20140928-5
- Use uaccess tag in udev rule instead of mode and group
- Renamed the udev rule file so it runs before 70-uaccess.rules

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 20140928-4
- Added systemd build dependency (%{_udevrulesdir} macro)

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 20140928-3
- Fixed rpmlint warnings and errors
- Install udev rule to %{_udevrulesdir}

* Thu Apr 21 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 20140928-2
- Removed broken NAME="%k" from udev rule

* Sun Sep 28 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 20140928-1
- Updated to 20140928

* Sun Jun 29 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 20140629-1
- Updated to 20140629

* Mon Oct  7 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 20130607-1
- Updated to 20130607

* Sun Apr 22 2012 Rok Mandeljc <rok.mandeljc@gmail.com> - 20120422-1
- RPM release for new version
