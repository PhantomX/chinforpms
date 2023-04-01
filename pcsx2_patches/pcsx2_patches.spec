%global commit b49b724e5efe47601cd8aa6133b53ee1c4c52c77
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230301

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           pcsx2_patches
Version:        %{date}
Release:        1%{?dist}
Summary:        PCSX2 emulator patches

License:        GPL-3.0-only AND LGPL-3.0-or-later
URL:            https://github.com/PCSX2/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        https://github.com/PCSX2/pcsx2/raw/e3eae7fbe83aad3952e3ed6a8e56fc016b51a9c3/COPYING.GPLv3

BuildArch:      noarch

BuildRequires:  zip


%description
PSX2 patch files.


%prep
%autosetup -n %{name}-%{commit} -p1

cp %{S:1} .


%build
for i in cheats_{ni,ws} ;do
  pushd ${i}
  zip -9 -q ../${i}.zip *.pnach
  popd
done


%install
mkdir -p %{buildroot}%{_datadir}/PCSX2/resources
install -pm0644 cheats_{ni,ws}.zip %{buildroot}%{_datadir}/PCSX2/resources/


%files
%license COPYING.GPLv3
%{_datadir}/PCSX2/resources/cheats_ni.zip
%{_datadir}/PCSX2/resources/cheats_ws.zip


%changelog
* Sat Aug 20 2022 Phantom X <megaphantomx at hotmail dot com> - 20220807-1.20220807git5dde7f4
- Initial spec

