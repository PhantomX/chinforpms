%global commit 3d28f9d362e6d9871747231b210c559536bb6dd4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230629
%bcond_with snapshot

%define _fortify_level 0

# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%undefine _auto_set_build_flags
%undefine _package_note_file

# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%global _lto_cflags %{nil}


%global winearchdir %{nil}
%global winesodir %{nil}
%ifarch %{ix86}
%global winearchdir i386-windows
%global winesodir i386-unix
%endif
%ifarch x86_64
%global winearchdir x86_64-windows
%global winesodir x86_64-unix
%endif
%ifarch arm
%global winearchdir arm-windows
%global winesodir arm-unix
%endif
%ifarch aarch64
%global winearchdir aarch64-windows
%global winesodir aarch64-unix
%global __brp_llvm_compile_lto_elf %nil
%global __brp_strip_lto %nil
%global __brp_strip_static_archive %nil
%endif

%ifarch %{ix86} x86_64
%global wine_mingw 1
# Package mingw files with debuginfo
%global with_debug 0
%endif
%global no64bit   0
%global winefastsync 5.16
%global winegecko 2.47.4
%global winemono  8.0.0
%global winevulkan 1.3.258

%global wineFAudio 23.03
%global winegsm 1.0.19
%global winejpeg 9e
%global winelcms2 2.15
%global winempg123 1.31.1
%global winepng 1.6.39
%global wineopenldap 2.5.14
%global winetiff 4.5.0
%global winejxrlib 1.1
%global winevkd3d 1.8
%global winexml2 2.11.4
%global winexslt 1.1.38
%global winezlib 1.2.13
%global winezydis 4.0.0

%global _default_patch_fuzz 2

%global libext .so
%global winedlldir %{winesodir}

%if 0%{?wine_mingw}
%undefine _annotated_build
%global libext %{nil}
%global winedlldir %{winearchdir}
%endif

%global wineacm acm%{?libext}
%global wineax ax%{?libext}
%global winecom com%{?libext}
%global winecpl cpl%{?libext}
%global winedll dll%{?libext}
%global winedll16 dll16%{?libext}
%global winedrv drv%{?libext}
%global winedrv16 drv16%{?libext}
%global wineds ds%{?libext}
%global wineexe exe%{?libext}
%global wineexe16 exe16%{?libext}
%global winemod16 mod16%{?libext}
%global wineocx ocx%{?libext}
%global winesys sys%{?libext}
%global winetlb tlb%{?libext}
%global winevxd vxd%{?libext}
%global winemsstyles msstyles%{?libext}

# build with staging-patches, see:  https://wine-staging.com/
# 1 to enable; 0 to disable.
%global wine_staging 1
%global wine_stagingver 8.13
%global wine_stg_url https://gitlab.winehq.org/wine/wine-staging
%if 0%(echo %{wine_stagingver} | grep -q \\. ; echo $?) == 0
%global strel v
%global stpkgver %{wine_stagingver}
%else
%global stpkgver %(c=%{wine_stagingver}; echo ${c:0:7})
%endif
%global ge_id a2fbe5ade7a8baf3747ca57b26680fee86fff9f0
%global ge_url https://github.com/GloriousEggroll/proton-ge-custom/raw/%{ge_id}/patches

%global tkg_id 57fa14541affdc1d7f9799fda9befdeb8f72be0b
%global tkg_url https://github.com/Frogging-Family/wine-tkg-git/raw/%{tkg_id}/wine-tkg-git/wine-tkg-patches
%global tkg_cid 51c8597825c2d86c5d2c912ff2a16adde64b23c1
%global tkg_curl https://github.com/Frogging-Family/community-patches/raw/%{tkg_cid}/wine-tkg-git

%if 0%{?wine_staging}
%global cap_st cap_sys_nice,
%endif

%global perms_pldr %caps(cap_net_raw+eip)
%global perms_srv %caps(%{?cap_st}cap_net_raw+eip)

# childwindow
%bcond_without childwindow
# fastsync/winesync
%bcond_without fastsync
# proton FS hack (wine virtual desktop with DXVK is not working well)
%bcond_with fshack
# Shared gpu resources
%bcond_with sharedgpures

%if %{with fshack}
%global wine_staging_opts %{?wine_staging_opts} -W winex11-WM_WINDOWPOSCHANGING -W winex11-_NET_ACTIVE_WINDOW
%endif

%global whq_url  https://source.winehq.org/git/wine.git/patch
%global whq_murl  https://gitlab.winehq.org/wine/wine
%global whqs_url  https://source.winehq.org/patches/data
%global valve_url https://github.com/ValveSoftware/wine

%global staging_banner Chinforpms Staging

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global vermajor %%(echo %%{ver} | cut -d. -f1)
%global verminor %%(echo %%{ver} | cut -d. -f2 | cut -d- -f1)

Name:           wine
# If rc, use "~" instead "-", as ~rc1
Version:        8.13
Release:        100%{?dist}
Summary:        A compatibility layer for windows applications

Epoch:          1

License:        LGPL-2.1-or-later AND BSD-2-Clause AND BSD-3-Clause AND libtiff AND MIT AND OLDAP-2.8 AND Zlib
URL:            http://www.winehq.org/

%if %{with snapshot}
Source0:        %{whq_murl}/-/archive/%{commit}/%{name}-%{shortcommit}.tar.bz2
%else
%if "%{verminor}" == "0"
%global verx 1
%endif
Source0:        https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz
Source10:       https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz.sign
%endif

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source6:        wine-README-chinforpms
Source7:        wine-README-chinforpms-fshack
Source8:        wine-README-chinforpms-fastsync

Source50:       https://raw.githubusercontent.com/KhronosGroup/Vulkan-Docs/v%{winevulkan}/xml/vk.xml#/vk-%{winevulkan}.xml

# desktop files
Source100:      wine-notepad.desktop
Source101:      wine-regedit.desktop
Source102:      wine-uninstaller.desktop
Source103:      wine-winecfg.desktop
Source104:      wine-winefile.desktop
Source105:      wine-winemine.desktop
Source106:      wine-winhelp.desktop
Source107:      wine-wineboot.desktop
Source108:      wine-wordpad.desktop
Source109:      wine-oleview.desktop
Source110:      wine-iexplore.desktop
Source111:      wine-inetcpl.desktop
Source112:      wine-joycpl.desktop
Source113:      wine-taskmgr.desktop

# AppData files
Source150:      wine.appdata.xml

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

# mime types
Source300:      wine-mime-msi.desktop


# smooth tahoma (#693180)
# disable embedded bitmaps
Source501:      wine-tahoma.conf
# and provide a readme
Source502:      wine-README-tahoma

Patch511:       wine-cjk.patch
Patch599:       0003-winemenubuilder-silence-an-err.patch

# build fixes

# wine bugs/upstream/reverts
#Patch???:      %%{whq_url}/commit#/%%{name}-whq-commit.patch
Patch700:        %{whq_url}/bd89ab3040e30c11b34a95072d88f635ade03bdc#/%{name}-whq-bd89ab3.patch

# wine staging patches for wine-staging
Source900:       %{wine_stg_url}/-/archive/%{?strel}%{wine_stagingver}/wine-staging-%{stpkgver}.tar.bz2

Patch900:       https://bugs.winehq.org/attachment.cgi?id=74866#/%{name}-whq-bug74866.patch
Patch901:        0001-Fix-staging-windows.networking.connectivity.dll.patch

# https://github.com/Tk-Glitch/PKGBUILDS/wine-tkg-git/wine-tkg-patches
Patch1000:       FS_bypass_compositor.patch
Patch1001:       %{tkg_url}/misc/CSMT-toggle/CSMT-toggle.patch#/%{name}-tkg-CSMT-toggle.patch

# fsync
Patch1020:       %{tkg_url}/proton/fsync/fsync-unix-staging.patch#/%{name}-tkg-fsync-unix-staging.patch
Patch1021:       %{tkg_url}/proton/fsync/server_Abort_waiting_on_a_completion_port_when_closing_it.patch#/%{name}-tkg-server_Abort_waiting_on_a_completion_port_when_closing_it.patch
Patch1022:       %{tkg_url}/proton/fsync/fsync_futex_waitv.patch#/%{name}-tkg-fsync_futex_waitv.patch
# FS Hack
Patch1023:       %{tkg_url}/proton/valve_proton_fullscreen_hack/valve_proton_fullscreen_hack-staging.patch#/%{name}-tkg-valve_proton_fullscreen_hack-staging.patch
Patch1024:       %{tkg_url}/misc/childwindow/childwindow-proton.patch#/%{name}-tkg-childwindow-proton.patch
Patch1025:       %{tkg_url}/misc/childwindow/OPWR-proton.patch#/%{name}-tkg-OPWR-proton.patch
Patch1026:       %{tkg_url}/proton/LAA/LAA-unix-staging.patch#/%{name}-tkg-LAA-unix-staging.patch
Patch1027:       %{tkg_url}/proton-tkg-specific/proton-tkg/staging/proton-tkg-staging.patch#/%{name}-tkg-proton-tkg-staging.patch
Patch1028:       %{tkg_url}/proton-tkg-specific/proton-tkg/proton-tkg-additions.patch#/%{name}-tkg-proton-tkg-additions.patch
Patch1029:       %{tkg_url}/proton-tkg-specific/proton-cpu-topology-overrides/proton-cpu-topology-overrides.patch#/%{name}-tkg-proton-cpu-topology-overrides.patch
Patch1030:       %{tkg_url}/proton/proton-win10-default/proton-win10-default.patch#/%{name}-tkg-proton-win10-default.patch
Patch1031:       %{tkg_url}/hotfixes/proton_fs_hack_staging/remove_hooks_that_time_out2.mypatch#/%{name}-tkg-remove_hooks_that_time_out2.patch
Patch1032:       %{tkg_url}/hotfixes/proton_fs_hack_staging/winex11.drv_Add_a_GPU_for_each_Vulkan_device_that_was_not_tied_to_an_XRandR_provider.mypatch#/%{name}-tkg-winex11.drv_Add_a_GPU_for_each_Vulkan_device_that_was_not_tied_to_an_XRandR_provider.patch
Patch1034:       %{tkg_url}/hotfixes/GetMappedFileName/Return_nt_filename_and_resolve_DOS_drive_path.mypatch#/%{name}-tkg-Return_nt_filename_and_resolve_DOS_drive_path.patch
Patch1035:       %{tkg_url}/hotfixes/rdr2/0001-proton-bcrypt_rdr2_fixes6.mypatch#/%{name}-tkg-0001-proton-bcrypt_rdr2_fixes6.patch
Patch1036:       %{tkg_url}/hotfixes/rdr2/0002-bcrypt-Add-support-for-calculating-secret-ecc-keys2.mypatch#/%{name}-tkg-0002-bcrypt-Add-support-for-calculating-secret-ecc-keys2.patch
Patch1037:       %{tkg_url}/hotfixes/rdr2/0003-bcrypt-Add-support-for-OAEP-padded-asymmetric-key-de3.mypatch#/%{name}-tkg-0003-bcrypt-Add-support-for-OAEP-padded-asymmetric-key-de3.patch
Patch1038:       %{tkg_url}/hotfixes/08cccb5/a608ef1.mypatch#/%{name}-tkg-a608ef1.patch
Patch1039:       %{tkg_url}/hotfixes/autoconf-opencl-hotfix/opencl-fixup.mypatch#/%{name}-tkg-opencl-fixup.patch
Patch1040:       %{tkg_url}/hotfixes/NosTale/nostale_mouse_fix.mypatch#/%{name}-tkg-nostale_mouse_fix.patch
Patch1041:       0001-proton-tkg-staging-fixup-1.patch
Patch1042:       0001-proton-tkg-staging-fixup-2.patch

Patch1050:       %{tkg_url}/misc/fastsync/fastsync-staging-protonify.patch#/%{name}-tkg-fastsync-staging-protonify.patch
Patch1051:       0001-fastsync-staging-protonify-fixup-1.patch
Patch1052:       0001-fastsync-staging-protonify-fixup-2.patch

Patch1060:       %{tkg_url}/proton/shared-gpu-resources/sharedgpures-driver.patch#/%{name}-tkg-sharedgpures-driver.patch
Patch1061:       %{tkg_url}/proton/shared-gpu-resources/sharedgpures-textures.patch#/%{name}-tkg-sharedgpures-textures.patch
Patch1062:       %{tkg_url}/proton/shared-gpu-resources/sharedgpures-fixup-staging.patch#/%{name}-tkg-sharedgpures-fixup-staging.patch
Patch1063:       %{tkg_url}/proton/shared-gpu-resources/sharedgpures-fences.patch#/%{name}-tkg-sharedgpures-fences.patch
# https://github.com/Frogging-Family/wine-tkg-git/issues/1005
Patch1064:       0001-sharedgpures-fixup.patch

Patch1089:       %{tkg_curl}/0001-ntdll-Use-kernel-soft-dirty-flags-for-write-watches-.mypatch#/%{name}-tkg-0001-ntdll-Use-kernel-soft-dirty-flags-for-write-watches.patch
Patch1090:       0001-fshack-revert-grab-fullscreen.patch
Patch1091:       %{valve_url}/commit/87a85d50c502f705eeaf7a9f3f4c9e54c707ae56.patch#/%{name}-valve-87a85d5.patch
Patch1092:       %{valve_url}/commit/464a79989b5250a1aa9e6a6e54aa0a334cd523ff.patch#/%{name}-valve-464a799.patch

Patch1300:       nier.patch
Patch1301:       0001-FAudio-Disable-reverb.patch
Patch1302:       0001-staging-update-nvapi-and-nvencodeapi-autoconf.patch
Patch1303:       0011-mfplat-Stub-out-MFCreateDXGIDeviceManager-to-avoid-t.patch
Patch1304:       0001-mfplat-custom-fixes-from-proton.patch

