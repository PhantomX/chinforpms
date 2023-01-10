Name:           lbreakouthd
Version:        1.1.1
Release:        1%{?dist}
Summary:        A breakout-style arcade game

License:        GPL-3.0-only
URL:            http://lgames.sourceforge.net/

Source0:        https://downloads.sourceforge.net/lgames/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  pkgconfig(SDL2_ttf)
Requires:       hicolor-icon-theme


%description
LBreakoutHD is an HD remake of LBreakout2, a breakout-style arcade game, with a
brand new fully scalable 16:9 view.


%prep
%autosetup -p1

cp -p %{S:1} %{name}.appdata.xml
sed -e 's|_VERSION_|%{version}|g' -i %{name}.appdata.xml

convert %{name}256.gif %{name}.png

sed -e 's|-Wno-format | |g' -i configure.ac
autoreconf -ivf


%build
%configure \
  --localstatedir=%{_var}/lib/games \
  --disable-silent-rules \
  --disable-rpath \
%{nil}

%make_build


%install
%make_install

desktop-file-edit \
  --set-icon=%{name} \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

rm -f %{buildroot}%{_datadir}/icons/*.gif
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

for res in 16 22 24 32 36 48 64 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}/
install -m0644 %{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc Changelog README
%attr(2551, root, games) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.png
%{_metainfodir}/%{name}.appdata.xml
%config(noreplace) %attr(664, root, games) %{_localstatedir}/lib/games/%{name}.hscr


%changelog
* Tue Jan 10 2023 Phantom X <megaphantomx at hotmail dot com> - 1.1.1-1
- 1.1.1

* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1.0.10-1
- 1.0.10

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.0.9-2
- BR: gcc-c++

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.0.9-1
- 1.0.9

* Mon Dec 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.8-1
- 1.0.8

* Sun Nov  1 2020 Phantom X <megaphantomx at hotmail dot com> - 1.0.6-1
- Initial spec
