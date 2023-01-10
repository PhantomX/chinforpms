%undefine _cmake_shared_libs

# Telegram Desktop's constants...
%global appname org.telegram.desktop
%global srcname tdesktop

# Telegram API tokens...
# https://github.com/telegramdesktop/tdesktop/blob/dev/snap/snapcraft.yaml
%global apiid 611335
%global apihash d524b414d21f4d37f08684c1df41ac9c

%global cvc_url https://chromium.googlesource.com
%global da_url https://github.com/desktop-app

# Enable or disable build with support...
# https://github.com/telegramdesktop/tdesktop/issues/23899
%bcond_without bundled_fonts
%bcond_without wayland
%bcond_without x11

# Reducing debuginfo verbosity...
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

%global kf5ver 4f35c8d

Name:           telegram-desktop
Version:        4.5.3
Release:        100%{?dist}
Summary:        Telegram Desktop official messaging app

Epoch:          1

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPL-3.0-or-later with OpenSSL exception -- main tarball;
# * tg_owt - BSD-3-Clause and Apache-2.0 -- static dependency or not;
# * rlottie - LGPL-2.1-or-later -- static dependency;
# * qt_functions.cpp - LGPL-3.0-only -- build-time dependency;
# * open-sans-fonts  - Apache-2.0 -- bundled font;
# * vazirmatn-fonts - OFL -- bundled font.
License:        GPL-3.0-or-later AND BSD-3-Clause AND Apache-2.0 AND LGPL-2.1-or-later AND LGPL-3.0-only AND OFL-1.1
URL:            https://github.com/telegramdesktop/%{srcname}

ExclusiveArch:  x86_64 aarch64

Source0:        %{url}/releases/download/v%{version}/%{srcname}-%{version}-full.tar.gz
Source20:       thunar-sendto-%{name}.desktop

Patch100:       %{name}-build-fix.patch

# Do not mess input text
# https://github.com/telegramdesktop/tdesktop/issues/522
Patch200:       %{name}-no-text-replace.patch
# Do not show unread counter on muted chats
Patch201:       %{name}-realmute.patch
# Always display scrollbars
Patch202:       %{name}-disable-overlay.patch
Patch203:       0001-Do-not-pop-up-emoji-tabbed-panel-and-media-menu-on-m.patch
Patch204:       %{name}-build-fixes.patch
Patch205:       0001-tgvoip-system-json11.patch
Patch206:       0001-fix-gsl-header-warnings.patch
Patch208:       0001-sane-background-and-text-colors.patch

BuildRequires:  cmake(Microsoft.GSL)
BuildRequires:  cmake(OpenAL)
BuildRequires:  cmake(range-v3)
BuildRequires:  cmake(tl-expected)

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(giomm-2.68)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glibmm-2.68)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(json11)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(sigc++-3.0)
BuildRequires:  pkgconfig(rnnoise)

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  libatomic
BuildRequires:  libdispatch-devel
BuildRequires:  libqrcodegencpp-devel
BuildRequires:  libstdc++-devel
BuildRequires:  minizip-compat-devel
BuildRequires:  ninja-build
BuildRequires:  python3

BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6OpenGLWidgets)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
Requires:       qt6-qtimageformats%{?_isa}

# kcoreaddons-qt6
BuildRequires:  extra-cmake-modules >= 5.98
BuildRequires:  cmake(Qt6LinguistTools)

%if %{with wayland}
BuildRequires:  cmake(PlasmaWaylandProtocols) >= 1.6.0
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6WaylandClient)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  qt6-qtbase-static
%endif

%if %{with x11}
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-record)
BuildRequires:  pkgconfig(xcb-screensaver)
%endif

BuildRequires:  cmake(absl) >= 20211102
BuildRequires:  cmake(tg_owt)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(protobuf-lite)
BuildRequires:  pkgconfig(vpx) >= 1.10.0

Requires:       hicolor-icon-theme
Recommends:     libdrm%{?_isa}
Recommends:     mesa-libgbm%{?_isa}
Recommends:     mesa-libEGL%{?_isa}
Recommends:     mesa-libGL%{?_isa}

%if %{with bundled_fonts}
Provides:       bundled(open-sans-fonts) = 1.10
Provides:       bundled(vazirmatn-fonts) = 27.2.2
%else
Requires:       open-sans-fonts
Requires:       vazirmatn-fonts
%endif

