%global orig_name vhba-module
BuildArch:      noarch

Name:           vhba
Version:        20250329
Release:        1%{?dist}
Summary:        Virtual SCSI host bus adapter driver

License:        GPL-2.0-only
URL:            https://cdemu.sourceforge.io/
Source0:        https://downloads.sourceforge.net/cdemu/%{orig_name}/%{orig_name}-%{version}.tar.xz
Source1:        vhba.udev
Source2:        vhba.modules

Provides:       %{name}-kmod-common = %{version}
Requires:       (kmod(vhba.ko) or %{name}-kmod)

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
* Wed Apr 09 2025 Phantom X <megaphantomx at hotmail dot com> - 20250329-1
- 20250329

* Sat Oct 05 2024 Phantom X <megaphantomx at hotmail dot com> - 20240917-1
- 20240917

* Sat Feb 17 2024 Phantom X <megaphantomx at hotmail dot com> - 20240202-1
- 20240202

* Sun Dec 19 2021 Phantom X <megaphantomx at hotmail dot com> - 20211218-1
- 20211218

* Mon Nov 01 2021 Phantom X <megaphantomx at hotmail dot com> - 20211023-1
- 20211023

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 20210418-1
- 20210418

* Mon Feb 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 20200106-1
- 20200106

* Sun Sep 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190831-1
- 20190831

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190410-1
- 20190410

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190302-1
- 20190302

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
- Added systemd build dependency (%%{_udevrulesdir} macro)

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
