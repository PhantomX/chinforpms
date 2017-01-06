%global pkgname IRPF2016

Name:           irpf2016
Version:        1.3
Release:        1%{?dist}
Summary:        Programa Gerador do IRPF 2016, versão Java

License:        Custom
URL:            http://idg.receita.fazenda.gov.br/interface/cidadao/irpf/2016
Source0:        http://downloadirpf.receita.fazenda.gov.br/irpf/2016/%{pkgname}-%{version}.zip
Source1:        %{name}.menu

BuildArch:      noarch

BuildRequires:  unzip
BuildRequires:  ImageMagick
BuildRequires:  java-headless
Requires:       java
Requires:       receitanet
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

%build
# Nothing to build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/ProgramasRFB/%{name}
cp -a * %{buildroot}%{_datadir}/ProgramasRFB/%{name}/

rmdir -p %{buildroot}%{_datadir}/ProgramasRFB/%{name}/* ||:

find %{buildroot}%{_datadir}/ProgramasRFB/%{name} -type d | xargs chmod 0755 2> /dev/null

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/bin/sh

exec java -jar %{_datadir}/ProgramasRFB/%{name}/irpf.jar "${@}"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/rfb-%{name}_program.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=%{pkgname}
Comment=%{pkgname} - Declaração de Ajuste Anual, Final de Espólio e Saída Definitiva do País
Exec=%{name}
Icon=%{name}
Categories=Office;X-rfb;X-%{name};
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/rfb-%{name}_program.desktop

cat > %{buildroot}%{_datadir}/applications/rfb-%{name}_help.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Ajuda do %{pkgname}
Exec=%{name} -h
Icon=%{name}
Categories=Office;X-rfb;X-%{name};
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/rfb-%{name}_help.desktop

cat > %{buildroot}%{_datadir}/applications/rfb-%{name}_leiame.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Leia-me do %{pkgname}
Exec=xdg-open %{_datadir}/ProgramasRFB/%{name}/Leia_me.htm
Icon=%{name}
Categories=Office;X-rfb;X-%{name};
EOF

mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -pm0644 %{SOURCE1} \
  %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/rfb-%{name}.menu

mkdir -p %{buildroot}%{_datadir}/desktop-directories
cat > %{buildroot}%{_datadir}/desktop-directories/rfb-%{name}.directory <<EOF
[Desktop Entry]
Version=1.0
Type=Directory
Name=Programas RFB2016
Icon=%{name}
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
ln -s ../../../../ProgramasRFB/%{name}/RFB.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

for res in 16 20 22 24 32 36 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert RFB.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

rm -f %{buildroot}%{_datadir}/ProgramasRFB/%{name}/IRPF-Licenses.txt

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license IRPF-Licenses.txt
#doc add-docs-here
%{_sysconfdir}/xdg/menus/applications-merged/rfb-%{name}.menu
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/desktop-directories/rfb-%{name}.directory
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/ProgramasRFB/%{name}

%changelog
* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1
- Initial spec.