%if 0%{?fedora} && 0%{?fedora} >= 37
BuildRequires:  pkgconfig(webkit2gtk-4.1)
Requires:       webkit2gtk4.1%{?_isa}
%else
BuildRequires:  pkgconfig(webkit2gtk-4.0)
Requires:       webkit2gtk3%{?_isa}
%endif

# Telegram Desktop has major issues when built against ffmpeg 5.x:
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=6273
# Upstream refuses to fix this issue:
# https://github.com/telegramdesktop/tdesktop/issues/24855
# https://github.com/telegramdesktop/tdesktop/issues/23899
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires:  compat-ffmpeg4-devel
%else
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
%endif

# Video calls doesn't work when built against openssl 3.0:
# https://github.com/telegramdesktop/tdesktop/issues/24698
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires:  openssl1.1-devel
%else
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(openssl)
%endif

# Telegram Desktop can use native open/save dialogs with XDG portals.
Recommends:     xdg-desktop-portal%{?_isa}
Recommends:     (xdg-desktop-portal-gnome%{?_isa} if gnome-shell%{?_isa})
Recommends:     (xdg-desktop-portal-kde%{?_isa} if plasma-workspace-wayland%{?_isa})

# Short alias for the main package...
Provides: telegram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: telegram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# Virtual provides for bundled libraries...
Provides:       bundled(rlottie) = 0~git
Provides:       bundled(libtgvoip) = 2.4.4
Provides:       bundled(kf5-kcoreaddons) = 0~git%{kf5ver}


%description
Telegram is a messaging app with a focus on speed and security, it's super
fast, simple and free. You can use Telegram on all your devices at the same
time — your messages sync seamlessly across any number of your phones,
tablets or computers.

With Telegram, you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 50,000 people or
channels for broadcasting to unlimited audiences. You can write to your
phone contacts and find people by their usernames. As a result, Telegram is
like SMS and email combined — and can take care of all your personal or
business messaging needs.

%prep
# Unpacking Telegram Desktop source archive...
%autosetup -N -n %{srcname}-%{version}-full
%autopatch -p1 -M 999

cp -p %{S:20} thunar-sendto-%{name}.desktop

# Unbundling libraries...
rm -rf Telegram/ThirdParty/{GSL,QR,dispatch,expected,fcitx5-qt,fcitx-qt5,hime,hunspell,jemalloc,kimageformats,lz4,minizip,nimf,plasma-wayland-protocols,range-v3,wayland-protocols,xxHash}

sed -e 's|DESKTOP_APP_USE_PACKAGED|\0_DISABLED|g' \
  -i cmake/external/rlottie/CMakeLists.txt cmake/external/kcoreaddons/CMakeLists.txt

rm -f Telegram/ThirdParty/libtgvoip/json11.*
sed -e 's|DESKTOP_APP_USE_PACKAGED|\0_DISABLED|g' \
  -i Telegram/{cmake,ThirdParty/libtgvoip}/lib_tgvoip.cmake

rm -f Telegram/lib_ui/qt_conf/linux.qrc

find Telegram -type f \( -name '*.c*' -o -name '*.h*' \) -exec chmod -x {} ';'

sed -e '/CONFIG:Debug/d' -i cmake/options_linux.cmake

sed '/^SingleMainWindow/s|^|X-|g' -i lib/xdg/%{appname}.desktop

sed \
  -e 's|${third_party_loc}/wayland-protocols/|${WaylandProtocols_DATADIR}/|g' \
  -i Telegram/lib_ui/CMakeLists.txt \
  Telegram/lib_base/CMakeLists.txt Telegram/CMakeLists.txt

sed \
  -e 's|${third_party_loc}/plasma-wayland-protocols/src/protocols|${PLASMA_WAYLAND_PROTOCOLS_DIR}|g' \
  -i Telegram/CMakeLists.txt


%build
# Building Telegram Desktop using cmake...
%cmake \
    -G Ninja \
    -DCMAKE_BUILD_TYPE:STRING="Release" \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DTDESKTOP_API_ID=%{apiid} \
    -DTDESKTOP_API_HASH=%{apihash} \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
%if %{with bundled_fonts}
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=OFF \
%else
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
%endif
    -DDESKTOP_APP_QT6:BOOL=ON \
    -DDESKTOP_APP_DISABLE_WEBRTC_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
