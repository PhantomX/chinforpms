%global commit 315c6d3fc4137a111ac54f9f8bab33d70f1a9f34
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240901
%global sbuild 2308
%bcond_without snapshot

# Enable ffmpeg support
%bcond_without ffmpeg

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global lib7zip_ver 53abfeb
%global xdelta_ver 3.1.0

%global pkgname puNES
%global appname io.github.punesemu.%{pkgname}

Name:           punes
Version:        0.111
Release:        2%{?dist}
Summary:        Nintendo Entertainment System emulator

License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-3-Clause AND MIT
URL:            https://github.com/punesemu/%{pkgname}

# Use Makefile to download
%if %{with snapshot}
Source0:        %{pkgname}-free-%{shortcommit}.tar.xz
%else
Source0:        %{pkgname}-free-%{version}.tar.xz
%endif
Source10:       Makefile

Patch0:         0001-lib7zip-add-libexec-p7zip-search-path.patch
Patch10:        0001-p7zip-remove-rar.patch
Patch11:        0001-p7zip-hardening-flags.patch
Patch12:        0001-p7zip-Revert-commit-c104127.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6OpenGLWidgets)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       p7zip-plugins%{?_isa}
Requires:       hicolor-icon-theme

Provides:       bundled(filter-c) = 0~git
Provides:       bundled(kissfft) = 1.3.0
Provides:       bundled(lib7zip) = 0~git%{lib7zip_ver}
Provides:       bundled(singleapplication) = 3.5.1
Provides:       bundled(xdelta) = %{xdelta_ver}


%description
puNES is a Qt-based Nintendo Entertainment System emulator and NSF/NSF2/NSFe
Music Player.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1 -p1

pushd src/extra
rm -rf 7z1900 bdf2ttf windows

cp -p emu2413/LICENSE LICENSE.emu2413
cp -p filter-c/LICENSE LICENSE.filter-c
cp -p lib7zip-%{lib7zip_ver}/COPYING COPYING.lib7zip
cp -p kissfft/COPYING COPYING.kissfft
cp -p NTSC-CRT/LICENSE LICENSE.NTSC-CRT
cp -p PAL-CRT/LICENSE LICENSE.PAL-CRT
cp -p qkeycode/LICENSE LICENSE.qkeycode
cp -p singleapplication/LICENSE LICENSE.singleapplication
cp -p xdelta-%{xdelta_ver}/COPYING COPYING.xdelta
popd

sed \
  -e 's|(ENABLE_GIT_INFO|\0_DISABLED|' \
  -e '/CMAKE_INSTALL_DOCDIR/d' \
  -i CMakeLists.txt

%if %{with snapshot}
sed \
  -e 's|@GIT_COUNT_COMMITS@|%{sbuild}|' \
  -e 's|@GIT_LAST_COMMIT@|%{shortcommit}|' \
  -e 's|@GIT_LAST_COMMIT_HASH@|%{commit}|' \
  -i compiled.h.in
%endif

%build
%cmake \
  -G Ninja \
%if %{without ffmpeg}
  -DENABLE_FFMPEG:BOOL=OFF \
%endif
%if %{with snapshot}
  -DENABLE_GIT_INFO:BOOL=ON \
%endif
  -DENABLE_OPENGL_CG:BOOL=OFF \
  -DENABLE_QT6_LIBS:BOOL=ON \
  -DDISABLE_PORTABLE_MODE:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install


desktop-file-edit \
  --remove-key="GenericName" \
  --remove-key="Encoding" \
  %{buildroot}/%{_datadir}/applications/%{appname}.desktop


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license COPYING* src/extra/LICENSE.*
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{pkgname}/
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.png
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Sun Oct 06 2024 Phantom X <megaphantomx at hotmail dot com> - 0.111-2.20240901git315c6d3
- Rebuild (ffmpeg)

* Sat Sep 28 2024 Phantom X <megaphantomx at hotmail dot com> - 0.111-1.20240901git315c6d3
- Initial spec
