# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%global rcrev 0
%global no64bit   0
%global winegecko 2.47
%global winemono  4.7.3
#global _default_patch_fuzz 2

# build with staging-patches, see:  https://wine-staging.com/
# uncomment to enable; comment-out to disable.
%if 0%{?fedora}
%global staging 1
%global stagingver 3.15
%if 0%(echo %{stagingver} | grep -q \\. ; echo $?) == 0
%global strel v
%endif
%global pba 1
%global pbaver 3.15
%if 0%(echo %{pbaver} | grep -q \\. ; echo $?) == 0
%global pbarel v
%global pbapkg knobs_and_switches-
%endif
%endif # 0%{?fedora}

# binfmt macros for RHEL
%if 0%{?rhel} == 7
%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt  %{?*} >/dev/null 2>&1 || : \
%{nil}
%endif

%if 0%{?rcrev}
%global rctag .rc%rcrev
%global rctagtarball -rc%rcrev
%endif

Name:           wine
Version:        3.15
Release:        104%{?rctag}.chinfo%{?dist}
Summary:        A compatibility layer for windows applications

License:        LGPLv2+
URL:            http://www.winehq.org/
Source0:        https://dl.winehq.org/wine/source/3.x/wine-%{version}%{?rctagtarball}.tar.xz
Source10:       https://dl.winehq.org/wine/source/3.x/wine-%{version}%{?rctagtarball}.tar.xz.sign

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source4:        wine-32.conf
Source5:        wine-64.conf

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

# build fixes

# wine bugs

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

### AUR - https://aur.archlinux.org/packages/wine-gaming-nine
# Steam patch, Crossover Hack version
# https://bugs.winehq.org/show_bug.cgi?id=39403
Patch600:       steam.patch
Patch601:       harmony-fix.patch
Patch602:       https://github.com/laino/wine-patches/raw/master/0003-wine-list.h-linked-list-cache-line-prefetching.patch#/laino-0003-wine-list.h-linked-list-cache-line-prefetching.patch
# Wbemprox videocontroller query fix v2
# https://bugs.winehq.org/show_bug.cgi?id=38879
Patch603:       wbemprox_query_v2.patch
# Keybind patch reversion
Patch604:       keybindings.patch
Patch605:       poe-fix.patch
Patch606:       user32-Call-DefWindowProc-in-DesktopWndProc.patch

%global whq_url  https://source.winehq.org/git/wine.git/patch
Patch700:       %{whq_url}/e84742abccd8314ce5382bed8e1f83f3de796cd3#/whq-e84742abccd8314ce5382bed8e1f83f3de796cd3.patch
Patch701:       %{whq_url}/53271d9567759634a84f901e5506084179940e87#/whq-53271d9567759634a84f901e5506084179940e87.patch
Patch702:       %{whq_url}/c8175e6c7a73d1c510fe2285f74e6bcf808c9fe2#/whq-c8175e6c7a73d1c510fe2285f74e6bcf808c9fe2.patch
Patch703:       %{whq_url}/8c9c2fca08bb654568071305ab98b16d5b712c47#/whq-8c9c2fca08bb654568071305ab98b16d5b712c47.patch
Patch704:       %{whq_url}/c3af72019ef1141610d2116d66e3fb7591832557#/whq-c3af72019ef1141610d2116d66e3fb7591832557.patch
Patch705:       %{whq_url}/58f3dc4becbb4afcb9b4ccc95ae635b59c9956e9#/whq-58f3dc4becbb4afcb9b4ccc95ae635b59c9956e9.patch
Patch706:       %{whq_url}/9a96657910c2ce30f6f8492bdd562932d63ba430#/whq-9a96657910c2ce30f6f8492bdd562932d63ba430.patch
Patch707:       %{whq_url}/12195e450fea6885eb2d3be05a8ed92dd93752c9#/whq-12195e450fea6885eb2d3be05a8ed92dd93752c9.patch
Patch708:       %{whq_url}/68e35eb7456e68d4233ffc5e795511823a45ba6a#/whq-68e35eb7456e68d4233ffc5e795511823a45ba6a.patch
Patch709:       %{whq_url}/fd044802b9de14416b4d5fa723d2596d39402c97#/whq-fd044802b9de14416b4d5fa723d2596d39402c97.patch
Patch710:       %{whq_url}/d99f6821183ef16457f5cedb13289bc715d11f09#/whq-d99f6821183ef16457f5cedb13289bc715d11f09.patch
Patch711:       %{whq_url}/54530bc4933ae1014c3697c95e22b8ca5a275bc4#/whq-54530bc4933ae1014c3697c95e22b8ca5a275bc4.patch
Patch712:       %{whq_url}/ceea5bda14ecf4c8ce262fc7ab88df49e500bc38#/whq-ceea5bda14ecf4c8ce262fc7ab88df49e500bc38.patch
Patch713:       %{whq_url}/4a6855a575c02aa1569aab8b2e96720fc02f3f26#/whq-4a6855a575c02aa1569aab8b2e96720fc02f3f26.patch
Patch714:       %{whq_url}/7f567451b29b1c1d3e16f147136e00f545d640b1#/whq-7f567451b29b1c1d3e16f147136e00f545d640b1.patch
Patch715:       %{whq_url}/b3d819a1d7a406176e343ebfc9ef74341a2f098b#/whq-b3d819a1d7a406176e343ebfc9ef74341a2f098b.patch
Patch716:       %{whq_url}/b29cdbd5f23548d9631e5c98ec923b6d2d16a3f8#/whq-b29cdbd5f23548d9631e5c98ec923b6d2d16a3f8.patch

# Reversions
Patch750:       %{whq_url}/6a4be7155d77c972e0c63a50f45be864584ccf87#/whq-6a4be7155d77c972e0c63a50f45be864584ccf87.patch
Patch751:       %{whq_url}/44e794327436effc75478ff68def40f9d8801a82#/whq-44e794327436effc75478ff68def40f9d8801a82.patch
Patch752:       %{whq_url}/c18f8e4c3235d0417bfb9fdba2d938bf2e42ee65#/whq-c18f8e4c3235d0417bfb9fdba2d938bf2e42ee65.patch

# wine staging patches for wine-staging
%if 0%{?staging}
Source900:      https://github.com/wine-staging/wine-staging/archive/%{?strel}%{stagingver}.tar.gz#/wine-staging-%{stagingver}.tar.gz
Patch900:       https://github.com/wine-staging/wine-staging/pull/60.patch#/staging-pull-60.patch
# New pulseaudio patches causing noise with a game
Patch901:       wine-staging-old-pulseaudio.patch
Patch902:       0001-winedevice-Avoid-invalid-memory-access-when-relocati.patch
%endif

%if 0%{?pba}
# acomminos PBA patches from Firerat github
# https://github.com/Firerat/wine-pba
Source1000:     https://github.com/Firerat/wine-pba/archive/%{?pbapkg}%{?pbarel}%{pbaver}.tar.gz#/wine-pba-%{pbaver}.tar.gz
Source1001:     wine-README-pba
Patch1000:      wine-staging-pba.patch
%endif

%if !%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%else
ExclusiveArch:  %{ix86} %{arm}
%endif

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
%ifarch aarch64
BuildRequires:  clang >= 5.0
%else
BuildRequires:  gcc
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  freeglut-devel
BuildRequires:  krb5-devel
BuildRequires:  lcms2-devel
BuildRequires:  libieee1284-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2
BuildRequires:  librsvg2-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libusb-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  ncurses-devel
%if 0%{?fedora}
BuildRequires:  ocl-icd-devel
BuildRequires:  opencl-headers
%endif
BuildRequires:  openldap-devel
BuildRequires:  perl-generators
BuildRequires:  unixODBC-devel
BuildRequires:  sane-backends-devel
BuildRequires:  samba-devel
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
BuildRequires:  fontforge freetype-devel
BuildRequires:  libgphoto2-devel
BuildRequires:  isdn4k-utils-devel
BuildRequires:  libpcap-devel
# modular x
BuildRequires:  libX11-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel mesa-libOSMesa-devel
BuildRequires:  libXxf86dga-devel libXxf86vm-devel
BuildRequires:  libXrandr-devel libXrender-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  fontconfig-devel
BuildRequires:  giflib-devel
BuildRequires:  cups-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXi-devel
BuildRequires:  libXcursor-devel
BuildRequires:  dbus-devel
BuildRequires:  gnutls-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  gsm-devel
BuildRequires:  libv4l-devel
BuildRequires:  fontpackages-devel
BuildRequires:  libtiff-devel
BuildRequires:  gettext-devel
BuildRequires:  chrpath
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
%if 0%{?fedora} > 24
BuildRequires:  mpg123-devel
%endif
BuildRequires:  SDL2-devel
BuildRequires:  libvkd3d-devel
BuildRequires:  vulkan-devel

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?staging}
BuildRequires:  gtk3-devel
BuildRequires:  libattr-devel
BuildRequires:  libva-devel
%endif # 0%{?staging}

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildRequires:  openal-soft-devel
BuildRequires:  icoutils
BuildRequires:  librsvg2-tools
%endif

