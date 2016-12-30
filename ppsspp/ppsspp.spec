%global gitcommitid ad04f97acbdab0aa06156cc0fa53b0bf92425222
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global use_git 1

# Enable system ffmpeg
%global sysffmpeg 0

%if 0%{?use_git}
%global gitcommitid1 5f474b1fb9c0798958086e3d5a370288fc0ee751
%global shortcommit1 %(c=%{gitcommitid1}; echo ${c:0:7})
%global srcname1 %{name}-lang

%global gitcommitid2 2f6023d14a09e6fc1babbb8b31231249719e9240
%global shortcommit2 %(c=%{gitcommitid2}; echo ${c:0:7})
%global srcname2 %{name}-ffmpeg

%global gitcommitid3 36bacb4cba27003c572e5bf7a9c4dfe3c9a8d40d
%global shortcommit3 %(c=%{gitcommitid3}; echo ${c:0:7})
%global srcname3 ffmpeg-gas-preprocessor

%global gitcommitid4 309a15145a1f04306dcdd2214ef9b333b3fde755
%global shortcommit4 %(c=%{gitcommitid4}; echo ${c:0:7})
%global srcname4 armips

%global gitcommitid5 b7f5a22753c81d834ab5133d655f1fd525280765
%global shortcommit5 %(c=%{gitcommitid5}; echo ${c:0:7})
%global srcname5 tinyformat

%global gitcommitid6 224b1f733b9c5fad21500c16b025da024759fe40
%global shortcommit6 %(c=%{gitcommitid6}; echo ${c:0:7})
%global srcname6 %{name}-glslang
%endif

%if 0%{?use_git}
%global gver .git%{shortcommit}
%endif

%global pngver %(pkg-config --variable=includedir libpng |sed 's|/usr/include/lib||g')

%undefine _hardened_build

Name:           ppsspp
Version:        1.3
Release:        2%{?gver}%{?dist}
Summary:        A PSP emulator

License:        PSPSDK
URL:            http://www.ppsspp.org/
%if 0%{?use_git}
Source0:        https://github.com/hrydgard/%{name}/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
Source1:        https://github.com/hrydgard/%{srcname1}/archive/%{gitcommitid1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
%if !0%{?sysffmpeg}
Source2:        https://github.com/hrydgard/%{srcname2}/archive/%{gitcommitid2}.tar.gz#/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/FFmpeg/gas-preprocessor/archive/%{gitcommitid3}.tar.gz#/%{srcname3}-%{shortcommit3}.tar.gz
%endif #{?sysffmpeg}
Source4:        https://github.com/Kingcom/%{srcname4}/archive/%{gitcommitid4}.tar.gz#/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/Kingcom/%{srcname5}/archive/%{gitcommitid5}.tar.gz#/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/hrydgard/glslang/archive/%{gitcommitid6}.tar.gz#/%{srcname6}-%{shortcommit6}.tar.gz
%else
Source0:        https://github.com/hrydgard/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif #{?use_git}

Patch0:         %{name}-noupdate.patch

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
%if 0%{?use_git}
%autosetup -n %{name}-%{gitcommitid} -p0
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

%if 0%{?use_git}
sed -i \
  -e "/GIT_VERSION/s|unknown|%{shortcommit}|g" \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} describe --always|echo \"%{shortcommit}\"|g" \
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
install -pm0755 build/PPSSPPSDL %{buildroot}%{_bindir}/%{name}

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
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/%{name}

%changelog
* Thu Dec 29 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.3-2.gitad04f97
- Option to build with ugly bundled binary ffmpeg.
- https://github.com/hrydgard/ppsspp/issues/9026
- System png.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
