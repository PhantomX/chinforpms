%global commit 9ea7fca481e1e4c2263ca69f9a5c9a70c92626dc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240812

BuildArch:      noarch

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           pcsx2_patches
Version:        %{date}
Release:        2%{?dist}
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
%autosetup -n %{name}-%{commit} -p1

cp %{S:1} .


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
* Tue Aug 20 2024 Phantom X <megaphantomx at hotmail dot com> - 20240812-2.20240812git9ea7fca
- Add extra patches

* Sat Aug 20 2022 Phantom X <megaphantomx at hotmail dot com> - 20220807-1.20220807git5dde7f4
- Initial spec

