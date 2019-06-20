%global _waterfox_extdir %{_datadir}/waterfox/extensions/%{_waterfox_app_id}
%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

# Seamonkey is legacy too
%global _seamonkey_app_id \{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a\}
%global _seamonkey_extdir %{_datadir}/mozilla/extensions/%{_seamonkey_app_id}

%global extension_id uBlock0@raymondhill.net

%global pkgname ublock-origin

Name:           waterfox-%{pkgname}
Version:        1.16.4.11
Release:        1%{?dist}
Summary:        An efficient blocker for Waterfox

License:        GPLv3+ and LGPLv3 and MIT and OFL
URL:            https://github.com/gorhill/uBlock
Source0:        %{url}/releases/download/firefox-legacy-%{version}/uBlock0.firefox-legacy.xpi#/%{pkgname}-%{version}.xpi
Source1:        %{name}.metainfo.xml

BuildArch:      noarch

BuildRequires:  libappstream-glib

Requires:       mozilla-filesystem
Requires:       waterfox-filesystem

# css/fonts/fontawesome-webfont.ttf http://fontawesome.io/ OFL
Provides:       bundled(fontawesome-fonts) = 4.2.0
# lib/punycode.js https://mths.be/punycode MIT
Provides:       bundled(js-punycode) = 1.3.2
# lib/diff https://github.com/Swatinem/diff LGPLv3
Provides:       bundled(js-github-swatinem-diff)
# lib/codemirror http://codemirror.net MIT
Provides:       bundled(js-codemirror) = 5.37.0


%description
An efficient blocker: easy on memory and CPU footprint, and yet can load and
enforce thousands more filters than other popular blockers out there.

Flexible, it's more than an "ad blocker": it can also read and create filters
from hosts files.

This is the legacy release.


%prep
%autosetup -c

%build


%install
install -Dpm644 %{S:0} %{buildroot}%{_datadir}/mozilla/addons/%{pkgname}-%{version}.xpi

# install into _seamonkey_extdir
mkdir -p %{buildroot}%{_seamonkey_extdir}
ln -s ../../addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_seamonkey_extdir}/%{extension_id}.xpi
 
# install into _waterfox_extdir
mkdir -p %{buildroot}%{_waterfox_extdir}
ln -s ../../../mozilla/addons/%{pkgname}-%{version}.xpi \
  %{buildroot}%{_waterfox_extdir}/%{extension_id}.xpi

install -Dpm644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE.txt css/fonts/OFL.txt lib/codemirror/LICENSE
%{_datadir}/mozilla/addons/*.xpi
%{_seamonkey_extdir}/%{extension_id}.xpi
%{_waterfox_extdir}/%{extension_id}.xpi
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Wed Jun 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.4.11-1
- 1.16.4.11

* Tue Apr 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.4.10-1
- 1.16.4.10

* Thu Feb 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.4.8-1
- 1.16.4.8

* Mon Dec 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.16.4.6-1
- 1.16.4.6

* Tue Oct 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.16.4.5-1
- 1.16.4.5

* Fri Jul 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.16.4.4-1
- 1.16.4.4

* Wed Jun 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.16.4.1-1
- Initial spec
