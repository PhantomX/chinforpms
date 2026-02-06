# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global pkgname code
%global pkgdistro el8

%ifarch aarch64
%global parch arm64
%else
%global parch x64
%endif

Name:           visual-studio-code
Version:        1.108.2
Release:        1%{?dist}
Summary:        Code editing. Redefined.

License:        LicenseRef-Microsoft-End-User-License-Agreement
URL:            https://code.visualstudio.com/
Source0:        https://update.code.visualstudio.com/%{version}/linux-rpm-%{parch}/stable#/%{pkgname}-%{version}-%{_arch}.rpm

Patch0:         0001-Move-user-flags-to-main-wrapper.patch

ExclusiveArch:  x86_64 aarch64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Recommends:     gnome-keyring
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*

%global __requires_exclude ^libffmpeg\\.so.*$
%global __requires_exclude %__requires_exclude|^libEGL\\.so.*$
%global __requires_exclude %__requires_exclude|^libGLESv2\\.so.*$
%global __requires_exclude %__requires_exclude|^libvk_swiftshader\\.so.*$


%description
Visual Studio Code is a new choice of tool that combines the simplicity
of a code editor with what developers need for the core edit-build-debug
cycle. See https://code.visualstudio.com/docs/setup/linux for installation instructions and FAQ.


%prep
%setup -c -T

rpm2cpio %{S:0} | cpio -imdv

%{_fixperms} .

%autopatch -p1

cat > %{pkgname}.wrapper <<'SEOF'
#!/usr/bin/bash
APP_NAME=%{pkgname}
APP_PATH="%{_libdir}/%{name}"

LD_LIBRARY_PATH="${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec "${APP_PATH}/bin/${APP_NAME}" "$@"
SEOF

chrpath -k -d usr/share/%{pkgname}/%{pkgname}
chrpath -k -d usr/share/%{pkgname}/*.so

sed -e '/VSCODE_PATH=/s|=".*"|="%{_libdir}/%{name}"|' \
  -i usr/share/%{pkgname}/bin/%{pkgname}


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{pkgname}.wrapper %{buildroot}%{_bindir}/%{pkgname}

mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 usr/share/%{pkgname}/%{pkgname} \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp usr/share/%{pkgname}/{bin,%{pkgname},chrome-sandbox,chrome_crashpad_handler,locales,resources,*.{bin,dat,json,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/
rm -f %{buildroot}%{_libdir}/%{name}/libvulkan.so*

cp -rp usr/share/%{pkgname}/resources %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{bash_completions_dir}
install -pm0644 ./usr/share/bash-completion/completions/%{pkgname} \
  %{buildroot}%{bash_completions_dir}/
  
mkdir -p %{buildroot}%{zsh_completions_dir}
install -pm0644 ./usr/share/zsh/site-functions/_%{pkgname} \
  %{buildroot}%{zsh_completions_dir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key=Exec \
  --set-value="%{pkgname} %F" \
  usr/share/applications/%{pkgname}.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key=Exec \
  --set-value="%{pkgname} --open-url %U" \
  usr/share/applications/%{pkgname}-url-handler.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps
install -pm0644 usr/share/pixmaps/vscode.png \
  %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/

for res in 16 24 32 48 64 96 128 192 256 512;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick usr/share/pixmaps/vscode.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/vscode.png
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 usr/share/mime/packages/%{pkgname}-workspace.xml \
  %{buildroot}%{_datadir}/mime/packages/

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 usr/share/appdata/%{pkgname}.appdata.xml \
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
desktop-file-validate %{buildroot}%{_datadir}/applications/%{pkgname}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{pkgname}-url-handler.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{pkgname}.appdata.xml


%files -f %{name}.lang
%license usr/share/%{pkgname}/LICENSES.chromium.html usr/share/%{pkgname}/resources/app/LICENSE.rtf
%{_bindir}/%{pkgname}
%{_libdir}/%{name}/%{pkgname}
%{_libdir}/%{name}/chrome_crashpad_handler
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.json
%{_libdir}/%{name}/*.pak
%{_libdir}/%{name}/*.so
%attr(4711,root,root) %{_libdir}/%{name}/chrome-sandbox
%{_libdir}/%{name}/bin
%dir %{_libdir}/%{name}/locales
%{_libdir}/%{name}/locales/en-US*.pak
%{_libdir}/%{name}/resources
%{_datadir}/applications/%{pkgname}.desktop
%{_datadir}/applications/%{pkgname}-url-handler.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_metainfodir}/%{pkgname}.appdata.xml
%{_datadir}/mime/packages/%{pkgname}-workspace.xml
%{bash_completions_dir}/%{pkgname}
%{zsh_completions_dir}/_%{pkgname}

%changelog
* Wed Feb 04 2026 - 1.108.2-1
- Initial spec

