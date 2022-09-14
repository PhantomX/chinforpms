%global commit 85d0d3f79d01309829d2c052e0c6f8e301775e32
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220208
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global sanitize 0

Name:           m64p
Version:        2022.08.6
Release:        1%{?gver}%{?dist}
Summary:        Custom plugins and Qt5 GUI for Mupen64Plus

# * mupen64plus-audio-sdl2 - GPLv2
# * mupen64plus-input-raphnetraw - GPLv2
License:        GPLv3 and (MIT or LGPLv3) and GPLv2
URL:            https://github.com/%{name}/%{name}

%if 0%{sanitize}
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
%else
# Use Makefile to download
%if 0%{?with_snapshot}
Source0:        %{name}-clean-%{shortcommit}.tar.xz
%else
Source0:        %{name}-clean-%{version}.tar.xz
%endif
%endif
Source1:        %{name}.appdata.xml

Patch0:         0001-Set-system-directories.patch
Patch1:         0001-input-qt-disable-all-VRU-support.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  librsvg2-tools
BuildRequires:  make
BuildRequires:  mupen64plus-devel
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6WebSockets)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  vulkan-headers

Requires:       hicolor-icon-theme
Requires:       mupen64plus
Requires:       mupen64plus-rsp-parallel%{?_isa}
Requires:       mupen64plus-video-parallel%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       mupen64plus-gui%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{summary}.

This build do not have VRU support.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

rm -f *.exe
rm -rf mupen64plus-core
rm -rf parallel-rdp-standalone
rm -rf parallel-rsp
rm -f mupen64plus-gui/discord/*.{dylib,so,dll}
rm -f mupen64plus-input-qt/vosk/*.{dylib,so,dll}

mkdir LICENSEdir READMEdir
for i in mupen64plus-{audio-sdl2,gui,input-{qt,raphnetraw}} ;do
  if [ -f $i/LICENSES ] ;then
    mkdir -p LICENSEdir/$i
    cp -p $i/LICENSES LICENSEdir/$i/
  fi
  if [ -f $i/LICENSE ] ;then
    mkdir -p LICENSEdir/$i
    cp -p $i/LICENSE LICENSEdir/$i/
  fi
done

for i in mupen64plus-input-raphnetraw ;do
  if [ -f $i/README.md ] ;then
    mkdir -p READMEdir/$i
    cp -p $i/README.md READMEdir/$i/
  fi
done

sed -e 's|_RPM_LIBDIR_|%{_libdir}|g' \
  -i mupen64plus-gui/{mainwindow,settingsdialog}.cpp

echo '#define GUI_VERSION "%{commit}"' > mupen64plus-gui/version.h

sed \
  -e 's|"../../mupen64plus-core/src/api"|%{_includedir}/mupen64plus|g' \
  -e 's|"../mupen64plus-core/src/api"|%{_includedir}/mupen64plus|g' \
  -e 's|-L/usr/local/lib ||g' \
  -e '/-no-pie/d' \
  -e '/^QMAKE_CXXFLAGS/d' \
  -e '/^QMAKE_CFLAGS/d' \
  -e '/^QMAKE_LFLAGS/d' \
  -i mupen64plus-*/mupen64plus-*.pro

sed -e '/^#include "config.h"/d' -i mupen64plus-input-raphnetraw/src/plugin_front.c

cat > mupen64plus-gui.desktop <<EOF
[Desktop Entry]
Name=mupen64plus-gui
Exec=mupen64plus-gui
Terminal=false
Type=Application
Icon=mupen64plus-gui
Comment=A frontend for Mupen64Plus
Categories=Game;Emulator;Qt;
Keywords=Emulator;Nintendo64;Mupen64plus;
EOF

cat > %{name}-env <<'EOF'
export OPTFLAGS="$CXXFLAGS"
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
%set_build_flags
export CXXFLAGS="$CXXFLAGS -fvisibility=hidden"
source ./%{name}-env

for i in mupen64plus-input-qt mupen64plus-gui ;do
  mkdir $i/build
  pushd $i/build
    %{qmake_qt6} ../$i.pro
  popd
done

for i in mupen64plus-audio-sdl2 mupen64plus-input-raphnetraw ;do
  pushd $i
    %make_build V=1 -C projects/unix all
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

ln -s ../mupen64plus/mupen64plus-rsp-parallel.so %{buildroot}%{_libdir}/%{name}/
ln -s ../mupen64plus/mupen64plus-video-parallel.so %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  mupen64plus-gui.desktop

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert mupen64plus-gui/mupen64plus.svg -h ${res} -w ${res} \
    -o ${dir}/mupen64plus-gui.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license LICENSE LICENSEdir/*
%doc mupen64plus-gui/README.md READMEdir/*
%{_bindir}/mupen64plus-gui
%{_libdir}/%{name}/*.so
%{_datadir}/applications/mupen64plus-gui.desktop
%{_datadir}/icons/hicolor/*/apps/mupen64plus-gui.*
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.08.6-1
- 2022.08.6
- Qt6

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.2.7-2.20220208git85d0d3f
- Fix for package_note_file

* Mon Feb 14 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.2.7-1.20220208git85d0d3f
- 2022.2.7
- Require external parallel packages

* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.8.9-1
- 2021.8.9

* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.6.6-1
- Initial spec
