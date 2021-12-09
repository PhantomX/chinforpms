# 87daea8a06ec2197443548ed49e27c6404a2cdb2 is the last one with SSE2 support
%global commit 94c6814be8a471de6c1f59bf73689b473aafc039
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210821
%global with_snapshot 1

%global sanitize 0
%bcond_with     native
# Revert SSE4 updates
%bcond_without  sse4

%global perms_pcsx2 %caps(cap_net_admin,cap_net_raw+eip)

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%undefine _hardened_build

%global jpgc_ver 1.05

Name:           pcsx2
Version:        1.7.0
Release:        137%{?gver}%{?dist}
Summary:        A Sony Playstation2 emulator

License:        GPLv3 and LGPLv3+
URL:            https://github.com/PCSX2/pcsx2

%if 0%{sanitize}
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
%else
# Use Makefile to download
%if 0%{?with_snapshot}
Source0:        %{name}-clean-%{shortcommit}.tar.xz
%else
Source0:        %{name}-clean-%{version}.tar.xz
%endif
%endif
Source1:        Makefile

%if %{without sse4}
# Revert this, needs sse4
Patch0:         0001-Revert-SSE4-updates.patch
%endif
Patch1:         0001-System-libchdr-support.patch
Patch2:         0001-common-build-as-static.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fmt) >= 7.1.3
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libsparsehash)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(harfbuzz)
#BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(soundtouch)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(yaml-cpp)
BuildRequires:  pkgconfig(zlib)
# use SDL that depends wxGTK
BuildRequires:  wxGTK3-devel
BuildRequires:  fonts-rpm-macros
BuildRequires:  gettext
BuildRequires:  libaio-devel
BuildRequires:  perl-interpreter
BuildRequires:  sdl_gamecontrollerdb >= 0-41

Requires:       joystick
Requires:       hicolor-icon-theme

Provides:       bundled(jpeg-compressor) = %{jpgc_ver}
Provides:       bundled(xbyak)

%if %{without sse4}
%global _description %{expand:
WARNING: This build is modified to require a CPU with SSE2 instructions and is
not supported by upstream.}
%else
%global _description %{expand:
WARNING: It requires a CPU with SSE4 instructions. If your CPU does not
support this instruction set, it does not have enough horsepower to run
this emulator anyway.}
%endif


%description
A Playstation 2 emulator. Requires a dump of a real PS2 BIOS (not included)
%_description


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

