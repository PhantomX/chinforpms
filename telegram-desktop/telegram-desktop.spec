# Telegram Desktop's constants...
%global appname tdesktop
%global launcher telegramdesktop

# Telegram API tokens...
# https://github.com/telegramdesktop/tdesktop/blob/dev/snap/snapcraft.yaml
%global apiid 611335
%global apihash d524b414d21f4d37f08684c1df41ac9c

%global da_url https://github.com/desktop-app

# Enable or disable build with GTK support...
%bcond_without rlottie
%bcond_without spellcheck
%bcond_without ipo

%bcond_with clang

%ifarch x86_64
%bcond_without ipo
%else
%bcond_with ipo
%endif

%bcond_without tgvoip

%if %{with clang}
%global optflags %(echo %{optflags} | sed -e 's/-mcet//g' -e 's/-fcf-protection//g' -e 's/-fstack-clash-protection//g' -e 's/$/-Qunused-arguments -Wno-unknown-warning-option -Wno-deprecated-declarations/')
%endif

# Decrease debuginfo verbosity to reduce memory consumption...
%ifarch x86_64
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%else
%global optflags %(echo %{optflags} | sed 's/-g /-g2 /')
%endif

Name:           telegram-desktop
Version:        2.1.22
Release:        100%{?dist}
Summary:        Telegram Desktop official messaging app

Epoch:          1

# * Telegram Desktop - GPLv3+ with OpenSSL exception -- main tarball;
# * rlottie - LGPLv2+ -- static dependency;
# * qt_functions.cpp - LGPLv3 -- build-time dependency.
License:        GPLv3+ and LGPLv2+ and LGPLv3
URL:            https://github.com/telegramdesktop/%{appname}

ExclusiveArch:  x86_64

Source0:        %{url}/releases/download/v%{version}/%{appname}-%{version}-full.tar.gz

Source20:       thunar-sendto-%{name}.desktop

Patch100:       %{name}-pr8009.patch

# Do not mess input text
# https://github.com/telegramdesktop/tdesktop/issues/522
Patch200:       %{name}-no-text-replace.patch
# Do not show unread counter on muted chats
Patch201:       %{name}-realmute.patch
# Always display scrollbars
Patch202:       %{name}-disable-overlay.patch
Patch204:       %{name}-build-fixes.patch

Requires:       qt5-qtimageformats%{?_isa}
Requires:       hicolor-icon-theme
Requires:       open-sans-fonts

# Compilers and tools...
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libatomic-static
BuildRequires:  ninja-build

# Development packages for Telegram Desktop...
BuildRequires:  guidelines-support-library-devel >= 3.0.1
BuildRequires:  mapbox-variant-devel >= 0.3.6
BuildRequires:  libqrcodegencpp-devel
BuildRequires:  ffmpeg-devel >= 3.1
BuildRequires:  openal-soft-devel
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtsvg-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  qt5-qtwayland-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  wayland-devel
BuildRequires:  dbusmenu-qt5-devel
BuildRequires:  libstdc++-devel
BuildRequires:  expected-devel
BuildRequires:  lz4-devel
BuildRequires:  range-v3-devel >= 0.10.0
BuildRequires:  openssl-devel
BuildRequires:  xxhash-devel
BuildRequires:  xz-devel
BuildRequires:  python3
BuildRequires:  minizip-compat-devel

%if %{with spellcheck}
BuildRequires: glib2-devel
BuildRequires: hunspell-devel
Requires:      hunspell%{?_isa}
%endif

%if %{with clang}
BuildRequires: compiler-rt
BuildRequires: clang
BuildRequires: llvm
%endif

# Telegram Desktop require patched version of rlottie since 1.8.0.
# Pull Request pending: https://github.com/Samsung/rlottie/pull/252
%if %{with rlottie}
BuildRequires:  rlottie-devel
%else
Provides:       bundled(rlottie) = 0~git
%endif

%if %{with tgvoip}
BuildRequires:  libtgvoip-devel >= 2.4.4
%else
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  openssl-devel
BuildRequires:  json11-devel
BuildRequires:  opus-devel

Provides:       bundled(libtgvoip) = 0~git
%endif
Provides:       bundled(lxqt-qtplugin) = 0.14.0~git

# Short alias for the main package...
Provides: telegram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


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
%autosetup -n %{appname}-%{version}-full -p1

cp -p %{S:20} thunar-sendto-%{launcher}.desktop

