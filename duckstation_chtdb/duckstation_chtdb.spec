%global commit 0140d2e314e83b95115f49c3c0e5896d55d16e3c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250713
BuildArch:      noarch

# Rebuild files
%bcond rebuild 1

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname chtdb

Name:           duckstation_%{pkgname}
Version:        44
Release:        1%{?dist}
Summary:        DuckStation emulator patches

License:        MIT
URL:            https://github.com/duckstation/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

Patch10:        0001-Personal-additions.patch

BuildRequires:  zip
%if %{with rebuild}
BuildRequires:  python3
%endif

Requires:       duckstation-data


%description
DuckStation patch files.


%prep
%autosetup -n %{pkgname}-%{commit} -p1


%build
%if %{with rebuild}
rm -f cheats/*
%{python3} chtdb.py export chtdb.txt cheats
%endif

pushd cheats
zip -9 -q ../cheats.zip *.cht
popd
pushd patches
zip -9 -q ../patches.zip *.cht
popd


%install
mkdir -p %{buildroot}%{_datadir}/duckstation/resources/
install -pm0644 cheats.zip %{buildroot}%{_datadir}/duckstation/resources/
install -pm0644 patches.zip %{buildroot}%{_datadir}/duckstation/resources/


%files
%doc README.md
%license LICENSE
%{_datadir}/duckstation/resources/cheats.zip
%{_datadir}/duckstation/resources/patches.zip


%changelog
* Thu Oct 24 2024 Phantom X <megaphantomx at hotmail dot com> - 7-1.20241021gitdaca782
- Add extra cheats and patches
- Rebuild support (needs python3)

* Mon Oct 21 2024 Phantom X <megaphantomx at hotmail dot com> - 6-1.20241020git57027a2
- Initial spec

