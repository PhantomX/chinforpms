%global pname FreeFileSync

Name:           freefilesync
Version:        8.10
Release:        1%{?dist}
Summary:        A file synchronization utility

License:        GPLv3
URL:            http://www.freefilesync.org/
Source0:        http://www.freefilesync.org/download/%{pname}_%{version}_Source.zip
Source1:        https://aur.archlinux.org/cgit/aur.git/plain/ffsicon.png?h=%{name}#/%{pname}.png
Source2:        https://aur.archlinux.org/cgit/aur.git/plain/rtsicon.png?h=%{name}#/RealTimeSync.png

BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  boost-devel
BuildRequires:  compat-wxGTK3-gtk2-devel
Requires:       hicolor-icon-theme
Requires(post): desktop-file-utils
Requires(postun): gtk-update-icon-cache
Requires(posttrans): gtk-update-icon-cache

%description
FreeFileSync is a free Open Source software that helps you synchronize
files and synchronize folders for Windows, Linux and macOS. It is
designed to save your time setting up and running backup jobs while
having nice visual feedback along the way.

%prep
%autosetup -p0 -c -n %{pname}-%{version}

find -type d 

cp %{SOURCE1} %{SOURCE2} .

chmod -x *.txt
sed 's/\r//' -i *.txt

sed \
  -e '/DOCSHAREDIR/d' \
  -e 's|wx-config |wx-config-3.0-gtk2 |g' \
  -e '/CXXFLAGS/s|-O3|-D"warn_static(arg)= " -DZEN_LINUX %{optflags}|g' \
  -e '/LINKFLAGS/s|-s|%{__global_ldflags}|g' \
  -i %{pname}/Source/Makefile %{pname}/Source/RealTimeSync/Makefile

sed 's/m_listBoxHistory->GetTopItem()/0/g' -i %{pname}/Source/ui/main_dlg.cpp

sed 's#inline##g' -i  %{pname}/Source/ui/version_check_impl.h

%build
%make_build -C %{pname}/Source
%make_build -C %{pname}/Source/RealTimeSync


%install
%make_install -C %{pname}/Source
%make_install -C %{pname}/Source/RealTimeSync

find %{buildroot}%{_datadir}/%{pname} -type f -exec chmod -x '{}' ';'

# Desktop files borrowed from https://aur.archlinux.org/packages/freefilesync and edited
mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{pname}.desktop <<EOF
[Desktop Entry]
Name=%{pname}
GenericName=File synchronization
GenericName[pt_BR]=Sincronização de arquivos
Comment=Backup software to synchronize files and folders
Comment[pt_BR]=Aplicação de backup para sincronizar arquivos e diretórios
Exec=%{pname}
Icon=%{pname}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Utility;
EOF

cat > %{buildroot}%{_datadir}/applications/RealTimeSync.desktop <<EOF
[Desktop Entry]
Name=RealTimeSync
GenericName=Automated Synchronization
GenericName[pt_BR]=Sincronização Automatizada
Comment=Real time synchronization
Comment[pt_BR]=Sincronização em tempo real
Exec=RealTimeSync
Icon=RealTimeSync
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Utility;
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -pm0644 %{pname}.png RealTimeSync.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/

for res in 16 22 24 32 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  for icon in %{pname} RealTimeSync ;do
    convert ${icon}.png -filter Lanczos -resize ${res}x${res}  \
      ${dir}/${icon}.png
  done
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
%license License.txt
%doc Changelog.txt
%{_bindir}/%{pname}
%{_bindir}/RealTimeSync
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/%{pname}


%changelog
* Thu Mar 30 2017 vinicius-mo <vinicius-mo at segplan.go.gov.br> - 8.10-1
- Initial spec.
