%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global snapid H8ZpNgIoPyvmkgxOWw5MSzsXK1wRZiHn
%global snaprev 5

%global app_name Authy

Name:           authy
# Version from application info
Version:        1.8.3
Release:        1%{?dist}
Summary:        Two factor authentication desktop application

License:        Unknown
URL:            https://authy.com/

Source0:        https://api.snapcraft.io/api/v1/snaps/download/%{snapid}_%{snaprev}.snap#/%{name}-%{version}.snap

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  squashfs-tools
Requires:       libappindicator-gtk3%{?_isa}
Requires:       libdbusmenu%{?_isa}
Requires:       libglvnd-egl%{?_isa}
Requires:       libglvnd-gles%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libVkICD_mock_icd.so


%description
The Twilio Authy app generates secure 2 step verification tokens on your device.
It help's you protect your account from hackers and hijackers by adding an
additional layer of security.


%prep
%setup -c -T
unsquashfs -n -d %{name} %{S:0}

find %{name}/ -name '*.so*' | xargs chmod +x

chrpath --delete %{name}/%{name}

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
cp -rp %{name}/{%{name},locales,resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

rm -fv %{buildroot}%{_libdir}/%{name}/libEGL.so*
rm -fv %{buildroot}%{_libdir}/%{name}/libGLESv2.so*

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
* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 1.8.3-1
- Initial spec
