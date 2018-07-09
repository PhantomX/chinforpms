%global pkgname FreeFileSync
%global xbrzver 1.6

Name:           freefilesync
Version:        10.1
Release:        1%{?dist}
Summary:        A file synchronization utility

License:        GPLv3
URL:            http://www.freefilesync.org/
Source0:        http://www.freefilesync.org/download/%{pkgname}_%{version}_Source.zip
Source1:        https://aur.archlinux.org/cgit/aur.git/plain/ffsicon.png?h=%{name}#/%{pkgname}.png
Source2:        https://aur.archlinux.org/cgit/aur.git/plain/rtsicon.png?h=%{name}#/RealTimeSync.png

BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  boost-devel
BuildRequires:  compat-wxGTK3-gtk2-devel
Requires:       hicolor-icon-theme

%description
FreeFileSync is a free Open Source software that helps you synchronize
files and synchronize folders for Windows, Linux and macOS. It is
designed to save your time setting up and running backup jobs while
having nice visual feedback along the way.


%prep
%autosetup -p0 -c -n %{pkgname}-%{version}

cp %{SOURCE1} %{SOURCE2} .

chmod -x *.txt
sed 's/\r//' -i *.txt

cp -p Changelog.txt %{pkgname}/Build

sed \
  -e '/DOCSHAREDIR/d' \
  -e 's|wx-config |%{_libdir}/wx/config/gtk2-unicode-3.0 |g' \
  -e 's|-O3 -DNDEBUG|-DNDEBUG -D"warn_static(arg)= " -DZEN_LINUX %{build_cxxflags}|g' \
  -e '/LINKFLAGS/s|-s|%{build_ldflags}|g' \
  -e '/LINKFLAGS/s|-pthread|-lz \0|g' \
  -i %{pkgname}/Source/Makefile %{pkgname}/Source/RealTimeSync/Makefile

# Fixes from https://aur.archlinux.org/packages/freefilesync
# wxgtk < 3.1.0
sed 's/m_listBoxHistory->GetTopItem()/0/g' -i %{pkgname}/Source/ui/main_dlg.cpp

# gcc 6.3.1
sed -i 's!static_assert!//static_assert!' zen/scope_guard.h

# linker error
sed 's#inline##g' -i %{pkgname}/Source/ui/version_check_impl.h

# edit lines to remove functions that require wxgtk 3.1.x  
sed -e 's:m_textCtrlOfflineActivationKey->ForceUpper:// &:g' \
  -i '%{pkgname}/Source/ui/small_dlgs.cpp'
sed -e 's:const double scrollSpeed =:& 6; //:g' -i 'wx+/grid.cpp'

%build
%make_build -C %{pkgname}/Source
%make_build -C %{pkgname}/Source/RealTimeSync


%install
%make_install -C %{pkgname}/Source
%make_install -C %{pkgname}/Source/RealTimeSync

find %{buildroot}%{_datadir}/%{pkgname} -type f -exec chmod -x '{}' ';'

# Desktop files borrowed from https://aur.archlinux.org/packages/freefilesync and edited
mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{pkgname}.desktop <<EOF
[Desktop Entry]
Name=%{pkgname}
GenericName=File synchronization
GenericName[pt_BR]=Sincronização de arquivos
Comment=Backup software to synchronize files and folders
Comment[pt_BR]=Aplicação de backup para sincronizar arquivos e diretórios
Exec=%{pkgname}
Icon=%{pkgname}
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
install -pm0644 %{pkgname}.png RealTimeSync.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/

for res in 16 22 24 32 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  for icon in %{pkgname} RealTimeSync ;do
    convert ${icon}.png -filter Lanczos -resize ${res}x${res}  \
      ${dir}/${icon}.png
  done
done


%files
%license License.txt
%doc Changelog.txt
%{_bindir}/%{pkgname}
%{_bindir}/RealTimeSync
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/%{pkgname}


%changelog
* Tue Jun 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 10.1-1
- 10.1

* Thu May 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 10.0-1
- 10.0

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 9.9-2
- Fix for Fedora 28 wx-config

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
