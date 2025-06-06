%global _build_id_links none
%undefine _debugsource_packages
%global __jar_repack %{nil}

%global pkgrel 1

%global jre_ver 11

Name:           kse
Version:        5.6.0
Release:        1%{?dist}
Summary:        Multipurpose keystore and certificate tool

License:        GPL-3.0-or-later

URL:            https://keystore-explorer.org

Source0:        https://github.com/kaikramer/keystore-explorer/releases/download/v%{version}/%{name}-%{version}-%{pkgrel}.noarch.rpm

ExclusiveArch:  x86_64


BuildRequires:  desktop-file-utils
Requires:       jre >= %{jre_ver}
Requires:       hicolor-icon-theme

Provides:       keystore-explorer = %{?epoch:%{epoch}:}%{version}-%{release}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*


%description
KeyStore Explorer is a user friendly GUI application for creating,
managing and examining keystores, keys, certificates, certificate
requests, certificate revocation lists and more.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv


%build


%install

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh
exec java -jar %{_libdir}/%{name}/%{name}.jar "${@}"
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}/lib
install -pm0644 opt/%{name}/%{name}.jar %{buildroot}%{_libdir}/%{name}/
install -pm0644 opt/%{name}/*.png %{buildroot}%{_libdir}/%{name}/

install -pm0644 opt/%{name}/lib/*.jar %{buildroot}%{_libdir}/%{name}/lib/
install -pm0755 opt/%{name}/lib/*.so %{buildroot}%{_libdir}/%{name}/lib/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name}" \
  --remove-category=Utility \
  opt/%{name}/%{name}.desktop

for res in 16 32 48 128 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 opt/%{name}/icons/%{name}_${res}.png \
    ${dir}/%{name}.png
done


%files
%license opt/kse/licenses/*
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Wed May 28 2025 Phantom X <megaphantomx at hotmail dot com> - 5.6.0-1
- 5.6.0
- Move to %%{_libdir}, because a new shared library is provided

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 5.5.3-1
- 5.5.3

* Fri Feb 24 2023 Phantom X <megaphantomx at hotmail dot com> - 5.5.2-1
- 5.5.2

* Wed Feb 02 2022 Phantom X <megaphantomx at hotmail dot com> - 5.5.1-1
- 5.5.1

* Mon Oct  5 2020 Phantom X <megaphantomx at hotmail dot com> - 5.4.4-1
- 5.4.4

* Sat Apr 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.3-1
- 5.4.3

* Mon Feb 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.2-1
- Initial spec
