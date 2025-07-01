BuildArch:      noarch

%undefine _annotated_build
%undefine _auto_set_build_flags

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
%define _fortify_level 0

%undefine _hardened_build
%undefine _package_note_file
%global _default_patch_fuzz 2
# Disable LTO
%global _lto_cflags %{nil}

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}

%global commit eb0d67a0111f4263b0fbb84948eb875ec225d848
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250630
%bcond_without snapshot

%bcond_with debug
%bcond_without gplasync
%bcond_with spirv
%bcond_without vulkan

%global gplasync_id 94eb0399ee647efdf630454ee1efe53130ed3fab

%global commit5 8b246ff75c6615ba4532fe4fde20f1be090c3764
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%global commit6 46dc0f6e514f5730784bb2cac2a7c731636839e8
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 Vulkan-Headers

%global commit7 275e6459c7ab1ddd4b125f28d0440716e4888078
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 libdisplay-info

%{?mingw_package_header}

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%global instmode 0644

%global winedll dll%{?libext}

%if %{with snapshot}
%global gplasync_ver master
%else
%global gplasync_ver 2.6.2-1
%endif

%global winecommonver 7.1

%global pkgname dxvk

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global gplasync_url https://gitlab.com/Ph42oN/dxvk-gplasync/-/raw/%{gplasync_id}
%global kg_url https://github.com/KhronosGroup
%global valve_url https://github.com/ValveSoftware/dxvk

Name:           wine-%{pkgname}
Version:        2.6.2
Release:        101%{?dist}
Epoch:          1
Summary:        Vulkan-based D3D8, D3D9, D3D10 and D3D11 implementation for Linux / Wine

License:        Zlib AND MIT%{!?with_vulkan: AND Apache-2.0}
URL:            https://github.com/doitsujin/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        README.%{pkgname}-mingw
Source2:        wine%{pkgname}cfg
Source3:        %{name}-README-chinforpms

Patch100:       0001-util-Add-d3d9.deferSurfaceCreation-to-some-games.patch
Patch101:       0001-util-Another-missing-weeb-games.patch

%if %{with gplasync}
Patch500:      %{gplasync_url}/patches/dxvk-gplasync-%{gplasync_ver}.patch#/%{name}-gplasync-%{gplasync_ver}.patch
Patch501:      0001-dxvk.conf-gplasync-options.patch
Source500:     %{gplasync_url}/README.md#/README.gplasync.md
%endif

%if %{without spirv}
Source5:        %{kg_url}/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%endif
%if %{without vulkan}
Source6:        %{kg_url}/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
%endif
Source7:        https://gitlab.freedesktop.org/JoshuaAshton/%{srcname7}/-/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz

ExclusiveArch:  %{ix86} x86_64

# mingw-binutils 2.35 or patched 2.34 is needed to prevent crashes
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-binutils >= 2.34-100
BuildRequires:  mingw64-binutils >= 2.34-100
BuildRequires:  mingw64-gcc >= 10.0
BuildRequires:  mingw64-gcc-c++ >= 10.0
BuildRequires:  mingw64-headers >= 8.0
BuildRequires:  mingw64-winpthreads-static >= 8.0

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc >= 10.0
BuildRequires:  mingw32-gcc-c++ >= 10.0
BuildRequires:  mingw32-headers >= 8.0
BuildRequires:  mingw32-winpthreads-static >= 8.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
%if %{with spirv}
BuildRequires:  spirv-headers-devel >= 1.5.5
%endif
%if %{with vulkan}
BuildRequires:  vulkan-headers >= 1.3.279
%endif

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson >= 0.49
BuildRequires:  ninja-build
BuildRequires:  wine-devel >= %{winecommonver}

Requires:       vulkan-loader >= 1.1

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Obsoletes:      %{name} < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-d8vk < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-d9vk < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-dxvk-d3d9 < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-dxvk-dxgi < %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       wine-d8vk = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       wine-d9vk = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       wine-dxvk-d3d9 = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       wine-dxvk-dxgi = %{?epoch:%{epoch}:}%{version}-%{release}


%description
Provides a Vulkan-based implementation of DXGI, D3D8, D3D9, D3D10 and D3D11
in order to run 3D applications on Linux using Wine.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -N -p1
%autopatch -M 499 -p1

%if %{with gplasync}
%patch -P 500 -p1
%patch -P 501 -p1
cp %{S:500} README.gplasync.md
%endif

cp %{S:1} README.%{pkgname}

