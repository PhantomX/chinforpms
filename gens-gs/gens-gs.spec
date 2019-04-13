%global orgname gens

Name:           %{orgname}-gs
Version:        2.16.7
Release:        100%{?dist}
Summary:        Sega Genesis, Sega CD, and Sega 32X emulator

URL:            http://segaretro.org/Gens/GS
#Most source files are GPLv2+ excludding the following, which are LGPLv2+:
#Source files for 2xsai, hq*x, super_eagle, super_2xsai, blargg_ntsc filters found in src/mdp/render/
#src/gens/ui/gtk/gtk-uri.h and src/gens/ui/gtk/gtk-uri.c
#As well, code in src/starscream uses the starscream license (non-free)
License:        GPLv2+ and LGPLv2+ and MIT and BSD and Starscream (Nonfree)

Source0:        https://retrocdn.net/images/6/6d/Gens-gs-r7.tar.gz
#Found via Arch Linux: https://www.archlinux.org/packages/community/i686/gens-gs/
#Replaces deprecated gtk functions with working ones
#Cannot be sumbitted upstream, as upcomming version no longers uses GTK
Patch0:         %{name}-gtk.patch

ExclusiveArch:  i686

BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl)

Requires:       hicolor-icon-theme
Requires:       %{name}-doc = %{?epoch:%{epoch}:}%{version}-%{release}

%if 0%{?fedora} >= 30
BuildRequires:  minizip-compat-devel
%else
BuildRequires:  minizip-devel
%endif


%package        doc
Summary:        Documentation Manual for Gens/GS
BuildArch:      noarch

%description
#taken from here: http://segaretro.org/Gens/GS 
Gens/GS is a Sega Mega Drive emulator derived from Gens and maintained by
GerbilSoft. Project goals include clean source code, combined features from
various developments of Gens, and improved platform portability.

%description doc
This package contains the documentation manual for Gens/GS

%prep
%autosetup -n %{name}-r7 -p1

#Erase all use of external libs:
sed -i '/extlib/d' configure.ac
sed -i 's/extlib//' src/Makefile.am

#Use shared minizip:
sed -i '/minizip/d' src/%{orgname}/Makefile.am
sed -i 's/"minizip\/unzip.h"/<minizip\/unzip.h>/' src/%{orgname}/util/file/decompressor/md_zip.c

#Remove all bundled code
rm -f -r src/extlib

#Rename to gens-gs to avoid conflicts:
sed -i 's/INIT(gens,/INIT(gens-gs,/' configure.ac
sed -i 's/gens.desktop/gens-gs.desktop/' xdg/Makefile.am
mv xdg/%{orgname}.desktop xdg/%{name}.desktop

# modify icon field in desktop to use hicolor icons
sed -i '/Icon=*/cIcon=%{name}' xdg/%{name}.desktop

sed -i 's/Exec=.*/Exec=%{name}/' xdg/%{name}.desktop

#Obsolete macro in configure.ac
sed -i 's/AC_PROG_LIBTOOL/LT_INIT([disable-static])/' configure.ac

autoreconf -ivf

%build

%configure \
  --without-7z --enable-mp3=no --with-pic \
  --disable-static --build=i686-redhat-linux \
  --docdir='%{_defaultdocdir}/%{name}-%{version}' \
  LIBS="-ldl -lX11 -lminizip" \
%{nil}

%make_build

%install
%make_install

#rename binary to gens-gs
mv %{buildroot}%{_bindir}/%{orgname} %{buildroot}%{_bindir}/%{name}

#Use imagemagick to create a 128x128 icon from 128x96 image
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
convert images/%{orgname}_small.png -background none -gravity center -extent 128x128! %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
#Copy icons into hicolor
for size in 16 32 48; do
  dim="${size}x${size}"
  install -p -D -m 0644 images/%{orgname}gs_$dim.png \
  %{buildroot}%{_datadir}/icons/hicolor/$dim/apps/%{name}.png
done

#install modified desktop file
desktop-file-install \
  --remove-key=Encoding \
  --dir %{buildroot}%{_datadir}/applications \
  xdg/%{name}.desktop

#remove any .la files that may have generated:
rm -f %{buildroot}%{_libdir}/mdp/*.la

%files
%license COPYING.txt
%doc README.txt NEWS.txt
%{_libdir}/mdp/
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_bindir}/%{name}
%{_bindir}/mdp_test
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files doc
%{_defaultdocdir}/%{name}-%{version}


%changelog
* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.16.7-100
- chinforpms

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.16.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.16.7-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 2.16.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.16.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.16.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 25 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.16.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 19 2016 Nicolas Chauvet <kwizart@gmail.com> - 2.16.7-6
- Drop BuildArch: noarch for doc - avoid pulling in x86_64 repo

* Mon Oct 27 2014 Jeremy Newton <alexjnewt@hotmail.com> - 2.16.7-5
- Patch to remove conflict with gens
- Remove prefix=/usr from configure

* Mon Oct 6 2014 Jeremy Newton <alexjnewt@hotmail.com> - 2.16.7-4
- Remove static libraries
- Created doc package
- Added Readme, News and Copying files

* Wed Jan 1 2014 Jeremy Newton <alexjnewt@hotmail.com> - 2.16.7-3
- Properly link Minizip, fix build issue

* Tue Jul 31 2012 Jeremy Newton <alexjnewt@hotmail.com> - 2.16.7-2
- Fixed License
- Disable Bundled 7zip and mpg123
- Added more build requires to avoid use of bundled code
- Manually unbundle minizip

* Tue Jul 24 2012 Jeremy Newton <alexjnewt@hotmail.com> - 2.16.7-1
- Initial working package SPEC created
