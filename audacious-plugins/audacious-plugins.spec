# build with GTK+2
%bcond_without gtk
# build with GTK+2 instead 3
%bcond_with gtk2
# build with qt5 instead 6
%bcond_with qt5

%{?with_gtk2:%global gtk_ver 2}%{!?with_gtk2: %global gtk_ver 3}
%{?with_qt5:%global qt_ver 5}%{!?with_qt5:%global qt_ver 6}

%global aud_plugin_api %(grep '[ ]*#define[ ]*_AUD_PLUGIN_VERSION[ ]\\+' %{_includedir}/libaudcore/plugin.h 2>/dev/null | sed 's!.*_AUD_PLUGIN_VERSION[ ]*\\([0-9]\\+\\).*!\\1!')
%if 0%{aud_plugin_api} > 0
%global aud_plugin_dep Requires: audacious(plugin-api)%{?_isa} = %{aud_plugin_api}
%endif
%{?aud_plugin_dep}

%global vc_url https://github.com/audacious-media-player/%{name}

%global tar_ver %%{lua:tar_ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(tar_ver)}

Name:           audacious-plugins
# If beta, use "~" instead "-", as ~beta1
Version:        4.4.2
Release:        100%{?dist}
Epoch:          1

# Minimum audacious/audacious-plugins version in inter-package dependencies.
%global aud_ver 4.4

Summary: Plugins for the Audacious audio player
URL:            http://audacious-media-player.org/

# list of license per plugin in README.licences
License:        BSD-2-Clause AND GPL-2.0-or-later AND LGPL-2.1-or-later AND GPL-3.0-only AND MIT AND BSD-3-Clause

Source0:        http://distfiles.audacious-media-player.org/%{name}-%{tar_ver}.tar.bz2
Source3:        README.licenses
# for optional packages
Source100:      audacious-plugins-amidi.metainfo.xml
Source101:      audacious-plugins-exotic.metainfo.xml
Source102:      audacious-plugins-jack.metainfo.xml
Source103:      audacious-plugins-ffaudio.metainfo.xml

# Fedora customization
Patch0:         audacious-plugins-3.7-alpha1-xmms-skindir.patch
# Fedora customization: add default system-wide module_path
Patch2:         audacious-plugins-3.6-ladspa.patch

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  audacious-devel >= %{aud_ver}
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(adplug)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libbinio)
BuildRequires:  pkgconfig(libbs2b)
BuildRequires:  pkgconfig(libcddb)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libcue)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  pkgconfig(libmpg123)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libopenmpt)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsidplayfp)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(lirc)
BuildRequires:  pkgconfig(neon)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(soxr)
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb-proto)
BuildRequires:  lame-devel
# ffaudio / ffmpeg
BuildRequires:  pkgconfig(libavcodec) >= 56.60.100
BuildRequires:  pkgconfig(libavformat) >= 56.40.101
BuildRequires:  pkgconfig(libavutil) >= 54.31.100 

BuildRequires:  pkgconfig(Qt%{qt_ver}Core)
BuildRequires:  pkgconfig(Qt%{qt_ver}Gui)
BuildRequires:  pkgconfig(Qt%{qt_ver}Widgets)
BuildRequires:  pkgconfig(Qt%{qt_ver}Multimedia)
BuildRequires:  pkgconfig(Qt%{qt_ver}Network)
BuildRequires:  pkgconfig(Qt%{qt_ver}OpenGL)
BuildRequires:  pkgconfig(Qt%{qt_ver}OpenGLWidgets)
BuildRequires:  pkgconfig(Qt%{qt_ver}Svg)
%if %{without qt5}
BuildRequires:  qt6-qtbase-private-devel
%else
BuildRequires:  pkgconfig(Qt5X11Extras)
%endif
BuildRequires:  pkgconfig(ampache_browser_1)

%{?with_gtk:BuildRequires: pkgconfig(gtk+-%{gtk_ver}.0)}
%{?with_gtk:BuildRequires: pkgconfig(gdk-x11-%{gtk_ver}.0)}

%global __provides_exclude_from ^%{_libdir}/audacious/.*\\.so$


%description
This package provides essential plugins for the Audacious audio player.


%package jack
Summary:        Audacious output plugin for Jack Audio Connection Kit
License:        BSD-2-Clause
%{?aud_plugin_dep}
Requires:       audacious-plugins%{?_isa} >= %{aud_ver}

%description jack
This package provides an Audacious output plugin that uses the
Jack Audio Connection Kit (JACK) sound service.


%package exotic
Summary:        Optional niche market plugins for Audacious 
# list of license per plugin in README.licences
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-3-Clause
%{?aud_plugin_dep}
Requires:       audacious-plugins%{?_isa} >= %{aud_ver}
# src/console/ for console.so input plugin in -exotic subpackage
Provides:       bundled(game-music-emu) = 0.5.5

%description exotic
This package provides optional plugins for Audacious, which do not aim
at a wide demographic audience. Most users of Audacious do not need this.

For example, included are input plugins for exotic audio file formats,
SID music (from Commodore 64 and compatibles), AdLib/OPL2 emulation,
console game music, the Portable Sound Format PSF1/PSF2, Vortex AM/YM
emulation, Nintendo DS Sound Format 2SF.


%package amidi
Summary:        Audacious input plugin for MIDI
License:        GPL-2.0-or-later
%{?aud_plugin_dep}
Requires:       audacious-plugins%{?_isa} >= %{aud_ver}

%description amidi
This package provides AMIDI-Plug, a modular MIDI music player, as an
input plugin for Audacious.