# Patch the patch
Patch5000:      0001-chinforpms-message.patch

# END of staging patches

%if !0%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 aarch64
%else
ExclusiveArch:  %{ix86}
%endif

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  git-core
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
%ifarch aarch64
BuildRequires:  clang >= 5.0
BuildRequires:  lld
%else
BuildRequires:  gcc
%endif
%if 0%{?wine_mingw}
%ifarch %{ix86} x86_64
# mingw-binutils 2.35 or patched 2.34 is needed to prevent crashes
BuildRequires:  mingw32-binutils >= 2.34-100
BuildRequires:  mingw64-binutils >= 2.34-100
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
%endif
%endif
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  fontforge
BuildRequires:  icoutils
BuildRequires:  patchutils
BuildRequires:  perl-generators
BuildRequires:  python3
BuildRequires:  pkgconfig(alsa)
BuildRequires:  cups-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glut)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  fontpackages-devel
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gmp)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  libieee1284-devel
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  librsvg2
BuildRequires:  librsvg2-tools
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(netapi)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  opencl-headers
BuildRequires:  pkgconfig(osmesa)
BuildRequires:  pkgconfig(sane-backends)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
%if %{with childwindow}
BuildRequires:  pkgconfig(xpresent)
%endif
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xxf86dga)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  libappstream-glib

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(libva)
%if 0%{?fastsync}
BuildRequires:  winesync-devel >= %{winefastsync}
%endif
%endif

