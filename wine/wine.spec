%global commit aa8621d2fdb121619f677396733e88176ce6aedc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250430
%bcond_with snapshot

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
%define _fortify_level 0

# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%undefine _auto_set_build_flags
%undefine _package_note_file
%undefine _annotated_build

# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%global _lto_cflags %{nil}

%global winepedir_i386 i386-windows
%global winesodir_i386 i386-unix
%global winepedir_x86_64 x86_64-windows
%global winesodir_x86_64 x86_64-unix
%ifarch %{ix86}
%global winepedir %{winepedir_i386}
%global winesodir %{winesodir_i386}
%endif
%ifarch x86_64
%global winepedir %{winepedir_x86_64}
%global winesodir %{winesodir_x86_64}
%endif
%ifarch aarch64
%global winepedir aarch64-windows
%global winesodir aarch64-unix
%global __brp_llvm_compile_lto_elf %nil
%global __brp_strip_lto %nil
%global __brp_strip_static_archive %nil
%endif

# Package mingw files with debuginfo
%global with_debug 0
%global no64bit   0
%global winegecko 2.47.4
%global winemono  10.1.0
%global winevulkan 1.4.318
%if 0%{?fedora}
%global opencl    1
%endif

%global winecapstone 5.0.3
%global wineFAudio 25.06
%global winefluidsynth 2.4.0
%global winegsm 1.0.19
%global winejpeg 9~f
%global winelcms2 2.17
%global wineldap 2.5.18
%global winempg123 1.33.0
%global winepng 1.6.48
%global wineopenldap 2.5.17
%global winetiff 4.7.0
%global winejxrlib 1.1
%global winevkd3d 1.16
%global winexml2 2.12.8
%global winexslt 1.1.43
%global winezlib 1.3.1
%global winezydis 4.1.0

%global _default_patch_fuzz 2


# build with staging-patches, see:  https://wine-staging.com/
# 1 to enable; 0 to disable.
%global wine_staging 1
%global wine_stagingver 10.10
%global wine_stg_url https://gitlab.winehq.org/wine/wine-staging
%if 0%(echo %{wine_stagingver} | grep -q \\. ; echo $?) == 0
%global strel v
%global stpkgver %{wine_stagingver}
%else
%global stpkgver %(c=%{wine_stagingver}; echo ${c:0:7})
%endif
%global ge_id 93139bc89acfb55755d0382ded255d90671ef5bf
%global ge_url https://github.com/GloriousEggroll/proton-ge-custom/raw/%{ge_id}/patches

%global tkg_id 320c3c0388ca30301ea92a9a4a5f2eb4987f3acf
%global tkg_url https://github.com/Frogging-Family/wine-tkg-git/raw/%{tkg_id}/wine-tkg-git/wine-tkg-patches
%global tkg_cid a6a468420c0df18d51342ac6864ecd3f99f7011e
%global tkg_curl https://github.com/Frogging-Family/community-patches/raw/%{tkg_cid}/wine-tkg-git

%if 0%{?wine_staging}
%global cap_st cap_sys_nice,
%endif

%global perms_pldr %caps(cap_net_raw+eip)
%global perms_srv %caps(%{?cap_st}cap_net_raw+eip)

# ntsync (disables fsync, needs full patched modules and kernel-headers)
%bcond_without ntsync
# proton FS hack (wine virtual desktop with DXVK is not working well)
%bcond_with fshack
%bcond_without ge_wayland
%bcond_without proton_mf
%bcond_without proton_winevulkan

# Enable when needed
%bcond_with patchutils

%if %{with fshack}
%global wine_staging_opts %{?wine_staging_opts} -W winex11-WM_WINDOWPOSCHANGING -W winex11-_NET_ACTIVE_WINDOW
%endif

%global whq_url  https://source.winehq.org/git/wine.git/patch
%global whq_murl  https://gitlab.winehq.org/wine/wine
%global whqs_url  https://source.winehq.org/patches/data
%global valve_url https://github.com/ValveSoftware/wine
%global vk_url https://raw.githubusercontent.com/KhronosGroup/Vulkan-Docs/v%{winevulkan}/xml

%global staging_banner Chinforpms Staging

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global vermajor %%(echo %%{ver} | cut -d. -f1)
%global verminor %%(echo %%{ver} | cut -d. -f2 | cut -d- -f1)

Name:           wine
# If rc, use "~" instead "-", as ~rc1
Version:        10.10
Release:        100%{?dist}
Summary:        A compatibility layer for windows applications

Epoch:          2

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
Source8:        wine-README-chinforpms-fsync
Source9:        wine-README-chinforpms-ntsync

Source50:       %{vk_url}/vk.xml#/vk-%{winevulkan}.xml
Source51:       %{vk_url}/video.xml#/video-%{winevulkan}.xml

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
Source114:      wine-desk.desktop

# AppData files
Source150:      wine.appdata.xml

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

Source250:      ntsync.modules

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
#Patch???:      %%{whq_murl}/-/commit/<commit>.patch#/%%{name}-whq-<commit>.patch
Patch700:        %{whq_murl}/-/commit/bd89ab3040e30c11b34a95072d88f635ade03bdc.patch#/%{name}-whq-bd89ab3.patch
Patch701:        %{whq_murl}/-/commit/240556e2b8cb94fc9cc85949b7e043f392b1802a.patch#/%{name}-whq-240556e.patch
Patch702:        %{whq_murl}/-/commit/2bfe81e41f93ce75139e3a6a2d0b68eb2dcb8fa6.patch#/%{name}-whq-2bfe81e.patch
Patch703:        %{whq_murl}/-/merge_requests/6072.patch#/%{name}-whq-mr6072.patch
Patch704:        0001-mr6072-fixup-1.patch
Patch705:        0001-mr6072-fixup-2.patch

# wine staging patches for wine-staging
Source900:       %{wine_stg_url}/-/archive/%{?strel}%{wine_stagingver}/wine-staging-%{stpkgver}.tar.bz2

# https://github.com/Tk-Glitch/PKGBUILDS/wine-tkg-git/wine-tkg-patches
Patch1000:       FS_bypass_compositor.patch
Patch1001:       %{tkg_url}/misc/CSMT-toggle/CSMT-toggle.patch#/%{name}-tkg-CSMT-toggle.patch

# fsync
Patch1020:       %{tkg_url}/proton/fsync/fsync-unix-staging.patch#/%{name}-tkg-fsync-unix-staging.patch
Patch1021:       %{tkg_url}/proton/fsync/fsync_futex_waitv.patch#/%{name}-tkg-fsync_futex_waitv.patch
# FS Hack
Patch1023:       %{tkg_url}/proton/valve_proton_fullscreen_hack/valve_proton_fullscreen_hack-staging.patch#/%{name}-tkg-valve_proton_fullscreen_hack-staging.patch
Patch1026:       %{tkg_url}/proton/LAA/LAA-unix-staging.patch#/%{name}-tkg-LAA-unix-staging.patch
Patch1027:       %{tkg_url}/proton-tkg-specific/proton-tkg/staging/proton-tkg-staging.patch#/%{name}-tkg-proton-tkg-staging.patch
Patch1028:       %{tkg_url}/proton-tkg-specific/proton-tkg/proton-tkg-additions.patch#/%{name}-tkg-proton-tkg-additions.patch
Patch1029:       %{tkg_url}/proton-tkg-specific/proton-cpu-topology-overrides/proton-cpu-topology-overrides.patch#/%{name}-tkg-proton-cpu-topology-overrides.patch
Patch1030:       %{tkg_url}/proton/proton-win10-default/proton-win10-default.patch#/%{name}-tkg-proton-win10-default.patch
Patch1031:       %{tkg_url}/hotfixes/proton_fs_hack_staging/remove_hooks_that_time_out2.mypatch#/%{name}-tkg-remove_hooks_that_time_out2.patch
Patch1034:       %{tkg_url}/hotfixes/GetMappedFileName/Return_nt_filename_and_resolve_DOS_drive_path.mypatch#/%{name}-tkg-Return_nt_filename_and_resolve_DOS_drive_path.patch
Patch1035:       %{tkg_url}/hotfixes/08cccb5/a608ef1.mypatch#/%{name}-tkg-a608ef1.patch
Patch1036:       %{tkg_url}/hotfixes/NosTale/nostale_mouse_fix.mypatch#/%{name}-tkg-nostale_mouse_fix.patch
Patch1037:       %{tkg_url}/hotfixes/shm_esync_fsync/HACK-user32-Always-call-get_message-request-after-waiting.mypatch#/%{name}-tkg-HACK-user32-Always-call-get_message-request-after-waiting.patch
Patch1038:       %{tkg_url}/proton/proton-mf-patch/gstreamer-patch1.patch#/%{name}-tkg-gstreamer-patch1.patch
Patch1039:       %{tkg_url}/proton/proton-mf-patch/gstreamer-patch2.patch#/%{name}-tkg-gstreamer-patch2.patch
Patch1040:       %{tkg_url}/proton/proton-winevulkan/proton10-winevulkan.patch#/%{name}-tkg-proton10-winevulkan.patch
Patch1041:       %{tkg_url}/misc/winewayland/ge-wayland.patch#/%{name}-tkg-ge-wayland.patch

Patch1051:       %{tkg_url}/proton-tkg-specific/proton-tkg/staging/proton-tkg-staging-nofsync.patch#/%{name}-tkg-proton-tkg-staging-nofsync.patch
Patch1052:       %{tkg_url}/misc/fastsync/ntsync5-staging-protonify.patch#/%{name}-tkg-ntsync5-staging-protonify.patch
Patch1053:       %{tkg_url}/misc/fastsync/ntsync-config.h.in-alt.patch#/%{name}-tkg-ntsync-config.h.in-alt.patch
Patch1055:       0001-tkg-cpu-topology-fixup-1.patch
Patch1056:       0001-tkg-cpu-topology-fixup-2.patch

Patch1090:       0001-fshack-revert-grab-fullscreen.patch
Patch1091:       %{valve_url}/commit/e277c9f152d529894bb78260553970d9b276a5d4.patch#/%{name}-valve-e277c9f.patch
Patch1092:       %{valve_url}/commit/52c401612a5c11fad63d3860f1b3b7d38fde387b.patch#/%{name}-valve-52c4016.patch
Patch1093:       %{valve_url}/commit/541b9e83ccb766d28d29ada3012cd8c7a8b9c6ee.patch#/%{name}-valve-541b9e8.patch

