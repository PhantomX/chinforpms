%undefine _cmake_shared_libs

%global commit 1e1c45be07bf5760e73414d9ed0253d6dedb8605
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240214
%bcond_without snapshot

%global commit10 bccaa94db814af33d8ef05c153e7c34d8bd4d685
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 SPIRV-Cross

%global commit11 9c7fd1a33e5cecbe465e1cd70170167d5e40d398
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 glslang

%bcond_with portaudio

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global glad_ver 2.0.3
%global imgui_ver 1.89.5

%global vc_url  https://github.com/snes9xgit/%{name}
%global kg_url  https://github.com/KhronosGroup

Name:           snes9x
Version:        1.62.3
Release:        9%{?dist}
Summary:        Super Nintendo Entertainment System emulator

License:        Other AND BSD-1-Clause AND Apache-2.0 AND BSD-3-Clause AND GPL-3.0-or-later AND CC0-1.0 AND MIT
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
Patch1:         0001-Use-system-libraries.patch
Patch2:         0001-Remove-application-path-from-database-search.patch
Patch3:         0001-format-security.patch

BuildRequires:   gcc-c++
BuildRequires:   cmake
BuildRequires:   autoconf
BuildRequires:   make
BuildRequires:   nasm
BuildRequires:   intltool
BuildRequires:   pkgconfig(alsa)
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
%if %{defined fedora} && 0%{?fedora} >= 38 && 0%{?fedora} < 40
BuildRequires:   minizip-compat-devel
%endif
%if %{defined fedora} && 0%{?fedora} >= 40
BuildRequires:   minizip-ng-compat-devel
%endif
BuildRequires:   cmake(VulkanHeaders) >= 1.3.249
%if %{with portaudio}
BuildRequires:   pkgconfig(portaudio-2.0)
%endif
BuildRequires:   desktop-file-utils
BuildRequires:   libappstream-glib
Requires:        hicolor-icon-theme
Requires:        vulkan-loader%{?_isa}


%global _description %{expand:
Snes9x is a portable, freeware Super Nintendo Entertainment System (SNES)
emulator. It basically allows you to play most games designed for the SNES
and Super Famicom Nintendo game systems on your computer.}

%description %_description


%package        common
Summary:        Super Nintendo Entertainment System emulator - common files
BuildArch:      noarch
Requires:       hicolor-icon-theme

%description    common
%_description

This package contains common file to %{name} sub packages.


%package gtk
Summary:        Super Nintendo Entertainment System emulator - GTK version
BuildRequires:  pkgconfig(gtkmm-3.0)
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(glslang) = 0~git%{shortcommit11}
Provides:       bundled(imgui) = %{imgui_ver}
Provides:       bundled(spirv-cross) = 0~git%{shortcommit10}

%description gtk %_description

This package contains a graphical user interface using GTK+.

%package qt
Summary:        Super Nintendo Entertainment System emulator - Qt version
BuildRequires:  cmake(cubeb)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
%dnl %{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(glslang) = 0~git%{shortcommit11}
Provides:       bundled(imgui) = %{imgui_ver}
Provides:       bundled(spirv-cross) = 0~git%{shortcommit10}

%description qt %_description

This package contains a graphical user interface using Qt.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -N -p1
%autopatch -M 500 -p1

%{?with_snapshot:tar -xf %{S:10} -C external/SPIRV-Cross --strip-components 1}
%{?with_snapshot:tar -xf %{S:11} -C external/glslang --strip-components 1}

# Remove bundled libs
rm -rf unzip

pushd external
rm -rf cubeb vulkan-headers
cp -p fmt/LICENSE.rst LICENSE.fmt
cp -p imgui/LICENSE.txt LICENSE.imgui
cp -p glslang/LICENSE.txt LICENSE.glslang
cp -p SPIRV-Cross/LICENSE LICENSE.SPIRV-Cross
cp -p VulkanMemoryAllocator-Hpp/LICENSE LICENSE.VulkanMemoryAllocator
popd

sed \
  -e 's|${MINIZIP_CFLAGS}|-I%{_includedir}/minizip|g' \
  -i gtk/CMakeLists.txt

cp -p gtk/data/%{name}-gtk.desktop %{name}-qt.desktop
cp -p %{SOURCE1} .
sed -e 's|%{name}-gtk|%{name}-qt|g' %{name}-gtk.appdata.xml > %{name}-qt.appdata.xml


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

pushd qt
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
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

pushd qt
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

mkdir -p %{buildroot}%{_bindir}
install -pm0755 qt/%{__cmake_builddir}/%{name}-qt %{buildroot}%{_bindir}/%{name}-qt

# Install AppData file
install -d %{buildroot}%{_metainfodir}
install -p -m 644 %{name}-{gtk,qt}.appdata.xml %{buildroot}%{_metainfodir}/

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-name="Snes9x Qt" \
  --set-key=Exec \
  --set-value="%{name}-qt %F" \
  --add-category=Qt \
  %{name}-qt.desktop


%find_lang %{name}-gtk


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gtk.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-qt.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml


%files
%license LICENSE
%doc docs/changes.txt
%doc unix/docs/readme_unix.html
%{_bindir}/%{name}

%files common
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%files gtk -f %{name}-gtk.lang
%license LICENSE external/LICENSE.*
%doc docs/changes.txt
%doc gtk/AUTHORS
%{_bindir}/%{name}-gtk
%{_metainfodir}/%{name}-gtk.appdata.xml
%{_datadir}/applications/%{name}-gtk.desktop


%files qt
%license LICENSE external/LICENSE.*
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_metainfodir}/%{name}-qt.appdata.xml


%changelog
* Wed Aug 30 2023 Phantom X <megaphantomx at hotmail dot com> - 1.62.3-5.20230827git94fbbfe
- Qt sub package

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