%if %{with wayland}
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
%else
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=ON \
%endif
%if %{with x11}
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
%else
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=ON \
%endif
    -DWaylandProtocols_DATADIR:PATH=%{_datadir}/wayland-protocols \
    -DPLASMA_WAYLAND_PROTOCOLS_DIR:PATH=%{_datadir}/plasma-wayland-protocols \
%{nil}

cp -p changelog.txt %{_vpath_builddir}/

%cmake_build


%install
%cmake_install

desktop-file-edit \
  --set-key=Exec \
  --set-value="%{_bindir}/%{name} -- %u" \
  --remove-key=Version \
  %{buildroot}%{_datadir}/applications/%{appname}.desktop

# sendto
mkdir -p "%{buildroot}%{_datadir}/Thunar/sendto"
desktop-file-install \
  --dir="%{buildroot}%{_datadir}/Thunar/sendto" \
  thunar-sendto-%{name}.desktop


%check
appstream-util validate-relax --nonet "%{buildroot}%{_metainfodir}/%{appname}.metainfo.xml"
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop


%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/Thunar/sendto/thunar-sendto-%{name}.desktop
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Mon Jan 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1:4.5.3-100
- 4.5.3

* Wed Jan 04 2023 Phantom X <megaphantomx at hotmail dot com> - 1:4.5.2-100
- 4.5.2

* Sat Dec 31 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.5.0-100
- 4.5.0

* Sun Dec 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.4.1-100
- 4.4.1

* Wed Dec 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.4.0-100
- 4.4.0

* Sun Nov 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.3.4-100
- 4.3.4

* Sun Nov 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.3.4-100
- 4.3.4

* Tue Nov 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.3.1-100
- 4.3.1

* Sat Nov 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.3.0-100
- 4.3.0

* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.2.4-100
- 4.2.4

* Sun Sep 25 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.2.2-100
- 4.2.2

* Fri Sep 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.2.1-100
- 4.2.1

* Mon Sep 19 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.2.0-101
- RPMFusion sync

* Sat Sep 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.2.0-100
- 4.2.0

* Fri Aug 19 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.1.1-100
- 4.1.1

* Sun Aug 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.1.0-100
- 4.1.0

* Fri Aug 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.0.4-100
- 4.0.4

* Wed Jul 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.0.2-101
- Rebuild (qt6)

* Sat Jun 25 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.0.2-100
- 4.0.2

* Sat Jun 25 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.0.1-100
- 4.0.1

* Tue Jun 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.0.0-100
- 4.0.0

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.7.6-100
- 3.7.6

* Fri May 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.7.5-100
- 3.7.5

* Thu May 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.7.4-100
- 3.7.4

* Fri Apr 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.7.3-100
- 3.7.3
- RPMFusion sync

* Mon Apr 25 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.7.2-100
- 3.7.2

* Thu Apr 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.7.1-100
- 3.7.1

* Sun Apr 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.7.0-100
- 3.7.0

* Thu Apr 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.6.3-100
- 3.6.3
- qt6

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.6.1-101
- ffmpeg5 patch

* Fri Mar 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.6.1-100
- 3.6.1

* Sun Mar 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.6.0-100
- 3.6.0

* Wed Mar 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.5.6-100
- 3.5.6

* Mon Mar 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.5.5-100
- 3.5.5

* Tue Feb 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.5.2-100
- 3.5.2

* Mon Feb 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.5.1-100
- 3.5.1
- RPMFusion sync
- Enable wayland support

* Tue Feb 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.5.0-100
- 3.5.0

* Thu Jan 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.4.8-100
- 3.4.8

* Mon Jan 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.4.5-100
- 3.4.5

* Tue Jan 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.4.3-100
- 3.4.3

* Sat Jan 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1:3.4.2-100
- 3.4.2

* Thu Dec 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.3.1-100
- 3.3.1
- BR: libdispatch

* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.3.0-100
- 3.3.0

* Wed Dec 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.2.8-100
- 3.2.8
- Remove old bundled tg_owt entries

* Tue Nov 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.2.5-100
- 3.2.5

* Wed Nov 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.2.0-100
- 3.2.0

* Tue Nov 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.1.13-100
- 3.1.13

* Fri Oct 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.1.8-100
- 3.1.7

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.1.5-100
- 3.1.5

* Mon Sep 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.1.4-100
- 3.1.4

* Mon Sep 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.1.0-100
- 3.1.0

