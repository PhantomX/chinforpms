Name:           dosbox-staging
Version:        0.76.0
Release:        1%{?dist}

Summary:        x86/DOS emulator with sound and graphics

License:        GPLv2+
URL:            https://dosbox-staging.github.io/

Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml


BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  librsvg2-tools
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl2) >= 2.0.2
BuildRequires:  pkgconfig(SDL2_net)
BuildRequires:  pkgconfig(opusfile)

Requires:       hicolor-icon-theme
Recommends:     fluid-soundfont-gm


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
# Use -O3 over -O2, as implementation relies on compiler optimizations.
# This makes the performance slightly better and average FPS timings much more
# predictable.

export CFLAGS="%(echo %{build_cflags} | sed -e 's/-O2\b/-O3/') -DNDEBUG"
export CXXFLAGS="%(echo %{build_cxxflags} | sed -e 's/-O2\b/-O3/') -DNDEBUG"

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

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert contrib/icons/%{name}.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png
done

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
* Fri Dec 04 2020 Phantom X <megaphantomx at hotmail dot com> - 0.76.0-1
- 0.76.0
- Upstream review sync
- BR: fluidsynth

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 0.75.2-1
- 0.75.2

* Wed Sep 23 2020 Phantom X <megaphantomx at hotmail dot com> - 0.75.1-1
- Initial spec


