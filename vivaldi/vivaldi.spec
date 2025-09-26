# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%bcond snapshot 0
%if %{with snapshot}
%global channel snapshot
%else
%global channel stable
%endif

%global pkgrel 1

%global ffmpegcodec 120726
%global vivaldi_ver %%(echo %{version} | cut -d. -f-2)

Name:           vivaldi
Version:        7.6.3797.56
Release:        1%{?dist}
Summary:        Web browser

License:        LicenseRef-Fedora-Proprietary
URL:            https://vivaldi.com/
Source0:        https://downloads.vivaldi.com/%{channel}/vivaldi-%{channel}-%{version}-%{pkgrel}.%{_arch}.rpm
Source1:        eula.txt

Patch0:         0001-Move-user-flags-to-main-wrapper.patch

ExclusiveArch:  x86_64 aarch64

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
Requires:       vulkan-loader%{?_isa}
Requires:       vivaldi-ffmpeg-codecs = %{vivaldi_ver}.%{ffmpegcodec}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*

%global __requires_exclude ^libffmpeg\\.so.*$
%global __requires_exclude %__requires_exclude|^libEGL\\.so.*$
%global __requires_exclude %__requires_exclude|^libGLESv2\\.so.*$
%global __requires_exclude %__requires_exclude|^libqt.*_shim\\.so.*$
%global __requires_exclude %__requires_exclude|^libQt.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libvk_swiftshader\\.so.*$


%description
Vivaldi web browser.


%prep
%setup -c -T

rpm2cpio %{S:0} | cpio -imdv

FCVER="$(grep ^FFMPEG_VERSION= opt/vivaldi/update-ffmpeg | cut -d= -f2 | cut -d' ' -f1)"
if [ "${FCVER}" != "%{ffmpegcodec}" ] ;then
  echo "Version mismatch. You have ${FCVER} in ffmpegcodec instead %{ffmpegcodec}"
  echo "Edit ffmpegcodec and try again"
  exit 1
fi

%autopatch -p1

cp %{S:1} .

find opt/%{name}/ -name '*.so*' | xargs chmod +x

chrpath --delete opt/%{name}/%{name}-bin

mv usr/share/applications/%{name}{-%{channel},}.desktop
sed -e 's|%{name}-%{channel}|%{name}|g' -i usr/share/applications/%{name}.desktop

cat > %{name}.wrapper <<'EORF'
#!/usr/bin/bash
APP_NAME=%{name}
APP_PATH="%{_libdir}/%{name}"

LD_LIBRARY_PATH="${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec "${APP_PATH}/${APP_NAME}" "$@"
EORF

sed -e '/^FFMPEG_VERSION/aexport VIVALDI_FFMPEG_AUTO=0' -i opt/%{name}/%{name}