%package ffaudio
Summary:        FFmpeg input plugin for Audacious
License:        BSD-2-Clause
%{?aud_plugin_dep}
Requires:       audacious-plugins%{?_isa} >= %{aud_ver}
Obsoletes:      audacious-plugins-freeworld-ffaudio < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       audacious-plugins-freeworld-ffaudio = %{?epoch:%{epoch}:}%{version}-%{release}

%description ffaudio
This package provides FFmpeg as an input plugin for Audacious.


%prep
%autosetup -n %{name}-%{tar_ver} -p1

for i in src/ladspa/plugin.cc
do
    sed -i -e 's!__RPM_LIBDIR__!%{_libdir}!g' $i
    sed -i -e 's!__RPM_LIB__!%{_lib}!g' $i
done
if grep -q __RPM_LIB src/ladspa/plugin.cc ;then
  exit 1
fi


%build
# Enforce availability of the audacious(plugin-api) dependency.
%{!?aud_plugin_dep:echo 'No audacious(plugin-api) dependency!' && exit -1}

%meson \
  %{?with_gtk:-Dgtk=true%{?with_gtk2: -Dgtk2=true}}%{!?with_gtk:-Dgtk=false} \
  %{?with_qt5:-Dqt5=true} \
  -Dampache=true \
  -Dfilewriter-mp3=true \
  -Dflac=true \
  -Dmpg123=true \
  -Dneon=true \
  -Dopus=true \
  -Dvorbis=true \
  -Dopenmpt=true \
  -Dstreamtuner=true \
  -Daac=false  \
  -Dffaudio=true \
  -Dsndio=false \
  -Dmms=false \
%{nil}

%meson_build


%install
%meson_install

mkdir -p %{buildroot}%{_metainfodir}
install -p -m0644 %{SOURCE100} %{buildroot}%{_metainfodir}/
install -p -m0644 %{SOURCE101} %{buildroot}%{_metainfodir}/
install -p -m0644 %{SOURCE102} %{buildroot}%{_metainfodir}/
install -p -m0644 %{SOURCE103} %{buildroot}%{_metainfodir}/

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%dir %{_libdir}/audacious
%dir %{_libdir}/audacious/Container/
%{_libdir}/audacious/Container/asx.so
%{_libdir}/audacious/Container/asx3.so
%{_libdir}/audacious/Container/audpl.so
%{_libdir}/audacious/Container/cue.so
%{_libdir}/audacious/Container/m3u.so
%{_libdir}/audacious/Container/pls.so
%{_libdir}/audacious/Container/xspf.so
%dir %{_libdir}/audacious/Effect/
%{_libdir}/audacious/Effect/background_music.so
%{_libdir}/audacious/Effect/bitcrusher.so
%{_libdir}/audacious/Effect/bs2b.so
%{_libdir}/audacious/Effect/compressor.so
%{_libdir}/audacious/Effect/crossfade.so
%{_libdir}/audacious/Effect/crystalizer.so
%{_libdir}/audacious/Effect/echo.so
%{_libdir}/audacious/Effect/ladspa.so
%{_libdir}/audacious/Effect/mixer.so
%{_libdir}/audacious/Effect/resample.so
%{_libdir}/audacious/Effect/silence-removal.so
%{_libdir}/audacious/Effect/sox-resampler.so
%{_libdir}/audacious/Effect/speed-pitch.so
%{_libdir}/audacious/Effect/stereo.so
%{_libdir}/audacious/Effect/voice_removal.so
%dir %{_libdir}/audacious/General/
%{_libdir}/audacious/General/albumart-qt.so
%{_libdir}/audacious/General/ampache.so
%{_libdir}/audacious/General/cd-menu-items.so
%{_libdir}/audacious/General/delete-files.so
%{_libdir}/audacious/General/lirc.so
%{_libdir}/audacious/General/lyrics-qt.so
%{_libdir}/audacious/General/mpris2.so
%{_libdir}/audacious/General/notify.so
%{_libdir}/audacious/General/playlist-manager-qt.so
%{_libdir}/audacious/General/qthotkey.so
%{_libdir}/audacious/General/qtui.so
%{_libdir}/audacious/General/scrobbler.so
%{_libdir}/audacious/General/search-tool-qt.so
%{_libdir}/audacious/General/skins-qt.so
%{_libdir}/audacious/General/song_change.so
%{_libdir}/audacious/General/song-info-qt.so
%{_libdir}/audacious/General/statusicon-qt.so
%{_libdir}/audacious/General/streamtuner.so
%dir %{_libdir}/audacious/Input/
%{_libdir}/audacious/Input/cdaudio-ng.so
%{_libdir}/audacious/Input/flacng.so
%{_libdir}/audacious/Input/metronom.so
%{_libdir}/audacious/Input/modplug.so
%{_libdir}/audacious/Input/openmpt.so
%{_libdir}/audacious/Input/opus.so
%{_libdir}/audacious/Input/sndfile.so
%{_libdir}/audacious/Input/tonegen.so
%{_libdir}/audacious/Input/vorbis.so
%{_libdir}/audacious/Input/wavpack.so
%dir %{_libdir}/audacious/Output/
%{_libdir}/audacious/Output/alsa.so
%{_libdir}/audacious/Output/filewriter.so
%{_libdir}/audacious/Output/oss4.so
%{_libdir}/audacious/Output/pipewire.so
%{_libdir}/audacious/Output/pulse_audio.so
%{_libdir}/audacious/Output/qtaudio.so
%{_libdir}/audacious/Output/sdlout.so
%dir %{_libdir}/audacious/Visualization/
%{_libdir}/audacious/Visualization/blur_scope-qt.so
%{_libdir}/audacious/Visualization/gl-spectrum-qt.so
%{_libdir}/audacious/Visualization/qt-spectrum.so
%{_libdir}/audacious/Visualization/vumeter-qt.so
%dir %{_libdir}/audacious/Transport/
%{_libdir}/audacious/Transport/gio.so
%{_libdir}/audacious/Transport/neon.so
%{_datadir}/audacious/
# extra GTK specific plugin versions
%if %{with gtk}
%{_libdir}/audacious/General/albumart.so
%{_libdir}/audacious/General/aosd.so
%{_libdir}/audacious/General/gtkui.so
%{_libdir}/audacious/General/hotkey.so
%{_libdir}/audacious/General/lyrics-gtk.so
%{_libdir}/audacious/General/playlist-manager.so
%{_libdir}/audacious/General/search-tool.so
%{_libdir}/audacious/General/skins.so
%{_libdir}/audacious/General/statusicon.so
%{_libdir}/audacious/Visualization/blur_scope.so
%{_libdir}/audacious/Visualization/cairo-spectrum.so
%{_libdir}/audacious/Visualization/gl-spectrum.so
%endif
# name is misleading as it's based on libmpg123 not libmad
%{_libdir}/audacious/Input/madplug.so

