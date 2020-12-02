# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global with_snapshot 0
%if 0%{?with_snapshot}
%global channel snapshot
%else
%global channel stable
%endif
%endif

%global pkgrel 1

Name:           vivaldi
Version:        3.4.2066.106
Release:        1%{?dist}
Summary:        Web browser

License:        Proprietary and others, see https://www.vivaldi.com/
URL:            https://vivaldi.com/
Source0:        https://downloads.vivaldi.com/%{channel}/vivaldi-%{channel}-%{version}-%{pkgrel}.x86_64.rpm
Source1:        eula.txt

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       ca-certificates
Requires:       libglvnd-egl%{?_isa}
Requires:       libglvnd-gles%{?_isa}
Requires:       libnotify%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       font(dejavusans)
Requires:       font(dejavusanscondensed)
Requires:       font(dejavusanslight)
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libvk_swiftshader.so


%description
Vivaldi web browser.


%prep
%setup -c -T

rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp %{S:1} .

find opt/%{name}/ -name '*.so*' | xargs chmod +x

chrpath --delete opt/%{name}/%{name}-bin

mv usr/share/applications/%{name}{-%{channel},}.desktop
sed -e 's|%{name}-%{channel}|%{name}|g' -i usr/share/applications/%{name}.desktop


%build

%install
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh
LD_LIBRARY_PATH="%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{_libdir}/%{name}/%{name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp opt/%{name}/{%{name}*,crashpad_handler,locales,MEIPreload,resources,update-*,*.{bin,dat,json,pak}} \
  %{buildroot}%{_libdir}/%{name}/

mv opt/%{name}/lib/*.so %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_libdir}/%{name}/extensions

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 usr/share/appdata/%{name}.appdata.xml \
  %{buildroot}%{_metainfodir}/

mkdir -p %{buildroot}%{_datadir}/xfce4/helpers
install -pm0644 usr/share/xfce4/helpers/%{name}.desktop \
  %{buildroot}%{_datadir}/xfce4/helpers/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  usr/share/applications/%{name}.desktop

for res in 16 22 24 32 48 64 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 opt/%{name}/product_logo_${res}.png \
    ${dir}/%{name}.png
done

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license eula.txt
%{_bindir}/%{name}
%{_libdir}/%{name}/%{name}
%{_libdir}/%{name}/%{name}-bin
%{_libdir}/%{name}/crashpad_handler
%{_libdir}/%{name}/update-*
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.json
%{_libdir}/%{name}/*.pak
%{_libdir}/%{name}/*.so
%attr(4755,root,root) %{_libdir}/%{name}/%{name}-sandbox
%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/MEIPreload
%{_libdir}/%{name}/resources
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/xfce4/helpers/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Fri Nov 27 2020 Phantom X <megaphantomx at hotmail dot com> - 3.4.2066.106-1
- Initial spec
