%global _seamonkey_app_id \{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a\}
%global _thunderbird_app_id \{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _moz_extensions %{_datadir}/mozilla/extensions
%global _seamonkey_extdir %{_moz_extensions}/%{_seamonkey_app_id}
%global _thunderbird_extdir %{_moz_extensions}/%{_thunderbird_app_id}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id jid1-OoNOA6XBjznvLQ@jetpack

%global with_dev 1

%if 0%{?with_dev}
%global rel dev
%else
%global rel final
%endif

%global pkgname gnotifier

Name:           mozilla-%{pkgname}
Version:        1.13.4
Release:        1%{?dist}
Summary:        Mozilla native notification system integration

License:        GPLv3
URL:            https://github.com/mkiol/GNotifier
Source0:        %{url}/raw/master/xpi/%{pkgname}-%{version}-%{rel}.xpi
Source1:        %{name}.metainfo.xml
Source2:        https://github.com/mkiol/GNotifier/blob/master/LICENSE
Source3:        https://github.com/mkiol/GNotifier/blob/master/README.md

BuildArch:      noarch

# GNOME Software Center not present on EL < 7 and Fedora
BuildRequires:  libappstream-glib
Requires:       libnotify
Requires:       mozilla-filesystem
Requires:       waterfox-filesystem

%description
GNotifier integrates Mozilla's notifications with the native
notification system from Linux desktop.

%prep
%autosetup -c

cp -p %{S:2} .
cp -p %{S:3} .

%build


%install

install -Dp -m 644 %{S:0} \
  %{buildroot}%{_datadir}/mozilla/addons/%{pkgname}-%{version}.xpi

# install classic version into _seamonkey_extdir
mkdir -p %{buildroot}%{_seamonkey_extdir}
ln -s ../../addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_seamonkey_extdir}/%{extension_id}.xpi

# install into _thunderbird_extdir
mkdir -p %{buildroot}%{_thunderbird_extdir}
ln -s ../../addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_thunderbird_extdir}/%{extension_id}.xpi
  
# install into _waterfox_extdir
mkdir -p %{buildroot}%{_waterfox_extdir}
ln -s ../../../mozilla/addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_waterfox_extdir}/%{extension_id}.xpi

install -Dpm644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE
%doc README.md
%{_datadir}/mozilla/addons/*.xpi
%{_seamonkey_extdir}/%{extension_id}.xpi
%{_thunderbird_extdir}/%{extension_id}.xpi
%{_waterfox_extdir}/%{extension_id}.xpi
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Thu Apr 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.13.4-1
- 1.13.4

* Wed Jun 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.13.2-2
- _metainfodir

* Tue Apr 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.4-1
- Initial spec