Patch1301:       0001-FAudio-Disable-reverb.patch
Patch1302:       0001-PSO2-fix.patch
Patch1303:       0001-mfplat-custom-fixes-from-proton.patch
Patch1304:       0001-proton-gstreamer-fixup-1.patch

# Patch the patch
Patch5000:      0001-chinforpms-message.patch

# END of staging patches

%if !0%{?no64bit}
# Fedora 36 Clang doesn't build PE binaries on ARM at the moment
# Wine 9.15 and higher requires ARM MinGW binaries (dlltool)
ExclusiveArch:  %{ix86} x86_64
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
# mingw-binutils 2.35 or patched 2.34 is needed to prevent crashes
BuildRequires:  mingw32-binutils >= 2.34-100
BuildRequires:  mingw64-binutils >= 2.34-100
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  fontforge
BuildRequires:  icoutils
%if %{with patchutils}
BuildRequires:  patchutils
%endif
BuildRequires:  perl-generators
BuildRequires:  python3
BuildRequires:  pkgconfig(alsa)
BuildRequires:  cups-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(egl)
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
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  libieee1284-devel
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  librsvg2
BuildRequires:  librsvg2-tools
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(netapi)
%if 0%{?opencl}
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  opencl-headers
%endif
BuildRequires:  pkgconfig(odbc)
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
%if %{with ntsync}
BuildRequires:  kernel-headers >= 6.14
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
%if 0%{?opencl}
Requires:       wine-opencl(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif
Recommends:     wine-dxvk(x86-32)
Recommends:     dosbox-staging
Recommends:     isdn4k-utils(x86-32)

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?opencl}
Requires:       wine-opencl(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       mesa-dri-drivers(x86-64)
%endif
Recommends:     wine-dxvk(x86-64)
Recommends:     dosbox-staging
Recommends:     isdn4k-utils(x86-64)

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?opencl}
Requires:       wine-opencl(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
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
Requires:       (wine-wow32 = %{?epoch:%{epoch}:}%{version}-%{release} if wine-core(x86-64))
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
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
Requires:       libXxf86vm(x86-32)
Requires:       libpcap(x86-32)
Requires:       libv4l(x86-32)
Requires:       unixODBC(x86-32)
Requires:       samba-libs(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
Requires:       libva(x86-32)
Recommends:     gstreamer1-plugins-ugly(x86-32)
%endif
%endif

%ifarch x86_64
Requires:       (wine-wow64 = %{?epoch:%{epoch}:}%{version}-%{release} if wine-core(x86-32))
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
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
Requires:       libXxf86vm(x86-64)
Requires:       libpcap(x86-64)
Requires:       libv4l(x86-64)
Requires:       unixODBC(x86-64)
Requires:       samba-libs(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
Requires:       libva(x86-64)
Recommends:     gstreamer1-plugins-ugly(x86-64)
%endif
%endif

%ifarch aarch64
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
Requires:       libXrender
Requires:       libpcap
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan-loader
%if 0%{?wine_staging}
Requires:       libva
Recommends:     gstreamer1-plugins-ugly
%endif
%endif

Provides:       bundled(fluidsynth) = %{winefluidsynth}
Provides:       bundled(gsm) = %{winegsm}
Provides:       bundled(capstone) = %{winecapstone}
Provides:       bundled(libFAudio) = %{wineFAudio}
Provides:       bundled(libjpeg) = %{winejpeg}
Provides:       bundled(lcms2) = %{winelcms2}
Provides:       bundled(openldap) = %{wineldap}
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
Summary:        Systemd config for the wine binfmt handler and module loading
Requires:       systemd >= 23
BuildArch:      noarch
Requires(post):  systemd
Requires(postun): systemd
Obsoletes:      wine-sysvinit < %{version}-%{release}
Obsoletes:      ntsync < 6.14
Provides:       ntsync = %{version}
Provides:       ntsync-kmod-common = %{version}
Requires:       kmod(ntsync.ko)

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
%ifarch aarch64
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

%if 0%{?opencl}
%package opencl
Summary: OpenCL support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description opencl
This package adds the opencl driver for wine.
%endif

%ifarch %{ix86}
%package wow32
Summary:        Wine wow32 package

%description wow32
This package adds symlinks for wine wow64 functionality.
%endif

%ifarch x86_64
%package wow64
Summary:        Wine wow64 package

%description wow64
This package adds symlinks for wine wow64 functionality.
%endif

%prep
%autosetup -S git_am -N -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}}

%patch -P 511 -p1 -b.cjk
%patch -P 599 -p1

%patch -P 704 -p1
%patch -P 703 -p1
%patch -P 705 -p1

# setup and apply wine-staging patches
%if 0%{?wine_staging}

tar -xf %{SOURCE900} --strip-components=1

%if %{without fshack}
%patch -P 1000 -p1
%endif
%patch -P 1001 -p1

%patch -P 5000 -p1

sed -e "s|'autoreconf'|'true'|g" -i ./staging/patchinstall.py
./staging/patchinstall.py --destdir="$(pwd)" --all %{?wine_staging_opts}

sed -e 's|-Wb,--subsystem|-Wl,--subsystem|' -i dlls/{dxgkrnl,dxgmms1,win32k}.sys/Makefile.in

%if %{with ntsync}
autoreconf -f
%endif

%if %{without ntsync}
%patch -P 1020 -p1
%patch -P 1021 -p1
%endif
%if %{with fshack}
%patch -P 702 -p1 -R
%patch -P 1023 -p1
%endif
%if %{with proton_mf}
%patch -P 1038 -p1
%patch -P 1039 -p1
%endif
%patch -P 1026 -p1
%if %{with proton_winevulkan}
%patch -P 1040 -p1
%endif
%if %{with ge_wayland}
%patch -P 1041 -p1
%endif
%patch -P 701 -p1 -R
%patch -P 700 -p1 -R
%if %{with ntsync}
%patch -P 1051 -p1
%else
%patch -P 1027 -p1
%endif
%patch -P 1028 -p1
%if %{with ntsync}
%patch -P 1053 -p1
%patch -P 1052 -p1
%else
%patch -P 1055 -p1
%patch -P 1029 -p1
%patch -P 1056 -p1
%endif
%patch -P 1030 -p1
%patch -P 1031 -p1
# https://bugs.winehq.org/show_bug.cgi?id=51687#c7
%dnl %patch -P 1034 -p1
%patch -P 1035 -p1
%patch -P 1036 -p1
%if %{without ntsync}
%patch -P 1037 -p1
%endif

%patch -P 1091 -p1 -R
%patch -P 1092 -p1
%if %{without proton_mf}
%patch -P 1093 -p1
%endif
%patch -P 1301 -p1
%patch -P 1302 -p1
%if %{with proton_mf}
%patch -P 1304 -p1
%endif
%patch -P 1303 -p1

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
%if %{with ntsync}
cat README.chinforpms %{SOURCE9} >> README.chinforpms.ntsync
touch -r README.chinforpms README.chinforpms.ntsync
mv -f README.chinforpms.ntsync README.chinforpms
%else
cat README.chinforpms %{SOURCE8} >> README.chinforpms.fsync
touch -r README.chinforpms README.chinforpms.fsync
mv -f README.chinforpms.fsync README.chinforpms
%endif

cp -p %{SOURCE502} README.tahoma

sed \
  -e '/winemenubuilder\.exe/s|-a ||g' \
  -e 's|    LicenseInformation|    LicenseInformation,\\\n    FileOpenAssociations|g' \
  -e '$a \\n[FileOpenAssociations]\nHKCU,Software\\Wine\\FileOpenAssociations,"Enable",,"N"' \
  -i loader/wine.inf.in

cp -p %{SOURCE50} ./dlls/winevulkan/vk-%{winevulkan}.xml
cp -p %{SOURCE51} ./dlls/winevulkan/video-%{winevulkan}.xml

find . \( -name "*.orig" -o -name "*.cjk" \) -delete

git add .
./tools/make_makefiles
./dlls/winevulkan/make_vulkan -x vk-%{winevulkan}.xml -X video-%{winevulkan}.xml
./tools/make_requests
./tools/make_specfiles
autoreconf -f


%build
export CFLAGS="%{build_cflags} -ftree-vectorize"

%if 0%{?wine_staging}
export CFLAGS+=" -Wno-error=implicit-function-declaration"
%endif

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

# required so that both Linux and Windows development files can be found
unset PKG_CONFIG_PATH 

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --with-dbus \
 --with-x \
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
 --with-mingw \
 --disable-tests \
 --without-oss \
%{nil}

%make_build TARGETFLAGS="" depend
%make_build TARGETFLAGS=""

%install
export PATH="$(pwd)/bin:$PATH"

%make_install \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
chrpath --delete %{buildroot}%{_bindir}/wine
chrpath --delete %{buildroot}%{_bindir}/wineserver

%ifarch %{ix86}
for winelibdir in %{winepedir_x86_64} %{winesodir_x86_64} ;do 
  ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_prefix}/lib64/%{name}")"/${winelibdir} %{buildroot}/%{_libdir}/%{name}/
done
%endif
%ifarch x86_64
for winelibdir in %{winepedir_i386} %{winesodir_i386} ;do 
  ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_prefix}/lib/%{name}")"/${winelibdir} %{buildroot}/%{_libdir}/%{name}/
done
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf

%if %{with ntsync}
# systemd module autoinsert rule
mkdir -p %{buildroot}%{_modulesloaddir}
install -m0644 %{SOURCE250} %{buildroot}%{_modulesloaddir}/ntsync.conf
%endif

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

install -p -m 644 dlls/desk.cpl/desk.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/desk.svg
sed -i -e "$MAIN_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/desk.svg

install -p -m 644 dlls/joy.cpl/joy.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg
sed -i -e "$MAIN_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg

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
  %{SOURCE114}

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

%pre core
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64
  %{_sbindir}/alternatives --remove-all wine || :
  %{_sbindir}/alternatives --remove-all wineserver || :
%else
  %{_sbindir}/alternatives --remove-all wine || :
  %{_sbindir}/alternatives --remove-all wineserver || :
%endif
fi


%files
# meta package

