%global _seamonkey_app_id \{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a\}
%global _thunderbird_app_id \{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _moz_extensions %{_datadir}/mozilla/extensions
%global _seamonkey_extdir %{_moz_extensions}/%{_seamonkey_app_id}
%global _thunderbird_extdir %{_moz_extensions}/%{_thunderbird_app_id}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id CSTBB@NArisT2_Noia4dev

%global inst_path %{_datadir}/mozilla/addons

%global pkgname classic_toolbar_buttons
%global ctrver  1.7.7.3

Name:           waterfox-classic-toolbar-buttons
Version:        1.6.1
Release:        1%{?dist}
Summary:        Classic toolbar button style for Waterfox

License:        MPLv2.0
URL:            https://github.com/Aris-t2/ClassicThemeRestorer
Source0:        %{url}/releases/download/%{ctrver}/%{pkgname}-%{version}-fx+sm+tb.xpi
Source1:        %{url}/raw/master/license
Source2:        %{name}.metainfo.xml

BuildArch:      noarch

BuildRequires:  libappstream-glib
Requires:       mozilla-filesystem
Requires:       waterfox-filesystem


%description
Classic toolbar button style for Waterfox, Thunderbird and Seamonkey
toolbars and other tweaks and settings.


%prep
%autosetup -c %{pkgname}-%{version}

cp -p %{S:1} .

%build


%install
install -Dpm644 %{S:0} %{buildroot}%{inst_path}/%{pkgname}-%{version}.xpi

mkdir -p %{buildroot}%{_seamonkey_extdir}
ln -s ../../addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_seamonkey_extdir}/%{extension_id}.xpi

mkdir -p %{buildroot}%{_thunderbird_extdir}
ln -s ../../addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_thunderbird_extdir}/%{extension_id}.xpi

mkdir -p %{buildroot}%{_waterfox_extdir}
ln -s ../../../mozilla/addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_waterfox_extdir}/%{extension_id}.xpi

install -Dpm644 %{S:2} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license license
%{inst_path}/*.xpi
%{_seamonkey_extdir}/%{extension_id}.xpi
%{_thunderbird_extdir}/%{extension_id}.xpi
%{_waterfox_extdir}/%{extension_id}.xpi
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Fri Sep 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.1-1
- Initial spec
