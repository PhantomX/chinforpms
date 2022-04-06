# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global __jar_repack %{nil}

%global pkgyear 2022
%global pkgname IRPF%{pkgyear}

%global jre_ver 11

Name:           irpf%{pkgyear}
Version:        1.0
Release:        1%{?dist}
Summary:        Programa Gerador do IRPF %{pkgyear}, versão Java

License:        Custom
URL:            https://www.gov.br/receitafederal/pt-br/assuntos/meu-imposto-de-renda
Source0:        https://downloadirpf.receita.fazenda.gov.br/irpf/%{pkgyear}/irpf/arquivos/%{pkgname}-%{version}.zip

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  unzip
BuildRequires:  ImageMagick
Requires:       jre-%{jre_ver}
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

exec /usr/lib/jvm/jre-%{jre_ver}/bin/java -jar %{_datadir}/ProgramasRFB/%{name}/irpf.jar "${@}"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/rfb-%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=%{pkgname}
Comment=%{pkgname} - Declaração de Ajuste Anual, Final de Espólio e Saída Definitiva do País
Exec=%{name}
Icon=%{name}
Categories=Office;
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/rfb-%{name}.desktop


mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
ln -s ../../../../ProgramasRFB/%{name}/RFB.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

for res in 16 24 32 48 64 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert RFB.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

rm -f %{buildroot}%{_datadir}/ProgramasRFB/%{name}/IRPF-Licenses.txt


%files
%license IRPF-Licenses.txt
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/ProgramasRFB/%{name}/


%changelog
* Mon Mar 07 2022 - 1.0-1
- Initial spec
