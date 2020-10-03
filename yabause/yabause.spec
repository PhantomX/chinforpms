%global commit 7e38821dbac265490f115e163c523a939acda759
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180707
%global with_snapshot 1

# Enable ffmpeg support
%bcond_with ffmpeg

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

#undefine _hardened_build
%undefine _cmake_shared_libs

%global vc_url https://github.com/Yabause/%{name}

Name:           yabause
Version:        0.9.15
Release:        101%{?gver}%{?dist}
Summary:        A Sega Saturn emulator

License:        GPLv2+
URL:            http://yabause.org

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://download.tuxfamily.org/%{name}/releases/%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         %{name}-pr369.patch
Patch1:         yabause-0.9.15-RWX.patch
Patch2:         0001-Add-CHD-support.patch

BuildRequires:  cmake3
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glut)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  cmake(OpenAL)
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5OpenGL)
BuildRequires:  cmake(Qt5Widgets)
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libavutil)
%endif
Requires:       hicolor-icon-theme

%description
Yabause is a Sega Saturn emulator. A popular console of the early 1990s. It
includes an 'emulated' Saturn BIOS which is compatible with at least some games
but optionally a real Saturn BIOS can be used, however it is not included.


%prep

%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
cp -p %{name}/{COPYING,AUTHORS,ChangeLog,README} .
%else
%autosetup -p1
%endif

# fix end-of-line encoding
find \( -name \*.c\* -or -name \*.h\* -or -name AUTHORS \) -exec sed -i 's/\r$//' {} \;

#fix permissions
find \( -name \*.c\* -or -name \*.h\* \) -exec chmod -x {} \;

sed -e 's|share/pixmaps|share/icons/hicolor/32x32/apps|g' \
  -i %{name}/src/qt/CMakeLists.txt


%build
# Disable LTO. Segfaults
%define _lto_cflags %{nil}

export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

pushd mini18n
minii18n="$(pwd)"
%cmake3 \
%{nil}
%cmake_build
popd

%cmake3 \
  -S %{name} \
  -DYAB_PORTS=qt \
  -DYAB_OPTIMIZATION=-O2 \
  -DYAB_USE_CXX:BOOL=ON \
  -DYAB_NETWORK:BOOL=ON \
  -DYAB_OPTIMIZED_DMA:BOOL=ON \
  -DYAB_USE_SCSP2:BOOL=OFF \
  -DYAB_USE_SCSPMIDI:BOOL=ON \
  -DYAB_USE_SSF:BOOL=ON \
  -DMINI18N_INCLUDE_DIR:PATH=${minii18n}/src \
  -DMINI18N_LIBRARY:FILEPATH=${minii18n}/%{__cmake_builddir}/src/libmini18n.a \
%ifarch %{ix86} x86_64
  -DSH2_DYNAREC:BOOL=OFF \
%else
  -DSH2_DYNAREC:BOOL=OFF \
%endif
%if %{with ffmpeg}
  -DYAB_WANT_MPEG:BOOL=ON \
%endif
  -DOpenGL_GL_PREFERENCE=GLVND \
%{nil}

%cmake_build


%install
%cmake_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Tue Jul 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.15-101.20180707git7e38821
- CHD support

* Mon Jul 20 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.15-100.20180707git7e38821
- Snapshot

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 0.9.15-8
- Rebuild for glew 2.1.0

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.9.15-7
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Sat Jul 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.9.15-6
- Fix qt 5.11 build

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.9.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Oct 29 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.15-1
- Updated to 0.9.15
- Use Qt5 on F25 and above
- Switched to SDL2
- Updated Source0 URL
- Fixed permissions and end-of-line encoding rpmlint warnings/errors
- Modernised the .spec file
- Disabled dynarec on arm

* Thu Jun 02 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.14-2
- Disabled hardened build for now, assembly is not ready

* Sat Jun 06 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.14-1
- Updated to 0.9.14

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.9.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Apr 29 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.13.1-1
- Updated to 0.9.13.1
- Ensured optimization level -O2 is used

* Tue May 14 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.12-1
- Updated to 0.9.12
- Switched to the qt port
- Switched to the upstream .desktop file

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.11.1-2
- Mass rebuilt for Fedora 19 Features

* Tue Feb 21 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.11.1-1
- Updated to 0.9.11.1
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Updated scriptlets to the latest spec
- Switched to cmake
- Dropped the selinux patch

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 05 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.10-2
- Rebuilt against openal-soft

* Tue Jun 02 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.10-1
- Updated to 0.9.10
- Added openal-devel to BuildRequires
- Dropped unnecessary configure switches, they don't change anything

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.9-2
- rebuild for new F11 features

* Tue Jan 13 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.9-1
- Updated to 0.9.9
- Re-enabled parallel build

* Wed Dec 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.8-1
- Updated to 0.9.8
- Dropped obsolete docs

* Sun Oct 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.7-1
- Updated to 0.9.7
- Dropped addlimits patch
- Disabled paralled build

* Sun Sep 14 2008 Xavier Lamien <lxntow[at]gmail.com> - 0.9.3-2
- Update files and rebuild for rpmfusion for inclusion.

* Mon Jan 21 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.3-1
- Upgrade to 0.9.3

* Wed Jan 09 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.2-1
- Upgrade to 0.9.2

* Sun Nov 18 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.1-1
- Upgrade to 0.9.1
- Added patch for devel only to link against selinux possibly due to broken
  GL libs

* Fri Sep 28 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.0-1
- Upgrade to 0.9.0

* Tue Aug 28 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.6-1
- Upgrade to 0.8.6
- License field changed due to new guidelines
- Added patch needed for compilation with F8 (devel)

* Tue Jun 26 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.5-1
- Upgrade to 0.8.5
- Minor changes to SPEC for new Fedora guidelines

* Sun Mar 04 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.0-2
- Dropped dribble-menus requirement, due to be obsoleted
- Changed .desktop category to Game;Emulator;

* Thu Jan 04 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.0-1
- Upgrade to 0.8.0

* Wed Sep 20 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.2-1
- Upgrade to 0.7.2

* Wed Aug 30 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.1-1
- Upgrade to 0.7.1
- Removed big endian patch as it's now merged upstream

* Sat Aug 26 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.0-2
- Added libXt-devel buildrequire
- Added patch to fix compilation on big endian systems

* Wed Aug 23 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.0-1
- Initial Release
