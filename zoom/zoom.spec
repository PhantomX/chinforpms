# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global progdir %{_libdir}/%{name}
%global appname us.zoom.Zoom

Name:           zoom
Version:        5.11.3.3882
Release:        1%{?dist}
Summary:        Video Conferencing and Web Conferencing Service

# See LICENSE
License:        Proprietary
URL:            https://www.zoom.us

Source0:        https://zoom.us/client/latest/zoom_x86_64.rpm#/%{name}-%{version}.x86_64.rpm
# https://zoom.us/terms
Source1:        LICENSE

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  chrpath
BuildRequires:  ImageMagick
Requires:       hicolor-icon-theme

Provides:       bundled(libicu) = 56.1
Provides:       bundled(qt) = 5.12.10

%global __provides_exclude_from ^%{progdir}/.*

%global __requires_exclude ^libfaac1.so.*
%global __requires_exclude %__requires_exclude|^libaomagent.so.*
%global __requires_exclude %__requires_exclude|^libcef.so.*
%global __requires_exclude %__requires_exclude|^libclDNN64.so.*
%global __requires_exclude %__requires_exclude|^libfdkaac2.*.so.*
%global __requires_exclude %__requires_exclude|^libicu.*.so.*
%global __requires_exclude %__requires_exclude|^libEGL.so
%global __requires_exclude %__requires_exclude|^libGLESv2.so
%global __requires_exclude %__requires_exclude|^libmkldnn.so
%global __requires_exclude %__requires_exclude|^libmpg123.so
%global __requires_exclude %__requires_exclude|^libOpenCL.so.*
%global __requires_exclude %__requires_exclude|^libQt.*.so.*


%description
Zoom, the cloud meeting company, unifies cloud video conferencing, simple online
meetings, and group messaging into one easy-to-use platform.


%prep
%setup -c -T

RVER="$(rpm -qp --qf %%{version} %{SOURCE0} 2> /dev/null)"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch"
  echo "You have ${RVER} in %{SOURCE0} instead %{version} "
  echo "Edit VERSION variable and try again"
  exit 1
fi

rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp %{S:1} .

mv usr/share/pixmaps/Zoom.png usr/share/pixmaps/%{name}.png
mv usr/share/applications/Zoom.desktop usr/share/applications/%{appname}.desktop

find opt/%{name}/ -name '*.so*' | xargs chmod +x
find opt/%{name}/ -type l -name '*.so' -delete

chmod -x opt/%{name}/timezones/ko/timezones.txt
sed '1 i\#!/usr/bin/sh' -i opt/%{name}/getbssid.sh

rm -f opt/%{name}/zoomlinux
rm -f opt/%{name}/libquazip*
rm -f opt/%{name}/libturbojpeg*

chrpath --delete opt/%{name}/%{name}
chrpath --delete opt/%{name}/zopen
find opt/%{name}/ -type f -name '*.so*' | xargs chrpath -k --delete

sed -e 's|/opt/zoom|%{progdir}|g' opt/%{name}/qt.conf


%build


%install
mkdir -p %{buildroot}%{progdir}
mv opt/%{name}/* %{buildroot}%{progdir}

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{appname} <<'EOF'
#!/usr/bin/sh
APP_PATH=%{progdir}
export APP_PATH
LD_LIBRARY_PATH="%{progdir}/cef:${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec ${APP_PATH}/ZoomLauncher "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{appname}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key="Encoding" \
  --remove-key="Name[en_US]" \
  --remove-category="Application" \
  --set-icon="%{appname}" \
  --set-key="Exec" \
  --set-value="%{appname} %U" \
  usr/share/applications/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/{apps,mimetypes}
install -pm0644 usr/share/pixmaps/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{appname}.png
install -pm0644 usr/share/pixmaps/application-x-*.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/mimetypes/

for res in 16 24 32 48 64 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}
  mkdir -p ${dir}/{apps,mimetypes}
  convert usr/share/pixmaps/%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/apps/%{appname}.png
  convert usr/share/pixmaps/application-x-%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/mimetypes/application-x-%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 ./usr/share/mime/packages/*.xml \
  %{buildroot}%{_datadir}/mime/packages/


%files
%license LICENSE
%{_bindir}/%{appname}
%{progdir}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/icons/hicolor/*x*/mimetypes/*.png
%{_datadir}/mime/packages/*.xml


%changelog
* Fri Aug 19 2022 - 5.11.3.3882-1
- 5.11.3.3882

* Fri Jul 01 2022 - 5.11.1.3595-1
- 5.11.1.3595

* Thu May 26 2022 - 5.10.6.3192-1
- 5.10.6.3192

* Wed Mar 16 2022 - 5.9.6.2225-1
- 5.9.6.2225

* Mon Feb 14 2022 - 5.9.3.1911-1
- 5.9.3.1911

* Fri Jan 14 2022 - 5.9.1.1380-1
- 5.9.1.1380

* Fri Oct 01 2021 - 5.8.0.16-1
- 5.8.0.16

* Thu Aug 26 2021 - 5.7.31792.0820-1
- 5.7.31792.0820

* Thu Aug 05 2021 - 5.7.28991.0726-1
- 5.7.28991.0726

* Thu Jun 17 2021 - 5.6.22045.0607-1
- 5.6.22045.0607

* Tue May 18 2021 - 5.6.16888.0424-1
- 5.6.16888.0424

* Mon Mar 29 2021 - 5.6.13632.0328-1
- 5.6.13632.0328

* Wed Jan 27 2021 - 5.4.57862.0110-1
- 5.4.57862.0110

* Mon Dec 28 2020 - 5.4.57450.1220-1
- 5.4.57450.1220

* Wed Oct 28 2020 - 5.4.53350.1027-1
- 5.4.53350.1027

* Wed Oct 14 2020 - 5.3.472687.1012-1
- 5.3.472687.1012

* Thu Sep 17 2020 - 5.2.458699.0906-1
- 5.2.458699.0906

* Mon Jun 01 2020 - 5.0.413237.0524-1
- Initial spec
