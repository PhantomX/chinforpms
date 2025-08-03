# Binary packaging only, rust is hateful

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global vc_url  https://github.com/ente-io/ente
%global vc_id  101458e5cded6c40d016e11094b0e9c24f1049ba
%global appname enteauth

Name:           ente-auth
Version:        4.4.3
Release:        1%{?dist}
Summary:        2FA app with free end-to-end encrypted backup and sync

License:        GPL-3.0-only
URL:            https://ente.io/auth
Source0:        %{vc_url}/releases/download/auth-v%{version}/%{name}-v%{version}-%{_arch}.rpm
Source1:        %{vc_url}/raw/%{vc_id}/LICENSE
Source2:        %{vc_url}/raw/%{vc_id}/README.md

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Recommends:     gnome-keyring
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{appname}/lib/.*

%global __requires_exclude ^libapp\\.so.*$
%global __requires_exclude %__requires_exclude|^libdartjni\\.so.*$
%global __requires_exclude %__requires_exclude|^libfile_saver_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libflutter_linux_gtk\\.so.*$
%global __requires_exclude %__requires_exclude|^libflutter_local_authentication_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libflutter_secure_storage_linux_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libgtk_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libscreen_retriever_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libsentry\\.so.*$
%global __requires_exclude %__requires_exclude|^libsodium_libs_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libsodium\\.so.*$
%global __requires_exclude %__requires_exclude|^libsqlite3_flutter_libs_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libtray_manager_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^liburl_launcher_linux_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libwindow_manager_plugin\\.so.*$
%global __requires_exclude %__requires_exclude|^libcurl\\.so.*\\(CURL_OPENSSL_4\\).*$
%global __requires_exclude %__requires_exclude|^libjvm.so.*\\(SUNWprivate_1.1\\).*$


%description
%{name} is an 2FA app with free end-to-end encrypted backup and sync.


%prep
%autosetup -c -T
rpm2cpio %{S:0} | cpio -imdv

cp -p %{S:1} %{S:2} .

cat > %{appname}.wrapper <<'EOF'
#!/usr/bin/bash
APP_NAME=%{appname}
APP_PATH="%{_libdir}/%{appname}"

LD_LIBRARY_PATH="${APP_PATH}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec "${APP_PATH}/${APP_NAME}" "$@"
EOF

chrpath -k -d usr/share/%{appname}/%{appname}
chrpath -k -d usr/share/%{appname}/lib/*.so


%build



%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{appname}.wrapper %{buildroot}%{_bindir}/%{appname}

mkdir -p %{buildroot}%{_libdir}/%{appname}/lib/
install -pm0755 usr/share/%{appname}/%{appname} \
  %{buildroot}%{_libdir}/%{appname}/

install -pm0755 usr/share/%{appname}/lib/*.so \
  %{buildroot}%{_libdir}/%{appname}/lib/

cp -rp usr/share/%{appname}/data %{buildroot}%{_libdir}/%{appname}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  usr/share/applications/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps
install -pm0644 usr/share/pixmaps/%{appname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/

for res in 16 24 32 48 64 96 128 192 256 512;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick usr/share/pixmaps/%{appname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{appname}.png
done


%files
%license LICENSE
%doc README.md
%{_bindir}/%{appname}
%{_libdir}/%{appname}/%{appname}
%{_libdir}/%{appname}/lib/*.so
%{_libdir}/%{appname}/data/
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Fri Aug 01 2025 Phantom X <megaphantomx at hotmail dot com> - 4.4.3-1
- Initial spec
