%undefine _hardened_build

%bcond_with ffmpeg
%global with_egl 1
%global with_llvm 0

%global commit 744abab4787e26282a8c9cf70d513f3d84425a32
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200413
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global distributor chinforpms

%global pkgname dolphin

Name:           dolphin-emu
Version:        5.0
Release:        110%{?gver}%{?dist}
Summary:        GameCube / Wii / Triforce Emulator

Epoch:          1

Url:            https://dolphin-emu.org/
##The project is licensed under GPLv2+ with some notable exceptions
#Source/Core/Common/GL/GLExtensions/* is MIT
#Source/Core/Core/HW/Sram.h is zlib
#Source/Core/Common/GekkoDisassembler.* is BSD (2 clause)
##The following is BSD (3 clause):
#dolphin-5.0/Source/Core/Common/SDCardUtil.cpp
#dolphin-5.0/Source/Core/Common/BitField.h
#dolphin-5.0/Source/Core/Core/IPC_HLE/l2cap.h
#dolphin-5.0/Source/Core/Core/IPC_HLE/hci.h
#dolphin-5.0/Source/Core/VideoBackends/Software/Clipper.cpp
#dolphin-5.0/Source/Core/AudioCommon/aldlist.cpp
##Any code in Externals has a license break down in Externals/licenses.md
License:        GPLv2+ and LGPLv2+ and BSD and MIT and zlib

# Use Makefile do download
%if 0%{?with_snapshot}
Source0:        %{pkgname}-%{shortcommit}.tar.xz
%else
Source0:        %{pkgname}-%{version}.tar.xz
%endif
Source1:        %{name}.appdata.xml


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(ao)
BuildRequires:  pkgconfig(bluez)
%if 0%{?with_egl}
BuildRequires:  pkgconfig(egl)
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(miniupnpc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(sfml-network)
BuildRequires:  pkgconfig(sfml-system)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
#BuildRequires:  bochs-devel
BuildRequires:  hidapi-devel
%if 0%{?with_llvm}
BuildRequires:  llvm-devel
%endif
BuildRequires:  lzo-devel
BuildRequires:  mbedtls-devel
BuildRequires:  minizip-compat-devel
BuildRequires:  pugixml-devel
BuildRequires:  xxhash-devel
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif

BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  hicolor-icon-theme

#Only the following architectures are supported:
ExclusiveArch:  x86_64 armv7l aarch64

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(soundtouch) = 1.9.2
Provides:       bundled(fmt) = 5.3.0


#Most of below is taken bundled spec file in source#
%description
Dolphin is a Gamecube, Wii and Triforce (the arcade machine based on the
Gamecube) emulator, which supports full HD video with several enhancements such
as compatibility with all PC controllers, turbo speed, networked multiplayer,
and more.
Most games run perfectly or with minor bugs.


%package nogui
Summary:        Dolphin Emulator without a graphical user interface
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

%description nogui
Dolphin Emulator without a graphical user interface.


%package data
Summary:        Dolphin Emulator data files
BuildArch:      noarch

%description data
This package provides the data files for dolphin-emu.

####################################################

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

#Allow building with cmake macro
sed -i '/CMAKE_C.*_FLAGS/d' CMakeLists.txt

#Font license, just making things more generic
sed 's| this directory | %{name}/Sys/GC |g' \
    Data/Sys/GC/font-licenses.txt > font-licenses.txt

###Remove Bundled:
pushd Externals
rm -rf \
  cubeb curl discord-rpc ed25519 enet ffmpeg gettext gtest hidapi libiconv-* \
  libpng libusb LZO mbedtls miniupnpc minizip OpenAL pugixml Qt SFML MoltenVK \
  XAudio2_7 xxhash zlib

#Remove Bundled Bochs source and replace with links:
#cd Bochs_disasm
#rm -rf `ls | grep -v 'stdafx' | grep -v 'CMakeLists.txt'`
#ln -s %{_includedir}/bochs/* ./
#ln -s %{_includedir}/bochs/disasm/* ./
popd

sed \
  -e "/LTO/s|-flto|-flto=%{_smp_build_ncpus}|g" \
  -e '/-flto=4/a\  check_and_add_flag(LTO)' \
  -i CMakeLists.txt

%if 0%{?with_snapshot}
sed -i \
  -e 's|GIT_FOUND|GIT_DISABLED|g' \
  CMakeLists.txt
%endif


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}

#Script to find xxhash is not implemented, just tell cmake it was found
%cmake .. \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DENABLE_LTO:BOOL=OFF \
  -DXXHASH_FOUND:BOOL=ON \
  -DUSE_SHARED_ENET:BOOL=ON \
