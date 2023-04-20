%undefine _cmake_shared_libs

%global commit bfdbc28357956eaf9009d4f9edd82c02a7513f70
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230417
%bcond_without snapshot

%global commit10 4e2fdb25671c742a9fbe93a6034eb1542244c7e1
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 SPIRV-Cross

%global commit11 6d41bb9c557c5a0eec61ffba1f775dc5f717a8f7
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 glslang

%bcond_with portaudio

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/snes9xgit/%{name}
%global kg_url  https://github.com/KhronosGroup

Name:           snes9x
Version:        1.62.3
Release:        1%{?dist}
Summary:        Super Nintendo Entertainment System emulator

License:        Other AND BSD-1-Clause AND Apache-2.0 AND BSD-3-Clause AND GPL-3.0-or-later AND CC0-1.0
URL:            http://www.snes9x.com/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}-gtk.appdata.xml
Source10:       %{kg_url}/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       %{kg_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz

# Fix CFLAGS usage in CLI version
Patch0:         %{name}-1.56.1-unix_flags.patch
Patch1:         0001-cmake-fix-data-files-install.patch
Patch2:         0001-gcc-13-build-fix.patch

Patch900:       https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator/commit/29d492b60c84ca784ea0943efc7d2e6e0f3bdaac.patch#/%{name}-gh-VulkanMemoryAllocator-29d492b.patch

BuildRequires:   gcc-c++
BuildRequires:   cmake
BuildRequires:   autoconf
BuildRequires:   make
BuildRequires:   nasm
BuildRequires:   intltool
BuildRequires:   pkgconfig(alsa)
BuildRequires:   pkgconfig(epoxy)
BuildRequires:   pkgconfig(gtkmm-3.0)
BuildRequires:   pkgconfig(gl)
BuildRequires:   pkgconfig(libpng)
BuildRequires:   pkgconfig(libpulse)
BuildRequires:   pkgconfig(libyuv)
BuildRequires:   pkgconfig(sdl2)
BuildRequires:   pkgconfig(xext)
BuildRequires:   pkgconfig(xinerama)
BuildRequires:   pkgconfig(xrandr)
BuildRequires:   pkgconfig(xv)
BuildRequires:   pkgconfig(wayland-client)
BuildRequires:   pkgconfig(wayland-egl)
BuildRequires:   pkgconfig(zlib)
BuildRequires:   minizip-ng-devel
BuildRequires:   cmake(VulkanHeaders)
%if %{with portaudio}
BuildRequires:   pkgconfig(portaudio-2.0)
%endif
BuildRequires:   desktop-file-utils
BuildRequires:   libappstream-glib
Requires:        hicolor-icon-theme
Requires:        vulkan-loader%{?_isa}

Provides:        bundled(glslang) = 0~git%{shortcommit11}
Provides:        bundled(spirv-cross) = 0~git%{shortcommit10}


%description
Snes9x is a portable, freeware Super Nintendo Entertainment System (SNES)
emulator. It basically allows you to play most games designed for the SNES
and Super Famicom Nintendo game systems on your computer.

%package gtk
Summary: Super Nintendo Entertainment System emulator - GTK version
Requires: hicolor-icon-theme

%description gtk
Snes9x is a portable, freeware Super Nintendo Entertainment System (SNES)
emulator. It basically allows you to play most games designed for the SNES
and Super Famicom Nintendo game systems on your computer.

This package contains a graphical user interface using GTK+.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -N -p1
%autopatch -M 500 -p1

%patch -P 900 -p1 -d external/VulkanMemoryAllocator-Hpp

%{?with_snapshot:tar -xf %{S:10} -C external/SPIRV-Cross --strip-components 1}
%{?with_snapshot:tar -xf %{S:11} -C external/glslang --strip-components 1}

# Remove bundled libs
rm -rf unzip

sed \
  -e 's|${MINIZIP_CFLAGS}|-I%{_includedir}/minizip|g' \
  -i gtk/CMakeLists.txt

pushd unix
autoreconf -ivf
popd


%build
# Build GTK version
pushd gtk
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%if !%{with portaudio}
  -DUSE_PORTAUDIO:BOOL=OFF \
%endif
%{nil}

popd

# Build CLI version
pushd unix
%configure \
  --with-system-zip \
  --enable-netplay \
%{nil}

popd

pushd gtk
%cmake_build
popd

pushd unix
%make_build
popd


%install
# Install GTK version
pushd gtk
%cmake_install
popd

# Install CLI version
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 unix/%{name} %{buildroot}%{_bindir}

# Validate desktop file
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/%{name}-gtk.desktop

# Install AppData file
install -d %{buildroot}%{_datadir}/metainfo
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/metainfo
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

%find_lang %{name}-gtk


%files
%license LICENSE
%doc docs/changes.txt
%doc unix/docs/readme_unix.html
%{_bindir}/%{name}


%files gtk -f %{name}-gtk.lang
%license LICENSE
%doc docs/changes.txt
%doc gtk/AUTHORS
%{_bindir}/%{name}-gtk
%{_datadir}/%{name}
%{_datadir}/metainfo/%{name}-gtk.appdata.xml
%{_datadir}/applications/%{name}-gtk.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Wed Apr 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.62.3-1.20230417gitbfdbc28
- 1.62.3

* Wed Mar 29 2023 Phantom X <megaphantomx at hotmail dot com> - 1.62.2-1.20230329gitafe8dd9
- 1.62.2

* Mon Mar 13 2023 Phantom X <megaphantomx at hotmail dot com> - 1.61-0.8.20230312gitcc0a877
- Vulkan support

* Mon May 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1.61-0.4.20220430git8c0a4a4
- Bump

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1.61-0.3.20220425gitf3fafab
- Bump
- meson->cmake

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.61-0.2.20220312gita8fafcd
- Update

* Mon Feb 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1.61-0.1.20220202gitf1ac3dc
- Last snapshot

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.60-104.20210825git46f11f6
- Bump

* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1.60-103.20210820gite66acce
- Update

* Fri May 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1.60-102.20210527git9398d21
- Bump
- Add forgotten BRs

* Fri Dec 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1.60-101.20201104git364aa1b
- Snapshot
- gtkmm3
- Portaudio switch

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Andrea Musuruane <musuruan@gmail.com> - 1.60-1
- Updated to 1.60

* Sat Mar 02 2019 Andrea Musuruane <musuruan@gmail.com> - 1.59.2-1
- Updated to 1.59.2
- Improved macro usage

* Fri Dec 21 2018 Andrea Musuruane <musuruan@gmail.com> - 1.58-1
- Updated to 1.58

* Sun Nov 25 2018 Andrea Musuruane <musuruan@gmail.com> - 1.57-1
- Updated to 1.57
- Updated BR to minizip-compat-devel for F30+

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.56.2-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.56.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 23 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.2-1
- Updated to 1.56.2

* Thu Jun 21 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.1-3
- Fixed joystick support (BZ #4947)

* Sat Jun 16 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.1-2
- Added an upstream patch to fix compiling on ppc64

* Sat Jun 16 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.1-1
- Updated to 1.56.1
- Removed obsolete scriptlets

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 26 2017 Andrea Musuruane <musuruan@gmail.com> - 1.55-1
- Updated to 1.55
- Added AppData file
- Added missing Requires

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.54.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.54.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Andrea Musuruane <musuruan@gmail.com> - 1.54.1-1
- Updated to 1.54.1
- Made separate gtk package
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped cleaning at the beginning of %%install

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.53-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.53-4
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.53-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun  1 2011 Matthias Saou <http://freshrpms.net/> 1.53-1
- Update to 1.53.
- Remove no longer needed patch and compile time lib hacks.

* Thu Oct 14 2010 Matthias Saou <http://freshrpms.net/> 1.52-2
- Add missing scriplets now that there are icons and a MimeType.

* Wed Aug 11 2010 Matthias Saou <http://freshrpms.net/> 1.52-1
- Update to 1.52, which is now hosted at google (sort of a unique fork).
- Now include the new gtk version, it also supports OpenGL.

* Wed May  6 2009 Matthias Saou <http://freshrpms.net/> 1.51-4
- Include patch to fix the current compilation errors.
- Quiet setup.

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.51-3
- rebuild for new F11 features

* Sat Oct 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.51-2
- rebuild for RPM Fusion
- always build for xorg

* Sat Aug 11 2007 Matthias Saou <http://freshrpms.net/> 1.51-1
- Update to 1.51.
- Bundle a second binary, osnes9x, the OpenGL version.
- Include useful readme_unix.txt.
- Remove no longer needed externc patch.

* Tue Oct 17 2006 Matthias Saou <http://freshrpms.net/> 1.50-1
- Update to 1.5... well, luckily it's also called 1.50 in some places, ugh.
- Update source URL.
- Include patch to fix C++ and C extern declarations.
- Remove no longer needed gcc4 patch.
- Remove no longer needed autoreconf and its build requirements.
- Remove no longer needed usagemsg patch, all now fits fine in 80 columns.
- Remove --without-assembler since build works again on i386 with it.
- Note : --with opengl doesn't work... some error in unix/opengl.cpp.

* Wed Mar 22 2006 Matthias Saou <http://freshrpms.net/> 1.43-7
- Add missing modular X build requirement.
- Add autoreconf call to fix configure's X detection.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 1.43-6
- Release bump to drop the disttag number in FC5 build.

* Tue Jan 24 2006 Matthias Saou <http://freshrpms.net/> 1.43-5
- Add wmclass patch from Bryan Moffit.

* Fri Jan 13 2006 Matthias Saou <http://freshrpms.net/> 1.43-4
- Add modular xorg build conditional.

* Thu Nov 10 2005 Matthias Saou <http://freshrpms.net/> 1.43-3
- Merge things from Ville's package : Usage message patch, optional OpenGL
  support using --with opengl.

* Thu May  5 2005 Matthias Saou <http://freshrpms.net/> 1.43-2
- Include gcc4 patch from Debian.
- Pass --without-assembler since build fails on i386/getset.S otherwise.

* Sun Apr 17 2005 Matthias Saou <http://freshrpms.net/> 1.43-1
- Update to 1.43 final (was WIP1).

* Sat Dec 18 2004 Matthias Saou <http://freshrpms.net/> 1.43-0
- Initial RPM release.