* Mon Sep 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.0.4-100
- 3.0.4

* Fri Sep 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.0.1-100
- 3.0.1

* Wed Sep 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:3.0.0-100
- 3.0.0

* Mon Aug 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.9.8-100
- 2.9.8

* Wed Aug 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.9.4-100
- 2.9.4

* Thu Aug 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.9.3-100
- 2.9.3

* Sat Jul 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.9.0-100
- 2.9.0

* Sat Jul 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.8.13-100
- 2.8.13

* Fri Jul 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.8.10-100
- 2.8.10

* Wed Jul 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.8.6-100
- 2.8.6
- BR: jemalloc

* Sat Jun 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.8.0-100
- 2.8.0 with 2.8.1 fix
- %%bcond_without tg_owt
- BR: rnnoise

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.1-100
- Fix alsa and libpulse BRs

* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.1-1
- 2.7.1

* Fri Mar 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.7.0-1
- 2.7.0

* Thu Mar 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.6-1
- 2.6.6

* Tue Mar 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.4-1
- 2.6.4

* Tue Mar 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.1-100
- 2.6.1
- RPMFusion sync
- Bundled tg_owt (RPMFusion retired)
- Reenable lto

* Thu Feb 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-100
- 2.5.9

* Sat Jan 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.8-100
- 2.5.8

* Tue Jan 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.6-100
- 2.5.6

* Mon Jan 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.5-100
- 2.5.5

* Mon Jan  4 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.3-100
- 2.5.3

* Mon Dec 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.2-100
- 2.5.2

* Mon Dec 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.15-100
- 2.4.15

* Wed Dec 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.14-100
- 2.4.14

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.11-101
- Rebuild (qt5)

* Tue Nov 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.11-100
- 2.4.11

* Wed Nov 18 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.10-100
- 2.4.10

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.9-100
- 2.4.9

* Tue Nov 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.6-100
- 2.4.6
- RPMFusion sync

* Mon Nov 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.5-100
- 2.4.5

* Sun Oct 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.4-100
- 2.4.4

* Wed Oct 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.3-100
- 2.4.3

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.2-100
- 2.4.2
- RPMFusion sync

* Fri Sep 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.3.2-101
- RPMFusion sync

* Mon Aug 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.3.2-100
- 2.3.2
- Added tg_owt bundle

* Mon Aug 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.3.0-100
- 2.3.0
- Build with bundled rlottie and tgvoip for the time

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.2.0-100
- 2.2.0

* Fri Jul 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.22-100
- 2.1.22

* Mon Jul 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.20-100
- 2.1.20

* Thu Jul 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.19-100
- 2.1.19
- BR: qt5-qtwayland

* Wed Jul 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.18-100
- 2.1.18

* Fri Jul 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.17-100
- 2.1.17

* Wed Jul 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.16-100
- 2.1.16

* Thu Jun 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.13-100
- 2.1.13

* Thu Jun 18 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.12-100
- 2.1.12

* Mon Jun 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.1.11-101
- Rebuild (qt5)

* Mon Jun 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.11-100
- 2.1.11

* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.9-100
- 2.1.9

* Wed Jun 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.8-100
- 2.1.8

* Thu May 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.7-100
- 2.1.7

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.6-100
- 2.1.6

* Sat May 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.4-100
- 2.1.4

* Fri May 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.3-100
- 2.1.3

* Thu May 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.2-100
- 2.1.2
- RPMFusion sync

* Mon May 04 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.1-101
- Build with gcc again

* Fri May 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.1-100
- 2.1.1

* Fri Apr 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.1.0-100
- 2.1.0

* Wed Apr 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.0.1-100
- 2.0.1
- RPMFusion sync

* Tue Mar 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.21-100
- 1.9.21

* Mon Mar 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.20-100
- 1.9.20

* Wed Feb 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.14-100
- 1.9.19

* Wed Feb 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.14-100
- 1.9.14

* Wed Feb 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.13-100
- 1.9.13

* Mon Feb 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.10-100
- 1.9.10
- BR: dbusmenu-qt5-devel

* Wed Jan 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.9-100
- 1.9.9
- RPMFusion sync

* Fri Jan 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.8-100
- 1.9.8

* Thu Jan 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.7-100
- 1.9.7
- RPMFusion sync
- Full tarball

* Wed Jan 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.6-100
- 1.9.6
- RPMFusion sync

