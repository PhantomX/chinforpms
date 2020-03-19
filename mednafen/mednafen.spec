# src/types.h is set to issue error on i386 and warning on other architectures
# when trying to enable position-independent code. It is not recommended for
# performance reasons
%undefine _hardened_build

Name:           mednafen
Version:        1.24.1
%if 1%(echo %{version} | cut -d. -f3) == 10
%global unstable UNSTABLE
%endif
Release:        100%{?unstable:.%{unstable}}%{?dist}
Epoch:          1
Summary:        A multi-system emulator utilizing OpenGL and SDL
#mednafen is a monstrosity build out of many emulators hence the colourful licensing
License:        GPLv2+ and BSD and ISC and LGPLv2+ and MIT and zlib 
URL:            https://mednafen.github.io

Source0:        https://mednafen.github.io/releases/files/%{name}-%{version}%{?unstable:-%{unstable}}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  gettext
#BuildRequires:  libmpcdec-devel >= 1.3.0
#BuildRequires:  lzo-devel >= 2.0.9
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(sdl2) >= 2.0.5
BuildRequires:  pkgconfig(jack) >= 1.0.2
BuildRequires:  pkgconfig(sndfile) >= 1.0.2
BuildRequires:  pkgconfig(zlib)

%description
A portable, utilizing OpenGL and SDL, argument(command-line)-driven multi-system
emulator. Mednafen has the ability to remap hotkey functions and virtual system
inputs to a keyboard, a joystick, or both simultaneously. Save states are
supported, as is real-time game rewinding. Screen snapshots may be taken, in the
PNG file format, at the press of a button. Mednafen can record audiovisual
movies in the QuickTime file format, with several different lossless codecs
supported.

The following systems are supported(refer to the emulation module documentation
for more details):

* Atari Lynx
* Neo Geo Pocket (Color)
* WonderSwan
* GameBoy (Color)
* GameBoy Advance
* Nintendo Entertainment System
* Super Nintendo Entertainment System/Super Famicom
* Virtual Boy
* PC Engine/TurboGrafx 16 (CD)
* SuperGrafx
* PC-FX
* Sega Game Gear
* Sega Genesis/Megadrive
* Sega Master System
* Sega Saturn (experimental, x86_64 only)
* Sony PlayStation

Due to the threaded model of emulation used in Mednafen, and limitations of SDL,
a joystick is preferred over a keyboard to play games, as the joystick will have
slightly less latency, although the latency differences may not be perceptible
to most people. 


%prep
%autosetup -n %{name}

# Permission cleanup
find \( -name \*.c\* -or -name \*.h\* -or -name \*.inc \) -exec chmod -x {} \;


%build
CFLAGS="%{build_cflags} -Wl,-z,relro -Wl,-z,now"
CXXFLAGS="%{build_cxxflags} -Wl,-z,relro -Wl,-z,now"

export CFLAGS
export CXXFLAGS

# Bad optmizations to non haswell
export ax_cv_cflags_gcc_option__mtune_haswell=no

%configure \
  --disable-rpath \
  --disable-silent-rules \
#  --with-external-mpcdec \
#  --with-external-lzo \
%{nil}
%make_build


%install
%make_install

