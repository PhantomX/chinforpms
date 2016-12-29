%global gitcommitid ad04f97acbdab0aa06156cc0fa53b0bf92425222
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global use_git 1

%if 0%{?use_git}
%global gitcommitid1 5f474b1fb9c0798958086e3d5a370288fc0ee751
%global shortcommit1 %(c=%{gitcommitid1}; echo ${c:0:7})
%global srcname1 %{name}-lang


%global gitcommitid2 309a15145a1f04306dcdd2214ef9b333b3fde755
%global shortcommit2 %(c=%{gitcommitid2}; echo ${c:0:7})
%global srcname2 armips

%global gitcommitid3 b7f5a22753c81d834ab5133d655f1fd525280765
%global shortcommit3 %(c=%{gitcommitid3}; echo ${c:0:7})
%global srcname3 tinyformat

%global gitcommitid4 224b1f733b9c5fad21500c16b025da024759fe40
%global shortcommit4 %(c=%{gitcommitid4}; echo ${c:0:7})
%global srcname4 glslang
%endif

%if 0%{?use_git}
%global gver .git%{shortcommit}
%endif

%undefine _hardened_build

Name:           ppsspp
Version:        1.3
Release:        1%{?gver}%{?dist}
Summary:        A PSP emulator

License:        PSPSDK
URL:            http://www.ppsspp.org/
%if 0%{?use_git}
Source0:        https://github.com/hrydgard/%{name}/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
Source1:        https://github.com/hrydgard/ppsspp-lang/archive/%{gitcommitid1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/Kingcom/armips/archive/%{gitcommitid2}.tar.gz#/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/Kingcom/tinyformat/archive/%{gitcommitid3}.tar.gz#/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/hrydgard/glslang/archive/%{gitcommitid4}.tar.gz#/%{srcname4}-%{shortcommit4}.tar.gz
%else
Source0:        https://github.com/hrydgard/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

Patch0:         %{name}-noupdate.patch

BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
#BuildRequires: pkgconfig(libpng)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(sdl2)
Requires:       snappy-devel
BuildRequires:  pkgconfig(zlib)
Provides:       bundled(libpng) = 1.7.0
Requires:       hicolor-icon-theme
Requires(post): desktop-file-utils


%description
%{summary}.

%prep
%if 0%{?use_git}
%autosetup -n %{name}-%{gitcommitid} -p0
tar -xf %{SOURCE1} -C assets/lang --strip-components 1
tar -xf %{SOURCE2} -C ext/armips --strip-components 1
tar -xf %{SOURCE3} -C ext/armips/ext/tinyformat --strip-components 1
tar -xf %{SOURCE4} -C ext/glslang --strip-components 1
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

#rm -rf ext/native/ext/libpng
#sed -e 's|png17|png|g' \
#  -i CMakeLists.txt Core/Screenshot.cpp \
#     Core/TextureReplacer.cpp ext/native/image/png_load.cpp \
#     ext/native/tools/CMakeLists.txt
#sed -e "/PNG_PNG_INCLUDE_DIR/s,libpng/,$(pkg-config --variable=includedir libpng |sed 's|/usr/include/||g')/," \
#  -i CMakeLists.txt

%build

mkdir -p build
pushd build

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DUSE_SYSTEM_FFMPEG:BOOL=ON \

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
* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
