%global commit 85d0d3f79d01309829d2c052e0c6f8e301775e32
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220208
%global with_snapshot 0

%if %{with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Use external mupen64plus
# Disabled by default, as it not the same
%bcond_with mupen64plus

%global sanitize 0

%global md5_ver 1.4
%global oglft_ver 1.15

%global appname io.github.%{name}.%{name}

Name:           simple64
Version:        2022.10.3
Release:        1%{?gver}%{?dist}
Summary:        Custom plugins and Qt5 GUI for Mupen64Plus

# * mupen64plus - GPLv2 and LGPLv2
# * parallel-rdp-standalone - MIT
# * rsp-parallel - MIT or LGPLv3
# * simple64-audio-sdl2 - GPLv2
# * simple64-input-raphnetraw - GPLv2
License:        GPLv3 and (MIT or LGPLv3) and GPLv2
URL:            https://github.com/%{name}/%{name}

%if 0%{sanitize}
%if %{with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
%else
# Use Makefile to download
%if %{with_snapshot}
Source0:        %{name}-clean-%{shortcommit}.tar.xz
%else
Source0:        %{name}-clean-%{version}.tar.xz
%endif
%endif
Source1:        %{appname}.appdata.xml

Patch0:         0001-Set-system-directories.patch
Patch1:         0001-input-qt-disable-all-VRU-support.patch
Patch2:         0001-Load-versioned-library.patch

Patch900:       0001-Rename-library-and-directories.patch
Patch901:       0001-Versioned-shared-lib.patch
Patch902:       0001-Use-system-libraries.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  librsvg2-tools
BuildRequires:  ninja-build

BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6WebSockets)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
%if %{with mupen64plus}
BuildRequires:  mupen64plus-devel
Requires:       mupen64plus-libs
Requires:       %{name}-plugins%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Obsoletes:      m64p < %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       m64p%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mupen64plus-gui%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-gui%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{summary}.

This build do not have VRU support.


%if %{without mupen64plus}
%package libs
Summary:        %{summary}
BuildRequires:  minizip-compat-devel
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(SDL2_net)
Requires:       dejavu-sans-fonts
Requires:       %{name}-plugins%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(md5-deutsch) = %{md5_ver}
Provides:       bundled(oglft) = %{oglft_ver}

%description libs
The %{name}-libs package contains the dynamic libraries needed for %{name} and
plugins.
%endif

%package plugins
Summary:        %{summary}
BuildRequires:  pkgconfig(hidapi-hidraw)
BuildRequires:  pkgconfig(lightning)
BuildRequires:  vulkan-headers
Requires:       vulkan-loader%{?_isa}
Obsoletes:      %{name}-rsp-parallel < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-video-parallel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-audio-sdl2 = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-input-qt = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-input-raphnetraw  = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-rsp-parallel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-video-parallel = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins
The %{name}-plugins package contains default plugins for %{name}.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -N -p1
%autopatch -p1 -M 500

rm -f *.exe
%if %{with mupen64plus}
rm -rf mupen64plus-core
%else
%patch900 -p1
%patch901 -p1
%patch902 -p1
%endif
rm -rf parallel-rdp-standalone/vulkan-headers
rm -f %{name}-gui/discord/*.{dylib,so,dll}
rm -f %{name}-input-qt/vosk/*.{dylib,so,dll}

rm -rf mupen64plus-core/subprojects/{minizip,xxhash}

cp %{S:1} .

mkdir LICENSEdir READMEdir
for i in %{name}-{audio-sdl2,gui,input-{qt,raphnetraw}} parallel-{rdp-standalone,rsp} %{!?_with_mupen64plus:mupen64plus-core} ;do
  if [ -f $i/LICENSES ] ;then
    cp -p $i/LICENSES LICENSEdir/LICENSES.$i
  fi
  if [ -f $i/LICENSE ] ;then
    cp -p $i/LICENSE LICENSEdir/LICENSE.$i
  fi
  if [ -f $i/LICENSE.LESSER ] ;then
    cp -p $i/LICENSE.LESSER LICENSEdir/LICENSE.LESSER.$i
  fi
  if [ -f $i/LICENSE.MIT ] ;then
    cp -p $i/LICENSE.MIT LICENSEdir/LICENSE.MIT.$i
  fi
done

for i in %{name}-input-raphnetraw parallel-rdp-standalone %{!?_with_mupen64plus:mupen64plus-core} ;do
  if [ -f $i/README.md ] ;then
    cp -p $i/README.md READMEdir/README.$i.md
  fi
done

sed -e 's|_RPM_LIBDIR_|%{_libdir}|g' \
  -i %{name}-gui/{mainwindow,settingsdialog}.cpp

echo '#define GUI_VERSION "%{commit}"' > %{name}-gui/version.h

%if %{with mupen64plus}
sed \
  -e 's|../mupen64plus-core/src/api|%{_includedir}/mupen64plus|g' \
  -i parallel-{rdp-standalone,rsp}/CMakeLists.txt \
     %{name}-{audio-sdl2,input-{raphnetraw,qt}}

sed -e '/^#include "config.h"/d' -i %{name}-input-raphnetraw/src/plugin_front.c
%else
sed \
  -e 's|DNO_ASM|\0 -DSHAREDIR="${SHARE_INSTALL_PREFIX}/%{name}"|g' \
  -e 's|mupen64plus|%{name}|g' \
  -i mupen64plus-core/CMakeLists.txt
%endif

sed \
  -e 's|-march=x86-64-v3 ||g' \
  -i */CMakeLists.txt

sed -e 's|<lightning.h>|<lightning/lightning.h>|g' -i parallel-rsp/rsp_jit.hpp

cat > %{appname}.desktop <<EOF
[Desktop Entry]
Name=%{name}-gui
Exec=%{name}-gui
Terminal=false
Type=Application
Icon=%{appname}
Comment=A frontend for Mupen64Plus
Categories=Game;Emulator;Qt;
Keywords=Emulator;Nintendo64;Mupen64plus;%{name};
EOF

%build
build_list="$(echo %{?!_with_mupen64plus:mupen64plus-core} %{name}-gui %{name}-{audio-sdl2,input-{raphnetraw,qt}} parallel-{rdp-standalone,rsp})"
for i in $build_list ;do
pushd $i
%cmake \
  -G Ninja \
  -DPARALLEL_RSP_BAKED_LIGHTNING:BOOL=OFF \
  -DENABLE_IPO:BOOL=OFF \
  -DPARALLEL_RSP_DEBUG_JIT:BOOL=OFF \
%{nil}
popd
done

for i in $build_list ;do
  pushd $i
    %cmake_build
  popd
done


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}-gui/%{__cmake_builddir}/%{name}-gui %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_libdir}/%{name}

