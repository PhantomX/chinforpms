%undefine _hardened_build
%undefine _cmake_shared_libs

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit c15f446ffc9120310a698faddec755a9a0e9ea29
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221031
%global with_snapshot 1

# Disable LTO. Crash.
%global _lto_cflags %{nil}

%global commit1 36c0c62815f9f6bf43c81a3977502cd3996302a0
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 LuaBridge

%global commit2 d2657e1267d2ce9399bcc6b9c5b01b465db057b1
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 mingw-breakpad

%global commit3 c896e2f920273bfee852da9cca2a356bc1c2031e
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 Vulkan-Headers

%global commit4 a6bfc237255a6bac1513f7c1ebde6d8aed6b5191
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 VulkanMemoryAllocator

%global commit5 10423ec659d301a0ff2daac8bbf38980abf27590
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 glslang

%global commit6 37afa119a904d81a3495e6ef9c03151feff56349
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 volk

# Enable system spirv (broken)
%global with_sysspirv 0
%global with_sysvulkan 0
# Build with x11 instead SDL
%global with_x11 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global imgui_ver 1.80
%global libelf_ver 1.0
%global nowide_ver 0.0.0
%global stb_ver 2.25

Name:           flycast
Version:        2.0
Release:        3%{?gver}%{?dist}
Summary:        Sega Dreamcast emulator

Epoch:          1

# ggpo - MIT
License:        GPLv2 and BSD
URL:            https://github.com/flyinghead/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/r%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        https://github.com/vinniefalco/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%if !%{?with_sysvulkan}
Source2:        https://github.com/flyinghead/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
%endif
Source3:        https://github.com/KhronosGroup/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
%if !%{?with_sysspirv}
Source5:        https://github.com/KhronosGroup/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%endif
Source6:        https://github.com/zeux/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz

Patch1:         0001-Use-system-libs.patch
Patch2:         0001-Use-system-SDL_GameControllerDB.patch
Patch3:         0001-Save-logfile-to-writable_data_path.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  libappstream-glib
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(gl)
BuildRequires:  cmake(glm)
%if 0%{?with_sysspirv}
BuildRequires:  pkgconfig(glslang)
%else
Provides:       bundled(glslang) = git~0%{shortcommit5}
%endif
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(miniupnpc)
BuildRequires:  pkgconfig(lzmasdk-c)
%if 0%{?with_x11}
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(x11)
%else
BuildRequires:  pkgconfig(sdl2)
%endif
BuildRequires:  pkgconfig(zlib)
%if 0%{?with_sysvulkan}
BuildRequires:  vulkan-headers >= 1.3.224.1
%endif
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb
Requires:       vulkan-loader%{?_isa} >= 1.3.224.1

Provides:       bundled(breakpad) = 0~git%{shortcommit2}
Provides:       bundled(chdpsr)
Provides:       bundled(ggpo)
Provides:       bundled(libelf) = %{libelf_ver}
Provides:       bundled(LuaBridge) = 0~git%{shortcommit1}
Provides:       bundled(nowide_ver) = %{nowide_ver}
Provides:       bundled(picotcp)
Provides:       bundled(stb) = %{stb_ver}
Provides:       bundled(vixl)
Provides:       bundled(volk) = 0~git%{shortcommit6}
Provides:       bundled(xbyak)


%description
%{name} is a multi-platform Sega Dreamcast emulator.


%prep
%autosetup -n %{name}-%{?gver:%{commit}}%{!?gver:r%{version}} -p1

rm -rf core/deps/{glm,libzip,lzma,miniupnpc,oboe,SDL2-*,xxHash,zlib}

pushd core/deps
tar -xf %{S:1} -C luabridge/ --strip-components 1
tar -xf %{S:2} -C breakpad/ --strip-components 1
%if !0%{?with_sysvulkan}
tar -xf %{S:3} -C Vulkan-Headers/ --strip-components 1
sed -e '/vulkan_INCLUDE_DIRS/s|vulkan.h|vulkan.h_disabled|g' -i ../../CMakeLists.txt
%endif
tar -xf %{S:4} -C VulkanMemoryAllocator/ --strip-components 1
%if !0%{?with_sysspirv}
tar -xf %{S:5} -C glslang/ --strip-components 1
cp -p glslang/LICENSE.txt LICENSE.glslang
%endif
tar -xf %{S:6} -C volk/ --strip-components 1

