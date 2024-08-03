# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global __jar_repack %{nil}

%global pkgyear 2021
%global pkgname IRPF%{pkgyear}

Name:           irpf%{pkgyear}
Version:        1.9
Release:        1%{?dist}
Summary:        Programa Gerador do IRPF %{pkgyear}, versão Java

License:        Custom
URL:            https://idg.receita.fazenda.gov.br/interface/cidadao/irpf/%{pkgyear}
Source0:        https://downloadirpf.receita.fazenda.gov.br/irpf/%{pkgyear}/irpf/arquivos/%{pkgname}-%{version}.zip

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  unzip
BuildRequires:  ImageMagick
Requires:       jre-11
Requires:       hicolor-icon-theme
Requires:       xdg-utils


%description
Permite a transmissão de arquivos para a Base de Dados da Receita Federal do
Brasil.


%prep
%autosetup -n %{pkgname}

unzip irpf.jar IRPF-Licenses.txt

unzip lib-modulos/irpf_icones.jar icones/RFB.png
mv icones/RFB.png .

rm -rf exec.{bat,sh} Execute.txt icones

find -type f -exec chmod 0644 '{}' ';'

cat > rfb-%{name}.desktop <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=%{pkgname}
Comment=%{pkgname} - Declaração de Ajuste Anual, Final de Espólio e Saída Definitiva do País
Exec=%{name}
Icon=%{name}
Categories=Office;
EOF


%build
# Nothing to build


%install

mkdir -p %{buildroot}%{_datadir}/ProgramasRFB/%{name}
cp -a * %{buildroot}%{_datadir}/ProgramasRFB/%{name}/

rmdir -p %{buildroot}%{_datadir}/ProgramasRFB/%{name}/* ||:

find %{buildroot}%{_datadir}/ProgramasRFB/%{name} -type d | xargs chmod 0755 2> /dev/null

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh

exec /usr/lib/jvm/jre-11/bin/java -jar %{_datadir}/ProgramasRFB/%{name}/irpf.jar "${@}"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  rfb-%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
ln -s ../../../../ProgramasRFB/%{name}/RFB.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

for res in 16 24 32 48 64 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick RFB.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

rm -f %{buildroot}%{_datadir}/ProgramasRFB/%{name}/IRPF-Licenses.txt


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/rfb-%{name}.desktop


%files
%license IRPF-Licenses.txt
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/ProgramasRFB/%{name}/


%changelog
* Mon Jan 24 2022 - 1.9-1
- 1.9

* Wed Mar 10 2021 - 1.2-1
- 1.2

* Fri Feb 26 2021 - 1.1-1
- 1.1

* Thu Feb 25 2021 - 1.0-1
- Initial spec