%files core
%license COPYING.LIB
%license LICENSE
%license LICENSE.OLD
%doc ANNOUNCE.md
%doc AUTHORS
%doc README.FEDORA
%doc README.chinforpms
%doc README.md
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%if (0%{?wine_staging} && %{without ntsync})
%doc README.esync
%endif
%{_bindir}/msidb
%{_bindir}/winedump
%{_libdir}/wine/%{winepedir}/explorer.exe
%{_libdir}/wine/%{winepedir}/cabarc.exe
%{_libdir}/wine/%{winepedir}/control.exe
%{_libdir}/wine/%{winepedir}/cmd.exe
%{_libdir}/wine/%{winepedir}/dxdiag.exe
%{_libdir}/wine/%{winepedir}/notepad.exe
%{_libdir}/wine/%{winepedir}/plugplay.exe
%{_libdir}/wine/%{winepedir}/progman.exe
%{_libdir}/wine/%{winepedir}/taskmgr.exe
%{_libdir}/wine/%{winepedir}/winedbg.exe
%{_libdir}/wine/%{winepedir}/winefile.exe
%{_libdir}/wine/%{winepedir}/winemine.exe
%{_libdir}/wine/%{winepedir}/winemsibuilder.exe
%{_libdir}/wine/%{winepedir}/winepath.exe
%{_libdir}/wine/%{winepedir}/winmgmt.exe
%{_libdir}/wine/%{winepedir}/winver.exe
%{_libdir}/wine/%{winepedir}/wordpad.exe
%{_libdir}/wine/%{winepedir}/write.exe
%{_libdir}/wine/%{winepedir}/wusa.exe
%{perms_pldr} %{_libdir}/wine/%{winesodir}/wine
%{perms_pldr} %{_libdir}/wine/%{winesodir}/wine-preloader
%{perms_srv} %{_bindir}/wineserver
%{_bindir}/wine

%dir %{_libdir}/wine
%dir %{_libdir}/wine/%{winepedir}
%dir %{_libdir}/wine/%{winesodir}

%{_libdir}/wine/%{winepedir}/arp.exe
%{_libdir}/wine/%{winepedir}/aspnet_regiis.exe
%{_libdir}/wine/%{winepedir}/attrib.exe
%{_libdir}/wine/%{winepedir}/cacls.exe
%{_libdir}/wine/%{winepedir}/certutil.exe
%{_libdir}/wine/%{winepedir}/clock.exe
%{_libdir}/wine/%{winepedir}/conhost.exe
%{_libdir}/wine/%{winepedir}/cscript.exe
%{_libdir}/wine/%{winepedir}/dism.exe
%{_libdir}/wine/%{winepedir}/dllhost.exe
%{_libdir}/wine/%{winepedir}/dotnetfx35.exe
%{_libdir}/wine/%{winepedir}/dplaysvr.exe
%{_libdir}/wine/%{winepedir}/dpnsvr.exe
%{_libdir}/wine/%{winepedir}/dpvsetup.exe
%{_libdir}/wine/%{winepedir}/eject.exe
%{_libdir}/wine/%{winepedir}/expand.exe
%{_libdir}/wine/%{winepedir}/extrac32.exe
%{_libdir}/wine/%{winepedir}/fc.exe
%{_libdir}/wine/%{winepedir}/findstr.exe
%{_libdir}/wine/%{winepedir}/find.exe
%{_libdir}/wine/%{winepedir}/fsutil.exe
%{_libdir}/wine/%{winepedir}/hh.exe
%{_libdir}/wine/%{winepedir}/hostname.exe
%{_libdir}/wine/%{winepedir}/icacls.exe
%{_libdir}/wine/%{winepedir}/icinfo.exe
%{_libdir}/wine/%{winepedir}/iexplore.exe
%{_libdir}/wine/%{winepedir}/ipconfig.exe
%{_libdir}/wine/%{winepedir}/klist.exe
%{_libdir}/wine/%{winepedir}/lodctr.exe
%{_libdir}/wine/%{winepedir}/makecab.exe
%{_libdir}/wine/%{winepedir}/mofcomp.exe
%{_libdir}/wine/%{winepedir}/mshta.exe
%{_libdir}/wine/%{winepedir}/msidb.exe
%{_libdir}/wine/%{winepedir}/msiexec.exe
%{_libdir}/wine/%{winepedir}/msinfo32.exe
%{_libdir}/wine/%{winepedir}/netsh.exe
%{_libdir}/wine/%{winepedir}/netstat.exe
%{_libdir}/wine/%{winepedir}/net.exe
%{_libdir}/wine/%{winepedir}/ngen.exe
%{_libdir}/wine/%{winepedir}/ntoskrnl.exe
%{_libdir}/wine/%{winepedir}/oleview.exe
%{_libdir}/wine/%{winepedir}/ping.exe
%{_libdir}/wine/%{winepedir}/pnputil.exe
%{_libdir}/wine/%{winepedir}/powershell.exe
%{_libdir}/wine/%{winepedir}/presentationfontcache.exe
%{_libdir}/wine/%{winepedir}/regasm.exe
%{_libdir}/wine/%{winepedir}/regedit.exe
%{_libdir}/wine/%{winepedir}/regini.exe
%{_libdir}/wine/%{winepedir}/regsvcs.exe
%{_libdir}/wine/%{winepedir}/regsvr32.exe
%{_libdir}/wine/%{winepedir}/reg.exe
%{_libdir}/wine/%{winepedir}/robocopy.exe
%{_libdir}/wine/%{winepedir}/rpcss.exe
%{_libdir}/wine/%{winepedir}/rundll32.exe
%{_libdir}/wine/%{winepedir}/schtasks.exe
%{_libdir}/wine/%{winepedir}/sc.exe
%{_libdir}/wine/%{winepedir}/sdbinst.exe
%{_libdir}/wine/%{winepedir}/secedit.exe
%{_libdir}/wine/%{winepedir}/servicemodelreg.exe
%{_libdir}/wine/%{winepedir}/services.exe
%{_libdir}/wine/%{winepedir}/setx.exe
%{_libdir}/wine/%{winepedir}/shutdown.exe
%{_libdir}/wine/%{winepedir}/sort.exe
%{_libdir}/wine/%{winepedir}/spoolsv.exe
%{_libdir}/wine/%{winepedir}/start.exe
%{_libdir}/wine/%{winepedir}/subst.exe
%{_libdir}/wine/%{winepedir}/svchost.exe
%{_libdir}/wine/%{winepedir}/systeminfo.exe
%{_libdir}/wine/%{winepedir}/taskkill.exe
%{_libdir}/wine/%{winepedir}/tasklist.exe
%{_libdir}/wine/%{winepedir}/termsv.exe
%{_libdir}/wine/%{winepedir}/timeout.exe
%{_libdir}/wine/%{winepedir}/uninstaller.exe
%{_libdir}/wine/%{winepedir}/unlodctr.exe
%{_libdir}/wine/%{winepedir}/view.exe
%{_libdir}/wine/%{winepedir}/wevtutil.exe
%{_libdir}/wine/%{winepedir}/where.exe
%{_libdir}/wine/%{winepedir}/whoami.exe
%{_libdir}/wine/%{winepedir}/wineboot.exe
%{_libdir}/wine/%{winepedir}/winebrowser.exe
%{_libdir}/wine/%{winepedir}/winecfg.exe
%{_libdir}/wine/%{winepedir}/wineconsole.exe
%{_libdir}/wine/%{winepedir}/winedevice.exe
%{_libdir}/wine/%{winepedir}/winemenubuilder.exe
%{_libdir}/wine/%{winepedir}/winhlp32.exe
%{_libdir}/wine/%{winepedir}/wmic.exe
%{_libdir}/wine/%{winepedir}/wmplayer.exe
%{_libdir}/wine/%{winepedir}/wscript.exe
%{_libdir}/wine/%{winepedir}/wuauserv.exe
%{_libdir}/wine/%{winepedir}/xcopy.exe

