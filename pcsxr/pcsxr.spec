%global commit 62467b86871aee3d70c7445f3cb79f0858ec566e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190306
%global with_snapshot 1

%undefine _hardened_build

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           pcsxr
Version:        1.9.94
Release:        100%{?gver}%{?dist}
Summary:        A plugin based PlayStation (PSX) emulator with high compatibility

#All code is distributed as GPLv3+ except:
# SOURCE/libpcsxcore/coff.h is BSD License (no advertising)
# SOURCE/libpcsxcore/sjisfont.h is Public Domain
# SOURCE/libpcsxcore/psemu_plugin_defs.h is Public Domain
License:        GPLv3+ and BSD and Public Domain
Url:            https://github.com/iCatButler/pcsxr

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

#Appdata:
Source1:        %{name}.appdata.xml
#This is a hack to get it to build
#I would send a patch upstream if I knew how to fix this properly
Patch0:         0001-Fix-Pango-includedirs.patch
Patch10:        0001-Add-CHD-support.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  glibc-devel
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  nasm

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  hicolor-icon-theme

Requires:       hicolor-icon-theme


#modified from debian files
%description
PCSX-Reloaded is an advanced PlayStation (PSX) emulator, which uses a plugin
architecture to provide full support for all components of the PSX. It has full
emulation support for game pads, videos, sound, memory cards, and other
important PSX components, and is able to play many games without problems.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

#remove any unnecessary files:
rm -f -r win32 macosx
#Remove changes to c/cxx flags, upstream strips out debug symbols
sed -i '/CMAKE_C.*_FLAGS/d' CMakeLists.txt
#Remove cmake rule to install license, the license macro install it instead
sed -i '/COPYING/d' doc/CMakeLists.txt
#Add snapshot info into about dialog
sed -i 's/"git"/"%{version}-%{release}"/' gui/AboutDlg.c

%build
%cmake \
  -DUSE_LIBCDIO:BOOL=ON \
  -DUSE_LIBARCHIVE:BOOL=ON \
  -DENABLE_CHD:BOOL=ON \
  -DCMAKE_EXE_LINKER_FLAGS="$LDFLAGS -zmuldefs -fno-pie -Wl,-z,relro -Wl,-z,now" \
  -DCMAKE_MODULE_LINKER_FLAGS="$LDFLAGS -zmuldefs -Wl,-z,relro -Wl,-z,now" \
%{nil}

%cmake_build

%install
%cmake_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

#Install appdata.xml and verify
install -p -D -m 0644 %{SOURCE1} \
  %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

appstream-util validate-relax --nonet \
  %{buildroot}/%{_datadir}/appdata/*.appdata.xml

#Find locale
%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%{_docdir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_libdir}/games/psemu
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/icons/hicolor/*/apps/%{name}-icon.png


%changelog
* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1.9.94-100.20190306git62467b8
- CHD support

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-26.20190306.git62467b8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-25.20190306.git62467b8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 16 2020 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-24.20190306.git62467b8
- Fix LDFLAGS

* Sat May 16 2020 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-23.20190306.git62467b8
- Fix build

* Tue Mar 31 2020 Adrian Reber <adrian@lisas.de> - 1.9.94-22.20190306.git62467b8
- Rebuilt for libcdio-2.1.0

* Fri Mar 6 2020 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-21.20190306.git62467b8
- Update git snapshot
- Fix Fedora 31 build issues

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-20.20181218.git7ce3857
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-19.20181218.git7ce3857
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-18.20181218.git7ce3857
- Update to git version, old upstream is dead

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Adrian Reber <adrian@lisas.de> - 1.9.94-14
- Rebuilt for libcdio-2.0.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-11
- Backport fix for overflow issues

* Sun Feb 12 2017 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-10
- Backport fix for zlib-1.2.9+

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.94-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-8
- Appdata fixes

* Sun Dec 4 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-7
- Added patch for missing include

* Sat Nov 26 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-6
- Remove assert patch (issue was fixed in 1.9.93)
- Added appdata
- Removed unnecessary build require libglade2
- Updated source0 url

* Wed Nov 23 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-5
- Remove static libraries
- Use license macro for COPYING

* Wed Nov 23 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-4
- Use make macros
- Remove redundant prefix parameter in configure macro
- Use autosetup

* Wed Nov 02 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.9.94-3
- Disable hardening (rfbz#4316)

* Tue Oct 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.9.94-2
- Restore dist tag

* Mon Oct 27 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.94-1
- Updated to 1.9.94 release (marked as alpha on website)
- Use SDL2

* Sat Apr 5 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.93-2.svn89782
- Update to svn for Fedora 21 (beta 1.9.93 version doesn't build)

* Sat Apr 5 2014 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.93-1
- Updated to new beta release

* Thu May 30 2013 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-4.20130530svn85000
- Updated to new SVN version

* Sat Feb 16 2013 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-3.20130216svn82923
- Updated to new SVN version
- Changing version numbering to match Guidelines

* Fri Jan 4 2013 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-2.20130104svn82044
- Fixed missing gtk3 dependency

* Fri Jan 4 2013 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20130104svn82044
- Updated to new SVN checkout version
- Removed unnecessary zero length Doc file (NEWS)

* Mon Jul 23 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120723svn78971
- Added a patch to temporarily fix a 64bit-only problem

* Thu Jul 19 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120719svn78971
- Updated to new SVN checkout version
- Removed unnessary hicolor icon updating

* Thu Jul 5 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120705svn78288
- Updated to new SVN checkout version

* Fri Mar 9 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120421svn77577
- Updated to new SVN checkout version

* Fri Mar 9 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120309svn75683
- Updated to new SVN checkout version
- Changed define to global

* Sun Feb 19 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120219svn75200
- Updated to new SVN checkout version

* Sun Feb 19 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120219svn75156
- Updated to new SVN checkout version
- Added svn macro
- Removed incorrect disabling of opengl for 64bit

* Wed Feb 8 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-3.20120128svn73976
- Minor source change for convenience.

* Wed Feb 8 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-2.20120128svn73976
- Fixed and optimized source files for size and convenience.
- Added missing file in license breakdown

* Sat Jan 28 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120128svn73976
- Fixed version number to be more specific
- Fixed inproper license
- Trimmed down the source, removed non-linux code

* Sat Jan 28 2012 Jeremy Newton <alexjnewt AT hotmail DOT com> - 1.9.92-1.20120128svn
- Initial package SPEC created
