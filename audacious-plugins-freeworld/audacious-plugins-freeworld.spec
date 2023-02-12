%global aud_plugin_api %(grep '[ ]*#define[ ]*_AUD_PLUGIN_VERSION[ ]\\+' %{_includedir}/libaudcore/plugin.h 2>/dev/null | sed 's!.*_AUD_PLUGIN_VERSION[ ]*\\([0-9]\\+\\).*!\\1!')
%if 0%{aud_plugin_api} > 0
%global aud_plugin_dep Requires: audacious(plugin-api)%{?_isa} = %{aud_plugin_api}
%endif
%{?aud_plugin_dep}

# build with qt6 instead 5
%bcond_without qt6

%{?with_qt6:%global qt_ver 6}%{!?with_qt6:%global qt_ver 5}

%global tar_ver %%{lua:tar_ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(tar_ver)}

Name:           audacious-plugins-freeworld
# If beta, use "~" instead "-", as ~beta1
Version:        4.3~beta1
Release:        100%{?dist}
Summary:        Additional plugins for the Audacious media player
Epoch:          1

# Minimum audacious/audacious-plugins version in inter-package dependencies.
%global aud_ver 4.3

License:        BSD-2-Clause
URL:            http://audacious-media-player.org/

Source0:        http://distfiles.audacious-media-player.org/audacious-plugins-%{tar_ver}.tar.bz2

BuildRequires:  audacious-devel >= %{aud_ver}
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  gettext
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(faad2)
BuildRequires:  pkgconfig(libbinio)
BuildRequires:  pkgconfig(libmms)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(Qt%{qt_ver}Core)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  ffmpeg-devel

# we need to have configure detect atleast one audio output to make it happy
BuildRequires:  pkgconfig(alsa)

# require all the plugins
Requires:       %{name}-aac%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-mms%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-ffaudio%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%global __provides_exclude_from ^%{_libdir}/audacious/.*\\.so$


%description
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This package contains additional plugins for the Audacious media player.


%package        aac
Summary:        AAC playback plugin for Audacious
%{?aud_plugin_dep}
Requires:       audacious-plugins%{?_isa} >= %{aud_ver}

%description    aac
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play AAC audio files.


%package        ffaudio
Summary:        FFMpeg/FAAD2 based input plugin for Audacious
%{?aud_plugin_dep}
Requires:       audacious-plugins%{?_isa} >= %{aud_ver}

%description ffaudio
FFMpeg/FAAD2 based input plugin for Audacious.


%package        mms
Summary:        MMS stream plugin for Audacious
%{?aud_plugin_dep}
Requires:       audacious-plugins%{?_isa} >= %{aud_ver}

%description    mms
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to access MMS streams.


%prep
%setup -q -n audacious-plugins-%{tar_ver}


%build
%meson \
  -Dgtk=false \
  -Dqt=false \
  -Daac=true \
  -Dffaudio=true \
  -Dmms=true \
  -Dflac=false \
  -Dmpg123=false \
  -Dneon=false \
  -Dopus=false \
  -Dvorbis=false \
  -Dopenmpt=false \
  -Dsndio=false \
  -Dwavpack=false \
%{nil}


%ninja_build -C %{_vpath_builddir} src/aac/aac-raw.so
%ninja_build -C %{_vpath_builddir} src/ffaudio/ffaudio.so
%ninja_build -C %{_vpath_builddir} src/mms/mms.so


%install
mkdir -p %{buildroot}%{_libdir}/audacious/{Input,Transport}
install -pm0755 %{_vpath_builddir}/src/aac/aac-raw.so %{buildroot}%{_libdir}/audacious/Input/
install -pm0755 %{_vpath_builddir}/src/ffaudio/ffaudio.so %{buildroot}%{_libdir}/audacious/Input/
install -pm0755 %{_vpath_builddir}/src/mms/mms.so %{buildroot}%{_libdir}/audacious/Transport/


%files

%files aac
%license COPYING
%{_libdir}/audacious/Input/aac-raw.so

%files ffaudio
%license COPYING
%{_libdir}/audacious/Input/ffaudio.so

%files mms
%license COPYING
%{_libdir}/audacious/Transport/mms.so


%changelog
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

* Wed Apr 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 4.0.2-100
- 4.0.2

* Mon Mar 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 4.0-100
- 4.0

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.10.1-5
- Rebuild for ffmpeg-4.3 git

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 06 2019 Leigh Scott <leigh123linux@gmail.com> - 3.10.1-3
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 3.10.1-1
- Update to 3.10.1

* Sun Oct 14 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.10-1
- Update to 3.10 as in Fedora proper
- Remove Group tag
- Use make macros and update buildroot macro
- Add versioned audacious* BuildRequires and Requires
- Drop obsolete Obsoletes

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.9-5
- Rebuilt for new ffmpeg snapshot

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.9-3
- Rebuilt for ffmpeg-3.5 git

* Mon Oct 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.9-2
- Rebuild for ffmpeg update

* Sun Sep 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.9-1
- Update to 3.9 as in Fedora proper

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.8-5
- Rebuild for ffmpeg update

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 13 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 3.8-3
- Drop mp3 plugin, this is now in Fedora proper

* Tue Oct 25 2016 Sérgio Basto <sergio@serjux.com> - 3.8-2
- Upgrade from 3.7.x to 3.8. Includes a plugin API change that requires rebuilds
  of 3rd party plugin packages.

* Tue Oct 25 2016 Sérgio Basto <sergio@serjux.com> - 3.8-1
- Update to 3.8 as in Fedora proper
- Disable wavpack and flac detection.

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.7.2-2
- Rebuilt for ffmpeg-3.1.1

* Wed May 18 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 3.7.2-1
- Upgrade to 3.7.2