%{_libdir}/wine/%{winepedir}/acledit.dll
%{_libdir}/wine/%{winepedir}/aclui.dll
%{_libdir}/wine/%{winepedir}/activeds.dll
%{_libdir}/wine/%{winepedir}/activeds.tlb
%{_libdir}/wine/%{winepedir}/actxprxy.dll
%{_libdir}/wine/%{winepedir}/adsldp.dll
%{_libdir}/wine/%{winepedir}/adsldpc.dll
%{_libdir}/wine/%{winepedir}/advapi32.dll
%{_libdir}/wine/%{winepedir}/advpack.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/audioses.dll
%endif
%if (0%{?wine_staging} && %{with ge_wayland})
%{_libdir}/wine/%{winepedir}/amdxc64.dll
%endif
%{_libdir}/wine/%{winepedir}/amsi.dll
%{_libdir}/wine/%{winepedir}/amstream.dll
%{_libdir}/wine/%{winepedir}/apisetschema.dll
%{_libdir}/wine/%{winepedir}/appxdeploymentclient.dll
%{_libdir}/wine/%{winepedir}/apphelp.dll
%{_libdir}/wine/%{winepedir}/appwiz.cpl
%{_libdir}/wine/%{winepedir}/atl.dll
%{_libdir}/wine/%{winepedir}/atl80.dll
%{_libdir}/wine/%{winepedir}/atl90.dll
%{_libdir}/wine/%{winepedir}/atl100.dll
%{_libdir}/wine/%{winepedir}/atl110.dll
%{_libdir}/wine/%{winepedir}/atlthunk.dll
%{_libdir}/wine/%{winepedir}/atmlib.dll
%{_libdir}/wine/%{winepedir}/authz.dll
%{_libdir}/wine/%{winesodir}/avicap32.so
%{_libdir}/wine/%{winepedir}/avicap32.dll
%{_libdir}/wine/%{winepedir}/avifil32.dll
%{_libdir}/wine/%{winepedir}/avrt.dll
%{_libdir}/wine/%{winesodir}/bcrypt.so
%{_libdir}/wine/%{winepedir}/bcp47langs.dll
%{_libdir}/wine/%{winepedir}/bcrypt.dll
%{_libdir}/wine/%{winepedir}/bcryptprimitives.dll
%{_libdir}/wine/%{winepedir}/bluetoothapis.dll
%{_libdir}/wine/%{winepedir}/browseui.dll
%{_libdir}/wine/%{winepedir}/bthprops.cpl
%{_libdir}/wine/%{winepedir}/cabinet.dll
%{_libdir}/wine/%{winepedir}/cards.dll
%{_libdir}/wine/%{winepedir}/cdosys.dll
%{_libdir}/wine/%{winepedir}/cfgmgr32.dll
%{_libdir}/wine/%{winepedir}/chcp.com
%{_libdir}/wine/%{winepedir}/clusapi.dll
%{_libdir}/wine/%{winepedir}/cng.sys
%{_libdir}/wine/%{winepedir}/colorcnv.dll
%{_libdir}/wine/%{winepedir}/combase.dll
%{_libdir}/wine/%{winepedir}/comcat.dll
%{_libdir}/wine/%{winepedir}/comctl32.dll
%{_libdir}/wine/%{winepedir}/comdlg32.dll
%{_libdir}/wine/%{winepedir}/coml2.dll
%{_libdir}/wine/%{winepedir}/compstui.dll
%{_libdir}/wine/%{winepedir}/comsvcs.dll
%{_libdir}/wine/%{winepedir}/concrt140.dll
%{_libdir}/wine/%{winepedir}/connect.dll
%{_libdir}/wine/%{winepedir}/coremessaging.dll
%{_libdir}/wine/%{winepedir}/credui.dll
%{_libdir}/wine/%{winepedir}/crtdll.dll
%{_libdir}/wine/%{winesodir}/crypt32.so
%{_libdir}/wine/%{winepedir}/crypt32.dll
%{_libdir}/wine/%{winepedir}/cryptbase.dll
%{_libdir}/wine/%{winepedir}/cryptdlg.dll
%{_libdir}/wine/%{winepedir}/cryptdll.dll
%{_libdir}/wine/%{winepedir}/cryptext.dll
%{_libdir}/wine/%{winepedir}/cryptnet.dll
%{_libdir}/wine/%{winepedir}/cryptowinrt.dll
%{_libdir}/wine/%{winepedir}/cryptsp.dll
%{_libdir}/wine/%{winepedir}/cryptui.dll
%{_libdir}/wine/%{winesodir}/ctapi32.so
%{_libdir}/wine/%{winepedir}/ctapi32.dll
%{_libdir}/wine/%{winepedir}/ctl3d32.dll
%{_libdir}/wine/%{winepedir}/d2d1.dll
%{_libdir}/wine/%{winepedir}/d3d10.dll
%{_libdir}/wine/%{winepedir}/d3d10_1.dll
%{_libdir}/wine/%{winepedir}/d3d10core.dll
%{_libdir}/wine/%{winepedir}/d3d11.dll
%{_libdir}/wine/%{winepedir}/d3d12.dll
%{_libdir}/wine/%{winepedir}/d3d12core.dll
%{_libdir}/wine/%{winepedir}/d3dcompiler_*.dll
%{_libdir}/wine/%{winepedir}/d3dim.dll
%{_libdir}/wine/%{winepedir}/d3dim700.dll
%{_libdir}/wine/%{winepedir}/d3drm.dll
%{_libdir}/wine/%{winepedir}/d3dx9_*.dll
%{_libdir}/wine/%{winepedir}/d3dx10_*.dll
%{_libdir}/wine/%{winepedir}/d3dx11_42.dll
%{_libdir}/wine/%{winepedir}/d3dx11_43.dll
%{_libdir}/wine/%{winepedir}/d3dxof.dll
%{_libdir}/wine/%{winepedir}/dataexchange.dll
%{_libdir}/wine/%{winepedir}/davclnt.dll
%{_libdir}/wine/%{winepedir}/dbgeng.dll
%{_libdir}/wine/%{winepedir}/dbghelp.dll
%{_libdir}/wine/%{winepedir}/dciman32.dll
%{_libdir}/wine/%{winepedir}/dcomp.dll
%{_libdir}/wine/%{winepedir}/ddraw.dll
%{_libdir}/wine/%{winepedir}/ddrawex.dll
%{_libdir}/wine/%{winepedir}/desk.cpl
%{_libdir}/wine/%{winepedir}/devenum.dll
%{_libdir}/wine/%{winepedir}/dhcpcsvc.dll
%{_libdir}/wine/%{winepedir}/dhcpcsvc6.dll
%{_libdir}/wine/%{winepedir}/dhtmled.ocx
%{_libdir}/wine/%{winepedir}/diasymreader.dll
%{_libdir}/wine/%{winepedir}/difxapi.dll
%{_libdir}/wine/%{winepedir}/dinput.dll
%{_libdir}/wine/%{winepedir}/dinput8.dll
%{_libdir}/wine/%{winepedir}/directmanipulation.dll
%{_libdir}/wine/%{winepedir}/dispex.dll
%{_libdir}/wine/%{winepedir}/dmband.dll
%{_libdir}/wine/%{winepedir}/dmcompos.dll
%{_libdir}/wine/%{winepedir}/dmime.dll
%{_libdir}/wine/%{winepedir}/dmloader.dll
%{_libdir}/wine/%{winepedir}/dmscript.dll
%{_libdir}/wine/%{winepedir}/dmstyle.dll
%{_libdir}/wine/%{winepedir}/dmsynth.dll
%{_libdir}/wine/%{winepedir}/dmusic.dll
%{_libdir}/wine/%{winepedir}/dmusic32.dll
%{_libdir}/wine/%{winepedir}/dplay.dll
%{_libdir}/wine/%{winepedir}/dplayx.dll
%{_libdir}/wine/%{winepedir}/dpnaddr.dll
%{_libdir}/wine/%{winepedir}/dpnet.dll
%{_libdir}/wine/%{winepedir}/dpnhpast.dll
%{_libdir}/wine/%{winepedir}/dpnhupnp.dll
%{_libdir}/wine/%{winepedir}/dpnlobby.dll
%{_libdir}/wine/%{winepedir}/dpvoice.dll
%{_libdir}/wine/%{winepedir}/dpwsockx.dll
%{_libdir}/wine/%{winepedir}/drmclien.dll
%{_libdir}/wine/%{winepedir}/dsdmo.dll
%{_libdir}/wine/%{winepedir}/dsound.dll
%{_libdir}/wine/%{winepedir}/dsquery.dll
%{_libdir}/wine/%{winepedir}/dssenh.dll
%{_libdir}/wine/%{winepedir}/dswave.dll
%{_libdir}/wine/%{winepedir}/dsuiext.dll
%{_libdir}/wine/%{winepedir}/dwmapi.dll
%{_libdir}/wine/%{winesodir}/dwrite.so
%{_libdir}/wine/%{winepedir}/dwrite.dll
%{_libdir}/wine/%{winepedir}/dx8vb.dll
%{_libdir}/wine/%{winepedir}/dxcore.dll
%{_libdir}/wine/%{winepedir}/dxdiagn.dll
%{_libdir}/wine/%{winepedir}/dxgi.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/dxgkrnl.sys
%{_libdir}/wine/%{winepedir}/dxgmms1.sys
%endif
%{_libdir}/wine/%{winepedir}/dxtrans.dll
%{_libdir}/wine/%{winepedir}/dxva2.dll
%{_libdir}/wine/%{winepedir}/esent.dll
%{_libdir}/wine/%{winepedir}/evr.dll
%{_libdir}/wine/%{winepedir}/explorerframe.dll
%{_libdir}/wine/%{winepedir}/faultrep.dll
%{_libdir}/wine/%{winepedir}/feclient.dll
%{_libdir}/wine/%{winepedir}/fltlib.dll
%{_libdir}/wine/%{winepedir}/fltmgr.sys
%{_libdir}/wine/%{winepedir}/fntcache.dll
%{_libdir}/wine/%{winepedir}/fontsub.dll
%{_libdir}/wine/%{winepedir}/fusion.dll
%{_libdir}/wine/%{winepedir}/fwpuclnt.dll
%{_libdir}/wine/%{winepedir}/gameux.dll
%{_libdir}/wine/%{winepedir}/gamingtcui.dll
%{_libdir}/wine/%{winepedir}/gdi32.dll
%{_libdir}/wine/%{winepedir}/gdiplus.dll
%{_libdir}/wine/%{winepedir}/geolocation.dll
%{_libdir}/wine/%{winepedir}/glu32.dll
%{_libdir}/wine/%{winesodir}/gphoto2.so
%{_libdir}/wine/%{winepedir}/gphoto2.ds
%{_libdir}/wine/%{winepedir}/gpkcsp.dll
%{_libdir}/wine/%{winepedir}/graphicscapture.dll
%{_libdir}/wine/%{winepedir}/hal.dll
%{_libdir}/wine/%{winepedir}/hhctrl.ocx
%{_libdir}/wine/%{winepedir}/hid.dll
%{_libdir}/wine/%{winepedir}/hidclass.sys
%{_libdir}/wine/%{winepedir}/hidparse.sys
%{_libdir}/wine/%{winepedir}/hlink.dll
%{_libdir}/wine/%{winepedir}/hnetcfg.dll
%{_libdir}/wine/%{winepedir}/hrtfapo.dll
%{_libdir}/wine/%{winepedir}/http.sys
%{_libdir}/wine/%{winepedir}/httpapi.dll
%{_libdir}/wine/%{winepedir}/hvsimanagementapi.dll
%{_libdir}/wine/%{winepedir}/ia2comproxy.dll
%{_libdir}/wine/%{winepedir}/iccvid.dll
%{_libdir}/wine/%{winepedir}/icmp.dll
%{_libdir}/wine/%{winepedir}/icmui.dll
%{_libdir}/wine/%{winepedir}/ieframe.dll
%{_libdir}/wine/%{winepedir}/ieproxy.dll
%{_libdir}/wine/%{winepedir}/iertutil.dll
%{_libdir}/wine/%{winepedir}/imaadp32.acm
%{_libdir}/wine/%{winepedir}/imagehlp.dll
%{_libdir}/wine/%{winepedir}/imm32.dll
%{_libdir}/wine/%{winepedir}/inetcomm.dll
%{_libdir}/wine/%{winepedir}/inetcpl.cpl
%{_libdir}/wine/%{winepedir}/inetmib1.dll
%{_libdir}/wine/%{winepedir}/infosoft.dll
%{_libdir}/wine/%{winepedir}/initpki.dll
%{_libdir}/wine/%{winepedir}/inkobj.dll
%{_libdir}/wine/%{winepedir}/inseng.dll
%{_libdir}/wine/%{winepedir}/iphlpapi.dll
%{_libdir}/wine/%{winepedir}/iprop.dll
%{_libdir}/wine/%{winepedir}/ir50_32.dll
%{_libdir}/wine/%{winepedir}/irprops.cpl
%{_libdir}/wine/%{winepedir}/itircl.dll
%{_libdir}/wine/%{winepedir}/itss.dll
%{_libdir}/wine/%{winepedir}/joy.cpl
%{_libdir}/wine/%{winepedir}/jscript.dll
%{_libdir}/wine/%{winepedir}/jsproxy.dll
%{_libdir}/wine/%{winesodir}/kerberos.so
%{_libdir}/wine/%{winepedir}/kerberos.dll
%{_libdir}/wine/%{winepedir}/kernel32.dll
%{_libdir}/wine/%{winepedir}/kernelbase.dll
%{_libdir}/wine/%{winepedir}/ksecdd.sys
%{_libdir}/wine/%{winepedir}/ksproxy.ax
%{_libdir}/wine/%{winepedir}/ksuser.dll
%{_libdir}/wine/%{winepedir}/ktmw32.dll
%{_libdir}/wine/%{winepedir}/l3codeca.acm
%{_libdir}/wine/%{winepedir}/l3codecx.ax
%{_libdir}/wine/%{winepedir}/light.msstyles
%{_libdir}/wine/%{winepedir}/loadperf.dll
%{_libdir}/wine/%{winesodir}/localspl.so
%{_libdir}/wine/%{winepedir}/localspl.dll
%{_libdir}/wine/%{winepedir}/localui.dll
%{_libdir}/wine/%{winepedir}/lz32.dll
%{_libdir}/wine/%{winepedir}/magnification.dll
%{_libdir}/wine/%{winepedir}/mapi32.dll
%{_libdir}/wine/%{winepedir}/mapistub.dll
%{_libdir}/wine/%{winepedir}/mciavi32.dll
%{_libdir}/wine/%{winepedir}/mcicda.dll
%{_libdir}/wine/%{winepedir}/mciqtz32.dll
%{_libdir}/wine/%{winepedir}/mciseq.dll
%{_libdir}/wine/%{winepedir}/mciwave.dll
%{_libdir}/wine/%{winepedir}/mf.dll
%{_libdir}/wine/%{winepedir}/mf3216.dll
%{_libdir}/wine/%{winepedir}/mfasfsrcsnk.dll
%{_libdir}/wine/%{winepedir}/mferror.dll
%{_libdir}/wine/%{winepedir}/mfh264enc.dll
%{_libdir}/wine/%{winepedir}/mfmediaengine.dll
%{_libdir}/wine/%{winepedir}/mfmp4srcsnk.dll
%{_libdir}/wine/%{winepedir}/mfplat.dll
%{_libdir}/wine/%{winepedir}/mfplay.dll
%{_libdir}/wine/%{winepedir}/mfreadwrite.dll
%{_libdir}/wine/%{winepedir}/mfsrcsnk.dll
%{_libdir}/wine/%{winepedir}/mgmtapi.dll
%{_libdir}/wine/%{winepedir}/midimap.dll
%{_libdir}/wine/%{winepedir}/mlang.dll
%{_libdir}/wine/%{winepedir}/mmcndmgr.dll
%{_libdir}/wine/%{winepedir}/mmdevapi.dll
%{_libdir}/wine/%{winepedir}/mouhid.sys
%{_libdir}/wine/%{winesodir}/mountmgr.so
%{_libdir}/wine/%{winepedir}/mountmgr.sys
%{_libdir}/wine/%{winepedir}/mp3dmod.dll
%{_libdir}/wine/%{winepedir}/mpr.dll
%{_libdir}/wine/%{winepedir}/mprapi.dll
%{_libdir}/wine/%{winepedir}/msacm32.dll
%{_libdir}/wine/%{winepedir}/msacm32.drv
%{_libdir}/wine/%{winepedir}/msado15.dll
%{_libdir}/wine/%{winepedir}/msadp32.acm
%{_libdir}/wine/%{winepedir}/msasn1.dll
%{_libdir}/wine/%{winepedir}/msauddecmft.dll
%{_libdir}/wine/%{winepedir}/mscat32.dll
%{_libdir}/wine/%{winepedir}/mscoree.dll
%{_libdir}/wine/%{winepedir}/mscorwks.dll
%{_libdir}/wine/%{winepedir}/msctf.dll
%{_libdir}/wine/%{winepedir}/msctfmonitor.dll
%{_libdir}/wine/%{winepedir}/msctfp.dll
%{_libdir}/wine/%{winepedir}/msdaps.dll
%{_libdir}/wine/%{winepedir}/msdasql.dll
%{_libdir}/wine/%{winepedir}/msdelta.dll
%{_libdir}/wine/%{winepedir}/msdmo.dll
%{_libdir}/wine/%{winepedir}/msdrm.dll
%{_libdir}/wine/%{winepedir}/msftedit.dll
%{_libdir}/wine/%{winepedir}/msg711.acm
%{_libdir}/wine/%{winepedir}/msgsm32.acm
%{_libdir}/wine/%{winepedir}/mshtml.dll
%{_libdir}/wine/%{winepedir}/mshtml.tlb
%{_libdir}/wine/%{winepedir}/msi.dll
%{_libdir}/wine/%{winepedir}/msident.dll
%{_libdir}/wine/%{winepedir}/msimtf.dll
%{_libdir}/wine/%{winepedir}/msimg32.dll
%{_libdir}/wine/%{winepedir}/msimsg.dll
%{_libdir}/wine/%{winepedir}/msisip.dll
%{_libdir}/wine/%{winepedir}/msisys.ocx
%{_libdir}/wine/%{winepedir}/msls31.dll
%{_libdir}/wine/%{winepedir}/msmpeg2vdec.dll
%{_libdir}/wine/%{winepedir}/msnet32.dll
%{_libdir}/wine/%{winepedir}/mspatcha.dll
%{_libdir}/wine/%{winepedir}/msports.dll
%{_libdir}/wine/%{winepedir}/msscript.ocx
%{_libdir}/wine/%{winepedir}/mssign32.dll
%{_libdir}/wine/%{winepedir}/mssip32.dll
%{_libdir}/wine/%{winepedir}/msrle32.dll
%{_libdir}/wine/%{winepedir}/mstask.dll
%{_libdir}/wine/%{winepedir}/msttsengine.dll
%{_libdir}/wine/%{winesodir}/msv1_0.so
%{_libdir}/wine/%{winepedir}/msv1_0.dll
%{_libdir}/wine/%{winepedir}/msvcirt.dll
%{_libdir}/wine/%{winepedir}/msvcp_win.dll
%{_libdir}/wine/%{winepedir}/msvcm80.dll
%{_libdir}/wine/%{winepedir}/msvcm90.dll
%{_libdir}/wine/%{winepedir}/msvcp60.dll
%{_libdir}/wine/%{winepedir}/msvcp70.dll
%{_libdir}/wine/%{winepedir}/msvcp71.dll
%{_libdir}/wine/%{winepedir}/msvcp80.dll
%{_libdir}/wine/%{winepedir}/msvcp90.dll
%{_libdir}/wine/%{winepedir}/msvcp100.dll
%{_libdir}/wine/%{winepedir}/msvcp110.dll
%{_libdir}/wine/%{winepedir}/msvcp120.dll
%{_libdir}/wine/%{winepedir}/msvcp120_app.dll
%{_libdir}/wine/%{winepedir}/msvcp140.dll
%{_libdir}/wine/%{winepedir}/msvcp140_1.dll
%{_libdir}/wine/%{winepedir}/msvcp140_2.dll
%{_libdir}/wine/%{winepedir}/msvcp140_atomic_wait.dll
%{_libdir}/wine/%{winepedir}/msvcp140_codecvt_ids.dll
%{_libdir}/wine/%{winepedir}/msvcr70.dll
%{_libdir}/wine/%{winepedir}/msvcr71.dll
%{_libdir}/wine/%{winepedir}/msvcr80.dll
%{_libdir}/wine/%{winepedir}/msvcr90.dll
%{_libdir}/wine/%{winepedir}/msvcr100.dll
%{_libdir}/wine/%{winepedir}/msvcr110.dll
%{_libdir}/wine/%{winepedir}/msvcr120.dll
%{_libdir}/wine/%{winepedir}/msvcr120_app.dll
%{_libdir}/wine/%{winepedir}/msvcrt.dll
%{_libdir}/wine/%{winepedir}/msvcrt20.dll
%{_libdir}/wine/%{winepedir}/msvcrt40.dll
%{_libdir}/wine/%{winepedir}/msvcrtd.dll
%{_libdir}/wine/%{winepedir}/msvfw32.dll
%{_libdir}/wine/%{winepedir}/msvidc32.dll
%{_libdir}/wine/%{winepedir}/msvproc.dll
%{_libdir}/wine/%{winepedir}/mswsock.dll
%{_libdir}/wine/%{winepedir}/msxml.dll
%{_libdir}/wine/%{winepedir}/msxml2.dll
%{_libdir}/wine/%{winepedir}/msxml3.dll
%{_libdir}/wine/%{winepedir}/msxml4.dll
%{_libdir}/wine/%{winepedir}/msxml6.dll
%{_libdir}/wine/%{winepedir}/mtxdm.dll
%{_libdir}/wine/%{winepedir}/nddeapi.dll
%{_libdir}/wine/%{winepedir}/ncrypt.dll
%{_libdir}/wine/%{winepedir}/ndis.sys
%{_libdir}/wine/%{winesodir}/netapi32.so
%{_libdir}/wine/%{winepedir}/netapi32.dll
%{_libdir}/wine/%{winepedir}/netcfgx.dll
%{_libdir}/wine/%{winepedir}/netio.sys
%{_libdir}/wine/%{winepedir}/netprofm.dll
%{_libdir}/wine/%{winepedir}/netutils.dll
%{_libdir}/wine/%{winepedir}/newdev.dll
%{_libdir}/wine/%{winepedir}/ninput.dll
%{_libdir}/wine/%{winepedir}/normaliz.dll
%{_libdir}/wine/%{winepedir}/npmshtml.dll
%{_libdir}/wine/%{winepedir}/npptools.dll
%{_libdir}/wine/%{winepedir}/nsi.dll
%{_libdir}/wine/%{winesodir}/nsiproxy.so
%{_libdir}/wine/%{winepedir}/nsiproxy.sys
%{_libdir}/wine/%{winesodir}/ntdll.so
%{_libdir}/wine/%{winepedir}/ntdll.dll
%{_libdir}/wine/%{winepedir}/ntdsapi.dll
%{_libdir}/wine/%{winepedir}/ntprint.dll
%{_libdir}/wine/%{winepedir}/objsel.dll
%{_libdir}/wine/%{winesodir}/odbc32.so
%{_libdir}/wine/%{winepedir}/odbc32.dll
%{_libdir}/wine/%{winepedir}/odbcbcp.dll
%{_libdir}/wine/%{winepedir}/odbccp32.dll
%{_libdir}/wine/%{winepedir}/odbccu32.dll
%{_libdir}/wine/%{winepedir}/ole32.dll
%{_libdir}/wine/%{winepedir}/oleacc.dll
%{_libdir}/wine/%{winepedir}/oleaut32.dll
%{_libdir}/wine/%{winepedir}/olecli32.dll
%{_libdir}/wine/%{winepedir}/oledb32.dll
%{_libdir}/wine/%{winepedir}/oledlg.dll
%{_libdir}/wine/%{winepedir}/olepro32.dll
%{_libdir}/wine/%{winepedir}/olesvr32.dll
%{_libdir}/wine/%{winepedir}/olethk32.dll
%{_libdir}/wine/%{winepedir}/opcservices.dll
%{_libdir}/wine/%{winepedir}/packager.dll
%{_libdir}/wine/%{winepedir}/pdh.dll
%{_libdir}/wine/%{winepedir}/photometadatahandler.dll
%{_libdir}/wine/%{winepedir}/pidgen.dll
%{_libdir}/wine/%{winepedir}/powrprof.dll
%{_libdir}/wine/%{winepedir}/printui.dll
%{_libdir}/wine/%{winepedir}/prntvpt.dll
%{_libdir}/wine/%{winepedir}/profapi.dll
%{_libdir}/wine/%{winepedir}/propsys.dll
%{_libdir}/wine/%{winepedir}/psapi.dll
%{_libdir}/wine/%{winepedir}/pstorec.dll
%{_libdir}/wine/%{winepedir}/pwrshplugin.dll
%{_libdir}/wine/%{winepedir}/qasf.dll
%{_libdir}/wine/%{winesodir}/qcap.so
%{_libdir}/wine/%{winepedir}/qcap.dll
%{_libdir}/wine/%{winepedir}/qedit.dll
%{_libdir}/wine/%{winepedir}/qdvd.dll
%{_libdir}/wine/%{winepedir}/qmgr.dll
%{_libdir}/wine/%{winepedir}/qmgrprxy.dll
%{_libdir}/wine/%{winepedir}/quartz.dll
%{_libdir}/wine/%{winepedir}/query.dll
%{_libdir}/wine/%{winepedir}/qwave.dll
%{_libdir}/wine/%{winepedir}/rasapi32.dll
%{_libdir}/wine/%{winepedir}/rasdlg.dll
%{_libdir}/wine/%{winepedir}/regapi.dll
%{_libdir}/wine/%{winepedir}/resampledmo.dll
%{_libdir}/wine/%{winepedir}/resutils.dll
%{_libdir}/wine/%{winepedir}/riched20.dll
%{_libdir}/wine/%{winepedir}/riched32.dll
%{_libdir}/wine/%{winepedir}/rpcrt4.dll
%{_libdir}/wine/%{winepedir}/rometadata.dll
%{_libdir}/wine/%{winepedir}/rsabase.dll
%{_libdir}/wine/%{winepedir}/rsaenh.dll
%{_libdir}/wine/%{winepedir}/rstrtmgr.dll
%{_libdir}/wine/%{winepedir}/rtutils.dll
%{_libdir}/wine/%{winepedir}/rtworkq.dll
%{_libdir}/wine/%{winepedir}/samlib.dll
%{_libdir}/wine/%{winepedir}/sapi.dll
%{_libdir}/wine/%{winepedir}/sas.dll
%{_libdir}/wine/%{winepedir}/scarddlg.dll
%{_libdir}/wine/%{winepedir}/scardsvr.dll
%{_libdir}/wine/%{winepedir}/sccbase.dll
%{_libdir}/wine/%{winepedir}/schannel.dll
%{_libdir}/wine/%{winepedir}/scrobj.dll
%{_libdir}/wine/%{winepedir}/scrrun.dll
%{_libdir}/wine/%{winepedir}/scsiport.sys
%{_libdir}/wine/%{winepedir}/sechost.dll
%{_libdir}/wine/%{winesodir}/secur32.so
%{_libdir}/wine/%{winepedir}/secur32.dll
%{_libdir}/wine/%{winepedir}/sensapi.dll
%{_libdir}/wine/%{winepedir}/serialui.dll
%{_libdir}/wine/%{winepedir}/setupapi.dll
%{_libdir}/wine/%{winepedir}/sfc_os.dll
%{_libdir}/wine/%{winepedir}/shcore.dll
%{_libdir}/wine/%{winepedir}/shdoclc.dll
%{_libdir}/wine/%{winepedir}/shdocvw.dll
%{_libdir}/wine/%{winepedir}/schedsvc.dll
%if (0%{?wine_staging} && %{with proton_winevulkan})
%{_libdir}/wine/%{winepedir}/sharedgpures.sys
%endif
%{_libdir}/wine/%{winepedir}/shell32.dll
%{_libdir}/wine/%{winepedir}/shfolder.dll
%{_libdir}/wine/%{winepedir}/shlwapi.dll
%{_libdir}/wine/%{winepedir}/slbcsp.dll
%{_libdir}/wine/%{winepedir}/slc.dll
%{_libdir}/wine/%{winepedir}/snmpapi.dll
%{_libdir}/wine/%{winepedir}/softpub.dll
%{_libdir}/wine/%{winepedir}/sppc.dll
%{_libdir}/wine/%{winepedir}/srclient.dll
%{_libdir}/wine/%{winepedir}/srvcli.dll
%{_libdir}/wine/%{winepedir}/srvsvc.dll
%{_libdir}/wine/%{winepedir}/sspicli.dll
%{_libdir}/wine/%{winepedir}/stdole2.tlb
%{_libdir}/wine/%{winepedir}/stdole32.tlb
%{_libdir}/wine/%{winepedir}/sti.dll
%{_libdir}/wine/%{winepedir}/strmdll.dll
%{_libdir}/wine/%{winepedir}/svrapi.dll
%{_libdir}/wine/%{winepedir}/sxs.dll
%{_libdir}/wine/%{winepedir}/t2embed.dll
%{_libdir}/wine/%{winepedir}/tapi32.dll
%{_libdir}/wine/%{winepedir}/taskschd.dll
%{_libdir}/wine/%{winepedir}/tbs.dll
%{_libdir}/wine/%{winepedir}/tdh.dll
%{_libdir}/wine/%{winepedir}/tdi.sys
%{_libdir}/wine/%{winepedir}/traffic.dll
%{_libdir}/wine/%{winepedir}/threadpoolwinrt.dll
%{_libdir}/wine/%{winepedir}/twinapi.appcore.dll
%{_libdir}/wine/%{winepedir}/tzres.dll
%{_libdir}/wine/%{winepedir}/ucrtbase.dll
%{_libdir}/wine/%{winepedir}/uianimation.dll
%{_libdir}/wine/%{winepedir}/uiautomationcore.dll
%{_libdir}/wine/%{winepedir}/uiribbon.dll
%{_libdir}/wine/%{winepedir}/unicows.dll
%{_libdir}/wine/%{winepedir}/updspapi.dll
%{_libdir}/wine/%{winepedir}/url.dll
%{_libdir}/wine/%{winepedir}/urlmon.dll
%{_libdir}/wine/%{winepedir}/usbd.sys
%{_libdir}/wine/%{winepedir}/user32.dll
%{_libdir}/wine/%{winepedir}/usp10.dll
%{_libdir}/wine/%{winepedir}/utildll.dll
%{_libdir}/wine/%{winepedir}/uxtheme.dll
%{_libdir}/wine/%{winepedir}/userenv.dll
%{_libdir}/wine/%{winepedir}/vbscript.dll
%{_libdir}/wine/%{winepedir}/vcomp.dll
%{_libdir}/wine/%{winepedir}/vcomp90.dll
%{_libdir}/wine/%{winepedir}/vcomp100.dll
%{_libdir}/wine/%{winepedir}/vcomp110.dll
%{_libdir}/wine/%{winepedir}/vcomp120.dll
%{_libdir}/wine/%{winepedir}/vcomp140.dll
%{_libdir}/wine/%{winepedir}/vcruntime140.dll
%ifarch x86_64
%{_libdir}/wine/%{winepedir}/vcruntime140_1.dll
%endif
%{_libdir}/wine/%{winepedir}/vdmdbg.dll
%{_libdir}/wine/%{winepedir}/vga.dll
%{_libdir}/wine/%{winepedir}/version.dll
%{_libdir}/wine/%{winepedir}/virtdisk.dll
%{_libdir}/wine/%{winepedir}/vssapi.dll
%{_libdir}/wine/%{winepedir}/vulkan-1.dll
%{_libdir}/wine/%{winepedir}/wbemdisp.dll
%{_libdir}/wine/%{winepedir}/wbemprox.dll
%{_libdir}/wine/%{winepedir}/wdscore.dll
%{_libdir}/wine/%{winepedir}/webservices.dll
%{_libdir}/wine/%{winepedir}/websocket.dll
%{_libdir}/wine/%{winepedir}/wer.dll
%{_libdir}/wine/%{winepedir}/wevtapi.dll
%{_libdir}/wine/%{winepedir}/wevtsvc.dll
%{_libdir}/wine/%{winepedir}/wiaservc.dll
%{_libdir}/wine/%{winepedir}/wldp.dll
%{_libdir}/wine/%{winepedir}/wimgapi.dll
%{_libdir}/wine/%{winesodir}/win32u.so
%{_libdir}/wine/%{winepedir}/win32u.dll
%{_libdir}/wine/%{winepedir}/windows.applicationmodel.dll
%{_libdir}/wine/%{winepedir}/windows.devices.bluetooth.dll
%{_libdir}/wine/%{winepedir}/windows.devices.enumeration.dll
%{_libdir}/wine/%{winepedir}/windows.devices.usb.dll
%{_libdir}/wine/%{winepedir}/windows.gaming.input.dll
%{_libdir}/wine/%{winepedir}/windows.gaming.ui.gamebar.dll
%{_libdir}/wine/%{winepedir}/windows.globalization.dll
%{_libdir}/wine/%{winepedir}/windows.media.dll
%{_libdir}/wine/%{winepedir}/windows.media.devices.dll
%{_libdir}/wine/%{winepedir}/windows.media.mediacontrol.dll
%{_libdir}/wine/%{winepedir}/windows.media.speech.dll
%{_libdir}/wine/%{winepedir}/windows.networking.dll
%{_libdir}/wine/%{winepedir}/windows.networking.hostname.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/win32k.sys
%{_libdir}/wine/%{winepedir}/windows.networking.connectivity.dll
%endif
%{_libdir}/wine/%{winepedir}/windows.perception.stub.dll
%{_libdir}/wine/%{winepedir}/windows.security.credentials.ui.userconsentverifier.dll
%{_libdir}/wine/%{winepedir}/windows.security.authentication.onlineid.dll
%{_libdir}/wine/%{winepedir}/windows.storage.dll
%{_libdir}/wine/%{winepedir}/windows.storage.applicationdata.dll
%{_libdir}/wine/%{winepedir}/windows.system.profile.systemid.dll
%{_libdir}/wine/%{winepedir}/windows.system.profile.systemmanufacturers.dll
%{_libdir}/wine/%{winepedir}/windows.ui.dll
%{_libdir}/wine/%{winepedir}/windows.ui.xaml.dll
%{_libdir}/wine/%{winepedir}/windows.web.dll
%{_libdir}/wine/%{winepedir}/windowscodecs.dll
%{_libdir}/wine/%{winepedir}/windowscodecsext.dll
%{_libdir}/wine/%{winesodir}/winebth.so
%{_libdir}/wine/%{winepedir}/winebth.sys
%{_libdir}/wine/%{winesodir}/winebus.so
%{_libdir}/wine/%{winepedir}/winebus.sys
%{_libdir}/wine/%{winesodir}/winedmo.so
%{_libdir}/wine/%{winepedir}/winedmo.dll
%{_libdir}/wine/%{winesodir}/winegstreamer.so
%{_libdir}/wine/%{winepedir}/winegstreamer.dll
%{_libdir}/wine/%{winepedir}/winehid.sys
%{_libdir}/wine/%{winepedir}/winemapi.dll
%{_libdir}/wine/%{winesodir}/wineusb.so
%{_libdir}/wine/%{winepedir}/wineusb.sys
%{_libdir}/wine/%{winesodir}/winevulkan.so
%{_libdir}/wine/%{winepedir}/winevulkan.dll
%{_libdir}/wine/%{winesodir}/winewayland.so
%{_libdir}/wine/%{winepedir}/winewayland.drv
%{_libdir}/wine/%{winesodir}/winex11.so
%{_libdir}/wine/%{winepedir}/winex11.drv
%{_libdir}/wine/%{winepedir}/wing32.dll
%{_libdir}/wine/%{winepedir}/winhttp.dll
%{_libdir}/wine/%{winepedir}/wininet.dll
%{_libdir}/wine/%{winepedir}/winmm.dll
%{_libdir}/wine/%{winepedir}/winprint.dll
%{_libdir}/wine/%{winepedir}/winnls32.dll
%{_libdir}/wine/%{winesodir}/winspool.so
%{_libdir}/wine/%{winepedir}/winspool.drv
%{_libdir}/wine/%{winepedir}/winsta.dll
%{_libdir}/wine/%{winepedir}/wintypes.dll
%{_libdir}/wine/%{winepedir}/wlanui.dll
%{_libdir}/wine/%{winepedir}/wmadmod.dll
%{_libdir}/wine/%{winepedir}/wmasf.dll
%{_libdir}/wine/%{winepedir}/wmi.dll
%{_libdir}/wine/%{winepedir}/wmilib.sys
%{_libdir}/wine/%{winepedir}/wmiutils.dll
%{_libdir}/wine/%{winepedir}/wmp.dll
%{_libdir}/wine/%{winepedir}/wmvcore.dll
%{_libdir}/wine/%{winepedir}/wmvdecod.dll
%{_libdir}/wine/%{winepedir}/spoolss.dll
%{_libdir}/wine/%{winesodir}/winscard.so
%{_libdir}/wine/%{winepedir}/winscard.dll
%{_libdir}/wine/%{winepedir}/wintab32.dll
%{_libdir}/wine/%{winepedir}/wintrust.dll
%{_libdir}/wine/%{winepedir}/winusb.dll
%{_libdir}/wine/%{winepedir}/wlanapi.dll
%{_libdir}/wine/%{winepedir}/wmphoto.dll
%{_libdir}/wine/%{winepedir}/wnaspi32.dll
%{_libdir}/wine/%{winepedir}/wofutil.dll
%ifarch x86_64
%{_libdir}/wine/%{winepedir}/wow64.dll
%{_libdir}/wine/%{winepedir}/wow64cpu.dll
%{_libdir}/wine/%{winepedir}/wow64win.dll
%endif
%{_libdir}/wine/%{winepedir}/wpc.dll
%{_libdir}/wine/%{winesodir}/wpcap.so
%{_libdir}/wine/%{winepedir}/wpcap.dll
%{_libdir}/wine/%{winesodir}/ws2_32.so
%{_libdir}/wine/%{winepedir}/ws2_32.dll
%{_libdir}/wine/%{winepedir}/wsdapi.dll
%{_libdir}/wine/%{winepedir}/wshom.ocx
%{_libdir}/wine/%{winepedir}/wsnmp32.dll
%{_libdir}/wine/%{winepedir}/wsock32.dll
%{_libdir}/wine/%{winepedir}/wtsapi32.dll
%{_libdir}/wine/%{winepedir}/wuapi.dll
%{_libdir}/wine/%{winepedir}/wuaueng.dll
%{_libdir}/wine/%{winepedir}/security.dll
%{_libdir}/wine/%{winepedir}/sfc.dll
%{_libdir}/wine/%{winesodir}/wineps.so
%{_libdir}/wine/%{winepedir}/wineps.drv
%{_libdir}/wine/%{winepedir}/d3d8.dll
%{_libdir}/wine/%{winepedir}/d3d8thk.dll
%{_libdir}/wine/%{winepedir}/d3d9.dll
%{_libdir}/wine/%{winesodir}/opengl32.so
%{_libdir}/wine/%{winepedir}/opengl32.dll
%{_libdir}/wine/%{winepedir}/wined3d.dll
%{_libdir}/wine/%{winepedir}/winexinput.sys
%{_libdir}/wine/%{winesodir}/dnsapi.so
%{_libdir}/wine/%{winepedir}/dnsapi.dll
%{_libdir}/wine/%{winepedir}/xactengine2_0.dll
%{_libdir}/wine/%{winepedir}/xactengine2_4.dll
%{_libdir}/wine/%{winepedir}/xactengine2_7.dll
%{_libdir}/wine/%{winepedir}/xactengine2_9.dll
%{_libdir}/wine/%{winepedir}/xactengine3_0.dll
%{_libdir}/wine/%{winepedir}/xactengine3_1.dll
%{_libdir}/wine/%{winepedir}/xactengine3_2.dll
%{_libdir}/wine/%{winepedir}/xactengine3_3.dll
%{_libdir}/wine/%{winepedir}/xactengine3_4.dll
%{_libdir}/wine/%{winepedir}/xactengine3_5.dll
%{_libdir}/wine/%{winepedir}/xactengine3_6.dll
%{_libdir}/wine/%{winepedir}/xactengine3_7.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_0.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_1.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_2.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_3.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_4.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_5.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_6.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_7.dll
%{_libdir}/wine/%{winepedir}/xapofx1_1.dll
%{_libdir}/wine/%{winepedir}/xapofx1_2.dll
%{_libdir}/wine/%{winepedir}/xapofx1_3.dll
%{_libdir}/wine/%{winepedir}/xapofx1_4.dll
%{_libdir}/wine/%{winepedir}/xapofx1_5.dll
%{_libdir}/wine/%{winepedir}/xaudio2_0.dll
%{_libdir}/wine/%{winepedir}/xaudio2_1.dll
%{_libdir}/wine/%{winepedir}/xaudio2_2.dll
%{_libdir}/wine/%{winepedir}/xaudio2_3.dll
%{_libdir}/wine/%{winepedir}/xaudio2_4.dll
%{_libdir}/wine/%{winepedir}/xaudio2_5.dll
%{_libdir}/wine/%{winepedir}/xaudio2_6.dll
%{_libdir}/wine/%{winepedir}/xaudio2_7.dll
%{_libdir}/wine/%{winepedir}/xaudio2_8.dll
%{_libdir}/wine/%{winepedir}/xaudio2_9.dll
%{_libdir}/wine/%{winepedir}/xinput1_1.dll
%{_libdir}/wine/%{winepedir}/xinput1_2.dll
%{_libdir}/wine/%{winepedir}/xinput1_3.dll
%{_libdir}/wine/%{winepedir}/xinput1_4.dll
%{_libdir}/wine/%{winepedir}/xinput9_1_0.dll
%{_libdir}/wine/%{winepedir}/xinputuap.dll
%{_libdir}/wine/%{winepedir}/xmllite.dll
%{_libdir}/wine/%{winepedir}/xolehlp.dll
%{_libdir}/wine/%{winepedir}/xpsprint.dll
%{_libdir}/wine/%{winepedir}/xpssvcs.dll