%if !%{with ffmpeg}
  -DENCODE_FRAMEDUMPS:BOOL=OFF \
%endif
%if !0%{?with_egl}
  -DENABLE_EGL:BOOL=OFF \
%endif
%if !0%{?with_llvm}
  -DENABLE_LLVM:BOOL=OFF \
%endif
  -DENABLE_TESTS:BOOL=OFF \
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DDISTRIBUTOR='%{distributor}' \
  -DDOLPHIN_WC_REVISION:STRING=%{release} \
  -DDOLPHIN_WC_DESCRIBE:STRING=%{version} \
%if 0%{?with_snapshot}
  -DDOLPHIN_WC_BRANCH:STRING=master \
%endif
%{nil}

%make_build

popd

%install
%make_install -C %{_target_platform}

mkdir -p %{buildroot}%{_udevrulesdir}/
install -pm0644 Data/51-usb-device.rules %{buildroot}%{_udevrulesdir}/

#Install appdata.xml
install -p -D -m 0644 %{SOURCE1} \
  %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml
%find_lang %{name}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}/%{_datadir}/appdata/*.appdata.xml


%files -f %{name}.lang
%doc Readme.md
%license license.txt
%{_bindir}/%{name}
%{_mandir}/man6/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}/sys/Resources/
%{_datadir}/%{name}/sys/Themes/
%{_datadir}/appdata/*.appdata.xml

%files nogui
%doc Readme.md
%license license.txt
%{_bindir}/%{name}-nogui
%{_mandir}/man6/%{name}-nogui.*

%files data
%doc Readme.md docs/gc-font-tool.cpp
%license license.txt font-licenses.txt
#For the gui package:
%exclude %{_datadir}/%{name}/sys/Resources/
%exclude %{_datadir}/%{name}/sys/Themes/
#Already packaged:
%exclude %{_datadir}/%{name}/sys/GC/font-licenses.txt
%{_datadir}/%{name}/
%{_udevrulesdir}/*.rules


%changelog
* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-110.20200316git0b91ea2
- New snapshot
- BR: minizip-compat-devel

* Wed Feb 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-109.20200225git459b472
- Bump

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-108.20200131git69ee15e
- New snapshot

* Sun Jan 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-107.20200105gitf35f4f2
- New snapshot

* Sun Dec 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-106.20191221git8a50d9c
- New snapshot
- Disable system bochs-devel

* Sun Nov 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-105.20191102git0f4c971
- New snapshot

* Mon Aug 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-104.20190825git755601c
- New snapshot

* Tue Jul 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-103.20190729gitdea2b9c
- New snapshot

* Tue Jul 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-102.20190630git0a7395b
- New snapshot

* Thu May 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-101.20190530git00ecfb3
- New snapshot

* Fri Apr 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-100.20190416git5c5e6df
- Snapshot
- chinforpms

* Sun Feb 10 2019 Kalev Lember <klember@redhat.com> - 5.0-27
- Rebuilt for miniupnpc soname bump

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 27 2018 Morten Stevens <mstevens@fedoraproject.org> - 5.0-25
- Rebuilt for mbed TLS 2.13.0

* Mon Aug 20 2018 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-24
- Fix for soundtouch 2.0.0-5 onwards

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Robert Scheck <robert@fedoraproject.org> - 5.0-22
- Rebuilt for mbed TLS 2.9.0 (libmbedcrypto.so.2)

* Wed Mar 07 2018 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-21
- Unbundle xxhash

* Mon Feb 19 2018 Robert Scheck <robert@fedoraproject.org> - 5.0-20
- Rebuilt for mbed TLS 2.7.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.0-18
- Remove obsolete scriptlets

* Sun Oct 15 2017 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-17
- Rebuild with gtk2, since it's been merged into wxGTK3
- Cleanup unnecessary walyand script due to gtk2, closer to upstream now

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 8 2017 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-14
- Rework and rebuild for bochs 2.6.9

* Sun May 7 2017 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-13
- Fix launcher script issues

* Wed Feb 15 2017 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-12
- Rebuilt SFML 2.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 4 2017 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-10
- Add launch scripts for seemless xwayland support
- Revert workaround in desktop file
- Use check macro
- Enable LTO

* Tue Jan 3 2017 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-9
- Workaround for wayland (force x11 for GUI)

* Thu Dec 22 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-8
- Appdata fixes

* Fri Dec 9 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-7
- Add appdata

* Tue Dec 6 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-6
- License fixes with added breakdown
- Split out common data into data subpackage

* Mon Dec 5 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-5
- Revert patch for curl 7.50
- Spec cleanup and fixes
- Add a patch for f26+

* Mon Jul 25 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-4
- Patch for curl 7.50

* Mon Jul 25 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-3
- Added systemd-devel as build require
- Rebuild for miniupnpc-2.0

* Thu Jul 7 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-2
- Added patch for building with mbedtls 2.3+

* Fri Jun 24 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-1
- Update to 5.0

* Thu Mar 24 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-0.2rc
- Update manpages to upstream
- Disable hardened build (breaks dolphin)

* Thu Mar 3 2016 Jeremy Newton <alexjnewt at hotmail dot com> - 5.0-0.1rc
- Update to 5.0rc
- Updated manpage

* Thu Nov 12 2015 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-10
- Patch for mbedtls updated for 2.0+ (f23+)

* Thu Nov 12 2015 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-9
- Patch for X11 for f22+
- Patch for mbedtls (used to be polarssl, fixes check)
- Changed the source download link (migrated to github)

* Mon Jul 20 2015 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-8
- Disabling polarssl check, as its not working on buildsys

* Sun Jun 14 2015 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-7
- Patching for the rename of polarssl

* Tue Dec 9 2014 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-6
- Patching for GCC 4.9

* Sat Dec 6 2014 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-5
- Line got deleted by accident, build fails

* Mon Oct 27 2014 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-4
- Change in wxGTK3-devel file
- Remove unnecessary CG requirement

* Thu Oct 2 2014 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-3
- Use polarssl 1.3 (fedora 21+) to avoid bundling
- patch to use entropy functionality in SSL instead of havege

* Thu Oct 2 2014 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-2
- Bundle polarssl (temporary fix, only for F19/20)

* Mon Mar 3 2014 Jeremy Newton <alexjnewt at hotmail dot com> - 4.0-1
- Update to dolphin 4.0.2
- Removed any unnecessary patches
- Added new and updated some old patches
- Removed exclusive arch, now builds on arm

* Wed Jan 1 2014 Jeremy Newton <alexjnewt at hotmail dot com> - 3.5-6
- Build for SDL2 (Adds vibration support)

* Mon Nov 18 2013 Jeremy Newton <alexjnewt at hotmail dot com> - 3.5-5
- Added patch for SFML, thanks to Hans de Goede

* Sat Jul 27 2013 Jeremy Newton <alexjnewt at hotmail dot com> - 3.5-4
- Updated for SFML compat

* Fri Jul 26 2013 Jeremy Newton <alexjnewt at hotmail dot com> - 3.5-3
- GCC 4.8 Fix (Fedora 19 and onwards)

* Tue Feb 19 2013 Jeremy Newton <alexjnewt at hotmail dot com> - 3.5-2
- Fixed date typos in SPEC

* Tue Feb 19 2013 Jeremy Newton <alexjnewt at hotmail dot com> - 3.5-1
- Updated to latest stable: removed GCC patch, updated CLRun patch
- Added patch to build on wxwidgets 2.8 (temporary workaround)

* Sat Feb 16 2013 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-12
- Removed patch for libav and disabled ffmpeg, caused rendering issues
- Minor consistency fixes to SPEC file

* Fri Dec 14 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-11
- Added patch for recent libav api change in fc18, credit to Xiao-Long Chen
- Renamed patch 1 for consistency

* Mon Jun 25 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-10
- Changed CLRun buildrequire package name
- Renamed GCC 4.7 patch to suit fedora standards
- Added missing hicolor-icon-theme require

* Sat Jun 02 2012 Xiao-Long Chen <chenxiaolong@cxl.epac.to> - 3.0-9
- Add patch to fix build with gcc 4.7.0 in fc17

* Thu Apr 5 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-8
- Removed bundled CLRun

* Tue Mar 13 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-7
- Removed bundled bochs
- Fixed get-source-from-git.sh: missing checkout 3.0

* Fri Feb 24 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-6
- Removed purposeless zerolength file
Lots of clean up and additions, thanks to Xiao-Long Chen:
- Added man page
- Added script to grab source
- Added copyright file
- Added ExclusiveArch
- Added Some missing dependencies

* Thu Feb 23 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-5
- Fixed Licensing
- Split sources and fixed source grab commands

* Fri Jan 27 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-4
- Tweaked to now be able to encode frame dumps

* Sun Jan 22 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-3
- Building now uses cmake macro
- Turned off building shared libs
- Removed unnecessary lines
- Fixed debuginfo-without-sources issue
- Reorganization of the SPEC for readability

* Thu Jan 12 2012 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-2
- Fixed up spec to Fedora Guidelines
- Fixed various trivial mistakes
- Added SOIL and SFML to dependancies
- Removed bundled SOIL and SFML from source spin

* Sun Dec 18 2011 Jeremy Newton <alexjnewt at hotmail dot com> - 3.0-1
- Initial package SPEC created
