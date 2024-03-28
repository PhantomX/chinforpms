# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global snapid H8ZpNgIoPyvmkgxOWw5MSzsXK1wRZiHn
%global snaprev 22

%global app_name Authy

Name:           authy
# Version from application info
Version:        2.4.2
Release:        1%{?dist}
Summary:        Two factor authentication desktop application

License:        Unknown
URL:            https://authy.com/

# curl -q -H 'Snap-Device-Series: 16' https://api.snapcraft.io/v2/snaps/info/authy
Source0:        https://api.snapcraft.io/api/v1/snaps/download/%{snapid}_%{snaprev}.snap#/%{name}-%{version}.snap

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  squashfs-tools
Requires:       libappindicator-gtk3%{?_isa}
Requires:       libdbusmenu%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg\\.so.*$
%global __requires_exclude %__requires_exclude|^libEGL\\.so.*$
%global __requires_exclude %__requires_exclude|^libGLESv2\\.so.*$
%global __requires_exclude %__requires_exclude|^libvk_swiftshader\\.so.*$


%description
The Twilio Authy app generates secure 2 step verification tokens on your device.
It help's you protect your account from hackers and hijackers by adding an
additional layer of security.


%prep
%setup -c -T
unsquashfs -n -d %{name} %{S:0}

RVER="$(strings %{name}/resources/app.asar |grep '"version": "' | tail -n1 | cut -d\" -f 4 )"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch. You have ${RVER} in %{S:0} instead %{version} "
  echo "Edit Version and try again"
  exit 1
fi

find %{name}/ -name '*.so*' | xargs chmod +x

chrpath --delete %{name}/%{name}

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
cp -rp %{name}/{%{name},locales,resources,swiftshader,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

chmod 0755 %{buildroot}%{_libdir}/%{name}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-icon="%{name}" \
  %{name}/meta/gui/%{name}.desktop

for res in 16 24 32 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{name}/meta/gui/icon.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done


%files
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Wed Dec 27 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4.2-1
- 2.4.2

* Mon Sep 11 2023 - 2.4.1-1
- 2.4.1

* Mon Jul 17 2023 - 2.3.0-1
- 2.3.0

* Sat Jan 07 2023 - 2.2.2-1
- 2.2.2

* Wed Nov 02 2022 - 2.2.1-2
- Fix snap revision

* Thu Jul 28 2022 - 2.2.1-1
- 2.2.1

* Wed Nov 24 2021 - 1.9.0-1
- 1.9.0

* Tue Aug 03 2021 - 1.8.4-1
- 1.8.4

* Wed Dec 02 2020 - 1.8.3-2
- Fix gpu acceleration

* Fri Sep 18 2020 - 1.8.3-1
- Initial spec