%if 0%{sanitize}
  mv 3rdparty/include .
  mv 3rdparty/jpgd .
  mv 3rdparty/xbyak .
  rm -rf 3rdparty/*
  mv include 3rdparty/
  mv jpgd 3rdparty/
  mv xbyak 3rdparty/
  rm -rf tools
  rm -f common/src/Utilities/x86/MemcpyFast.cpp
  rm -rf .git
%endif

# To remove executable bits from man, doc and icon files
chmod -x pcsx2/Docs/GPL.txt pcsx2/Docs/License.txt pcsx2/Docs/PCSX2_FAQ.md \
  pcsx2/Docs/Configuration_Guide/Configuration_Guide.md bin/docs/PCSX2.1 linux_various/PCSX2.xpm

# Remove DOS encoding errors in txt files
sed -i 's/\r//' pcsx2/Docs/GPL.txt
sed -i 's/\r//' pcsx2/Docs/License.txt

#Remove fedora incompatible values
sed -i 's/@PCSX2_MENU_CATEGORIES@/Game;Emulator;GTK;/g' linux_various/PCSX2.desktop.in

sed \
  -e 's|/usr/share/fonts/truetype/my_favorite_font_e_g_DejaVu Sans.ttf|%{_fontbasedir}/google-roboto/Roboto-Regular.ttf|' \
  -i pcsx2/GS/GS.cpp

%if 0%{?with_snapshot}
sed -i \
  -e '/PCSX2_GIT_REV/s| ""| "v%{version}-git%{shortcommit}"|g' \
  cmake/Pcsx2Utils.cmake
%endif

cp -pf %{_datadir}/SDL_GameControllerDB/gamecontrollerdb.txt \
  pcsx2/PAD/Linux/res/game_controller_db.txt

sed -e '/ALSA::ALSA/a		rt' -i pcsx2/CMakeLists.txt


%build

# pcsx2 contains cflags that override Fedora cflags, however
# a conservative approach has been taken because to quote upsteam "PCSX2 is not
# an ordinary sofware. Most of the code executed are self-generated by PCSX2
# itself (aka dynamic recompiler/virtual machine). That means 1/ gcc flags
# have no much impact on speed 2/ some gcc flags (used to) crash PCSX2"
# Extensive testing will is therefore needed. See rpmfusion bug #2455

%global _lto_cflags %{nil}
%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//') -fuse-ld=bfd

%cmake \
  -DUSER_CMAKE_LD_FLAGS="-Wl,-z,noexecstack" \
  -DDISABLE_BUILD_DATE:BOOL=TRUE \
  -DPACKAGE_MODE:BOOL=TRUE \
  -DBUILD_REPLAY_LOADERS:BOOL=FALSE \
  -DXDG_STD:BOOL=TRUE \
  -DEGL_API:BOOL=TRUE \
  -DGLSL_API:BOOL=TRUE \
  -DCMAKE_BUILD_STRIP:BOOL=FALSE \
  -DPORTAUDIO_API:BOOL=FALSE \
  -DSDL2_API:BOOL=TRUE \
  -DEXTRA_PLUGINS:BOOL=FALSE \
%if 0%{with native}
  -DDISABLE_ADVANCE_SIMD:BOOL=FALSE \
%else
  -DDISABLE_ADVANCE_SIMD:BOOL=TRUE \
%endif
  -DUSE_LTO:BOOL=FALSE \
  -DUSE_VTUNE:BOOL=FALSE \
  -DUSE_SYSTEM_YAML:BOOL=TRUE \
  -DDISABLE_PCSX2_WRAPPER:BOOL=TRUE \
  -DDISABLE_SETCAP:BOOL=TRUE \
  -DENABLE_TESTS:BOOL=FALSE \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DCMAKE_BUILD_TYPE=Release \
%{nil}

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_bindir}/PCSX2 %{buildroot}%{_bindir}/PCSX2.bin

cat > %{buildroot}%{_bindir}/PCSX2 <<EOF
#!/usr/bin/sh
export GDK_BACKEND=x11
export __GL_THREADED_OPTIMIZATIONS=1
export mesa_glthread=true
export MESA_NO_ERROR=1
exec %{_bindir}/PCSX2.bin
EOF
chmod 0755 %{buildroot}%{_bindir}/PCSX2

mkdir -p %{buildroot}%{_libdir}/PCSX2

# strip extra copies of pdf files, which are now in /doc/pcsx2
rm -rf %{buildroot}/usr/share/doc/P*

# Install icon
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps/
convert linux_various/PCSX2.xpm \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/PCSX2.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert linux_various/PCSX2.xpm -filter Lanczos -resize ${res}x${res} \
    ${dir}/PCSX2.png
done

# Install Desktop file
mv linux_various/PCSX2.desktop.in -f linux_various/PCSX2.desktop
desktop-file-install \
  --dir=%{buildroot}/%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="PCSX2" \
  linux_various/PCSX2.desktop

#strip extra copy of icon file, Wrong place for fedora
rm -rf %{buildroot}/usr/share/pixmaps

# Install man page
mkdir -p %{buildroot}/%{_mandir}/man1
install -p -D -m 644 bin/docs/PCSX2.1 %{buildroot}/%{_mandir}/man1

%find_lang pcsx2_Iconized
%find_lang pcsx2_Main


%files -f pcsx2_Iconized.lang -f pcsx2_Main.lang
%doc bin/docs/Configuration_Guide.pdf bin/docs/PCSX2_FAQ.pdf
%{_bindir}/PCSX2
%{perms_pcsx2} %{_bindir}/PCSX2.bin
%dir %{_libdir}/PCSX2
%{_datadir}/applications/PCSX2.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_mandir}/man1/PCSX2.*
%{_datadir}/PCSX2/


%changelog
* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-137.20210821git94c6814
- Downgrade more

* Sun Nov 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-136.20211005git660c623
- Last snapshot that works well on potatoes

* Tue Oct 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-135.20211026git3705054
- Update

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-133.20211002git6035377
- Last snapshot

* Sat Sep 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-132.20210924git2406ae6
- Bump

* Thu Sep 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-131.20210902gitbb5bfda
- Bump
- Update SSE2 build warnings

* Sun Aug 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-130.20210821git94c6814
- Update

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-129.20210713git21908bd
- Update

* Tue Jul 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-128.20210705git6dd90ae
- Last snapshot

* Tue May 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-127.20210520gite011119
- Bump

* Sun May 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-126.20210430git6a2ed3d
- Update

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-125.20210430git5639273
- Bump

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-124.20210419git6f7890b
- Last snapshot

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-123.20210418git256afa8
- Update

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-122.20210407git05a31bd
- Bump

* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-121.20210323gitbc477e1
- Bump
- BR: libchdr, and patch to support system library

* Mon Mar 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-120.20210307gitb33321d
- Update

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-119.20210228gitf9d96f5
- New snapshot
- SSE4 is needed now by upstream, but a sse4 switch is added to maintain a SSE2
  minimal, for older CPUs that can run some not demanding games

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-118.20210212git7187b88
- Bump

* Thu Feb 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-117.20210204gitd55c611
- Update

* Wed Dec 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-114.20201223git74336d9
- New snapshot
- BR: yaml-cpp

* Sun Nov 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-113.20201128git76c98e7
- Bump

* Fri Nov 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-112.20201113git319287d
- Update
- BR: samplerate

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-111.20201030git7a2c94f
- Bump

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-110.20201021git418974a
- Bump

* Fri Oct  2 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-109.20201002git85c1aca
- New snapshot

* Sat Sep 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-108.20200919gite1ff498
- Bump

* Sat Sep 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-107.20200912git6229b20
- New snapshot

* Mon Aug 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-106.20200830git6f0011a
- New snapshot
- x86_64 support
- native switch

* Tue Aug 18 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-105.20200813git61f3258
- Bump
- EGL
- GTK3

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-104.20200729git95b5ab5
- New snapshot

* Fri Jul 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-103.20200717git30e6a7a
- Bump and test new cmake out of source macros

* Sun Jul 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-102.20200711git257f8b1
- New snapshot
- Copy game_controller_db.txt from sdl_gamecontrollerdb

* Mon Jun 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.7.0-101.20200620git297f91a
- Bump

* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.7.0-100.20200513git94e1635
- New snapshot
- Disable hardening
- Remove execstack

* Tue May 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.6.0-101.20200511git593d948
- Bump

* Thu Mar 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.6.0-100.20200229gitc43b511
- New snapshot

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-108.20200131git69ae598
- New snapshot

* Fri Dec 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-107.20191202git23174f3
- New snapshot
- PR to remove portaudio support, SDL2 do the work already
- Convert and resize icon to png

* Sun Nov 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-106.20191103git3c38087
- New snapshot

* Mon Oct 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-105.20191006gitafde59b
- New snapshot

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-104.20190917git6392f79
- New snapshot

* Sun Aug 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-103.20190818git33571dd
- New snapshot

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-102.20190517gitc6fcf0a
- New snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-101.20190502git079baae
- New snapshot

* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-100.20190411git163fd2b
- chinforpms
- New snapshot
- Make build on Fedora > 30
- Makefile to sanitize

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Sat Jul 28 2018 Sérgio Basto <sergio@serjux.com> - 1.4-10
- Try fix rfbz #4962
- Use the same SDL that wxGTK depends on (F27 SDL, F28 SDL2)

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun May 20 2018 Sérgio Basto <sergio@serjux.com> - 1.4-8
- Try fix f27 (#4775) use compat-wxGTK3-gtk2-devel
- Add BR xz-devel to dectect LibLZMA
- Remove manually-specified variables were not used by the project
- Add DISABLE_ADVANCE_SIMD=TRUE, recomended by upstream
- OpenGL_GL_PREFERENCE=GLVND to not use legacy OpenGL

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Sérgio Basto <sergio@serjux.com> - 1.4-6
- Rebuilt to fix core dump with wxWindow

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 1.4-5
- Rebuild for soundtouch 2.0.0
- Just enable compat-wxGTK3-gtk2, pcsx2 fails to detect wxGTK3
  therefore SDL2 also is disabled, intructions on
  https://github.com/PCSX2/pcsx2/wiki/Installing-on-Linux
- Enable GLSL_API and AVX
- Fix Perl builroot changes.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Sérgio Basto <sergio@serjux.com> - 1.4-2
- Add gcc6 patch

* Thu Feb 11 2016 Giles Birchley <gbirchley@blueyonder.co.uk> -1.4-1
- Build for new release 1.4
- Drop patch pcsx2-1.3.1_fedora_cflags_opts.diff - cflag options now streamlined upstream
- Add dependency for lzma-devel
- Add dependency for libICE-devel
- Remove dependency for Cg
- Remove dependency for libjpeg-turbo-devel
- Remove dependency for package glew-devel
- Add build option to retain WxWidget 2.8 -DWX28_API=TRUE
- Add build option -DGTK3_API=FALSE
- Add build option -DSDL2_API=FALSE
- Add build option -DDISABLE_ADVANCE_SIMD=TRUE
- For now, avoided specifying crosscompile (-DCMAKE_TOOLCHAIN_FILE=cmake/linux-compiler-i386-multilib.cmake) as not sure of rpmfusion guideline on this
- Binary name has been altered to PCSX2 upstream; renamed PCSX2.desktop.in, PCSX2.xpm and PCSX2.1
- Added new launcher script PCSX2-linux.sh

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.1-1
- Updated source to 1.2.1
- Updated patch1 permissions
- Source required modification to remove copyrighted files - added Source1

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.0-1
- Updated source to 1.2
- Updated patch1
- Source required modification to remove copyrighted files - added Source1

* Sat Jul 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-5
- made overlooked change suggested in rpmfusion review (#2455)
- changed requires from libGL-devel/libGLU-devel instead of mesa-libGL-devel

* Sun Jun 30 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-4
- made some minor changes suggested in rpmfusion review (#2455)
- removed backslash in cmake command
- removed pcsx2-1.1.0-fedora_cflags.diff
- replaced patch with pcsx2-1.1.0-fedora_cflags_opts.diff

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-3
- made some minor changes suggested in rpmfusion review (#2455)
- fix URL

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-2
- made some minor changes suggested in rpmfusion review (#2455):
- changed icon install permissions
- changed URL
- changed description line length
- reintroduced %%{version} macro to source0
- removed extra backslash from %%cmake
- changed line indentations so all are single space
- removed -DDOC_DIR from %%cmake
- removed extraneous remove lines

* Sun Jun 09 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-1
- changes following rpmfusion review (#2455).
- removed Group tag.
- updated source to v1.1 (linux fixes) 
- removed pcsx2-1.0.0_helpfile.diff (no longer needed).
- removed pcsx2-1.0.0_fedora_cmake.diff (Fedora<16 is no longer supported).
- removed pcsx2-1.1.0_fedora_gcc.diff as this patch is now applied in 1.1.0 source
- added Requires: hicolor-icon-theme (icons in %%{_datadir}/icons/hicolor/).
- added BuildRequires: libaio-devel (needed for 1.1.0).
- added warning about SSE2 to %%description.
- comment about 64 bit status shortened.
- version from names of docs removed (unversioned in 1.1.0).
- fixed omissions in pcsx2.xpm shebang (fix rpmlint error)
- Use %%{_docdir} instead of %%{_defaultdocdir}.
- removed some docs that were either misplaced or should not be packaged.
- removed specification of CMAKE_INSTALL_PREFIX and CMAKE_VERBOSE_MAKEFILE (%%cmake macro already sets them).
- moved %%find_lang macro to end of %%install.
- moved shell invocation to line following %%post %%postun (fix rpmlint error)

* Mon May 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-2
- further changes to comply with rpmfusion review (#2455):
- libGL-devel/libGLU-devel instead of mesa-libGL-devel
- Remove BuildRequires: libCg (redundant with Cg)
- Use %%{_prefix} instead of /usr for CMAKE install prefix
- add Gregory Hainaut's patch to fix issue with gcc 4.8, for Fedora 19 build
- Changed cmake option of DBUILD_REPLAY_LOADERS to false and changed %%files accrdingly

* Tue Mar 05 2013 Giles Birchley <gbirchey@blueyonder.co.uk>
- bleeding edge build, altered package name
- added pcsx2 as a conflict

* Mon Oct 15 2012 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-1
- Build of official 1.0.0 Release
- Significant modifications to script to comply with Fedora/RPMFusion packaging requirements
- Removed redundant BuildRequires
- Added upstream source
- Added Patch to make CFLAGS compliant
- Changed DCMAKE_BUILD_STRIP to FALSE to allow rpm debug package to be created
- Changed document destination in cmake by specifying DDOC_DIR=
- Changed language detection
- Changed icon and desktop file installation

* Tue Aug 09 2011 Danger Boy <Danger[dot] Boy [at]necac.tv.idl> - 0.9.8.4851-1
- initial build
