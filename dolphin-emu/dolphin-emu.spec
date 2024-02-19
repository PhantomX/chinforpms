%undefine _hardened_build
%undefine _cmake_shared_libs
# Disable LTO. Segfaults.
%global _lto_cflags -fno-lto

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%bcond_without ffmpeg
%bcond_without egl
%bcond_with enet
%bcond_with fmt
%bcond_with llvm
%bcond_with vulkan
%bcond_with unittests

#JIT is only supported on x86_64 and aarch64:
%ifarch x86_64 aarch64
%global enablejit 1
%endif

%global commit 982ad933559be802db81078eda8c9cdd892944c5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240217
%bcond_without snapshot

%global commit2 50b4d5389b6a06f86fb63a2848e1a7da6d9755ca
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 SPIRV-Cross

%global commit3 498e20dfd1343d99b9115201034bb0219801cdec
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 VulkanMemoryAllocator

%global commit4 cc5e1daa5c7f2335a9460ae79c829011dc5cef2d
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 implot

%global commit5 d9e990e6d13527532b7e2bb23164a1f3b7f33bb5
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 rcheevos

%global commit6 e69e5f977d458f2650bb346dadf2ad30c5320281
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 fmt

%global commit7 2a85cd64459f6ba038d233a634d9440490dbba12
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 enet

%global commit18 c5641f2c22d117da7971504591a8f6a41ece488b
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 tinygltf

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global enet_ver 1.3.18
%global fmt_ver 10.2.1

%global distributor chinforpms

%global pkgname dolphin
%global vc_url  https://github.com/%{name}/%{pkgname}

# Rev number - 20413
%global baserelease 41542
%global sbuild %( echo $(( %{baserelease} - 20413 )) )

Name:           dolphin-emu
Version:        5.0.%{sbuild}
Release:        1%{?dist}
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
License:        GPL-2.0-or-later AND LGPLv2+ AND BSD-2-Clause AND BSD-3-Clause AND MIT AND Zlib

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml
Source2:        https://github.com/KhronosGroup/SPIRV-Cross/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/epezent/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/RetroAchievements/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%if %{without fmt}
Source6:       https://github.com/fmtlib/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
%endif
%if %{without enet}
Source7:       https://github.com/lsalzman/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
%endif
Source18:      https://github.com/syoyo/%{srcname18}/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz

%if %{with vulkan}
#Can't be upstreamed as-is, needs rework:
Patch1:         0001-Use-system-headers-for-Vulkan.patch
%endif
Patch11:        0001-system-library-support.patch

Patch100:       0001-New-Aspect-ratio-mode-for-RESHDP-Force-fitting-4-3.patch


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(ao)
BuildRequires:  pkgconfig(bluez)
BuildRequires:  pkgconfig(bzip2)
%if %{with egl}
BuildRequires:  pkgconfig(egl)
%endif
%if %{with fmt}
BuildRequires:  pkgconfig(fmt) >= %{fmt_ver}
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(libcurl)
%if %{with enet}
BuildRequires:  pkgconfig(libenet) >= %{enet_ver}
%endif
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(spng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libzstd) >= 1.4.0
BuildRequires:  mgba-devel
BuildRequires:  pkgconfig(miniupnpc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(sdl2) >= 2.26.0
BuildRequires:  pkgconfig(sfml-network)
BuildRequires:  pkgconfig(sfml-system)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib-ng)
%if %{with llvm}
BuildRequires:  llvm-devel
%endif
BuildRequires:  lzo-devel
BuildRequires:  mbedtls-devel >= 2.28.0
BuildRequires:  minizip-ng-devel
BuildRequires:  picojson-devel
BuildRequires:  pugixml-devel
BuildRequires:  vulkan-headers
BuildRequires:  xxhash-devel
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif
%if %{with vulkan}
BuildRequires:  pkgconfig(glslang) >= 11.0.0
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools
BuildRequires:  pkgconfig(SPIRV-Tools)
%else
#This is hard to unbundle and is unmaintainable with little benefit:
Provides:       bundled(glslang)
%endif

BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  hicolor-icon-theme

#Only the following architectures are supported (64bit little endian only):
ExclusiveArch:  x86_64 aarch64 ppc64le

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

##Bundled code ahoy
#The following isn't in Fedora yet:
Provides:       bundled(FreeSurround)
Provides:       bundled(imgui) = 1.89.7
Provides:       bundled(cpp-argparse)
#Is this technically bundled code? Adding this just in case:            
#https://github.com/AdmiralCurtiss/rangeset
Provides:       bundled(rangeset)
#soundtouch cannot be unbundled easily, as it requires compile time changes:
Provides:       bundled(soundtouch) = 2.3.2
#dolphin uses a very old bochs, which is impatible with f35+'s bochs.
#We could rework dolphin to use latest, but this requires a lot of work.
#Furthermore, the dolphin gtest test cases that fail with f33/34 bochs
#My best guess is that this is 2.6.6, as dolphin does not specify
Provides:       bundled(bochs) = 2.6.6
Provides:       bundled(FatFS) = 86631
Provides:       bundled(implot) = 0~git%{shortcommit4}
Provides:       bundled(rcheevos) = 0~git%{shortcommit5}
Provides:       bundled(spirv-cross) = 0~git%{shortcommit2}
%if %{without enet}
Provides:       bundled(enet) = %{enet_ver}
%endif
%if %{without fmt}
Provides:       bundled(fmt) = %{fmt_ver}
%endif

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


