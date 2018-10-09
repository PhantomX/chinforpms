%global commit fd6c3145d5379a74fa7945f10855eb03e07a573a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180907
%global with_snapshot 1

# Enable system ffmpeg
%global with_sysffmpeg 0
%if !0%{?with_sysffmpeg}
%global bundleffmpegver 3.0.2
%endif

%global commit1 1153a4293006db9d2a6e701df72df843b98234b5
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{name}-lang

%global commit2 a2e98d7ba4c7c5cac08608732c3058cb46e3e0ef
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-ffmpeg

%global commit3 36bacb4cba27003c572e5bf7a9c4dfe3c9a8d40d
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 ffmpeg-gas-preprocessor

%global commit4 9efe3367284d2d1eeb14fc302a2c12c36e3e255e
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 armips

%global commit6 29619b2312f7bc862221749f3f4d37c3e6a0dee2
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{name}-glslang

%global commit7 be7425ef70231ab82930331959ab487d605d0482
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 SPIRV-Cross

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pngver %(pkg-config --variable=includedir libpng |sed 's|/usr/include/lib||g')

%undefine _hardened_build

Name:           ppsspp
Version:        1.6.3
Release:        4%{?gver}%{?dist}
Summary:        A PSP emulator
Epoch:          1

License:        GPLv2+
URL:            http://www.ppsspp.org/
%if 0%{?with_snapshot}
Source0:        https://github.com/hrydgard/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/hrydgard/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif #{?with_snapshot}
Source1:        https://github.com/hrydgard/%{srcname1}/archive/%{commit1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
%if !0%{?with_sysffmpeg}
Source2:        https://github.com/hrydgard/%{srcname2}/archive/%{commit2}.tar.gz#/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/FFmpeg/gas-preprocessor/archive/%{commit3}.tar.gz#/%{srcname3}-%{shortcommit3}.tar.gz
%endif #{?with_sysffmpeg}
Source4:        https://github.com/Kingcom/%{srcname4}/archive/%{commit4}.tar.gz#/%{srcname4}-%{shortcommit4}.tar.gz
Source6:        https://github.com/hrydgard/glslang/archive/%{commit6}.tar.gz#/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/KhronosGroup/SPIRV-Cross/archive/%{commit7}.tar.gz#/%{srcname7}-%{shortcommit7}.tar.gz
Source10:       %{name}.appdata.xml

Patch0:         %{name}-noupdate.patch
Patch1:         %{name}-nodiscord.patch

%if !0%{?with_sysffmpeg}
ExclusiveArch:  %{ix86} x86_64 %{arm} %{mips32}
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
%if 0%{?with_sysffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
%else
Provides:       bundled(ffmpeg) = %{bundleffmpegver}
%endif #{?with_sysffmpeg}
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  snappy-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme
Requires:       google-roboto-condensed-fonts

Provides:       ppsspp-data.noarch = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      ppsspp-data.noarch < %{?epoch:%{epoch}:}%{version}-%{release}


%description
PPSSPP is a PSP emulator written in C++. It translates PSP CPU instructions
directly into optimized x86, x64, ARM or ARM64 machine code, using JIT
recompilers (dynarecs).

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p0
%else
%autosetup -n %{name}-%{version} -p0
%endif

tar -xf %{SOURCE1} -C assets/lang --strip-components 1
%if !0%{?with_sysffmpeg}
tar -xf %{SOURCE2} -C ffmpeg --strip-components 1
tar -xf %{SOURCE3} -C ffmpeg/gas-preprocessor --strip-components 1
%endif #{?with_sysffmpeg}
tar -xf %{SOURCE4} -C ext/armips --strip-components 1
tar -xf %{SOURCE6} -C ext/glslang --strip-components 1
tar -xf %{SOURCE7} -C ext/SPIRV-Cross --strip-components 1

find ext Core -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" -o -name "*.y" \) -exec chmod -x {} ';'

%if 0%{?with_snapshot}
sed -i \
  -e "/GIT_VERSION/s|unknown|%{version}-%{release}|g" \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} describe --always|echo \"%{version}-%{release}\"|g" \
  git-version.cmake
%endif

cp Qt/PPSSPP.desktop %{name}.desktop

sed -i -e '/_FLAGS_/s| -O3 | |g' CMakeLists.txt

rm -rf ext/native/ext/libpng
sed -e 's|png17|%{pngver}|g' \
  -i CMakeLists.txt Core/Screenshot.cpp \
     Core/Debugger/WebSocket/GPUBufferSubscriber.cpp \
     Core/TextureReplacer.cpp ext/native/image/png_load.cpp \
     ext/native/tools/CMakeLists.txt
sed -e "/PNG_PNG_INCLUDE_DIR/s|libpng/|lib%{pngver}/|" \
  -i CMakeLists.txt

rm -rf ext/glew/{GL,*.c}
rm -rf ext/native/ext/libzip

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

popd
%endif


%build

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
%make_build V=1
make install
popd
%endif

mkdir -p build
pushd build

%cmake .. \
  -DOpenGL_GL_PREFERENCE=GLVND \
%if 0%{?with_sysffmpeg}
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
%endif #{?with_sysffmpeg}
  -DUSE_SYSTEM_LIBZIP:BOOL=ON \
  -DUSE_WAYLAND_WSI:BOOL=ON \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON

%make_build

popd


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 build/PPSSPPSDL %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r build/assets %{buildroot}%{_datadir}/%{name}/
rm -f %{buildroot}%{_datadir}/%{name}/assets/Roboto-Condensed.ttf
ln -sf ../../fonts/google-roboto/RobotoCondensed-Regular.ttf \
  %{buildroot}%{_datadir}/%{name}/assets/Roboto-Condensed.ttf

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
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/assets
%{_datadir}/%{name}/assets/*.ini
%{_datadir}/%{name}/assets/*.png
%{_datadir}/%{name}/assets/*.ttf
%{_datadir}/%{name}/assets/*.txt
%{_datadir}/%{name}/assets/*.zim
%dir %{_datadir}/%{name}/assets/flash0
%dir %{_datadir}/%{name}/assets/flash0/font
%{_datadir}/%{name}/assets/flash0/font/*
%dir %{_datadir}/%{name}/assets/lang
%{_datadir}/%{name}/assets/lang/*
%dir %{_datadir}/%{name}/assets/shaders
%{_datadir}/%{name}/assets/shaders/*
%{_metainfodir}/*.xml


%changelog
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
