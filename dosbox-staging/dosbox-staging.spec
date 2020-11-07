Name:           dosbox-staging
Version:        0.75.2
Release:        1%{?dist}

Summary:        x86/DOS emulator with sound and graphics

License:        GPLv2+
URL:            https://dosbox-staging.github.io/

Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml


BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_net)
BuildRequires:  pkgconfig(opusfile)

Requires:       hicolor-icon-theme


%description
%{name} is a DOS-emulator using SDL for easy portability to different
platforms. 
%{name} emulates a 286/386 realmode CPU, Directory FileSystem/XMS/EMS,
a SoundBlaster card for excellent sound compatibility with older games...
You can "re-live" the good old days with the help of DOSBox, it can run plenty
of the old classics that don't run on your new computer!


%prep
%autosetup -n %{name}-%{version}

cp -p README manual.txt

sed \
  -e 's|DOSBOX|DOSBOX-STAGING|' \
  -e 's|dosbox |%{name} |g' \
  -i.orig docs/dosbox.1

./autogen.sh

%build
CFLAGS="%{build_cflags} -DNDEBUG" \
CXXFLAGS="%{build_cxxflags} -DNDEBUG" \
%configure \
  --program-suffix=-staging \
  --enable-core-inline \
%{nil}

%make_build


%check
make check


%install
%make_install

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --set-key="Exec" \
  --set-value="%{name}" \
  --dir=%{buildroot}%{_datadir}/applications \
  contrib/linux/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m0644 contrib/icons/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license COPYING
%doc AUTHORS README.md THANKS manual.txt docs/README.video
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/metainfo/%{name}.appdata.xml


%changelog
* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 0.75.2-1
- 0.75.2

* Wed Sep 23 2020 Phantom X <megaphantomx at hotmail dot com> - 0.75.1-1
- Initial spec