%files jack
%{_libdir}/audacious/Output/jack-ng.so
%{_metainfodir}/%{name}-jack.metainfo.xml

%files exotic
%{_libdir}/audacious/Input/adplug.so
%{_libdir}/audacious/Input/console.so
%{_libdir}/audacious/Input/psf2.so
%{_libdir}/audacious/Input/sid.so
%{_libdir}/audacious/Input/vtx.so
%{_libdir}/audacious/Input/xsf.so
%{_metainfodir}/%{name}-exotic.metainfo.xml

%files amidi
%{_libdir}/audacious/Input/amidi-plug.so
#%%{_libdir}/audacious/Input/amidi-plug/
%{_metainfodir}/%{name}-amidi.metainfo.xml

%files ffaudio
%{_libdir}/audacious/Input/ffaudio.so
%{_metainfodir}/%{name}-ffaudio.metainfo.xml


%changelog
* Mon Nov 18 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.4.2-100
- 4.4.2

* Tue Oct 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.4-101
- Rebuild (ffmpeg)

* Wed Jun 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.4-100
- 4.4

* Mon May 01 2023 Phantom X <megaphantomx at hotmail dot com> - 1:4.3.1-100
- 4.3.1

* Sun Mar 12 2023 Phantom X <megaphantomx at hotmail dot com> - 1:4.3-100
- 4.3
- Rawhide sync

* Sat Feb 11 2023 Phantom X <megaphantomx at hotmail dot com> - 1:4.3~beta1-100
- 4.3-beta1

* Sat Jul 30 2022 Phantom X <megaphantomx at hotmail dot com> - 4.2-100
- 4.2

* Sat Jul 11 2020 Phantom X <megaphantomx at hotmail dot com> - 4.0.5-100
- 4.0.5

* Fri Jun 19 2020 Phantom X <megaphantomx at hotmail dot com> - 4.0.4-100
- 4.0.4

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 4.0.3-100
- 4.0.3
- streamtuner plugin is disabled now

* Wed Apr 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 4.0.2-100
- 4.0.2

* Mon Mar 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 4.0-100
- 4.0
- Qt is the default now

* Mon Feb 17 2020 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 3.10.1-7
- Rebuild against fluidsynth2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 26 2019 Michael Schwendt <mschwendt@fedoraproject.org> - 3.10.1-5
- Merge libopenmpt based input plugin that will be available in 4.0.
- Remove aging Obs/Prov and conditionals for RHEL <= 6.
- Use new RPM macros to exclude plugin .so Provides.

