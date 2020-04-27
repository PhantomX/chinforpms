%global __jar_repack %{nil}

%global pkgrel 1

Name:           kse
Version:        5.4.3
Release:        1%{?dist}
Summary:        Multipurpose keystore and certificate tool

License:        GPLv3+

URL:            https://keystore-explorer.org

Source0:        https://github.com/kaikramer/keystore-explorer/releases/download/v%{version}/%{name}-%{version}.rpm

BuildArch:      noarch


BuildRequires:  desktop-file-utils
Requires:       jre >= 1.8.0
Requires:       hicolor-icon-theme

Provides:       keystore-explorer = %{?epoch:%{epoch}:}%{version}-%{release}


%description
KeyStore Explorer is a user friendly GUI application for creating,
managing and examining keystores, keys, certificates, certificate
requests, certificate revocation lists and more.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames


%build


%install

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/usr/bin/sh
exec java -jar %{_datadir}/%{name}/%{name}.jar "${@}"
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/%{name}/lib
install -pm0644 opt/%{name}/%{name}.jar %{buildroot}%{_datadir}/%{name}/

install -pm0644 opt/%{name}/lib/*.jar %{buildroot}%{_datadir}/%{name}/lib/

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
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Sat Apr 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.3-1
- 5.4.3

* Mon Feb 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.4.2-1
- Initial spec
