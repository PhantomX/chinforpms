%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global pkgrel 1

%global vc_url  https://github.com/protonpass/proton-pass-common
%global vc_id a77008491ff59cb247d968327b0cddfe0d1c5f98

Name:           proton-authenticator
Version:        1.0.0
Release:        1%{?dist}
Summary:        Two factor authentication desktop application

License:        GPL-3.0-only
URL:            https://proton.me/authenticator

Source0:        https://proton.me/download/authenticator/linux/ProtonAuthenticator-%{version}-%{pkgrel}.%{_arch}.rpm
Source1:        %{vc_url}/raw/%{vc_id}/LICENSE
Source2:        %{vc_url}/raw/%{vc_id}/README.md

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
Securely sync and backup your 2FA codes easily.


%prep
%autosetup -c -T
rpm2cpio %{S:0} | cpio -imdv

cp -p %{S:1} %{S:2} .

mv "usr/share/applications/Proton Authenticator.desktop" usr/share/applications/%{name}.desktop


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/bin/%{name} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  usr/share/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor
for path in usr/share/icons/hicolor/*/ ;do
  res="$(basename ${path})"
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}/apps
  mkdir -p ${dir}
  install -pm0644 ${path}/apps/* \
    ${dir}/
done

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Fri Aug 01 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-1
- Initial spec

