%undefine _hardened_build

%global commit d30ea441b92e
%global date 20230309
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}hg%{commit}
%endif

%global pkgname blastem

Name:           %{pkgname}-bindata
Version:        0.6.3
Release:        0.5%{?dist}
Summary:        Blastem binary support files

License:        GPL-3.0-only
URL:            https://www.retrodev.com/%{pkgname}/
Source0:        https://www.retrodev.com/repos/%{pkgname}/archive/%{commit}.tar.bz2#/%{pkgname}-%{commit}.tar.bz2

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  ImageMagick
BuildRequires:  python3-devel
BuildRequires:  python3-pillow
BuildRequires:  vasm
BuildRequires:  xcftools
Requires:       %{pkgname} >= %{version}

%description
BlastEm is an open source, higly accurate emulator for the Genesis/Megadrive
that runs on modest hardware.

This package contains optional binary data files needed for console models with
TMSS support and menus, splitted from main packaged because they need vasm
assembler.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

%py3_shebang_fix img2tiles.py


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
* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.5.20230309hgd30ea441b92e
- BR: ImageMagick

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.4.20220326hg9209858b2f74
- Rebump

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.3.20220326hg9209858b2f74
- New snapshot

* Sun Jan 09 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.2.20220101hg3748a2a8a4b7
- Bump

* Wed Oct 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.1.20210921hg460e14497120
- Initial spec
