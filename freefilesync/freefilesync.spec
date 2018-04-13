%global pname FreeFileSync
%global xbrzver 1.6

Name:           freefilesync
Version:        9.9
Release:        1%{?dist}
Summary:        A file synchronization utility

License:        GPLv3
URL:            http://www.freefilesync.org/
Source0:        http://www.freefilesync.org/download/%{pname}_%{version}_Source.zip
Source1:        https://aur.archlinux.org/cgit/aur.git/plain/ffsicon.png?h=%{name}#/%{pname}.png
Source2:        https://aur.archlinux.org/cgit/aur.git/plain/rtsicon.png?h=%{name}#/RealTimeSync.png
Source3:        http://downloads.sourceforge.net/project/xbrz/xBRZ/xBRZ_%{xbrzver}.zip

BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  boost-devel
BuildRequires:  compat-wxGTK3-gtk2-devel
Requires:       hicolor-icon-theme

%description
FreeFileSync is a free Open Source software that helps you synchronize
files and synchronize folders for Windows, Linux and macOS. It is
designed to save your time setting up and running backup jobs while
having nice visual feedback along the way.

%prep
%autosetup -p0 -c -n %{pname}-%{version}

mkdir -p xBRZ/src
unzip %{SOURCE3} -d xBRZ/src

cp %{SOURCE1} %{SOURCE2} .

chmod -x *.txt
sed 's/\r//' -i *.txt

cp -p Changelog.txt %{pname}/Build

sed \
  -e '/DOCSHAREDIR/d' \
  -e 's|wx-config |wx-config-3.0-gtk2 |g' \
  -e '/CXXFLAGS/s|-O3|-D"warn_static(arg)= " -DZEN_LINUX %{optflags}|g' \
  -e '/LINKFLAGS/s|-s|%{build_ldflags}|g' \
  -i %{pname}/Source/Makefile %{pname}/Source/RealTimeSync/Makefile

# Fixes from https://aur.archlinux.org/packages/freefilesync
# wxgtk < 3.1.0
sed 's/m_listBoxHistory->GetTopItem()/0/g' -i %{pname}/Source/ui/main_dlg.cpp

# gcc 6.3.1
sed -i 's!static_assert!//static_assert!' zen/scope_guard.h

# linker error
sed 's#inline##g' -i %{pname}/Source/ui/version_check_impl.h

# add xbrz.cpp entries in Makefile
sed "/zlib_wrap.cpp/ a CPP_LIST+=../../xBRZ/src/xbrz.cpp" \
  -i %{pname}/Source/Makefile
sed "/popup_dlg_generated.cpp/ a CPP_LIST+=../../../xBRZ/src/xbrz.cpp" \
 -i %{pname}/Source/RealTimeSync/Makefile

# edit lines to remove functions that require wxgtk 3.1.x  
sed -e 's:m_textCtrlOfflineActivationKey->ForceUpper:// &:g' \
  -i '%{pname}/Source/ui/small_dlgs.cpp'
sed -e 's:const double scrollSpeed =:& 6; //:g' -i 'wx+/grid.cpp'

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


%files
%license License.txt
%doc Changelog.txt
%{_bindir}/%{pname}
%{_bindir}/RealTimeSync
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/%{pname}


%changelog
* Thu Apr 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 9.9-1
- 9.9
- More fixes from https://aur.archlinux.org/packages/freefilesync

* Fri Feb 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 9.8-1
- 9.8

* Tue Nov 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 9.5-1
- 9.5

* Thu Oct 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 9.4-1
- 9.4

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 9.2-1
- 9.2

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 9.1-1
- 9.1

* Thu Mar 30 2017 Phantom X <megaphantomx at bol dot com dot br> - 8.10-1
- Initial spec.
