%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch x86_64
%global parch amd64
%else
%global parch i386
%endif

%global real_name hakuneko

Name:           %{real_name}-desktop
Version:        6.1.7
Release:        2%{?dist}
Summary:        Manga Downloader

License:        Unlicense and MIT
URL:            https://hakuneko.download

Source0:        https://github.com/manga-download/hakuneko/releases/download/v%{version}/%{name}_%{version}_linux_%{parch}.rpm
Source1:        https://github.com/manga-download/hakuneko/raw/master/UNLICENSE

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       libdbusmenu%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*

%global __requires_exclude ^libffmpeg\\.so.*$
%global __requires_exclude %__requires_exclude|^libEGL\\.so.*$
%global __requires_exclude %__requires_exclude|^libGLESv2\\.so.*$
%global __requires_exclude %__requires_exclude|^libVkICD_mock_icd\\.so.*$
%global __requires_exclude %__requires_exclude|^libvulkan\\.so.*$


%description
HakuNeko allows you to download manga images from some selected online
manga reader websites.

%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp %{S:1} .

find usr/lib/%{name}/ -name '*.so*' | xargs chmod +x

chrpath --delete usr/lib/%{name}/%{real_name}

%build

%install
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EORF'
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
  done < <(LANG=C grep -v '^#' "${APP_USER_FLAGS_FILE}" | tr -d \'\")
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
exec "${APP_PATH}/%{real_name}" "${APP_USER_FLAGS}" "$@"
EORF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp usr/lib/%{name}/{%{real_name},kindlegen,locales,resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name}" \
  usr/share/applications/%{name}.desktop

for res in 16 24 32 48 64 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/apps/%{name}.png \
    ${dir}/
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license UNLICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Wed Dec  2 2020 Phantom X <megaphantomx at hotmail dot com> - 6.1.7-2
- Fix gpu acceleration

* Mon Jan 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.1.7-1
- 6.1.7

* Wed Oct 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.8-1
- 5.0.8

* Tue Jul 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.6-1
- 5.0.6 testing

* Sun Aug 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.4.0-2
- New source
- Add missing locales directory

* Sun Aug 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.4.0-1
- 0.4.0

* Wed Mar 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.3.1-1
- 0.3.1

* Sat Mar 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-1
- 0.3.0

* Fri Feb 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.0-1
- 0.2.0

* Fri Nov 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1.0-1
- 0.1.0

* Sat Oct 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.0.32-1
- Fist spec
