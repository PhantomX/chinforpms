Name:           manaplus
Version:        1.8.9.1
Epoch:          1
Release:        100%{?dist}
Summary:        OpenSource 2D MMORPG client for Evol Online and The Mana World

License:        GPLv2+
URL:            http://manaplus.org/

Source0:        http://download.evolonline.org/manaplus/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_gfx)
BuildRequires:  pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  pkgconfig(SDL2_net)
BuildRequires:  pkgconfig(SDL2_ttf)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  librsvg2-tools
BuildRequires:  gettext-devel

Requires:       dejavu-sans-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       dejavu-serif-fonts
Requires:       liberation-mono-fonts
Requires:       liberation-sans-fonts
Requires:       mplus-1p-fonts
Requires:       hicolor-icon-theme
Requires:       xorg-x11-utils
Requires:       xdg-utils

Obsoletes:      mana < 0.6.1-8
Provides:       evolonline-client = %{version}-%{release}
Provides:       manaworld-client = %{version}-%{release}

%description
ManaPlus is an extended client for Evol Online, The Mana World, and similar
servers based on a fork of eAthena. Evol Online is a 2D fantasy-style game
which aims to create a friendly environment for interacting with others where
people can escape reality and enjoy themselves. The Mana World (TMW) is a
serious effort to create an innovative free and open source MMORPG.
TMW uses 2D graphics and aims to create a large and diverse interactive world.

%prep
%autosetup

%build
%configure \
  --disable-silent-rules \
  --disable-rpath \
  --with-dyecmd \
  --with-sdl2 \
  --without-internalsdlgfx
  
%make_build

%install
%make_install

# Use system fonts
rm -f %{buildroot}%{_datadir}/%{name}/data/fonts/*.ttf
ln -s ../../../fonts/dejavu/DejaVuSans-Bold.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/dejavusans-bold.ttf
ln -s ../../../fonts/dejavu/DejaVuSansMono-Bold.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/dejavusansmono-bold.ttf
ln -s ../../../fonts/dejavu/DejaVuSansMono.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/dejavusansmono.ttf
ln -s ../../../fonts/dejavu/DejaVuSans.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/dejavusans.ttf
ln -s ../../../fonts/dejavu/DejaVuSerifCondensed-Bold.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/dejavuserifcondensed-bold.ttf
ln -s ../../../fonts/dejavu/DejaVuSerifCondensed.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/dejavuserifcondensed.ttf
ln -s ../../../fonts/liberation/LiberationSans-Bold.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/liberationsans-bold.ttf
ln -s ../../../fonts/liberation/LiberationMono-Bold.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/liberationsansmono-bold.ttf
ln -s ../../../fonts/liberation/LiberationMono-Regular.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/liberationsansmono.ttf
ln -s ../../../fonts/liberation/LiberationSans-Regular.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/liberationsans.ttf
ln -s ../../../fonts/mplus/mplus-1p-bold.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/mplus-1p-bold.ttf
ln -s ../../../fonts/mplus/mplus-1p-regular.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/mplus-1p-regular.ttf
install -pm0644 data/fonts/wqy-microhei.ttf %{buildroot}%{_datadir}/%{name}/data/fonts/

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}test.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
ln -sf ../../../../%{name}/data/icons/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert data/icons/%{name}.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png
done

rm -rf %{buildroot}%{_datadir}/pixmaps

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog docs/FAQ.txt README
%{_bindir}/%{name}
%{_bindir}/dyecmd
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}test.desktop
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/*/%{name}*
%{_mandir}/man6/%{name}.6*
%{_mandir}/man6/%{name}test.6*


%changelog
* Thu Nov 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.9.1-100.chinfo
- 1.8.9.1
- SDL2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10.27.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.10.27.2-14
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10.27.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10.27.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10.27.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10.27.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10.27.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10.27.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.3.10.27.2-7
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.3.10.27.2-6
- Add an AppData file for the software center

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10.27.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.10.27.2-4
- Rebuild for new SDL_gfx

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10.27.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 09 2013 Bruno Wolff III <bruno@wolff.to> - 1.3.10.27.2-2
- Obsolete mana

* Sat Nov 09 2013 Bruno Wolff III <bruno@wolff.to> - 1.3.10.27.2-1
- Update to upstream 1.3.10.27.2
- ChangeLog: https://www.gitorious.org/manaplus/manaplus/source/94aee6b81132884686bce4473d67380c57c72fff:ChangeLog
- Temporarily, the -n option is needed for %%setup

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 16 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.3.17-1
- New upstream release 1.3.3.17
* Sun Feb 17 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.2.17-1
- New upstream release 1.3.2.17
* Sat Feb 9 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.2.3-2
- Dropped / between two filepath macros
- Fixed the path of the two SansSerif fonts
- Fixed name of xorg-x11-utils dependency
* Sun Feb 3 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.2.3-1
- New upstream release 1.3.2.3
* Fri Feb 1 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.1.20-2
- Added comments to the patches
* Fri Feb 1 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.1.20-1
- First version for official fedora repos.
