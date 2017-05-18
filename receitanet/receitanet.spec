%global __jar_repack %{nil}

%global pkgname Receitanet

Name:           receitanet
Version:        1.10
Release:        2%{?dist}
Summary:        Receitanet

License:        Custom
URL:            http://www.receita.fazenda.gov.br
Source0:        http://www.receita.fazenda.gov.br/Publico/programas/%{name}/%{pkgname}-%{version}.jar

BuildArch:      noarch

BuildRequires:  fakeroot
BuildRequires:  ImageMagick
BuildRequires:  java-headless
Requires:       java
Requires:       hicolor-icon-theme

%description
Permite a transmissão de arquivos para a Base de Dados da Receita Federal do
Brasil.


%prep
%autosetup -c -T
echo ${pwd} | fakeroot java -jar %{SOURCE0} -console ||:

%build
# Nothing to build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/ProgramasRFB/%{name}
cp -a imagens lib %{name}.{dat,jar} %{buildroot}%{_datadir}/ProgramasRFB/%{name}/

find %{buildroot}%{_datadir}/ProgramasRFB/%{name} -type d | xargs chmod 0755 2> /dev/null

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/bin/sh

exec java -jar %{_datadir}/ProgramasRFB/%{name}/%{name}.jar "${@}"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/rfb-%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=%{pkgname}
Comment=Executa %{pkgname}
Exec=%{name}
Icon=%{name}
Categories=Office;
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/rfb-%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
convert imagens/Receitanet.xpm \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

convert imagens/Ajuda.xpm \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}_ajuda.png

for res in 16 20 22 24 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert imagens/Receitanet.xpm -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
  convert imagens/Receitanet.xpm -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}_ajuda.png
done

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
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/ProgramasRFB/%{name}

%changelog
* Thu Mar 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.10-2
- Disable jar repack

* Wed Mar 01 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.10-1
- 1.10

* Fri Jan 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.09-2
- Drop menus, only install main desktop file.

* Thu Jan 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.09-1
- Initial spec.
