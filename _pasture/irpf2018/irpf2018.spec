# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global __jar_repack %{nil}

%global pkgyear 2018
%global pkgname IRPF%{pkgyear}

Name:           irpf%{pkgyear}
Version:        1.6
Release:        2%{?dist}
Summary:        Programa Gerador do IRPF %{pkgyear}, versão Java

License:        Custom
URL:            http://idg.receita.fazenda.gov.br/interface/cidadao/irpf/%{pkgyear}
Source0:        http://downloadirpf.receita.fazenda.gov.br/irpf/%{pkgyear}/irpf/arquivos/%{pkgname}-%{version}.zip

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  unzip
BuildRequires:  ImageMagick
Requires:       jre-1.8.0
Requires:       hicolor-icon-theme
Requires:       xdg-utils

%description
Permite a transmissão de arquivos para a Base de Dados da Receita Federal do
Brasil.


%prep
%autosetup -n %{pkgname}

unzip irpf.jar icones/RFB.png IRPF-Licenses.txt
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

exec /usr/lib/jvm/jre-1.8.0/bin/java -jar %{_datadir}/ProgramasRFB/%{name}/irpf.jar "${@}"
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

for res in 16 22 24 32 36 48 64 72 96 128 192 256 ;do
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
* Fri Oct 02 2020 - 1.6-2
- Update wrapper

* Thu Feb 28 2019 - 1.6-1
- 1.6

* Tue Apr 17 2018 - 1.4-1
- 1.4

* Tue Feb 27 2018 - 1.0-1
- Initial spec
