%undefine _hardened_build
%undefine _cmake_shared_libs
# Disable LTO. Segfaults.
%global _lto_cflags -fno-lto

%bcond_with ffmpeg
%global with_egl 1
%global with_llvm 0
%global with_sysvulkan 1
%global with_unittests 0

# Add extra RESHDP Edition modifications (as a new binary)
# https://github.com/MoArtis/dolphin
%global with_reshdp 1

%global commit e957ed0809c73417103010f91ba058dd7a96bf86
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210103
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global distributor chinforpms

%global pkgname dolphin
%global vc_url  https://github.com/%{name}/%{pkgname}

Name:           dolphin-emu
Version:        5.0
Release:        127%{?gver}%{?dist}
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

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

%if 0%{?with_sysvulkan}
#Can't be upstreamed as-is, needs rework:
Patch1:         0001-Use-system-headers-for-Vulkan.patch
%endif
#Update soundtouch:
#https://github.com/dolphin-emu/dolphin/pull/8725
Patch2:         0002-soundtounch-update-to-2.1.2.patch
Patch3:         0003-soundtouch-Use-shorts-instead-of-floats-for-samples.patch
Patch4:         0004-soundtounch-disable-exceptions.patch
#This needs to be fixed, I've reverted the patch that breaks minizip
Patch5:         0005-Revert-Externals-Update-minizip-search-path.patch

