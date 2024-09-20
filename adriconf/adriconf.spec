Name:           adriconf
Version:        2.7.2
Release:        1%{?dist}
Summary:        Advanced DRI Configurator

License:        GPL-3.0-or-later
URL:            https://gitlab.freedesktop.org/mesa/%{name}

Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.bz2

Patch0:         %{url}/-/commit/26b7f8b0e82ea83a1275ab5d91e33df9d8ceaa68.patch#/%{name}-gl-26b7f8b.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtest-devel
BuildRequires:  ImageMagick
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(atkmm-2.36)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gtkmm-4.0)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libpci)
BuildRequires:  pkgconfig(pugixml)
Requires:       hicolor-icon-theme


%description
adriconf (Advanced DRI CONFigurator) is a GUI tool used to configure
open source graphics drivers. It works by setting options and writing
them to the standard drirc file used by the Mesa drivers.


%prep
%autosetup -n %{name}-v%{version} -p1


%build
%cmake \
  -DDATADIR:PATH=%{_datadir}/drirc.d \
  -DENABLE_UNIT_TESTS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key Version \
  --remove-category GNOME \
  --remove-category GTK \
  flatpak/org.freedesktop.%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 flatpak/org.freedesktop.%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

for res in 16 22 24 32 48 64 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick flatpak/org.freedesktop.%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/org.freedesktop.%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 flatpak/org.freedesktop.%{name}.metainfo.xml \
  %{buildroot}%{_metainfodir}/


%find_lang %{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.freedesktop.%{name}.metainfo.xml


%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/*.metainfo.xml


%changelog
* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 2.7.2-1
- 2.7.2

* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 2.7.1-1
- 2.7.1

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 2.5.0-2
- gcc 13 fix

* Wed Apr 06 2022 Phantom X <megaphantomx at hotmail dot com> - 2.5.0-1
- 2.5.0
- BR: -boost
- BR: libxml++-3.0->pugixml

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 2.4.1-1
- 2.4.1

* Fri Oct 23 2020 Phantom X <megaphantomx at hotmail dot com> - 2.4-1
- 2.4

* Tue Jan 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.6.1-1
- 1.6.1

* Tue Jan 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.6-1
- 1.6

* Sun Sep 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.1-1
- 1.5.1

* Tue Feb 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1
- 1.4
- BR: libxml++-3.0

* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1
- Initial spec
