# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global progdir %{_libdir}/%{name}

Name:           zoom
Version:        5.3.472687.1012
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

%global __provides_exclude_from ^%{progdir}/.*

%global __requires_exclude ^libfaac1.so.*
%global __requires_exclude %__requires_exclude|^libicu.*.so.*
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
mv usr/share/applications/Zoom.desktop usr/share/applications/us.zoom.Zoom.desktop

find opt/%{name}/ -name '*.so*' | xargs chmod +x
find opt/%{name}/ -type l -name '*.so' -delete

chmod -x opt/%{name}/zcacert.pem
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
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh
LD_LIBRARY_PATH="%{progdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{progdir}/ZoomLauncher "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key="Encoding" \
  --remove-key="Name[en_US]" \
  --remove-category="Application" \
  --set-icon="us.zoom.Zoom" \
  --set-key="Exec" \
  --set-value="%{name} %U" \
  usr/share/applications/us.zoom.Zoom.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/{apps,mimetypes}
install -pm0644 usr/share/pixmaps/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/us.zoom.Zoom.png
install -pm0644 usr/share/pixmaps/application-x-*.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/mimetypes/

for res in 16 24 32 48 64 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}
  mkdir -p ${dir}/{apps,mimetypes}
  convert usr/share/pixmaps/%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/apps/us.zoom.Zoom.png
  convert usr/share/pixmaps/application-x-%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/mimetypes/application-x-%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 ./usr/share/mime/packages/*.xml \
  %{buildroot}%{_datadir}/mime/packages/


%files
%license LICENSE
%{_bindir}/%{name}
%{progdir}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/icons/hicolor/*x*/mimetypes/*.png
%{_datadir}/mime/packages/*.xml


%changelog
* Wed Oct 14 2020 Phantom X <megaphantomx at hotmail dot com> - 5.3.472687.1012-1
- 5.3.472687.1012

* Thu Sep 17 2020 Phantom X <megaphantomx at hotmail dot com> - 5.2.458699.0906-1
- 5.2.458699.0906

* Mon Jun 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.0.413237.0524-1
- Initial spec
