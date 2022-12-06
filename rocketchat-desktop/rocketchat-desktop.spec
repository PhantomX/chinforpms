%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch x86_64
%global parch x86_64
%else
%global parch i686
%endif

%global real_name rocketchat
%global app_name Rocket.Chat

Name:           %{real_name}-desktop
Version:        3.8.14
Release:        1%{?dist}
Summary:        Rocket.Chat desktop application

License:        MIT
URL:            https://rocket.chat
Source0:        https://github.com/RocketChat/Rocket.Chat.Electron/releases/download/%{version}/%{real_name}-%{version}-linux-%{parch}.rpm
Source1:        https://github.com/RocketChat/Rocket.Chat.Electron/raw/%{version}/LICENSE

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       libappindicator-gtk3%{?_isa}
Requires:       libdbusmenu%{?_isa}
Requires:       vulkan-loader%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude_from ^%{_libdir}/%{name}/resources/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libEGL.so
%global __requires_exclude %__requires_exclude|^libGLESv2.so
%global __requires_exclude %__requires_exclude|^libvk_swiftshader.so
%global __requires_exclude %__requires_exclude|^libvulkan.so


%description
Rocket.Chat Native Cross-Platform Desktop Application via Electron.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp %{S:1} .

find opt/%{app_name}/ -name '*.so*' | xargs chmod +x

chrpath --delete opt/%{app_name}/%{name}

%build


%install
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/bash
APP_NAME=%{name}
APP_PATH="%{_libdir}/%{name}"

XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-${HOME}/.config}"
APP_USER_FLAGS_FILE="${XDG_CONFIG_HOME}/${APP_NAME}-userflags.conf"
APP_USER_FLAGS=""
if [[ -r "${APP_USER_FLAGS_FILE}" ]]; then
  APP_USER_FLAGS="$(grep -v '^#' "${APP_USER_FLAGS_FILE}")"
fi

LD_LIBRARY_PATH="${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec "${APP_PATH}/${APP_NAME}" "${APP_USER_FLAGS}" "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp opt/%{app_name}/{%{name},locales,resources,swiftshader,*.{bin,dat,json,pak,so}} \
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
  --set-value="%{name}" \
  --remove-category=GNOME \
  --remove-category=GTK \
  usr/share/applications/%{name}.desktop

for res in 16 32 48 64 128 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/apps/%{name}.png \
    ${dir}/
done


%files
%license LICENSE opt/%{app_name}/LICENSE*
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png



%changelog
* Mon Dec 05 2022 Phantom X <megaphantomx at hotmail dot com> - 3.8.14-1
- 3.8.14

* Mon Nov 21 2022 Phantom X <megaphantomx at hotmail dot com> - 3.8.13-1
- 3.8.13

* Fri Oct 21 2022 Phantom X <megaphantomx at hotmail dot com> - 3.8.12-1
- 3.8.12

* Wed Oct 05 2022 Phantom X <megaphantomx at hotmail dot com> - 3.8.11-1
- 3.8.11

* Thu Jun 02 2022 Phantom X <megaphantomx at hotmail dot com> - 3.8.7-1
- 3.8.7

* Thu May 19 2022 Phantom X <megaphantomx at hotmail dot com> - 3.8.6-1
- 3.8.6

* Tue May 10 2022 Phantom X <megaphantomx at hotmail dot com> - 3.8.5-1
- 3.8.5

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 3.7.8-1
- 3.7.8

* Wed Feb 16 2022 Phantom X <megaphantomx at hotmail dot com> - 3.7.7-1
- 3.7.7

* Wed Jan 19 2022 Phantom X <megaphantomx at hotmail dot com> - 3.7.6-1
- 3.7.6

* Tue Jan 04 2022 Phantom X <megaphantomx at hotmail dot com> - 3.7.4-1
- 3.7.4

* Fri Dec 03 2021 Phantom X <megaphantomx at hotmail dot com> - 3.7.0-1
- 3.7.0

* Wed Nov 24 2021 Phantom X <megaphantomx at hotmail dot com> - 3.6.0-1
- 3.6.0

* Fri Oct 08 2021 Phantom X <megaphantomx at hotmail dot com> - 3.5.7-1
- 3.5.7

* Fri Sep 24 2021 Phantom X <megaphantomx at hotmail dot com> - 3.5.6-1
- 3.5.6

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 3.5.4-1
- 3.5.4

* Fri Aug 27 2021 Phantom X <megaphantomx at hotmail dot com> - 3.4.0-1
- 3.4.0

* Thu Aug 26 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.4-1
- 3.2.4

* Fri Jul 02 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.3-1
- 3.2.3

* Mon Jun 21 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.2-1
- 3.2.2

* Wed Dec  2 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0.7-2
- Fix gpu acceleration

* Fri Nov 13 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0.7-1
- 3.0.7

* Wed Oct 28 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0.5-1
- 3.0.5

* Tue Oct 20 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0.4-1
- 3.0.4

* Wed Oct 14 2020 Phantom X <megaphantomx at hotmail dot com> - 3.0.3-1
- 3.0.3

* Mon Jul 27 2020 Phantom X <megaphantomx at hotmail dot com> - 2.17.11-1
- 2.17.11

* Tue Jul 14 2020 Phantom X <megaphantomx at hotmail dot com> - 2.17.10-1
- 2.17.10

* Mon Mar 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.17.9-1
- 2.17.9

* Fri Feb 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.17.7-1
- 2.17.7

* Mon Feb 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.17.5-1
- 2.17.5

* Tue Dec 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.17.0-1
- 2.17.0

* Mon Nov 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.16.2-1
- 2.16.2

* Tue Oct 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.16.0-1
- 2.16.0

* Mon Aug 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.15.5-1
- 2.15.5

* Wed Aug 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.5.3-2
- System dictionaries

* Fri Jul 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.5.3-1
- Initial spec
