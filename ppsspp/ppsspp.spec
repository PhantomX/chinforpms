%global commit 14d2bf5989331f776a826603cb8fdb78c5da55da
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20170128
%global use_snapshot 1

# Enable system ffmpeg
%global sysffmpeg 0

%if 0%{?use_snapshot}
%global commit1 c440eda0f3c4dfc9940b1643ce4e292ebc0c618f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{name}-lang

%global commit2 2f6023d14a09e6fc1babbb8b31231249719e9240
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-ffmpeg

%global commit3 36bacb4cba27003c572e5bf7a9c4dfe3c9a8d40d
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 ffmpeg-gas-preprocessor

%global commit4 309a15145a1f04306dcdd2214ef9b333b3fde755
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 armips

%global commit5 b7f5a22753c81d834ab5133d655f1fd525280765
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 tinyformat

%global commit6 807a0d9e2f4e176f75d62ac3c179c81800ec2608
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{name}-glslang
%endif

%if 0%{?use_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pngver %(pkg-config --variable=includedir libpng |sed 's|/usr/include/lib||g')

%undefine _hardened_build

Name:           ppsspp
Version:        1.3
Release:        3%{?gver}%{?dist}
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
%else
Source0:        https://github.com/hrydgard/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif #{?use_snapshot}

Patch0:         %{name}-noupdate.patch
# Fix assets/gamecontrollerdb.txt loading
Patch1:         %{name}-datadir.patch

BuildRequires:  desktop-file-utils
%if 0%{?sysffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
%else
Provides:       bundled(ffmpeg) = 3.0.2
%endif #{?sysffmpeg}
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  snappy-devel
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme
Requires(post): desktop-file-utils


%description
%{summary}.

%prep
%if 0%{?use_snapshot}
%autosetup -n %{name}-%{commit} -p0
tar -xf %{SOURCE1} -C assets/lang --strip-components 1
%if !0%{?sysffmpeg}
tar -xf %{SOURCE2} -C ffmpeg --strip-components 1
tar -xf %{SOURCE3} -C ffmpeg/gas-preprocessor --strip-components 1
%endif #{?sysffmpeg}
tar -xf %{SOURCE4} -C ext/armips --strip-components 1
tar -xf %{SOURCE5} -C ext/armips/ext/tinyformat --strip-components 1
tar -xf %{SOURCE6} -C ext/glslang --strip-components 1
%else
%autosetup -n %{name}-%{version} -p0
%endif

%if 0%{?use_snapshot}
sed -i \
  -e "/GIT_VERSION/s|unknown|%{version}.%{shortcommit}|g" \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} describe --always|echo \"%{version}.%{shortcommit}\"|g" \
  git-version.cmake
%endif

cp Qt/PPSSPP.desktop %{name}.desktop

sed -i -e '/_FLAGS_/s| -O3 | |g' CMakeLists.txt

%global pngver %(pkg-config --variable=includedir libpng |sed 's|/usr/include/lib||g')
rm -rf ext/native/ext/libpng
sed -e 's|png17|%{pngver}|g' \
  -i CMakeLists.txt Core/Screenshot.cpp \
     Core/TextureReplacer.cpp ext/native/image/png_load.cpp \
     ext/native/tools/CMakeLists.txt
sed -e "/PNG_PNG_INCLUDE_DIR/s|libpng/|lib%{pngver}/|" \
  -i CMakeLists.txt

cat > %{name}.wrapper <<'EOF'
#!/usr/bin/sh
MESA_GL_VERSION_OVERRIDE=3.3COMPAT
export MESA_GL_VERSION_OVERRIDE
exec ppsspp.bin "$@"
EOF

%build

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
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -pm0755 build/PPSSPPSDL %{buildroot}%{_bindir}/%{name}.bin
install -pm0755 %{name}.wrapper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r build/assets %{buildroot}%{_datadir}/%{name}/

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
update-desktop-database &> /dev/null || :
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
* Sat Jan 28 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-3.20170128git14d2bf5
- New snapshot
- Fix assets/gamecontrollerdb.txt loading
- Better GIT_VERSION display
- Wrapper to export MEsa GL to 3.3COMPAT

* Thu Dec 29 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.3-2.20161227gitad04f97
- Option to build with ugly bundled binary ffmpeg.
- https://github.com/hrydgard/ppsspp/issues/9026
- System png.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
