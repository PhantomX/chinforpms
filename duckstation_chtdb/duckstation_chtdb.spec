%global commit 57027a2973141356282a42957b2af42164776bf8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20241020
BuildArch:      noarch

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname chtdb

Name:           duckstation_%{pkgname}
Version:        6
Release:        1%{?dist}
Summary:        DuckStation emulator patches

License:        MIT
URL:            https://github.com/duckstation/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

BuildRequires:  zip

Requires:       duckstation-data


%description
PCSX2 patch files.


%prep
%autosetup -n %{pkgname}-%{commit} -p1


%build
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
* Mon Oct 21 2024 Phantom X <megaphantomx at hotmail dot com> - 6-1.20241020git57027a2
- Initial spec

