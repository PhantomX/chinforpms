%global commit 5de47c6cf281d9941e3548f07a7d8c3ff29dfb5c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210811
%global with_snapshot 1

# Disable ffmpeg support
%bcond_without ffmpeg
# Enable Qt build
%bcond_with qt
# Enable EGL/GLESV2 (currently only working with Qt build)
%global with_egl 0

# Enable system ffmpeg
%global with_sysffmpeg 0
%if !0%{?with_sysffmpeg}
%global bundleffmpegver 3.0.2
%endif
# Use smaller ffmpeg tarball, with binaries removed beforehand (use Makefile to download)
%global with_smallffmpeg 1

# https://github.com/hrydgard/ppsspp/issues/13312
%global _lto_cflags %{nil}

%global commit2 a5baf97df4579b4614cd5e643241c7acfc36b0c4
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-ffmpeg

%global commit3 cbe88474ec196370161032a3863ec65050f70ba4
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 ffmpeg-gas-preprocessor

%global commit4 7885552b208493a6a0f21663770c446c3ba65576
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 armips

%global commit6 dc11adde23c455a24e13dd54de9b4ede8bdd7db8
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{name}-glslang

%global commit7 bab4e5911b1bfa5a86bc80006b7301ae48363844
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 SPIRV-Cross

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%undefine _hardened_build
%undefine _cmake_shared_libs

%global vc_url  https://github.com/hrydgard

%global jpgc_ver 1.05

Name:           ppsspp
Version:        1.11.3
Release:        117%{?gver}%{?dist}
Summary:        A PSP emulator
Epoch:          1

License:        BSD and GPLv2+
URL:            http://www.ppsspp.org/
%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
%if %{with ffmpeg}
%if !0%{?with_sysffmpeg}
%if 0%{?with_smallffmpeg}
Source2:        %{srcname2}-nobin-%{shortcommit2}.tar.xz
%else
Source2:        %{vc_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
%endif
Source3:        https://github.com/FFmpeg/gas-preprocessor/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%endif
%endif
Source4:        https://github.com/Kingcom/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source6:        %{vc_url}/glslang/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/KhronosGroup/SPIRV-Cross/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source10:       %{name}.appdata.xml
Source11:       Makefile

Patch0:         %{name}-noupdate.patch
Patch1:         0001-Disable-Discord-support.patch
Patch2:         0001-Set-pulseaudio-application-name.patch
Patch3:         0001-Use-system-libraries.patch
Patch4:         0001-Use-system-vulkan-headers.patch

%if !0%{?with_sysffmpeg}
ExclusiveArch:  %{ix86} x86_64 %{arm} %{mips32}
%endif
# https://github.com/hrydgard/ppsspp/issues/8823
ExcludeArch: %{power64}

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  make
%if %{with ffmpeg}
%if 0%{?with_sysffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
%else
Provides:       bundled(ffmpeg) = %{bundleffmpegver}
%endif
%endif
BuildRequires:  pkgconfig(gl)
%if 0%{?with_egl}
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
%else
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libglvnd)
%endif
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxxhash) >= 0.8.0
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(libzstd) >= 1.4.9
BuildRequires:  pkgconfig(miniupnpc) >= 2.1
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(snappy)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers >= 1.2.141
%if %{with qt}
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5OpenGL)
%endif

