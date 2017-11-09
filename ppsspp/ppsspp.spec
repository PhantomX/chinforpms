%global commit ca3be1877ecae3e08a9016c83d57529df8f66c75
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20171108
%global use_snapshot 1

# Enable system ffmpeg
%global sysffmpeg 0
%if !0%{?sysffmpeg}
%global bundleffmpegver 3.0.2
%endif

%if 0%{?use_snapshot}
%global commit1 4fddbc9d3032113bdfed5186de73545e19340b4f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{name}-lang

%global commit2 a2e98d7ba4c7c5cac08608732c3058cb46e3e0ef
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-ffmpeg

%global commit3 36bacb4cba27003c572e5bf7a9c4dfe3c9a8d40d
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 ffmpeg-gas-preprocessor

%global commit4 770365d44df35d6e675c58bb2a774ca412278ef5
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 armips

%global commit5 b7f5a22753c81d834ab5133d655f1fd525280765
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 tinyformat

%global commit6 136b1e2d5d90284fd7bdd77ed605c70a8d31c8c4
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{name}-glslang

%global commit7 90966d50f57608587bafd95b4e345b02b814754a
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 SPIRV-Cross
%endif

%if 0%{?use_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pngver %(pkg-config --variable=includedir libpng |sed 's|/usr/include/lib||g')

%undefine _hardened_build

Name:           ppsspp
Version:        1.4
Release:        11%{?gver}%{?dist}
Summary:        A PSP emulator

License:        PSPSDK
URL:            http://www.ppsspp.org/
%if 0%{?use_snapshot}
Source0:        https://github.com/hrydgard/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
Source1:        https://github.com/hrydgard/%{srcname1}/archive/%{commit1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
%if !0%{?sysffmpeg}
Source2:        https://github.com/hrydgard/%{srcname2}/archive/%{commit2}.tar.gz#/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/FFmpeg/gas-preprocessor/archive/%{commit3}.tar.gz#/%{srcname3}-%{shortcommit3}.tar.gz
%endif #{?sysffmpeg}
Source4:        https://github.com/Kingcom/%{srcname4}/archive/%{commit4}.tar.gz#/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/Kingcom/%{srcname5}/archive/%{commit5}.tar.gz#/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/hrydgard/glslang/archive/%{commit6}.tar.gz#/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/KhronosGroup/SPIRV-Cross/archive/%{commit7}.tar.gz#/%{srcname7}-%{shortcommit7}.tar.gz
%else
Source0:        https://github.com/hrydgard/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif #{?use_snapshot}

Patch0:         %{name}-noupdate.patch

%if !0%{?sysffmpeg}
ExclusiveArch:  %{ix86} x86_64 %{arm} %{mips32}
%endif

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
%if 0%{?sysffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
%else
Provides:       bundled(ffmpeg) = %{bundleffmpegver}
%endif #{?sysffmpeg}
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  snappy-devel
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme
Requires:       google-roboto-condensed-fonts


%description
%{summary}.

%prep
%autosetup -n %{name}-%{?use_snapshot:%{commit}}%{!?use_snapshot:%{version}} -p0
%if 0%{?use_snapshot}
tar -xf %{SOURCE1} -C assets/lang --strip-components 1
%if !0%{?sysffmpeg}
tar -xf %{SOURCE2} -C ffmpeg --strip-components 1
tar -xf %{SOURCE3} -C ffmpeg/gas-preprocessor --strip-components 1
%endif #{?sysffmpeg}
tar -xf %{SOURCE4} -C ext/armips --strip-components 1
tar -xf %{SOURCE5} -C ext/armips/ext/tinyformat --strip-components 1
tar -xf %{SOURCE6} -C ext/glslang --strip-components 1
tar -xf %{SOURCE7} -C ext/SPIRV-Cross --strip-components 1
%endif

%if 0%{?use_snapshot}
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
     Core/TextureReplacer.cpp ext/native/image/png_load.cpp \
     ext/native/tools/CMakeLists.txt
sed -e "/PNG_PNG_INCLUDE_DIR/s|libpng/|lib%{pngver}/|" \
  -i CMakeLists.txt

%if !0%{?sysffmpeg}
pushd ffmpeg
sed \
  -e '/^ARCH=/s|=.*|=%{_target_cpu}|g' \
  -e '/extra-cflags/s|-O3|%{optflags}|g' \
  -e 's|disable-everything|\0 --disable-debug --disable-stripping|g' \
  -e '/make install/d' \
  -i linux_*.sh

rm -rf linux/*/include
rm -rf linux/*/lib

popd
%endif

cat > %{name}.wrapper <<'EOF'
#!/usr/bin/sh
MESA_GL_VERSION_OVERRIDE=4.3COMPAT
export MESA_GL_VERSION_OVERRIDE
exec /usr/bin/ppsspp.bin "$@"
EOF

%build

%if !0%{?sysffmpeg}
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
%if 0%{?sysffmpeg}
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \
%endif #{?sysffmpeg}
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON

%make_build

popd


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 build/PPSSPPSDL %{buildroot}%{_bindir}/%{name}.bin
install -pm0755 %{name}.wrapper %{buildroot}%{_bindir}/%{name}

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

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE.TXT
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
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


%changelog
* Wed Nov 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-11.20171107gitca3be18
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
- Option to build with ugly bundled binary ffmpeg.
- https://github.com/hrydgard/ppsspp/issues/9026
- System png.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