%if %{with spirv}
ln -s %{_includedir}/spirv include/spirv/include/spirv
%else
tar -xf %{S:5} -C include/spirv --strip-components 1
cp -p include/spirv/LICENSE LICENSE.spirv
%endif
%if %{with vulkan}
mkdir -p include/vulkan/include
ln -s %{_includedir}/vk_video include/vulkan/include/vk_video
ln -s %{_includedir}/vulkan include/vulkan/include/vulkan
%else
tar -xf %{S:6} -C include/vulkan --strip-components 1
cp -p include/vulkan/LICENSE.txt LICENSE.vulkan
%endif
tar -xf %{S:7} -C subprojects/libdisplay-info --strip-components 1
cp -p subprojects/libdisplay-info/LICENSE LICENSE.libdisplay-info

cp -p %{S:2} .
cp -p %{S:3} README.chinforpms

sed -e '/command:/s|git|false|g' -i meson.build

sed -e 's|@VCS_TAG@|v%{version}-%{release}|g' -i version.h.in

sed -e "/strip =/s|=.*|= 'true'|g" -i build-win*.txt


%build
export WINEPREFIX="$(pwd)/%{_vpath_builddir}/wine-build"

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

export CFLAGS="%{build_cflags} -Wno-error"

export CFLAGS="`echo $CFLAGS | sed \
  -e 's/-m64//' \
  -e 's/-m32//' \
  -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//' \
  -e 's/-fstack-protector-strong//' \
  -e 's/-grecord-gcc-switches//' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-cc1,,' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,' \
  -e 's/-fasynchronous-unwind-tables//' \
  -e 's/-fstack-clash-protection//' \
  -e 's/-fcf-protection//' \
  `"

export CXXFLAGS="${CFLAGS}"

export LDFLAGS="-Wl,-O1,--sort-common"

TEMP_CFLAGS="`mesonarray "${CFLAGS}"`"
TEMP_LDFLAGS="`mesonarray "${LDFLAGS}"`"

sed \
  -e "/-DNOMINMAX/a\  '$TEMP_CFLAGS'," \
  -e "/static-libstdc++/a\  '$TEMP_LDFLAGS'," \
  -i meson.build

%if %{without debug}
mkdir bin
# -Wl -S to build working stripped PEs
cat > bin/x86_64-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/x86_64-w64-mingw32-gcc -Wl,-S "$@"
EOF
cat > bin/i686-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/i686-w64-mingw32-gcc -Wl,-S "$@"
EOF
for i in bin/*-gcc ;do
  sed -e 's|-gcc|-g++|g' ${i} > ${i%gcc}g++
done
sed -e 's|gcc|g++|g' -i bin/*-g++
chmod 0755 bin/*g*
export PATH="$(pwd)/bin:$PATH"
%endif

%define _vpath_srcdir ..
for i in %{targetbits}
do
mkdir build${i}
pushd build${i}
%meson \
  --cross-file %{_vpath_srcdir}/build-%{cfname}${i}.txt \
  %{!?with_debug:-Db_ndebug=true} \
%{nil}

%meson_build

popd
done


%install

for dll in dxgi d3d8 d3d9 d3d11 d3d10core ;do

  case ${dll} in
    dxgi|d3d8|d3d9|d3d11)
      dlldir=${dll}
      ;;
    d3d10core)
      dlldir=d3d10
      ;;
  esac

  for i in %{targetbits} ;do
    instdir=%{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    dllname=${dll}
    mkdir -p ${instdir}
    install -pm%{instmode} build${i}/%{_vpath_builddir}/src/${dlldir}/${dll}.%{winedll} \
      ${instdir}/${dllname}.%{winedll}
  done
done

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 wine%{pkgname}cfg %{buildroot}%{_bindir}/


%files
%license LICENSE LICENSE.*
%doc README.chinforpms README.md README.%{pkgname} %{pkgname}.conf %{?with_gplasync:README.gplasync.md}
%{_bindir}/wine%{pkgname}cfg
%{_datadir}/wine/%{pkgname}/*/*.dll


%changelog
* Tue Jun 10 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.2-100
- 2.6.2

* Tue Apr 08 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.6.1-100
- 2.6.1

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.6-101
- gplasync update

* Thu Mar 13 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.6-100
- 2.6

* Mon Jan 13 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.3-100
- 2.5.3

* Fri Dec 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.2-100
- 2.5.2

* Mon Nov 18 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.1-100
- 2.5.1

* Mon Nov 11 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.5-100
- 2.5

* Thu Sep 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.1-100
- 2.4.1

* Fri Sep 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.4-105.20240919git43c2767
- Debug switch

* Thu Jul 11 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.4-100.20240711gitba47af5
- 2.4

* Sun Jul 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.3.1-107.20240707gitfe9c875
- d8vk

* Wed Mar 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.3.1-100
- 2.3.1

* Sat Jan 13 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2.3-103.20240109giteb80695
- gplasync patch

* Mon Sep 04 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2.3-100
- 2.3

* Fri May 12 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2.2-100
- 2.2

* Tue Jan 24 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2.1-100
- 2.1

