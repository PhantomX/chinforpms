# Binary packaging only, rust is hateful

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global desktop_name com.github.qarmin.%{name}
%global czkawka_id 20c89f44f06f483cb44f32bb5ec2f674a5b8e27f

Name:           czkawka
Version:        3.2.0
Release:        1%{?dist}
Summary:        File cleaning utility

License:        MIT
URL:            https://github.com/qarmin/%{name}

Source0:        %{url}/releases/download/%{version}/linux_czkawka_gui_alternative.AppImage#/%{name}-%{version}.AppImage
Source1:        %{url}/raw/%{czkawka_id}/LICENSE
Source2:        %{url}/raw/%{czkawka_id}/README.md
Source3:        %{url}/raw/%{czkawka_id}/data/%{desktop_name}.metainfo.xml

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       hicolor-icon-theme

Provides:       %{name}-gui = %{?epoch:%{epoch}:}%{version}-%{release}


%description
Czkawka (tch•kav•ka, hiccup) is a simple, fast and free app to remove
unnecessary files from your computer.

%prep
%autosetup -c -T
cp -a %{S:0} .
chmod +x *.AppImage
./%{name}-%{version}.AppImage --appimage-extract

cp -p %{S:1} %{S:2} %{S:3} .


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 squashfs-root/usr/bin/%{name}_gui %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key X-AppImage-Version \
  squashfs-root/%{desktop_name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm0644 squashfs-root/%{desktop_name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 %{desktop_name}.metainfo.xml %{buildroot}%{_metainfodir}/

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_name}.metainfo.xml


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}_gui
%{_datadir}/applications/%{desktop_name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{desktop_name}.svg
%{_metainfodir}/%{desktop_name}.metainfo.xml


%changelog
* Thu Nov 18 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-1
- Initial spec
