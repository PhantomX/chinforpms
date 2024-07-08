%undefine _annotated_build
%undefine _auto_set_build_flags
%define _fortify_level 0
%undefine _hardened_build
%undefine _package_note_file
%global _default_patch_fuzz 2
# Disable LTO
%global _lto_cflags %{nil}

%global commit 1a039a4729b9a8f0440739eec4cedf59e79a3aa0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230615
%bcond_without snapshot

%bcond_with sysspirv
%bcond_without sysvulkan

%global commit5 0bcc624926a25a2a273d07877fd25a6ff5ba1cfb
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%global commit6 98f440ce6868c94f5ec6e198cc1adda4760e8849
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 Vulkan-Headers

%global commit7 275e6459c7ab1ddd4b125f28d0440716e4888078
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 libdisplay-info

%{?mingw_package_header}

# Disable sse3 flags
%bcond_without nosse3

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%global instmode 0644

%global winedll dll%{?libext}

%global winecommonver 5.3

%global pkgname d8vk

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global kg_url https://github.com/KhronosGroup
%global valve_url https://github.com/ValveSoftware/dxvk

Name:           wine-%{pkgname}
Version:        1.0
Release:        3%{?dist}

Summary:        Vulkan-based D3D8 implementation for Linux / Wine

License:        Zlib AND MIT%{!?with_sysvulkan: AND Apache-2.0}
URL:            https://github.com/AlpyneDreams/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/refs/tags/%{pkgname}-v%{version}.tar.gz
%endif
Source1:        README.%{pkgname}-mingw
Source2:        wine%{pkgname}cfg

%if %{without sysspirv}
Source5:        %{kg_url}/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%endif
%if %{without sysvulkan}
Source6:        %{kg_url}/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
%endif
Source7:        https://gitlab.freedesktop.org/JoshuaAshton/%{srcname7}/-/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz

Patch10:        0001-gcc-14-build-fix.patch

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
%if %{with sysspirv}
BuildRequires:  spirv-headers-devel >= 1.5.5
%endif
%if %{?with_sysvulkan}
BuildRequires:  vulkan-headers >= 1.3.231
%endif

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson >= 0.49
BuildRequires:  ninja-build
BuildRequires:  wine-devel >= %{winecommonver}

Requires:       vulkan-loader >= 1.1

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Requires:       wine-dxvk >= 2.2
Enhances:       wine


%description
Provides a Vulkan-based implementation of DXGI, D3D9, D3D10 and D3D11
in order to run 3D applications on Linux using Wine.


%package mingw-debuginfo
Summary:        Debug information for package %{name}
AutoReq:        0
AutoProv:       1
BuildArch:      noarch
%description mingw-debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{pkgname}-v%{version}} -p1

cp %{S:1} README.%{pkgname}

%if %{with sysspirv}
ln -s %{_includedir}/spirv include/spirv/include/spirv
%else
tar -xf %{S:5} -C include/spirv --strip-components 1
cp -p include/spirv/LICENSE LICENSE.spirv
%endif
%if %{with sysvulkan}
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

sed -e '/command:/s|git|false|g' -i meson.build

sed -e 's|@VCS_TAG@|v%{version}-%{release}|g' -i version.h.in

sed -e "/strip =/s|=.*|= 'true'|g" -i build-win*.txt

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=[0-9]//'`"

TEMP_CFLAGS="`echo "$TEMP_CFLAGS" | sed -e 's/-O2\b/-O3/'`"

TEMP_CFLAGS="$TEMP_CFLAGS -Wno-error"

export TEMP_CFLAGS="`echo $TEMP_CFLAGS | sed \
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

TEMP_LDFLAGS="-Wl,-O1,--sort-common"

TEMP_CFLAGS="`mesonarray "${TEMP_CFLAGS}"`"
TEMP_LDFLAGS="`mesonarray "${TEMP_LDFLAGS}"`"

sed \
  -e "/-DNOMINMAX/a\  '$TEMP_CFLAGS'," \
  -e "/static-libstdc++/a\  '$TEMP_LDFLAGS'," \
%if %{without nosse3}
  -e "/-msse3/d" \
%endif
  -i meson.build

%build
export WINEPREFIX="$(pwd)/%{_vpath_builddir}/wine-build"

for i in %{targetbits}
do
meson \
  --wrap-mode=nodownload \
  --cross-file build-%{cfname}${i}.txt \
  --buildtype "plain" \
  -Denable_d3d9=true \
  -Denable_d3d10=false \
  -Denable_d3d11=false \
  -Denable_dxgi=false \
  %{_vpath_builddir}${i}

%ninja_build -C %{_vpath_builddir}${i}

done


%install

for dll in d3d8 ;do

  case ${dll} in
    d3d8)
      dlldir=${dll}
      ;;
  esac

  for i in %{targetbits} ;do
    instdir=%{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    dllname=${dll}
    mkdir -p ${instdir}
    install -pm%{instmode} %{_vpath_builddir}${i}/src/${dlldir}/${dll}.%{winedll} \
      ${instdir}/${dllname}.%{winedll}
  done
done

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 wine%{pkgname}cfg %{buildroot}%{_bindir}/


%files
%license LICENSE LICENSE.*
%doc README.md README.%{pkgname} dxvk.conf
%{_bindir}/wine%{pkgname}cfg
%{_datadir}/wine/%{pkgname}/*/*.dll

%files mingw-debuginfo
%{_prefix}/lib/debug/%{_datadir}/wine/%{pkgname}/*/*.debug


%changelog
* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0-3.20230615git1a039a4
- gcc 14 build fix

* Wed May 10 2023 Phantom X <megaphantomx at hotmail dot com> - 1.0-1
- Initial spec