* Sun Jun 21 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 3.6.2-1
- Upgrade to 3.6.2

* Sat May 23 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 3.6.1-1
- Upgrade to 3.6.1 (rf#3659)

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 3.5.1-3
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 3.5.1-2
- Rebuilt for FFmpeg 2.4.x

* Fri Aug 08 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 3.5.1-1
- Upgrade to 3.5.1

* Thu Aug 07 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 3.5-3
- Fix building with new libmms (rf#3327)

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 3.5-2
- Rebuilt for ffmpeg-2.3

* Thu May  1 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 3.5-1
- Upgrade to 3.5

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 3.4.3-2
- Rebuilt for ffmpeg-2.2

* Sun Mar  2 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 3.4.3-1
- Upgrade to 3.4.3

* Thu Nov 21 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 3.4.2-1
- Upgrade to 3.4.2

* Sun Oct 13 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 3.4.1-1
- Upgrade to 3.4.1

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.4-3
- Rebuilt

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.4-2
- Rebuilt for FFmpeg 2.0.x

* Tue Jul  9 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 3.4-1
- Upgrade to 3.4, resolves rf#2849, rf#2868

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.3.4-2
- Rebuilt for x264/FFmpeg

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 3.3.4-1
- Upgrade to 3.3.4
- Drop .desktop files, the mimetypes have moved to the main pkg (rf#2636)

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.3.2-2
- Rebuilt for FFmpeg 1.0

* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 3.3.2-1
- Upgrade to 3.3.2

* Tue Jul 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.3-0.2.alpha1
- Rebuilt for mpeg123

* Sun Jun 24 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 3.3-0.1.alpha1
- Upgrade to 3.3-alpha1

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.2-3
- Rebuilt for x264/FFmpeg

* Sun Jan 29 2012 Hans de Goede <j.w.r.degoede@gmail.com> 3.2-2
- Silence false error printf's when reaching EOF on mp3 files

* Sun Jan 29 2012 Hans de Goede <j.w.r.degoede@gmail.com> 3.2-1
- Upgrade to 3.2

* Thu Nov  3 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.4-1
- Upgrade to 3.0.4

* Sun Sep  4 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.2-2
- Rebuild for ffmpeg-0.8

* Sat Aug 27 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.2-1
- Update to 3.0.2

* Wed Jun 22 2011 Hans de Goede <j.w.r.degoede@gmail.com> 2.5.2-1
- Update to 2.5.2
- Drop Provides + Obsoletes for upgrade path from livna / freshrpms

* Fri Apr 29 2011 Hans de Goede <j.w.r.degoede@gmail.com> 2.4.5-1
- Update to 2.4.5

* Mon Apr 11 2011 Hans de Goede <j.w.r.degoede@gmail.com> 2.4.4-1
- Update to 2.4.4

* Fri Jan 28 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.3-2
- Change audacious version require to use the new Fedora packages
  audacious(plugin-api) provides, for proper detection of plugin ABI changes

* Thu Jan 20 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.3-1
- Update to 2.4.3

* Sun Aug 29 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.0-1
- Update to 2.4.0

* Tue Aug 24 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4-0.1.rc2
- Update to 2.4-rc2

* Fri Jan 29 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-3
- Fix another hang in the madplug plugin (rf1061)

* Mon Jan 25 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-2
- Don't hang when trying to identify unknown files as mp3 files (rf1031)

* Sat Dec 19 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-1
- Update to 2.2

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.5.1-2
- rebuild for new F11 features

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.5.1-1
- Update to 1.5.1

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.4.5-2
- obsolete nonfree -plugins from livna 
- add metapackage that requires all the plugins and obsoletes the 
 -extras package from freshrpms

* Tue Feb 12 2008 Ralf Ertzinger <ralf@skytale.net> 1.4.5-1
- Update to 1.4.5

* Wed Jan 02 2008 Ralf Ertzinger <ralf@skytale.net> 1.4.4-1
- Update to 1.4.4

* Wed Dec 12 2007 Ralf Ertzinger <ralf@skytale.net> 1.4.2-1
- Update to 1.4.2

* Thu Nov 22 2007 Ralf Ertzinger <ralf@skytale.net> 1.4.1-2
- Update to 1.4.1

* Sat Jun 09 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.5-1.fc8
- Update to 1.3.5
- Disable SSE2 patch (now upsteam)

* Fri Jun 01 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.4-2.fc8
- Disable SSE2/AltiVec

* Sat May 26 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.4-1.fc8
- Update to 1.3.4

* Sun Apr 22 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.3-1.fc7
- Update to 1.3.3
- Introduce aud_ver variable into specfile

* Thu Apr 12 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.2-1.fc7
- Update to 1.3.2

* Wed Apr 04 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.1-3.fc7
- Update to 1.3.1

* Thu Nov 30 2006 Ralf Ertzinger <ralf@skytale.net> 1.2.5-1.fc7
- Update to 1.2.5

* Fri Nov 10 2006 Ralf Ertzinger <ralf@skytale.net> 1.2.2-1.fc7
- Update to 1.2.2

* Tue Nov 7 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-7.fc7
- Rebuild without gnome-vfs and Require: the correct audacious version
- Drop "X-Livna" and "Application" category from .desktop file

* Sat Oct 21 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info 1.1.2-5
- require audacious, not audacious-plugins-nonfree

* Wed Oct 18 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-4.fc6
- Add obsoletes/provides against bmp-mp3

* Mon Oct 16 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-2.fc6
- Fix directory name on %%setup

* Wed Sep 06 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-1.fc6
- Update to 1.1.2

* Tue Aug 15 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.1-4.fc6
- Properly add Requires(post/postun)
- Carry over changes from main audacious-1.1.1-4 package

* Tue Aug 01 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.1-3.fc6
- Initial RPM for livna
