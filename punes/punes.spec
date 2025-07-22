%global commit ed201432b7186fed32ba8091afdeb9994295272b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250510
%global sbuild 2355
%bcond snapshot 1

# Enable ffmpeg support
%bcond ffmpeg 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global lib7zip_ver 53abfeb
%global sevenzip_ver 17.04
%global xdelta_ver 3.1.0

%global pkgname puNES
%global appname io.github.punesemu.%{pkgname}

Name:           punes
Version:        0.111
Release:        4%{?dist}
Summary:        NES emulator

License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-3-Clause AND MIT
URL:            https://github.com/punesemu/%{pkgname}

# Use Makefile to download
%if %{with snapshot}
Source0:        %{pkgname}-free-%{shortcommit}.tar.xz
%else
Source0:        %{pkgname}-free-%{version}.tar.xz
%endif
Source10:       Makefile

Patch0:         0001-lib7zip-add-libdir-punes-search-path.patch
Patch10:        0001-p7zip-remove-rar.patch
Patch11:        0001-p7zip-hardening-flags.patch
Patch12:        0001-p7zip-Revert-commit-c104127.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
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

%ifarch %{ix86}
BuildRequires:  nasm
%endif
%ifarch x86_64
BuildRequires:  yasm
%endif

Requires:       hicolor-icon-theme

Provides:       bundled(filter-c) = 0~git
Provides:       bundled(kissfft) = 1.3.0
Provides:       bundled(lib7zip) = 0~git%{lib7zip_ver}
Provides:       bundled(p7zip) = %{sevenzip_ver}
Provides:       bundled(singleapplication) = 3.5.1
Provides:       bundled(xdelta) = %{xdelta_ver}


%description
puNES is a Qt-based NES emulator and NSF/NSF2/NSFe Music Player.


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
cp -p p7zip-%{sevenzip_ver}/DOC/copying.txt COPYING.p7zip
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

sed \
  -e 's|_RPMLIBDIR_|%{_libdir}/%{name}|g' \
  -i src/extra/lib7zip-%{lib7zip_ver}/src/OSFunctions_UnixLike.cpp


%build
pushd src/extra/p7zip-%{sevenzip_ver}
pushd CPP/7zip/CMAKE/
sh ./generate.sh
popd
%ifarch %{ix86}
cp -f makefile.linux_x86_asm_gcc_4.X makefile.machine
%endif
%ifarch x86_64
cp -f makefile.linux_amd64_asm makefile.machine
%endif

%make_build common7z \
    OPTFLAGS="$CFLAGS" \
    LDFLAGS="$LDFLAGS" \
    DEST_HOME=%{_prefix} \
    DEST_BIN=%{_bindir} \
    DEST_SHARE=%{_libdir}/%{name}
popd

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

mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 src/extra/p7zip-%{sevenzip_ver}/bin/7z.so %{buildroot}%{_libdir}/%{name}/

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
%{_libdir}/%{name}/7z.so
%{_datadir}/%{pkgname}/
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.png
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Wed Dec 25 2024 Phantom X <megaphantomx at hotmail dot com> - 0.111-3.20240901git315c6d3
- Bundle p7zip

* Sun Oct 06 2024 Phantom X <megaphantomx at hotmail dot com> - 0.111-2.20240901git315c6d3
- Rebuild (ffmpeg)

* Sat Sep 28 2024 Phantom X <megaphantomx at hotmail dot com> - 0.111-1.20240901git315c6d3
- Initial spec
