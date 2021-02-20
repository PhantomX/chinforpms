%undefine _annotated_build
%undefine _hardened_build
%global _default_patch_fuzz 2
# Disable LTO
%global _lto_cflags %{nil}

%global with_sysvulkan 0

# Need be set for release builds too
%global commit d003424bc826afd005c68f8a8f0d42e4dae00fd0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20201214
%global with_snapshot 0

%global buildcommit %(c=%{commit}; echo ${c:0:15})

%global commit1 9857a0e60fdd2f53ab4223aa2435135630f4c29f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dxil-spirv

%global commit2 ef3290bbea35935ba8fd623970511ed9f045bbd7
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 SPIRV-Tools

%global commit3 621884d70917038caf7509f7b1b3c143807ff43f
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 SPIRV-Cross

%global commit4 fe9850767d00e46b230da6cfbc15eb86636017bd
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 Vulkan-Headers

%{?mingw_package_header}

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%global instmode 0644

%global winedll dll%{?libext}

%global valve_url https://github.com/ValveSoftware/dxvk

%global dxvk_async 1

%global winecommonver 5.3

%global pkgname vkd3d-proton

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global kg_url https://github.com/KhronosGroup

Name:           wine-%{pkgname}
Version:        2.2
Release:        1%{?gver}%{?dist}
Summary:        Direct3D 12 to Vulkan translation library

License:        LGPLv2+
URL:            https://github.com/HansKristian-Work/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        https://github.com/HansKristian-Work/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{kg_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{kg_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%if !0%{?with_sysvulkan}
Source4:        %{kg_url}/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
%endif

Source10:        README.%{pkgname}-mingw
Source11:        winevkd3dcfg

ExclusiveArch:  %{ix86} x86_64

BuildArch:      noarch

BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-headers >= 7.0
BuildRequires:  mingw64-winpthreads-static >= 7.0
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-headers >= 7.0
BuildRequires:  mingw32-winpthreads-static >= 7.0
BuildRequires:  mingw-w64-tools >= 7.0
BuildRequires:  pkgconfig(vulkan) >= 1.2.140
BuildRequires:  spirv-headers-devel >= 1.5.4
BuildRequires:  gcc
BuildRequires:  gcc-c++

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson >= 0.51

Requires:       vulkan-loader >= 1.2

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Provides:       wine-vkd3d-d3d12 = %{?epoch:%{epoch}:}%{version}-%{release}


%description
VKD3D-Proton is a fork of VKD3D, which aims to implement the full Direct3D 12
API on top of Vulkan. The project serves as the development effort for Direct3D
12 support in Proton.


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
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

tar -xf %{S:1} -C subprojects/dxil-spirv --strip-components 1
tar -xf %{S:2} -C subprojects/dxil-spirv/third_party/SPIRV-Tools --strip-components 1
tar -xf %{S:3} -C subprojects/dxil-spirv/third_party/SPIRV-Cross --strip-components 1
%if !0%{?with_sysvulkan}
tar -xf %{S:4} -C subprojects/Vulkan-Headers --strip-components 1
%endif

find -type f -name '*.h' -exec chmod -x {} ';'

%if 0%{?with_sysvulkan}
mkdir -p subprojects/Vulkan-Headers/include
ln -sf %{_includedir}/vulkan \
  subprojects/Vulkan-Headers/include/vulkan
%endif

mkdir -p subprojects/SPIRV-Headers/include
ln -sf %{_includedir}/spirv \
  subprojects/SPIRV-Headers/include/spirv

mkdir -p subprojects/dxil-spirv/third_party/spirv-headers/include/
ln -sf %{_includedir}/spirv \
  subprojects/dxil-spirv/third_party/spirv-headers/include/spirv

sed \
  -e 's|"unknown"|"%{shortcommit3}"|' \
  -e 's| unknown | %{shortcommit3} |' \
  -e 's|GIT_FOUND|GIT_FOUND_DISABLED|g' \
  -i subprojects/dxil-spirv/third_party/SPIRV-Cross/CMakeLists.txt

sed \
  -e '/-Wno-format/d' \
  -e '/command/s|git|true|g' \
  -i meson.build

sed -e 's|@VCS_TAG@|%{buildcommit}|g' -i vkd3d_build.h.in
sed -e 's|@VCS_TAG@|v%{version}|g' -i vkd3d_version.h.in

cp %{S:10} README.%{pkgname}

cp %{S:11} .

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'`"

# -fno-tree-dce: fix x86 gcc 10 crashes
TEMP_CFLAGS="$TEMP_CFLAGS -Wno-error -mno-avx -mno-avx2"

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
  -e "/^c_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^cpp_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^c_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
  -e "/^cpp_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
  -i build-win*.txt

sed \
  -e "/^c_link_args =/ac_args = ['$TEMP_CFLAGS']" \
  -e "/^c_link_args =/acpp_args = ['$TEMP_CFLAGS']" \
  -i build-win64.txt


%build
for i in %{targetbits}
do
meson \
  --wrap-mode=nodownload \
  --cross-file build-%{cfname}${i}.txt \
  --buildtype "plain" \
  -Denable_d3d12=true \
  %{_target_platform}${i} \
%{nil}

%ninja_build -C %{_target_platform}${i}

done


%install

for dll in d3d12 libvkd3d-proton-utils-2 ;do

  case ${dll} in
    d3d12)
      dlldir=${dll}
      ;;
    libvkd3d-proton-utils*)
      dlldir=vkd3d-utils
      ;;
  esac

  for i in %{targetbits} ;do
    instdir=%{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    dllname=${dll}
    mkdir -p ${instdir}
    install -pm%{instmode} %{_target_platform}${i}/libs/${dlldir}/${dll}.%{winedll} \
      ${instdir}/${dllname}.%{winedll}
  done
done

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 winevkd3dcfg %{buildroot}%{_bindir}/


%files
%license COPYING LICENSE
%doc README.md README.%{pkgname}
%{_bindir}/winevkd3dcfg
%{_datadir}/wine/%{pkgname}/*/*.dll

%files mingw-debuginfo
%{_datadir}/wine/%{pkgname}/*/*.debug


%changelog
* Fri Feb 19 2021 Phantom X <megaphantomx at hotmail dot com> - 2.2-1
- 2.2
- Build with bundled vulkan headers for the time

* Mon Dec 14 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1-1
- 2.1

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 2.0-1
- 2.0

* Fri Oct 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1-2.20201023gitc3e3965
- Bump

* Wed Oct  7 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1-1.20201007git9c04f35
- Initial spec
