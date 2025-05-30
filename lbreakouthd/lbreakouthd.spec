Name:           lbreakouthd
Version:        1.1.9
Release:        2%{?dist}
Summary:        A breakout-style arcade game

License:        GPL-3.0-only
URL:            http://lgames.sourceforge.net/

Source0:        https://downloads.sourceforge.net/lgames/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml

Patch0:         0001-gcc-15-build-fix.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
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

mkdir -p %{buildroot}%{_metainfodir}/
install -m0644 %{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


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
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.1.9-2
- Fix build with gcc 15

* Fri Sep 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1.1.9-1
- 1.1.9

* Tue May 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.1.3-1
- 1.1.3

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