Requires:       wine-common = %{version}-%{release}
Requires:       wine-desktop = %{version}-%{release}
Requires:       wine-fonts = %{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
%if 0%{?fedora} || 0%{?rhel} <= 6
Requires:       wine-core(x86-32) = %{version}-%{release}
Requires:       wine-capi(x86-32) = %{version}-%{release}
Requires:       wine-cms(x86-32) = %{version}-%{release}
Requires:       wine-ldap(x86-32) = %{version}-%{release}
Requires:       wine-twain(x86-32) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} == 6
Requires:       wine-openal(x86-32) = %{version}-%{release}
Requires:       wine-xaudio2(x86-32) >= %{version}-%{release}
%endif
%if 0%{?fedora}
Requires:       wine-opencl(x86-32) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{version}-%{release}
Requires:       wine-capi(x86-64) = %{version}-%{release}
Requires:       wine-cms(x86-64) = %{version}-%{release}
Requires:       wine-ldap(x86-64) = %{version}-%{release}
Requires:       wine-twain(x86-64) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
Requires:       wine-openal(x86-64) = %{version}-%{release}
Requires:       wine-xaudio2(x86-64) >= %{version}-%{release}
%endif 
%if 0%{?fedora}
Requires:       wine-opencl(x86-64) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
Requires:       mesa-dri-drivers(x86-64)
%endif

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{version}-%{release}
Requires:       wine-capi = %{version}-%{release}
Requires:       wine-cms = %{version}-%{release}
Requires:       wine-ldap = %{version}-%{release}
Requires:       wine-twain = %{version}-%{release}
Requires:       wine-pulseaudio = %{version}-%{release}
Requires:       wine-openal = %{version}-%{release}
%if 0%{?fedora}
Requires:       wine-opencl = %{version}-%{release}
Requires:       wine-xaudio2 >= %{version}-%{release}
%endif
Requires:       mesa-dri-drivers
Requires:       samba-winbind-clients
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{version}-%{release}
Requires:       wine-capi(aarch-64) = %{version}-%{release}
Requires:       wine-cms(aarch-64) = %{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{version}-%{release}
Requires:       wine-twain(aarch-64) = %{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{version}-%{release}
Requires:       wine-openal(aarch-64) = %{version}-%{release}
Requires:       wine-xaudio2(aarch-64) >= %{version}-%{release}
Requires:       wine-opencl(aarch-64) = %{version}-%{release}
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
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives

# require -filesystem
Requires:       wine-filesystem = %{version}-%{release}

%ifarch %{ix86}
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-32)
Requires:       freetype(x86-32)
Requires:       nss-mdns(x86-32)
Requires:       gnutls(x86-32)
Requires:       libxslt(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXinerama(x86-32)
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-32)
Requires:       libpcap(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       samba-libs(x86-32)
Requires:       unixODBC(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?staging}
Requires:       libva(x86-32)
%endif
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       nss-mdns(x86-64)
Requires:       gnutls(x86-64)
Requires:       libxslt(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXinerama(x86-64)
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-64)
Requires:       libpcap(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       samba-libs(x86-64)
Requires:       unixODBC(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?staging}
Requires:       libva(x86-64)
%endif
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gnutls
Requires:       libXrender
Requires:       libXcursor
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng
Requires:       libpcap
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan
%if 0%{?staging}
Requires:       libva
%endif
%endif

# removed as of 1.7.35
Obsoletes:      wine-wow < 1.7.35
Provides:       wine-wow = %{version}-%{release}

%description core
Wine core package includes the basic wine stuff needed by all other packages.

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
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
%endif

%if 0%{?rhel} == 6
%package sysvinit
Summary:        SysV initscript for the wine binfmt handler
BuildArch:      noarch
Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun): /sbin/chkconfig, /sbin/service

%description sysvinit
Register the wine binary handler for windows executables via SysV init files.
%endif

%package filesystem
Summary:        Filesystem directories for wine
BuildArch:      noarch

%description filesystem
Filesystem directories and basic configuration for wine.

%package common
Summary:        Common files
Requires:       wine-core = %{version}-%{release}
BuildArch:      noarch

%description common
Common wine files and scripts.

%package desktop
Summary:        Desktop integration features for wine
Requires:       wine-core = %{version}-%{release}
Requires:       wine-common = %{version}-%{release}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires:       wine-systemd = %{version}-%{release}
%endif
%if 0%{?rhel} == 6
Requires:       wine-sysvinit = %{version}-%{release}
%endif
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package fonts
Summary:       Wine font files
BuildArch:     noarch
# arial-fonts are available with staging-patchset, only.
%if 0%{?staging}
Requires:      wine-arial-fonts = %{version}-%{release}
%else # 0%{?staging}
Obsoletes:     wine-arial-fonts <= %{version}-%{release}
%endif # 0%{?staging}
Requires:      wine-courier-fonts = %{version}-%{release}
Requires:      wine-fixedsys-fonts = %{version}-%{release}
Requires:      wine-small-fonts = %{version}-%{release}
Requires:      wine-system-fonts = %{version}-%{release}
Requires:      wine-marlett-fonts = %{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{version}-%{release}
Requires:      wine-tahoma-fonts = %{version}-%{release}
# times-new-roman-fonts are available with staging-patchset, only.
%if 0%{?staging}
Requires:      wine-times-new-roman-fonts = %{version}-%{release}
%else
Obsoletes:     wine-times-new-roman-fonts <= %{version}-%{release}
%endif
Requires:      wine-symbol-fonts = %{version}-%{release}
Requires:      wine-wingdings-fonts = %{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
%if 0%{?fedora} > 12
Requires:      liberation-narrow-fonts
%endif

%description fonts
%{summary}

%if 0%{?staging}
%package arial-fonts
Summary:       Wine Arial font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description arial-fonts
%{summary}
%endif # 0%{?staging}

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
Requires:      wine-filesystem = %{version}-%{release}

%description tahoma-fonts
%{summary}
Please note: If you want system integration for wine tahoma fonts install the
wine-tahoma-fonts-system package.

%package tahoma-fonts-system
Summary:       Wine Tahoma font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-tahoma-fonts = %{version}-%{release}

%description tahoma-fonts-system
%{summary}

%if 0%{?staging}
%package times-new-roman-fonts
Summary:       Wine Times New Roman font family
BuildArch:     noarch
Requires:      wine-filesystem = %{version}-%{release}

%description times-new-roman-fonts
%{summary}
Please note: If you want system integration for wine times new roman fonts install the
wine-times-new-roman-fonts-system package.

%package times-new-roman-fonts-system
Summary:       Wine Times New Roman font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-times-new-roman-fonts = %{version}-%{release}

%description times-new-roman-fonts-system
%{summary}
%endif

%package symbol-fonts
Summary:       Wine Symbol font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description symbol-fonts
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
Requires:      wine-wingdings-fonts = %{version}-%{release}

%description wingdings-fonts-system
%{summary}


%package ldap
Summary: LDAP support for wine
Requires: wine-core = %{version}-%{release}

%description ldap
LDAP support for wine

%package cms
Summary: Color Management for wine
Requires: wine-core = %{version}-%{release}

%description cms
Color Management for wine

%package twain
Summary: Twain support for wine
Requires: wine-core = %{version}-%{release}
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

%package capi
Summary: ISDN support for wine
Requires: wine-core = %{version}-%{release}
%ifarch x86_64
Requires:       isdn4k-utils(x86-64)
%endif
%ifarch %{ix86}
Requires:       isdn4k-utils(x86-32)
%endif
%ifarch %{arm} aarch64
Requires:       isdn4k-utils
%endif

%description capi
ISDN support for wine

%package devel
Summary: Wine development environment
Requires: wine-core = %{version}-%{release}

%description devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package pulseaudio
Summary: Pulseaudio support for wine
Requires: wine-core = %{version}-%{release}
# midi output
Requires: wine-alsa%{?_isa} = %{version}-%{release}

%description pulseaudio
This package adds a pulseaudio driver for wine.

%package alsa
Summary: Alsa support for wine
Requires: wine-core = %{version}-%{release}

%description alsa
This package adds an alsa driver for wine.

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%package openal
Summary: Openal support for wine
Requires: wine-core = %{version}-%{release}

%description openal
This package adds an openal driver for wine.
%endif

%if 0%{?fedora}
%package opencl
Summary: OpenCL support for wine
Requires: wine-core = %{version}-%{release}

%Description opencl
This package adds the opencl driver for wine.
%endif

%package xaudio2
Summary: xaudio2 support for wine
Requires: wine-core = %{version}-%{release}
Requires: wine-openal%{?_isa} = %{version}-%{release}

%description xaudio2
This package adds xaudio2 support for wine.


%prep
%setup -q -n wine-%{version}%{?rctagtarball}
%patch511 -p1 -b.cjk
%patch599 -p1
%patch600 -p1
%patch601 -p1
%patch602 -p1
%patch604 -p1 -R
%patch605 -p1
%patch606 -p1

%patch752 -p1 -R
%patch751 -p1 -R
%patch750 -p1 -R

%patch700 -p1
%patch701 -p1
%patch702 -p1
%patch703 -p1
%patch704 -p1
%patch705 -p1
%patch706 -p1
%patch707 -p1
%patch708 -p1
%patch709 -p1
%patch710 -p1
%patch711 -p1
%patch712 -p1
%patch713 -p1
%patch714 -p1
%patch715 -p1
%patch716 -p1

# setup and apply wine-staging patches
%if 0%{?staging}
gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

%patch900 -p1
%patch901 -p1

%if 0%{?pba}
tar xvf %{S:1000}
mv wine-pba*/README.md README_pba.md
mv wine-pba*/LICENSE LICENSE_pba.md
mkdir -p patches/wined3d-Persistent_Buffer_Allocator
mv wine-pba-*/patches/*.patch patches/wined3d-Persistent_Buffer_Allocator/

%patch1000 -p1

cp -p %{S:1001} README-pba-pkg
%endif # 0%{?pba}

mv patches/winepulse-PulseAudio_Support patches/winepulse-PulseAudio_Support_new
mv patches/winepulse-PulseAudio_Support_old patches/winepulse-PulseAudio_Support
cp -f patches/winepulse-PulseAudio_Support_new/0001-winepulse.drv-Use-a-separate-mainloop-and-ctx-for-pu.patch \
  patches/winepulse-PulseAudio_Support/
cp -f patches/winepulse-PulseAudio_Support_new/0006-winepulse-fetch-actual-program-name-if-possible.patch \
  patches/winepulse-PulseAudio_Support/

./patches/patchinstall.sh DESTDIR="`pwd`" --all -W ntoskrnl.exe-Fix_Relocation

%patch902 -p1

# fix parallelized build
sed -i -e 's!^loader server: libs/port libs/wine tools.*!& include!' Makefile.in

%else # 0%{?staging}

rm -rf patches/

%endif # 0%{?staging}

%patch603 -p1

sed -i \
  -e 's|-lncurses |-lncursesw |g' \
  -e 's|"-lncurses"|"-lncursesw"|g' \
  -e 's|OpenCL/opencl.h|CL/opencl.h|g' \
  configure

%build

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# Use -O1 optimization
# https://bugs.winehq.org/show_bug.cgi?id=45199
export CFLAGS="`echo %{build_cflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//' -e 's/-O2/-O1/'` -Wno-error"

%ifarch aarch64
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
%endif

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --without-hal --with-dbus \
 --without-ffmpeg \
 --with-x \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
%{?staging: --with-xattr} \
 --disable-tests

make %{?_smp_mflags} TARGETFLAGS=""

%install

%makeinstall \
        includedir=%{buildroot}%{_includedir}/wine \
        sysconfdir=%{buildroot}%{_sysconfdir}/wine \
        dlldir=%{buildroot}%{_libdir}/wine \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
%endif
%ifnarch %{arm} aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
%ifnarch %{arm}
touch %{buildroot}%{_bindir}/wine-preloader
%endif
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
%if 0%{?rhel} < 7
mkdir -p %{buildroot}%{_initrddir}
install -p -c -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/wine
%endif
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf
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
%if 0%{?fedora} > 10
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# This replacement masks a composite program icon .SVG down
# so that only its full-size scalable icon is visible
PROGRAM_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="368"\n'\
'   y="8"\n'\
'   viewBox="368, 8, 256, 256"/;'

# This icon file is still in the legacy format
install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

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

%endif

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

cp -p %{SOURCE3} README-FEDORA

cp -p %{SOURCE502} README-tahoma

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%ifarch %{ix86} %{arm}
install -p -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif

%ifarch x86_64 aarch64
install -p -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif


# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf \
      %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

%if 0%{?staging}
# install Times New Roman font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
ln -s ../../wine/fonts/times.ttf times.ttf
popd
%endif

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

%if 0%{?fedora} || 0%{?rhel} > 6
rm -f %{buildroot}%{_initrddir}/wine
%endif

# wine makefiles are currently broken and don't install the wine man page
install -p -m 0644 loader/wine.man %{buildroot}%{_mandir}/man1/wine.1
install -p -m 0644 loader/wine.de.UTF-8.man %{buildroot}%{_mandir}/de.UTF-8/man1/wine.1
install -p -m 0644 loader/wine.fr.UTF-8.man %{buildroot}%{_mandir}/fr.UTF-8/man1/wine.1
mkdir -p %{buildroot}%{_mandir}/pl.UTF-8/man1
install -p -m 0644 loader/wine.pl.UTF-8.man %{buildroot}%{_mandir}/pl.UTF-8/man1/wine.1


%if 0%{?rhel} == 6
%post sysvinit
if [ $1 -eq 1 ]; then
/sbin/chkconfig --add wine
/sbin/chkconfig --level 2345 wine on
/sbin/service wine start &>/dev/null || :
fi

%preun sysvinit
if [ $1 -eq 0 ]; then
/sbin/service wine stop >/dev/null 2>&1
/sbin/chkconfig --del wine
fi
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} > 6
%post systemd
%binfmt_apply wine.conf

%postun systemd
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi
%endif

%post core -p /sbin/ldconfig

%posttrans core
%ifarch x86_64 aarch64
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine64 10 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine64-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver64 20
%else
%ifnarch %{arm}
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine32-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%else
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%endif
%endif

%postun core
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
fi

%post ldap -p /sbin/ldconfig
%postun ldap -p /sbin/ldconfig

%post cms -p /sbin/ldconfig
%postun cms -p /sbin/ldconfig

%post twain -p /sbin/ldconfig
%postun twain -p /sbin/ldconfig

%post capi -p /sbin/ldconfig
%postun capi -p /sbin/ldconfig

%post alsa -p /sbin/ldconfig
%postun alsa -p /sbin/ldconfig

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%post openal -p /sbin/ldconfig
%postun openal -p /sbin/ldconfig
%post xaudio2 -p /sbin/ldconfig
%postun xaudio2 -p /sbin/ldconfig
%endif

%files
# meta package

%files core
%license COPYING.LIB
%license LICENSE
%license LICENSE.OLD
%doc ANNOUNCE
%doc AUTHORS
%doc README-FEDORA
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%if 0%{?staging}
%if 0%{?pba}
%license LICENSE_pba.md
%doc README_pba.md
%doc README-pba-pkg
%endif
%{_bindir}/msidb
%{_libdir}/wine/runas.exe.so
%endif
%{_bindir}/winedump
%{_libdir}/wine/explorer.exe.so
%{_libdir}/wine/cabarc.exe.so
%{_libdir}/wine/control.exe.so
%{_libdir}/wine/cmd.exe.so
%{_libdir}/wine/notepad.exe.so
%{_libdir}/wine/plugplay.exe.so
%{_libdir}/wine/progman.exe.so
%{_libdir}/wine/taskmgr.exe.so
%{_libdir}/wine/winedbg.exe.so
%{_libdir}/wine/winefile.exe.so
%{_libdir}/wine/winemine.exe.so
%{_libdir}/wine/winemsibuilder.exe.so
%{_libdir}/wine/winepath.exe.so
%{_libdir}/wine/winver.exe.so
%{_libdir}/wine/wordpad.exe.so
%{_libdir}/wine/write.exe.so
%{_libdir}/wine/wusa.exe.so
%{_libdir}/wine/dxdiag.exe.so

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%ifnarch %{arm}
%{_bindir}/wine32-preloader
%endif
%{_bindir}/wineserver32
%config %{_sysconfdir}/ld.so.conf.d/wine-32.conf
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{_bindir}/wineserver64
%config %{_sysconfdir}/ld.so.conf.d/wine-64.conf
%endif
%ifarch x86_64 aarch64
%{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ifnarch %{arm}
%ghost %{_bindir}/wine-preloader
%endif
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine
%dir %{_libdir}/wine/fakedlls
%{_libdir}/wine/fakedlls/*

%{_libdir}/wine/attrib.exe.so
%{_libdir}/wine/arp.exe.so
%{_libdir}/wine/aspnet_regiis.exe.so
%{_libdir}/wine/cacls.exe.so
%{_libdir}/wine/conhost.exe.so
%{_libdir}/wine/cscript.exe.so
%{_libdir}/wine/dpnsvr.exe.so
%{_libdir}/wine/eject.exe.so
%{_libdir}/wine/expand.exe.so
%{_libdir}/wine/extrac32.exe.so
%{_libdir}/wine/findstr.exe.so
%{_libdir}/wine/fsutil.exe.so
%{_libdir}/wine/hostname.exe.so
%{_libdir}/wine/ipconfig.exe.so
%{_libdir}/wine/winhlp32.exe.so
%{_libdir}/wine/mshta.exe.so
%if 0%{?staging}
%{_libdir}/wine/msidb.exe.so
%endif
%{_libdir}/wine/msiexec.exe.so
%{_libdir}/wine/net.exe.so
%{_libdir}/wine/netstat.exe.so
%{_libdir}/wine/ngen.exe.so
%{_libdir}/wine/ntoskrnl.exe.so
%{_libdir}/wine/oleview.exe.so
%{_libdir}/wine/ping.exe.so
%{_libdir}/wine/powershell.exe.so
%{_libdir}/wine/reg.exe.so
%{_libdir}/wine/regasm.exe.so
%{_libdir}/wine/regedit.exe.so
%{_libdir}/wine/regsvcs.exe.so
%{_libdir}/wine/regsvr32.exe.so
%{_libdir}/wine/rpcss.exe.so
%{_libdir}/wine/rundll32.exe.so
%{_libdir}/wine/schtasks.exe.so
%{_libdir}/wine/sdbinst.exe.so
%{_libdir}/wine/secedit.exe.so
%{_libdir}/wine/servicemodelreg.exe.so
%{_libdir}/wine/services.exe.so
%{_libdir}/wine/start.exe.so
%{_libdir}/wine/tasklist.exe.so
%{_libdir}/wine/termsv.exe.so
%{_libdir}/wine/view.exe.so
%{_libdir}/wine/wevtutil.exe.so
%{_libdir}/wine/wineboot.exe.so
%{_libdir}/wine/winebrowser.exe.so
%{_libdir}/wine/wineconsole.exe.so
%{_libdir}/wine/winemenubuilder.exe.so
%{_libdir}/wine/winecfg.exe.so
%{_libdir}/wine/winedevice.exe.so
%{_libdir}/wine/wmplayer.exe.so
%{_libdir}/wine/wscript.exe.so
%{_libdir}/wine/uninstaller.exe.so

%{_libdir}/libwine.so.1*

%{_libdir}/wine/acledit.dll.so
%{_libdir}/wine/aclui.dll.so
%{_libdir}/wine/activeds.dll.so
%{_libdir}/wine/actxprxy.dll.so
%{_libdir}/wine/adsldp.dll.so
%{_libdir}/wine/adsldpc.dll.so
%{_libdir}/wine/advapi32.dll.so
%{_libdir}/wine/advpack.dll.so
%{_libdir}/wine/amstream.dll.so
%{_libdir}/wine/api-ms-win-appmodel-identity-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-2.dll.so
%{_libdir}/wine/api-ms-win-core-apiquery-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-appcompat-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-appinit-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-atoms-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-bem-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-com-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-com-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-com-private-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-console-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-console-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-crt-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-crt-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-debug-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-debug-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-2.dll.so
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-3.dll.so
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-file-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-file-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-file-l1-2-1.dll.so
%{_libdir}/wine/api-ms-win-core-file-l1-2-2.dll.so
%{_libdir}/wine/api-ms-win-core-file-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-file-l2-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-file-l2-1-2.dll.so
%{_libdir}/wine/api-ms-win-core-handle-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-heap-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-heap-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-heap-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-heap-obsolete-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-interlocked-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-interlocked-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-io-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-io-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-job-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-job-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-kernel32-private-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-largeinteger-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-1.dll.so
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-2.dll.so
%{_libdir}/wine/api-ms-win-core-localization-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-localization-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-localization-l1-2-1.dll.so
%{_libdir}/wine/api-ms-win-core-localization-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-3-0.dll.so
%{_libdir}/wine/api-ms-win-core-localization-private-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-localregistry-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-memory-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-memory-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-memory-l1-1-2.dll.so
%{_libdir}/wine/api-ms-win-core-misc-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-namespace-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-normalization-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-path-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-privateprofile-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-processtopology-obsolete-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-2.dll.so
%{_libdir}/wine/api-ms-win-core-profile-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-psapi-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-psapi-ansi-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-psapi-obsolete-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-quirks-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-realtime-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-registry-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-registry-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-registryuserspecific-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-shlwapi-legacy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-shutdown-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-sidebyside-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-string-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-string-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-string-obsolete-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-stringansi-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-synch-ansi-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-synch-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-synch-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-synch-l1-2-1.dll.so
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-1.dll.so
%{_libdir}/wine/api-ms-win-core-threadpool-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-threadpool-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-core-threadpool-legacy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-threadpool-private-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-timezone-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-toolhelp-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-url-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-util-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-version-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-version-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-version-private-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-versionansi-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-windowserrorreporting-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-winrt-errorprivate-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-winrt-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-winrt-registration-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-winrt-roparameterizediid-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-winrt-string-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-core-xstate-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-core-xstate-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-conio-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-convert-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-environment-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-filesystem-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-heap-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-locale-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-math-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-multibyte-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-private-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-process-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-runtime-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-stdio-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-string-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-time-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-crt-utility-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-devices-config-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-devices-config-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-devices-query-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-normaliz-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-ole32-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-shell32-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-user32-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-downlevel-version-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-dx-d3dkmt-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-eventing-classicprovider-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-eventing-consumer-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-eventing-controller-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-eventing-legacy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-eventing-provider-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-eventlog-legacy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-gdi-dpiinfo-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-mm-joystick-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-mm-misc-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-mm-mme-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-mm-time-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-ntuser-dc-access-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-ntuser-rectangle-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-perf-legacy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-power-base-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-power-setting-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-rtcore-ntuser-draw-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-4.dll.so
%{_libdir}/wine/api-ms-win-rtcore-ntuser-window-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-rtcore-ntuser-winevent-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-3.dll.so
%{_libdir}/wine/api-ms-win-security-activedirectoryclient-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-audit-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-security-base-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-base-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-security-base-private-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-security-credentials-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-grouppolicy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-1.dll.so
%{_libdir}/wine/api-ms-win-security-lsapolicy-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-provider-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-sddl-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-security-systemfunctions-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-service-core-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-service-core-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-service-management-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-service-management-l2-1-0.dll.so
%{_libdir}/wine/api-ms-win-service-private-l1-1-1.dll.so
%{_libdir}/wine/api-ms-win-service-winsvc-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-service-winsvc-l1-2-0.dll.so
%{_libdir}/wine/api-ms-win-shcore-obsolete-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-shcore-stream-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-shcore-thread-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-shell-shellcom-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-shell-shellfolders-l1-1-0.dll.so
%{_libdir}/wine/api-ms-win-shcore-scaling-l1-1-1.dll.so
%{_libdir}/wine/apphelp.dll.so
%{_libdir}/wine/appwiz.cpl.so
%{_libdir}/wine/atl.dll.so
%{_libdir}/wine/atl80.dll.so
%{_libdir}/wine/atl90.dll.so
%{_libdir}/wine/atl100.dll.so
%{_libdir}/wine/atl110.dll.so
%{_libdir}/wine/atmlib.dll.so
%{_libdir}/wine/authz.dll.so
%{_libdir}/wine/avicap32.dll.so
%{_libdir}/wine/avifil32.dll.so
%{_libdir}/wine/avrt.dll.so
%{_libdir}/wine/bcrypt.dll.so
%{_libdir}/wine/bluetoothapis.dll.so
%{_libdir}/wine/browseui.dll.so
%{_libdir}/wine/bthprops.cpl.so
%{_libdir}/wine/cabinet.dll.so
%{_libdir}/wine/cards.dll.so
%{_libdir}/wine/cdosys.dll.so
%{_libdir}/wine/cfgmgr32.dll.so
%{_libdir}/wine/clock.exe.so
%{_libdir}/wine/clusapi.dll.so
%{_libdir}/wine/combase.dll.so
%{_libdir}/wine/comcat.dll.so
%{_libdir}/wine/comctl32.dll.so
%{_libdir}/wine/comdlg32.dll.so
%{_libdir}/wine/compstui.dll.so
%{_libdir}/wine/comsvcs.dll.so
%{_libdir}/wine/concrt140.dll.so
%{_libdir}/wine/connect.dll.so
%{_libdir}/wine/credui.dll.so
%{_libdir}/wine/crtdll.dll.so
%{_libdir}/wine/crypt32.dll.so
%{_libdir}/wine/cryptdlg.dll.so
%{_libdir}/wine/cryptdll.dll.so
%{_libdir}/wine/cryptext.dll.so
%{_libdir}/wine/cryptnet.dll.so
%{_libdir}/wine/cryptui.dll.so
%{_libdir}/wine/ctapi32.dll.so
%{_libdir}/wine/ctl3d32.dll.so
%{_libdir}/wine/d2d1.dll.so
%{_libdir}/wine/d3d10.dll.so
%{_libdir}/wine/d3d10_1.dll.so
%{_libdir}/wine/d3d10core.dll.so
%{_libdir}/wine/d3d11.dll.so
%{_libdir}/wine/d3d12.dll.so
%{_libdir}/wine/d3dcompiler_*.dll.so
%{_libdir}/wine/d3dim.dll.so
%{_libdir}/wine/d3drm.dll.so
%{_libdir}/wine/d3dx9_*.dll.so
%{_libdir}/wine/d3dx10_*.dll.so
%{_libdir}/wine/d3dx11_42.dll.so
%{_libdir}/wine/d3dx11_43.dll.so
%{_libdir}/wine/d3dxof.dll.so
%{_libdir}/wine/davclnt.dll.so
%{_libdir}/wine/dbgeng.dll.so
%{_libdir}/wine/dbghelp.dll.so
%{_libdir}/wine/dciman32.dll.so
%{_libdir}/wine/ddraw.dll.so
%{_libdir}/wine/ddrawex.dll.so
%{_libdir}/wine/devenum.dll.so
%{_libdir}/wine/dhcpcsvc.dll.so
%{_libdir}/wine/dhtmled.ocx.so
%{_libdir}/wine/difxapi.dll.so
%{_libdir}/wine/dinput.dll.so
%{_libdir}/wine/dinput8.dll.so
%{_libdir}/wine/dism.exe.so
%{_libdir}/wine/dispex.dll.so
%{_libdir}/wine/dmband.dll.so
%{_libdir}/wine/dmcompos.dll.so
%{_libdir}/wine/dmime.dll.so
%{_libdir}/wine/dmloader.dll.so
%{_libdir}/wine/dmscript.dll.so
%{_libdir}/wine/dmstyle.dll.so
%{_libdir}/wine/dmsynth.dll.so
%{_libdir}/wine/dmusic.dll.so
%{_libdir}/wine/dmusic32.dll.so
%{_libdir}/wine/dplay.dll.so
%{_libdir}/wine/dplayx.dll.so
%{_libdir}/wine/dpnaddr.dll.so
%{_libdir}/wine/dpnet.dll.so
%{_libdir}/wine/dpnhpast.dll.so
%{_libdir}/wine/dpnlobby.dll.so
%{_libdir}/wine/dpvoice.dll.so
%{_libdir}/wine/dpwsockx.dll.so
%{_libdir}/wine/drmclien.dll.so
%{_libdir}/wine/dsound.dll.so
%{_libdir}/wine/dsquery.dll.so
%{_libdir}/wine/dssenh.dll.so
%{_libdir}/wine/dswave.dll.so
%{_libdir}/wine/dwmapi.dll.so
%{_libdir}/wine/dwrite.dll.so
%{_libdir}/wine/dx8vb.dll.so
%{_libdir}/wine/dxdiagn.dll.so
%{_libdir}/wine/dxgi.dll.so
%if 0%{?staging}
%{_libdir}/wine/dxgkrnl.sys.so
%{_libdir}/wine/dxgmms1.sys.so
%endif
%{_libdir}/wine/dxva2.dll.so
%{_libdir}/wine/esent.dll.so
%{_libdir}/wine/evr.dll.so
%{_libdir}/wine/explorerframe.dll.so
%{_libdir}/wine/ext-ms-win-authz-context-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-domainjoin-netjoin-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-dwmapi-ext-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-gdi-dc-l1-2-0.dll.so
%{_libdir}/wine/ext-ms-win-gdi-dc-create-l1-1-1.dll.so
%{_libdir}/wine/ext-ms-win-gdi-devcaps-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-gdi-draw-l1-1-1.dll.so
%{_libdir}/wine/ext-ms-win-gdi-render-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-kernel32-package-current-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-kernel32-package-l1-1-1.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-draw-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-gui-l1-3-0.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-keyboard-l1-3-0.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-message-l1-1-1.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-5-1.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-mouse-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-1-1.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-3-1.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-rectangle-ext-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-uicontext-ext-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-1.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-4.dll.so
%{_libdir}/wine/ext-ms-win-ntuser-windowclass-l1-1-1.dll.so
%{_libdir}/wine/ext-ms-win-oleacc-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-ras-rasapi32-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-gdi-devcaps-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-gdi-object-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-gdi-rgn-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-cursor-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dc-access-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-2-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-rawinput-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-syscolors-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-sysparams-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-security-credui-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-security-cryptui-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-uxtheme-themes-l1-1-0.dll.so
%if 0%{?staging}
%{_libdir}/wine/ext-ms-win-appmodel-usercontext-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-xaml-pal-l1-1-0.dll.so
%endif
%{_libdir}/wine/faultrep.dll.so
%{_libdir}/wine/fc.exe.so
%{_libdir}/wine/feclient.dll.so
%{_libdir}/wine/find.exe.so
%{_libdir}/wine/fltlib.dll.so
%{_libdir}/wine/fltmgr.sys.so
%{_libdir}/wine/fntcache.dll.so
%{_libdir}/wine/fontsub.dll.so
%{_libdir}/wine/fusion.dll.so
%{_libdir}/wine/fwpuclnt.dll.so
%{_libdir}/wine/gameux.dll.so
%{_libdir}/wine/gdi32.dll.so
%{_libdir}/wine/gdiplus.dll.so
%{_libdir}/wine/glu32.dll.so
%{_libdir}/wine/gphoto2.ds.so
%{_libdir}/wine/gpkcsp.dll.so
%{_libdir}/wine/hal.dll.so
%{_libdir}/wine/hh.exe.so
%{_libdir}/wine/hhctrl.ocx.so
%{_libdir}/wine/hid.dll.so
%{_libdir}/wine/hidclass.sys.so
%{_libdir}/wine/hlink.dll.so
%{_libdir}/wine/hnetcfg.dll.so
%{_libdir}/wine/httpapi.dll.so
%{_libdir}/wine/icacls.exe.so
%{_libdir}/wine/iccvid.dll.so
%{_libdir}/wine/icinfo.exe.so
%{_libdir}/wine/icmp.dll.so
%{_libdir}/wine/ieframe.dll.so
%if 0%{?staging}
%{_libdir}/wine/iertutil.dll.so
%endif
%{_libdir}/wine/ieproxy.dll.so
%{_libdir}/wine/imaadp32.acm.so
%{_libdir}/wine/imagehlp.dll.so
%{_libdir}/wine/imm32.dll.so
%{_libdir}/wine/inetcomm.dll.so
%{_libdir}/wine/inetcpl.cpl.so
%{_libdir}/wine/inetmib1.dll.so
%{_libdir}/wine/infosoft.dll.so
%{_libdir}/wine/initpki.dll.so
%{_libdir}/wine/inkobj.dll.so
%{_libdir}/wine/inseng.dll.so
%{_libdir}/wine/iphlpapi.dll.so
%{_libdir}/wine/iprop.dll.so
%{_libdir}/wine/irprops.cpl.so
%{_libdir}/wine/itircl.dll.so
%{_libdir}/wine/itss.dll.so
%{_libdir}/wine/joy.cpl.so
%{_libdir}/wine/jscript.dll.so
%{_libdir}/wine/jsproxy.dll.so
%{_libdir}/wine/kerberos.dll.so
%{_libdir}/wine/kernel32.dll.so
%{_libdir}/wine/kernelbase.dll.so
%{_libdir}/wine/ksuser.dll.so
%{_libdir}/wine/ktmw32.dll.so
%if 0%{?fedora} > 24
%{_libdir}/wine/l3codeca.acm.so
%endif
%{_libdir}/wine/loadperf.dll.so
%{_libdir}/wine/localspl.dll.so
%{_libdir}/wine/localui.dll.so
%{_libdir}/wine/lodctr.exe.so
%{_libdir}/wine/lz32.dll.so
%{_libdir}/wine/mapi32.dll.so
%{_libdir}/wine/mapistub.dll.so
%{_libdir}/wine/mciavi32.dll.so
%{_libdir}/wine/mcicda.dll.so
%{_libdir}/wine/mciqtz32.dll.so
%{_libdir}/wine/mciseq.dll.so
%{_libdir}/wine/mciwave.dll.so
%{_libdir}/wine/mf.dll.so
%{_libdir}/wine/mf3216.dll.so
%{_libdir}/wine/mfplat.dll.so
%{_libdir}/wine/mfreadwrite.dll.so
%{_libdir}/wine/mgmtapi.dll.so
%{_libdir}/wine/midimap.dll.so
%{_libdir}/wine/mlang.dll.so
%{_libdir}/wine/mmcndmgr.dll.so
%{_libdir}/wine/mmdevapi.dll.so
%{_libdir}/wine/mofcomp.exe.so
%{_libdir}/wine/mountmgr.sys.so
%{_libdir}/wine/mpr.dll.so
%{_libdir}/wine/mp3dmod.dll.so
%{_libdir}/wine/mprapi.dll.so
%{_libdir}/wine/msacm32.dll.so
%{_libdir}/wine/msacm32.drv.so
%{_libdir}/wine/msadp32.acm.so
%{_libdir}/wine/msasn1.dll.so
%{_libdir}/wine/mscat32.dll.so
%{_libdir}/wine/mscoree.dll.so
%{_libdir}/wine/msctf.dll.so
%{_libdir}/wine/msctfp.dll.so
%{_libdir}/wine/msdaps.dll.so
%{_libdir}/wine/msdelta.dll.so
%{_libdir}/wine/msdmo.dll.so
%{_libdir}/wine/msdrm.dll.so
%{_libdir}/wine/msftedit.dll.so
%{_libdir}/wine/msg711.acm.so
%{_libdir}/wine/msgsm32.acm.so
%{_libdir}/wine/mshtml.dll.so
%{_libdir}/wine/mshtml.tlb.so
%{_libdir}/wine/msi.dll.so
%{_libdir}/wine/msident.dll.so
%{_libdir}/wine/msimtf.dll.so
%{_libdir}/wine/msimg32.dll.so
%{_libdir}/wine/msimsg.dll.so
%{_libdir}/wine/msinfo32.exe.so
%{_libdir}/wine/msisip.dll.so
%{_libdir}/wine/msisys.ocx.so
%{_libdir}/wine/msls31.dll.so
%{_libdir}/wine/msnet32.dll.so
%{_libdir}/wine/mspatcha.dll.so
%{_libdir}/wine/msports.dll.so
%{_libdir}/wine/msscript.ocx.so
%{_libdir}/wine/mssign32.dll.so
%{_libdir}/wine/mssip32.dll.so
%{_libdir}/wine/msrle32.dll.so
%{_libdir}/wine/mstask.dll.so
%{_libdir}/wine/msvcirt.dll.so
%{_libdir}/wine/msvcm80.dll.so
%{_libdir}/wine/msvcm90.dll.so
%{_libdir}/wine/msvcp60.dll.so
%{_libdir}/wine/msvcp70.dll.so
%{_libdir}/wine/msvcp71.dll.so
%{_libdir}/wine/msvcp80.dll.so
%{_libdir}/wine/msvcp90.dll.so
%{_libdir}/wine/msvcp100.dll.so
%{_libdir}/wine/msvcp110.dll.so
%{_libdir}/wine/msvcp120.dll.so
%{_libdir}/wine/msvcp120_app.dll.so
%{_libdir}/wine/msvcp140.dll.so
%{_libdir}/wine/msvcr70.dll.so
%{_libdir}/wine/msvcr71.dll.so
%{_libdir}/wine/msvcr80.dll.so
%{_libdir}/wine/msvcr90.dll.so
%{_libdir}/wine/msvcr100.dll.so
%{_libdir}/wine/msvcr110.dll.so
%{_libdir}/wine/msvcr120.dll.so
%{_libdir}/wine/msvcr120_app.dll.so
%{_libdir}/wine/msvcrt.dll.so
%{_libdir}/wine/msvcrt20.dll.so
%{_libdir}/wine/msvcrt40.dll.so
%{_libdir}/wine/msvcrtd.dll.so
%{_libdir}/wine/msvfw32.dll.so
%{_libdir}/wine/msvidc32.dll.so
%{_libdir}/wine/mswsock.dll.so
%{_libdir}/wine/msxml.dll.so
%{_libdir}/wine/msxml2.dll.so
%{_libdir}/wine/msxml3.dll.so
%{_libdir}/wine/msxml4.dll.so
%{_libdir}/wine/msxml6.dll.so
%{_libdir}/wine/mtxdm.dll.so
%{_libdir}/wine/nddeapi.dll.so
%{_libdir}/wine/ncrypt.dll.so
%{_libdir}/wine/ndis.sys.so
%{_libdir}/wine/netapi32.dll.so
%{_libdir}/wine/netcfgx.dll.so
%{_libdir}/wine/netprofm.dll.so
%{_libdir}/wine/netsh.exe.so
%{_libdir}/wine/newdev.dll.so
%{_libdir}/wine/ninput.dll.so
%{_libdir}/wine/normaliz.dll.so
%{_libdir}/wine/npmshtml.dll.so
%{_libdir}/wine/npptools.dll.so
%{_libdir}/wine/ntdll.dll.so
%{_libdir}/wine/ntdsapi.dll.so
%{_libdir}/wine/ntprint.dll.so
%if 0%{?staging}
%{_libdir}/wine/nvcuda.dll.so
%{_libdir}/wine/nvcuvid.dll.so
%endif
%{_libdir}/wine/objsel.dll.so
%{_libdir}/wine/odbc32.dll.so
%{_libdir}/wine/odbccp32.dll.so
%{_libdir}/wine/odbccu32.dll.so
%{_libdir}/wine/ole32.dll.so
%{_libdir}/wine/oleacc.dll.so
%{_libdir}/wine/oleaut32.dll.so
%{_libdir}/wine/olecli32.dll.so
%{_libdir}/wine/oledb32.dll.so
%{_libdir}/wine/oledlg.dll.so
%{_libdir}/wine/olepro32.dll.so
%{_libdir}/wine/olesvr32.dll.so
%{_libdir}/wine/olethk32.dll.so
%{_libdir}/wine/opcservices.dll.so
%{_libdir}/wine/packager.dll.so
%{_libdir}/wine/pdh.dll.so
%{_libdir}/wine/photometadatahandler.dll.so
%{_libdir}/wine/pidgen.dll.so
%{_libdir}/wine/powrprof.dll.so
%{_libdir}/wine/presentationfontcache.exe.so
%{_libdir}/wine/printui.dll.so
%{_libdir}/wine/prntvpt.dll.so
%{_libdir}/wine/propsys.dll.so
%{_libdir}/wine/psapi.dll.so
%{_libdir}/wine/pstorec.dll.so
%{_libdir}/wine/qcap.dll.so
%{_libdir}/wine/qedit.dll.so
%{_libdir}/wine/qmgr.dll.so
%{_libdir}/wine/qmgrprxy.dll.so
%{_libdir}/wine/quartz.dll.so
%{_libdir}/wine/query.dll.so
%{_libdir}/wine/rasapi32.dll.so
%{_libdir}/wine/rasdlg.dll.so
%{_libdir}/wine/regapi.dll.so
%{_libdir}/wine/resutils.dll.so
%{_libdir}/wine/riched20.dll.so
%{_libdir}/wine/riched32.dll.so
%{_libdir}/wine/rpcrt4.dll.so
%{_libdir}/wine/rsabase.dll.so
%{_libdir}/wine/rsaenh.dll.so
%{_libdir}/wine/rstrtmgr.dll.so
%{_libdir}/wine/rtutils.dll.so
%{_libdir}/wine/samlib.dll.so
%{_libdir}/wine/sapi.dll.so
%{_libdir}/wine/sas.dll.so
%{_libdir}/wine/sc.exe.so
%{_libdir}/wine/scarddlg.dll.so
%{_libdir}/wine/sccbase.dll.so
%{_libdir}/wine/schannel.dll.so
%{_libdir}/wine/scrobj.dll.so
%{_libdir}/wine/scrrun.dll.so
%{_libdir}/wine/scsiport.sys.so
%{_libdir}/wine/secur32.dll.so
%{_libdir}/wine/sensapi.dll.so
%{_libdir}/wine/serialui.dll.so
%{_libdir}/wine/setupapi.dll.so
%{_libdir}/wine/sfc_os.dll.so
%{_libdir}/wine/shcore.dll.so
%{_libdir}/wine/shdoclc.dll.so
%{_libdir}/wine/shdocvw.dll.so
%{_libdir}/wine/schedsvc.dll.so
%{_libdir}/wine/shell32.dll.so
%{_libdir}/wine/shfolder.dll.so
%{_libdir}/wine/shlwapi.dll.so
%{_libdir}/wine/shutdown.exe.so
%{_libdir}/wine/slbcsp.dll.so
%{_libdir}/wine/slc.dll.so
%{_libdir}/wine/snmpapi.dll.so
%{_libdir}/wine/softpub.dll.so
%{_libdir}/wine/spoolsv.exe.so
%{_libdir}/wine/srclient.dll.so
%{_libdir}/wine/sspicli.dll.so
%{_libdir}/wine/stdole2.tlb.so
%{_libdir}/wine/stdole32.tlb.so
%{_libdir}/wine/sti.dll.so
%{_libdir}/wine/strmdll.dll.so
%{_libdir}/wine/subst.exe.so
%{_libdir}/wine/svchost.exe.so
%{_libdir}/wine/svrapi.dll.so
%{_libdir}/wine/sxs.dll.so
%{_libdir}/wine/systeminfo.exe.so
%{_libdir}/wine/t2embed.dll.so
%{_libdir}/wine/tapi32.dll.so
%{_libdir}/wine/taskkill.exe.so
%{_libdir}/wine/taskschd.dll.so
%{_libdir}/wine/tdh.dll.so
%{_libdir}/wine/tdi.sys.so
%{_libdir}/wine/traffic.dll.so
%{_libdir}/wine/ucrtbase.dll.so
%if 0%{?staging}
%{_libdir}/wine/uianimation.dll.so
%endif
%{_libdir}/wine/uiautomationcore.dll.so
%{_libdir}/wine/uiribbon.dll.so
%{_libdir}/wine/unicows.dll.so
%{_libdir}/wine/unlodctr.exe.so
%{_libdir}/wine/updspapi.dll.so
%{_libdir}/wine/url.dll.so
%{_libdir}/wine/urlmon.dll.so
%{_libdir}/wine/usbd.sys.so
%{_libdir}/wine/user32.dll.so
%{_libdir}/wine/usp10.dll.so
%{_libdir}/wine/uxtheme.dll.so
%if 0%{?staging}
%{_libdir}/wine/uxtheme-gtk.dll.so
%endif
%{_libdir}/wine/userenv.dll.so
%{_libdir}/wine/vbscript.dll.so
%{_libdir}/wine/vcomp.dll.so
%{_libdir}/wine/vcomp90.dll.so
%{_libdir}/wine/vcomp100.dll.so
%{_libdir}/wine/vcomp110.dll.so
%{_libdir}/wine/vcomp120.dll.so
%{_libdir}/wine/vcomp140.dll.so
%{_libdir}/wine/vcruntime140.dll.so
%{_libdir}/wine/vdmdbg.dll.so
%{_libdir}/wine/version.dll.so
%{_libdir}/wine/virtdisk.dll.so
%{_libdir}/wine/vssapi.dll.so
%{_libdir}/wine/vulkan-1.dll.so
%{_libdir}/wine/wbemdisp.dll.so
%{_libdir}/wine/wbemprox.dll.so
%{_libdir}/wine/wdscore.dll.so
%{_libdir}/wine/webservices.dll.so
%{_libdir}/wine/wer.dll.so
%{_libdir}/wine/wevtapi.dll.so
%{_libdir}/wine/wiaservc.dll.so
%{_libdir}/wine/wimgapi.dll.so
%{_libdir}/wine/winmgmt.exe.so
%if 0%{?staging}
%{_libdir}/wine/win32k.sys.so
%endif
%{_libdir}/wine/windowscodecs.dll.so
%{_libdir}/wine/windowscodecsext.dll.so
%{_libdir}/wine/winebus.sys.so
%{_libdir}/wine/winegstreamer.dll.so
%{_libdir}/wine/winehid.sys.so
%{_libdir}/wine/winejoystick.drv.so
%{_libdir}/wine/winemapi.dll.so
%{_libdir}/wine/winevulkan.dll.so
%{_libdir}/wine/winex11.drv.so
%{_libdir}/wine/wing32.dll.so
%{_libdir}/wine/winhttp.dll.so
%{_libdir}/wine/wininet.dll.so
%{_libdir}/wine/winmm.dll.so
%{_libdir}/wine/winnls32.dll.so
%{_libdir}/wine/winspool.drv.so
%{_libdir}/wine/winsta.dll.so
%{_libdir}/wine/wmasf.dll.so
%{_libdir}/wine/wmi.dll.so
%{_libdir}/wine/wmic.exe.so
%{_libdir}/wine/wmiutils.dll.so
%{_libdir}/wine/wmp.dll.so
%{_libdir}/wine/wmvcore.dll.so
%{_libdir}/wine/spoolss.dll.so
%{_libdir}/wine/winscard.dll.so
%{_libdir}/wine/wintab32.dll.so
%{_libdir}/wine/wintrust.dll.so
%{_libdir}/wine/winusb.dll.so
%{_libdir}/wine/wlanapi.dll.so
%{_libdir}/wine/wmphoto.dll.so
%{_libdir}/wine/wnaspi32.dll.so
%if 0%{?staging}
%{_libdir}/wine/wow64cpu.dll.so
%endif
%{_libdir}/wine/wpc.dll.so
%{_libdir}/wine/wpcap.dll.so
%{_libdir}/wine/ws2_32.dll.so
%{_libdir}/wine/wsdapi.dll.so
%{_libdir}/wine/wshom.ocx.so
%{_libdir}/wine/wsnmp32.dll.so
%{_libdir}/wine/wsock32.dll.so
%{_libdir}/wine/wtsapi32.dll.so
%{_libdir}/wine/wuapi.dll.so
%{_libdir}/wine/wuaueng.dll.so
%if 0%{?staging}
%{_libdir}/wine/wuauserv.exe.so
%endif
%{_libdir}/wine/security.dll.so
%{_libdir}/wine/sfc.dll.so
%{_libdir}/wine/wineps.drv.so
%{_libdir}/wine/d3d8.dll.so
%{_libdir}/wine/d3d9.dll.so
%{_libdir}/wine/opengl32.dll.so
%{_libdir}/wine/wined3d.dll.so
%{_libdir}/wine/dnsapi.dll.so
%{_libdir}/wine/iexplore.exe.so
%{_libdir}/wine/x3daudio1_0.dll.so
%{_libdir}/wine/x3daudio1_1.dll.so
%{_libdir}/wine/x3daudio1_2.dll.so
%{_libdir}/wine/x3daudio1_3.dll.so
%{_libdir}/wine/x3daudio1_4.dll.so
%{_libdir}/wine/x3daudio1_5.dll.so
%{_libdir}/wine/x3daudio1_6.dll.so
%{_libdir}/wine/x3daudio1_7.dll.so
%{_libdir}/wine/xapofx1_1.dll.so
%{_libdir}/wine/xapofx1_2.dll.so
%{_libdir}/wine/xapofx1_3.dll.so
%{_libdir}/wine/xapofx1_4.dll.so
%{_libdir}/wine/xapofx1_5.dll.so
%{_libdir}/wine/xaudio2_0.dll.so
%{_libdir}/wine/xaudio2_1.dll.so
%{_libdir}/wine/xaudio2_2.dll.so
%{_libdir}/wine/xaudio2_3.dll.so
%{_libdir}/wine/xaudio2_4.dll.so
%{_libdir}/wine/xaudio2_5.dll.so
%{_libdir}/wine/xaudio2_6.dll.so
%{_libdir}/wine/xaudio2_8.dll.so
%{_libdir}/wine/xaudio2_9.dll.so
%{_libdir}/wine/xcopy.exe.so
%{_libdir}/wine/xinput1_1.dll.so
%{_libdir}/wine/xinput1_2.dll.so
%{_libdir}/wine/xinput1_3.dll.so
%{_libdir}/wine/xinput1_4.dll.so
%{_libdir}/wine/xinput9_1_0.dll.so
%{_libdir}/wine/xmllite.dll.so
%{_libdir}/wine/xolehlp.dll.so
%{_libdir}/wine/xpsprint.dll.so
%{_libdir}/wine/xpssvcs.dll.so

%if 0%{?staging}
%ifarch x86_64 aarch64
%{_libdir}/wine/nvapi64.dll.so
%{_libdir}/wine/nvencodeapi64.dll.so
%else
%{_libdir}/wine/nvapi.dll.so
%{_libdir}/wine/nvencodeapi.dll.so
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/winevdm.exe.so
%{_libdir}/wine/ifsmgr.vxd.so
%{_libdir}/wine/mmdevldr.vxd.so
%{_libdir}/wine/monodebg.vxd.so
%{_libdir}/wine/rundll.exe16.so
%{_libdir}/wine/vdhcp.vxd.so
%{_libdir}/wine/user.exe16.so
%{_libdir}/wine/vmm.vxd.so
%{_libdir}/wine/vnbt.vxd.so
%{_libdir}/wine/vnetbios.vxd.so
%{_libdir}/wine/vtdapi.vxd.so
%{_libdir}/wine/vwin32.vxd.so
%{_libdir}/wine/w32skrnl.dll.so
%{_libdir}/wine/avifile.dll16.so
%{_libdir}/wine/comm.drv16.so
%{_libdir}/wine/commdlg.dll16.so
%{_libdir}/wine/compobj.dll16.so
%{_libdir}/wine/ctl3d.dll16.so
%{_libdir}/wine/ctl3dv2.dll16.so
%{_libdir}/wine/ddeml.dll16.so
%{_libdir}/wine/dispdib.dll16.so
%{_libdir}/wine/display.drv16.so
%{_libdir}/wine/gdi.exe16.so
%{_libdir}/wine/imm.dll16.so
%{_libdir}/wine/krnl386.exe16.so
%{_libdir}/wine/keyboard.drv16.so
%{_libdir}/wine/lzexpand.dll16.so
%{_libdir}/wine/mmsystem.dll16.so
%{_libdir}/wine/mouse.drv16.so
%{_libdir}/wine/msacm.dll16.so
%{_libdir}/wine/msvideo.dll16.so
%{_libdir}/wine/ole2.dll16.so
%{_libdir}/wine/ole2conv.dll16.so
%{_libdir}/wine/ole2disp.dll16.so
%{_libdir}/wine/ole2nls.dll16.so
%{_libdir}/wine/ole2prox.dll16.so
%{_libdir}/wine/ole2thk.dll16.so
%{_libdir}/wine/olecli.dll16.so
%{_libdir}/wine/olesvr.dll16.so
%{_libdir}/wine/rasapi16.dll16.so
%{_libdir}/wine/setupx.dll16.so
%{_libdir}/wine/shell.dll16.so
%{_libdir}/wine/sound.drv16.so
%{_libdir}/wine/storage.dll16.so
%{_libdir}/wine/stress.dll16.so
%{_libdir}/wine/system.drv16.so
%{_libdir}/wine/toolhelp.dll16.so
%{_libdir}/wine/twain.dll16.so
%{_libdir}/wine/typelib.dll16.so
%{_libdir}/wine/ver.dll16.so
%{_libdir}/wine/w32sys.dll16.so
%{_libdir}/wine/win32s16.dll16.so
%{_libdir}/wine/win87em.dll16.so
%{_libdir}/wine/winaspi.dll16.so
%{_libdir}/wine/windebug.dll16.so
%{_libdir}/wine/wineps16.drv16.so
%{_libdir}/wine/wing.dll16.so
%{_libdir}/wine/winhelp.exe16.so
%{_libdir}/wine/winnls.dll16.so
%{_libdir}/wine/winoldap.mod16.so
%{_libdir}/wine/winsock.dll16.so
%{_libdir}/wine/wintab.dll16.so
%{_libdir}/wine/wow32.dll.so
%endif

%files xaudio2
%{_libdir}/wine/xaudio2_7.dll.so

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/l_intl.nls

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

%if 0%{?staging}
%files arial-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/arial*
%endif #0%{?staging}

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
%if 0%{?staging}
%{_datadir}/wine/fonts/msyh.ttf
%endif

%files tahoma-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/tahoma*ttf

%files tahoma-fonts-system
%doc README-tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%if 0%{?staging}
%files times-new-roman-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/times.ttf

%files times-new-roman-fonts-system
%{_datadir}/fonts/wine-times-new-roman-fonts
%endif

%files symbol-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/symbol.ttf

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
%if 0%{?fedora} >= 10
%{_datadir}/icons/hicolor/*/apps/*png
%{_datadir}/icons/hicolor/scalable/apps/*svg
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%files systemd
%config %{_binfmtdir}/wine.conf
%endif

%if 0%{?rhel} == 6
%files sysvinit
%{_initrddir}/wine
%endif

# ldap subpackage
%files ldap
%{_libdir}/wine/wldap32.dll.so

# cms subpackage
%files cms
%{_libdir}/wine/mscms.dll.so

# twain subpackage
%files twain
%{_libdir}/wine/twain_32.dll.so
%{_libdir}/wine/sane.ds.so

# capi subpackage
%files capi
%{_libdir}/wine/capi2032.dll.so

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
%{_libdir}/*.so
%{_libdir}/wine/*.a
%{_libdir}/wine/*.def

%files pulseaudio
%{_libdir}/wine/winepulse.drv.so

%files alsa
%{_libdir}/wine/winealsa.drv.so

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%files openal
%{_libdir}/wine/openal32.dll.so
%endif

%if 0%{?fedora}
%files opencl
%{_libdir}/wine/opencl.dll.so
%endif

%changelog
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

* Tue Nov 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.21-100.chinfo
- 2.21
- Drop nine, it have proper separated wine-nine package now
- Drop laino package, only one patch is needed
- Update patch list from AUR

* Mon Nov 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.20-100.chinfo
- 2.20
- Rearrange files that are already in default wine from %%{?compholios} sections

* Mon Oct 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.19-101.chinfo
- wine-d3d9 2.19

* Sat Oct 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.19-100.chinfo
- 2.19

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.18-101.chinfo
- BR: mesa-libEGL-devel with nine, fixes Fedora 27 build

* Thu Oct 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.18-100.chinfo
- 2.18

* Wed Sep 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.17-100.chinfo
- 2.17

* Thu Sep 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.16-100.chinfo
- 2.16

* Wed Aug 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.15-100.chinfo
- 2.15

* Thu Aug 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.14-101.chinfo
- nine 2.14

* Tue Aug 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.14-100.chinfo
- 2.14

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.13-100.chinfo
- 2.13
- Disable laino patches

* Wed Jul 12 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.12-100.chinfo
- 2.12

* Tue Jun 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.11-100.chinfo
- 2.11

* Tue Jun 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.10-100.chinfo
- 2.10
- laino patches

* Mon May 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.9-100.chinfo
- 2.9

* Tue May 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.8-100.chinfo
- 2.8

* Tue May 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.7-100.chinfo
- 2.7

* Wed Apr 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.6-100.chinfo
- 2.6

* Sun Apr 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.5-100.chinfo
- 2.5

* Sun Mar 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.4-101.chinfo
- Fix wine-mono version

* Tue Mar 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.4-100.chinfo
- 2.4

* Mon Mar 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.3-100.chinfo
- 2.3

* Wed Feb 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.2-100.chinfo
- 2.2

* Thu Feb 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-100.chinfo
- 2.1

* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-100.chinfo
- 2.0 final

* Mon Jan 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.7.rc7.chinfo
- 2.0-rc6

* Mon Jan 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.6.rc5.chinfo
- 2.0-rc5

* Mon Jan 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.5.rc4.chinfo
- 2.0-rc4

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.4.rc3.nine
- rebuilt

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.3.rc3.nine
- Drop epoch.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.2.rc3.nine
- nine patches
- extra patches
- joy.cpl desktop file

* Tue Dec 27 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc3
- version update

* Wed Dec 21 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc2
- version update

* Thu Dec 15 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc1
- version update

* Wed Nov 23 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-2
- drop sysvinit on Fedora, again

* Wed Nov 16 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-1
- version update
- remove old cruft in spec
- add hard cups-libs dependency (rhbz#1367537)
- include mp3 support (rhbz#1395711)

* Thu Nov 03 2016 Michael Cronenworth <mike@cchtml.com> 1.9.22-1
- version update

* Mon Oct 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.21-1
- version update

* Sun Oct 02 2016 Michael Cronenworth <mike@cchtml.com> 1.9.20-1
- version update

* Mon Sep 19 2016 Michael Cronenworth <mike@cchtml.com> 1.9.19-1
- version update

* Thu Sep 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.18-2
- fix aarch64 definition

* Wed Sep 07 2016 Michael Cronenworth <mike@cchtml.com> 1.9.18-1
- version update

* Sun Aug 28 2016 Michael Cronenworth <mike@cchtml.com> 1.9.17-1
- version update

* Sat Aug 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.16-2
- build on aarch64

* Tue Aug 09 2016 Michael Cronenworth <mike@cchtml.com> 1.9.16-1
- version update

* Fri Jul 29 2016 Michael Cronenworth <mike@cchtml.com> 1.9.15-1
- version update

* Mon Jul 11 2016 Michael Cronenworth <mike@cchtml.com> 1.9.14-1
- version update

* Fri Jul 01 2016 Michael Cronenworth <mike@cchtml.com> 1.9.13-1
- version update

* Wed Jun 15 2016 Michael Cronenworth <mike@cchtml.com> 1.9.12-1
- version update

* Tue Jun 07 2016 Michael Cronenworth <mike@cchtml.com> 1.9.11-1
- version update

* Tue May 24 2016 Michael Cronenworth <mike@cchtml.com> 1.9.10-2
- gecko update

* Tue May 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.10-1
- version upgrade

* Sun May 01 2016 Michael Cronenworth <mike@cchtml.com> 1.9.9-1
- version upgrade

* Sun Apr 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.8-1
- version upgrade

* Sun Apr 03 2016 Michael Cronenworth <mike@cchtml.com> 1.9.7-1
- version upgrade

* Mon Mar 21 2016 Michael Cronenworth <mike@cchtml.com> 1.9.6-1
- version upgrade

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.5-2
- update mono requirement

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.5-1
- version upgrade

* Mon Feb 22 2016 Michael Cronenworth <mike@cchtml.com> 1.9.4-1
- version upgrade

* Mon Feb 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.3-1
- version upgrade

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Michael Cronenworth <mike@cchtml.com> 1.9.2-1
- version upgrade
- enable gstreamer support

* Sun Jan 10 2016 Michael Cronenworth <mike@cchtml.com> 1.9.1-1
- version upgrade

* Mon Dec 28 2015 Michael Cronenworth <mike@cchtml.com> 1.9.0-1
- version upgrade

* Wed Dec 23 2015 Michael Cronenworth <mike@cchtml.com> 1.8-1
- version upgrade

* Tue Dec 15 2015 Michael Cronenworth <mike@cchtml.com> 1.8-0.2
- version upgrade, 1.8-rc4
- enabling compiler optimizations again (-O2), thanks to gcc 5.3

* Sun Dec 06 2015 Michael Cronenworth <mike@cchtml.com> 1.8-0.1
- version upgrade, 1.8-rc3

* Sun Nov 15 2015 Michael Cronenworth <mike@cchtml.com> 1.7.55-1
- version upgrade

* Wed Nov 04 2015 Michael Cronenworth <mike@cchtml.com> 1.7.54-1
- version upgrade

* Wed Oct 21 2015 Michael Cronenworth <mike@cchtml.com> 1.7.53-1
- version upgrade

* Sat Oct 03 2015 Michael Cronenworth <mike@cchtml.com> 1.7.52-1
- version upgrade

* Tue Sep 08 2015 Michael Cronenworth <mike@cchtml.com> 1.7.51-1
- version upgrade

* Mon Aug 24 2015 Michael Cronenworth <mike@cchtml.com> 1.7.50-1
- version upgrade

* Fri Aug 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.49-2
- backport gecko 2.40 patch

* Fri Aug 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.49-1
- version upgrade

* Mon Aug 10 2015 Björn Esser <bjoern.esser@gmail.com> - 1.7.48-2
- rebuilt for mingw-wine-gecko-2.40

* Fri Jul 31 2015 Michael Cronenworth <mike@cchtml.com> 1.7.48-1
- version upgrade

* Sun Jul 12 2015 Michael Cronenworth <mike@cchtml.com> 1.7.47-1
- version upgrade

* Mon Jun 29 2015 Michael Cronenworth <mike@cchtml.com> 1.7.46-1
- version upgrade

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.45-1
- version upgrade

* Sun May 31 2015 Michael Cronenworth <mike@cchtml.com> 1.7.44-1
- version upgrade

* Mon May 18 2015 Michael Cronenworth <mike@cchtml.com> 1.7.43-1
- version upgrade

* Mon May 04 2015 Michael Cronenworth <mike@cchtml.com> 1.7.42-1
- version upgrade

* Sat Apr 18 2015 Michael Cronenworth <mike@cchtml.com> 1.7.41-1
- version upgrade
- Disable gstreamer support (rhbz#1204185)

* Mon Apr 06 2015 Michael Cronenworth <mike@cchtml.com> 1.7.40-1
- version upgrade

* Sun Mar 22 2015 Michael Cronenworth <mike@cchtml.com> 1.7.39-1
- version upgrade
- Enable some optimizations and workarounds for GCC5 regressions

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 1.7.38-3
- Drop sysvinit subpackage on F23+

* Sat Mar 07 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.38-2
- Fix wine-gecko and wine-mono versions

* Sat Mar 07 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.38-1
- version upgrade

* Sun Feb 22 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.37-1
- version upgrade

* Mon Feb 16 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.36-2
- Patch for RtlUnwindEx fix (staging bz #68)
- Use new systemd macros for binfmt handling

* Sun Feb 08 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.36-1
- version upgrade

* Wed Feb 04 2015 Orion Poplawski <orion@cora.nwra.com> - 1.7.35-3
- Add patch to fix stack smashing (bug #1110419)

* Mon Jan 26 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.35-2
- Rebuild (libgphoto2)

* Sun Jan 25 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.35-1
- version upgrade
- use alternatives system, remove wow sub-package

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.34-2
- Rebuild (libgphoto2)

* Sat Jan 10 2015 Michael Cronenworth <mike@cchtml.com>
- 1.7.34-1
- version upgrade
- enable OpenCL support (rhbz#1176605)

* Sun Dec 14 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.33-1
- version upgrade

* Sun Nov 30 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.32-1
- version upgrade
- wine-mono upgrade

* Fri Nov 14 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.31-1
- version upgrade
- wine-gecko upgrade
- add some missing arch requires

* Sun Nov 02 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.30-1
- version upgrade (rhbz#1159548)
- use winepulse patch from compholio patchset when build w/o
  compholio (rhbz#1151862)

* Fri Oct 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.29-1
- version upgrade

* Sun Oct 05 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.28-1
- version upgrade
- New sub-package for wingdings font system integration

* Wed Sep 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.27-1
- version upgrade

* Mon Sep 08 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.26-1
- version upgrade

* Sun Aug 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.25-1
- version upgrade

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.24-1
- version upgrade
- No longer install Wine fonts into system directory (rhbz#1039763)

* Thu Jul 17 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-4
- prevent accidential build with compholio-patchset on EPEL
- rebuild for pulseaudio (bug #1117683)

* Mon Jul 14 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-3
- dropped virtual Provides: %%{name}(compholio)

* Sat Jul 12 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-2
- added conditionalized option to build with compholio-patchset for pipelight
  Source900 -- compholio-patchset, wine-arial-fonts sub-package,
  BR: libattr-devel and configure --with-xattr for Silverlight DRM-stuff

* Fri Jul 11 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.22-1
- version upgrade

* Wed Jul 09 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.21-2
- Fixes for EPEL7 (rhbz#1117422)

* Tue Jul 01 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.21-1
- version upgrade

* Thu Jun 19 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.20-1
- version upgrade

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.19-1
- version upgrade

* Sat May 10 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.18-1
- version upgrade

* Fri Apr 25 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.17-2
- fix systemd binfmt location (rhbz#1090170)

* Tue Apr 22 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.17-1
- version upgrade

* Mon Apr 07 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.16-2
- explicitly require libpng (fixes rhbz#1085075)

* Mon Apr 07 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.16-1
- version upgrade

* Mon Mar 24 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.15-1
- version upgrade

* Sat Mar 08 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.14-1
- version upgrade

* Sun Feb 23 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.13-1
- version upgrade
- upgraded winepulse

* Sat Feb 08 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.12-1
- version upgrade

* Sun Jan 26 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.11-1
- version upgrade

* Thu Jan 09 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.10-1
- version upgrade
- upgraded winepulse

* Sun Dec 08 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.8-1
- version upgrade
- wine mono 4.5.2
- upgraded winepulse

* Sat Nov 23 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.7-1
- version upgrade

* Mon Oct 28 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.5-1
- version upgrade (rhbz#1023716)
- upgraded winepulse

* Sat Oct 12 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.4-1
- version upgrade (rhbz#1018601)

* Sat Sep 28 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.3-1
- version upgrade (rhbz#1008441)
- upgraded winepulse
- wine gecko 2.24
- fix systemd subpackage scriplet (rhbz#1010742)

* Sun Sep 15 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.2-1
- version upgrade
- workaround for rhbz#968860
- upgraded winepulse

* Sat Aug 31 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.1-2
- fix icons with patch provided by Frank Dana (rhbz#997543)
- pull in mesa-dri-drivers in meta package to make direct rendering work out
  of the box (rhbz#827776)
- restart systemd binfmt handler on post/postun (rhbz#912354)
- add arabic translation to fedora desktop files provided by Mosaab Alzoubi
  (rhbz#979770)

* Sat Aug 31 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.1-1
- version upgrade
- build with lcms2

* Sat Aug 17 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.0-1
- version upgrade
- wine pulse update

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Dennis Gilmore <dennis@ausil.us> - 1.6-2
- wine-desktop has architecture specific Requires so can not be noarch

* Sat Jul 20 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-1
- 1.6 release

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.6-0.5.rc5
- Perl 5.18 rebuild

* Fri Jul 12 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.4.rc5
- 1.6 rc5

* Sat Jun 29 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.3.rc4
- 1.6 rc4

* Thu Jun 27 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.2.rc3
- 1.6 rc3

* Sun Jun 16 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.1.rc2
- 1.6 rc2

* Thu May 30 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.31-1
- version upgrade
- upgraded winepulse
- wine gecko 2.21
- wine meta: require samba-winbind-clients for ntlm

* Tue May 14 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.30-1
- version upgrade

* Thu May 09 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.29-1
- version upgrade

* Sat Mar 30 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.27-1
- version upgrade

* Sun Mar 17 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.26-1
- version upgrade

* Tue Mar 05 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.25-1
- version upgrade
- now font package for wingdings family

* Mon Feb 18 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.24-1
- version upgrade

* Sun Feb 10 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.23-1
- version upgrade

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.5.22-2
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077
- Cleanup spec as per recently changed packaging guidelines
- fix bogus date changelog

* Sat Jan 19 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.22-1
- version upgrade
- upgraded winepulse
- wine gecko 1.9

* Sun Jan 06 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.21-1
- version upgrade

* Fri Dec 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.20-1
- version upgrade
- upgraded winepulse

* Sun Dec 09 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.19-1
- version upgrade
- upgraded winepulse

* Fri Nov 23 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.18-1
- version upgrade

* Mon Nov 12 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.17-1
- version upgrade
- upgraded winepulse

* Sun Oct 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.16-1
- version upgrade (rhbz#870611)
- wine mono 0.8
- update pulse patch
- fix midi in winepulse (rhbz#863129)
- fix dependencies for openssl (rhbz#868576)
- move wineboot.exe.so to -core instead of -wow (rhbz#842820)

* Mon Oct 15 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.15-1
- version upgrade
- wine gecko 1.8

* Sat Sep 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.14-1
- version upgrade

* Sat Sep 15 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.13-1
- version upgrade

* Fri Aug 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.12-1
- version upgrade

* Thu Aug 30 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.11-2
- rebuild on rawhide for fixed libOSMesa

* Sat Aug 18 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.11-1
- version upgrade
- use changed libOSMesa check from gentoo (>f18 still fails see rhbz#849405)

* Tue Jul 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.10-1
- version upgrade
- wine gecko 1.7

* Sat Jul 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.9-2
- isdn4linux now builds on ARM

* Wed Jul 18 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.9-1
- version upgrade
- clean up cjk patch to comply with default fonts where possible
- update fedora readme to point out required font packages per cjk locale

* Thu Jul 12 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.8-2
- bump for libgphoto2 2.5.0

* Wed Jul 04 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.8-1
- version upgrade (rhbz#834762)
- change {mingw-,}wine-mono require

* Sun Jun 24 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.7-1
- version upgrade (rhbz#834762)
- require new wine-gecko version

* Sat Jun 09 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.6-1
- version upgrade (rhbz#830424)
- split tahoma font package and add -system subpackage (rhbz#693180)

* Thu May 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.5-2
- fix description

* Mon May 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.5-1
- version upgrade (rhbz#817257)
- split out -filesystem and clean up -common/-core requires
- re-add winepulse driver (rhbz#821207, rhbz#783699)
- add font replacements for CJK to wine.inf and add information for cjk users
  to fedora readme (rhbz#815125, rhbz#820096)
- add support for and require wine-mono

* Mon May 14 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.4-1
- version upgrade

* Mon Apr 30 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.3-1
- version upgrade

* Sat Apr 21 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.2-2
- reenable xinput2 (rhbz#801436)

* Sat Apr 14 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.2-1
- version upgrade

* Sat Mar 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.1-1
- version upgrade

* Tue Mar 20 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.0-2
- require wine gecko from fedora mingw

* Mon Mar 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.0-1
- version upgrade

* Wed Mar 07 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-1
- version upgrade

* Tue Mar 06 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.8.rc6
- version upgrade

* Sat Feb 25 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.7.rc5
- version upgrade

* Tue Feb 21 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.6.rc4
- fix dependency issue (#795295)

* Sun Feb 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.5.rc4
- version upgrade

* Fri Feb 17 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.4.rc3
- version upgrade
- cleanup arm dependency fixes

* Fri Feb 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4-0.3.rc2
- Fix architecture dependencies on ARM so it installs

* Thu Feb 02 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.2.rc2
- version upgrade

* Sat Jan 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.1.rc1
- version upgrade

* Wed Jan 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.37-2
- Add initial support for wine on ARM

* Fri Jan 13 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.37-1
- version upgrade
- drop obsoleted patches

* Sat Dec 31 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.36-1
- version upgrade

* Mon Dec 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.35-1
- version upgrade

* Thu Dec 08 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.34-1
- version upgrade

* Sun Nov 20 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.33-1
- version upgrade(rhbz#755192)

* Sat Nov 05 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.32-1
- version upgrade (rhbz#745434)

* Fri Nov 04 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.31-2
- pull in correct wine-alsa arch in the pa meta package (rhbz#737431)

* Sun Oct 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.31-1
- version upgrade

* Mon Oct 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.30-1
- version upgrade

* Sat Sep 24 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.29-1
- version upgrade

* Sun Sep 11 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.28-1
- version upgrade
- require -alsa from -pulseaudio package for new sound api

* Mon Aug 29 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.27-1
- version upgrade
- fix epel build (rhbz#733802)

* Tue Aug 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-3
- drop pulse configure option
- fix f16 build (dbus/hal configure options)

* Mon Aug 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-2
- drop pulse patches
- make pulseaudio package meta and require alsa pa plugin
- update udisks patch

* Sun Aug 07 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-1
- version upgrade

* Fri Jul 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.25-1
- version upgrade
- remove -jack and -esd (retired upstream)
- rebase to Maarten Lankhorst's winepulse
- drop obsolete winepulse readme
- add udisks support from pending patches (winehq#21713, rhbz#712755)
- disable xinput2 (broken)

* Sun Jul 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.24-1
- version upgrade
- add sign as source10
- drop mshtml patch (upstream)

* Sun Jun 26 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.23-1
- version upgrade
- winepulse upgrade (0.40)
- fix gcc optimization problem (rhbz#710352, winehq#27375)

* Tue Jun 21 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.22-2
- workaround gcc optimization problem (rhbz#710352)

* Sun Jun 12 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.22-1
- version upgrade

* Sat May 28 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.21-1
- version upgrade

* Sun May 15 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.20-1
- version upgrade

* Sat Apr 30 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.19-1
- version upgrade (#701003)
- remove wine-oss
- disable hal (>=f16)

* Sat Apr 16 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.18-1
- version upgrade

* Thu Apr 07 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-3
- add fix for office installation (upstream #26650)

* Tue Apr 05 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-2
- cleanup spec file
- remove rpath via chrpath
- convert README files to utf8
- move SysV init script so sysvinit subpackage (>=f15)
- add some missing lsb keywords to init file
- create systemd subpackage and require it in the wine-desktop package (>=f15)
- disable embedded bitmaps in tahoma (#693180)
- provide readme how to disable wine-tahoma in fontconfig (#693180)

* Sat Apr 02 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-1
- version upgrade

* Fri Mar 18 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.16-1
- version upgrade
- cleanup unneeded patches
- drop some patches
- reenable smp build

* Thu Mar 17 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-3
- reenable fonts

* Sun Mar 13 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-2
- use svg files for icons (#684277)

* Tue Mar 08 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-1
- version upgrade

* Tue Mar 01 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.14-2
- prepare for wine-gecko

* Sat Feb 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.14-1
- version upgrade

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.13-1
- version upgrade
- update desktop files

* Mon Jan 24 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.12-1
- version upgrade

* Sun Jan 09 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.11-1
- version upgrade

* Tue Dec 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.10-1
- version upgrade

* Sat Dec 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.9-1
- version upgrade

* Sat Nov 27 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.8-1
- version upgrade
- require libXcursor (#655255)
- require wine-openal in wine meta package (#657144)

* Tue Nov 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.7-2
- cleanup cflags a bit

* Sat Nov 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.7-1
- version upgrade
- fix package description (#652718)
- compile with D_FORTIFY_SOURCE=0 for now to avoid breaking wine (#650875)

* Fri Oct 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.6-1
- version upgrade
- rebase winepulse configure patch
- add gstreamer BR for new gstreamer support
- add libtiff BR for new tiff support

* Mon Oct 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-1
- version upgrade

* Sun Oct 03 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.4-1
- version upgrade

* Wed Sep 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.3-2
- winepulse upgrade (0.39)

* Mon Sep 20 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.3-1
- version upgrade

* Wed Sep 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.2-1
- version upgrade

* Sat Aug 21 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.1-1
- version ugprade

* Sat Jul 31 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.0-1
- version upgrade

* Wed Jul 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2.0-2
- fix segfault (#617968)
- enable openal-soft on el6

* Fri Jul 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-1
- final release

* Fri Jul 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.8.rc7
- improve font patch

* Sun Jul 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.7.rc7
- version upgrade
- make sure font packages include the license file in case they are installed
  standalone

* Sun Jul 04 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.6.rc6
- version upgrade
- use new winelogo from user32
- winepulse upgrade

* Sun Jun 27 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.5.rc5
- version upgrade
- require liberation-narrow-fonts

* Fri Jun 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.4.rc4
- version upgrade
- fixes winecfg on 64bit (#541986)
- require wine-common from -core to ensure man pages and wine.inf are present
  (#528335)

* Sun Jun 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.3.rc3
- version upgrade

* Mon May 31 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.2.rc2
- version upgrade

* Mon May 24 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.1.rc1
- upgrade to rc1
- add BR for ImageMagick and icoutils
- spec cleanup
- install available icon files (#594950)
- desktop package requires wine x86-32 because of wine/wine64 rename
- put system/small fonts in right place

* Wed May 19 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-5
- fix font issues

* Thu May 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-4
- fix install of 32bit only wine on x86_64 via install wine.i686

* Wed May 12 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-3
- move wine symlink to -wow for 32bit (#591690)

* Tue May 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-2
- fix manpage conflict between -common and -devel

* Sun May 09 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-1
- version upgrade (#580024)

* Sun Apr 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.43-1
- version upgrade

* Sun Apr 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.42-1
- version upgrade
- rework for wow64

* Mon Mar 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-3
- add support for mingw32-wine-gecko

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-2
- convert to font package guidelines
- add libv4l-devel BR

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-1
- version upgrade (#577587, #576607)
- winepulse upgrade (0.36)

* Sat Mar 06 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.40-1
- version upgrade

* Sun Feb 21 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.39-1
- version upgrade

* Tue Feb 09 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.38-1
- version upgrade
- winepulse upgrade (0.35)

* Mon Jan 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.36-1
- version upgrade (#554102)
- require -common in -desktop (#549190)

* Sat Dec 19 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.35-1
- version upgrade

* Fri Dec 18 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.34-1
- version upgrade (#546749)

* Mon Nov 16 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.33-1
- version upgrade
- winepulse update (.33)
- require gnutls (#538694)
- use separate WINEPREFIX on x86_64 per default (workaround for #533806)
- drop explicit xmessage require (#537610)

* Tue Oct 27 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.32-1
- version upgrade (#531358)
- update winepulse

* Mon Sep 28 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.30-1
- version upgrade
- openal support
- drop steam regression patch

* Sun Sep 13 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-3
- patch for steam regression (upstream #19916)
- update winepulse winecfg patch

* Thu Sep 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-2
- rebuild for new gcc (#505862)

* Wed Sep 02 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-1
- version upgrade

* Mon Aug 24 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.28-1
- version upgrade
- make 32bit and 64bit version parallel installable

* Sun Aug 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.27-1
- version upgrade
- WinePulse 0.30

* Thu Aug 06 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.26-2
- build 32bit wine on x86_64 and prepare for 64bit parallel build (#487651)
- fix subpackage problems (#485410,#508766,#508944,#514967)
- fix nss dependencies on x86_64 (#508412)

* Sat Jul 18 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.26-1
- version upgrade
- WinePulse 0.29
- require Xrender isa for x86_64 (#510947)

* Thu Jul 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.25-1
- version upgrade (#509648)

* Mon Jun 29 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-3
- pull in nss correctly on x86_64

* Sun Jun 21 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-2
- adjust wine-menu to follow wine behavior (wine-wine instead of Wine)
  (fixes #479649, #495953)
- fix wine help desktop entry (#495953, #507154)
- add some more wine application desktop entries (#495953)
- split alsa/oss support into wine-alsa/wine-oss
- drop nas require from wine meta package
- fix dns resolution (#492700)

* Fri Jun 19 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-1
- version upgrade
- WinePulse 0.28
- drop meta package requires for jack and esd (#492983)

* Wed Jun 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.23-1
- version upgrade (#491321)
- rediff pulseaudio patch (Michael Cronenworth)

* Wed May 13 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.21-2
- fix uninstaller (#500479)

* Tue May 12 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.21-1
- version upgrade

* Mon Apr 27 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.20-1
- version upgrade

* Mon Mar 30 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.18-1
- version upgrade (#490672, #491321)
- winepulse update

* Sun Mar 15 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net> - 1.1.15-3
— Make sure F11 font packages have been built with F11 fontforge

* Tue Feb 24 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.15-2
- switch from i386 to ix86

* Sun Feb 15 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.15-1
- version upgrade
- new pulse patches

* Sat Jan 31 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.14-1
- version upgrade

* Sat Jan 17 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.13-1
- version upgrade
- fix gcc compile problems (#440139, #461720)

* Mon Jan 05 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.12-1
- version upgrade

* Sat Dec 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.10-1
- version upgrade
- add native pulseaudio driver from winehq bugzilla (#10495)
  fixes #474435, #344281

* Mon Nov 24 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.9-2
- fix #469907

* Sun Nov 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.9-1
- version upgrade

* Sun Oct 26 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.7-1
- version upgrade

* Thu Oct 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.6-1
- version upgrade
- fix multiarch problems (#466892,#467480)

* Sat Sep 20 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.5-1
- version upgrade

* Fri Sep 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.4-1
- version upgrade
- drop wine-prefixfonts.patch (#460745)

* Fri Aug 29 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.3-1
- version upgrade

* Sun Jul 27 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.2-1
- version upgrade (#455960, #456831)
- require freetype (#452417)
- disable wineprefixcreate patch for now

* Fri Jul 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.1-1
- version upgrade

* Tue Jun 17 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-1
- version upgrade (#446311,#417161)
- fix wine.desktop mime types (#448338)
- add desktop package including desktop files and binary handler (#441310)
- pull in some wine alsa/pulseaudio patches (#344281)

* Mon Jun 16 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.5.rc5
- version upgrade

* Fri Jun 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.4.rc4
- version upgrade

* Sun Jun 01 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.3.rc3
- version upgrade

* Fri May 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.2.rc2
- version upgrade
- add compile workaround for fedora 9/rawhide (#440139)

* Sat May 10 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.1.rc1
- version upgrade to rc1

* Mon May 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.61-1
- version upgrade

* Fri Apr 18 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.60-1
- version upgrade

* Sat Apr 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.59-1
- version upgrade

* Sat Mar 22 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.58-1
- version upgrade

* Tue Mar 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.57-1
- version upgrade

* Sat Feb 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.56-1
- version upgrade

* Sun Feb 10 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.55-1
- version upgrade

* Fri Jan 25 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.54-1
- version upgrade
- remove default pulseaudio workaround (#429420,#428745)
- improve pulseaudio readme

* Sun Jan 13 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.53-2
- add some missing BR

* Sat Jan 12 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.53-1
- version upgrade

* Sat Dec 29 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.52-2
- fix menu bug (#393641)

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.52-1
- version upgrade

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-3
- add -n Wine to pulseaudio workaround
- try to fix menu bug #393641

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-2
- add fix for #344281 pulseaudio workaround
- fix #253474: wine-jack should require jack-audio-connection-kit

* Sun Dec 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-1
- version upgrade

* Sat Dec 01 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.50-1
- version upgrade

* Tue Nov 13 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.49-1
- version upgrade

* Fri Oct 26 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.48-1
- version upgrade

* Sat Oct 13 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.47-1
- version upgrade

* Sun Oct 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.46-1
- version upgrade

* Sun Sep 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.45-1
- version upgrade

* Sat Aug 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.44-1
- version upgrade

* Sat Aug 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.43-2
- fix license
- fix #248999

* Sat Aug 11 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.43-1
- version upgrade
- fix init-script output (#252144)
- add lsb stuff (#247096)

* Sat Jul 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.42-1
- version upgrade

* Mon Jul 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.41-1
- version upgrade

* Tue Jul 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.40-1
- version upgrade

* Mon Jun 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.39-2
- fix desktop entries

* Sun Jun 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.39-1
- version upgrade
- convert to utf8 (#244046)
- fix mime entry (#243511)

* Wed Jun 06 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-3
- fix description

* Sun Jun 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-2
- allow full opt flags again
- set ExclusiveArch to i386 for koji to only build i386

* Sat Jun 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-1
- version upgrade (#242087)
- fix menu problem (#220723)
- fix BR
- clean up desktop file section

* Wed May 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.37-1
- version upgrade
- add BR for xcursor (#240648)
- add desktop entry for wineboot (#240683)
- add mime handler for msi files (#240682)
- minor cleanups

* Wed May 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.36-2
- fix BR (#238774)
- fix some typos

* Sat Apr 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.36-1
- version upgrade

* Mon Apr 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.35-1
- version upgrade (#234766)
- sources file comments (#235232)
- smpflags work again (mentioned by Marcin Zajączkowski)
- drop arts sound driver package, as it is no longer part of wine

* Sun Apr 01 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.34-1
- version upgrade

* Sat Mar 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.33-1
- version upgrade

* Sun Mar 04 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.32-1
- version upgrade

* Sat Feb 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.31-1
- version upgrade

* Wed Feb 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.30-1
- version upgrade

* Thu Jan 11 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.29-1
- version upgrade

* Mon Dec 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.27-1
- version upgrade (#220130)
- fix submenus (#216076)
- fix BR (#217338)

* Thu Nov 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.25-1
- version upgrade
- fix init script (#213230)
- fix twain subpackage content (#213396)
- create wine submenu (#205024)

* Sat Oct 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.24-1
- version upgrade

* Tue Oct 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.23-1
- version upgrade

* Sat Sep 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.22-1
- version upgrade

* Sun Sep 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.21-1
- version upgrade
- own datadir/wine (#206403)
- do not include huge changelogs (#204302)

* Mon Aug 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.20-1
- version upgrade

* Mon Aug 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.19-1
- version upgrade

* Thu Aug 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.18-1
- version upgrade

* Mon Jul 10 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.17-1
- version upgrade

* Thu Jun 29 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.16-1
- version upgrade
- rename wine to wine-core
- add meta package wine

* Fri Jun 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15-1
- version upgrade

* Tue May 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.14-1
- version upgrade

* Fri May 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-2
- enable dbus/hal support

* Mon May 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-1
- version upgrade

* Sat Apr 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.12-1
- fix rpath issues (#187429,#188905)
- version upgrade

* Mon Apr 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.11-1
- version upgrade
- fix #187546

* Mon Mar 20 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.10-2
- bump for x86_64 tree inclusion \o/

* Thu Mar 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.10-1
- version upgrade
- drop ancient extra fonts

* Fri Mar 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.9-1
- version upgrade

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.8-1
- version upgrade

* Thu Feb 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-3
- fix up tarball

* Wed Feb 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-2
- fix up post/preun scriplets (#178954)

* Thu Feb 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-1
- version upgrade

* Thu Jan 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.6-1
- version upgrade
- drop wmf exploit patch (part of current version)

* Sun Jan 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.5-2
- fix for CVE-2005-4560

* Fri Jan 06 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.5-1
- version upgrade
- fix #177089 (winemine desktop entry should be in Game not in System)
- fix cflags for compile
- test new BR

* Wed Jan 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-5
- fix #176834

* Mon Jan 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-4
- add dist

* Sun Jan 01 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-3
- use ExclusiveArch instead of ExcludeArch

* Sun Jan 01 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-2
- own font directory
- fix devel summary
- add ExcludeArch x86_64 for now

* Sat Dec 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-1
- version upgrade
- changed wine.init perissions to 0644
- added autoconf BR

* Mon Dec 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.3-1
- version upgrade

* Thu Nov 24 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.2-1
- version upgrade

* Thu Nov 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de
0.9.1-3
- fix typo in winefile desktop file
- drop in ld config instead of editing ld.so.conf

* Sun Nov 13 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.1-2
- add fontforge BR and include generated fonts...

* Sat Nov 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.1-1
- version upgrade
- move uninstaller and winecfg into wine main package...
- drop wine suite

* Sat Oct 29 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-3
- s/libwine/wine/

* Thu Oct 27 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-2
- remerge some subpackages which should be defaults

* Tue Oct 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-1
- upgrade to new version
- start splitting

* Mon Oct 24 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0-1.20050930
- add fedora readme
- switch to new (old) versioning sheme

* Sat Oct 22 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-3
- add desktop files
- revisit summary and description
- consistant use of %%{buildroot}

* Sat Oct 22 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-2
- some more spec tuneups...

* Sat Oct 01 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-1
- version upgrade

* Sun Sep 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050925-1
- upgrade to current cvs

* Mon Sep 19 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050830-1
- version upgrade

* Mon Sep 19 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050524-2
- fedorarized version

* Mon May 30 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050524-1fc3
- Update to 20050524
- Remove pdf documentation build as it's no more included in the main archive
- Workaround for generic.ppd installation

* Tue Apr 19 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050419-1fc3
- Update to 20050419

* Thu Mar 10 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050310-1fc3
- Update to 20050310

* Sat Feb 12 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050211-1fc3
- Update to 20050211

* Tue Jan 11 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050111-1fc3
- Update to 20050111

* Wed Dec 1 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20041201-1fc3
- Recompile for FC3
- Update to 20041201
- Small reorganization:
    - use the generic ICU static libs name;
    - no more wine group;
    - use Wine's generated stdole32.tlb file;
    - use Wine's generated fonts.

* Wed Oct 20 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20041019-1fc2
- Update to 20041019

* Wed Sep 15 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040914-1fc2
- Update to 20040914

* Sat Aug 14 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040813-1fc2
- Update to 20040813

* Sat Jul 17 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040716-1fc2
- Update to 20040716

* Fri Jun 25 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040615-1fc2
- Recompile for FC2
- Backport from current CVS some fixes to the preloader to prevent
  a segfault on startup
- Include a currently uncommitted patch from Alexandre Julliard regarding
  further issues with the preloader

* Sun Jun 20 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040615-1fc1
- Update to 20040615
- Use of wineprefixcreate instead of old RedHat patches

* Wed May 5 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040505-1fc1
- Update to 20040505

* Fri Apr 9 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040408-1fc1
- Update to 20040408
- Change the handling of paths to DOS drives in the installation process

* Wed Mar 17 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040309-1fc1
- Update to 20040309
- Replaced winedefault.reg by wine.inf

* Wed Feb 18 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040213-1fc1
- Update to 20040213
- Moved Wine dlls back to %%{_libdir}/wine rather than %%{_libdir}/wine/wine

* Sun Jan 25 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040121-fc1
- Update to 20040121

* Sat Dec 13 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031212-fc1
- Update to 20031212

* Tue Nov 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031118-fc1
- Update to 20031118

* Thu Oct 16 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031016-1rh9
- Update to 20031016

* Thu Sep 11 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030911-1rh9
- Fix of include location
- Better separation of run-time and development files
- Update to 20030911

* Wed Aug 13 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030813-1rh9
- Update to 20030813

* Wed Jul 09 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030709-1rh9
- Update to 20030709

* Wed Jun 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030618-1rh9
- Change the default C drive to ~/.wine/c, copied from /usr/share/wine
  if non-existant (Thanks to Rudolf Kastl)
- Updated to 20030618

* Tue May 20 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030508-1rh9
- Adapted for RH9

* Thu May 08 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030508-1
- Add libraries definition files to devel package
- Update to 20030508

* Tue Apr 08 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030408-1
- Update to 20030408

* Tue Mar 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030318-1
- Update to 20030318

* Tue Mar 11 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030219-2
- Fix the symlinks in wine-c.

* Wed Feb 19 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030219-1
- Update to 20030129
- Various fixes in RPM build process

* Fri Jan 17 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030115-1
- Update to 20030115
- fix to build problem

* Thu Nov  7 2002 Vincent Béron <vberon@mecano.gme.usherb.ca> 20021031-1
- Update to 20021031
- Tweaks here and there

* Wed Sep  4 2002 Bill Nottingham <notting@redhat.com> 20020605-2
- fix docs (#72923)

* Wed Jul 10 2002 Karsten Hopp <karsten@redhat.de> 20020605-1
- update
- remove obsolete part of redhat patch
- redo destdir patch
- redo kde patch
- redo defaultversion patch
- fix 'my_perl unknown' error
- work around name conflict with textutils 'expand'

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020327-1
- Fix wineshelllink (#61761)
- Fix up initscript (#53625)
- Clean up spec file
- Default to emulating Windoze ME rather than 3.1, nobody uses 3.1
  applications anymore
- Auto-generate default config if none exists (#61920)

* Mon Mar 04 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020304-1
- Assign gid 66 (closest to 666 [Microsoft number] we can get for a
  system account ;) )
- Don't use glibc private functions (__libc_fork)
- Update

* Tue Feb 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020226-1
- Fix bug #60250
- Update

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020221-1
- Update
- Don't try to launch winesetup in winelauncher, we aren't shipping it
  (#59621)

* Sun Jan 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020127-1
- Update
- Fix build in current environment

* Wed Aug 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010822-1
- Make sure the package can be cleanly uninstalled (#52007)
- Add build dependencies

* Thu Jul 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010726-1
- Fix -devel package group (#49989)
- remove internal CVS files
- chkconfig deletion should be in %%preun, not %%postun
- rename initscript ("Starting windows:" at startup does look off)

* Thu May 03 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010503-1
- Update
- generate HTML documentation rather than shipping plain docbook text
  (#38453)

* Sat Apr 14 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Update registry to mount "/" as drive "Z:", fixes winedbg (needs to be
  accessible from 'doze drives)
- Don't create KDE 1.x style desktop entries in wineshelllink
- Be more tolerant on failing stuff in %%post

* Thu Mar  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update

* Thu Feb 15 2001 Tim Powers <timp@redhat.com>
- fixed time.h build problems

* Wed Jan 31 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add a patch to handle .exe and .com file permissions the way we want them

* Thu Jan 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Restore wine's ability to use a global config file, it was removed
  in CVS for whatever reason
- Move libraries to %%{_libdir}/wine to prevent conflicts with libuser
  (Bug #24202)
- Move include files to /usr/include/wine to prevent it from messing with
  some autoconf scripts (some broken scripts assume they're running on windoze
  if /usr/include/windows.h exists...)

* Tue Dec 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix %%pre and %%postun scripts
- --enable-opengl, glibc 2.2 should be safe
- Update CVS

* Mon Nov 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update CVS
- Add a new (user) group wine that can write to the "C: drive"
  %%{_datadir}/wine-c
- Fix up winedbg installation (registry entries)
- Add "Program Files/Common Files" subdirectory to the "C: drive", it's
  referenced in the registry

* Wed Oct 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update

* Mon Aug 7 2000 Tim Powers <timp@redhat.com>
- rebuilt with new DGA

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- fix compilation with gcc 2.96

* Fri Jul 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move init script back
- new version
- move man pages to FHS locations

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move initscript
- new snapshot

* Fri Jun 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Start the initscript on startup

* Tue May  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- New version
- new feature: You can now launch wine by just running a windows .exe file
  (./some.exe or just click on it in kfm, gmc and the likes)
- some spec file modifications

* Sun Feb 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- newer version
- Improve the system.ini file - all multimedia stuff should work now.

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- enable and fix up the urlmon/wininet patch
- add: autoexec.bat, config.sys, windows/win.ini windows/system.ini
  windows/Profiles/Administrator
- allow i[456]86 arches
- add some system.ini configuration

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update current
- add urlmon and wininet patches from Corel (don't apply them for now though)
- create empty shell*dll and winsock*dll files (as mentioned in the HOWTO)

* Mon Jan 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current (lots of important fixes)
- Fix up the default wine.conf file (We really don't want it to look
  for CD-ROMs in /cdrom!)
- create a "root filesystem" with everything required to run wine without
  windows in %%{_datadir}/wine-c (drive c:)
- add RedHat file in /usr/doc/wine-%%{version} explaining the new directory
  layout
- wine-devel requires wine

* Tue Dec 14 1999 Preston Brown <pbrown@redhat.com>
- updated source for Powertools 6.2
- better files list

* Fri Jul 23 1999 Tim Powers <timp@redhat.com>
- updated source
- built for 6.1

* Tue Apr 13 1999 Michael Maher <mike@redhat.com>
- built package for 6.0
- updated package and spec file

* Mon Oct 26 1998 Preston Brown <pbrown@redhat.com>
- updated to 10/25/98 version.  There is really no point in keeping the
- older one, it is full of bugs and the newer one has fewer.
- commented out building of texinfo manual, it is horrendously broken.

* Mon Oct 12 1998 Michael Maher <mike@redhat.com>
- built package for 5.2
- pressured by QA, not updating.

* Fri May 22 1998 Cristian Gafton <gafton@redhat.com>
- repackaged for PowerTools