%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.wrapper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp opt/%{name}/{%{name}{,-bin,-sandbox},chrome_crashpad_handler,locales,MEIPreload,resources,*.{bin,dat,json,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

mv opt/%{name}/lib/*.so %{buildroot}%{_libdir}/%{name}/
rm -f %{buildroot}%{_libdir}/%{name}/libvulkan.so*

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

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license eula.txt
%{_bindir}/%{name}
%{_libdir}/%{name}/%{name}
%{_libdir}/%{name}/%{name}-bin
%{_libdir}/%{name}/chrome_crashpad_handler
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
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/xfce4/helpers/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Wed Sep 24 2025 - 7.6.3797.56-1
- 7.6.3797.56

* Mon Sep 22 2025 - 7.6.3797.55-1
- 7.6.3797.55

* Thu Sep 18 2025 - 7.6.3797.52-1
- 7.6.3797.52

* Fri Sep 12 2025 - 7.5.3735.74-1
- 7.5.3735.74

* Thu Aug 28 2025 - 7.5.3735.66-1
- 7.5.3735.66

* Thu Aug 21 2025 - 7.5.3735.64-1
- 7.5.3735.64

* Thu Aug 14 2025 - 7.5.3735.62-1
- 7.5.3735.62

* Wed Jul 30 2025 - 7.5.3735.58-1
- 7.5.3735.58

* Wed Jul 23 2025 - 7.5.3735.56-1
- 7.5.3735.56

* Wed Jul 16 2025 - 7.5.3735.54-1
- 7.5.3735.54

* Wed Jul 09 2025 - 7.5.3735.47-1
- 7.5.3735.47

* Thu Jul 03 2025 - 7.5.3735.44-1
- 7.5.3735.41

* Fri Jun 20 2025 - 7.4.3684.55-1
- 7.4.3684.55

* Thu Jun 19 2025 - 7.4.3684.52-1
- 7.4.3684.52

* Thu Jun 19 2025 - 7.4.3684.50-1
- 7.4.3684.50

* Wed Jun 04 2025 - 7.4.3684.46-1
- 7.4.3684.46

* Wed May 28 2025 - 7.4.3684.43-1
- 7.4.3684.43

* Mon May 19 2025 - 7.4.3684.38-1
- 7.4.3684.38

* Thu May 15 2025 - 7.3.3635.14-1
- 7.3.3635.14

* Thu May 08 2025 - 7.3.3635.12-1
- 7.3.3635.12

* Thu Apr 24 2025 - 7.3.3635.11-1
- 7.3.3635.11

* Wed Apr 02 2025 - 7.3.3635.7-1
- 7.3.3635.7

* Fri Mar 28 2025 - 7.3.3635.4-1
- 7.3.3635.4

* Thu Mar 27 2025 - 7.3.3635.2-1
- 7.3.3635.2

* Wed Mar 26 2025 - 7.2.3621.71-1
- 7.2.3621.71

* Wed Mar 19 2025 - 7.2.3621.67-1
- 7.2.3621.67

* Tue Mar 18 2025 - 7.2.3621.63-1
- 7.2.3621.63

* Tue Mar 11 2025 - 7.1.3570.60-1
- 7.1.3570.60

* Thu Feb 27 2025 - 7.1.3570.58-1
- 7.1.3570.58

* Wed Feb 19 2025 - 7.1.3570.54-1
- 7.1.3570.54

* Wed Feb 05 2025 - 7.1.3570.47-1
- 7.1.3570.47

* Thu Jan 30 2025 - 7.1.3570.42-1
- 7.1.3570.42

* Thu Jan 23 2025 - 7.1.3570.39-1
- 7.1.3570.39

* Wed Jan 08 2025 - 7.0.3495.29-1
- 7.0.3495.29

* Fri Dec 27 2024 - 7.0.3495.27-1
- 7.0.3495.27

* Wed Dec 04 2024 - 7.0.3495.23-1
- 7.0.3495.23

* Mon Nov 25 2024 - 7.0.3495.18-1
- 7.0.3495.18

* Mon Nov 18 2024 - 7.0.3495.15-1
- 7.0.3495.15

* Mon Nov 11 2024 - 7.0.3495.11-1
- 7.0.3495.11

* Sun Nov 03 2024 - 7.0.3495.10-1
- 7.0.3495.10

* Thu Oct 24 2024 - 7.0.3495.6-1
- 7.0.3495.6

* Mon Oct 14 2024 - 6.9.3447.54-1
- 6.9.3447.54

* Wed Oct 09 2024 - 6.9.3447.51-1
- 6.9.3447.51

* Wed Sep 25 2024 - 6.9.3447.48-1
- 6.9.3447.48

* Fri Sep 20 2024 - 6.9.3447.46-1
- 6.9.3447.46

* Wed Sep 11 2024 - 6.9.3447.44-1
- 6.9.3447.44

* Thu Sep 05 2024 - 6.9.3447.41-1
- 6.9.3447.41

* Fri Aug 30 2024 - 6.9.3447.37-1
- 6.9.3447.37

* Sat Aug 24 2024 - 6.8.3381.57-1
- 6.8.3381.57

* Wed Aug 21 2024 - 6.8.3381.55-1
- 6.8.3381.55

* Sun Aug 18 2024 - 6.8.3381.53-1
- 6.8.3381.53

* Fri Aug 02 2024 - 6.8.3381.50-1
- 6.8.3381.50

* Fri Jul 19 2024 - 6.8.3381.48-1
- 6.8.3381.48

* Thu Jun 27 2024 - 6.8.3381.46-1
- 6.8.3381.46

* Thu Jun 20 2024 - 6.8.3381.44-1
- 6.8.3381.44

* Fri May 24 2024 - 6.7.3329.35-1
- 6.7.3329.35

* Wed May 15 2024 - 6.7.3329.31-1
- 6.7.3329.31

* Tue May 14 2024 - 6.7.3329.29-1
- 6.7.3329.29

* Sat May 11 2024 - 6.7.3329.27-1
- 6.7.3329.27

* Sun Apr 28 2024 - 6.7.3329.21-1
- 6.7.3329.21

* Fri Apr 26 2024 - 6.7.3329.17-1
- 6.7.3329.17

* Fri Apr 12 2024 - 6.6.3271.61-1
- 6.6.3271.61

* Thu Mar 28 2024 - 6.6.3271.55-1
- 6.6.3271.55

* Mon Mar 04 2024 - 6.6.3271.45-1
- 6.6.3271.45

* Wed Feb 14 2024 - 6.5.3206.63-1
- 6.5.3206.63

* Thu Feb 01 2024 - 6.5.3206.59-1
- 6.5.3206.59

* Wed Jan 17 2024 - 6.5.3206.55-1
- 6.5.3206.55

* Mon Jan 08 2024 - 6.5.3206.50-1
- 6.5.3206.50

* Sun Dec 24 2023 - 6.5.3206.42-1
- 6.5.3206.42

* Fri Dec 01 2023 - 6.4.3160.47-1
- 6.4.3160.47

* Fri Nov 17 2023 - 6.4.3160.44-1
- 6.4.3160.44

* Thu Nov 02 2023 - 6.4.3160.41-1
- 6.4.3160.41

* Thu Oct 26 2023 - 6.4.3160.34-1
- 6.4.3160.34

* Wed Oct 11 2023 - 6.2.3105.58-1
- 6.2.3105.58

* Tue Oct 03 2023 - 6.2.3105.54-1
- 6.2.3105.54

* Mon Sep 25 2023 - 6.2.3105.51-1
- 6.2.3105.51

* Tue Sep 12 2023 - 6.2.3105.48-1
- 6.2.3105.48

* Wed Sep 06 2023 - 6.2.3105.47-1
- 6.2.3105.47

* Fri Sep 01 2023 - 6.2.3105.45-1
- 6.2.3105.45

* Wed Aug 16 2023 - 6.1.3035.302-1
- 6.1.3035.302

* Fri Aug 04 2023 - 6.1.3035.257-1
- 6.1.3035.257

* Wed Jul 26 2023 - 6.1.3035.204-1
- 6.1.3035.204

* Mon Jul 17 2023 - 6.1.3035.111-1
- 6.1.3035.111

* Wed Jun 14 2023 - 6.1.3035.84-1
- 6.1.3035.85

* Tue Jun 06 2023 - 6.0.2979.25-1
- 6.0.2979.25

* Thu May 18 2023 - 6.0.2979.22-1
- 6.0.2979.22

* Thu May 04 2023 - 6.0.2979.18-1
- 6.0.2979.18

* Wed Apr 19 2023 - 6.0.2979.15-1
- 6.0.2979.15

* Mon Apr 17 2023 - 5.7.2921.68-1
- 5.7.2921.68

* Tue Mar 28 2023 - 5.7.2921.65-1
- 5.7.2921.67

* Thu Mar 16 2023 - 5.7.2921.63-1
- 5.7.2921.63

* Thu Feb 23 2023 - 5.7.2921.60-1
- 5.7.2921.60

* Fri Feb 17 2023 - 5.7.2921.53-1
- 5.7.2921.53

* Sat Jan 28 2023 - 5.6.2867.62-1
- 5.6.2867.62

* Wed Jan 11 2023 - 5.6.2867.58-1
- 5.6.2867.58

* Fri Jan 06 2023 - 5.6.2867.50-2
- Fix userflags parsing in wrapper

* Tue Dec 20 2022 - 5.6.2867.50-1
- 5.6.2867.50

* Thu Dec 15 2022 - 5.6.2867.46-1
- 5.6.2867.46

* Fri Dec 09 2022 - 5.6.2867.36-1
- 5.6.2867.36

* Mon Dec 05 2022 - 5.5.2805.50-1
- 5.5.2805.50

* Tue Nov 29 2022 - 5.5.2805.48-1
- 5.5.2805.48

* Mon Nov 14 2022 - 5.5.2805.44-1
- 5.5.2805.44

* Mon Oct 31 2022 - 5.5.2805.42-1
- 5.5.2805.42

* Wed Oct 19 2022 - 5.5.2805.38-1
- 5.5.2805.38

* Mon Oct 10 2022 - 5.5.2805.35-1
- 5.5.2805.35

* Wed Oct 05 2022 - 5.5.2805.32-1
- 5.5.2805.32

* Fri Sep 16 2022 - 5.4.2753.51-1
- 5.4.2753.51

* Thu Sep 08 2022 - 5.4.2753.47-1
- 5.4.2753.47

* Fri Sep 02 2022 - 5.4.2753.45-1
- 5.4.2753.45

* Sat Aug 27 2022 - 5.4.2753.40-1
- 5.4.2753.40

* Wed Aug 17 2022 - 5.4.2753.37-1
- 5.4.2753.37

* Fri Aug 12 2022 - 5.4.2753.31-1
- 5.4.2753.31

* Thu Aug 04 2022 - 5.3.2679.73-1
- 5.3.2679.73

* Thu Jul 21 2022 - 5.3.2679.70-1
- 5.3.2679.70

* Tue Jul 05 2022 - 5.3.2679.68-1
- 5.3.2679.68

* Mon Jun 27 2022 - 5.3.2679.61-1
- 5.3.2679.61

* Thu Jun 16 2022 - 5.3.2679.58-1
- 5.3.2679.58

* Tue Jun 07 2022 - 5.3.2679.38-1
- 5.3.2679.38

* Thu May 26 2022 - 5.2.2623.48-1
- 5.2.2623.48

* Wed May 11 2022 - 5.2.2623.46-1
- 5.2.2623.46

* Fri Apr 29 2022 - 5.2.2623.41-1
- 5.2.2623.41

* Fri Apr 15 2022 - 5.2.2623.39-1
- 5.2.2623.39

* Wed Apr 13 2022 - 5.2.2623.33-1
- 5.2.2623.33

* Fri Apr 08 2022 - 5.2.2623.26-1
- 5.2.2623.26

* Wed Apr 06 2022 - 5.2.2623.24-1
- 5.2.2623.24

* Sat Mar 26 2022 - 5.1.2567.73-1
- 5.1.2567.73

* Wed Mar 16 2022 - 5.1.2567.66-1
- 5.1.2567.66

* Wed Mar 02 2022 - 5.1.2567.57-1
- 5.1.2567.57

* Wed Feb 16 2022 - 5.1.2567.49-1
- 5.1.2567.49

* Wed Feb 09 2022 - 5.1.2567.39-1
- 5.1.2567.39

* Mon Jan 31 2022 - 5.0.2497.51-1
- 5.0.2497.51

* Sat Jan 22 2022 - 5.0.2497.48-1
- 5.0.2497.48

* Fri Jan 07 2022 - 5.0.2497.35-1
- 5.0.2497.35

* Thu Dec 16 2021 - 5.0.2497.32-1
- 5.0.2497.32

* Thu Dec 02 2021 - 5.0.2497.24-1
- 5.0.2497.24

* Tue Nov 09 2021 - 4.3.2439.65-1
- 4.3.2439.65

* Fri Nov 05 2021 - 4.3.2439.63-1
- 4.3.2439.63

* Wed Oct 20 2021 - 4.3.2439.44-1
- 4.3.2439.44

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
