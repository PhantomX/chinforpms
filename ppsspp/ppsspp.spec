%global commit fcaef648ec2f8972e7ff0916619ade9db47ebf37
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200907
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

%global commit1 d5a2a51942377820764604d9bb424fa9a879c4bd
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{name}-lang

%global commit2 55147e5f33f5ae4904f75ec082af809267122b94
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-ffmpeg

%global commit3 cbe88474ec196370161032a3863ec65050f70ba4
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 ffmpeg-gas-preprocessor

%global commit4 7885552b208493a6a0f21663770c446c3ba65576
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 armips

%global commit6 d0850f875ec392a130ccf00018dab458b546f27c
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{name}-glslang

%global commit7 685f86471e9d26b3eb7676695a2e2cefb4551ae9
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 SPIRV-Cross

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pngver %(pkg-config --variable=includedir libpng |sed 's|/usr/include/lib||g')

%undefine _hardened_build
%undefine _cmake_shared_libs

%global vc_url  https://github.com/hrydgard

Name:           ppsspp
Version:        1.10.3
Release:        105%{?gver}%{?dist}
Summary:        A PSP emulator
Epoch:          1

License:        BSD and GPLv2+
URL:            http://www.ppsspp.org/
%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{vc_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%if %{with ffmpeg}
%if !0%{?with_sysffmpeg}
Source2:        %{vc_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/FFmpeg/gas-preprocessor/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%endif
%endif
Source4:        https://github.com/Kingcom/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source6:        %{vc_url}/glslang/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/KhronosGroup/SPIRV-Cross/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source10:       %{name}.appdata.xml

Patch0:         %{name}-noupdate.patch
Patch1:         %{name}-nodiscord.patch
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
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxxhash) >= 0.8.0
BuildRequires:  pkgconfig(libzip)
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

tar -xf %{SOURCE1} -C assets/lang --strip-components 1
%if %{with ffmpeg}
%if !0%{?with_sysffmpeg}
tar -xf %{SOURCE2} -C ffmpeg --strip-components 1
tar -xf %{SOURCE3} -C ffmpeg/gas-preprocessor --strip-components 1
%endif
%endif
tar -xf %{SOURCE4} -C ext/armips --strip-components 1
tar -xf %{SOURCE6} -C ext/glslang --strip-components 1
tar -xf %{SOURCE7} -C ext/SPIRV-Cross --strip-components 1

rm -rf ext/{glew,rapidjson,miniupnp,snappy,zlib}/*.{c,cpp,h}
rm -rf ext/vulkan
rm -f ext/xxhash.*

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

rm -rf ext/native/ext/libpng*
sed -e 's|png17|%{pngver}|g' \
  -i CMakeLists.txt Core/Screenshot.cpp \
     Core/Debugger/WebSocket/GPUBufferSubscriber.cpp \
     Core/TextureReplacer.cpp ext/native/image/png_load.cpp \
     ext/native/tools/CMakeLists.txt
sed -e "/PNG_PNG_INCLUDE_DIR/s|libpng/|lib%{pngver}/|" \
  -i CMakeLists.txt

rm -rf ext/glew/{GL,*.c}
rm -rf ext/native/ext/libzip

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
# https://github.com/hrydgard/ppsspp/issues/13312
%define _lto_cflags %{nil}

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
  -B %{__cmake_builddir} \
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