Requires:       vulkan-loader%{?_isa}
Requires:       hicolor-icon-theme
Requires:       google-roboto-condensed-fonts
Requires:       %{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(armips) = 0~git%{shortcommit4}
Provides:       bundled(gason)
Provides:       bundled(glslang) = 0~git%{shortcommit6}
Provides:       bundled(jpeg-compressor) = %{jpgc_ver}
Provides:       bundled(libkirk)
Provides:       bundled(sfmt19937)
Provides:       bundled(sha1-reichl)
Provides:       bundled(spirv-cross) = 0~git%{shortcommit7}
Provides:       bundled(xbrz)

Provides:       %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs < %{?epoch:%{epoch}:}%{version}-%{release}

%if %{with qt}
Provides:       %{name}-qt = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-qt < %{?epoch:%{epoch}:}%{version}-%{release}
%else
Provides:       %{name}-sdl = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-sdl < %{?epoch:%{epoch}:}%{version}-%{release}
%endif


%description
PPSSPP is a PSP emulator written in C++. It translates PSP CPU instructions
directly into optimized x86, x64, ARM or ARM64 machine code, using JIT
recompilers (dynarecs).


%package        data
Summary:        Data files of %{name}
BuildArch:      noarch

%description data
Data files of %{name}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

%if %{with ffmpeg}
%if !0%{?with_sysffmpeg}
tar -xf %{SOURCE2} -C ffmpeg --strip-components 1
tar -xf %{SOURCE3} -C ffmpeg/gas-preprocessor --strip-components 1
%endif
%endif
tar -xf %{SOURCE4} -C ext/armips --strip-components 1
tar -xf %{SOURCE6} -C ext/glslang --strip-components 1
tar -xf %{SOURCE7} -C ext/SPIRV-Cross --strip-components 1

rm -rf ext/glew/GL
rm -rf ext/{glew,rapidjson,miniupnp,snappy}/*.{c,cpp,h}
rm -rf ext/{libpng,libzip,vulkan,zlib,zstd}*
rm -f ext/xxhash.*
rm -rf MoltenVK/*

find ext Core -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" -o -name "*.y" \) -exec chmod -x {} ';'

%if 0%{?with_snapshot}
sed -i \
  -e "/GIT_VERSION/s|unknown|%{version}-%{release}|g" \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} describe --always|echo \"%{version}-%{release}\"|g" \
  git-version.cmake
%endif

sed \
  -e 's|"unknown"|"%{shortcommit7}"|' \
  -e 's| unknown | %{shortcommit7} |' \
  -e 's|GIT_FOUND|GIT_FOUND_DISABLED|g' \
  -i ext/SPIRV-Cross/CMakeLists.txt

cp Qt/PPSSPP.desktop %{name}.desktop

sed \
  -e '/Wno-deprecated-register/d' \
  -e '/Wno-tautological-pointer-compare/d' \
  -i CMakeLists.txt

sed \
  -e 's| -O3 | -O2 |g' \
  -i CMakeLists.txt ext/armips/ext/tinyformat/Makefile

%if %{with ffmpeg}
%if !0%{?with_sysffmpeg}
pushd ffmpeg
sed \
  -e '/^ARCH=/s|=.*|=%{_target_cpu}|g' \
  -e '/extra-cflags/s|-O3|%{build_cflags}|g' \
  -e 's|disable-everything|\0 --disable-debug --disable-stripping|g' \
  -e '/make install/d' \
  -i linux_*.sh

rm -rf */*/include
rm -rf */*/lib
rm -rf wiiu

popd
%endif
%endif


%build
export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

%if %{with ffmpeg}
%if !0%{?with_sysffmpeg}
pushd ffmpeg
%ifarch x86_64
./linux_x86-64.sh
%endif
%ifarch %{ix86}
./linux_x86.sh
%endif
%ifarch %{arm}
./linux_arm.sh
%endif
%ifarch %{mips32}
./linux_mips32.sh
%endif
%make_build
make install
popd
%endif
%endif

%cmake \
%if 0%{?with_egl}
  -DUSING_EGL:BOOL=ON \
  -DUSING_GLES2:BOOL=ON \
%endif
  -DOpenGL_GL_PREFERENCE=GLVND \
%if %{with ffmpeg}
%if 0%{?with_sysffmpeg}
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
%endif
%else
  -DUSE_FFMPEG:BOOL=OFF \
%endif
  -DUSE_SYSTEM_LIBZIP:BOOL=ON \
  -DUSE_SYSTEM_MINIUPNPC:BOOL=ON \
  -DUSE_SYSTEM_SNAPPY:BOOL=ON \
  -DUSE_SYSTEM_XXHASH:BOOL=ON \
  -DUSE_SYSTEM_ZSTD:BOOL=ON \
  -DUSE_DISCORD:BOOL=OFF \
  -DUSE_WAYLAND_WSI:BOOL=ON \
  -DUSING_X11_VULKAN:BOOL=ON \
  -DENABLE_HLSL:BOOL=OFF \
  -DENABLE_GLSLANG_BINARIES:BOOL=OFF \
%ifarch %{ix86}
  -DX86:BOOL=ON \
%endif
%ifarch %{arm} aarch64
  -DARM:BOOL=ON \
%endif
%ifarch armv7l armv7hl armv7hnl
  -DARMV7:BOOL=ON \
%endif
%ifarch x86_64
  -DX86_64:BOOL=ON \
%endif
  -DBUILD_TESTING:BOOL=OFF \
  -DHEADLESS:BOOL=OFF \
%if %{with qt}
  -DUSING_QT_UI:BOOL=ON \
%endif
%{nil}

%cmake_build


%install

mkdir -p %{buildroot}%{_bindir}
%if %{with qt}
  install -pm0755 %{_vpath_builddir}/PPSSPPQt %{buildroot}%{_bindir}/%{name}
%else
  install -pm0755 %{_vpath_builddir}/PPSSPPSDL %{buildroot}%{_bindir}/%{name}
%endif

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r %{_vpath_builddir}/assets %{buildroot}%{_datadir}/%{name}/
rm -f %{buildroot}%{_datadir}/%{name}/assets/Roboto-Condensed.ttf
ln -sf ../../fonts/google-roboto/RobotoCondensed-Regular.ttf \
  %{buildroot}%{_datadir}/%{name}/assets/Roboto-Condensed.ttf

%if %{with qt}
  install -pm 644 Qt/languages/* %{buildroot}%{_datadir}/%{name}/assets/lang/
%endif

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --mode 0644 \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name}" \
  --set-key="StartupNotify" \
  --set-value="false" \
  --add-category="Game" \
  --add-category="Emulator" \
  --set-icon="%{name}" \
  --remove-key="Encoding" \
  --remove-key="Version" \
  --remove-key="X-Window-Icon" \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp -r icons/hicolor/* %{buildroot}%{_datadir}/icons/hicolor/

install -pm0644 icons/icon-512.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:10} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license LICENSE.TXT
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.xml


%files data
%doc README.md
%license LICENSE.TXT
%{_datadir}/%{name}/


%changelog
* Wed Aug 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-117.20210811git5de47c6
- Update

* Thu Jul 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-116.20210722git868f5f6
- Bump
- Remove lang submodules, now in mainline

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-115.20210712git11957dd
- Update

* Wed Jul 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-114.20210707git752fdc9
- Last snapshot

* Wed Jun 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-113.20210622git8e9b012
- Update

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-112.20210610git39f4790
- Bump

* Sat May 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-111.20210528gitecc2f62
- Bump

* Tue May 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-110.20210517gitbac74b4
- Last snapshot
- Remove CHD patch

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-109.20210512gite725edd
- Update

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-108.20210501git630f071
- Bump

* Sat Apr 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-107.20210424gitfd2ff87
- Update

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-106.20210419gitbbdb4f7
- Last snapshot

* Sun Apr 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-105.20210417git036efc2
- Bump
- Added libzstd to system libraries patch
- BR: libzstd

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-104.20210407git28065c1
- Update

* Wed Mar 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-103.20210323gita37ea1e
- Add experimental CHD support from SleepyMan

* Mon Mar 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-102.20210308git1cfaa9f
- Bump to fix custom textures crashes

* Fri Mar 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-101.20210305git71707b5
- Bump to remove revert

* Wed Mar 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.3-100.20210303gitbd87a76
- 1.11.3

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.2-100.20210228git0fb655a
- 1.11.2

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.11.1-100.20210211gitd1c4b86
- 1.11.1

* Sat Jan 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-118.20210130gitc84ddaa
- New snapshot

* Thu Jan 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-117.20210106git1ee7faa
- Bump

* Wed Dec 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-116.20201223gitb403853
- Update

* Tue Dec 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-115.20201214gitafaff2e
- New snapshot

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-114.20201125git6e2447d
- Bump

* Sun Nov 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-113.20201115gite1f56b1
- Update

* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-112.20201110git0510101
- Bump

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-111.20201030gitf3c05cb
- New snapshot

* Sat Oct 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-110.20201023git254c316
- Update

* Mon Oct 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-109.20201011git615e07f
- Bump

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-108.20201002git5c9b7bb
- New snapshot

* Sat Sep 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-107.20200919git7ed1ade
- Bump

* Tue Sep 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-106.20200914git68735b4
- New snapshot

* Mon Sep 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-105.20200907gitfcaef64
- Bump

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-104.20200905git5f1e3b2
- New snapshot

* Sat Aug 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-103.20200828gitcb3ed8f
- Bump
- BR: libxxhash

* Tue Aug 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-102.20200825git3574a35
- New snapshot

* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-101.20200805git937042b
- Bump
- BR: vulkan-headers

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-100.20200726git2af805d
- 1.10.3
- BR: miniupnc
- Enable system snappy for real

* Sun Jul 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.2-100.20200710gite667421
- 1.10.2

* Sat Jun 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.0-100.20200627git401df20
- 1.10.0

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.4-110.20200620gitb879b43
- New snapshot

* Sun Jun 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-109.20200607gitba06c87
- Bump

* Sun May 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-108.20200517gitfdd0b37
- New snapshot

* Wed Apr 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-107.20200421git134c9cf
- Bump

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-106.20200220git7d13d2e
- New snapshot

* Tue Feb 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-105.20200225git4602f89
- Bump

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-104.20200127gita9302c4
- New snapshot

* Sun Jan 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-103.20200105git6d8ddb7
- New snapshot

* Wed Dec 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-102.20191217git608d716
- New snapshot

* Mon Nov 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-101.20191118git1439421
- New snapshot

* Fri Oct 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.4-100.201901025git86de0a4
- New snapshot

* Fri Sep 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.9.2-100.20190927git9e7625c
- New snapshot

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-109.20190919git5a53570
- New snapshot

* Sun Sep 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-108.20190904git2439c3e
- New snapshot

* Sat Aug 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-107.20190824git0889013
- New snapshot

* Thu Aug 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-106.20190815git3356f94
- New snapshot

* Sat Jul 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-105.20190718git37a97e7
- New snapshot

* Thu Jun 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-104.20190618git53e8263
- New snapshot

* Sun Jun 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-103.20190602git816abce
- New snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-102.20190502git709c9dc
- New snapshot

* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-101.20190410git54e102c
- New snapshot

* Mon Mar 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.8.0-100.20190318gitb004852
- New snapshot

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7.5-4.20190302git7c7d276
- New snapshot

* Thu Feb 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.7.5-3.20190207gitbff58d0
- New snapshot

* Wed Jan 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.7.5-2.20190102git12e54ba
- New snapshot

* Mon Dec 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.5-1.20181210gitb282d83
- New snapshot
- Borrow some from RPMFusion
- Split data package

* Sat Nov 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.7.2-1.20181113git04708fe
- New snapshot
- USE_DISCORD=OFF

* Sat Oct 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-6.20181027gitcaa506b
- New snapshot

* Tue Oct 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-5.20181009git3189385
- New snapshot
- Provides ppsspp-data to not crash with RPMFusion package

* Sat Sep 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-4.20180907gitfd6c314
- New snapshot
- Dropped unneeded GL wrapper. Mesa 8.2 sets proper compat now.

* Fri Aug 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-3.20180515gitec5b0c2
- New snapshot

* Tue Jul 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-2.20180717git9be6b22
- New snapshot

* Fri Jun 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-1.20180620git06340bf
- New snapshot, 1.6.3

* Thu May 31 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.6.2-1.20180531gitcae79bf
- New snapshot, 1.6.2
- BR: glew
- BR: wayland-devel
- Set default OpenGL provider to libglvnd

* Sat May 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-5.20180510gitd10d57b
- New snapshot
- Appdata

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-4.20180414gitfb377b0
- New snapshot

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-3.20180406gitca0fb77
- New snapshot

* Sat Mar 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-2.20180308git0ed3dea
- New snapshot

* Wed Mar 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5.4-1.20180305git90dbd9a
- New snapshot
- BR: gcc-c++
- Remove obsolete scriptlets

* Sun Feb 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.4-14.20180211git4e5fb6e
- New snapshot
- USE_SYSTEM_LIBZIP

* Mon Jan 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.4-13.20180108git6224260
- New snapshot

* Thu Dec 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-12.20171214gitc55847a
- New snapshot

* Tue Nov 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-11.20171107gitca3be18
- New snapshot

* Fri Oct 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-10.20171013gited602a3
- New snapshot

* Sat Sep 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-9.20170825gitd36fdd6
- New snapshot

* Sun Aug 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-8.20170825git4938ab7
- New snapshot

* Thu Jul 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-7.20170727gitf8213a9
- New snapshot

* Sat Jul 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-6.20170613gita9f70d1
- New snapshot

* Fri Jun 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-5.20170613git3249d81
- New snapshot

* Tue Jun 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-4.20170613gitdd23588
- New snapshot
- R: google-roboto-condensed-fonts

* Fri May 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-3.20170519git66dc0ea
- New snapshot

* Sat Apr 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-2.20170422git2c6161c
- New snapshot

* Sun Apr 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1.20170402git4ea01be
- New snapshot

* Sat Mar 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-7.20170318git24cfb73
- New snapshot

* Mon Mar 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-6.20170306git9f17c7f
- New snapshot
- Fix forgotten GIT_VERSION

* Sun Mar 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-5.20170305git042d09a
- New snapshot
- Update GIT_VERSION again

* Fri Feb 03 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-4.20170203git48934df
- New snapshot
- Build proper ffmpeg static libraries instead using distributed binary ones
- Set ExclusiveArch if building with bundled ffmpeg

* Sat Jan 28 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-3.20170128git14d2bf5
- New snapshot
- Fix assets/gamecontrollerdb.txt loading
- Better GIT_VERSION display
- Wrapper to export Mesa GL to 3.3COMPAT

* Thu Dec 29 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.3-2.20161227gitad04f97
- Option to build with ugly bundled ffmpeg binary.
- https://github.com/hrydgard/ppsspp/issues/9026
- System png.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
