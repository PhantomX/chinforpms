%global with_xpi 1

%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id ClassicThemeRestorer@ArisT2Noia4dev

%global inst_path %{_waterfox_extdir}/%{extension_id}

%global pkgname ClassicThemeRestorer

Name:           waterfox-classic-theme-restorer
Version:        1.7.8
Release:        1%{?dist}
Summary:        Customize Waterfox Australis UI

License:        MPLv2.0
URL:            https://github.com/Aris-t2/%{pkgname}
%if 0%{?with_xpi}
Source0:        %{url}/releases/download/%{version}/CTR_v%{version}.xpi#/%{pkgname}-%{version}.xpi
Source1:        %{url}/raw/master/license
Source2:        %{url}/raw/master/README.md
%else
Source0:        %{url}/archive/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
%endif
Source3:        %{name}.metainfo.xml


BuildArch:      noarch

BuildRequires:  libappstream-glib
Requires:       waterfox-filesystem

%description
Classic Theme Restorer brings back appmenu button, squared tabs,
add-ons bar, small nav-bar buttons, a few older buttons and more to
Waterfox Australis UI. Use 'Customize' menu to move buttons on
toolbars.


%prep
%if 0%{?with_xpi}
%autosetup -c %{pkgname}-%{version}
mkdir xpi
mv content defaults locale *.{png,manifest,rdf} xpi/
cp -p %{S:1} .
cp -p %{S:2} .
%else
%autosetup -n %{pkgname}-%{version}
%endif

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
install -Dpm644 %{S:3} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license license
%doc README.md
%{inst_path}
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Sat Oct 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.8-1
- 1.7.8

* Fri Sep 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.7.7-1
- 1.7.7.7

* Fri Jul 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.7.2-1
- 1.7.7.2

* Sun Jul 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.7.1-1
- 1.7.7.1

* Thu Jun 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.7-1
- 1.7.7

* Wed Jun 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.6.1-2
- _metainfodir

* Fri Jun 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.6.1-1
- 1.7.6.1
- with_xpi

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.6-1
- 1.7.6

* Tue Apr 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.4-1
- Initial spec
