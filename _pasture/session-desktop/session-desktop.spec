%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global app_name Session

Name:           session-desktop
Version:        1.11.5
Release:        1%{?dist}
Summary:        Onion routing based messenger

License:        GPL-3.0-only
URL:            https://getsession.org/
Source0:        https://github.com/oxen-io/%{name}/releases/download/v%{version}/%{name}-linux-%{_arch}-%{version}.rpm
Source1:        https://github.com/oxen-io/%{name}/raw/v%{version}/LICENSE

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       libappindicator-gtk3%{?_isa}
Requires:       libdbusmenu%{?_isa}
Requires:       libnotify%{?_isa}
Requires:       vulkan-loader%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*

%global __requires_exclude ^libffmpeg\\.so.*$
%global __requires_exclude %__requires_exclude|^libEGL\\.so.*$
%global __requires_exclude %__requires_exclude|^libGLESv2\\.so.*$
%global __requires_exclude %__requires_exclude|^libvk_swiftshader\\.so.*$
%global __requires_exclude %__requires_exclude|^libvulkan\\.so.*$


%description
Session is an end-to-end encrypted messenger that minimises sensitive metadata.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv

cp %{S:1} .

find opt/%{app_name}/ -name '*.so*' | xargs chmod +x

chrpath --delete opt/%{app_name}/%{name}

pushd opt/%{app_name}/resources/app.asar.unpacked/node_modules/@signalapp/better-sqlite3
rm -rf build/{deps,node_gyp_bins}
rm -rf build/Release/*.a
popd

cat > %{name}.wrapper <<'EORF'
#!/usr/bin/bash
APP_NAME=%{name}
APP_PATH="%{_libdir}/%{name}"

XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-${HOME}/.config}"
APP_USER_FLAGS_FILE="${XDG_CONFIG_HOME}/${APP_NAME}-userflags.conf"
APP_USER_FLAGS=()
if [[ -r "${APP_USER_FLAGS_FILE}" ]]; then
  while read -r param
  do
    APP_USER_FLAGS+=("${param}")
  done < <(LANG=C grep '^-' "${APP_USER_FLAGS_FILE}" | tr -d \'\")
else
  if [ -w "${XDG_CONFIG_HOME}" ] ; then
    cat > "${APP_USER_FLAGS_FILE}" <<'EOF'
# %{name} user flags (One parameter per line)
# --proxy-server="socks5://proxy:port"
EOF
  fi
fi

LD_LIBRARY_PATH="${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec "${APP_PATH}/${APP_NAME}" ${APP_USER_FLAGS:+"${APP_USER_FLAGS[@]}"} "$@"
EORF


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.wrapper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp opt/%{app_name}/{%{name},locales,resources,*.{bin,dat,json,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

rm -fv %{buildroot}%{_libdir}/%{name}/libvulkan.so*

# FIXME: Acceleration do not works without these
%dnl rm -fv %{buildroot}%{_libdir}/%{name}/libEGL.so*
%dnl rm -fv %{buildroot}%{_libdir}/%{name}/libGLESv2.so*


chmod 0755 %{buildroot}%{_libdir}/%{name}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name} %%U" \
  usr/share/applications/%{name}.desktop

for res in 16 32 48 64 128 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/apps/%{name}.png \
    ${dir}/
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE opt/Session/LICENSE*
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Wed Dec 27 2023 Phantom X <megaphantomx at hotmail dot com> - 1.11.5-1
- Initial spec

