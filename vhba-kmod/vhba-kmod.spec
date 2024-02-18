# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels akmod

%global orig_name vhba-module
%global debug_package %{nil}

%define repo chinforpms

Name:           vhba-kmod
Version:        20240202
Release:        1%{?dist}
Summary:        Virtual SCSI host bus adapter driver

License:        GPL-2.0-only
URL:            https://cdemu.sourceforge.io/
Source0:        https://downloads.sourceforge.net/cdemu/%{orig_name}/%{orig_name}-%{version}.tar.xz
Source1:        vhba-kmod-excludekernel-filter.txt

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
BuildRequires:  %{_bindir}/make
%{!?kernels:BuildRequires: buildsys-build-%{repo}-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} --filterfile %{SOURCE1} 2>/dev/null) }

%description
An implementation of a Virtual SCSI Host Bus Adapter (VHBA), which acts
as a low-level SCSI driver that provides a virtual SCSI adapter with one
or more virtual SCSI devices. It is part of cdemu, a CD/DVD-ROM device
emulator for Linux.

This package provides kernel module for kernel %{kversion}.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

for kernel_version in %{?kernel_versions} ; do
  cp -a %{orig_name}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
  make %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
for kernel_version in %{?kernel_versions}; do
  install -D -m 0755 _kmod_build_${kernel_version%%___*}/vhba.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/vhba.ko
done
%{?akmod_install}


%changelog
* Sat Feb 17 2024 Phantom X <megaphantomx at hotmail dot com> - 20240202-1
- 20240202

* Sun Dec 19 2021 Phantom X <megaphantomx at hotmail dot com> - 20211218-1
- 20211218

* Mon Nov 01 2021 Phantom X <megaphantomx at hotmail dot com> - 20211023-1
- 20211023

* Sat May 22 2021 Phantom X <megaphantomx at hotmail dot com> - 20210418-2
- Use chinforpms as repo

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 20210418-1
- 20210418

* Mon Feb 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 20200106-1
- 20200106

* Tue Nov 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190831-2
- M instead SUBDIRS

* Sun Sep 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190831-1
- 20190831

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190410-1
- 20190410

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190302-1
- 20190302

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170610-2
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
- Install udev rule to %%{_udevrulesdir}

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
