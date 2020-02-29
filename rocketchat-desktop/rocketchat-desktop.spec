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
Version:        2.17.7
Release:        1%{?dist}
Summary:        Rocket.Chat desktop application

License:        MIT
URL:            https://rocket.chat
Source0:        https://github.com/RocketChat/Rocket.Chat.Electron/releases/download/%{version}/%{real_name}-%{version}.%{parch}.rpm
Source1:        https://github.com/RocketChat/Rocket.Chat.Electron/raw/develop/LICENSE

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       libappindicator-gtk3%{?_isa}
Requires:       libglvnd-egl%{?_isa}
Requires:       libglvnd-gles%{?_isa}
Requires:       hicolor-icon-theme
Recommends:     hunspell

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libVkICD_mock_icd.so


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
#!/usr/bin/sh
LD_LIBRARY_PATH="%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{_libdir}/%{name}/%{name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp opt/%{app_name}/{%{name},locales,resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

rm -fv %{buildroot}%{_libdir}/%{name}/libEGL.so*
rm -fv %{buildroot}%{_libdir}/%{name}/libGLESv2.so*

chmod 0755 %{buildroot}%{_libdir}/%{name}/%{name}

rm -rf %{buildroot}%{_libdir}/%{name}/resources/dictionaries
ln -sf ../../../share/myspell %{buildroot}%{_libdir}/%{name}/resources/dictionaries

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
