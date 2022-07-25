# Binary packaging only, rust is hateful

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global vc_url  https://github.com/%{name}/%{name}
%global rustdesk_id dc4757fe94006156752040a8fc0b70ccea9fd330

Name:           rustdesk
Version:        1.1.9
Release:        1%{?dist}
Summary:        A remote desktop software

License:        AGPLv3
URL:            https://rustdesk.com/

Source0:        %{vc_url}/releases/download/%{version}/%{name}-%{version}-fedora28-centos8.rpm
Source1:        %{vc_url}/raw/%{rustdesk_id}/LICENCE
Source2:        %{vc_url}/raw/%{rustdesk_id}/README.md

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  systemd
Requires:       hicolor-icon-theme
Requires:       python3-pynput
%{?systemd_requires}

Recommends:     rustdesk-server

%global __provides_exclude_from ^%{_prefix}/lib/%{name}/.*


%description
Yet another remote desktop software, written in Rust. Works out of the box, no
configuration required. You have full control of your data, with no concerns
about security. You can use our rendezvous/relay server, set up your own, or
write your own rendezvous/relay server.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp -p %{S:1} %{S:2} .

sed \
  -e 's|/usr/bin/|%{_bindir}/|g' \
  -e 's|/var/run/|%{_rundir}/|g' \
  -i usr/share/%{name}/files/%{name}.service

sed \
  -e '/new-window/d' \
  -e '/New Window/d' \
  -i usr/share/%{name}/files/%{name}.desktop

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/bin/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_prefix}/lib/%{name}
install -pm0755 usr/lib/%{name}/libsciter-gtk.so \
  %{buildroot}%{_prefix}/lib/%{name}/

mkdir -p %{buildroot}%{_datadir}/%{name}
install -pm0755 usr/share/%{name}/files/pynput_service.py \
  %{buildroot}%{_prefix}/lib/%{name}/

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 usr/share/%{name}/files/%{name}.service \
  %{buildroot}%{_unitdir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-icon="%{name}" \
  --remove-category=Other \
  --add-category=Network \
  usr/share/%{name}/files/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 usr/share/%{name}/files/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

for res in 16 24 32 48 64 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert usr/share/%{name}/files/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done


%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service


%files
%license LICENCE
%doc README.md
%{_bindir}/%{name}
%{_prefix}/lib/%{name}/*.so
%{_prefix}/lib/%{name}/*.py
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_unitdir}/%{name}.service


%changelog
* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.9-1
- Initial spec