* Thu Nov 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.0-100
- 2.0

* Sat Oct 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-103.20221021gitae76433
- Master snapshot
- Disable async, as it seems to be unneeded now

* Tue Aug 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.3-100
- 1.10.3

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.2-101
- Reenable async

* Thu Jul 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.2-100
- 1.10.2
- dxvk_async disabled for the time

* Sun Jul 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-108.20220702gitf95f541
- Update

* Mon Jun 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-107.20220613gitbd29fbd
- Bump

* Sat May 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-106.20220525git0678d80
- Update

* Sat May 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-105.20220510git5b7406f
- Bump

* Mon May 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-104.20220502git15fa310
- Last snaphost

* Sat Apr 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-103.20220411git736f743
- Update

* Sun Apr 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-102.20220409git727ba89
- Bump

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-101.20220329git6a80b51
- Snapshot

* Sat Mar 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10.1-100
- 1.10.1

* Fri Mar 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.10-100
- 1.10

* Fri Feb 25 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.4-104.20220224gitb42c072
- Last snapshot

* Tue Feb 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.4-103.20220215gitd45f5a8
- Again

* Tue Feb 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.4-102.20220213gitbc137fd
- Bump

* Sun Feb 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.4-101.20220202git2673d74
- Snapshot

* Mon Jan 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.4-100
- 1.9.4

* Tue Jan 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.3-100
- 1.9.3

* Sat Dec 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-109.20211205gitc13395d
- Add a PR to fix flickering

* Mon Dec 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-108.20211205gitc13395d
- Float emulation update

* Fri Dec 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-107.20211130git804eca9
- Last snapshot

* Sat Nov 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-106.20211111git12249fd
- Update

* Sat Nov 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-105.20211105git1fd037c
- Bump

* Mon Oct 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-104.20211022git8912c7a
- Last snapshot

* Sun Oct 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-103.20211015git7f89fe1
- Update

* Sun Oct 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-102.20211007git3e64e1b
- Bump

* Thu Oct 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-101.20211007git24eb875
- Snapshot

* Mon Sep 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.2-100
- 1.9.2

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.1-104.20210912gitdd7ffbc
- Last snapshot

* Mon Aug 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.1-103.20210827git69588b0
- Update

* Wed Aug 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.1-102.20210817git3718cee
- Bump

* Mon Aug 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.1-101.20210808gitada463b
- Snapshot

* Mon Jul 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9.1-100
- 1.9.1

* Thu Jul 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9-102.20210721git5037e49
- Bump

* Sun Jul 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9-101.20210703git9579132
- Snapshot

* Tue Jun 15 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.9-100.20210615git6b8ab4f
- 1.9

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-111.20210612git30a1a29
- Update

* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-110.20210606git01033af
- Last snapshot

* Sat Jun 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-109.20210601gitf4cbc9a
- Bump

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-108.20210521git94674ac
- Update

* Sun May 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-107.20210507gitb84a03b
- Bump

* Tue Apr 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-106.20210423git525fd53
- Update script to architecture-specific dll directories

* Sun Apr 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-105.20210423git525fd53
- Update

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-104.20210416git6339c8e
- Bump

* Sun Apr 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-103.20210330gita690210
- Last snapshot

* Sun Mar 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-102.20210327git6b83306
- Bump
- sse3 switch

* Sun Mar 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-101.20210313git2f553b5
- Snapshot

* Mon Mar 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8.1-100
- 1.8.1

* Fri Feb 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.8-100
- 1.8

* Sat Feb 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-107.20210212git0c18a86
- Update

* Sat Feb 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-106.20210206gitfcaab6a
- Bump
- Add some PRs

* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-105.20210130git9bee3e1
- New snapshot
- Update flags

* Sun Jan 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-104.20210116gitf869881
- Bump

* Fri Jan 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-103.20210108git0eec958
- Update

* Mon Dec 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-102.20201226gitea13a68
- Bump

* Tue Dec 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-101.20201214git56399e4
- Snapshot

* Wed Dec  2 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.3-100.20201202git0b4e167
- 1.7.3

* Sat Nov 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.2-101.20201121gitf74071a
- Snapshot

* Wed Oct 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.2-100
- 1.7.2

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.1-102.20200926gitccb7822
- Add -fno-tree-dce to fix crash with x86

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.1-101.20200926gitccb7822
- New snapshot

* Thu Aug 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7.1-100
- 1.7.1

* Mon Aug 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7-107.20200809gitb28a735
- New snapshot

* Sat Aug 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7-106.20200807git98c7da8
- Bump

* Wed Jul 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7-105.20200721git3b52cad
- New snapshot

* Mon Jul 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.7-104.20200710git5ab12d9
- Bump

* Mon Jun 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7-103.20200615git291f7e0
- New snapshot

