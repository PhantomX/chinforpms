%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

%global pkgname UserAgent-Switcher

# needed for this package
%global extension_id \{a6c4a591-f1b2-4f03-b3ff-767e5bedf4e7\}

%global waterfox_min 56.0

# Don't have release urls
%global commit 6a5c4c4783d268a5d997269fcb560d3ff583ee20
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190516

%global gver .%{date}git%{shortcommit}

Name:           waterfox-useragent-switcher
Version:        0.3.0
Release:        1%{?gver}%{?dist}
Summary:        Spoofs and mimics Waterfox User-Agent strings

License:        MPLv2.0
URL:            https://add0n.com/%{name}.html

Source0:        https://github.com/ray-lothian/%{pkgname}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
Source1:        %{name}.metainfo.xml

Patch0:         0001-manifest.json-add-browser_style.patch

BuildArch:      noarch

BuildRequires:  libappstream-glib
BuildRequires:  zip
Requires:       waterfox-filesystem

Provides:       bundled(ua-parser-js) = 0.7.19


%description
User Agent Switcher and Manager spoofs Waterfox User-Agent string. This
string is used by web servers to provide content to you.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

sed \
  -e'/"version"/s|:.*$|: "%{version}",|g' \
  -e'/"strict_min_version"/s|:.*$|: "%{waterfox_min}"|g' \
  -i extension/manifest.json

mv extension/{LICENSE,ReadMe.txt} .

find extension -type f -exec chmod -x '{}' ';'

%build
pushd extension
  zip -9 -r ../%{pkgname}.xpi *
popd

%install
# install into _waterfox_extdir

mkdir -p %{buildroot}%{_waterfox_extdir}
install -pm0644 %{pkgname}.xpi %{buildroot}%{_waterfox_extdir}/%{extension_id}.xpi

# install MetaInfo file for waterfox, etc
install -Dpm644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE
%doc ReadMe.txt
%{_waterfox_extdir}/%{extension_id}.xpi
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Tue Jun 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-1.20190516git6a5c4c4
- 0.3.0

* Fri Mar 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2.8-1.20190314gitaa31d04
- Initial spec