%if %{without mupen64plus}
cp -a mupen64plus-core/%{__cmake_builddir}/lib%{name}.so.* %{buildroot}%{_libdir}/
chmod +x %{buildroot}%{_libdir}/*.so.*
%endif

for i in %{name}-audio-sdl2 %{name}-input-{raphnetraw,qt} ;do
  install -pm0755 $i/%{__cmake_builddir}/$i.so %{buildroot}%{_libdir}/%{name}/
done

install -pm0755 parallel-rdp-standalone/%{__cmake_builddir}/%{name}-video-parallel.so %{buildroot}%{_libdir}/%{name}/
install -pm0755 parallel-rsp/%{__cmake_builddir}/%{name}-rsp-parallel.so %{buildroot}%{_libdir}/%{name}/

%if %{without mupen64plus}
mkdir -p %{buildroot}%{_datadir}/%{name}
install -pm0644 mupen64plus-core/data/mupencheat.txt %{buildroot}%{_datadir}/%{name}/
install -pm0644 mupen64plus-core/data/mupen64plus.ini %{buildroot}%{_datadir}/%{name}/%{name}.ini
ln -sf ../fonts/dejavu-sans-fonts/DejaVuSans.ttf %{buildroot}%{_datadir}/%{name}/font.ttf
%endif

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm0644 %{name}-gui/icons/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appname}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert %{name}-gui/icons/%{name}.svg -h ${res} -w ${res} \
    -o ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{appname}.appdata.xml %{buildroot}%{_metainfodir}/%{appname}.appdata.xml


%files
%license LICENSE LICENSEdir/*
%doc %{name}-gui/README.md READMEdir/*
%{_bindir}/%{name}-gui
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/%{appname}.appdata.xml
%if %{without mupen64plus}
%{_datadir}/%{name}/
%endif

%if %{without mupen64plus}
%files libs
%license LICENSE
%{_libdir}/lib%{name}.so.*
%endif

%files plugins
%license LICENSE
%{_libdir}/%{name}/*.so


%changelog
* Fri Oct 07 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.10.3-1
- 2022.10.3
- All cmake now
- make->ninja-build

* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.09.6-1
- 2022.09.6
- Rename
- Use internal renamed mupen64plus library by default

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