* Thu Jan 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.3-102
- RPMFusion sync

* Wed Jan 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.3-101
- Fix system font patch

* Tue Jan 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.3-100
- 1.9.3
- BR: enchant-devel
- Remove gyp, only cmake is needed

* Sun Dec 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.15-101
- Rebuild (qt5)

* Mon Oct 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.15-100
- 1.8.15

* Thu Oct 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.13-100
- 1.8.13
- RPMFusion sync

* Sun Sep 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.9-100
- 1.8.9

* Thu Sep 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.8-100
- 1.8.8
- RPMFusion sync

* Fri Sep 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.4-100
- 1.8.4

* Tue Aug 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.1-100
- 1.8.2

* Mon Aug 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.1-100
- 1.8.1
- RPMFusion sync. Bundled rlottie

* Fri Jul 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.14-102
- -O3 optimization with LTO builds

* Thu Jul 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.14-101
- RPMFusion sync. System rlottie

* Mon Jul 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.14-100
- 1.7.14

* Wed Jul 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.10-101
- Rebuild (qt5)

* Tue Jun 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.10-100
- 1.7.10

* Sun Jun 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.9-100
- 1.7.9

* Tue Jun 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.8-100
- 1.7.8

* Thu Jun 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.7-102
- Disable gtk3 integration by default

* Thu Jun 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.7-101
- Arch Linux patch to fix hidpi bug

* Mon Jun 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.7-100
- 1.7.7

* Thu Jun 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.6-100
- 1.7.6
- Thunar sendto

* Mon Jun 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.3-100
- 1.7.3
- RPMFusion sync

* Wed May 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.1-100
- 1.7.1
- Update crl
- qtlottie
- RPMFusion sync

* Fri May 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.0-100
- 1.7.0
- RPMFusion sync

* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.7-100
- 1.6.7

* Fri Apr 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.6-100
- 1.6.6

* Mon Apr 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.5-100
- 1.6.5

* Tue Mar 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.3-100
- 1.6.3

* Mon Mar 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.2-100
- 1.6.2

* Thu Mar 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.1-100
- 1.6.1

* Tue Mar 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.0-100
- 1.6.0

* Wed Mar 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.17-100
- 1.5.17

* Wed Mar 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.16-100
- 1.5.16

* Tue Feb 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.15-100
- 1.5.15
- RPMFusion sync (lto fixes)

* Mon Feb 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.12-100
- 1.5.12

* Sat Feb 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.11-100
- 1.5.11

* Thu Jan 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.9-100
- 1.5.9

* Tue Jan 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.8-100
- 1.5.8

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.7-100
- 1.5.7
- RPMFusion sync
- Drop opus BR, unneeded with libtgvoip with libraries link fixes

* Wed Jan 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.6-100
- 1.5.6
- Update crl

* Mon Dec 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.4-100
- 1.5.4

* Sun Dec 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.3-100
- 1.5.3

* Thu Dec 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.2-100
- 1.5.2
- RPMFusion sync

* Tue Dec 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.1-100
- 1.5.1
- RPMFusion sync

* Mon Dec 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.4.7-100.chinfo
- 1.4.7

* Sat Oct 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:1.4.4-100.chinfo
- 1.4.4

* Mon Oct 15 2018 Phantom X <megaphantomx at bol dot com dot br>  - 1:1.4.3-100.chinfo
- 1.4.3

* Sun Sep 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.4.0-100.chinfo
- 1.4.0

* Thu Sep 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.17-100.chinfo
- 1.3.17

* Thu Sep 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.16-100.chinfo
- 1.3.16
- RPMFusion sync
- Patch to always display scrollbars

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.15-100.chinfo
- 1.3.15
- RPMFusion sync

* Fri Aug 31 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.14-101.chinfo
- gcc gix

* Tue Aug 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.14-100.chinfo
- 1.3.14

* Sun Aug 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.12-100.chinfo
- 1.3.12

* Mon Jul 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.10-100.chinfo
- 1.3.10
- RPMFusion sync

* Fri Jul 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.9-101.chinfo
- Update libtgvoip requirements
- Remove gtk2 requirements

* Tue Jul 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.3.9-100.chinfo
- Add patches to fix some ugly issues that upstream will not fix

* Mon Jul 02 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.9-2
- Rebuild for libtgvoip update.

