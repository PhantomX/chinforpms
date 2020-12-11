%global _seamonkey_app_id \{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a\}
%global _thunderbird_app_id \{3550f703-e582-4d05-9a08-453d09bdfdc6\}
%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _moz_extensions %{_datadir}/mozilla/extensions
%global _seamonkey_extdir %{_moz_extensions}/%{_seamonkey_app_id}
%global _thunderbird_extdir %{_moz_extensions}/%{_thunderbird_app_id}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id \{9533f794-00b4-4354-aa15-c2bbda6989f8\}

%global pkgname FireTray

%global commit 890dc57fd508417c6c1c5a38be68332421035c07
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190115
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           mozilla-firetray
Version:        0.6.5
Release:        1%{?gver}%{?dist}
Summary:        A system tray addon for mozilla

License:        GPLv3+
URL:            https://github.com/Ximi1970/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        %{name}.metainfo.xml

Patch0:         0001-Waterfox-minimal-version.patch

BuildArch:      noarch

BuildRequires:  libappstream-glib
Requires:       mozilla-filesystem
Requires:       waterfox-filesystem
Requires:       gdk-pixbuf2 >= 2.24.1
Requires:       gtk3

%global inst_path %{_datadir}/mozilla/addons/%{pkgname}-%{version}


%description
Firetray is a system tray addon for mozilla.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

sed -e 's|$(shell git rev-parse --short HEAD)|%{version}-%{release}|g' \
  -i src/Makefile


%build
pushd src
  %make_build -j 1 build
popd


%install
mkdir -p %{buildroot}%{inst_path}

pushd build-%{version}-%{release}
  rm -f *.xpi
  for f in $(find . -print | sed -e '/\.\/$/d') ; do
    if [ -d ${f} ] ; then
      install -dm 755 %{buildroot}%{inst_path}/${f}
    else
      install -pm 644 ${f} %{buildroot}%{inst_path}/${f}
    fi
  done
popd

for extdir in %{_seamonkey_extdir} %{_thunderbird_extdir} ;do
  mkdir -p %{buildroot}${extdir}
  ln -s ../../addons/%{pkgname}-%{version} \
    %{buildroot}${extdir}/%{extension_id}
done

mkdir -p %{buildroot}%{_waterfox_extdir}
ln -s ../../../mozilla/addons/%{pkgname}-%{version} \
    %{buildroot}%{_waterfox_extdir}/%{extension_id}

install -Dpm644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license LICENSE
%doc Changelog README.md
%{inst_path}
%{_seamonkey_extdir}/%{extension_id}
%{_thunderbird_extdir}/%{extension_id}
%{_waterfox_extdir}/%{extension_id}
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Tue Jun  4 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.6.5-1
- Initial spec