# Unbundling libraries...
rm -rf Telegram/ThirdParty/{Catch,GSL,QR,SPMediaKeyTap,expected,fcitx-qt5,hime,hunspell,libdbusmenu-qt,libqtxdg,libtgvoip,lxqt-qtplugin,lz4,materialdecoration,minizip,nimf,qt5ct,range-v3,variant,xxHash}

%if %{with rlottie}
  rm -rf Telegram/ThirdParty/rlottie
%endif
%if %{with tgvoip}
  rm -rf Telegram/ThirdParty/libtgvoip
%endif

rm -f Telegram/lib_ui/qt_conf/linux.qrc

sed -e '/CONFIG:Debug/d' -i cmake/options_linux.cmake

# Fix private qt5 issues
cp -rs \
  %{_qt5_includedir}/QtXkbCommonSupport/%{_qt5_version}/QtXkbCommonSupport \
  Telegram/SourceFiles/


%build
%if %{with ipo} && %{without clang}
export CC=gcc
export CXX=g++

RPM_FLTO_FLAGS="-flto=%{_smp_build_ncpus} -fuse-linker-plugin"
export CFLAGS="$(echo %{optflags} | sed -e 's/-O2\b/-O3/') $RPM_FLTO_FLAGS"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="%{build_ldflags} $RPM_FLTO_FLAGS"
%endif

# Building Telegram Desktop using cmake...
%cmake \
    -B %{__cmake_builddir} \
    -G Ninja \
    -DCMAKE_BUILD_TYPE:STRING="Release" \
%if %{with clang}
    -DCMAKE_C_COMPILER=%{_bindir}/clang \
    -DCMAKE_CXX_COMPILER=%{_bindir}/clang++ \
    -DCMAKE_AR=%{_bindir}/llvm-ar \
    -DCMAKE_RANLIB=%{_bindir}/llvm-ranlib \
    -DCMAKE_LINKER=%{_bindir}/llvm-ld \
    -DCMAKE_OBJDUMP=%{_bindir}/llvm-objdump \
    -DCMAKE_NM=%{_bindir}/llvm-nm \
%else
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
%endif
%if %{without spellcheck}
    -DDESKTOP_APP_DISABLE_SPELLCHECK:BOOL=ON \
%endif
    -DTDESKTOP_API_ID=%{apiid} \
    -DTDESKTOP_API_HASH=%{apihash} \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_GSL:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_EXPECTED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_VARIANT:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_QRCODE:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
%if %{with rlottie}
    -DDESKTOP_APP_USE_PACKAGED_RLOTTIE:BOOL=ON \
    -DDESKTOP_APP_LOTTIE_USE_CACHE:BOOL=OFF \
%else
    -DDESKTOP_APP_USE_PACKAGED_RLOTTIE:BOOL=OFF \
%endif
%if %{with tgvoip}
    -DTDESKTOP_USE_PACKAGED_TGVOIP:BOOL=ON \
%endif
    -DDESKTOP_APP_USE_GLIBC_WRAPS:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
    -DTDESKTOP_DISABLE_GTK_INTEGRATION:BOOL=ON \
    -DTDESKTOP_DISABLE_REGISTER_CUSTOM_SCHEME:BOOL=ON \
    -DTDESKTOP_DISABLE_DESKTOP_FILE_GENERATION:BOOL=ON \
    -DTDESKTOP_USE_FONTCONFIG_FALLBACK:BOOL=OFF \
    -DTDESKTOP_LAUNCHER_BASENAME=%{launcher} \
%{nil}

%cmake_build


%install
%cmake_install

desktop-file-edit \
  --set-key=Exec \
  --set-value="%{_bindir}/%{name} -- %u" \
  %{buildroot}%{_datadir}/applications/%{launcher}.desktop

# sendto
mkdir -p "%{buildroot}%{_datadir}/Thunar/sendto"
desktop-file-install \
  --dir="%{buildroot}%{_datadir}/Thunar/sendto" \
  thunar-sendto-%{launcher}.desktop


%check
appstream-util validate-relax --nonet "%{buildroot}%{_metainfodir}/%{launcher}.appdata.xml"
desktop-file-validate %{buildroot}%{_datadir}/applications/%{launcher}.desktop


%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/%{name}
%{_datadir}/applications/%{launcher}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/Thunar/sendto/thunar-sendto-%{launcher}.desktop
%{_metainfodir}/%{launcher}.appdata.xml


%changelog
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
