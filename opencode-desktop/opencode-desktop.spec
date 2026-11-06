# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch aarch64
%global parch arm64
%else
%global parch %{_arch}
%endif

%global vc_url  https://github.com/anomalyco/opencode
%global vc_id   ee368d2ab04b89f0eeb691a0e69c9a195893aa19

%global binname ai.opencode
%global appname %{binname}.desktop

Name:           opencode-desktop
Version:        2.2.5
Release:        1%{?dist}
Summary:        Open source coding agent

License:        MIT
URL:            https://opencode.ai

Source0:        %{vc_url}/releases/download/v%{version}/%{name}-linux-%{_arch}.rpm#/%{name}-%{version}-%{parch}.rpm
Source1:        %{vc_url}/raw/%{vc_id}/LICENSE
Source2:        %{vc_url}/raw/%{vc_id}/README.md

ExclusiveArch:  x86_64 aarch64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Requires:       hicolor-icon-theme


%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*

%global __requires_exclude ^libffmpeg\\.so.*$
%global __requires_exclude %__requires_exclude|^libvk_swiftshader\\.so.*$


%description
%{Summary}.


%prep
%autosetup -c -T
rpm2cpio %{S:0} | cpio -imdv

cp -p %{S:1} %{S:2} .

cat > %{binname}.wrapper <<'SEOF'
#!/usr/bin/bash
APP_NAME=%{binname}
APP_PATH="%{_libdir}/%{name}"

XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-${HOME}/.config}"
APP_USER_FLAGS_FILE="${XDG_CONFIG_HOME}/%{name}-userflags.conf"
APP_USER_FLAGS=()
if [[ -r "${APP_USER_FLAGS_FILE}" ]]; then
  while read -r param
  do
    APP_USER_FLAGS+=("$(eval "echo ${param}")")
  done < <(LANG=C grep '^-' "${APP_USER_FLAGS_FILE}" | tr -d \'\")
else
  if [ -w "${XDG_CONFIG_HOME}" ] ; then
    cat > "${APP_USER_FLAGS_FILE}" <<'EOF'
# %{name} user flags (One parameter per line, environment variables are evaluated)
#--proxy-server="socks5://proxy:port"
EOF
  fi
fi

LD_LIBRARY_PATH="${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec "${APP_PATH}/${APP_NAME}" "$@"
SEOF

mv opt/OpenCode opt/%{name}

chrpath -k -d opt/%{name}/%{binname}
chrpath -k -d opt/%{name}/*.so


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{binname}.wrapper %{buildroot}%{_bindir}/%{binname}

mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 opt/%{name}/%{binname} \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp opt/%{name}/{%{binname},chrome-sandbox,chrome_crashpad_handler,locales,resources,*.{bin,dat,json,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/
rm -f %{buildroot}%{_libdir}/%{name}/libvulkan.so*

cp -rp opt/%{name}/resources %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key=Exec \
  --set-value="%{binname} %U" \
  usr/share/applications/%{name}.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key=Exec \
  --set-value="%{binname} %U" \
  usr/share/applications/%{appname}.desktop

for res in 32 64 128;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/apps/%{binname}.png \
     ${dir}/%{binname}.png
done

for res in 16 24 48 96;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick usr/share/icons/hicolor/128x128/apps/%{binname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{binname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 usr/share/metainfo/%{appname}.metainfo.xml \
  %{buildroot}%{_metainfodir}/

rm -f %{name}.lang.temp
for langpack in $(ls %{buildroot}%{_libdir}/%{name}/locales/*.pak); do
  language_file=$(basename $langpack)
  language=$(basename $language_file .pak | cut -d '_' -f 1 | sed -e 's/-/_/g')
  case $language in
    ca*|de*|es*|ja*|sr*)
      language=$(echo $language | cut -d '_' -f 1)
      ;;
  esac
  echo "%%lang($language) %{_libdir}/%{name}/locales/$language_file" >> %{name}.lang.temp
done
grep -v -E 'en_US|lang\(en\)' %{name}.lang.temp > %{name}.lang


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files -f %{name}.lang
%license LICENSE opt/%{name}/LICENSE*
%doc README.md
%{_bindir}/%{binname}
%{_libdir}/%{name}/%{binname}
%{_libdir}/%{name}/chrome_crashpad_handler
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.json
%{_libdir}/%{name}/*.pak
%{_libdir}/%{name}/*.so
%attr(4711,root,root) %{_libdir}/%{name}/chrome-sandbox
%dir %{_libdir}/%{name}/locales
%{_libdir}/%{name}/locales/en-US*.pak
%{_libdir}/%{name}/resources
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Thu Nov 05 2026 - 2.2.5-1
- Initial spec
