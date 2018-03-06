Name:           aegisub
Version:        3.2.2
Release:        2.chinfo%{?dist}
Summary:        A general-purpose subtitle editor with ASS/SSA support
Epoch:          1

License:        BSD
URL:            http://www.aegisub.org/
Source0:        http://ftp.aegisub.org/pub/archives/releases/source/%{name}-%{version}.tar.xz

ExclusiveArch:  %{ix86} x86_64 armv7hl

BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(ffms2)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  wxGTK3-devel
Requires:       hicolor-icon-theme

Provides:       bundle(luajit) = 2.0.3

%description
Aegisub is a free, cross-platform open source tool for creating and modifying
subtitles. Aegisub makes it quick and easy to time subtitles to audio, and
features many powerful tools for styling them, including a built-in real-time
video preview.

%prep
%autosetup

sed -i -e '/version\.sh/s|\$srcdir/\.\.|$srcdir|g' configure
sed -i -e '/version_h_path/s|/aegisub/build/|/build/|g' build/version.sh

sed -i -e "/AEGISUB_COMMAND=/s|%{name}-.\..|%{name}|g" configure
sed -i -e 's| -O3||g' configure || exit 1

sed -i -e '/^repack-thes-dict_LIBS :=/s|$| -lpthread|g' tools/Makefile

%build
%configure \
  --disable-debug \
  --with-ffms2 \
  --with-alsa \
  --with-libpulse \
  --without-portaudio \
  --without-openal \
  --without-oss \
  --with-player-audio=PulseAudio \
  --with-hunspell \
  --disable-update-checker \
  --with-wx-config=/usr/bin/wx-config-3.0

%make_build


%install
%make_install

desktop-file-edit \
  --add-category="GTK" \
  --remove-mime-type="text/plain" \
  --remove-key="TryExec" \
  --set-key="Exec" \
  --set-value="%{name} %f" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%find_lang %{name}-32


%files -f %{name}-32.lang
%license LICENCE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/automation
%dir %{_datadir}/%{name}/automation/autoload
%{_datadir}/%{name}/automation/autoload/*
%dir %{_datadir}/%{name}/automation/demos
%{_datadir}/%{name}/automation/demos/*
%dir %{_datadir}/%{name}/automation/include
%{_datadir}/%{name}/automation/include/*


%changelog
* Sat Jun 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:3.2.2-2.chinfo
- BR: intltool

* Fri Jan 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.2.2-1
- Initial spec
