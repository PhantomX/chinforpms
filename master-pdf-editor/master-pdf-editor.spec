# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global major_ver %%(echo %{version} | cut -d. -f1)

%global binname masterpdfeditor%%{major_ver}

Name:           master-pdf-editor
Version:        4.3.89
Release:        1%{?dist}
Summary:        Master PDF Editor - free edition

License:        Proprietary

URL:            https://code-industry.net
Source0:        http://code-industry.net/public/%{name}-%{version}_qt5.amd64.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Requires:       hicolor-icon-theme


%description
Master PDF Editor is the complete solution for viewing, printing and editing
PDF files.


%prep
%autosetup -n %{name}-%{major_ver}

chrpath --delete %{binname}

cat > %{binname}.wrapper <<'EOF'
#!/usr/bin/sh
exec %{_libdir}/%{name}/%{binname} "${@}"
EOF


%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{binname}.wrapper %{buildroot}%{_bindir}/%{binname}

mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 %{binname} %{buildroot}%{_libdir}/%{name}/
install -pm0644 %{binname}.png %{buildroot}%{_libdir}/%{name}/
cp -rp fonts lang stamps templates %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{binname}" \
  --set-key="Path" \
  --set-value="%{_libdir}/%{name}" \
  --set-icon="%{binname}" \
  %{binname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps

install -pm0644 %{binname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{binname}.png
ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_datadir}/icons/hicolor/128x128/apps")"/%{binname}.png \
  %{buildroot}%{_libdir}/%{name}/%{binname}.png
  
for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick %{binname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{binname}.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license license.txt
%{_bindir}/%{binname}
%{_libdir}/%{name}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/*/%{binname}.png


%changelog
* Mon Jun 02 2025 - 4.3.89-1
- Initial spec

