%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

%global pkgname openwith

# needed for this package
%global extension_id %{pkgname}@darktrojan.net

%global inst_path %{_waterfox_extdir}/%{extension_id}

Name:           waterfox-%{pkgname}
Version:        6.8.6
Release:        2%{?dist}
Summary:        Quickly test out your web pages in other browsers from Waterfox

License:        MPLv2.0
URL:            https://github.com/darktrojan/%{pkgname}

Source0:        %{url}/archive/VERSION_%{version}/%{pkgname}-%{version}.tar.gz
Source1:        https://www.mozilla.org/media/MPL/2.0/index.815ca599c9df.txt#/LICENSE
Source2:        %{name}.metainfo.xml

Patch0:         %{pkgname}-list-more-browsers.patch

BuildArch:      noarch

BuildRequires:  libappstream-glib
Requires:       waterfox-filesystem


%description
Open With opens the current page in your other browsers from Waterfox with just
two clicks.


%prep
%autosetup -n %{pkgname}-VERSION_%{version} -p1

mkdir xpi
mv components content defaults locale modules skin *.{png,manifest,rdf} xpi/

cp -p %{S:1} .

%build


%install
# install into _waterfox_extdir

mkdir -p %{buildroot}%{inst_path}

pushd xpi
  for f in $(find . -print | sed -e '/\.\/$/d') ; do
    if [ -d ${f} ] ; then
      install -dm 755 %{buildroot}%{inst_path}/${f}
    else
      install -pm 644 ${f} %{buildroot}%{inst_path}/${f}
    fi
  done
popd

# install MetaInfo file for waterfox, etc
install -Dpm644 %{S:2} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE
%doc README.md
%{inst_path}
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Tue Feb 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 6.8.6-2
- Seamonkey desktop file is named mozilla-seamonkey
- Add links, icecat and konqueror on the search list

* Mon Feb 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 6.8.6-1
- Initial spec