* Wed Jun 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7-102.20200609git86c53bb
- Bump

* Wed Jun 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7-101.20200601git5558460
- Snapshot

* Sat May 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.7-100
- 1.7

* Tue May 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.1-103.20200511git6643c75
- New snapshot
- Use RPM release in version.h to dismiss upstream bug reports

* Tue May 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.1-102.20200505git68be040
- Bump
- Change to Sporif async patch, as tkg

* Sat May 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.1-101.20200501gitc9dde91
- Snapshot
- Only mingw supported now

* Mon Apr 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6.1-100
- 1.6.1

* Wed Apr 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6-103.20200414gitce3d0ab
- New snapshot
- Remove winepath fix

* Sat Apr 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6-102.20200410git7f03f45
- Bump
- Fix winepath EOL on script

* Sun Apr 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6-101.20200403git00d371d
- Snapshot

* Fri Mar 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.6-100
- 1.6

* Sun Mar 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.5-100
- 1.5.5

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.4-102.20200221git0e35389
- New snapshot

* Sun Feb 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.4-101.202002015git50cf3a4
- Snapshot

* Fri Feb 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.4-100.20200207gitc780ed5
- 1.5.4

* Thu Jan 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.3-100
- 1.5.3

* Sat Jan 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.5.2-100.20200124git9b48651
- 1.5.2

* Thu Jan 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.5.1-1
- 1.5.1

* Wed Dec 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5-2.20191225git0993f6f
- Snapshot

* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5-1
- 1.5
- Provides wine-d9vk, merged upstream

* Tue Dec 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4.6-1
- 1.4.6

* Tue Nov 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4.5-1
- 1.4.5

* Mon Oct 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4.4-1
- 1.4.4

* Fri Oct 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4.3-1
- 1.4.3

* Fri Oct 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4.2-1
- 1.4.2

* Fri Sep 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4.1-1
- 1.4.1

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1
- 1.4

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3.4-3
- Fix obsoletes

* Mon Sep 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3.4-2
- async patch

* Mon Sep 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3.4-1
- 1.3.4

* Thu Aug 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3.3-1
- 1.3.3

* Mon Aug 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3.2-1
- 1.3.2

* Sun Jul 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3.1-1
- 1.3.1

* Mon Jul 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3-2
- mingw build fu

* Sun Jul 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1
- 1.3

* Thu Jun 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.3-1
- 1.2.3

* Sat Jun 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.2-1
- 1.2.2

* Sun May 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.1-1
- 1.2.1

* Mon May 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2-1
- 1.2

* Sun May 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1.1-1
- 1.1.1

* Tue Apr 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0.3-1
- 1.0.3

* Mon Apr 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-1
- 1.0.2

* Fri Mar 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0.1-1
- 1.0.1
- Set WINEPREFIX

* Mon Feb 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1
- 1.0

* Sat Feb 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.96-3
- Update script to overrides, staging don't have redirect support anymore

* Wed Jan 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.96-2
- Reenable dxgi dll installation

* Sat Jan 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.96-1
- 0.96

* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.95-2
- dxgi unneeded now
- Update dlls suffix

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.95-1
- 0.95

* Tue Jan 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.94-1
- 0.94
- libwine renamed build

* Mon Nov 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.92-1
- 0.92

* Sun Nov 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.91-1
- 0.91

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.90-1
- 0.90

* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.81-2
- BR: gcc
- BR: gcc-c++

* Fri Oct 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.81-1
- 0.81

* Sun Sep 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.80-1
- 0.80

* Sat Sep 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.72-1
- 0.72

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.71-1
- 0.71

* Wed Aug 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.70-2
- Add forgotten d3d10 dlls

* Fri Aug 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.70-1
- 0.70

* Sun Aug 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.65-1
- 0.65

* Sun Aug 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.64-1
- 0.64

* Sat Jul 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.63-1
- 0.63

* Mon Jul 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.62-1
- 0.62

* Thu Jun 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.61-1
- 0.61
- Set minimal version for wine requirements

* Thu Jun 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.54-1
- 0.54

* Mon May 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.53-1
- 0.53

* Wed May 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.52-1
- 0.52

* Sun May 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.51-1
- 0.51

* Mon May 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.50-1
- 0.50

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.42-1
- 0.42

* Sat Apr 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.41-1
- 0.41

* Fri Mar 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.31-2
- Update script

* Thu Mar 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.31-1
- 0.31
- Rename spec file to mingw-wine-dxvk
- Change installation paths
- Strip

* Fri Mar 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.30-1
- 0.30

* Tue Jan 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.21-1
- Fix dll names.

* Fri Jan 26 2018 Phantom X <megaphantomx at bol dot com dot br>
- Install as fakedll, to use with wine-staging dll redirection
- Configuration script

* Fri Jan 19 2018 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
