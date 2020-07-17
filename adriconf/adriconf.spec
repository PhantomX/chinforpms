Name:           adriconf
Version:        1.6.1
Release:        1%{?dist}
Summary:        Advanced DRI Configurator

License:        GPLv3+
URL:            https://github.com/jlHertel/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtest-devel
BuildRequires:  ImageMagick
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libpci)
BuildRequires:  pkgconfig(libxml++-3.0)
BuildRequires:  pkgconfig(x11)
Requires:       hicolor-icon-theme


%description
adriconf (Advanced DRI CONFigurator) is a GUI tool used to configure
open source graphics drivers. It works by setting options and writing
them to the standard drirc file used by the Mesa drivers.


%prep
%autosetup -p1


%build
%cmake \
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
  flatpak/br.com.jeanhertel.%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 flatpak/br.com.jeanhertel.%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

for res in 16 22 24 32 48 64 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert flatpak/br.com.jeanhertel.%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/br.com.jeanhertel.%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 flatpak/br.com.jeanhertel.%{name}.appdata.xml \
  %{buildroot}%{_metainfodir}/
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/br.com.jeanhertel.%{name}.appdata.xml

%find_lang %{name}


%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/*.appdata.xml


%changelog
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