Patch100:       0001-New-Aspect-ratio-mode-for-RESHDP-Force-fitting-4-3.patch
Patch101:       0001-DSP-interrupt-hack-for-RE-2-and-3.patch
Patch102:       0001-Mask-hack-for-RE3.patch
Patch103:       0001-RESHDP-Edition-label.patch


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(ao)
BuildRequires:  pkgconfig(bluez)
BuildRequires:  pkgconfig(bzip2)
%if 0%{?with_egl}
BuildRequires:  pkgconfig(egl)
%endif
BuildRequires:  pkgconfig(fmt) >= 7.1.0
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libzstd) >= 1.4.0
BuildRequires:  pkgconfig(miniupnpc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(sfml-network)
BuildRequires:  pkgconfig(sfml-system)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
%ifarch x86_64
BuildRequires:  bochs-devel
%endif
%if 0%{?with_llvm}
BuildRequires:  llvm-devel
%endif
BuildRequires:  lzo-devel
BuildRequires:  mbedtls-devel
BuildRequires:  minizip-devel
BuildRequires:  picojson-devel
BuildRequires:  pugixml-devel
BuildRequires:  xxhash-devel
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif
%if 0%{?with_sysvulkan}
BuildRequires:  pkgconfig(glslang) >= 11.0.0
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  vulkan-headers
%endif

BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  hicolor-icon-theme

#Only the following architectures are supported:
ExclusiveArch:  x86_64 armv7l aarch64

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

##Bundled code ahoy
#The following isn't in Fedora yet:
Provides:       bundled(FreeSurround)
Provides:       bundled(imgui) = 1.70
Provides:       bundled(cpp-argparse)
#Is this technically bundled code? Adding this just in case:            
#https://github.com/AdmiralCurtiss/rangeset
Provides:       bundled(rangeset)
#soundtouch cannot be unbundled easily, as it requires compile time changes:
Provides:       bundled(soundtouch) = 2.1.2
#dolphin uses tests not included in upstream gtest (possibly unbundle later):
Provides:       bundled(gtest) = 1.9.0


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

%if 0%{?with_sysvulkan}
  # Fix for newer vulkan/glslang
  sed "s/VK_PRESENT_MODE_RANGE_SIZE_KHR/(VkPresentModeKHR)("`
    `"VK_PRESENT_MODE_FIFO_RELAXED_KHR - VK_PRESENT_MODE_IMMEDIATE_KHR + 1)/" \
    -i.orig Source/Core/VideoBackends/Vulkan/SwapChain.h
  sed "/maxMeshViewCountNV/ a /* .maxDualSourceDrawBuffersEXT = */ 1," \
    -i.orig Source/Core/VideoBackends/Vulkan/ShaderCompiler.cpp
  sed \
    -e "/OSDependent/ a MachineIndependent" \
    -e "/OSDependent/ a GenericCodeGen" -e "/HLSL/d" \
    -i.orig Source/Core/VideoBackends/Vulkan/CMakeLists.txt
%endif


###Remove Bundled:
pushd Externals
rm -rf \
  bzip2 cubeb curl discord-rpc ed25519 enet ffmpeg fmt gettext hidapi \
  libiconv-* liblzma libpng libusb LZO mbedtls miniupnpc minizip OpenAL \
  pugixml Qt SFML MoltenVK  WIL XAudio2_7 xxhash zlib zstd

%if 0%{?with_sysvulkan}
  rm -rf glslang Vulkan
%endif

#Remove Bundled Bochs source and replace with links (for x86 only):
%ifarch x86_64
pushd Bochs_disasm
rm -rf `ls | grep -v 'stdafx' | grep -v 'CMakeLists.txt'`
ln -s %{_includedir}/bochs/* ./
ln -s %{_includedir}/bochs/disasm/* ./
popd
#FIXME: This test fails because we unbundle bochs
sed -i "/x64EmitterTest/d" ../Source/UnitTests/Common/CMakeLists.txt
%else
rm -rf Bochs_disasm
%endif

#Replace bundled picojson with a modified system copy (remove use of throw)
pushd picojson
rm picojson.h
#In master, picojson has build option "PICOJSON_NOEXCEPT", but for now:
sed "s/throw std::.*;/std::abort();/g" %{_includedir}/picojson.h > picojson.h
popd

popd

sed \
  -e "/LTO/s|-flto|-flto=%{_smp_build_ncpus}|g" \
  -i CMakeLists.txt

%if 0%{?with_snapshot}
sed \
  -e 's|GIT_FOUND|GIT_DISABLED|g' \
  -i CMakeLists.txt
%endif


%build
export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

#Script to find xxhash is not implemented, just tell cmake it was found
%cmake \
  -DAPPROVED_VENDORED_DEPENDENCIES=";" \
  -DENABLE_LTO:BOOL=OFF \
  -DXXHASH_FOUND:BOOL=ON \
  -DUSE_SHARED_ENET:BOOL=ON \
  -DENABLE_ANALYTICS:BOOL=OFF \
%if !%{with ffmpeg}
  -DENCODE_FRAMEDUMPS:BOOL=OFF \
%endif
%if !0%{?with_egl}
  -DENABLE_EGL:BOOL=OFF \
%endif
%if !0%{?with_llvm}
  -DENABLE_LLVM:BOOL=OFF \
%endif
%if !0%{?with_unittests}
  -DENABLE_TESTS:BOOL=OFF \
%endif
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DDISTRIBUTOR='%{distributor}' \
  -DDOLPHIN_WC_REVISION:STRING=%{release} \
  -DDOLPHIN_WC_DESCRIBE:STRING=%{version} \
%if 0%{?with_snapshot}
  -DDOLPHIN_WC_BRANCH:STRING=master \
%endif
%{nil}

%if 0%{?with_reshdp}
%cmake_build
mv %{__cmake_builddir}/Binaries/%{name} %{name}-reshdp
mv %{__cmake_builddir}/Binaries/%{name}-nogui %{name}-reshdp-nogui
%endif

patch -p1 -R -i %{P:103}
patch -p1 -R -i %{P:102}
patch -p1 -R -i %{P:101}
%cmake_build


%install
%cmake_install

mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-x11
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/usr/bin/bash
export QT_QPA_PLATFORM=xcb
exec %{_bindir}/%{name}-x11
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

sed -e '/^Exec=/s|=.*$|=%{name}|' \
  -i %{buildroot}/%{_datadir}/applications/%{name}.desktop

echo '.so man6/%{name}.6' > %{buildroot}%{_mandir}/man6/%{name}-x11.6

%if 0%{?with_reshdp}
install -pm0755 %{name}-reshdp %{buildroot}%{_bindir}/%{name}-reshdp-x11
install -pm0755 %{name}-reshdp-nogui %{buildroot}%{_bindir}/

cat > %{buildroot}%{_bindir}/%{name}-reshdp <<EOF
#!/usr/bin/bash
export QT_QPA_PLATFORM=xcb
exec %{_bindir}/%{name}-reshdp-x11
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}-reshdp

cp -p %{buildroot}%{_datadir}/applications/%{name}{,-reshdp}.desktop
sed \
  -e '/^Exec=/s|=.*$|=%{name}-reshdp|' \
  -e '/Name.*=/s|$| (RESHDP Edition)|g' \
 -i %{buildroot}%{_datadir}/applications/%{name}-reshdp.desktop

echo '.so man6/%{name}.6' > %{buildroot}%{_mandir}/man6/%{name}-reshdp.6
echo '.so man6/%{name}.6' > %{buildroot}%{_mandir}/man6/%{name}-reshdp-x11.6
echo '.so man6/%{name}-nogui.6' > %{buildroot}%{_mandir}/man6/%{name}-reshdp-nogui.6

%endif

mkdir -p %{buildroot}%{_udevrulesdir}/
install -pm0644 Data/51-usb-device.rules %{buildroot}%{_udevrulesdir}/

#Install appdata.xml
install -p -D -m 0644 %{SOURCE1} \
  %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml
%find_lang %{name}

%check
%if 0%{?with_unittests}
%cmake_build --target unittests
%endif
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}/%{_datadir}/appdata/*.appdata.xml


%files -f %{name}.lang
%doc Readme.md
%license license.txt Externals/licenses.md
%{_bindir}/%{name}
%{_bindir}/%{name}-x11
%{_mandir}/man6/%{name}.*
%{_mandir}/man6/%{name}-x11.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}/sys/Resources/
%{_datadir}/%{name}/sys/Themes/
%{_datadir}/appdata/*.appdata.xml
%if 0%{?with_reshdp}
%{_bindir}/%{name}-reshdp
%{_bindir}/%{name}-reshdp-x11
%{_datadir}/applications/%{name}-reshdp.desktop
%{_mandir}/man6/%{name}-reshdp.*
%{_mandir}/man6/%{name}-reshdp-x11.*
%endif

%files nogui
%doc Readme.md
%license license.txt Externals/licenses.md
%{_bindir}/%{name}-nogui
%{_mandir}/man6/%{name}-nogui.*
%if 0%{?with_reshdp}
%{_bindir}/%{name}-reshdp-nogui
%{_mandir}/man6/%{name}-reshdp-nogui.*
%endif

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
* Sun Jan 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-127.20210103gite957ed0
- Bump
- Update RESHDP patches and rename executables

* Wed Dec 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-126.20201221git1d489b3
- New snapshot

* Mon Dec 14 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-125.20201214git214ea8f
- Update

* Sat Nov 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-124.20201128gitcf32c4d
- Bump
- fmt >= 7.1.0

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-123.20201106git2acd3ab
- New snapshot

* Thu Oct 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-122.20201021git89b01cd
- Update

* Sun Oct 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-121.20201003git0fe6081
- Bump

* Thu Sep 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-120.20200924git57f14b2
- New snapshot
- System vulkan support fixes from Rawhide

* Mon Sep 14 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-119.20200913giteae6819
- Bump
- Rawhide sync

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-118.20200901gitdb06710
- New snapshot

* Fri Aug 14 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-117.20200811git07a0d44
- Bump

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-116.20200802gitdc8dd5a
- New snapshot

* Thu Jul 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-115.20200716gitc596483
- Bump

* Fri Jul 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-114.20200709git5281efe
- New snapshot

* Sun Jul 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-113.20200705git0dbe8fb
- Bump
- BR: lzma

* Fri Jun 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-112.20200619git03e0d2c
- New snapshot
- Added DSP hack binary

* Sat May 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-111.20200528gitb3c705f
- Bump
- BR: minizip-devel

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
