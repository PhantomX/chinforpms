%global _build_id_links none
%undefine _debugsource_packages

%global rname   dbeaver

%global jre_ver 17

%global vc_url https://github.com/%{rname}/%{rname}/

Name:           %{rname}-ce
Version:        22.0.3
Release:        1%{?dist}
Summary:        Free database tool

License:        ASL 2.0
URL:            https://dbeaver.io

Source0:        %{vc_url}/releases/download/%{version}/%{name}-%{version}-linux.gtk.%{_arch}-nojdk.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  desktop-file-utils
BuildRequires:  unzip
BuildRequires:  ImageMagick
Requires:       ( jre-%{jre_ver} or jre-11 )
Requires:       hicolor-icon-theme


%description
Free multi-platform database tool for developers, SQL programmers, database
administrators and analysts. Supports all popular databases: MySQL, PostgreSQL, MariaDB, SQLite, Oracle, DB2, SQL Server, Sybase, MS Access, Teradata, Firebird, Derby, etc.

%prep
%autosetup -n %{rname}

sed -e 's/\r//' licenses/*.txt

echo '-Ddbeaver.distribution.type=rpm' >> %{rname}.ini
echo '-Duser.language=en' >> %{rname}.ini

cat > %{name}.sh <<'EOF'
#!/usr/bin/bash
APP_NAME=%{rname}
APP_PATH="%{_libdir}/%{name}"

exec "${APP_PATH}/${APP_NAME}" "$@"
EOF


%build


%install
mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 %{rname} %{buildroot}%{_libdir}/%{name}/

install -pm0644 icon.xpm .eclipseproduct \
  %{buildroot}%{_libdir}/%{name}/

cp -rp configuration configuration features p2 plugins \
  %{buildroot}%{_libdir}/%{name}/

ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_licensedir}/%{name}")" \
  %{buildroot}%{_libdir}/%{name}/licenses

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -pm0644 %{rname}.ini %{buildroot}%{_sysconfdir}/%{name}/
ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_sysconfdir}/%{name}")"/%{rname}.ini \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.sh %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Path" \
  --set-value="%{_libdir}/%{name}" \
  --set-key="Exec" \
  --set-value="%{name}" \
  --set-icon="%{name}" \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 %{rname}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_datadir}/icons/hicolor/256x256/apps")"/%{name}.png \
  %{buildroot}%{_libdir}/%{name}/%{rname}.png

for res in 16 24 32 48 64 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{rname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done


%files
%license licenses/*.{txt,html}
%doc readme.txt
%config %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Mon Apr 18 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.3-1
- 22.0.3

* Tue Apr 05 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.2-1
- Initial spec