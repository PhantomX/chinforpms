%global _firefox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _moz_extensions %{_datadir}/mozilla/extensions
%global _firefox_extdir %{_moz_extensions}/%{_firefox_app_id}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id keepassxc-browser@keepassxc.org

%global pkgname keepassxc-browser
%global vc_url  https://github.com/keepassxreboot/%{pkgname}

Name:           mozilla-%{pkgname}
Version:        1.5.3
Release:        1%{?dist}
Summary:        KeePassXC Browser Extension 

License:        GPLv3
URL:            https://keepassxc.org/

Source0:        %{vc_url}/releases/download/%{version}/%{pkgname}_%{version}_firefox.zip
Source1:        %{name}.metainfo.xml
Source2:        %{vc_url}/raw/develop/LICENSE
Source3:        %{vc_url}/raw/develop/README.md

BuildArch:      noarch

BuildRequires:  libappstream-glib
BuildRequires:  unzip
BuildRequires:  zip

Requires:       keepassxc >= 2.3.0
Requires:       mozilla-filesystem
Requires:       waterfox-filesystem


%description
Browser extension for KeePassXC with Native Messaging.


%prep
%autosetup -cT %{pkgname}-%{version}

unzip %{S:0} -d xpi
cp -p %{S:2} .
cp -p %{S:3} .

%build
pushd xpi
  zip -9 -r ../%{pkgname}.xpi *
popd

%install
install -Dp -m 644 %{pkgname}.xpi \
  %{buildroot}%{_datadir}/mozilla/addons/%{pkgname}-%{version}.xpi

mkdir -p %{buildroot}%{_firefox_extdir}
ln -s ../../addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_firefox_extdir}/%{extension_id}.xpi

mkdir -p %{buildroot}%{_waterfox_extdir}
ln -s ../../../mozilla/addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_waterfox_extdir}/%{extension_id}.xpi

install -Dpm644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE
%doc README.md
%{_datadir}/mozilla/addons/*.xpi
%{_firefox_extdir}/%{extension_id}.xpi
%{_waterfox_extdir}/%{extension_id}.xpi
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Tue Oct 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.3-1
- Initial spec
