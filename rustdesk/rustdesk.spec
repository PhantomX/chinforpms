# Binary packaging only, rust is hateful

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global vc_url  https://github.com/%{name}/%{name}
%global rustdesk_id dc4757fe94006156752040a8fc0b70ccea9fd330

%global pkgrel 0

Name:           rustdesk
Version:        1.3.2
Release:        1%{?dist}
Summary:        A remote desktop software

License:        AGPL-3.0-only
URL:            https://rustdesk.com/

Source0:        %{vc_url}/releases/download/%{version}/%{name}-%{version}-%{pkgrel}.%{_arch}.rpm
Source1:        %{vc_url}/raw/%{rustdesk_id}/LICENCE
Source2:        %{vc_url}/raw/%{rustdesk_id}/README.md

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  systemd
Requires:       hicolor-icon-theme
Requires:       python3-pynput
%{?systemd_requires}

Recommends:     rustdesk-server

%global __provides_exclude_from ^%{_libdir}/%{name}/lib/.*

%global __requires_exclude ^libapp\\.so.*$
%global __requires_exclude %__requires_exclude|^libdesktop_drop_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libdesktop_multi_window_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libfile_selector_linux_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libflutter_custom_cursor_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libflutter_linux_gtk\\.so.*$
%global __requires_exclude %__requires_exclude|^librustdesk\\.so.*$
%global __requires_exclude %__requires_exclude|^libscreen_retriever_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libtexture_rgba_renderer_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^liburl_launcher_linux_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libwindow_manager_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libwindow_size_plugin\\.so.*$


%description
Yet another remote desktop software, written in Rust. Works out of the box, no
configuration required. You have full control of your data, with no concerns
about security. You can use our rendezvous/relay server, set up your own, or
write your own rendezvous/relay server.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp -p %{S:1} %{S:2} .

sed \
  -e 's|/usr/bin/|%{_bindir}/|g' \
  -e 's|/var/run/|%{_rundir}/|g' \
  -i usr/share/%{name}/files/%{name}.service

sed \
  -e '/new-window/d' \
  -e '/New Window/d' \
  -e '/^Exec=/d' \
  -i usr/share/%{name}/files/%{name}.desktop

cat > %{name}.wrapper <<'EORF'
#!/usr/bin/bash
APP_NAME=%{name}
APP_PATH="%{_libdir}/%{name}"

LD_LIBRARY_PATH="${APP_PATH}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec "${APP_PATH}/${APP_NAME}" "$@"
EORF

chrpath -k -d usr/lib/%{name}/%{name}
chrpath -k -d usr/lib/%{name}/lib/*.so


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.wrapper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}/lib/
install -pm0755 usr/lib/%{name}/%{name} \
  %{buildroot}%{_libdir}/%{name}/

install -pm0755 usr/lib/%{name}/lib/*.so \
  %{buildroot}%{_libdir}/%{name}/lib/

cp -rp usr/lib/%{name}/data %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 usr/share/%{name}/files/%{name}.service \
  %{buildroot}%{_unitdir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-icon="%{name}" \
  --set-key="Exec" \
  --set-value="%{name} %u" \
  --add-mime-type="x-scheme-handler/%{name}" \
  usr/share/%{name}/files/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{256x256,scalable}/apps
install -pm0644 usr/share/icons/hicolor/256x256/apps/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
install -pm0644 usr/share/icons/hicolor/scalable/apps/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

for res in 16 24 32 48 64 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick usr/share/icons/hicolor/256x256/apps/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done


%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service


%files
%license LICENCE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/%{name}/%{name}
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/data/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_unitdir}/%{name}.service


%changelog
* Fri Nov 15 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.2-1
- 1.3.2

* Fri Sep 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.0-1
- 1.3.0

* Tue Jan 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.2.3-1
- 1.2.3

* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.9-1
- Initial spec

