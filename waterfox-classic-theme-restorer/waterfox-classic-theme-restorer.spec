%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id ClassicThemeRestorer@ArisT2Noia4dev

%global inst_path %{_waterfox_extdir}/%{extension_id}

%global pkgname ClassicThemeRestorer

Name:           waterfox-classic-theme-restorer
Version:        1.7.4
Release:        1%{?dist}
Summary:        Customize Waterfox Australis UI

License:        MPLv2.0
URL:            https://github.com/Aris-t2/ClassicThemeRestorer
Source0:        https://github.com/Aris-t2/ClassicThemeRestorer/archive/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
Source1:        %{name}.metainfo.xml

BuildArch:      noarch

# GNOME Software Center not present on EL < 7 and Fedora
BuildRequires:  libappstream-glib
Requires:       waterfox-filesystem

%description
Classic Theme Restorer brings back appmenu button, squared tabs,
add-ons bar, small nav-bar buttons, a few older buttons and more to
Waterfox Australis UI. Use 'Customize' menu to move buttons on
toolbars.

%prep
%autosetup -n %{pkgname}-%{version}


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
appstream-util validate-relax --nonet %{SOURCE1}
DESTDIR=%{buildroot} appstream-util install %{SOURCE1}

%files
%license license
%doc README.md
%{inst_path}
# GNOME Software Center metadata
%{_datadir}/appdata/%{name}.metainfo.xml


%changelog
* Tue Apr 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.4-1
- Initial spec