%if 0
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/nvcuda.dll.so
%{_libdir}/wine/%{winesodir}/nvcuvid.dll.so
%{_libdir}/wine/%{winepedir}/nvcuda.dll
%{_libdir}/wine/%{winepedir}/nvcuvid.dll
%ifarch x86_64 aarch64
%{_libdir}/wine/%{winepedir}/nvapi64.dll
%{_libdir}/wine/%{winesodir}/nvencodeapi64.dll.so
%exclude %{_libdir}/wine/%{winesodir}/nvencodeapi.dll.so
%{_libdir}/wine/%{winepedir}/nvencodeapi64.dll
%exclude %{_libdir}/wine/%{winepedir}/nvencodeapi.dll
%else
%{_libdir}/wine/%{winepedir}/nvapi.dll
%{_libdir}/wine/%{winesodir}/nvencodeapi.dll.so
%exclude %{_libdir}/wine/%{winesodir}/nvencodeapi64.dll.so
%{_libdir}/wine/%{winepedir}/nvencodeapi.dll
%exclude %{_libdir}/wine/%{winepedir}/nvencodeapi64.dll
%endif
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 aarch64
%{_libdir}/wine/%{winepedir}/winevdm.exe
%{_libdir}/wine/%{winepedir}/ifsmgr.vxd
%{_libdir}/wine/%{winepedir}/mmdevldr.vxd
%{_libdir}/wine/%{winepedir}/monodebg.vxd
%{_libdir}/wine/%{winepedir}/rundll.exe16
%{_libdir}/wine/%{winepedir}/vdhcp.vxd
%{_libdir}/wine/%{winepedir}/user.exe16
%{_libdir}/wine/%{winepedir}/vmm.vxd
%{_libdir}/wine/%{winepedir}/vnbt.vxd
%{_libdir}/wine/%{winepedir}/vnetbios.vxd
%{_libdir}/wine/%{winepedir}/vtdapi.vxd
%{_libdir}/wine/%{winepedir}/vwin32.vxd
%{_libdir}/wine/%{winepedir}/w32skrnl.dll
%{_libdir}/wine/%{winepedir}/avifile.dll16
%{_libdir}/wine/%{winepedir}/comm.drv16
%{_libdir}/wine/%{winepedir}/commdlg.dll16
%{_libdir}/wine/%{winepedir}/compobj.dll16
%{_libdir}/wine/%{winepedir}/ctl3d.dll16
%{_libdir}/wine/%{winepedir}/ctl3dv2.dll16
%{_libdir}/wine/%{winepedir}/ddeml.dll16
%{_libdir}/wine/%{winepedir}/dispdib.dll16
%{_libdir}/wine/%{winepedir}/display.drv16
%{_libdir}/wine/%{winepedir}/gdi.exe16
%{_libdir}/wine/%{winepedir}/imm.dll16
%{_libdir}/wine/%{winepedir}/krnl386.exe16
%{_libdir}/wine/%{winepedir}/keyboard.drv16
%{_libdir}/wine/%{winepedir}/lzexpand.dll16
%{_libdir}/wine/%{winepedir}/mmsystem.dll16
%{_libdir}/wine/%{winepedir}/mouse.drv16
%{_libdir}/wine/%{winepedir}/msacm.dll16
%{_libdir}/wine/%{winepedir}/msvideo.dll16
%{_libdir}/wine/%{winepedir}/ole2.dll16
%{_libdir}/wine/%{winepedir}/ole2conv.dll16
%{_libdir}/wine/%{winepedir}/ole2disp.dll16
%{_libdir}/wine/%{winepedir}/ole2nls.dll16
%{_libdir}/wine/%{winepedir}/ole2prox.dll16
%{_libdir}/wine/%{winepedir}/ole2thk.dll16
%{_libdir}/wine/%{winepedir}/olecli.dll16
%{_libdir}/wine/%{winepedir}/olesvr.dll16
%{_libdir}/wine/%{winepedir}/rasapi16.dll16
%{_libdir}/wine/%{winepedir}/setupx.dll16
%{_libdir}/wine/%{winepedir}/shell.dll16
%{_libdir}/wine/%{winepedir}/sound.drv16
%{_libdir}/wine/%{winepedir}/storage.dll16
%{_libdir}/wine/%{winepedir}/stress.dll16
%{_libdir}/wine/%{winepedir}/system.drv16
%{_libdir}/wine/%{winepedir}/toolhelp.dll16
%{_libdir}/wine/%{winepedir}/twain.dll16
%{_libdir}/wine/%{winepedir}/typelib.dll16
%{_libdir}/wine/%{winepedir}/ver.dll16
%{_libdir}/wine/%{winepedir}/w32sys.dll16
%{_libdir}/wine/%{winepedir}/win32s16.dll16
%{_libdir}/wine/%{winepedir}/win87em.dll16
%{_libdir}/wine/%{winepedir}/winaspi.dll16
%{_libdir}/wine/%{winepedir}/windebug.dll16
%{_libdir}/wine/%{winepedir}/wineps16.drv16
%{_libdir}/wine/%{winepedir}/wing.dll16
%{_libdir}/wine/%{winepedir}/winhelp.exe16
%{_libdir}/wine/%{winepedir}/winnls.dll16
%{_libdir}/wine/%{winepedir}/winoldap.mod16
%{_libdir}/wine/%{winepedir}/winsock.dll16
%{_libdir}/wine/%{winepedir}/wintab.dll16
%{_libdir}/wine/%{winepedir}/wow32.dll
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
%{_datadir}/applications/wine-desk.desktop
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
%if %{with ntsync}
%{_modulesloaddir}/ntsync.conf
%endif

