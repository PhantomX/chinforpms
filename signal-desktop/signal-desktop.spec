%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global use_beta 0

%if 0%{?use_beta}
%global beta beta
%global app_name signal-desktop-beta
%else
%global app_name signal-desktop
%endif

Name:           signal-desktop
Version:        1.31.0
Release:        1%{?beta:.%{beta}}%{?dist}
Summary:        Private messaging from your desktop

License:        MIT
URL:            https://signal.org
# https://updates.signal.org/desktop/apt/dists/xenial/main/binary-amd64/Packages.gz
Source0:        https://updates.signal.org/desktop/apt/pool/main/s/%{app_name}/%{app_name}_%{version}%{?beta:-beta.1}_amd64.deb

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       libappindicator-gtk3%{?_isa}
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
ar p %{S:0} data.tar.xz | tar xJ

mv opt/Signal* opt/%{name}

find opt/%{name}/ -name '*.so*' | xargs chmod +x

find . -type f -name "%{app_name}*" -exec rename "%{app_name}" "%{name}" '{}' ';'

gunzip usr/share/doc/%{name}*/changelog.gz

chrpath --delete opt/%{name}/%{name}

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
cp -rp opt/%{name}/{%{name},locales,resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

rm -fv %{buildroot}%{_libdir}/%{name}/libEGL.so*
rm -fv %{buildroot}%{_libdir}/%{name}/libGLESv2.so*

chmod 0755 %{buildroot}%{_libdir}/%{name}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name}" \
  --set-icon="%{name}" \
  --remove-category=GNOME \
  --remove-category=GTK \
  usr/share/applications/%{name}.desktop

for res in 16 24 32 48 64 128 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/apps/%{name}.png \
    ${dir}/
done


%files
%license opt/%{name}/LICENSE*
%doc usr/share/doc/%{name}*/changelog
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png



%changelog
* Sun Feb 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.31.0-1
- Initial spec