* Fri Jun 29 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.9-1
- Updated to 1.3.9.

* Sun Jun 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.8-1
- Updated to 1.3.8.

* Mon Jun 11 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.7-1
- Updated to 1.3.7.

* Mon Jun 11 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.6-1
- Updated to 1.3.6 (alpha).

* Sat Jun 09 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.5-1
- Updated to 1.3.5 (alpha).

* Fri Jun 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.4-1
- Updated to 1.3.4 (alpha).

* Thu Jun 07 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.3-1
- Updated to 1.3.3 (alpha).

* Tue Jun 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.1-1
- Updated to 1.3.1 (alpha).

* Fri Jun 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.3.0-1
- Updated to 1.3.0.

* Sat May 26 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.24-1
- Updated to 1.2.24 (alpha).

* Fri May 25 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.23-1
- Updated to 1.2.23 (alpha).

* Thu May 24 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.22-1
- Updated to 1.2.22 (alpha).

* Sat May 19 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.21-2
- Updated to 1.2.21 (alpha).

* Sun May 13 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.20-1
- Updated to 1.2.20 (alpha).

* Tue May 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.19-1
- Updated to 1.2.19 (alpha).

* Sat May 05 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.18-1
- Updated to 1.2.18 (alpha).

* Mon Apr 09 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.17-2
- Added custom API tokens.

* Sun Apr 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.17-1
- Updated to 1.2.17.

* Sun Apr 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.16-1
- Updated to 1.2.16.

* Mon Mar 26 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.15-1
- Updated to 1.2.15.

* Thu Mar 22 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.14-1
- Updated to 1.2.14.

* Wed Mar 21 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.13-1
- Updated to 1.2.13 (alpha).

* Mon Mar 12 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.12-1
- Updated to 1.2.12 (alpha).

* Sat Mar 10 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.11-1
- Updated to 1.2.11 (alpha).

* Fri Mar 09 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.10-1
- Updated to 1.2.10 (alpha).

* Thu Mar 08 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.9-1
- Updated to 1.2.9 (alpha).

* Wed Jan 03 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.8-1
- Updated to 1.2.8 (alpha).

* Mon Jan 01 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.7-1
- Updated to 1.2.7 (alpha).

* Sat Dec 30 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.6-1
- Updated to 1.2.6.

* Fri Dec 29 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.5-1
- Updated to 1.2.5 (alpha).

* Wed Dec 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.4-1
- Updated to 1.2.4 (alpha).

* Sun Dec 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.3-1
- Updated to 1.2.3 (alpha).

* Tue Dec 12 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.1-1
- Updated to 1.2.1.

* Sun Dec 10 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.2.0-1
- Updated to 1.2.0.

* Sat Dec 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.29-1
- Updated to 1.1.29 (alpha).

* Sat Dec 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.28-1
- Updated to 1.1.28 (alpha).

* Wed Dec 06 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.27-1
- Updated to 1.1.27 (alpha).

* Sat Dec 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.26-1
- Updated to 1.1.26 (alpha).

* Fri Dec 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.25-1
- Updated to 1.1.25 (alpha).

* Thu Nov 30 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.24-1
- Updated to 1.1.24 (alpha).

* Sat Nov 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.23-4
- Rebuild against libtgvoip 1.0.1.

* Fri Nov 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.23-3
- Rebuild for Qt 5.9 major update. Backported upstream patches.

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.1.23-2
- Rebuild for ffmpeg update

* Wed Sep 06 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.23-1
- Updated to 1.1.23.

* Mon Sep 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.22-1
- Updated to 1.1.22.

* Mon Sep 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.21-1
- Updated to 1.1.21.

* Fri Aug 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.19-2
- Moved VoIP library into a separate package.

* Wed Aug 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.19-1
- Updated to 1.1.19.

* Thu Jul 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.18-1
- Updated to 1.1.18.

* Thu Jul 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.17-1
- Updated to 1.1.17.

* Sun Jul 23 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.15-1
- Updated to 1.1.15.

* Wed Jul 19 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.14-1
- Updated to 1.1.14 (alpha).

* Fri Jul 14 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.13-1
- Updated to 1.1.13 (alpha).

* Wed Jul 12 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.12-1
- Updated to 1.1.12 (alpha).

* Sun Jul 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.11-2
- Fixed some small bugs.

* Fri Jul 07 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.11-1
- Updated to 1.1.11 (alpha).

