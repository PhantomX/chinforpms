%global _lto_cflags %{nil}

%global commit 45762c8f9f5c5ecd73696d786dbfc6f9a869b525
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230403
%bcond_without snapshot

# Enable ffmpeg support
%bcond_without ffmpeg

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url https://github.com/mgba-emu/mgba

%global appname io.%{name}.mGBA

Name:           mgba
Version:        0.11.0
Release:        0.9%{?dist}
Summary:        A Nintendo Gameboy Advance Emulator

License:        MPL-2.0
URL:            http://mgba.io

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-vfs-lzma-update-bool-for-lzma-sdk.patch


BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(libedit)
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(lzmasdk-c) >= 22.01
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  libzip-tools
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  discount

Requires:       hicolor-icon-theme


%description
mGBA is an emulator for running Game Boy Advance games. It aims to be faster
and more accurate than many existing Game Boy Advance emulators, as well as
adding features that other emulators lack. It also supports Game Boy and
Game Boy Color games.


%package libs
Summary:        mGBA libraries
%description libs
Libraries used by mGBA.

%package devel
Summary:        mGBA development files
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files libraries needed for 
mGBA development.


%package sdl
Summary:        mGBA with SDL frontend
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mGBA = %{?epoch:%{epoch}:}%{version}-%{release}
%description sdl
mGBA with SDL frontend.

%package qt
Summary:        mGBA with Qt5 frontend
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mGBA-qt = %{?epoch:%{epoch}:}%{version}-%{release}
%description qt
mGBA with Qt5 frontend.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:r%{version}} -p1

rm -rf src/third-party/{discord-rpc,inih,libpng,lzma,sqlite3,zlib}

%if %{with snapshot}
sed -i \
  -e 's|${GIT_COMMIT}|%{commit}|g' \
  -e 's|${GIT_COMMIT_SHORT}|%{shortcommit}|g' \
  -e 's|${GIT_BRANCH}|master|g' \
  -e 's|${GIT_REV}|-1|g' \
  src/core/version.c.in
%endif

sed -e 's|BUILD_UPDATER ON|BUILD_UPDATER OFF|g' -i CMakeLists.txt


%build
%cmake \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -DSKIP_GIT:BOOL=ON \
  -DUSE_DISCORD_RPC:BOOL=OFF \
%if %{without ffmpeg}
  -DUSE_FFMPEG:BOOL=OFF \
%endif
  -DBUILD_UPDATER:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_datadir}/doc/mGBA %{name}-docs


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{appname}.desktop


%files sdl
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man6/%{name}.6*

%files qt
%license LICENSE
%doc README.md
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.png
%{_datadir}/%{name}/
%{_mandir}/man6/%{name}-qt.6*

%files libs
%license LICENSE %{name}-docs/licenses/blip_buf.txt
%doc README.md %{name}-docs/README.html
%{_libdir}/lib%{name}.so.*

%files devel
%license LICENSE
%{_includedir}/%{name}/
%{_includedir}/%{name}-util/
%{_libdir}/lib%{name}.so


%changelog
* Sun Oct 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0.11.0-0.1.20221016git2cea9e6
- 0.11.0 snapshot

* Thu Aug 04 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.20.20220727git4247fd0
- Bump

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.19.20220714git004f317
- Update

* Tue Jun 21 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.18.20220617git0dce8b3
- lzma-sdk rebuild

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.17.20220617git0dce8b3
- Bump

* Thu May 19 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.16.20220516git14e1552
- Update

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.15.20220423git69d4518
- Bump

* Sun Apr 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.14.20220403git969d36d
- Last snapshot

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.13.20220312git50e0fe9
- Bump

* Wed Mar 02 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.12.20220301git245a20b
- Update

* Sat Feb 12 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.11.20220212git9cfa712
- Bump

* Sun Jan 30 2022 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.10.20220127gitd071bff
- Last snapshot

* Sun Dec 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.9.20211206git2f8526a
- Update

* Wed Nov 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.8.20211123gitcf5d85a
- Bump

* Thu Oct 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.7.20211015gita997e2b
- Last snapshot

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.6.20210930git40d4c43
- Update

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.5.20210916git2ac6920
- Bump

* Sun Aug 15 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.4.20210814git2fec366
- Last snapshot

* Mon Jul 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.3.20210724git9d3b445
- Update

* Sun Jul 11 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.2.20210711git617bb0a
- Bump

* Sat Jun 19 2021 Phantom X <megaphantomx at hotmail dot com> - 0.10.0-0.1.20210618git34fed80
- 0.10.0 snapshot

* Sat May 08 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.1-2.20210507gite00987d
- Bump
- New lzma-sdk rebuild

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.1-1.20210419git2973211
- New snapshot

* Fri Apr 09 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-2.20210409gitafd9704
- Snapshot

* Mon Mar 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-1
- 0.9.0

* Sun Mar 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.12.20210328git00531d1
- Update

* Sun Mar 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.11.20210321git9e251c5
- Bump to fix save files issues

* Wed Mar 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.10.20210312git47728c7
- Last snapshot

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.9.20210210git2a35f06
- Update

* Sun Jan 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.8.20210124git40c3fc6
- Bump

* Thu Jan 07 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.7.20210106git3d4faa4
- Update

* Tue Dec 15 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.6.20201214git7b78906
- New snapshot

* Wed Nov 11 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.5.20201110git74edd96
- Bump

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.4.20201030git7bf7d02
- Update

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.3.20200927gita3d5e34
- New snapshot

* Mon Sep 14 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.2.20200914gitca67e63
- Bump to better #1875 fix

* Fri Sep 11 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.0-0.1.20200911git06a3770
- Snapshot

* Fri Sep 11 2020 Phantom X <megaphantomx at hotmail dot com> - 0.8.3-1
- Initial spec
