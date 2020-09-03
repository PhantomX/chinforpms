%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global use_beta 0

%if 0%{?use_beta}
%global beta beta
%global app_name signal-desktop-beta
%else
%global app_name signal-desktop
%endif

Name:           signal-desktop
Version:        1.35.1
Release:        1%{?beta:.%{beta}}%{?dist}
Summary:        Private messaging from your desktop

License:        MIT
URL:            https://signal.org
# https://updates.signal.org/desktop/apt/dists/xenial/main/binary-amd64/Packages.gz
Source0:        https://updates.signal.org/desktop/apt/pool/main/s/%{app_name}/%{app_name}_%{version}%{?beta:-beta.1}_amd64.deb

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       cairo%{?_isa}
Requires:       glib2%{?_isa}
Requires:       pango%{?_isa}
Requires:       libdbusmenu%{?_isa}
Requires:       libglvnd-egl%{?_isa}
Requires:       libglvnd-gles%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __provides_exclude_from %__provides_exclude_from|^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libVkICD_mock_icd.so
%global __requires_exclude %__requires_exclude|^libcairo.so.*
%global __requires_exclude %__requires_exclude|^libcairo-gobject.so.*
%global __requires_exclude %__requires_exclude|^libcroco-0.6.so.*
%global __requires_exclude %__requires_exclude|^libexif.so.*
%global __requires_exclude %__requires_exclude|^libexpat.so.*
%global __requires_exclude %__requires_exclude|^libffi.so.*
%global __requires_exclude %__requires_exclude|^libfontconfig.so.*
%global __requires_exclude %__requires_exclude|^libfreetype.so.*
%global __requires_exclude %__requires_exclude|^libfribidi.so.*
%global __requires_exclude %__requires_exclude|^libgdk_pixbuf-2.0.so.*
%global __requires_exclude %__requires_exclude|^libgif.so.*
%global __requires_exclude %__requires_exclude|^libgio-2.0.so.*
%global __requires_exclude %__requires_exclude|^libglib-2.0.so.*
%global __requires_exclude %__requires_exclude|^libgmodule-2.0.so.*
%global __requires_exclude %__requires_exclude|^libgobject-2.0.so.*
%global __requires_exclude %__requires_exclude|^libgsf-1.so.*
%global __requires_exclude %__requires_exclude|^libgthread-2.0.so.*
%global __requires_exclude %__requires_exclude|^libharfbuzz.so.*
%global __requires_exclude %__requires_exclude|^libjpeg.so.*
%global __requires_exclude %__requires_exclude|^liblcms2.so.*
%global __requires_exclude %__requires_exclude|^liborc-0.4.so.*
%global __requires_exclude %__requires_exclude|^libpango-1.0.so.*
%global __requires_exclude %__requires_exclude|^libpangocairo-1.0.so.*
%global __requires_exclude %__requires_exclude|^libpangoft2-1.0.so.*
%global __requires_exclude %__requires_exclude|^libpixman-1.so.*
%global __requires_exclude %__requires_exclude|^libpng16.so.*
%global __requires_exclude %__requires_exclude|^librsvg-2.so.*
%global __requires_exclude %__requires_exclude|^libtiff.so.*
%global __requires_exclude %__requires_exclude|^libvips.so.*
%global __requires_exclude %__requires_exclude|^libvips-cpp.so.*
%global __requires_exclude %__requires_exclude|^libwebp.so.*
%global __requires_exclude %__requires_exclude|^libwebpdemux.so.*
%global __requires_exclude %__requires_exclude|^libwebpmux.so.*
%global __requires_exclude %__requires_exclude|^libxml2.so.*
%global __requires_exclude %__requires_exclude|^libz.so.*


%description
%{summary}.


%prep
%setup -c -T
ar p %{S:0} data.tar.xz | tar xJ

mv opt/Signal* opt/%{name}

find opt/%{name}/ -name '*.so*' | xargs chmod +x

find . -type f -name "%{app_name}*" -exec rename "%{app_name}" "%{name}" '{}' ';'

gunzip usr/share/doc/%{name}*/changelog.gz

chrpath --delete opt/%{name}/%{name}

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
cp -rp opt/%{name}/{%{name},locales,resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

rm -fv %{buildroot}%{_libdir}/%{name}/libEGL.so*
rm -fv %{buildroot}%{_libdir}/%{name}/libGLESv2.so*

rm -rf %{buildroot}%{_libdir}/%{name}/resources/app.asar.unpacked/node_modules/sharp/src
rm -rf %{buildroot}%{_libdir}/%{name}/resources/app.asar.unpacked/node_modules/sharp/vendor/include
rm -rf %{buildroot}%{_libdir}/%{name}/resources/app.asar.unpacked/node_modules/sharp/vendor/lib/{cmake,*.so}

chmod 0755 %{buildroot}%{_libdir}/%{name}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name}" \
  --set-icon="%{name}" \
  --remove-category=GNOME \
  --remove-category=GTK \
  usr/share/applications/%{name}.desktop

for res in 16 24 32 48 64 128 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/apps/%{name}.png \
    ${dir}/
done


%files
%license opt/%{name}/LICENSE*
%doc usr/share/doc/%{name}*/changelog
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png



%changelog
* Thu Sep 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1.35.1-1
- 1.35.1

* Fri Aug 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1.34.5-1
- 1.34.5

* Thu Mar 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.32.2-1
- 1.32.2

* Sun Feb 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.31.0-1
- Initial spec
