%global commit 170ae3477c5b69975540aa382ac9ce3442d5c40e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20201010
%global with_snapshot 1

%undefine _hardened_build
%undefine _cmake_shared_libs

# Enable system libchdr (disables 7z archive loading when lzmasdk is disabled)
%global with_libchdr 1
# Enable system lzma-sdk
%global with_lzmasdk 1
# Enable system spirv (broken)
%global with_spirv 0
# Build with x11 instead SDL
%global with_x11 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           flycast
Version:        7
Release:        23%{?gver}%{?dist}
Summary:        Sega Dreamcast emulator

License:        GPLv2 and BSD
URL:            https://github.com/flyinghead/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/r%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

Patch1:         0001-Use-system-libs.patch
Patch2:         0001-Change-configdir-name.patch
Patch3:         0001-Save-logfile-to-writable_data_path.patch

BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(alsa)
%if !0%{?with_libchdr}
BuildRequires:  pkgconfig(flac)
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glm)
%if 0%{?with_spirv}
BuildRequires:  pkgconfig(glslang)
%endif
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(libzip)
%if 0%{?with_lzmasdk}
BuildRequires:  pkgconfig(lzmasdk-c)
%endif
%if 0%{?with_x11}
BuildRequires:  pkgconfig(x11)
%else
BuildRequires:  pkgconfig(sdl2)
%endif
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python3-devel
Requires:       hicolor-icon-theme
Requires:       vulkan-loader%{?_isa}


%description
%{name} is a multi-platform Sega Dreamcast emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup %{name}-r%{version} -p1
%endif

rm -rf core/deps/{flac,glm,libzip,SDL2-*,xxHash,zlib}

%if 0%{?with_libchdr}
rm -rf core/deps/{chdr,crypto}
%endif
%if 0%{?with_lzmasdk}
rm -rf core/deps/lzma
%endif
%if 0%{?with_spirv}
rm -rf core/deps/glslang
%endif

find . -type f \( -name "*.cpp" -o -name "*.h" \) -exec chmod -x {} ';'

pushd shell/linux

rename reicast %{name} * man/* tools/*

# Rebranding
sed -e 's|reicast|%{name}|g' \
  -i Makefile *.desktop man/*.1 tools/*.py

sed -e 's|REICAST|FLYCAST|g' -i man/*.1
sed -e 's|Reicast|Flycast|g' -i *.desktop tools/*.py

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tools/%{name}-joyconfig.py

popd

sed \
  -e 's|@GIT_VERSION@|%{version}-%{release}|g' \
  -i core/version.h*

sed \
  -e 's|AO_FOUND|AO_FOUND_DISABLED|g' \
  -e 's|${GIT_EXECUTABLE} describe --tags --always|echo "%{version}-%{release}"|g' \
  -i CMakeLists.txt

%if 0%{?with_snapshot}
  sed \
    -e 's|${GIT_EXECUTABLE} rev-parse --short HEAD|echo "%{shortcommit}"|g' \
    -i CMakeLists.txt
  sed -e 's|@GIT_HASH@|%{shortcommit}|g' -i core/version.h.in
%endif


%build
# Disable LTO. Crash.
%define _lto_cflags %{nil}

export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now -Wl,--sort-common"
EXTRA_CFLAGS="-D NDEBUG -frename-registers -ftree-vectorize"
export CFLAGS="%{build_cflags} ${EXTRA_CFLAGS}"
export CXXFLAGS="%{build_cxxflags} ${EXTRA_CFLAGS}"

%cmake \
  -GNinja \
%if 0%{?with_x11}
  -DSDL2_FOUND:BOOL=OFF \
%endif
%if 0%{?with_libchdr}
  -DUSE_SYSTEM_CHDR:BOOL=ON \
%endif
%if 0%{?with_lzmasdk}
  -DUSE_SYSTEM_LZMA:BOOL=ON \
%endif
%if 0%{?with_spirv}
  -DUSE_SYSTEM_SPIRV:BOOL=ON \
%endif \
  -DCMAKE_BUILD_TYPE:STRING=Release \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/%{name} %{buildroot}%{_bindir}/
install -pm755 shell/linux/tools/%{name}-joyconfig.py %{buildroot}%{_bindir}/%{name}-joyconfig

mkdir -p %{buildroot}%{_datadir}/%{name}/mappings
for mapping in gcwz generic pandora xboxdrv xpad ;do
  install -pm0644 shell/linux/mappings/controller_$mapping.cfg %{buildroot}%{_datadir}/%{name}/mappings/
done
install -pm0644 shell/linux/mappings/keyboard.cfg %{buildroot}%{_datadir}/%{name}/mappings/

mkdir -p %{buildroot}%{_mandir}/man1
install -m644 shell/linux/man/%{name}*.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  shell/linux/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -pm0644 shell/linux/%{name}.png %{buildroot}%{_datadir}/pixmaps/

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{buildroot}%{_datadir}/pixmaps/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-joyconfig
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_metainfodir}/*.xml


%changelog
* Sun Oct 11 2020 Phantom X <megaphantomx at hotmail dot com> - 7-23.20201010git170ae34
- Bump

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 7-22.20200901git734514c
- New snapshot

* Sat Aug 08 2020 Phantom X <megaphantomx at hotmail dot com> - 7-21.20200731git125c1ff
- Rebuild with system lzmasdk

* Fri Aug 07 2020 Phantom X <megaphantomx at hotmail dot com> - 7-20.20200731git125c1ff
- Rebuilt with system libchdr

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 7-19.20200731git125c1ff
- Last snapshot

* Tue Jul 28 2020 Phantom X <megaphantomx at hotmail dot com> - 7-18.20200723gitdd102c8
- Add CFLAGS from old linux Makefile, this fix some crashes

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 7-17.20200723gitdd102c8
- cmake and SDL2

* Tue Jul 21 2020 Phantom X <megaphantomx at hotmail dot com> - 7-16.20200710git860425b
- New snapshot

* Sat Jul 11 2020 Phantom X <megaphantomx at hotmail dot com> - 7-15.20200710git1713124
- Bump

* Thu Jul 02 2020 Phantom X <megaphantomx at hotmail dot com> - 7-14.20200701git42cb880
- New snapshot

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 7-13.20200620git959b634
- Bump

* Sun Jun 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-12.20200606git1879090
- New snapshot

* Sat May 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-11.20200530git002a05f
- Bump

* Sun May 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-10.20200515gitdf97c42
- New snapshot

* Wed Apr 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-9.20200421git8b7fcc4
- Bump

* Wed Apr 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-8.20200408git786c8e7
- New snapshot
- Remove libpng BR

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-7.20200320git0c2e951
- Bump

* Sun Mar 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-6.20200314git1abfdaf
- New snapshot

* Mon Nov 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-5.20191110git8f86be3
- New snapshot

* Sun Nov 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-4.20191027gitb9970fc
- New snapshot

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-3.20190919gitb693d1c
- New snapshot

* Sun Sep 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-2.20190915git732e685
- New snapshot
- Enable pulseaudio support

* Thu Aug 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-1.20190815gitb2475c4
- Initial spec
