%undefine _hardened_build

%global commit 9209858b2f74
%global date 20220326
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}hg%{commit}
%endif

%global pkgname blastem

Name:           %{pkgname}-bindata
Version:        0.6.3
Release:        0.4%{?gver}%{?dist}
Summary:        Blastem binary support files

License:        GPLv3
URL:            https://www.retrodev.com/%{pkgname}/
Source0:        https://www.retrodev.com/repos/%{pkgname}/archive/%{commit}.tar.bz2#/%{pkgname}-%{commit}.tar.bz2

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  python3-pillow
BuildRequires:  vasm
BuildRequires:  xcftools
BuildRequires:  /usr/bin/pathfix.py
Requires:       %{pkgname} >= %{version}

%description
BlastEm is an open source, higly accurate emulator for the Genesis/Megadrive
that runs on modest hardware.

This package contains optional binary data files needed for console models with
TMSS support and menus, splitted from main packaged because they need vasm
assembler.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" img2tiles.py


%build
%make_build menu.bin tmss.md


%install
mkdir -p %{buildroot}%{_datadir}/%{pkgname}/
install -pm0644 menu.bin tmss.md %{buildroot}%{_datadir}/%{pkgname}/


%files
%license COPYING
%doc README
%{_datadir}/%{pkgname}/menu.bin
%{_datadir}/%{pkgname}/tmss.md


%changelog
* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.4.20220326hg9209858b2f74
- Rebump

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.3.20220326hg9209858b2f74
- New snapshot

* Sun Jan 09 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.2.20220101hg3748a2a8a4b7
- Bump

* Wed Oct 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.1.20210921hg460e14497120
- Initial spec
