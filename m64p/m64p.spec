%global commit 094325c6cc30f80a510a47652860bbbbe3c1212b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210606
%global with_snapshot 0

Name:           m64p
Version:        2021.6.6
Release:        1%{?dist}
Summary:        Custom plugins and Qt5 GUI for Mupen64Plus

# * mupen64plus-audio-sdl2 - GPLv2
# * mupen64plus-input-raphnetraw - GPLv2
# * parallel-rdp-standalone - MIT
# * parallel-rsp - MIT or LGPLv3
License:        GPLv3 and (MIT or LGPLv3) and GPLv2
URL:            https://github.com/loganmc10/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

Patch0:         0001-Set-system-directories.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  icoutils
BuildRequires:  make
BuildRequires:  mupen64plus-devel
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5WebSockets)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers

Requires:       hicolor-icon-theme
Requires:       mupen64plus
Requires:       vulkan-loader%{?_isa}

%description
%{summary}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

rm -f *.exe
rm -rf mupen64plus-core
rm -rf parallel-rdp-standalone/vulkan-headers
rm -f mupen64plus-gui/discord/*.{dylib,so,dll}

mkdir LICENSEdir READMEdir
for i in mupen64plus-{audio-sdl2,gui,input-{qt,raphnetraw}} parallel-{rdp-standalone,rsp} ;do
  if [ -f $i/LICENSES ] ;then
    mkdir -p LICENSEdir/$i
    cp -p $i/LICENSES LICENSEdir/$i/
  fi
  if [ -f $i/LICENSE ] ;then
    mkdir -p LICENSEdir/$i
    cp -p $i/LICENSE LICENSEdir/$i/
  fi
done

for i in mupen64plus-input-raphnetraw parallel-rdp-standalone ;do
  if [ -f $i/README.md ] ;then
    mkdir -p READMEdir/$i
    cp -p $i/README.md READMEdir/$i/
  fi
done

sed -e 's|_RPM_LIBDIR_|%{_libdir}|g' -i mupen64plus-gui/mainwindow.cpp

echo '#define GUI_VERSION "%{commit}"' > mupen64plus-gui/version.h

sed \
  -e 's|"../../mupen64plus-core/src/api"|%{_includedir}/mupen64plus|g' \
  -e 's|-L/usr/local/lib ||g' \
  -e '/-no-pie/d' \
  -i mupen64plus-*/mupen64plus-*.pro

sed \
  -e 's|../mupen64plus-core/src/api|%{_includedir}/mupen64plus|g' \
  -i parallel-{rdp-standalone,rsp}/CMakeLists.txt 

sed -e '/^#include "config.h"/d' -i mupen64plus-input-raphnetraw/src/plugin_front.c

cat > %{name}.desktop <<EOF
[Desktop Entry]
Name=m64p
Exec=mupen64plus-gui
Terminal=false
Type=Application
Icon=%{name}
Comment=A frontend for Mupen64Plus
Categories=Game;Emulator;Qt;
Keywords=Emulator;Nintendo64;Mupen64plus;
EOF

icotool -x mupen64plus-gui/mupen64plus.ico

cat > %{name}-env <<'EOF'
export OPTFLAGS="%{optflags}"
export LDFLAGS="$OPTFLAGS %{build_ldflags}"
export V=1
export LDCONFIG=/bin/true
export PREFIX=/usr
export LIBDIR=%{_libdir}
export INCDIR=%{_includedir}/%{name}
export SHAREDIR=%{_datadir}/%{name}
export MANDIR=%{_mandir}
export PIC=1
export PIE=1
EOF

%build
source ./%{name}-env

for i in mupen64plus-input-qt mupen64plus-gui ;do
  mkdir $i/build
  pushd $i/build
    %{qmake_qt5} ../$i.pro
  popd
done

for i in parallel-rdp-standalone parallel-rsp ;do
  pushd $i
    %cmake
  popd
done

for i in mupen64plus-audio-sdl2 mupen64plus-input-raphnetraw ;do
  pushd $i
    %make_build V=1 -C projects/unix all
  popd
done

for i in parallel-rdp-standalone parallel-rsp ;do
  pushd $i
    %cmake_build
  popd
done

for i in mupen64plus-input-qt mupen64plus-gui ;do
  pushd $i/build
    %make_build
  popd
done

%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 mupen64plus-gui/build/mupen64plus-gui %{buildroot}%{_bindir}/


mkdir -p %{buildroot}%{_libdir}/%{name}

for i in mupen64plus-audio-sdl2 mupen64plus-input-raphnetraw ;do
  install -pm0755 $i/projects/unix/$i.so %{buildroot}%{_libdir}/%{name}/
done

install -pm0755 mupen64plus-input-qt/build/libmupen64plus-input-qt.so \
  %{buildroot}%{_libdir}/%{name}/mupen64plus-input-qt.so

install -pm0755 parallel-rdp-standalone/%{__cmake_builddir}/mupen64plus-video-parallel.so \
  %{buildroot}%{_libdir}/%{name}/
install -pm0755 parallel-rsp/%{__cmake_builddir}/mupen64plus-rsp-parallel.so \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

for res in 16 24 32 48 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 mupen64plus_*_${res}x${res}x32.png \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license LICENSE LICENSEdir/*
%doc mupen64plus-gui/README.md READMEdir/*
%{_bindir}/mupen64plus-gui
%{_libdir}/%{name}/*.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.6.6-1
- Initial spec