Requires:       wine-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-desktop = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
Requires:       wine-core(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif
Recommends:     wine-dxvk(x86-32)
Recommends:     dosbox-staging
Recommends:     isdn4k-utils(x86-32)
%if 0%{?fastsync}
Recommends:     winesync >= %{winefastsync}
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       mesa-dri-drivers(x86-64)
%endif
Recommends:     wine-dxvk(x86-64)
Recommends:     dosbox-staging
Recommends:     isdn4k-utils(x86-64)

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mesa-dri-drivers
Requires:       samba-winbind-clients
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       mesa-dri-drivers(aarch-64)
%endif

%description
Wine as a compatibility layer for UNIX to run Windows applications. This
package includes a program loader, which allows unmodified Windows
3.x/9x/NT binaries to run on x86 and x86_64 Unixes. Wine can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the
wine-* sub packages.

%package core
Summary:        Wine core package
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives

# require -filesystem
Requires:       wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch %{ix86}
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-32)
Requires:       freetype(x86-32)
Requires:       nss-mdns(x86-32)
Requires:       gmp(x86-32)
Requires:       gnutls(x86-32)
Requires:       gstreamer1-plugins-good(x86-32)
Requires:       libgcrypt(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXfixes(x86-32)
Requires:       libXi(x86-32)
Requires:       libXinerama(x86-32)
%if %{with childwindow}
Requires:       libXpresent(x86-32)
%endif
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
Requires:       libXxf86vm(x86-32)
Requires:       libpcap(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       samba-libs(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
Requires:       libva(x86-32)
Recommends:     gstreamer1-plugins-ugly(x86-32)
%endif
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       nss-mdns(x86-64)
Requires:       gmp(x86-64)
Requires:       gnutls(x86-64)
Requires:       gstreamer1-plugins-good(x86-64)
Requires:       libgcrypt(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXfixes(x86-64)
Requires:       libXi(x86-64)
Requires:       libXinerama(x86-64)
%if %{with childwindow}
Requires:       libXpresent(x86-64)
%endif
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
Requires:       libXxf86vm(x86-64)
Requires:       libpcap(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       samba-libs(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
Requires:       libva(x86-64)
Recommends:     gstreamer1-plugins-ugly(x86-64)
%endif
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gmp
Requires:       gnutls
Requires:       gstreamer1-plugins-good
Requires:       libgcrypt
Requires:       libXcursor
Requires:       libXfixes
%if %{with childwindow}
Requires:       libXpresent
%endif
Requires:       libXrender
Requires:       libpcap
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       SDL2
Requires:       vulkan-loader
%if 0%{?wine_staging}
Requires:       libva
Recommends:     gstreamer1-plugins-ugly
%endif
%endif

Provides:       bundled(gsm) = %{winegsm}
Provides:       bundled(libFAudio) = %{wineFAudio}
Provides:       bundled(libjpeg) = %{winejpeg}
Provides:       bundled(lcms2) = %{winelcms2}
Provides:       bundled(mpg123) = %{winempg123}
Provides:       bundled(libpng) = %{winepng}
Provides:       bundled(libtiff) = %{winetiff}
Provides:       bundled(jxrlib) = %{winejxrlib}
Provides:       bundled(libxml2) = %{winexml2}
Provides:       bundled(libxslt) = %{winexslt}
Provides:       bundled(libvkd3d) = %{winevkd3d}
Provides:       bundled(openldap) = %{wineopenldap}
Provides:       bundled(zlib) = %{winezlib}
Provides:       bundled(zydis) = %{winezydis}

# removed as of 1.7.35
Obsoletes:      wine-wow < 1.7.35
Provides:       wine-wow = %{?epoch:%{epoch}:}%{version}-%{release}

# removed as of 6.21
Obsoletes:      wine-capi < %{?epoch:%{epoch}:}6.20-101
Provides:       wine-capi = %{?epoch:%{epoch}:}%{version}-%{release}

# removed as of 7.21
Obsoletes:      wine-openal < %{?epoch:%{epoch}:}7.21-100
Provides:       wine-openal = %{?epoch:%{epoch}:}%{version}-%{release}

%description core
Wine core package includes the basic wine stuff needed by all other packages.

%package systemd
Summary:        Systemd config for the wine binfmt handler
Requires:       systemd >= 23
BuildArch:      noarch
Requires(post):  systemd
Requires(postun): systemd
Obsoletes:      wine-sysvinit < %{version}-%{release}

%description systemd
Register the wine binary handler for windows executables via systemd binfmt
handling. See man binfmt.d for further information.

%package filesystem
Summary:        Filesystem directories for wine
BuildArch:      noarch

%description filesystem
Filesystem directories and basic configuration for wine.

%package common
Summary:        Common files
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description common
Common wine files and scripts.

%package desktop
Summary:        Desktop integration features for wine
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-systemd = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package fonts
Summary:       Wine font files
BuildArch:     noarch
# arial-fonts are available with staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-arial-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Obsoletes:     wine-arial-fonts <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:      wine-courier-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-fixedsys-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-small-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-system-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-marlett-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-tahoma-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
# times-new-roman-fonts are available with staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-times-new-roman-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Obsoletes:     wine-times-new-roman-fonts <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:      wine-symbol-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-webdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-wingdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
Requires:      liberation-narrow-fonts

%description fonts
%{summary}

%if 0%{?wine_staging}
%package arial-fonts
Summary:       Wine Arial font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description arial-fonts
%{summary}
%endif

%package courier-fonts
Summary:       Wine Courier font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description courier-fonts
%{summary}

%package fixedsys-fonts
Summary:       Wine Fixedsys font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description fixedsys-fonts
%{summary}

%package small-fonts
Summary:       Wine Small font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description small-fonts
%{summary}

%package system-fonts
Summary:       Wine System font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description system-fonts
%{summary}


%package marlett-fonts
Summary:       Wine Marlett font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description marlett-fonts
%{summary}


%package ms-sans-serif-fonts
Summary:       Wine MS Sans Serif font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description ms-sans-serif-fonts
%{summary}

# rhbz#693180
# http://lists.fedoraproject.org/pipermail/devel/2012-June/168153.html
%package tahoma-fonts
Summary:       Wine Tahoma font family
BuildArch:     noarch
Requires:      wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%description tahoma-fonts
%{summary}
Please note: If you want system integration for wine tahoma fonts install the
wine-tahoma-fonts-system package.

%package tahoma-fonts-system
Summary:       Wine Tahoma font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-tahoma-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description tahoma-fonts-system
%{summary}

%if 0%{?wine_staging}
%package times-new-roman-fonts
Summary:       Wine Times New Roman font family
BuildArch:     noarch
Requires:      wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%description times-new-roman-fonts
%{summary}
Please note: If you want system integration for wine times new roman fonts install the
wine-times-new-roman-fonts-system package.

%package times-new-roman-fonts-system
Summary:       Wine Times New Roman font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-times-new-roman-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description times-new-roman-fonts-system
%{summary}
%endif

%package symbol-fonts
Summary:       Wine Symbol font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description symbol-fonts
%{summary}

%package webdings-fonts
Summary:       Wine Webdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description webdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-webdings-fonts-system package.

%package webdings-fonts-system
Summary:       Wine Webdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-webdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description webdings-fonts-system
%{summary}

%package wingdings-fonts
Summary:       Wine Wingdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description wingdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-wingdings-fonts-system package.

%package wingdings-fonts-system
Summary:       Wine Wingdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-wingdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description wingdings-fonts-system
%{summary}


%package ldap
Summary: LDAP support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description ldap
LDAP support for wine

%package cms
Summary: Color Management for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description cms
Color Management for wine

%package twain
Summary: Twain support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
%ifarch %{ix86}
Requires: sane-backends-libs(x86-32)
%endif
%ifarch x86_64
Requires: sane-backends-libs(x86-64)
%endif
%ifarch %{arm} aarch64
Requires: sane-backends-libs
%endif

%description twain
Twain support for wine

%package devel
Summary: Wine development environment
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package pulseaudio
Summary: Pulseaudio support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
# midi output
Requires: wine-alsa%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description pulseaudio
This package adds a pulseaudio driver for wine.

%package alsa
Summary: Alsa support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description alsa
This package adds an alsa driver for wine.

%package opencl
Summary: OpenCL support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%Description opencl
This package adds the opencl driver for wine.

%prep
%autosetup -S git_am -N -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}}

%patch -P 511 -p1 -b.cjk
%patch -P 599 -p1

# setup and apply wine-staging patches
%if 0%{?wine_staging}

tar -xf %{SOURCE900} --strip-components=1

%patch -P 901 -p1

%if %{without fshack}
%patch -P 1000 -p1
%endif
%patch -P 1001 -p1

%patch -P 5000 -p1

sed -e "s|'autoreconf'|'true'|g" -i ./staging/patchinstall.py
./staging/patchinstall.py --destdir="$(pwd)" --all %{?wine_staging_opts}

%{__scm_apply_patch -p1 -q} -i patches/mfplat-streaming-support/0008-winegstreamer-Allow-videoconvert-to-parallelize.patch

%patch -P 900 -p1
%patch -P 1020 -p1
%patch -P 1021 -p1
%patch -P 1022 -p1
%if %{with fshack}
%patch -P 1023 -p1
%endif
%if %{with childwindow}
%patch -P 1024 -p1
%patch -P 1025 -p1
%endif
%if %{with sharedgpures}
%patch -P 1060 -p1
%patch -P 1061 -p1
%patch -P 1062 -p1
%patch -P 1063 -p1
%endif
%patch -P 1026 -p1
%patch -P 700 -p1 -R
%patch -P 1041 -p1
%patch -P 1027 -p1
%patch -P 1042 -p1
%patch -P 1028 -p1
%patch -P 1029 -p1
%if %{with fastsync}
%patch -P 1051 -p1
%patch -P 1050 -p1
%patch -P 1052 -p1
%endif
%patch -P 1030 -p1
%patch -P 1031 -p1
%patch -P 1032 -p1
%dnl #FIXME see bugzilla (Elder Scrolls Online crash) %patch1034 -p1
%patch -P 1035 -p1
%patch -P 1036 -p1
%patch -P 1037 -p1
%patch -P 1038 -p1
%patch -P 1039 -p1
%patch -P 1040 -p1

%patch -P 1089 -p1
%patch -P 1091 -p1 -R
%patch -P 1092 -p1
%patch -P 1300 -p1
%patch -P 1301 -p1
%dnl %patch -P 1302 -p1
%patch -P 1303 -p1
%patch -P 1304 -p1

sed \
  -e "s/ (Staging)/ (%{staging_banner})/g" \
  -i configure*

%else

rm -rf patches/

%endif

# Verify gecko and mono versions
GECKO_VER="$(grep '^#define' dlls/appwiz.cpl/addons.c | grep ' GECKO_VERSION ' | awk '{print $3}' | tr -d \")"
GECKO_VER2="$(grep '#define' dlls/mshtml/nsiface.idl | grep ' GECKO_VERSION ' | awk '{print $3}' | sed -e 's,\\",,g' -e 's,"),,')"
if [ "${GECKO_VER}" != "%{winegecko}" ] || [ "${GECKO_VER2}" != "%{winegecko}" ] ;then
  echo "winegecko version mismatch. Edit %%global winegecko to ${GECKO_VER}."
  exit 1
fi
MONO_VER="$(grep '^#define' dlls/appwiz.cpl/addons.c | grep ' MONO_VERSION ' | awk '{print $3}' | tr -d \")"
MONO_VER2="$(grep '^#define' dlls/mscoree/mscoree_private.h | grep ' WINE_MONO_VERSION ' | awk '{print $3}' | tr -d \")"
if [ "${MONO_VER}" != "%{winemono}" ] || [ "${MONO_VER2}" != "%{winemono}" ];then
  echo "winemono version mismatch. Edit %%global winemono to ${MONO_VER}."
  exit 1
fi

WINEVULKAN_VER="$(grep '^VK_XML_VERSION' dlls/winevulkan/make_vulkan | awk '{print $3}' | tr -d \")"
if [ "${WINEVULKAN_VER}" != "%{winevulkan}" ] ;then
  echo "winevulkan version mismatch. Edit %%global winevulkan to ${WINEVULKAN_VER}."
  exit 1
fi

cp -p %{SOURCE3} README.FEDORA
cp -p %{SOURCE6} README.chinforpms
%if %{with fshack}
cat README.chinforpms %{SOURCE7} >> README.chinforpms.fshack
touch -r README.chinforpms README.chinforpms.fshack
mv -f README.chinforpms.fshack README.chinforpms
%endif
%if %{with fastsync}
cat README.chinforpms %{SOURCE8} >> README.chinforpms.fastsync
touch -r README.chinforpms README.chinforpms.fastsync
mv -f README.chinforpms.fastsync README.chinforpms
%endif

cp -p %{SOURCE502} README.tahoma

sed -e '/winemenubuilder\.exe/s|-a ||g' -i loader/wine.inf.in

cp -p %{SOURCE50} ./dlls/winevulkan/vk-%{winevulkan}.xml

find . \( -name "*.orig" -o -name "*.cjk" \) -delete

git add .
./tools/make_makefiles
./dlls/winevulkan/make_vulkan
./tools/make_requests
./tools/make_specfiles
autoreconf -f


%build
# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo %{build_cflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=[0-9]//'` -Wno-error"

export CFLAGS="$CFLAGS -ftree-vectorize"

%ifarch aarch64
%global toolchain clang
%endif

# Remove this flags by upstream recommendation (see configure.ac)
export CFLAGS="`echo $CFLAGS | sed \
  -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//' \
  -e 's/-fstack-protector-strong//' \
  -e 's/-fstack-clash-protection//' \
  -e 's/-fcf-protection//' \
  `"

export LDFLAGS="-Wl,-O1,--sort-common %{build_ldflags}"

# https://bugs.winehq.org/show_bug.cgi?id=43530
export LDFLAGS="`echo $LDFLAGS | sed \
  -e 's/-Wl,-z,now//' \
  -e 's/-Wl,-z,relro//' \
  `"

%if 0%{?wine_mingw}
# mingw compiler do not support plugins and some flags are crashing it
export CROSSCFLAGS="`echo $CFLAGS | sed \
  -e 's/-grecord-gcc-switches//' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-cc1,,' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,' \
  -e 's/-fasynchronous-unwind-tables//' \
  `"

# mingw linker do not support -z,relro and now
export CROSSLDFLAGS="`echo $LDFLAGS | sed \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-ld,,' \
  -e 's,-Wl,--build-id=sha1,,' \
  `"

mkdir bin
%if !0%{?with_debug}
# -Wl -S to build working stripped PEs
cat > bin/x86_64-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/x86_64-w64-mingw32-gcc -Wl,-S "$@"
EOF
cat > bin/i686-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/i686-w64-mingw32-gcc -Wl,-S "$@"
EOF
%endif
chmod 0755 bin/*gcc
export PATH="$(pwd)/bin:$PATH"
%endif

# required so that both Linux and Windows development files can be found
unset PKG_CONFIG_PATH 

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --with-dbus \
 --with-x \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
%if 0%{?wine_mingw}
 --with-mingw \
%else
 --without-mingw \
%endif
 --disable-tests \
 --without-oss \
%{nil}

%make_build TARGETFLAGS="" depend
%make_build TARGETFLAGS=""

%install
%if 0%{?wine_mingw}
export PATH="$(pwd)/bin:$PATH"
%endif

%make_install \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
%ifarch aarch64
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine64-preloader
%endif
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
%endif
%ifnarch aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
touch %{buildroot}%{_bindir}/wine-preloader
touch %{buildroot}%{_bindir}/wineserver

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
%ifarch x86_64 aarch64
chrpath --delete %{buildroot}%{_bindir}/wine64
chrpath --delete %{buildroot}%{_bindir}/wineserver64
%else
chrpath --delete %{buildroot}%{_bindir}/wine32
chrpath --delete %{buildroot}%{_bindir}/wineserver32
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf

# add wine dir to desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -p -m 644 %{SOURCE200} \
%{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
mkdir -p %{buildroot}%{_datadir}/desktop-directories
install -p -m 644 %{SOURCE201} \
%{buildroot}%{_datadir}/desktop-directories/Wine.directory

# add gecko dir
mkdir -p %{buildroot}%{_datadir}/wine/gecko

# add mono dir
mkdir -p %{buildroot}%{_datadir}/wine/mono

# extract and install icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# This replacement masks a composite program icon .SVG down
# so that only its full-size scalable icon is visible
PROGRAM_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="368"\n'\
'   y="8"\n'\
'   viewBox="368, 8, 256, 256"/;'

MAIN_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="8"\n'\
'   y="8"\n'\
'   viewBox="8, 8, 256, 256"/;'

# This icon file is still in the legacy format
install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e "$MAIN_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

# The rest come from programs/, and contain larger scalable icons
# with a new layout that requires the PROGRAM_ICONFIX sed adjustment
install -p -m 644 programs/notepad/notepad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg

install -p -m 644 programs/regedit/regedit.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg

install -p -m 644 programs/msiexec/msiexec.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg

install -p -m 644 programs/winecfg/winecfg.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg

install -p -m 644 programs/winefile/winefile.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg

install -p -m 644 programs/winemine/winemine.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg

install -p -m 644 programs/winhlp32/winhelp.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg

install -p -m 644 programs/wordpad/wordpad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg

install -p -m 644 programs/iexplore/iexplore.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/iexplore.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/iexplore.svg

install -p -m 644 dlls/joy.cpl/joy.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg

install -p -m 644 programs/taskmgr/taskmgr.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/taskmgr.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/taskmgr.svg

for file in %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/*.svg ;do
  basefile=$(basename ${file} .svg)
  for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
    dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
    mkdir -p ${dir}
    rsvg-convert -w ${res} -h ${res} ${file} \
      -o ${dir}/${basefile}.png
  done
done

# install desktop files
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE100}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE101}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE102}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE103}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE104}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE105}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE106}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE107}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE108}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE109}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE110}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE111}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE112}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE113}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/wine.desktop

#mime-types
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE300}

# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s \
  $(realpath -m --relative-to=%{_fontconfig_confdir} %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf) \
  %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

%if 0%{?wine_staging}
# install Times New Roman font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
ln -s ../../wine/fonts/times.ttf times.ttf
popd
%endif

# install Webdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-webdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-webdings-fonts
ln -s ../../wine/fonts/webdings.ttf webdings.ttf
popd

# install Wingdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
ln -s ../../wine/fonts/wingding.ttf wingding.ttf
popd

# clean readme files
pushd documentation
for lang in it hu sv es pt pt_br;
do iconv -f iso8859-1 -t utf-8 README.$lang > \
 README.$lang.conv && mv -f README.$lang.conv README.$lang
done;
popd

rm -f %{buildroot}%{_initrddir}/wine

# wine makefiles are currently broken and don't install the wine man page
install -p -m 0644 loader/wine.man %{buildroot}%{_mandir}/man1/wine.1
install -p -m 0644 loader/wine.de.UTF-8.man %{buildroot}%{_mandir}/de.UTF-8/man1/wine.1
install -p -m 0644 loader/wine.fr.UTF-8.man %{buildroot}%{_mandir}/fr.UTF-8/man1/wine.1
mkdir -p %{buildroot}%{_mandir}/pl.UTF-8/man1
install -p -m 0644 loader/wine.pl.UTF-8.man %{buildroot}%{_mandir}/pl.UTF-8/man1/wine.1

# install and validate AppData file
mkdir -p %{buildroot}/%{_metainfodir}/
install -p -m 0644 %{SOURCE150} %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml

%post systemd
%binfmt_apply wine.conf

%postun systemd
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi

%posttrans core
%ifarch x86_64 aarch64
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine64 10 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine64-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver64 20
%else
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine32-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%endif

%postun core
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
fi

%files
# meta package

%files core
%license COPYING.LIB
%license LICENSE
%license LICENSE.OLD
%doc ANNOUNCE
%doc AUTHORS
%doc README.FEDORA
%doc README.chinforpms
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%if 0%{?wine_staging}
%doc README.esync
%endif
%{_bindir}/msidb
%{_bindir}/winedump
%{_libdir}/wine/%{winedlldir}/explorer.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cabarc.%{wineexe}
%{_libdir}/wine/%{winedlldir}/control.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cmd.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dxdiag.%{wineexe}
%{_libdir}/wine/%{winedlldir}/notepad.%{wineexe}
%{_libdir}/wine/%{winedlldir}/plugplay.%{wineexe}
%{_libdir}/wine/%{winedlldir}/progman.%{wineexe}
%{_libdir}/wine/%{winedlldir}/taskmgr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winedbg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winefile.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winemine.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winemsibuilder.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winepath.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winmgmt.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winver.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wordpad.%{wineexe}
%{_libdir}/wine/%{winedlldir}/write.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wusa.%{wineexe}

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%{perms_pldr} %{_bindir}/wine32-preloader
%{perms_srv} %{_bindir}/wineserver32
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{perms_srv} %{_bindir}/wineserver64
%endif
%ifarch x86_64 aarch64
%{perms_pldr} %{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ghost %{_bindir}/wine-preloader
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine
%dir %{_libdir}/wine/%{winearchdir}
%dir %{_libdir}/wine/%{winesodir}
%if !0%{?wine_mingw}
%{_libdir}/wine/%{winearchdir}/*
%endif

%{_libdir}/wine/%{winedlldir}/attrib.%{wineexe}
%{_libdir}/wine/%{winedlldir}/arp.%{wineexe}
%{_libdir}/wine/%{winedlldir}/aspnet_regiis.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cacls.%{wineexe}
%{_libdir}/wine/%{winedlldir}/conhost.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cscript.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dism.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dllhost.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dpnsvr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/eject.%{wineexe}
%{_libdir}/wine/%{winedlldir}/expand.%{wineexe}
%{_libdir}/wine/%{winedlldir}/extrac32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/fc.%{wineexe}
%{_libdir}/wine/%{winedlldir}/find.%{wineexe}
%{_libdir}/wine/%{winedlldir}/findstr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/fsutil.%{wineexe}
%{_libdir}/wine/%{winedlldir}/hostname.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ipconfig.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winhlp32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/mshta.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winedlldir}/msidb.%{wineexe}
%endif
%{_libdir}/wine/%{winedlldir}/msiexec.%{wineexe}
%{_libdir}/wine/%{winedlldir}/net.%{wineexe}
%{_libdir}/wine/%{winedlldir}/netstat.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ngen.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ntoskrnl.%{wineexe}
%{_libdir}/wine/%{winedlldir}/oleview.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ping.%{wineexe}
%{_libdir}/wine/%{winedlldir}/powershell.%{wineexe}
%{_libdir}/wine/%{winedlldir}/reg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regasm.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regedit.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regini.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regsvcs.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regsvr32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/rpcss.%{wineexe}
%{_libdir}/wine/%{winedlldir}/rundll32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/schtasks.%{wineexe}
%{_libdir}/wine/%{winedlldir}/sdbinst.%{wineexe}
%{_libdir}/wine/%{winedlldir}/secedit.%{wineexe}
%{_libdir}/wine/%{winedlldir}/servicemodelreg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/services.%{wineexe}
%{_libdir}/wine/%{winedlldir}/start.%{wineexe}
%{_libdir}/wine/%{winedlldir}/tasklist.%{wineexe}
%{_libdir}/wine/%{winedlldir}/termsv.%{wineexe}
%{_libdir}/wine/%{winedlldir}/view.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wevtutil.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wineboot.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winebrowser.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wineconsole.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winecfg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winemenubuilder.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winedevice.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wmplayer.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wscript.%{wineexe}
%{_libdir}/wine/%{winedlldir}/uninstaller.%{wineexe}

%{_libdir}/wine/%{winedlldir}/acledit.%{winedll}
%{_libdir}/wine/%{winedlldir}/aclui.%{winedll}
%{_libdir}/wine/%{winedlldir}/activeds.%{winedll}
%{_libdir}/wine/%{winedlldir}/activeds.%{winetlb}
%{_libdir}/wine/%{winedlldir}/actxprxy.%{winedll}
%{_libdir}/wine/%{winedlldir}/adsldp.%{winedll}
%{_libdir}/wine/%{winedlldir}/adsldpc.%{winedll}
%{_libdir}/wine/%{winedlldir}/advapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/advpack.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winedlldir}/audioses.%{winedll}
%endif
%{_libdir}/wine/%{winedlldir}/amsi.%{winedll}
%{_libdir}/wine/%{winedlldir}/amstream.%{winedll}
%{_libdir}/wine/%{winedlldir}/apisetschema.%{winedll}
%{_libdir}/wine/%{winedlldir}/apphelp.%{winedll}
%{_libdir}/wine/%{winedlldir}/appwiz.%{winecpl}
%{_libdir}/wine/%{winedlldir}/atl.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl80.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl90.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl100.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl110.%{winedll}
%{_libdir}/wine/%{winedlldir}/atlthunk.%{winedll}
%{_libdir}/wine/%{winedlldir}/atmlib.%{winedll}
%{_libdir}/wine/%{winedlldir}/authz.%{winedll}
%{_libdir}/wine/%{winesodir}/avicap32.so
%{_libdir}/wine/%{winedlldir}/avicap32.%{winedll}
%{_libdir}/wine/%{winedlldir}/avifil32.%{winedll}
%{_libdir}/wine/%{winedlldir}/avrt.%{winedll}
%{_libdir}/wine/%{winesodir}/bcrypt.so
%{_libdir}/wine/%{winedlldir}/bcrypt.%{winedll}
%{_libdir}/wine/%{winedlldir}/bcryptprimitives.%{winedll}
%{_libdir}/wine/%{winedlldir}/bluetoothapis.%{winedll}
%{_libdir}/wine/%{winedlldir}/browseui.%{winedll}
%{_libdir}/wine/%{winedlldir}/bthprops.%{winecpl}
%{_libdir}/wine/%{winedlldir}/cabinet.%{winedll}
%{_libdir}/wine/%{winedlldir}/cards.%{winedll}
%{_libdir}/wine/%{winedlldir}/cdosys.%{winedll}
%{_libdir}/wine/%{winedlldir}/certutil.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cfgmgr32.%{winedll}
%{_libdir}/wine/%{winedlldir}/chcp.%{winecom}
%{_libdir}/wine/%{winedlldir}/clock.%{wineexe}
%{_libdir}/wine/%{winedlldir}/clusapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/cng.%{winesys}
%{_libdir}/wine/%{winedlldir}/combase.%{winedll}
%{_libdir}/wine/%{winedlldir}/comcat.%{winedll}
%{_libdir}/wine/%{winedlldir}/comctl32.%{winedll}
%{_libdir}/wine/%{winedlldir}/comdlg32.%{winedll}
%{_libdir}/wine/%{winedlldir}/compstui.%{winedll}
%{_libdir}/wine/%{winedlldir}/comsvcs.%{winedll}
%{_libdir}/wine/%{winedlldir}/concrt140.%{winedll}
%{_libdir}/wine/%{winedlldir}/connect.%{winedll}
%{_libdir}/wine/%{winedlldir}/credui.%{winedll}
%{_libdir}/wine/%{winedlldir}/crtdll.%{winedll}
%{_libdir}/wine/%{winesodir}/crypt32.so
%{_libdir}/wine/%{winedlldir}/crypt32.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptdlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptdll.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptext.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptnet.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptowinrt.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptsp.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptui.%{winedll}
%{_libdir}/wine/%{winesodir}/ctapi32.so
%{_libdir}/wine/%{winedlldir}/ctapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/ctl3d32.%{winedll}
%{_libdir}/wine/%{winedlldir}/d2d1.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d10.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d10_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d10core.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d11.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d12.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d12core.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dcompiler_*.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dim.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dim700.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3drm.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx9_*.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx10_*.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx11_42.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx11_43.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dxof.%{winedll}
%{_libdir}/wine/%{winedlldir}/davclnt.%{winedll}
%{_libdir}/wine/%{winedlldir}/dbgeng.%{winedll}
%{_libdir}/wine/%{winedlldir}/dbghelp.%{winedll}
%{_libdir}/wine/%{winedlldir}/dciman32.%{winedll}
%{_libdir}/wine/%{winedlldir}/dcomp.%{winedll}
%{_libdir}/wine/%{winedlldir}/ddraw.%{winedll}
%{_libdir}/wine/%{winedlldir}/ddrawex.%{winedll}
%{_libdir}/wine/%{winedlldir}/devenum.%{winedll}
%{_libdir}/wine/%{winedlldir}/dhcpcsvc.%{winedll}
%{_libdir}/wine/%{winedlldir}/dhcpcsvc6.%{winedll}
%{_libdir}/wine/%{winedlldir}/dhtmled.%{wineocx}
%{_libdir}/wine/%{winedlldir}/diasymreader.%{winedll}
%{_libdir}/wine/%{winedlldir}/difxapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/dinput.%{winedll}
%{_libdir}/wine/%{winedlldir}/dinput8.%{winedll}
%{_libdir}/wine/%{winedlldir}/directmanipulation.%{winedll}
%{_libdir}/wine/%{winedlldir}/dispex.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmband.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmcompos.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmime.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmloader.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmscript.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmstyle.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmsynth.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmusic.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmusic32.%{winedll}
%{_libdir}/wine/%{winedlldir}/dotnetfx35.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dplay.%{winedll}
%{_libdir}/wine/%{winedlldir}/dplaysvr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dplayx.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnaddr.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnet.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnhpast.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnhupnp.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnlobby.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpvoice.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpwsockx.%{winedll}
%{_libdir}/wine/%{winedlldir}/drmclien.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsdmo.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsound.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsquery.%{winedll}
%{_libdir}/wine/%{winedlldir}/dssenh.%{winedll}
%{_libdir}/wine/%{winedlldir}/dswave.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsuiext.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpvsetup.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dwmapi.%{winedll}
%{_libdir}/wine/%{winesodir}/dwrite.so
%{_libdir}/wine/%{winedlldir}/dwrite.%{winedll}
%{_libdir}/wine/%{winedlldir}/dx8vb.%{winedll}
%{_libdir}/wine/%{winedlldir}/dxdiagn.%{winedll}
%{_libdir}/wine/%{winedlldir}/dxgi.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winedlldir}/dxgkrnl.%{winesys}
%{_libdir}/wine/%{winedlldir}/dxgmms1.%{winesys}
%endif
%{_libdir}/wine/%{winedlldir}/dxtrans.%{winedll}
%{_libdir}/wine/%{winedlldir}/dxva2.%{winedll}
%{_libdir}/wine/%{winedlldir}/esent.%{winedll}
%{_libdir}/wine/%{winedlldir}/evr.%{winedll}
%{_libdir}/wine/%{winedlldir}/explorerframe.%{winedll}
%{_libdir}/wine/%{winedlldir}/faultrep.%{winedll}
%{_libdir}/wine/%{winedlldir}/feclient.%{winedll}
%{_libdir}/wine/%{winedlldir}/fltlib.%{winedll}
%{_libdir}/wine/%{winedlldir}/fltmgr.%{winesys}
%{_libdir}/wine/%{winedlldir}/fntcache.%{winedll}
%{_libdir}/wine/%{winedlldir}/fontsub.%{winedll}
%{_libdir}/wine/%{winedlldir}/fusion.%{winedll}
%{_libdir}/wine/%{winedlldir}/fwpuclnt.%{winedll}
%{_libdir}/wine/%{winedlldir}/gameux.%{winedll}
%{_libdir}/wine/%{winedlldir}/gamingtcui.%{winedll}
%{_libdir}/wine/%{winedlldir}/gdi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/gdiplus.%{winedll}
%{_libdir}/wine/%{winedlldir}/geolocation.%{winedll}
%{_libdir}/wine/%{winedlldir}/glu32.%{winedll}
%{_libdir}/wine/%{winesodir}/gphoto2.so
%{_libdir}/wine/%{winedlldir}/gphoto2.%{wineds}
%{_libdir}/wine/%{winedlldir}/gpkcsp.%{winedll}
%{_libdir}/wine/%{winedlldir}/graphicscapture.%{winedll}
%{_libdir}/wine/%{winedlldir}/hal.%{winedll}
%{_libdir}/wine/%{winedlldir}/hh.%{wineexe}
%{_libdir}/wine/%{winedlldir}/hhctrl.%{wineocx}
%{_libdir}/wine/%{winedlldir}/hid.%{winedll}
%{_libdir}/wine/%{winedlldir}/hidclass.%{winesys}
%{_libdir}/wine/%{winedlldir}/hidparse.%{winesys}
%{_libdir}/wine/%{winedlldir}/hlink.%{winedll}
%{_libdir}/wine/%{winedlldir}/hnetcfg.%{winedll}
%{_libdir}/wine/%{winedlldir}/hrtfapo.%{winedll}
%{_libdir}/wine/%{winedlldir}/http.%{winesys}
%{_libdir}/wine/%{winedlldir}/httpapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/ia2comproxy.%{winedll}
%{_libdir}/wine/%{winedlldir}/icacls.%{wineexe}
%{_libdir}/wine/%{winedlldir}/iccvid.%{winedll}
%{_libdir}/wine/%{winedlldir}/icinfo.%{wineexe}
%{_libdir}/wine/%{winedlldir}/icmp.%{winedll}
%{_libdir}/wine/%{winedlldir}/ieframe.%{winedll}
%{_libdir}/wine/%{winedlldir}/ieproxy.%{winedll}
%{_libdir}/wine/%{winedlldir}/imaadp32.%{wineacm}
%{_libdir}/wine/%{winedlldir}/imagehlp.%{winedll}
%{_libdir}/wine/%{winedlldir}/imm32.%{winedll}
%{_libdir}/wine/%{winedlldir}/inetcomm.%{winedll}
%{_libdir}/wine/%{winedlldir}/inetcpl.%{winecpl}
%{_libdir}/wine/%{winedlldir}/inetmib1.%{winedll}
%{_libdir}/wine/%{winedlldir}/infosoft.%{winedll}
%{_libdir}/wine/%{winedlldir}/initpki.%{winedll}
%{_libdir}/wine/%{winedlldir}/inkobj.%{winedll}
%{_libdir}/wine/%{winedlldir}/inseng.%{winedll}
%{_libdir}/wine/%{winedlldir}/iphlpapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/iprop.%{winedll}
%{_libdir}/wine/%{winedlldir}/ir50_32.%{winedll}
%{_libdir}/wine/%{winedlldir}/irprops.%{winecpl}
%{_libdir}/wine/%{winedlldir}/itircl.%{winedll}
%{_libdir}/wine/%{winedlldir}/itss.%{winedll}
%{_libdir}/wine/%{winedlldir}/joy.%{winecpl}
%{_libdir}/wine/%{winedlldir}/jscript.%{winedll}
%{_libdir}/wine/%{winedlldir}/jsproxy.%{winedll}
%{_libdir}/wine/%{winesodir}/kerberos.so
%{_libdir}/wine/%{winedlldir}/kerberos.%{winedll}
%{_libdir}/wine/%{winedlldir}/kernel32.%{winedll}
%{_libdir}/wine/%{winedlldir}/kernelbase.%{winedll}
%{_libdir}/wine/%{winedlldir}/klist.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ksecdd.%{winesys}
%{_libdir}/wine/%{winedlldir}/ksproxy.%{wineax}
%{_libdir}/wine/%{winedlldir}/ksuser.%{winedll}
%{_libdir}/wine/%{winedlldir}/ktmw32.%{winedll}
%{_libdir}/wine/%{winedlldir}/l3codeca.%{wineacm}
%{_libdir}/wine/%{winedlldir}/light.%{winemsstyles}
%{_libdir}/wine/%{winedlldir}/loadperf.%{winedll}
%{_libdir}/wine/%{winesodir}/localspl.so
%{_libdir}/wine/%{winedlldir}/localspl.%{winedll}
%{_libdir}/wine/%{winedlldir}/localui.%{winedll}
%{_libdir}/wine/%{winedlldir}/lodctr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/lz32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mapistub.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciavi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mcicda.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciqtz32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciseq.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciwave.%{winedll}
%{_libdir}/wine/%{winedlldir}/mf.%{winedll}
%{_libdir}/wine/%{winedlldir}/mf3216.%{winedll}
%{_libdir}/wine/%{winedlldir}/mferror.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfmediaengine.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfplat.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfplay.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfreadwrite.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfsrcsnk.%{winedll}
%{_libdir}/wine/%{winedlldir}/mgmtapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/midimap.%{winedll}
%{_libdir}/wine/%{winedlldir}/mlang.%{winedll}
%{_libdir}/wine/%{winedlldir}/mmcndmgr.%{winedll}
%{_libdir}/wine/%{winedlldir}/mmdevapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/mofcomp.%{wineexe}
%{_libdir}/wine/%{winesodir}/mountmgr.so
%{_libdir}/wine/%{winedlldir}/mountmgr.%{winesys}
%{_libdir}/wine/%{winedlldir}/mp3dmod.%{winedll}
%{_libdir}/wine/%{winedlldir}/mpr.%{winedll}
%{_libdir}/wine/%{winedlldir}/mprapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/msacm32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msacm32.%{winedrv}
%{_libdir}/wine/%{winedlldir}/msado15.%{winedll}
%{_libdir}/wine/%{winedlldir}/msadp32.%{wineacm}
%{_libdir}/wine/%{winedlldir}/msasn1.%{winedll}
%{_libdir}/wine/%{winedlldir}/msauddecmft.%{winedll}
%{_libdir}/wine/%{winedlldir}/mscat32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mscoree.%{winedll}
%{_libdir}/wine/%{winedlldir}/mscorwks.%{winedll}
%{_libdir}/wine/%{winedlldir}/msctf.%{winedll}
%{_libdir}/wine/%{winedlldir}/msctfmonitor.%{winedll}
%{_libdir}/wine/%{winedlldir}/msctfp.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdaps.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdasql.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdelta.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdmo.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdrm.%{winedll}
%{_libdir}/wine/%{winedlldir}/msftedit.%{winedll}
%{_libdir}/wine/%{winedlldir}/msg711.%{wineacm}
%{_libdir}/wine/%{winedlldir}/msgsm32.%{wineacm}
%{_libdir}/wine/%{winedlldir}/mshtml.%{winedll}
%{_libdir}/wine/%{winedlldir}/mshtml.%{winetlb}
%{_libdir}/wine/%{winedlldir}/msi.%{winedll}
%{_libdir}/wine/%{winedlldir}/msident.%{winedll}
%{_libdir}/wine/%{winedlldir}/msimtf.%{winedll}
%{_libdir}/wine/%{winedlldir}/msimg32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msimsg.%{winedll}
%{_libdir}/wine/%{winedlldir}/msinfo32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/msisip.%{winedll}
%{_libdir}/wine/%{winedlldir}/msisys.%{wineocx}
%{_libdir}/wine/%{winedlldir}/msls31.%{winedll}
%{_libdir}/wine/%{winedlldir}/msmpeg2vdec.%{winedll}
%{_libdir}/wine/%{winedlldir}/msnet32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mspatcha.%{winedll}
%{_libdir}/wine/%{winedlldir}/msports.%{winedll}
%{_libdir}/wine/%{winedlldir}/msscript.%{wineocx}
%{_libdir}/wine/%{winedlldir}/mssign32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mssip32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msrle32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mstask.%{winedll}
%{_libdir}/wine/%{winesodir}/msv1_0.so
%{_libdir}/wine/%{winedlldir}/msv1_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcirt.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp_win.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcm80.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcm90.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp60.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp70.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp71.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp80.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp90.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp100.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp110.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp120.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp120_app.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp140.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp140_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp140_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp140_atomic_wait.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr70.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr71.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr80.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr90.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr100.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr110.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr120.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr120_app.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrt.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrt20.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrt40.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrtd.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvfw32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvidc32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mswsock.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml2.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml3.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml4.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml6.%{winedll}
%{_libdir}/wine/%{winedlldir}/mtxdm.%{winedll}
%{_libdir}/wine/%{winedlldir}/nddeapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/ncrypt.%{winedll}
%{_libdir}/wine/%{winedlldir}/ndis.%{winesys}
%{_libdir}/wine/%{winesodir}/netapi32.so
%{_libdir}/wine/%{winedlldir}/netapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/netcfgx.%{winedll}
%{_libdir}/wine/%{winedlldir}/netio.%{winesys}
%{_libdir}/wine/%{winedlldir}/netprofm.%{winedll}
%{_libdir}/wine/%{winedlldir}/netsh.%{wineexe}
%{_libdir}/wine/%{winedlldir}/netutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/newdev.%{winedll}
%{_libdir}/wine/%{winedlldir}/ninput.%{winedll}
%{_libdir}/wine/%{winedlldir}/normaliz.%{winedll}
%{_libdir}/wine/%{winedlldir}/npmshtml.%{winedll}
%{_libdir}/wine/%{winedlldir}/npptools.%{winedll}
%{_libdir}/wine/%{winedlldir}/nsi.%{winedll}
%{_libdir}/wine/%{winesodir}/nsiproxy.so
%{_libdir}/wine/%{winedlldir}/nsiproxy.%{winesys}
%{_libdir}/wine/%{winesodir}/ntdll.so
%{_libdir}/wine/%{winedlldir}/ntdll.%{winedll}
%{_libdir}/wine/%{winedlldir}/ntdsapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/ntprint.%{winedll}
%{_libdir}/wine/%{winedlldir}/objsel.%{winedll}
%{_libdir}/wine/%{winesodir}/odbc32.so
%{_libdir}/wine/%{winedlldir}/odbc32.%{winedll}
%{_libdir}/wine/%{winedlldir}/odbcbcp.%{winedll}
%{_libdir}/wine/%{winedlldir}/odbccp32.%{winedll}
%{_libdir}/wine/%{winedlldir}/odbccu32.%{winedll}
%{_libdir}/wine/%{winedlldir}/ole32.%{winedll}
%{_libdir}/wine/%{winedlldir}/oleacc.%{winedll}
%{_libdir}/wine/%{winedlldir}/oleaut32.%{winedll}
%{_libdir}/wine/%{winedlldir}/olecli32.%{winedll}
%{_libdir}/wine/%{winedlldir}/oledb32.%{winedll}
%{_libdir}/wine/%{winedlldir}/oledlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/olepro32.%{winedll}
%{_libdir}/wine/%{winedlldir}/olesvr32.%{winedll}
%{_libdir}/wine/%{winedlldir}/olethk32.%{winedll}
%{_libdir}/wine/%{winedlldir}/opcservices.%{winedll}
%{_libdir}/wine/%{winedlldir}/packager.%{winedll}
%{_libdir}/wine/%{winedlldir}/pdh.%{winedll}
%{_libdir}/wine/%{winedlldir}/pnputil.%{wineexe}
%{_libdir}/wine/%{winedlldir}/photometadatahandler.%{winedll}
%{_libdir}/wine/%{winedlldir}/pidgen.%{winedll}
%{_libdir}/wine/%{winedlldir}/powrprof.%{winedll}
%{_libdir}/wine/%{winedlldir}/presentationfontcache.%{wineexe}
%{_libdir}/wine/%{winedlldir}/printui.%{winedll}
%{_libdir}/wine/%{winedlldir}/prntvpt.%{winedll}
%{_libdir}/wine/%{winedlldir}/propsys.%{winedll}
%{_libdir}/wine/%{winedlldir}/psapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/pstorec.%{winedll}
%{_libdir}/wine/%{winedlldir}/pwrshplugin.%{winedll}
%{_libdir}/wine/%{winedlldir}/qasf.%{winedll}
%{_libdir}/wine/%{winesodir}/qcap.so
%{_libdir}/wine/%{winedlldir}/qcap.%{winedll}
%{_libdir}/wine/%{winedlldir}/qedit.%{winedll}
%{_libdir}/wine/%{winedlldir}/qdvd.%{winedll}
%{_libdir}/wine/%{winedlldir}/qmgr.%{winedll}
%{_libdir}/wine/%{winedlldir}/qmgrprxy.%{winedll}
%{_libdir}/wine/%{winedlldir}/quartz.%{winedll}
%{_libdir}/wine/%{winedlldir}/query.%{winedll}
%{_libdir}/wine/%{winedlldir}/qwave.%{winedll}
%{_libdir}/wine/%{winedlldir}/rasapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/rasdlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/regapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/resutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/riched20.%{winedll}
%{_libdir}/wine/%{winedlldir}/riched32.%{winedll}
%{_libdir}/wine/%{winedlldir}/rpcrt4.%{winedll}
%{_libdir}/wine/%{winedlldir}/robocopy.%{wineexe}
%{_libdir}/wine/%{winedlldir}/rsabase.%{winedll}
%{_libdir}/wine/%{winedlldir}/rsaenh.%{winedll}
%{_libdir}/wine/%{winedlldir}/rstrtmgr.%{winedll}
%{_libdir}/wine/%{winedlldir}/rtutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/rtworkq.%{winedll}
%{_libdir}/wine/%{winedlldir}/samlib.%{winedll}
%{_libdir}/wine/%{winedlldir}/sapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/sas.%{winedll}
%{_libdir}/wine/%{winedlldir}/sc.%{wineexe}
%{_libdir}/wine/%{winedlldir}/scarddlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/scardsvr.%{winedll}
%{_libdir}/wine/%{winedlldir}/sccbase.%{winedll}
%{_libdir}/wine/%{winedlldir}/schannel.%{winedll}
%{_libdir}/wine/%{winedlldir}/scrobj.%{winedll}
%{_libdir}/wine/%{winedlldir}/scrrun.%{winedll}
%{_libdir}/wine/%{winedlldir}/scsiport.%{winesys}
%{_libdir}/wine/%{winedlldir}/sechost.%{winedll}
%{_libdir}/wine/%{winesodir}/secur32.so
%{_libdir}/wine/%{winedlldir}/secur32.%{winedll}
%{_libdir}/wine/%{winedlldir}/sensapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/serialui.%{winedll}
%{_libdir}/wine/%{winedlldir}/setupapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/setx.%{wineexe}
%{_libdir}/wine/%{winedlldir}/sfc_os.%{winedll}
%{_libdir}/wine/%{winedlldir}/shcore.%{winedll}
%{_libdir}/wine/%{winedlldir}/shdoclc.%{winedll}
%{_libdir}/wine/%{winedlldir}/shdocvw.%{winedll}
%{_libdir}/wine/%{winedlldir}/schedsvc.%{winedll}
%if %{with sharedgpures}
%{_libdir}/wine/%{winedlldir}/sharedgpures.%{winesys}
%endif
%{_libdir}/wine/%{winedlldir}/shell32.%{winedll}
%{_libdir}/wine/%{winedlldir}/shfolder.%{winedll}
%{_libdir}/wine/%{winedlldir}/shlwapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/shutdown.%{wineexe}
%{_libdir}/wine/%{winedlldir}/slbcsp.%{winedll}
%{_libdir}/wine/%{winedlldir}/slc.%{winedll}
%{_libdir}/wine/%{winedlldir}/snmpapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/softpub.%{winedll}
%{_libdir}/wine/%{winedlldir}/spoolsv.%{wineexe}
%{_libdir}/wine/%{winedlldir}/sppc.%{winedll}
%{_libdir}/wine/%{winedlldir}/srclient.%{winedll}
%{_libdir}/wine/%{winedlldir}/srvcli.%{winedll}
%{_libdir}/wine/%{winedlldir}/sspicli.%{winedll}
%{_libdir}/wine/%{winedlldir}/stdole2.%{winetlb}
%{_libdir}/wine/%{winedlldir}/stdole32.%{winetlb}
%{_libdir}/wine/%{winedlldir}/sti.%{winedll}
%{_libdir}/wine/%{winedlldir}/strmdll.%{winedll}
%{_libdir}/wine/%{winedlldir}/subst.%{wineexe}
%{_libdir}/wine/%{winedlldir}/svchost.%{wineexe}
%{_libdir}/wine/%{winedlldir}/svrapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/sxs.%{winedll}
%{_libdir}/wine/%{winedlldir}/systeminfo.%{wineexe}
%{_libdir}/wine/%{winedlldir}/t2embed.%{winedll}
%{_libdir}/wine/%{winedlldir}/tapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/taskkill.%{wineexe}
%{_libdir}/wine/%{winedlldir}/taskschd.%{winedll}
%{_libdir}/wine/%{winedlldir}/tbs.%{winedll}
%{_libdir}/wine/%{winedlldir}/tdh.%{winedll}
%{_libdir}/wine/%{winedlldir}/tdi.%{winesys}
%{_libdir}/wine/%{winedlldir}/traffic.%{winedll}
%{_libdir}/wine/%{winedlldir}/threadpoolwinrt.%{winedll}
%{_libdir}/wine/%{winedlldir}/twinapi.appcore.%{winedll}
%{_libdir}/wine/%{winedlldir}/tzres.%{winedll}
%{_libdir}/wine/%{winedlldir}/ucrtbase.%{winedll}
%{_libdir}/wine/%{winedlldir}/uianimation.%{winedll}
%{_libdir}/wine/%{winedlldir}/uiautomationcore.%{winedll}
%{_libdir}/wine/%{winedlldir}/uiribbon.%{winedll}
%{_libdir}/wine/%{winedlldir}/unicows.%{winedll}
%{_libdir}/wine/%{winedlldir}/unlodctr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/updspapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/url.%{winedll}
%{_libdir}/wine/%{winedlldir}/urlmon.%{winedll}
%{_libdir}/wine/%{winedlldir}/usbd.%{winesys}
%{_libdir}/wine/%{winedlldir}/user32.%{winedll}
%{_libdir}/wine/%{winedlldir}/usp10.%{winedll}
%{_libdir}/wine/%{winedlldir}/utildll.%{winedll}
%{_libdir}/wine/%{winedlldir}/uxtheme.%{winedll}
%{_libdir}/wine/%{winedlldir}/userenv.%{winedll}
%{_libdir}/wine/%{winedlldir}/vbscript.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp90.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp100.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp110.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp120.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp140.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcruntime140.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcruntime140_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/vdmdbg.%{winedll}
%{_libdir}/wine/%{winedlldir}/vga.%{winedll}
%{_libdir}/wine/%{winedlldir}/version.%{winedll}
%{_libdir}/wine/%{winedlldir}/virtdisk.%{winedll}
%{_libdir}/wine/%{winedlldir}/vssapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/vulkan-1.%{winedll}
%{_libdir}/wine/%{winedlldir}/wbemdisp.%{winedll}
%{_libdir}/wine/%{winedlldir}/wbemprox.%{winedll}
%{_libdir}/wine/%{winedlldir}/wdscore.%{winedll}
%{_libdir}/wine/%{winedlldir}/webservices.%{winedll}
%{_libdir}/wine/%{winedlldir}/websocket.%{winedll}
%{_libdir}/wine/%{winedlldir}/wer.%{winedll}
%{_libdir}/wine/%{winedlldir}/wevtapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wevtsvc.%{winedll}
%{_libdir}/wine/%{winedlldir}/where.%{wineexe}
%{_libdir}/wine/%{winedlldir}/whoami.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wiaservc.%{winedll}
%{_libdir}/wine/%{winedlldir}/wimgapi.%{winedll}
%{_libdir}/wine/%{winesodir}/win32u.so
%{_libdir}/wine/%{winedlldir}/win32u.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.devices.bluetooth.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.devices.enumeration.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.gaming.input.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.gaming.ui.gamebar.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.globalization.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.media.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.media.devices.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.media.speech.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.networking.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.networking.hostname.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winedlldir}/win32k.%{winesys}
%{_libdir}/wine/%{winedlldir}/windows.networking.connectivity.%{winedll}
%endif
%{_libdir}/wine/%{winedlldir}/windows.perception.stub.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.system.profile.systemmanufacturers.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.ui.%{winedll}
%{_libdir}/wine/%{winedlldir}/windowscodecs.%{winedll}
%{_libdir}/wine/%{winedlldir}/windowscodecsext.%{winedll}
%{_libdir}/wine/%{winesodir}/winebus.so
%{_libdir}/wine/%{winedlldir}/winebus.%{winesys}
%{_libdir}/wine/%{winesodir}/winegstreamer.so
%{_libdir}/wine/%{winedlldir}/winegstreamer.%{winedll}
%{_libdir}/wine/%{winedlldir}/winehid.%{winesys}
%{_libdir}/wine/%{winedlldir}/winemapi.%{winedll}
%{_libdir}/wine/%{winesodir}/wineusb.so
%{_libdir}/wine/%{winedlldir}/wineusb.%{winesys}
%{_libdir}/wine/%{winesodir}/winevulkan.so
%{_libdir}/wine/%{winedlldir}/winevulkan.%{winedll}
%{_libdir}/wine/%{winesodir}/winewayland.so
%{_libdir}/wine/%{winedlldir}/winewayland.%{winedrv}
%{_libdir}/wine/%{winesodir}/winex11.so
%{_libdir}/wine/%{winedlldir}/winex11.%{winedrv}
%{_libdir}/wine/%{winedlldir}/wing32.%{winedll}
%{_libdir}/wine/%{winedlldir}/winhttp.%{winedll}
%{_libdir}/wine/%{winedlldir}/wininet.%{winedll}
%{_libdir}/wine/%{winedlldir}/winmm.%{winedll}
%{_libdir}/wine/%{winedlldir}/winprint.%{winedll}
%{_libdir}/wine/%{winedlldir}/winnls32.%{winedll}
%{_libdir}/wine/%{winesodir}/winspool.so
%{_libdir}/wine/%{winedlldir}/winspool.%{winedrv}
%{_libdir}/wine/%{winedlldir}/winsta.%{winedll}
%{_libdir}/wine/%{winedlldir}/wintypes.%{winedll}
%{_libdir}/wine/%{winedlldir}/wlanui.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmasf.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmic.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wmiutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmp.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmvcore.%{winedll}
%{_libdir}/wine/%{winedlldir}/spoolss.%{winedll}
%{_libdir}/wine/%{winesodir}/winscard.so
%{_libdir}/wine/%{winedlldir}/winscard.%{winedll}
%{_libdir}/wine/%{winedlldir}/wintab32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wintrust.%{winedll}
%{_libdir}/wine/%{winedlldir}/winusb.%{winedll}
%{_libdir}/wine/%{winedlldir}/wlanapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmphoto.%{winedll}
%{_libdir}/wine/%{winedlldir}/wnaspi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wofutil.%{winedll}
%ifarch x86_64
%{_libdir}/wine/%{winedlldir}/wow64.%{winedll}
%{_libdir}/wine/%{winedlldir}/wow64cpu.%{winedll}
%{_libdir}/wine/%{winedlldir}/wow64win.%{winedll}
%endif
%{_libdir}/wine/%{winedlldir}/wpc.%{winedll}
%{_libdir}/wine/%{winesodir}/wpcap.so
%{_libdir}/wine/%{winedlldir}/wpcap.%{winedll}
%{_libdir}/wine/%{winesodir}/ws2_32.so
%{_libdir}/wine/%{winedlldir}/ws2_32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wsdapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wshom.%{wineocx}
%{_libdir}/wine/%{winedlldir}/wsnmp32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wsock32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wtsapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wuapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wuaueng.%{winedll}
%{_libdir}/wine/%{winedlldir}/wuauserv.%{wineexe}
%{_libdir}/wine/%{winedlldir}/security.%{winedll}
%{_libdir}/wine/%{winedlldir}/sfc.%{winedll}
%{_libdir}/wine/%{winesodir}/wineps.so
%{_libdir}/wine/%{winedlldir}/wineps.%{winedrv}
%{_libdir}/wine/%{winedlldir}/d3d8.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d8thk.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d9.%{winedll}
%{_libdir}/wine/%{winesodir}/opengl32.so
%{_libdir}/wine/%{winedlldir}/opengl32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wined3d.%{winedll}
%{_libdir}/wine/%{winedlldir}/winexinput.%{winesys}
%{_libdir}/wine/%{winesodir}/dnsapi.so
%{_libdir}/wine/%{winedlldir}/dnsapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/iexplore.%{wineexe}
%{_libdir}/wine/%{winedlldir}/xactengine2_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine2_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine2_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine2_9.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_6.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_6.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_6.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_8.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_9.%{winedll}
%{_libdir}/wine/%{winedlldir}/xcopy.%{wineexe}
%{_libdir}/wine/%{winedlldir}/xinput1_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput1_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput1_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput1_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput9_1_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinputuap.%{winedll}
%{_libdir}/wine/%{winedlldir}/xmllite.%{winedll}
%{_libdir}/wine/%{winedlldir}/xolehlp.%{winedll}
%{_libdir}/wine/%{winedlldir}/xpsprint.%{winedll}
%{_libdir}/wine/%{winedlldir}/xpssvcs.%{winedll}

%if 0
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/nvcuda.dll.so
%{_libdir}/wine/%{winesodir}/nvcuvid.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/nvcuda.dll
%{_libdir}/wine/%{winedlldir}/nvcuvid.dll
%endif
%ifarch x86_64 aarch64
%{_libdir}/wine/%{winedlldir}/nvapi64.%{winedll}
%{_libdir}/wine/%{winesodir}/nvencodeapi64.dll.so
%exclude %{_libdir}/wine/%{winesodir}/nvencodeapi.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/nvencodeapi64.dll
%exclude %{_libdir}/wine/%{winedlldir}/nvencodeapi.dll
%endif
%else
%{_libdir}/wine/%{winedlldir}/nvapi.%{winedll}
%{_libdir}/wine/%{winesodir}/nvencodeapi.dll.so
%exclude %{_libdir}/wine/%{winesodir}/nvencodeapi64.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/nvencodeapi.dll
%exclude %{_libdir}/wine/%{winedlldir}/nvencodeapi64.dll
%endif
%endif
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/%{winedlldir}/winevdm.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ifsmgr.%{winevxd}
%{_libdir}/wine/%{winedlldir}/mmdevldr.%{winevxd}
%{_libdir}/wine/%{winedlldir}/monodebg.%{winevxd}
%{_libdir}/wine/%{winedlldir}/rundll.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/vdhcp.%{winevxd}
%{_libdir}/wine/%{winedlldir}/user.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/vmm.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vnbt.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vnetbios.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vtdapi.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vwin32.%{winevxd}
%{_libdir}/wine/%{winedlldir}/w32skrnl.%{winedll}
%{_libdir}/wine/%{winedlldir}/avifile.%{winedll16}
%{_libdir}/wine/%{winedlldir}/comm.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/commdlg.%{winedll16}
%{_libdir}/wine/%{winedlldir}/compobj.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ctl3d.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ctl3dv2.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ddeml.%{winedll16}
%{_libdir}/wine/%{winedlldir}/dispdib.%{winedll16}
%{_libdir}/wine/%{winedlldir}/display.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/gdi.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/imm.%{winedll16}
%{_libdir}/wine/%{winedlldir}/krnl386.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/keyboard.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/lzexpand.%{winedll16}
%{_libdir}/wine/%{winedlldir}/mmsystem.%{winedll16}
%{_libdir}/wine/%{winedlldir}/mouse.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/msacm.%{winedll16}
%{_libdir}/wine/%{winedlldir}/msvideo.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2conv.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2disp.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2nls.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2prox.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2thk.%{winedll16}
%{_libdir}/wine/%{winedlldir}/olecli.%{winedll16}
%{_libdir}/wine/%{winedlldir}/olesvr.%{winedll16}
%{_libdir}/wine/%{winedlldir}/rasapi16.%{winedll16}
%{_libdir}/wine/%{winedlldir}/setupx.%{winedll16}
%{_libdir}/wine/%{winedlldir}/shell.%{winedll16}
%{_libdir}/wine/%{winedlldir}/sound.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/storage.%{winedll16}
%{_libdir}/wine/%{winedlldir}/stress.%{winedll16}
%{_libdir}/wine/%{winedlldir}/system.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/toolhelp.%{winedll16}
%{_libdir}/wine/%{winedlldir}/twain.%{winedll16}
%{_libdir}/wine/%{winedlldir}/typelib.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ver.%{winedll16}
%{_libdir}/wine/%{winedlldir}/w32sys.%{winedll16}
%{_libdir}/wine/%{winedlldir}/win32s16.%{winedll16}
%{_libdir}/wine/%{winedlldir}/win87em.%{winedll16}
%{_libdir}/wine/%{winedlldir}/winaspi.%{winedll16}
%{_libdir}/wine/%{winedlldir}/windebug.%{winedll16}
%{_libdir}/wine/%{winedlldir}/wineps16.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/wing.%{winedll16}
%{_libdir}/wine/%{winedlldir}/winhelp.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/winnls.%{winedll16}
%{_libdir}/wine/%{winedlldir}/winoldap.%{winemod16}
%{_libdir}/wine/%{winedlldir}/winsock.%{winedll16}
%{_libdir}/wine/%{winedlldir}/wintab.%{winedll16}
%{_libdir}/wine/%{winedlldir}/wow32.%{winedll}
%endif

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/nls/c_037.nls
%{_datadir}/wine/nls/c_10000.nls
%{_datadir}/wine/nls/c_10001.nls
%{_datadir}/wine/nls/c_10002.nls
%{_datadir}/wine/nls/c_10003.nls
%{_datadir}/wine/nls/c_10004.nls
%{_datadir}/wine/nls/c_10005.nls
%{_datadir}/wine/nls/c_10006.nls
%{_datadir}/wine/nls/c_10007.nls
%{_datadir}/wine/nls/c_10008.nls
%{_datadir}/wine/nls/c_10010.nls
%{_datadir}/wine/nls/c_10017.nls
%{_datadir}/wine/nls/c_10021.nls
%{_datadir}/wine/nls/c_10029.nls
%{_datadir}/wine/nls/c_10079.nls
%{_datadir}/wine/nls/c_10081.nls
%{_datadir}/wine/nls/c_10082.nls
%{_datadir}/wine/nls/c_1026.nls
%{_datadir}/wine/nls/c_1250.nls
%{_datadir}/wine/nls/c_1251.nls
%{_datadir}/wine/nls/c_1252.nls
%{_datadir}/wine/nls/c_1253.nls
%{_datadir}/wine/nls/c_1254.nls
%{_datadir}/wine/nls/c_1255.nls
%{_datadir}/wine/nls/c_1256.nls
%{_datadir}/wine/nls/c_1257.nls
%{_datadir}/wine/nls/c_1258.nls
%{_datadir}/wine/nls/c_1361.nls
%{_datadir}/wine/nls/c_20127.nls
%{_datadir}/wine/nls/c_20866.nls
%{_datadir}/wine/nls/c_20932.nls
%{_datadir}/wine/nls/c_20949.nls
%{_datadir}/wine/nls/c_21866.nls
%{_datadir}/wine/nls/c_28591.nls
%{_datadir}/wine/nls/c_28592.nls
%{_datadir}/wine/nls/c_28593.nls
%{_datadir}/wine/nls/c_28594.nls
%{_datadir}/wine/nls/c_28595.nls
%{_datadir}/wine/nls/c_28596.nls
%{_datadir}/wine/nls/c_28597.nls
%{_datadir}/wine/nls/c_28598.nls
%{_datadir}/wine/nls/c_28599.nls
%{_datadir}/wine/nls/c_28603.nls
%{_datadir}/wine/nls/c_28605.nls
%{_datadir}/wine/nls/c_437.nls
%{_datadir}/wine/nls/c_500.nls
%{_datadir}/wine/nls/c_708.nls
%{_datadir}/wine/nls/c_737.nls
%{_datadir}/wine/nls/c_720.nls
%{_datadir}/wine/nls/c_775.nls
%{_datadir}/wine/nls/c_850.nls
%{_datadir}/wine/nls/c_852.nls
%{_datadir}/wine/nls/c_855.nls
%{_datadir}/wine/nls/c_857.nls
%{_datadir}/wine/nls/c_860.nls
%{_datadir}/wine/nls/c_861.nls
%{_datadir}/wine/nls/c_862.nls
%{_datadir}/wine/nls/c_863.nls
%{_datadir}/wine/nls/c_864.nls
%{_datadir}/wine/nls/c_865.nls
%{_datadir}/wine/nls/c_866.nls
%{_datadir}/wine/nls/c_869.nls
%{_datadir}/wine/nls/c_874.nls
%{_datadir}/wine/nls/c_875.nls
%{_datadir}/wine/nls/c_932.nls
%{_datadir}/wine/nls/c_936.nls
%{_datadir}/wine/nls/c_949.nls
%{_datadir}/wine/nls/c_950.nls
%{_datadir}/wine/nls/l_intl.nls
%{_datadir}/wine/nls/locale.nls
%{_datadir}/wine/nls/normidna.nls
%{_datadir}/wine/nls/normnfc.nls
%{_datadir}/wine/nls/normnfd.nls
%{_datadir}/wine/nls/normnfkc.nls
%{_datadir}/wine/nls/normnfkd.nls
%{_datadir}/wine/nls/sortdefault.nls

%files common
%{_bindir}/notepad
%{_bindir}/winedbg
%{_bindir}/winefile
%{_bindir}/winemine
%{_bindir}/winemaker
%{_bindir}/winepath
%{_bindir}/msiexec
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/wineboot
%{_bindir}/wineconsole
%{_bindir}/winecfg
%{_mandir}/man1/wine.1*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*

%files fonts
# meta package

%if 0%{?wine_staging}
%files arial-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/arial*
%endif

%files courier-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cou*

%files fixedsys-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/*vgafix.fon

%files system-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cvgasys.fon
%{_datadir}/wine/fonts/hvgasys.fon
%{_datadir}/wine/fonts/jvgasys.fon
%{_datadir}/wine/fonts/svgasys.fon
%{_datadir}/wine/fonts/vgas1255.fon
%{_datadir}/wine/fonts/vgas1256.fon
%{_datadir}/wine/fonts/vgas1257.fon
%{_datadir}/wine/fonts/vgas874.fon
%{_datadir}/wine/fonts/vgasys.fon
%{_datadir}/wine/fonts/vgasyse.fon
%{_datadir}/wine/fonts/vgasysg.fon
%{_datadir}/wine/fonts/vgasysr.fon
%{_datadir}/wine/fonts/vgasyst.fon

%files small-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sma*
%{_datadir}/wine/fonts/jsma*

%files marlett-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/marlett.ttf

%files ms-sans-serif-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sse*
%if 0%{?wine_staging}
%{_datadir}/wine/fonts/msyh.ttf
%endif

%files tahoma-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/tahoma*ttf

%files tahoma-fonts-system
%doc README.tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%if 0%{?wine_staging}
%files times-new-roman-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/times.ttf

%files times-new-roman-fonts-system
%{_datadir}/fonts/wine-times-new-roman-fonts
%endif

%files symbol-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/symbol.ttf

%files webdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/webdings.ttf

%files webdings-fonts-system
%{_datadir}/fonts/wine-webdings-fonts

%files wingdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/wingding.ttf

%files wingdings-fonts-system
%{_datadir}/fonts/wine-wingdings-fonts

%files desktop
%{_datadir}/applications/wine-iexplore.desktop
%{_datadir}/applications/wine-inetcpl.desktop
%{_datadir}/applications/wine-joycpl.desktop
%{_datadir}/applications/wine-taskmgr.desktop
%{_datadir}/applications/wine-notepad.desktop
%{_datadir}/applications/wine-winefile.desktop
%{_datadir}/applications/wine-winemine.desktop
%{_datadir}/applications/wine-mime-msi.desktop
%{_datadir}/applications/wine.desktop
%{_datadir}/applications/wine-regedit.desktop
%{_datadir}/applications/wine-uninstaller.desktop
%{_datadir}/applications/wine-winecfg.desktop
%{_datadir}/applications/wine-wineboot.desktop
%{_datadir}/applications/wine-winhelp.desktop
%{_datadir}/applications/wine-wordpad.desktop
%{_datadir}/applications/wine-oleview.desktop
%{_datadir}/desktop-directories/Wine.directory
%config %{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/*png
%{_datadir}/icons/hicolor/scalable/apps/*svg

%files systemd
%config %{_binfmtdir}/wine.conf

# ldap subpackage
%files ldap
%{_libdir}/wine/%{winedlldir}/wldap32.%{winedll}

# cms subpackage
%files cms
%{_libdir}/wine/%{winedlldir}/mscms.%{winedll}

# twain subpackage
%files twain
%{_libdir}/wine/%{winedlldir}/twain_32.%{winedll}
%{_libdir}/wine/%{winesodir}/sane.so
%{_libdir}/wine/%{winedlldir}/sane.%{wineds}

%files devel
%{_bindir}/function_grep.pl
%{_bindir}/widl
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winedump
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/wmc
%{_bindir}/wrc
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/winemaker.1*
%attr(0755, root, root) %dir %{_includedir}/wine
%{_includedir}/wine/*
%{_libdir}/wine/%{winesodir}/*.a
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/*.a
%endif

%files pulseaudio
%{_libdir}/wine/%{winesodir}/winepulse.so
%{_libdir}/wine/%{winedlldir}/winepulse.%{winedrv}

%files alsa
%{_libdir}/wine/%{winesodir}/winealsa.so
%{_libdir}/wine/%{winedlldir}/winealsa.%{winedrv}

%files opencl
%{_libdir}/wine/%{winesodir}/opencl.so
%{_libdir}/wine/%{winedlldir}/opencl.%{winedll}


%changelog
* Mon Jul 24 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.13-100
- 8.13

* Sun Jul 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.12-100
- 8.12

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.11-100.20230629git3d28f9d
- 8.11

* Sun Jun 11 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.10-100
- 8.10

* Sat May 27 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.9-100
- 8.9

* Sun May 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.8-100
- 8.8
- Disable shared GPU resources again

* Mon May 08 2023 Phantom X <megaphantomx at hotmail dot com>  - 1:8.7-100.20230505git222d20a
- 8.7
- Reenable shared GPU resources

* Sun Apr 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.6-100
- 8.6
- Disable shared GPU resources, it needs rebase

* Mon Apr 03 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.5-100
- 8.5

* Tue Mar 21 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.4-100.20230320gitfd99bd4
- 8.4

* Tue Mar 07 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.3-100.20230307git50f5f9a
- 8.3
- tkg sync and cleanup

* Mon Feb 20 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.2-100
- 8.2

* Fri Feb 03 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.1-100
- 8.1

* Wed Jan 25 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.0-100.20230124gitbe57ebe
- 8.0

* Fri Jan 20 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.0~rc5-100
- 8.0-rc5
- Shared GPU resources patchset

* Sun Jan 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.0~rc4-100
- 8.0-rc4

* Sun Jan 08 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.0~rc3-100
- 8.0-rc3

* Fri Dec 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1:8.0~rc2-100.20221222gitd059dd1
- 8.0-rc2

* Sun Dec 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1:8.0~rc1-100
- 8.0-rc1

* Sun Nov 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.22-100
- 7.22

* Mon Nov 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.21-100
- 7.21

* Wed Nov 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.20-100.20221101git7be72ce
- 7.20

* Tue Oct 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.19-100.20221017git03f5f72
- 7.19

* Sat Sep 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.18-100
- 7.18

* Sat Sep 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.17-100
- 7.17

* Mon Aug 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.16-100
- 7.16

* Sun Aug 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.15-100
- 7.15

* Sun Aug 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.14-103.202200805gitbfc73b0
- mfplat streaming updates

* Sun Aug 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.14-102.202200805gitbfc73b0
- Snapshot

* Sun Jul 31 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.14-101
- Remove upstream fixed patch

* Sat Jul 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.14-100
- 7.14

* Sat Jul 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.13-101.20220722git7b77b4e
- Snapshot

* Sat Jul 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.13-100
- 7.13

* Sat Jul 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.12-101.20220708git7b79e3a
- Snapshot

* Sat Jul 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.12-100
- 7.12

* Sat Jun 25 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.11-101.20220624gitaf8ed02
- Snapshot

* Sat Jun 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.11-100
- 7.11

* Sat Jun 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.10-101.20220610git35939bb
- Snapshot

* Sat Jun 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.10-100
- 7.10

* Mon May 30 2022 Phantom X - 1:7.9-102.20220527gitd928668
- Forgotten last snapshot

* Sat May 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.9-101.20220526gitd3378c1
- Snapshot

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.8-101.20220513git5aa9340
- Snapshot

* Sat May 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.8-100
- 7.8

* Tue May 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.7-102.20220502gitf91f434
- fastsync

* Sat Apr 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.7-101.20220428git64b96ee
- Snapshot

* Sat Apr 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.7-100
- 7.7

* Sat Apr 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.6-102.20220415gite254680
- Bump

* Tue Apr 12 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.6-101.20220411git02faaea
- Snapshot

* Sat Apr 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.6-100
- 7.6

* Mon Apr 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.5-101.20220401git0de8d01
- Snapshot

* Sat Mar 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.5-100
- 7.5

* Mon Mar 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-103.20220318git47b02e8
- Weekend bump

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-102.20220315git670a1e8
- tkg updates

* Tue Mar 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-101.20220314git8a52d3e
- Snapshot

* Sun Mar 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-100
- 7.4

* Sat Mar 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-103.20220304git18230d2
- Bump

* Wed Mar 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-102.20220301git89a8b32
- Snapshot

* Sun Feb 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-101
- Update tkg patches

* Sat Feb 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-100
- 7.3

* Tue Feb 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.2-102.20220221git53cb28e
- Bump to get staging restored mfplat streaming support

* Mon Feb 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.2-101.20220218gitbf42dca
- Snapshot
- Use mfplat patch from Proton-GE, cleaning all reverts

* Mon Feb 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.2-100
- 7.2
- Disable fastsync for the time

* Tue Feb 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.1-102.20220207git54b8c8c
- Bump
- wine-mono 7.1.2
- mfplat streaming restoring optional support

* Sun Feb 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.1-101.20220204git4364ff8
- Snapshot

* Sat Jan 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.1-100
- 7.1

* Sat Jan 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0-101.20220121gitc09a5da
- Snapshot

* Tue Jan 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0-100
- 7.0

* Sat Jan 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc6-100
- 7.0-rc6

* Sat Jan 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc5-100
- 7.0-rc5

* Mon Jan 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc4-100
- 7.0-rc4

* Fri Dec 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc3-101.20211230gitb6dc839
- Snapshot

* Mon Dec 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc3-100
- 7.0-rc3

* Sat Dec 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-103.20211223git7555573
- Bump

* Tue Dec 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-102.20211220git656d7f5
- Snapshot

* Mon Dec 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-101
- Add some pending hotfixes

* Sat Dec 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-100
- 7.0-rc2

* Sat Dec 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc1-100
- 7.0-rc1
- fastsync optional support

* Sun Dec 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.23-100
- 6.23

* Sat Nov 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.22-102.20211126gitf03933f
- Snapshot

* Tue Nov 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.22-101
- Disable extfaudio

* Sat Nov 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.22-100
- 6.22

* Wed Nov 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-103.20211116gitb65ef71
- Bump

* Sat Nov 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-102.20211112gitbe0684d
- Bump

* Wed Nov 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-101.20211109git6a072b9
- Snapshot

* Sat Nov 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-100
- 6.21

* Tue Nov 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.20-102.20211101git0b79e2c
- futex_waitv support

* Sat Oct 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.20-101.20211029git5f93c68
- Snapshot
- Obsoletes wine-capi packages

* Mon Oct 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.20-100
- 6.20
- Add reverts for external FAudio and mfplat

* Wed Oct 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.19-101.20211012git50f889f
- Snapshot

* Sat Oct 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.19-100
- 6.19

* Wed Oct 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-104.20211005gited38d12
- Bump

* Mon Oct 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-103.20211004git5a8dcb0
- Bump

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-102.20211001gita87abdb
- Snapshot

* Sat Sep 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-101
- Add some fixes in review

* Sat Sep 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-100
- 6.18

* Mon Sep 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.17-101.20210917git16e73be
- Snapshot

* Sat Sep 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.17-100
- 6.17

* Sat Sep 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.16-101.20210903git8b9f1e1
- Snapshot

* Sat Aug 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.16-100
- 6.16

* Sat Aug 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.15-101.20210820git7d60044
- Snapshot

* Sat Aug 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.15-100
- 6.15

* Tue Aug 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.14-102.20210809gitcaf5ab5
- Bump

* Sat Aug 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.14-101.20210806git2cc98b7
- Snapshot

* Sat Jul 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.14-100
- 6.14

* Tue Jul 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.13-102.20210726gitf1023b4
- Bump

* Fri Jul 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.13-101.20210722gitc518a53
- Snapshot

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.13-100
- 6.13

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-105.20210719gitd60c450
- Bump

* Sat Jul 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-104.20210709git49cde09
- Weekend snapshot

* Fri Jul 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-103.20210708gitd10887b
- Bump

* Tue Jul 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-102.20210705git14f03e8
- Snapshot with some server fixes

* Sat Jul 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-101
- Staging update

* Fri Jul 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-100
- 6.12

* Sun Jun 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.11-102.20210625git542175a
- Snapshot
- Add dosbox alternate binary patch

* Sun Jun 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.11-101
- tkg update

* Sat Jun 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.11-100
- 6.11
- Add offline vk.xml for make_vulkan

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-104.20210611gitf5bd0be
- Bump

* Thu Jun 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-103.20210609git2a505ef
- Snapshot

* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-102
- Add some fixes from Proton GE

* Sun Jun 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-101
- Revert commits breaking joystick

* Sat Jun 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-100
- 6.10
- Add rt prio and net raw capabilitiess

* Sat May 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-103.20210528git35180d3
- Bump

* Wed May 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-102.20210525git8ddff3f
- Staging update again

* Tue May 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-101.20210524git94eb8d3
- Snapshot

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-100
- 6.9

* Sat May 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.8-100
- 6.8
- Disable childwindow patch, since nine crashes with it

* Tue May 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-105.20210503git3ba4412
- Update

* Sun May 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-104.20210430git2deb8c2
- Staging update
- tkg update

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-103.20210430git2deb8c2
- Update
- More architecture-specific updates

* Wed Apr 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-102.20210427git4ccf749
- Bump

* Tue Apr 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-101.20210426gitd7feceb
- Snapshot
- Architecture-specific updates

* Sat Apr 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-100
- 6.7
- BR: gmp (wine-tkg-proton-bcrypt)

* Sat Apr 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.6-101.20210416git749f8c2
- Snapshot

* Mon Apr 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.6-100
- 6.6
- Patchsets review, fshack can be enabled now

* Mon Apr 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.5-102.20210402git2fcc1d0
- Bug#50914 fix

* Sat Apr 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.5-101.20210402git2fcc1d0
- Snapshot
- wine-mono 6.1.1

* Sun Mar 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.5-100
- 6.5

* Wed Mar 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.4-102.20210323gitf69c8f0
- Bump

* Sat Mar 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.4-101.20210319git41df83c
- Snapshot

* Sun Mar 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.4-100
- 6.4

* Sat Mar 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.3-101.20210305git5bccf6f
- Snapshot

* Sat Feb 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.3-100
- 6.3

* Sat Feb 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.2-101.20210219git4de079b
- Snapshot

* Sat Feb 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.2-100
- 6.2

* Sat Feb 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.1-102.20210205git4f1b297
- Snapshot

* Mon Feb 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.1-101
- mfplat fix

* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.1-100
- 6.1

* Fri Jan 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-106.20210128gitf72ef20
- Update

* Tue Jan 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-105.20210125git2d6462c
- Bump
- BR: libudev

* Tue Jan 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-104.20210118git88220e0
- tkg update

* Mon Jan 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-103.20210115git00401d2
- Pass -fno-tree-dce only to affected objects

* Mon Jan 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-102.20210115git00401d2
- Disable ntdll-NtAlertThreadByThreadId

* Mon Jan 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-101.20210115git00401d2
- Snapshot

* Fri Jan 15 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-100
- 6.0

* Sat Jan 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc6-100
- 6.0-rc6

* Mon Jan 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc5-101
- Revert some staging patches

* Sun Jan 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc5-100
- 6.0-rc5

* Sat Dec 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc4-100
- 6.0-rc4

* Thu Dec 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc3-101.20201224git9d7a710
- Snapshot

* Sat Dec 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc3-100
- 6.0-rc3

* Thu Dec 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:6.0~rc2-101.20201217gitef876fc
- Snapshot and staging fixes

* Sun Dec 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc2-100
- 6.0-rc2

* Wed Dec 09 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc1-101.20201209git3100197
- Snapshot

* Sat Dec 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc1-100
- 6.0-rc1

* Thu Dec 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.22-102.20201202gite4fbae8
- New snapshot

* Sat Nov 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.22-101.20201127gitcbca9f8
- Snapshot

* Sat Nov 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.22-100
- 5.22

* Sun Nov 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.21-101.20201113gitcf49617
- Snapshot
- Remove glu BR

* Sat Nov 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.21-100
- 5.21

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.20-101.20201030git03eaa2c
- Snapshot

* Sat Oct 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.20-100
- 5.20

* Tue Oct 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-103.20201016git0c249e6
- tkg updates. fsync reverts unneeded

* Fri Oct 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-102.20201016git0c249e6
- Snapshot

* Mon Oct 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-101
- tkg sync

* Sat Oct 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-100
- 5.19

* Wed Oct 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-103.20201006gitc29f9e6
- Bump

* Sun Oct 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-102.20201002gitcce4f36
- Snapshot

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-101
- Staging update

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-100
- 5.18

* Wed Sep 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.17-101.20200915git26eedec
- Snapshot

* Sat Sep 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.17-100
- 5.17
- tkg updates

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.16-101.20200904git432858b
- Snapshot

* Sun Aug 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.16-100
- 5.16

* Thu Aug 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-104.20200826git666f614
- New snapshot

* Sat Aug 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-103.20200821gitab94abb
- Bump

* Wed Aug 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-102.20200818git8f3bd63
- Snapshot

* Mon Aug 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-101
- Staging update

* Sun Aug 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-100
- 5.15

* Sat Aug 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-103.20200807git1ec8bf9
- New snapshot

* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-102.20200806git8cbbb4f
- Bump

* Wed Aug 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-101.20200804git2b76b9f
- Snapshot

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-100
- 5.14
- New Webdings font

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.13-102.20200724git0d42388
- nofshack fixes

* Sat Jul 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.13-101.20200724git0d42388
- Snapshot

* Sun Jul 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.13-100
- 5.13

* Wed Jul 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-103.20200714git54b2a10
- Bump

* Mon Jul 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-102.20200713gitcaa41d4
- Snapshot

* Mon Jul 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-101
- Staging update

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-100
- 5.12

* Thu Jul 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-103.20200701git10b1793
- Bump

* Sat Jun 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-102.20200626git13b2587
- New snapshot and more fsync reverts

* Mon Jun 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-101
- tkg and ge minor updates

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-100
- 5.11

* Tue Jun 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.10-106.20200615git634cb77
- New snapshot

* Sun Jun 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-105.20200612git948a6a4
- Bump

* Thu Jun 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-104.20200610git3430431
- New snapshot

* Wed Jun 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-103.20200609gitbf454cc
- Bump

* Tue Jun 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-102.20200608git1752958
- Snapshot
- wine-mono 5.1.0

* Mon Jun 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-101
- Staging update

* Sat Jun 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-100
- 5.10

* Thu Jun 04 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.9-102.20200603gitaba27fd
- Bump

* Wed Jun 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.9-101.20200602git48020f4
- Snapshot and tkg reverts

* Sat May 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.9-100
- 5.9

* Wed May 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-105.20200515git4358ddc
- Fix wine-mono patch

* Tue May 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-104.20200515git3bb824f
- New snapshot
- wine-mono 5.0.1

* Sat May 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-103.20200515git9e26bc8
- Bump

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-102.20200513gitdebe646
- Snapshot

* Mon May 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-101
- Bug#49109/49128 better fix

* Sat May 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-100
- 5.8

* Thu May 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-108.20200506git148fc1a
- Bump
- Revert some upstream patches to fix 64 bit Unity3D games

* Tue May 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-107.20200504git4e2ad33
- New snapshot

* Sat May 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-106.20200501gitd1f858e
- Disable fshack again, not good yet
- Bump

* Fri May 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-105.20200430git0c27d24
- New snapshot
- Patchsets review
- Reenable fshack

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-104.20200428git7ccc45f
- Bump and tkg reverts

* Tue Apr 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-103.20200427git28ec279
- Again

* Tue Apr 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-102.20200427git28ec279
- Snapshot

* Sun Apr 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-101
- Bug 49011 fix

* Sat Apr 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-100
- 5.7

* Thu Apr 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-104.20200422gitf52b33c
- Bump

* Tue Apr 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-103.20200420gitf31a29b
- New snapshot
- winemono 5.0.0

* Sun Apr 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-102.20200417git59987bc
- Bump

* Wed Apr 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-101.20200415gitf6c131f
- Snapshot

* Sat Apr 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-100
- 5.6

* Fri Apr 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.5-102.20200402git3047385
- Snapshot

* Mon Mar 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.5-101
- Staging fixes
- Revert server timeout disabled by proton-tkg-staging patch

* Sun Mar 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.5-100
- 5.5
- New tkg links

* Wed Mar 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.4-102.20200324git9c190f8
- Bump

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.4-101.20200320git3ddf3a7
- Snapshot
- Disable some compilation flags

* Sat Mar 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.4-100
- 5.4

* Wed Mar 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-103.20200310git4dfd5f2
- Bump

* Sat Mar 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-102.20200306giteb63713
- Bump

* Thu Mar 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-101.20200304git0eea1b0
- Snapshot

* Sat Feb 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-100
- 5.3

* Fri Feb 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.2-102.20200227gitc6b852e
- Bump
- BR: libgcrypt

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.2-101.20200221gitb253bd6
- Snapshot

* Sun Feb 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.2-100
- 5.2

* Tue Feb 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.1-102.20200210git0df9cce
- New snapshot
- tkg sync
- FS hack switch, disabled for the time

* Sun Feb 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.1-101.20200207gitf909d18
- New snapshot

* Sun Feb 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.1-100
- 5.1

* Tue Jan 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-100
- 5.0

* Sat Jan 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc6-100
- 5.0-rc6

* Wed Jan 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc5-101.20200114git9f8935d
- New snapshot

* Sat Jan 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc5-100
- 5.0-rc5

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc4-100
- 5.0-rc4

* Wed Jan 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc3-100.20191230git5034d10
- 5.0-rc3

* Sat Dec 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc2-100
- 5.0-rc2

* Sat Dec 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc1-100
- 5.0-rc1

* Thu Dec 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.21-102.20191211git750d382
- New snapshot
- wine-gecko 2.47.1
- Fix gtk3 requires when disabled

* Fri Dec 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.21-101.20191205git7ca1c49
- Snapshot

* Sat Nov 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.21-100
- 4.21

* Thu Nov 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.20-102.20191127git4ccdf3e
- Snapshot

* Thu Nov 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.20-101.20191120gitaa3d01e
- Snapshot

* Sat Nov 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.20-100
- 4.20

* Tue Nov 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-105.20191112git292b728
- New snapshot, again

* Thu Nov 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-104
- Revert to release

* Thu Nov 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-103.20191106gitf205838
- Try to fix last one

* Wed Nov 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-102.20191105git7f469b6
- New snapshot
- Patchsets review. All extra patches applied only with staging

* Mon Nov 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-101
- Update revert list

* Sat Nov 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-100
- 4.19

* Sat Oct 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.18-100
- 4.18

* Mon Oct 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-103.20191009git71e96bd
- New snapshot
- R: gstreamer1-plugins-good

* Thu Oct 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-102.20191002git5e8eb5f
- Snapshot

* Sun Sep 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-101
- tkg updates and some reverts

* Sat Sep 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-100
- 4.17
- Retire deprecated isdn4k-utils support

* Wed Sep 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-102
- tkg updates

* Sun Sep 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-101
- tkg updates

* Sat Sep 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-100
- 4.16
- raw-input switch

* Sun Sep 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.15-101
- Disable raw-input

* Sat Aug 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.15-100
- 4.15

* Tue Aug 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-103
- tkg updates

* Fri Aug 23 2019 Phantom X <megaphantomx at bol dot com dot br>  - 1:4.14-102
- tkg updates

* Mon Aug 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-101
- Missing patch
- Deprecate old unmaintained patches

* Sat Aug 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-100
- 4.14

* Fri Aug 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.13-101
- Upstream and tkg updates
- Mono update

* Sat Aug 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.13-100
- 4.13

* Tue Jul 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-105
- Staging and tkg updates

* Fri Jul 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-104
- Try again

* Thu Jul 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-103
- Something broke

* Wed Jul 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-102
- Update staging patchset
- Raw input fix by Guy1524

* Sun Jul 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-101
- mingw build
- gtk3 switch, disabled by default

* Sun Jul 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-100
- 4.12.1

* Sat Jul 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12-100
- 4.12
- f30 sync

* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.11-100
- 4.11

* Sat Jun 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.10-101
- Monotonic patch update from tkg

* Mon Jun 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.10-100
- 4.10

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.9-101
- Some fixes from bugzilla

* Sat May 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.9-100
- 4.9

* Tue May 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-102
- Trim down reverts
- Update staging
- chinforpms experimental message and README
- Trim changelog

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-101
- Revert some upstream patches to fix joystick issues
- Revert staging patch to fix symlink issues

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-100
- 4.8

* Thu May 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.7-101
- no-PIC flags patches from upstream

* Mon Apr 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.7-100
- 4.7

* Thu Apr 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.6-101
- wine-mono 4.8.2

* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.6-100
- 4.6
- esync merged with staging

* Sat Mar 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.5-100
- 4.5

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-103
- Revert xaudio2_7 application name patch, new one fail

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-102
- Replace xaudio2_7 application name with pulseaudio patch

* Mon Mar 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-101
- Some FAudio updates from Valve git

* Sun Mar 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-100
- 4.4

* Mon Mar 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.3-101
- Upstream fixes for whq#42982 and whq#43071

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.3-100
- 4.3
- pkgconfig style BRs
- Upstream FAudio support

* Mon Feb 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.2-101
- faudio update from tkg

* Sun Feb 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.2-100
- 4.2
- Add -ftree-vectorize -ftree-slp-vectorize to CFLAGS

* Mon Feb 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.1-100
- 4.1

* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0-101
- Optional enabled FAudio support. Obsoletes wine-xaudio and wine-freeworld
- Remove old Fedora and RH conditionals, only current Fedora is supported

* Tue Jan 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0-100
- 4.0

* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc7-101
- Patch to fix wine-dxup build

* Sat Jan 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc7-100
- 4.0-rc7

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc6-100
- 4.0-rc6
- Revert -O1 optimizations, seems good now
- Disable mime type registering

* Mon Jan 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc5-101
- Fix includedir

* Sat Jan 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc5-100
- 4.0-rc5

* Sun Dec 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc4-100
- 4.0-rc4

* Sat Dec 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc3-100
- 4.0-rc3

* Tue Dec 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc2-101
- Some Tk-Glitch patches, including optional esync

* Mon Dec 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc2-100
- 4.0-rc2

* Sat Dec 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc1-100
- 4.0-rc1

* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.21-100
- 3.21
- Disable broken wine-pba
- Change rc versioning to "~" system

* Fri Nov 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.20-100.chinfo
- 3.20

* Mon Oct 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.19-100.chinfo
- 3.19

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.18-100.chinfo
- 3.18

* Sun Sep 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.17-100.chinfo
- 3.17

* Thu Sep 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.16-100.chinfo
- 3.16

* Thu Sep 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-104.chinfo
- More upstream fixes
- Change compiler optimizations to -O1 to fix whq#45199

* Sat Sep 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-103.chinfo
- Try again again

* Fri Sep 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-102.chinfo
- Try again

* Thu Sep 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-101.chinfo
- Random upstream patches

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-100.chinfo
- 3.15

* Mon Aug 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-103.chinfo
- Revert pulseaudio fixes

* Mon Aug 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-102.chinfo
- wine-pba patches
- Try new pulseaudio fixes
- license macros

* Fri Aug 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-101.chinfo
- Virtual desktop fix

* Mon Aug 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-100.chinfo
- 3.14

* Sun Aug 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-102.chinfo
- Staging update

* Sun Jul 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-101.chinfo
- Revert to old staging winepulse patches

* Sat Jul 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-100.chinfo
- 3.13
- Clean xaudio2 package, only xaudio2_7.dll.so is needed

* Tue Jul 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.12-100.chinfo
- 3.12
- Split xaudio2, for freeworld packages support

* Sun Jun 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.11-100.chinfo
- 3.11

* Mon Jun 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.10-100.chinfo
- 3.10

* Sat May 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.9-100.chinfo
- 3.9
- BR: vkd3d-devel
- f28 sync

* Sat May 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.8-100.chinfo
- 3.8

* Sat Apr 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.7-100.chinfo
- 3.7

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-102.chinfo
- Revert ARMv7 fix.

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-101.chinfo
- f28 sync

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-100.chinfo
- 3.6

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.5-100.chinfo
- 3.5

* Fri Mar 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.4-100.chinfo
- 3.4

* Sun Mar 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.3-100.chinfo
- 3.3
- Updated URLs
- New wine-staging URL
- s/compholio/staging/
- BR: samba-devel
- BR: SDL2-devel
- BR: vulkan-devel
- R: samba-libs