%package tool
Summary:        Dolphin Emulator CLI utility

%description tool
This package provides "dolphin-tool", which is a CLI-based utility for
functions such as managing disc images.


%package data
Summary:        Dolphin Emulator data files
BuildArch:      noarch

%description data
This package provides the data files for dolphin-emu.


####################################################

%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -N -p1
%autopatch -M 500 -p1

#Allow building with cmake macro
sed -i '/CMAKE_C.*_FLAGS/d' CMakeLists.txt

#Font license, just making things more generic
sed 's| this directory | %{name}/Sys/GC |g' \
    Data/Sys/GC/font-licenses.txt > font-licenses.txt

# Fix for newer vulkan/glslang
sed "s/VK_PRESENT_MODE_RANGE_SIZE_KHR/(VkPresentModeKHR)("`
  `"VK_PRESENT_MODE_FIFO_RELAXED_KHR - VK_PRESENT_MODE_IMMEDIATE_KHR + 1)/" \
  -i.orig Source/Core/VideoBackends/Vulkan/VKSwapChain.h

%if %{with vulkan}
  sed "/maxMeshViewCountNV/ a /* .maxDualSourceDrawBuffersEXT = */ 1," \
    -i.orig Source/Core/VideoBackends/Vulkan/ShaderCompiler.cpp
  sed \
    -e "/OSDependent/ a MachineIndependent" \
    -e "/OSDependent/ a GenericCodeGen" -e "/HLSL/d" \
    -i.orig Source/Core/VideoBackends/Vulkan/CMakeLists.txt
%endif

#This test fails without JIT enabled:
#https://bugs.dolphin-emu.org/issues/12421
%if ! 0%{?enablejit}
sed -i "/PageFaultTest/d" Source/UnitTests/Core/CMakeLists.txt
%endif

###Remove Bundled:
pushd Externals
rm -rf \
  bzip2 cubeb curl discord-rpc ed25519 ffmpeg gettext gtest hidapi \
  libiconv-* liblzma libspng libusb lz4 LZO mbedtls mGBA miniupnpc minizip OpenAL \
  pugixml Qt SFML MoltenVK  WIL XAudio2_7 xxhash zlib-ng zstd Vulkan

%if %{with vulkan}
  rm -rf glslang
%endif

tar -xf %{S:2} -C spirv_cross/SPIRV-Cross --strip-components 1
tar -xf %{S:3} -C VulkanMemoryAllocator/ --strip-components 1
tar -xf %{S:4} -C implot/implot --strip-components 1
tar -xf %{S:5} -C rcheevos/rcheevos --strip-components 1
%if %{without fmt}
tar -xf %{S:6} -C fmt/fmt --strip-components 1
%else
rm -rf fmt
%endif
%if %{without enet}
tar -xf %{S:7} -C enet/enet --strip-components 1
%else
rm -rf enet
%endif
tar -xf %{S:18} -C tinygltf/tinygltf --strip-components 1

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

%if %{with snapshot}
sed \
  -e 's|GIT_FOUND|GIT_DISABLED|g' \
  -e 's|${DOLPHIN_VERSION_MAJOR}.${DOLPHIN_VERSION_MINOR}|%{version}|g' \
  -e 's|${DOLPHIN_WC_DESCRIBE} (no further info)|%{release}|g' \
  -i CMakeLists.txt CMake/ScmRevGen.cmake
%endif


%build
#Script to find xxhash is not implemented, just tell cmake it was found
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DAPPROVED_VENDORED_DEPENDENCIES=";" \
  -DENABLE_LTO:BOOL=OFF \
  -DXXHASH_FOUND:BOOL=ON \
  %{?!enablejit:-DENABLE_GENERIC=ON} \
  -DUSE_SHARED_ENET:BOOL=ON \
  -DENABLE_CLI_TOOL:BOOL=ON \
  -DENABLE_ANALYTICS:BOOL=OFF \
  -DENABLE_AUTOUPDATE:BOOL=OFF \
%if %{without ffmpeg}
  -DENCODE_FRAMEDUMPS:BOOL=OFF \
%endif
%if %{without egl}
  -DENABLE_EGL:BOOL=OFF \
%endif
%if %{without enet}
  -DUSE_SYSTEM_ENET:BOOL=OFF \
%endif
%if %{without fmt}
  -DUSE_SYSTEM_FMT:BOOL=OFF \
%endif
%if %{without llvm}
  -DENABLE_LLVM:BOOL=OFF \