* Tue Jul 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.10-1
- Updated to 1.1.10.

* Fri Jun 30 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.9-1
- Updated to 1.1.9.

* Wed May 31 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.7-1
- Updated to 1.1.7.

* Sat May 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.6-1
- Updated to 1.1.6 (alpha).

* Fri May 26 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.5-1
- Updated to 1.1.5 (alpha).

* Thu May 25 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.4-1
- Updated to 1.1.4 (alpha).

* Wed May 24 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.3-1
- Updated to 1.1.3 (alpha).

* Thu May 18 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.2-1
- Updated to 1.1.2.

* Wed May 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.1-1
- Updated to 1.1.1 (alpha).

* Tue May 16 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.0-3
- Backported patch with crash fixes.

* Mon May 15 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.0-2
- Restored russian locale.

* Sun May 14 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.1.0-1
- Updated to 1.1.0.

* Sun May 14 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.38-2
- Fixed rpmlint errors and warnings. Set soname for shared library.

* Sat May 13 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.38-1
- Updated to 1.0.38 (alpha).

* Wed May 10 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.37-1
- Updated to 1.0.37 (alpha).

* Wed May 10 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.36-1
- Updated to 1.0.36 (alpha).

* Sun Apr 30 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.35-1
- Updated to 1.0.35 (alpha).

* Sun Apr 30 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.34-2
- Rebuild for ffmpeg update

* Mon Apr 24 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.34-1
- Updated to 1.0.34 (alpha).

* Sun Apr 16 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.33-1
- Updated to 1.0.33 (alpha).

* Thu Apr 13 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.32-1
- Updated to 1.0.32 (alpha).

* Tue Apr 11 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.31-1
- Updated to 1.0.31 (alpha).

* Wed Apr 05 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.29-1
- Updated to 1.0.29.

* Tue Apr 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.28-1
- Updated to 1.0.28 (alpha).

* Mon Apr 03 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.27-3
- Strip binary into debuginfo subpackage.

* Sat Apr 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.27-2
- Built against system Qt.

* Fri Mar 31 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.27-1
- Updated to 1.0.27.

* Thu Mar 30 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.26-3
- Fixed build under GCC 7.0.

* Thu Mar 30 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.26-2
- Backported patch to fix build under Fedora 26+.

* Thu Mar 30 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.26-1
- Updated to 1.0.26.

* Wed Mar 22 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.25-1
- Updated to 1.0.25 (alpha).

* Sun Mar 19 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.24-1
- Updated to 1.0.24 (alpha).

* Fri Mar 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.23-2
- Added additional russian locale.

* Wed Mar 15 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.23-1
- Updated to 1.0.23 (alpha).

* Mon Mar 13 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.22-1
- Updated to 1.0.22 (alpha).

* Sat Mar 11 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.21-1
- Updated to 1.0.21 (alpha).
- Updated GSL build stage. Added Variant to build.

* Thu Mar 09 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.20-1
- Updated to 1.0.20 (alpha).

* Wed Mar 08 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.19-1
- Updated to 1.0.19 (alpha).

* Sat Mar 04 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.18-2
- Fixed build of latest commits. Added GSL support.

* Thu Mar 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.18-1
- Updated to 1.0.18 (alpha).

* Tue Feb 28 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.17-1
- Updated to 1.0.17 (alpha).

* Mon Feb 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.15-1
- Updated to 1.0.15 (alpha).

* Tue Feb 21 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.14-1
- Updated to 1.0.14.

* Mon Feb 20 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.13-1
- Updated to 1.0.13.
- Added changelog.txt to documents.

* Sun Feb 19 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.12-1
- Updated to 1.0.12.

* Fri Feb 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.11-1
- Updated to 1.0.11 (alpha).

* Sun Feb 12 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.9-1
- Updated to 1.0.9 (alpha).
- Updated GYP, Breakpad and LSS to latest commits.

* Thu Feb 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.6-2
- Backported QTBUG-56514 patch to fix building under GCC 7.0.

* Wed Feb 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.6-1
- Updated to 1.0.6.

* Fri Jan 27 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.3-1
- Updated to 1.0.3 (alpha).

* Thu Jan 19 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.2-1
- Updated to 1.0.2.

* Tue Jan 17 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.1-1
- Updated to 1.0.1.

* Thu Jan 12 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 1.0.0-1
- Updated to 1.0.0.