# Documentation cleanup
rm -rf Documentation/*.def Documentation/*.php Documentation/generate.sh \
    Documentation/Makefile.* Documentation/docgen.inc

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc ChangeLog TODO Documentation/*
%{_bindir}/%{name}


%changelog
* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.24.1-100
- 1.24.1

* Thu Dec 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.24.0-100.UNSTABLE
- 1.24.0

* Wed Sep 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.23.0-100.UNSTABLE
- 1.23.0

* Wed Apr 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.22.2-100
- 1.22.2

* Tue Jan 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.22.1-100
- 1.22.1

* Sun Jan 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.22.0-0.100.UNSTABLE
- 1.22.0
- UNSTABLE automagic label

* Sun Apr 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.21.3-1.chinfo
- 1.21.3

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.21.2-1.chinfo
- 1.21.2

* Sat Mar 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.21.1-1.chinfo
- 1.21.1
- URL update
- BR: alsa
- BR: sdl -> sdl2

* Wed Sep 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.48-1.chinfo
- 0.9.48

* Sat Sep 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.47-1.chinfo
- 0.9.47

* Thu Aug 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.46-1.chinfo
- 0.9.46

* Sun Jul 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.45.1-1.chinfo
- 0.9.45.1
- Disabled haswell optimizations

* Sun Apr 02 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.43-1
- Updated to 0.9.43

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.39.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Oct 29 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.39.2-1
- Updated to 0.9.39.2
- Updated %%description
- Dropped gcc-6 fix
- Cleaned up the .spec file
- Disabled hardened build, see types.h

* Mon Jul 04 2016 Sérgio Basto <sergio@serjux.com> - 0.9.38.7-2
- Fix error compiling with GCC 6.x on Fedora 24

* Thu Dec 31 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.38.7-1
- Updated to 0.9.38.7

* Sun Sep 27 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.38.6-1
- Updated to 0.9.38.6

* Tue Jul 14 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.38.5-1
- Updated to 0.9.38.5

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.9.33.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Apr 29 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.33.3-1
- Updated to 0.9.33.3
- Updared the Source URL

* Sun Nov 10 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.32-0.1
- Updated to 0.9.32-WIP

* Tue May 14 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.28-0.1
- Updated to 0.9.28-WIP

* Mon Apr 29 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.25-0.3
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 09 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.25-0.1
- Updated to 0.9.25-WIP

* Sat Aug 25 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.24-0.1
- Updated to 0.9.24-WIP

* Mon Jul 02 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.22-0.1
- Updated to 0.9.22-WIP

* Wed May 02 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.21-0.1
- Updated to 0.9.21-WIP
- Dropped upstreamed gcc-47 patch

* Fri Feb 10 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.19-0.1
- Updated to 0.9.19-WIP
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Updated %%description

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.18-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.18-0.1
- Updated to 0.9.18-WIP
- Dropped the NES sound patch

* Sat Aug 27 2011 Julian Weissgerber <sloevenh1@googlemail.com> - 0.9.17-0.2
- Patch to fix segfault when NES sound is enabled

* Wed Jun 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.17-0.1
- Updated to 0.9.17-WIP
- Updated the License tag

* Thu Apr 29 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.8.12-2.0.8.C
- Rebuilt for new libcdio

* Thu Jul 09 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.8.12-1.0.8.C
- Updated to 0.8.C
- Dropped the upstreamed gcc44 patch

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.8.11-2.0.8.B
- rebuild for new F11 features

* Sun Mar 08 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.8.11-1.0.8.B
- Updated to 0.8.B
- ExcludeArch: ppc64 on Fedora 11+

* Thu Nov  6 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.8.10-2.0.8.A
- Rebuilt. Something has mangled the x86_64 rpm

* Sun Nov  2 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.8.10-1.0.8.A
- Updated to 0.8.A

* Sat Sep 20 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.8.9-1
- Updated to 0.8.9
- Dropped the rpath patch, does not seem to be necessary

* Tue Jan 08 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.7-1
- Upgrade to 0.8.7

* Sun Nov 25 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.5-1
- Upgrade to 0.8.5

* Sun Nov 18 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.4-1
- Upgrade to 0.8.4
- Removed several patches which have been applied upstream
- License change due to new guidelines
- New URL as project homepage has changed

* Sat Apr 28 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.1-2
- Added patch to fix crashes with wonderswan roms
- Added patch to fix compilation on ppc

* Thu Apr 26 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.1-1
- Upgrade to 0.8.1

* Tue Feb 13 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.2-1
- Upgrade to 0.7.2

* Wed Jan 03 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.1-1
- Upgrade to 0.7.1
- Updated rpath patch
- Added support for jack

* Fri Oct 06 2006 Ian Chapman <packages[AT]amiga-hardware.ocm> 0.6.5-2
- Rebuild for new version of libcdio in fc6

* Thu Sep 07 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.6.5-1
- Upgrade to 0.6.5

* Wed Aug 23 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.6.4-1
- Upgrade to 0.6.4
- Minor alteration to RPM description due to new features

* Sat Aug 12 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.6.3-1
- Upgrade to 0.6.3
- Drop the libtool buildrequire and use the patch for fixing rpath

* Mon Jun 19 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.6.2-1
- Upgrade to 0.6.2

* Sun Jun 04 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.6.1-2
- Removed gawk buildrequire. Doesn't seem to be needed.
- Removed bison buildrequire. Doesn't seem to be needed.
- Replaced xorg-x11-devel with libGLU-devel for compatibility reasons with
  modular and non modular X
- Removed SDL-devel buildrequire, implied by SDL_net-devel

* Tue May 23 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.6.1-1.iss
- Initial Release