%endif
%if %{without unittests}
  -DENABLE_TESTS:BOOL=OFF \
%endif
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  -DDISTRIBUTOR='%{distributor}' \
%{nil}

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-x11
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/bash
export QT_QPA_PLATFORM=xcb
exec %{_bindir}/%{name}-x11 "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

sed -e '/^Exec=/s|=.*$|=%{name}|' \
  -i %{buildroot}/%{_datadir}/applications/%{name}.desktop

echo '.so man6/%{name}.6' > %{buildroot}%{_mandir}/man6/%{name}-x11.6

mkdir -p %{buildroot}%{_udevrulesdir}/
install -pm0644 Data/51-usb-device.rules %{buildroot}%{_udevrulesdir}/

#Install appdata.xml
install -p -D -m 0644 %{SOURCE1} \
  %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
%find_lang %{name}

%check
%if %{with unittests}
%cmake_build --target unittests
%endif
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/*.appdata.xml


%files -f %{name}.lang
%doc Readme.md
%license COPYING Data/license.txt Externals/licenses.md
%{_bindir}/%{name}
%{_bindir}/%{name}-x11
%{_mandir}/man6/%{name}.*
%{_mandir}/man6/%{name}-x11.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}/sys/Resources/
%{_datadir}/%{name}/sys/Themes/
%{_metainfodir}/*.appdata.xml

%files nogui
%doc Readme.md
%license COPYING Data/license.txt Externals/licenses.md
%{_bindir}/%{name}-nogui
%{_mandir}/man6/%{name}-nogui.*

%files data
%doc Readme.md docs/gc-font-tool.cpp
%license COPYING Data/license.txt font-licenses.txt
#For the gui package:
%exclude %{_datadir}/%{name}/sys/Resources/
%exclude %{_datadir}/%{name}/sys/Themes/
#Already packaged:
%exclude %{_datadir}/%{name}/sys/GC/font-licenses.txt
%{_datadir}/%{name}/
%{_udevrulesdir}/*.rules

%files tool
%license COPYING Data/license.txt
%{_bindir}/dolphin-tool


%changelog
* Wed Jun 07 2023 Phantom X <megaphantomx at hotmail dot com> - 1:5.0.19552-1.20230607git44d9304
- Use upstream version scheme

* Thu May 18 2023 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-178.20230517git11768e3
- Qt6

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-176.20230315git91fca07
- gcc 13 build fix

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-163.20220715git1da24f6
- Update
- BR: png -> spng
- BR: zlib -> zlib-ng

* Mon Jul 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-161.20220702gitd625c61
- Bump
- Remove RESHDP modifications
- Remove -D_GLIBCXX_ASSERTIONS for the time

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-160.20220617git23ed611
- Update

* Thu May 19 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-159.20220517git6260166
- Bump
- Rawhide sync (SoundTouch 2.3.1)

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-158.20220424git4cd48e6
- Bump

* Sun Apr 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-157.20220410git1f4df1d
- Update

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-156.20220315gitbf261f6
- Bump

* Wed Mar 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-155.20220302gitd32c720
- Last snapshot

* Sat Feb 12 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-154.20220211git466bb17
- Bump

* Sat Jan 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-153.20220120git7b8e846
- Update

* Sun Jan 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-152.20220108git94ad33c
- Last snapshot

* Sat Dec 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-151.20211225gita29d762
- Bump

* Sun Dec 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-150.20211210gitbfddce4
- Update
- New tools package

* Wed Nov 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-149.20211123gitaa5cb35
- Bump

* Mon Nov 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-148.20211107gitaa6db1e
- Last snapshot

* Thu Oct 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-147.20211027git7558da2
- Update

* Tue Oct 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-146.20211012git6987ea0
- Bump

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-145.20210930git890a5ed
- Last snapshot
- Fedora sync (bundle glslang again)

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-144.20210916gitd14d759
- Last snapshot

* Sun Aug 15 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-143.20210815git4c179fe
- Update

* Mon Jul 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-142.20210725git7fe97b2
- Last snapshot
- BR: mgba

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-141.20210714git9b17805
- Bump

* Sat Jul 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-140.20210630git2409d30
- Update

* Tue Jun 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-139.20210622gitbe2ec72
- New snapshot

* Sat May 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-138.20210529gitb3a414e
- Bump

* Mon May 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-137.20210509giteb5cd9b
- Update

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-136.20210501git1f26b69
- Bump

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-135.20210419git4d37dad
- Update
- Drop now unneeded DSP interrupt hack

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-134.20210407git5322256
- Bump

* Thu Apr 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-133.20210401gita2fa9aa
- Last snapshot

* Mon Mar 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-132.20210307git72a6fff
- Update

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-131.20210226git9d0983c
- New snapshot

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-130.20210212gitc5ee86c
- Update

* Thu Feb 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-129.20210204gitabc5d6c
- Bump

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:5.0-128.20210121gitcaff472
- Latest snapshot

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