* Wed Jan 11 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.27-1
- Updated to 0.10.27 (alpha).

* Sat Jan 07 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.26-1
- Updated to 0.10.26 (alpha).

* Thu Jan 05 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.25-1
- Updated to 0.10.25 (alpha). Added patch to build with GCC 6.3.1.

* Mon Jan 02 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.23-1
- Updated to 0.10.23 (alpha). Updated externals to latest commits.

* Tue Dec 20 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.20-1
- Updated to 0.10.20.

* Sun Oct 30 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.19-2
- Fixed build under Fedora Rawhide (26).

* Tue Oct 25 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.19-1
- Updated to 0.10.19.

* Fri Oct 21 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.16-2
- Use specified revisions of 3rd-party libraries.

* Thu Oct 20 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.16-1
- Updated to 0.10.16.

* Wed Oct 19 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.15-1
- Updated to 0.10.15.

* Tue Oct 18 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.14-1
- Updated to 0.10.14.

* Sat Oct 08 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.11-3
- GYP will now export correct build flags for project.

* Sat Oct 08 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.11-2
- Will use configure macro to export correct build flags.

* Mon Oct 03 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.11-1
- Updated to 0.10.11.

* Wed Sep 21 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.7-1
- Updated to 0.10.7.

* Tue Sep 20 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.6-3
- Added new patch to build project using systemwide cmake.

* Sat Sep 17 2016 Vitaly Zaitsev <vitaly@easycoding.org> - 0.10.6-2
- Created new SPEC.
- Added installation of tg protocol and mime-handler.

* Wed Sep 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.6-1
- update to 0.10.6

* Mon Aug  8 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.1-2
- added appdata file

* Mon Aug  8 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.1-1
- update to 0.10.1

* Thu Aug  4 2016 Arkady L. Shane <ashejn@russianfedora.pro> 0.10.0-1
- update to 0.10.0

* Mon Jun 27 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.56-1.R
- update to 0.9.56

* Thu Jun 16 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.51-1.R
- update to 0.9.51

* Wed May 25 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.49-1.R
- update to 0.9.49

* Wed May 11 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.48-1.R
- update to 0.9.48

* Thu Apr 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.42-1.R
- update to 0.9.42

* Wed Apr 13 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.41-1.R
- update to 0.9.41

* Tue Apr  5 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.40-1.R
- update to 0.9.40

* Wed Mar 16 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.33-1.R
- update to 0.9.33

* Tue Mar 15 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.32-1.R
- update to 0.9.32

* Mon Feb 29 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.28-1.R
- update to 0.9.28

* Tue Feb 23 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.26-1.R
- update to 0.9.26

* Wed Feb 17 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.24-1.R
- update to 0.9.18

* Sun Jan 10 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.18-1.R
- update to 0.9.18

* Thu Dec 10 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.15-1.R
- update to 0.9.15

* Thu Nov 26 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.13-1.R
- update to 0.9.13

* Fri Nov 13 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.10-1.R
- update to 0.9.10

* Tue Oct 27 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.9.6-1.R
- clean up spec
- update to 0.9.6

* Mon Aug 03 2015 rommon <rommon@t-online.de> - 0.8.45-1
- update to new version

* Sat Jul 18 2015 rommon <rommon@t-online.de> - 0.8.38-1
- update to new version

* Fri Jun 26 2015 rommon <rommon@t-online.de> - 0.8.32-1
- update to new version
- rename from telegram to telegram-desktop

* Tue Jun 9 2015 rommon <rommon@t-online.de> - 0.8.24-1
- update to new version

* Fri May 1 2015 rommon <rommon@t-online.de> - 0.8.11-1
- update to new version

* Mon Apr 27 2015 rommon <rommon@t-online.de> - 0.8.7-1
- update to new version

* Mon Apr 27 2015 rommon <rommon@t-online.de> - 0.8.4-5
- fix icon permissions

* Fri Apr 24 2015 rommon <rommon@t-online.de> - 0.8.4-4
- fix desktop file

* Tue Apr 21 2015 rommon <rommon@t-online.de> - 0.8.4-3
- changed desktop file

* Tue Apr 21 2015 rommon <rommon@t-online.de> - 0.8.4-2
- adaption for 32/64 bit builds

* Tue Apr 21 2015 rommon <rommon@t-online.de> - 0.8.4-1
- initial package
