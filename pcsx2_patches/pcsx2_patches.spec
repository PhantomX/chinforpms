%global commit 8c102fb889d74291c45e092f29336dbaa2654ded
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20260327

BuildArch:      noarch

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           pcsx2_patches
Version:        607
Epoch:          1
Release:        1%{?dist}
Summary:        PCSX2 emulator patches

License:        GPL-3.0-only AND LGPL-3.0-or-later
URL:            https://github.com/PCSX2/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        https://github.com/PCSX2/pcsx2/raw/e3eae7fbe83aad3952e3ed6a8e56fc016b51a9c3/COPYING.GPLv3

Patch10:        0001-Personal-additions.patch

BuildRequires:  zip

Requires:       pcsx2


%description
PCSX2 patch files.


%prep
%autosetup -n %{name}-%{commit} -p1 -N
sed -e 's/\r//' -i patches/*.pnach
%autopatch -p1

cp %{S:1} .

cp -a patches/SLPS-25450_{B4EC196F,4D7B34BA}.pnach
mv patches/SLPS-25842_{E84AA114,2E49AF5A}.pnach


%build
pushd patches
zip -9 -q ../patches.zip *.pnach
popd


%install
mkdir -p %{buildroot}%{_datadir}/PCSX2/resources
install -pm0644 patches.zip %{buildroot}%{_datadir}/PCSX2/resources/


%files
%license COPYING.GPLv3
%{_datadir}/PCSX2/resources/patches.zip


%changelog
* Wed Aug 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1:363-1.20240827git81c1b6a
- Use commit number as version

* Tue Aug 20 2024 Phantom X <megaphantomx at hotmail dot com> - 20240812-2.20240812git9ea7fca
- Add extra patches

* Sat Aug 20 2022 Phantom X <megaphantomx at hotmail dot com> - 20220807-1.20220807git5dde7f4
- Initial spec

