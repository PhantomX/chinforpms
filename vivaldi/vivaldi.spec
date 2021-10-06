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

%global pkgrel 1

Name:           vivaldi
Version:        4.2.2406.52
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
Requires:       libnotify%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       font(dejavusans)
Requires:       font(dejavusanscondensed)
Requires:       font(dejavusanslight)
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libEGL.so
%global __requires_exclude %__requires_exclude|^libGLESv2.so
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
APP_PATH=%{_libdir}/%{name}
LD_LIBRARY_PATH="${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec ${APP_PATH}/%{name} --password-store=basic "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp opt/%{name}/{%{name}*,crashpad_handler,locales,MEIPreload,resources,swiftshader,update-*,*.{bin,dat,json,pak,so}} \
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
  --set-key="Exec" \
  --set-value="%{name} %%U" \
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
%attr(4711,root,root) %{_libdir}/%{name}/%{name}-sandbox
%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/MEIPreload
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/swiftshader/*.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/xfce4/helpers/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Sat Oct 02 2021 - 4.2.2406.52-1
- 4.2.2406.52

* Wed Sep 15 2021 - 4.2.2406.44-1
- 4.2.2406.44

* Sun Aug 22 2021 - 4.1.2369.21-1
- 4.1.2369.21

* Sat Aug 07 2021 - 4.1.2369.16-1
- 4.1.2369.16

* Tue Aug 03 2021 - 4.1.2369.11-1
- 4.1.2369.11

* Tue Jul 20 2021 - 4.0.2312.41-1
- 4.0.2312.41

* Tue Jul 06 2021 - 4.0.2312.38-1
- 4.0.2312.38

* Sat Jul 03 2021 - 4.0.2312.36-1
- 4.0.2312.36

* Fri Jun 25 2021 - 4.0.2312.33-1
- 4.0.2312.33

* Sun Jun 13 2021 - 4.0.2312.27-1
- 4.0.2312.27

* Wed Jun 09 2021 - 4.0.2312.24-1
- 4.0.2312.24

* Tue May 18 2021 - 3.8.2259.42-1
- 3.8.2259.42

* Wed May 05 2021 - 3.8.2259.40-1
- 3.8.2259.40

* Thu Apr 22 2021 - 3.7.2218.58-1
- 3.7.2218.58

* Thu Apr 15 2021 - 3.7.2218.55-1
- 3.7.2218.55

* Wed Mar 31 2021 - 3.7.2218.52-1
- 3.7.2218.52

* Wed Mar 24 2021 - 3.7.2218.49-1
- 3.7.2218.49

* Wed Mar 17 2021 - 3.7.2218.45-1
- 3.7.2218.45

* Wed Feb 24 2021 - 3.6.2165.40-1
- 3.6.2165.40

* Mon Feb 08 2021 - 3.6.2165.36-1
- 3.6.2165.36

* Thu Jan 28 2021 - 3.6.2165.34-1
- 3.6.2165.34

* Fri Jan  8 2021 - 3.5.2115.87-1
- 3.5.2115.87

* Sat Dec 12 2020 - 3.5.2115.81-1
- 3.5.2115.81

* Wed Dec 09 2020 - 3.5.2115.73-1
- 3.5.2115.73

* Wed Dec 02 2020 - 3.4.2066.106-2
- Add --password-store=basic parameter to wrapper
- with_snapshot switch to change channels
- Fix gpu acceleration

* Fri Nov 27 2020 - 3.4.2066.106-1
- Initial spec