* Sat Aug 31 2019 Hans de Goede <hdegoede@redhat.com> - 3.10.1-4
- Rebuilt for libsidplayfp-2.0 (rhbz#1723876)
- Make bundled(game-music-emu) provides versioned

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 30 2018 Michael Schwendt <mschwendt@fedoraproject.org> - 3.10.1-1
- Update to 3.10.1.

* Wed Sep 19 2018 Michael Schwendt <mschwendt@fedoraproject.org> - 3.10-1
- GNOME shortcuts plugin is not available anymore.
- Update to 3.10 release.

* Fri Jul 13 2018 Michael Schwendt <mschwendt@fedoraproject.org> - 3.10-0.1.beta1
- Revert gnomeshortcuts plugin to 3.9 release, as the 3.10 version fails
  with GNOME >= 3.26 in Fedora >= 27.
- Upgrade to 3.10-beta1.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Michael Schwendt <mschwendt@fedoraproject.org> - 3.9-6
- Fix for gnomeshortcuts plugin for GNOME 3.26.
  Listen on org.gnome.SettingsDaemon.MediaKeys.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Michael Schwendt <mschwendt@fedoraproject.org> - 3.9-4
- Make build again after a change in Qt 5.
- Merge post-3.9 unbundling of adplug plugin and make it build without
  touching more than the plugin directory.
- Use %%autosetup.
- Avoid harmless macro in comment, which is an rpmbuild error now.

* Thu Jan 25 2018 Adrian Reber <adrian@lisas.de> - 3.9-3
- Rebuilt for libcdio-2.0.0

* Fri Sep  1 2017 Michael Schwendt <mschwendt@fedoraproject.org> - 3.9-2
- Build ampache_browser plugin.

* Sun Aug 20 2017 Michael Schwendt <mschwendt@fedoraproject.org> - 3.9-1
- Update to 3.9 release.
- TODO: ampache_browser lib needed for new plugin

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.8.2-4
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat May 13 2017 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8.2-3
- BR lame-devel and build filewriter with MP3 encoding (#1450225)
  now that LAME is available.
- Update gnomeshortcuts patch for -Werror=format-security.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 22 2017 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8.2-1
- Update to 3.8.2 (CVE-2016-9959 console video game music emu).

* Thu Dec  8 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8.1-2
- Build with --disable-mpg123 on Fedora < 25.

* Thu Dec  8 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8.1-1
- Update to 3.8.1.

* Mon Nov 14 2016 Adrian Reber <adrian@lisas.de> - 3.8-4
- Rebuilt for libcdio-0.94

* Sun Nov 13 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8-3
- Build with pkgconfig(libmpg123) and replace audacious-plugins-freeworld-mp3

* Sat Oct 22 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8-2
- Build Qt Audio output plugin.
- Improve BR for cleaner F25 buildroot.
- Revise configure options. 

* Thu Sep 22 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8-1
- Update to 3.8.

* Wed Sep  7 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.8-0.1.beta2
- Update to 3.8-beta2.

* Tue Jun  7 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.7.2-2
- Rebuild with new libcue

* Wed Apr 13 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7.2-1
- Update to 3.7.2.

* Thu Feb 25 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.7.1-4
- Rebuild with new libcue

* Sun Feb 14 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7.1-3
- Fix missing C++ header in jack-ng.cc (thanks Florian Weimer).

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7.1-1
- Update to 3.7.1.

* Sun Dec  6 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7-3
- Merge off-by-one fix in adplug/core/rol.cc as it can crash the player
  during probing of unknown input data.

* Sun Nov 29 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7-2
- Add ModernToolkit kudo to subpackage appdata files.

* Tue Nov 10 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7-1
- Update to 3.7.

* Sun Oct  4 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7-0.3.beta1
- Fix narrowing-conversion problem for ARM in adplug plugin once more.
  Upstream sync to AdPlug 2.2.1 overwrote the merged patch again.

* Sun Oct  4 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7-0.2.beta1
- Update to 3.7-beta1.
- Add search-tool-qt and statusicon-qt plugins.

* Wed Jul 15 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7-0.1.alpha1
- Copy from Copr packages:
- Update to 3.7-alpha1.
- Add playlist-manager-qt and skins-qt plugins.

* Fri Jul 10 2015 Hans de Goede <hdegoede@redhat.com> - 3.6.2-3
- Rebuilt for libsidplayfp soname bump

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun  7 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7-0.0.1
- Update to git master (20150607) 3.7-devel.

* Sun May 31 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6.2-1
- Update to 3.6.1 (222k diff, bug-fixes and translation updates).

* Thu Apr  9 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6.1-1
- Update to 3.6.1 (56k diff).
- Don't mention the old and dropped GSF plugin in subpackage description
  anymore.

* Tue Mar  3 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6-3
- armv7hl build fails with a narrowing conversion GCC error not found
  in Copr (x86_64/i686 only) builds. Probably further patches necessary.
  On ARM char is unsigned by default.
- For Fedora 23, build with gtk2 and Qt.
  Run "audacious --qt" once to switch to Qt user-interface.
- For Fedora 22, build with gtk2 and without Qt by default.
- Use %%make_install and %%license.
- Drop old Obs/Prov from -exotic subpackage.

* Mon Mar  2 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6-2
- Add build switches for test-building:
    --with gtk2
    --without qt
- Statusicon plugin is enabled by default for gtk2.
- Rediff ladspa patch, so it applies also to gtk2 based tarball.

* Sun Mar  1 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6-1
- Update to 3.6 final release.
- Derive source tarball version and builddir from %%version as to avoid
  a version definition in two macros.

* Thu Feb 19 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6-0.5.beta1
- Patch to prevent narrowing conversion error with GCC 5.

* Sun Feb 15 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6-0.4.beta1
- No AUTHORS file available anymore.
- Update to 3.6-beta1-gtk3.

* Tue Dec  9 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6-0.3.alpha1
- Update patches.

* Tue Dec  9 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.6-0.2.alpha1
- Update to 3.6-alpha1-gtk3.
- Oct 7: 3.6-0.1.20141007gitgc26d0fa
- TODO: rediff/revisit patches.
- No statusicon plugin anymore.
- Add a hack in %%build to make available Qt5's moc and uic in PATH.
- Plugin API version definition has moved to libaudcore header directory.
- Build with --enable-qt and --enable-gtk.
- Upgrade to git snapshot for another look at the Qt GUI for 3.6.

* Fri Jul 25 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.5.1-2
- Explicitly enable/disable some plugins for the updated configure script.

* Thu Jul 24 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.5.1-1
- Update to 3.5.1.

* Sat Jun 14 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.5-3
- Add appdata metainfo files for optional subpackages.
- Update list of licenses.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.5-1
- Update to 3.5 final release.
- Merge spec changes from packages released via Fedora Copr:
  - Plugin version moved to api.h header.
  - New delete-files plugin
  - No unix-io transport plugin anymore
  - No amidi-plug backend dir anymore
  - New asx3 Container plugin.

* Wed Jan  8 2014 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4.3-1
- Merge post-3.4.3 patch for fixing a font rendering problem in the
  skinned ui.
- Update to 3.4.3 (a few bug-fixes and translation updates). An update
  of 3rd party plugin packages to 3.4.3 is needed to get all fixes.

* Mon Dec 16 2013 Adrian Reber <adrian@lisas.de> - 3.4.2-2
- Rebuilt for libcdio-0.92

* Sun Nov  3 2013 Dan Fruehauf <malkodan@gmail.com> - 3.4.2-1
- Update to 3.4.2 final (fixes bugs 340, 346, 347, 356, 360, and 362).

* Mon Sep  9 2013 Dan Fruehauf <malkodan@gmail.com> - 3.4.1-1
- Update to 3.4.1 final (a few bug fixes, fixes gtk ui - #336).

* Tue Aug 27 2013 Hans de Goede <hdegoede@redhat.com> - 3.4-3
- Fix the skinned ui drawing only the skin background on F20+

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-1
- Update to 3.4 final (just the merged big-endian fix, and translation updates).

* Wed Jun 12 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-0.7.beta2
- New visualization plugin: gl-spectrum
- Update to 3.4-beta2 (which also includes newer Autotools files).

* Wed May 22 2013 Dan Horák <dan[at]danny.cz> - 3.4-0.6.beta1
- fix build on big-endian platforms

* Thu May  2 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-0.5.beta1
- BR soxr-devel (new package) and build SoX Resampler plugin (#958421).
- Due to more build requirements being optional also for features enabled
  by default, specify _all_ individual plug-ins in %%files lists instead
  of including full directories. Get rid of the few related existance
  checks in %%check.

* Tue Apr 23 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-0.4.beta1
- BR libsidplayfp-devel and include SID music player plug-in in the
  audacious-plugins-exotic subpackage. This sid.so plugin based on
  libsidplayfp 1.0.x is extensible with the original (albeit non-free and
  therefore not included) Kernal and Basic ROM image files to make it
  handle all files from the leading SID music collection.

* Mon Apr 22 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-0.3.beta1
- BR audacious-devel 3.4-beta1 for aud_drct_play_plause().

* Mon Apr 22 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-0.2.beta1
- Scrobbler2 plugin replaces scrobbler.
- Update to 3.4-beta1.
- BR autoconf automake and
  run autoreconf -f -I m4 for aarch64 updates (#925051).

* Thu Feb 14 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-0.2.alpha1
- Patch gnomeshortcuts plug-in to avoid auto-activating gnome-settings-daemon.

* Thu Feb  7 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.4-0.1.alpha1
- Playlist column resize feature requires GTK+ 3.8 to work correctly.
- Add scrobbler2 to %%check.
- Incremental upgrade to 3.4-alpha1.

* Sun Feb  3 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.4-1
- Update to 3.3.4 (last upstream maintenance release for 3.3.x).

* Tue Jan 22 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.3-4
- Make AOSD plug-in not crash when running into old config values from
  Audacious 3.2.4 or older. User should revisit plug-in preferences, too!

* Fri Jan 11 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.3-3
- Drop added .desktop files in favour of advertizing all MimeTypes in
  Audacious' own .desktop file. This is supposed to fix the assignment
  of Default Applications (GNOME bz #690119).
- Fedora 19 development: merge conditional upstream patch for libcdio 0.90
  and BR libcdio-paranoia-devel.

* Thu Jan  3 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.3-2
- Merge fix for wavpack input to not complain about .wvc files.
- Fix m3u parser to handle (=skip) empty lines.

* Tue Dec 11 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3 (a few bug-fixes and translation updates).

* Mon Sep 24 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2 (a few bug-fixes and translation updates).

* Sat Sep  8 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.1-3
- Merge fix for "Playlist does not progress for cue sheet
  of single flac file".

* Thu Aug 23 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.1-2
- Add recent method to filter plugin .so Provides to avoid polluting
  the RPM metadata.

* Mon Aug 13 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1 (a few bug-fixes and translation updates).

* Fri Jul 27 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3-1
- Update to 3.3 final.

* Thu Jul 26 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3-0.4.beta2
- Include the -sid desktop file in the src.rpm unconditionally,
  so it isn't missing when copying the src.rpm to older dists.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-0.3.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3-0.2.beta2
- Update to 3.3-beta2 and build for API 41.

* Thu Jul  5 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3-0.2.beta1
- A few plugins changed licensing to two-clause BSD.
- Update to 3.3-beta1.

* Sat Jun 30 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3-0.2.alpha1
- Make -sid Obsoletes non-versioned to avoid upgrade path issues.

* Mon Jun 18 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.3-0.1.alpha1
- Upgrade to 3.3-alpha1.

* Wed May 30 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2.3-2
- Fedora 18 only:
  Kill -sid subpackage, don't build libsidplay1 plugin anymore.
- Drop old -esd Obsoletes.

* Sat May 26 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2.3-1
- Update to 3.2.3 (bug-fixes and translation updates).

* Sun Apr  1 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2.2-1
- Updated to 3.2.2 for merged/additional fixes.

* Sun Mar 25 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2.1-3
- Fix playlist_delete_selected for gtkui.

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for c++ ABI breakage

* Sat Feb 18 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1 (first bugfix release in 3.2.x branch).

* Sat Jan 21 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2-1
- Update to 3.2 final (mostly translation updates and a very few fixes).

* Thu Jan 12 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2-0.4.beta2
- Update to 3.2-beta2.

* Sun Jan  8 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2-0.3.beta1
- Rebuild for GCC 4.7 as requested.
- Build experimental gio transport plugin.

* Mon Jan  2 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2-0.2.beta1
- Update to 3.2-beta1.

* Fri Dec 23 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.2-0.1.alpha1
- Explicitly link with gmodule-2.0.pc libs for missing libs.
- Upgrade to 3.2-alpha1.

* Sat Dec 10 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- Move plugin-api guard to %%build section to allow for --nodeps %%prep.

* Tue Dec  6 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1.

* Sun Nov 20 2011 Adrian Reber <adrian@lisas.de> - 3.1-2
- Rebuild for libcdio-0.83

* Wed Nov  9 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.1-1
- Update to 3.1.

* Wed Oct 26 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.1-0.1.beta3
- Update to 3.1-beta3.

* Mon Oct 17 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.1-0.1.beta2
- Update to 3.1-beta2.

* Tue Oct 11 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.1-0.1.beta1
- LADSPA plugin supports LADSPA_PATH environment variable again.
- Rocklight plugin not built anymore, and build-switch has been removed.
- Update to 3.1-beta1.

* Wed Sep 21 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.1-0.1.alpha1
- LADSPA plugin has returned, but is missing support for multiple search
  paths for modules (AUDPLUG-403).
- Upgrade to 3.1-alpha1.

* Mon Sep 19 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.3-1
- Update to 3.0.3 (some more translation updates).
- Let the plugin pkgs depend on audacious(plugin-api)%%{?_isa}.

* Fri Sep 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.2-3
- Use %%_isa in more dependencies.
- Drop unneeded BuildRoot stuff.
- Drop %%defattr lines.
- Drop old -wavpack and -vortex Obsoletes/Provides.

* Thu Sep  8 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.2-2
- Merge changes from pre-3.0.3 git, such as using libmodplug system
  library (BR libmodplug-devel).

* Thu Aug 25 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2 (few more fixes, 7k diff).

* Wed Aug 17 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.1-2
- Avoid xspf NULL ptr crash in g_utf8_validate.

* Thu Aug 11 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1 (a fix for xspf plus translation updates).

* Tue Jul 19 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0-1
- Update to 3.0 release.

* Mon Jul  4 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0-0.2.beta1
- Update to 3.0-beta1.

* Tue Jun 14 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 3.0-0.1.alpha1
- Several plugins are no longer available.
- Add BR libsmbclient-devel for SMB transport plugin.
- Handle the "enable gnomeshortcuts plugin by default" in this package.
- Build with GTK+ 3.
- Upgrade to 3.0-alpha1.

* Thu Jun  9 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5.1-3
- Rebuild for libmtp SONAME bump.
- Drop old audacious-plugins-metronome subpackage Obsoletes/Provides.

* Wed Jun  8 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5.1-2
- Fix Ogg metadata save for i686 (#711796).

* Thu May 19 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1.
- No longer --disable-sse2 for %%ix86 since this option has been dropped.

* Sat Apr 23 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5.0-3
- Merge fix for skinned ui track next/prev (AUD-331).
- Fix missing newline NULL-ptr crash in m3u loader (#699107).

* Fri Apr 22 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5.0-2
- Build OSS output plugin according to default.
- Build amidi plugin according to default.
- Only --disable-sse2 for %%ix86.
- Add a few more plugins to %%check section.

* Sat Apr 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0.

* Wed Apr  6 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.8.beta2
- Update to 2.5-beta2.

* Sat Mar 26 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.7.beta1
- Use correct icon name in -amidi/-sid desktop files.
- Add audio/midi MIME type to audacious-plugins-amidi package.

* Thu Mar 10 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.6.beta1
- Update to 2.5-beta1.
- TODO: openal audio output plugin?

* Wed Feb 23 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.5.alpha2
- Remove the extra vfs_close() call in adplug's new binio_virtual.h class,
  because closing the copied fd there crashes the player later.

* Tue Feb 22 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.4.alpha2
- Upgrade to 2.5-alpha2.
- Update the audacious(plugin-api) stuff in the spec file, so the new
  _AUD_PLUGIN_VERSION_MIN is not taken by mistake.
- Legacy icons patch merged upstream.
- Libnotify 0.7.0 API patch not necessary anymore.
- Merge from 2.4.3-10:
- Move the following exotic decoders into the audacious-plugins-exotic
  subpackage: adplug.so, console.so, psf2.so, vtx.so, xsf.so
- In spec file, update list of licenses used by various plugins.
- Update stripped tarball to also remove the .usf plugin source.

* Fri Feb  4 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.3.alpha1
- Enhance the audacious(plugin-api) stuff in the spec file and apply it
  to all subpackages.

* Tue Feb  1 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.2.alpha1
- Patch gtkui to not use legacy icon names anymore.

* Mon Jan 31 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.5-0.1.alpha1
- Upgrade to 2.5-alpha1.

* Fri Jan 28 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.3-5
- Merge fix for AUD-289.

* Thu Jan 27 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.3-4
- Require specific audacious(plugin-api) capability.
- Drop Obsoletes for audacious-plugins-arts (last in dist-f11-updates).

* Mon Jan 17 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.3-3
- F15 devel: Move adplug plugin into a subpackage: audacious-plugins-adplug
- Patch adplug core loaders a bit to prevent stupid crashes when
  loading either damaged or incorrectly parsed files into the playlist.

* Sun Jan 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.3-2
- Temporarily --disable-adplug for investigation of bz #669889.
- Require at least Audacious 2.4.3 (for uri_to_filename).

* Fri Jan 14 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3 (maintenance release in stable branch, 38k diff).

* Sun Dec 19 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.2-2
- Fix "Jump To" dialog seek (#663621) (AUDPLUG-308).

* Thu Dec  9 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2 (maintenance release in stable branch).
- strip-m3u-lines.patch not applied due to rewrite.

* Thu Nov  4 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.0-8
- Patch for libnotify 0.7.0 API change.

* Thu Nov  4 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.0-7
- Prevent buffer realloc crash in cue.c playlist_load_cue (#649645).

* Fri Oct  8 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.0-6
- Merge updated blur-scope plugin to fix segfaults.

* Fri Oct  8 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.0-5
- Merge psf.so (OpenPSF PSF1/PSF2 Audio Plugin) from upstream hg to
  resolve licensing issue.

* Wed Oct  6 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.0-4
- PATCH: handle .m3u files with extra whitespace (#640516, Hans de Goede).
- Merge scrobbler patch that prevents submitting NULL tags.
- Reenable projectM plugin for Fedora >= 14 (GCC >= 4.5).
- Update stripped tarball that removes the .psf plugin because of
  a licensing issue.

* Wed Sep 29 2010 jkeating - 2.4.0-3
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.0-2
- Handle neon transport fseek SEEK_END corner-case (#632369, Hans de Goede)
  so streamed files get a duration and become seekable.

* Thu Aug 26 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0 final.
- To avoid short loud blasting noise with Pulse Audio during track changes 
  and at track end, users may configure Pulse Audio daemon to run with
  "flat-volumes = no" instead of its default.

* Thu Aug 19 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.11.rc2
- Back out the pulse_flush() patch, because it is definitely a Pulse Audio
  bug that leads to loud noise and isn't specific to Audacious.

* Sat Aug 14 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.10.rc2
- In pulse_flush() call pa_stream_cork() to pause playback quickly in order
  to avoid loud clicks/noise when stopping/changing currently playing
  track. Afterwards restore previous 'corked' state again.
  Is this a Pulse Audio issue?

* Sat Aug 14 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.9.rc2
- Update to rc2.

* Tue Aug 10 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.8.rc1
- Update to rc1.

* Tue Aug  3 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.7.beta2
- Update to beta2.

* Mon Aug  2 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.6.beta1
- Nothing has ever before owned directory %%_libdir/audacious/ - now fixed.

* Wed Jul 21 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.5.beta1
- ESD (EsounD) output plugin no longer available.
- BR curl-devel, scrobbler built by default.
- Add %%check section to test availability of some files.
- Update to beta1.

* Thu Jul 15 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.4.alpha3
- BR libnotify-devel for "notify" plugin.
- Update to alpha3.

* Tue Jun 29 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.3.alpha2
- Returned: scrobbler/last.fm plugin (--enable-scrobbler)
- Remaining neon patch merged upstream.
- Update to alpha2.

* Mon Jun 14 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.2.alpha1
- Don't build projectM plugin, because it causes a C++ segfault on app exit
  even if just linking with libprojectM.

* Wed Jun  9 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.4-0.1.alpha1
- No longer available:
   * scrobbler/last.fm plugin (AUDPLUG-179)
     but has been resurrected post-alpha1
   * icecast plugin (AUDPLUG-156)
- Add BR libprojectM-devel, gtkglext-devel, libbs2b-devel
- Merge WavPack input plugin into base -plugins package.
- Merge Vortex input plugin into base -plugins package.
- Remove obsolete --disable-libmadtest configure option.
- Remove Provides/Obsoletes for old audacious-plugins-pulseaudio package,
  which were last in Fedora 8.
- Upgrade to 2.4 alpha1.

* Mon Jun  7 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-34
- Don't register window-state-event callback as this makes KDE hang
  when turning on sticky view mode (#601233) (AUDPLUG-178).

* Mon May 31 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-33
- Fix amidi-plug backend loader (#598005) and get_song_tuple.

* Sat Apr 10 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-32
- Fix the gtk_message_dialog_new_with_markup() call as in 2.3.

* Thu Apr  8 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-31
- Merge minor enhancements to the Status Icon patch to improve
  where it pops up with fast mouse movement.

* Fri Mar 19 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-30
- Fix colour array indexing in Scope Mode.

* Fri Mar 19 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-29
- Fix scaled visualization modes.

* Tue Mar 16 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-28
- Avoid div-by-zero crash due to almost empty MIDI files, which
  don't contain any delta-time events (#573851).

* Sat Mar 13 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-27
- Don't accept playlist_font name without space(s) (#573075). 

* Sat Mar 13 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-26
- Don't warn on stderr about missing adplug.db (#573187).

* Thu Mar  4 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-25
- Update icon popup patch for new playlist API to also fix a double-free
  (which made the popup crash with streaming audio).

* Tue Mar  2 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-24
- Patch notification area status icon (fix popup and title changes).

* Mon Feb 15 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-23
- Patch out the tuple/mowgli refcounting in the scrobbler plugin
  worker thread and use tuple_copy() instead. Let's see whether that
  will crash, too (see comment in -22).

* Mon Feb  8 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-22
- Remove scrobbler plugin, since upstream has disabled it by default
  in the post-2.2 tree, because it is believed to cause memory corruption
  that crashes Audacious: http://jira.atheme.org/browse/AUDPLUG-179

* Sat Feb  6 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-21
- Fix streambrowser streaminfo URL Add.

* Sat Feb  6 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-20
- Use John Lindgren's revised patch for the fix in -19
  (which properly frees also the g_build_filename allocated string).

* Fri Feb  5 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-19
- Fix temp file vulnerability in streambrowser plugin.

* Fri Feb  5 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-18
- Destroy neon request+session if ne_read_response_block failed and
  closed the connection. That way we don't call neon lib again with old 
  request+session which then crashes (#562164).

* Thu Feb  4 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-17
- Fix non-top-level ladspa plugin dialogs.

* Thu Feb  4 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-16
- Restore and fix the restore() function in "ladspa" plugin (#561635).
- Substitute hardcoded ladspa search paths in source code.

* Wed Feb  3 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-15
- Prevent race condition crash in streambrowser GUI (#561469).

* Tue Jan 26 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-14
- Fix too many open file descriptors issue in adplug plugin.
- Guard against out-of-bounds array access in adplug .lds decoder.

* Mon Jan 25 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-13
- In neon transport, after error handling set destroyed session
  pointers to NULL, so vfs seek doesn't crash.

* Fri Jan 22 2010 Adrian Reber <adrian@lisas.de> - 2.2-12
- Rebuild for libcdio-0.82 (F-13 Rawhide only)

* Sun Jan 17 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-11
- Rebuild for audacious.pc --libs changes.

* Fri Jan  8 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-10
- In neon transport, after error handling set destroyed request
  pointers to NULL, so vfs read exits early.

* Fri Jan  8 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-9
- Enable modplug plugin again: The code is an "in-progress rewrite [...]
  with many fixes for module formats not available in libmodplug, and is
  built partially on top of the work that the Schism Tracker authors have
  been doing.  Using libmodplug would be a step backwards as far as module
  compatibility goes." (AUDPLUG-158)

* Sat Jan  2 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-8
- Fix stack smashing in ui_svis_expose (#551801).

* Thu Dec 31 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-7
- Fix xspf Container plugin's handling of plain file names.
- Disable modplug plugin (where is it compared with libmodplug and
  its fixes and CVEs?). Give precedence to audacious-plugin-xmp
- Remove BR libmodplug-devel as the modplug plugin has never used
  the external library.

* Wed Dec 30 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-6
- Fix the alarm plugin.

* Fri Dec 25 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-5
- Remove BR libtimidity-devel as that plugin is no longer available.

* Fri Dec 25 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-4
- Let bluetooth plugin access "alsa-gapless" config values not "alsa"
  as it will be called in post-2.2.

* Sat Dec 19 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-3
- Beat bluetooth plugin a bit.
- Fix missing aud_cfg_db_close calls.
- Avoid that neon's ne_request_destroy() is called with a NULL ptr.

* Wed Dec  2 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-2
- Move SID music plugin into audacious-plugins-sid package. Its 
  built with libsidplay 1 while 3rd party package providers may
  build it with libsidplay 2.
- Include metronome plugin in base plugins package. No reason to
  split this off into an optional subpackage.

* Wed Nov 25 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-1
- Upgrade to 2.2 (declared as the next "stable release" after 2.1).
- The ladspa plugin has been reworked since beta2.

* Tue Nov 24 2009 Michael Schwendt <mschwendt@fedoraproject.org>
- BR libcue-devel which is available now and is enabled by default
  post 2.2-beta2
- Drop --disable-tta switch as that plugin is gone.

* Fri Nov 13 2009 Michael Schwendt <mschwendt@fedoraproject.org>
- Remove BR libmpcdec-devel ("musepack" plugin is not available anymore
  after 2.1 as it got removed in favour of "ffaudio"/ffmpeg plugin).

* Tue Nov 10 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-0.4.beta2
- Upgrade to 2.2-beta2
- Add patch to use old/working ladspa plugin from 2.0.1 (#533641).

* Fri Oct 30 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-0.4.beta1
- Fix non-top-level filewriter plugin dialogs.

* Sun Oct 25 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-0.3.beta1
- Update pulse_audio patch with correct get_song_name().

* Sun Oct 25 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-0.2.beta1
- Patch modplug plugin to remove old cruft and fix playback.

* Thu Oct 22 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-0.1.beta1
- Upgrade to 2.2-beta1
- Port old pulse_audio plugin from Audacious 2.1
  and patch it to fix volume issues.

* Wed Oct 21 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1-7
- Patch pulseaudio plugin to not suffer from precision loss when
  calculating the volume level to save.

* Wed Oct 21 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1-6
- Rediff the underruns patch and set buffer_time_min.

* Mon Oct 19 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1-5
- Patch pulseaudio plugin to not get confused by volume values passed
  in via callback.

* Sun Oct 18 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-0.1.alpha2
- Upgrade to 2.2-alpha2 (breaks ALSA output with alsa-plugins-pulseaudio!)

* Sun Sep 20 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.2-0.1.alpha1
- Upgrade to 2.2-alpha1 (primarly for alsa-gapless output plugin).
- Removes pulse_audio output plugin!
- Obsolete patches: timidity-cfg, keep-mixer-open

* Sun Sep 20 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1-4
- Patch alsa-ng plugin with some buffer prefilling to fight underruns.
- Merge minor changes from 2.2-alpha1 alsa-ng plugin.

* Thu Jul 30 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1-3
- Keep mixer open and not start at only %50 volume.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1-1
- Upgrade to 2.1 final.

* Mon Jun 29 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.1-0.1.beta1
- Upgrade to 2.1beta1.
- Drop merged/obsolete patches.

* Sat Jun  6 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.1-0.3
- Make libtimidity not try to open non-existing files.
- Fix non-top-level configure dialogs.

* Sat Jun  6 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.1-0.1
- Upgrade to 2.0.1.
- Fix sndfile plugin cleanup crash.
- Major spec overhaul, and drop old %%changelog entries.
- Obsolete -arts plugin.
- Multiple different licenses are used for the individual plugins.
- Move amidi-plug directory to amidi subpackage.
- Build with libsndfile plugin for advanced formats in WAV and
  patch it for pause and seek (also fixes #501007).

* Wed May 06 2009 Ralf Ertzinger <ralf@skytale.net> 1.5.1-5
- Fix possible crash on neon buffer underrun (BZ#496413)