# ldap subpackage
%files ldap
%{_libdir}/wine/%{winepedir}/wldap32.dll

# cms subpackage
%files cms
%{_libdir}/wine/%{winepedir}/mscms.dll

# twain subpackage
%files twain
%{_libdir}/wine/%{winepedir}/twain_32.dll
%{_libdir}/wine/%{winesodir}/sane.so
%{_libdir}/wine/%{winepedir}/sane.ds

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
%{_libdir}/wine/%{winepedir}/*.a

%files pulseaudio
%{_libdir}/wine/%{winesodir}/winepulse.so
%{_libdir}/wine/%{winepedir}/winepulse.drv

%files alsa
%{_libdir}/wine/%{winesodir}/winealsa.so
%{_libdir}/wine/%{winepedir}/winealsa.drv

%if 0%{?opencl}
%files opencl
%{_libdir}/wine/%{winesodir}/opencl.so
%{_libdir}/wine/%{winepedir}/opencl.dll
%endif

%ifarch %{ix86}
%files wow32
%{_libdir}/wine/%{winepedir_x86_64}
%{_libdir}/wine/%{winesodir_x86_64}
%endif

%ifarch x86_64
%files wow64
%{_libdir}/wine/%{winepedir_i386}
%{_libdir}/wine/%{winesodir_i386}
%endif


%changelog
* Sat Jun 14 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.10-100
- 10.10
- BR: libOSMesa removed
- tkg mf and winevulkan patches

* Sun Jun 01 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.9-100
- 10.9

* Sun May 18 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.8-100
- 10.8

* Sat May 03 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.7-100
- 10.7

* Thu May 01 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.6-102.20250429gitf37d05e
- Change mesa-libOSMesa to libOSMesa

* Fri Apr 25 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.6-101.20250424gitf171f6c
- Support only mingw builds

* Mon Apr 21 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.6-100
- 10.6

* Sun Apr 06 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.5-100
- 10.5

* Sat Mar 22 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.4-100
- 10.4

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.3-101
- Merge ntsync modules file to systemd package

* Sat Mar 08 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.3-100
- 10.3

* Sat Feb 22 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.2-100.20250222gite1b8e7f
- 10.2

* Sun Feb 16 2025 Phantom X <megaphantomx at hotmail dot com> - 2:10.1-101.20250214git4de5639
- Bump to fix crashes
- Update to new preloader locations, no needing altenatives

* Sun Feb 09 2025 Phantom X <megaphantomx at hotmail dot com> - 1:10.1-100
- 10.1

* Tue Jan 21 2025 Phantom X <megaphantomx at hotmail dot com> - 1:10.0-100
- 10.0

* Sat Jan 18 2025 Phantom X <megaphantomx at hotmail dot com> - 1:10.0~rc6-100
- 10.0-rc6

* Mon Jan 13 2025 Phantom X <megaphantomx at hotmail dot com> - 1:10.0~rc5-101.20250113gitf2eebf3
- Try ntsync7

* Sat Jan 11 2025 Phantom X <megaphantomx at hotmail dot com> - 1:10.0~rc5-100
- 10.0-rc5

* Sat Jan 04 2025 Phantom X <megaphantomx at hotmail dot com> - 1:10.0~rc4-100
- 10.0-rc4

* Sat Dec 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1:10.0~rc3-100
- 10.0-rc3

* Sat Dec 14 2024 Phantom X <megaphantomx at hotmail dot com> - 1:10.0~rc2-100
- 10.0-rc2

* Sat Dec 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1:10.0~rc1-100
- 10.0-rc1

* Sat Nov 23 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.22-100
- 9.22

* Sun Nov 10 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.21-101
- tkg fixes

* Sat Nov 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.21-100
- 9.21

* Sat Oct 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.20-100
- 9.20

* Sun Oct 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.19-100
- 9.19

* Sat Sep 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.18-100
- 9.18

* Sat Sep 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.17-100
- 9.17

* Sat Aug 24 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.16-100
- 9.16

* Sun Aug 11 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.15-100
- 9.15

* Sun Jul 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.14-100
- 9.14

* Mon Jul 15 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.13-100
- 9.13

* Sun Jun 30 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.12-100
- 9.12

* Sat Jun 15 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.11-100
- 9.11

* Sat Jun 01 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.10-100
- 9.10
- Disable childwindow again

* Sun May 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.9-101.20240524gitb210a20
- Reenable childwindow

* Sat May 18 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.9-100
- 9.9

* Sat May 04 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.8-100
- 9.8

* Sun Apr 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.7-100
- 9.7

* Sat Apr 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.6-100
- 9.6
- Disable childwindow and OPWR patch for the time

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.5-101
- tkg sync

* Sat Mar 23 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.5-100
- 9.5

* Sat Mar 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.4-101
- Staging 9.4.1

* Sat Mar 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.4-100
- 9.4

* Wed Feb 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.3-100.20240227gitc2a4f38
- 9.3

* Sun Feb 11 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.2-100
- 9.2

* Sat Jan 27 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.1-100
- 9.1

* Sat Jan 13 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.0~rc5-100
- 9.0-rc5

* Sat Jan 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1:9.0~rc4-100
- 9.0-rc4

* Sat Dec 23 2023 Phantom X <megaphantomx at hotmail dot com> - 1:9.0~rc3-100
- 9.0-rc3

* Sat Dec 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1:9.0~rc2-100
- 9.0-rc2

* Sat Dec 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1:9.0~rc1-100
- 9.0-rc1

* Sat Nov 25 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.21-100
- 8.21

* Sat Nov 11 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.20-100
- 8.20

* Mon Oct 30 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.19-100
- 8.19

* Sun Oct 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.18-100
- 8.18

* Mon Oct 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.17-101
- Staging 8.17.1

* Sun Oct 01 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.17-100
- 8.17

* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.16-100
- 8.16

* Sat Sep 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.15-100
- 8.15

* Mon Aug 21 2023 Phantom X <megaphantomx at hotmail dot com> - 1:8.14-100
- 8.14

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