cp -p breakpad/LICENSE LICENSE.breakpad
cp -p nowide/COPYING COPYING.nowide
cp -p picotcp/COPYING COPYING.picotcp
cp -p volk/LICENSE.md LICENSE.volk.md
cp -p xbyak/COPYRIGHT COPYRIGHT.xbyak
popd

find . -type f \( -name '*.c*' -o -name '*.h*' \) -exec chmod -x {} ';'

pushd core/deps/breakpad
sed -e '/" -Werror"/d' -i configure.ac
autoreconf -if
popd

pushd shell/linux

# Rebranding
sed -e 's|reicast|%{name}|g' \
  -i man/*.1

popd

sed \
  -e 's|@GIT_VERSION@|%{version}-%{release}|g' \
  -i core/version.h*

sed \
  -e 's|LINK_FLAGS_RELEASE -s||g' \
  -e 's|IMPORTED_TARGET ao|IMPORTED_TARGET ao_DISABLED|g' \
  -e 's|${GIT_EXECUTABLE} describe --tags --always|echo "%{version}-%{release}"|g' \
  -i CMakeLists.txt

%if 0%{?with_snapshot}
  sed \
    -e 's|${GIT_EXECUTABLE} rev-parse --short HEAD|echo "%{shortcommit}"|g' \
    -i CMakeLists.txt
  sed -e 's|@GIT_HASH@|%{shortcommit}|g' -i core/version.h.in
%endif

sed -e 's|_RPM_GCDBDIR_|%{_datadir}/SDL_GameControllerDB|g' -i core/sdl/sdl.cpp


%build
%set_build_flags
export LDFLAGS+=" -Wl,--sort-common"
EXTRA_CFLAGS="-D NDEBUG -frename-registers -ftree-vectorize -fno-operator-names"
export CFLAGS+=" ${EXTRA_CFLAGS}"
export CXXFLAGS+=" ${EXTRA_CFLAGS}"

%cmake \
  -GNinja \
%if 0%{?with_x11}
  -DSDL2_FOUND:BOOL=OFF \
%endif
  -DUSE_HOST_CHDR:BOOL=ON \
  -DUSE_HOST_LZMA:BOOL=ON \
%if 0%{?with_sysspirv}
  -DUSE_HOST_SPIRV:BOOL=ON \
%endif
  -DCMAKE_BUILD_TYPE:STRING=Release \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/mappings
for mapping in generic pandora xboxdrv xpad ;do
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
install -pm 0644 shell/linux/org.flycast.Flycast.metainfo.xml %{buildroot}%{_metainfodir}/

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.flycast.Flycast.metainfo.xml


%files
%license LICENSE core/deps/{COPYING,COPYRIGHT,LICENSE}.*
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_metainfodir}/*.xml


%changelog
* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-20.20220715git76bf574
- Bump

* Wed Jun 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-19.20220627git6a5db32
- Update

* Tue Jun 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-18.20220620git7485252
- Bump and lzma-sdk rebuild

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-17.20220611git05961ac
- Bump

* Fri May 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-16.20220527git22ad95c
- Update

* Thu May 19 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-15.20220518gitaf2fe24
- Bump

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-14.20220513git0e23b0b
- Update

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-13.20220426git15ca7e8
- Bump

* Sun Apr 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-12.20220410gitf46bccf
- Bump

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-11.20220327git0c46ea1
- Update

* Tue Mar 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-10.20220307git514eedb
- Bump

* Sat Feb 19 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-9.20220215git4fe8e40
- Last snapshot

* Wed Feb 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-8.20220206git4fe8e40
- Update

* Thu Jan 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-7.20220106git746b3c5
- Bump

* Fri Dec 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-6.20211223gitfde683a
- Return to master branch

* Fri Dec 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-5.20211216git71d0167
- Last snapshot

* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-4.20211206git27041cb
- Update

* Sat Nov 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-3.20211127git3d74553
- Bump

* Tue Nov 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-2.20211114gitc6374a8
- net-rollback branch try

* Wed Sep 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-1.20210927git5d068fc
- 1.1 last snapshot

* Sun Aug 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.0-4.20210826gita51f310
- Bump

* Thu Aug 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.0-3.20210811gitc27180f
- Update

* Sun Jul 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.0-2.20210717git147bd83
- Bump

* Mon Jul 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0-1.20210705gitb40328e
- 1.0 last snapshot

* Fri Jun 04 2021 Phantom X <megaphantomx at hotmail dot com> - 7-57.20210603git58974c9
- Update

* Sat May 29 2021 Phantom X <megaphantomx at hotmail dot com> - 7-56.20210529git24f9003
- Bump

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 7-55.20210522gitd29d43e
- Update
- Make system libchdr and lzmasdk mandatory

* Tue May 18 2021 Phantom X <megaphantomx at hotmail dot com> - 7-54.20210518git3a1ae0d
- Bump

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 7-53.20210512git23f483c
- Update

* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 7-52.20210505gitd7fd665
- New lzma-sdk rebuild

* Sat Apr 24 2021 Phantom X <megaphantomx at hotmail dot com> - 7-51.20210422git92ccd6e
- Update

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 7-50.20210420gita9e22c2
- Bump
- Add upstream metadata file

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 7-49.20210406git7296829
- Update

* Thu Apr 01 2021 Phantom X <megaphantomx at hotmail dot com> - 7-48.20210401gitb3de6a1
- Last snapshot

* Tue Mar 30 2021 Phantom X <megaphantomx at hotmail dot com> - 7-47.20210329gita892917
- Bump

* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 7-46.20210323git7205068
- Update

* Sat Mar 20 2021 Phantom X <megaphantomx at hotmail dot com> - 7-45.20210320git0b6420d
- Bump

* Wed Mar 17 2021 Phantom X <megaphantomx at hotmail dot com> - 7-44.20210316gitee109d0
- Bump to fix savestate

* Tue Mar 16 2021 Phantom X <megaphantomx at hotmail dot com> - 7-43.20210315gitbceed97
- Bump

* Tue Mar 09 2021 Phantom X <megaphantomx at hotmail dot com> - 7-42.20210309gitcb52d0b
- https://github.com/flyinghead/flycast/issues/198

* Mon Mar 08 2021 Phantom X <megaphantomx at hotmail dot com> - 7-41.20210308git99e3750
- Bump with bad commits reverted

* Fri Mar 05 2021 Phantom X <megaphantomx at hotmail dot com> - 7-40.20210302git77961d2
- Last working snapshot with post commits

* Thu Mar 04 2021 Phantom X <megaphantomx at hotmail dot com> - 7-39.20210302git77961d2
- Last working snapshot
- Missing BR: libchdr

* Thu Feb 25 2021 Phantom X <megaphantomx at hotmail dot com> - 7-38.20210224gitc6389de
- Bump

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 7-37.20210211git485ce40
- Update

* Fri Feb 05 2021 Phantom X <megaphantomx at hotmail dot com> - 7-36.20210201git30b5469
- Bump

* Fri Jan 29 2021 Phantom X <megaphantomx at hotmail dot com> - 7-35.20210128git958775f
- Bump

* Sat Jan 16 2021 Phantom X <megaphantomx at hotmail dot com> - 7-34.20210116git0c62231
- Update

* Thu Jan 07 2021 Phantom X <megaphantomx at hotmail dot com> - 7-33.20210107gite5b3c52
- New snapshot

* Wed Dec 23 2020 Phantom X <megaphantomx at hotmail dot com> - 7-32.20201221git1a59f8b
- One more

* Sat Dec 19 2020 Phantom X <megaphantomx at hotmail dot com> - 7-31.20201218gitd0d9712
- Bump

* Fri Dec 11 2020 Phantom X <megaphantomx at hotmail dot com> - 7-30.20201209gitd960f8e
- New snapshot
- R: sdl_gamecontrollerdb

* Sat Dec  5 2020 Phantom X <megaphantomx at hotmail dot com> - 7-29.20201204git579db85
- New snapshot

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 7-28.20201126git8f77a54
- Bump to remove 0001-Change-configdir-name.patch

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 7-27.20201125gitfad94ca
- Bump

* Sun Nov 22 2020 Phantom X <megaphantomx at hotmail dot com> - 7-26.20201121gita7979d4
- New snapshot

* Wed Nov 18 2020 Phantom X <megaphantomx at hotmail dot com> - 7-25.20201117git03e5988
- Bump

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 7-24.20201104gitf2893b7
- Update

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
