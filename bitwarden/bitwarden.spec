%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global app_name Bitwarden

Name:           bitwarden
Version:        1.16.6
Release:        1%{?dist}
Summary:        A secure and free password manager for all of your devices

License:        GPL-3.0 and MIT
URL:            https://bitwarden.com/

Source0:        https://github.com/%{name}/desktop/releases/download/v%{version}/%{app_name}-%{version}-x86_64.rpm
Source1:        https://github.com/%{name}/desktop/raw/master/LICENSE.txt#/LICENSE

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       libdbusmenu%{?_isa}
Requires:       libglvnd-egl%{?_isa}
Requires:       libglvnd-gles%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libVkICD_mock_icd.so


%description
%{summary}.


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

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name}" \
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
* Thu Oct 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.6-1
- Initial spec
