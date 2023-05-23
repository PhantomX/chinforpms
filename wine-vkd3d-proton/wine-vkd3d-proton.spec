%undefine _annotated_build
%undefine _auto_set_build_flags
%define _fortify_level 0
%undefine _hardened_build
# Disable LTO
%global _lto_cflags %{nil}

%bcond_with sysspirv
%bcond_without sysvulkan

# Need be set for release builds too
%global commit ccb7444c187adb23577d5f12711b229ab4e32845
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230411
%bcond_with snapshot

%global buildcommit %(c=%{commit}; echo ${c:0:15})

%global commit1 f20a0fb4e984a83743baa9d863eb7b26228bcca3
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dxil-spirv

%global commit2 e150e716ff57dd69cf31d45344121f10de8925af
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 SPIRV-Tools

%global commit3 210a80013067672b52847ec7aa70ff78b2f4d77e
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 SPIRV-Cross

%global commit4 bd6443d28f2ebecedfb839b52d612011ba623d14
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 Vulkan-Headers

%global commit5 aa331ab0ffcb3a67021caa1a0c1c9017712f2f31
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 SPIRV-Headers

%{?mingw_package_header}

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%global instmode 0644

%global winedll dll%{?libext}

%global valve_url https://github.com/ValveSoftware/dxvk

%global winecommonver 5.3

%global pkgname vkd3d-proton

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global kg_url https://github.com/KhronosGroup

Name:           wine-%{pkgname}
Version:        2.9
Release:        1%{?dist}
Summary:        Direct3D 12 to Vulkan translation library

# dxil-spirv - MIT
License:        LGPL-2.1-or-later AND MIT
URL:            https://github.com/HansKristian-Work/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        https://github.com/HansKristian-Work/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{kg_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{kg_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%if %{without sysvulkan}
Source4:        %{kg_url}/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
%endif
%if %{without sysspirv}
Source5:        %{kg_url}/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%endif

Source10:        README.%{pkgname}-mingw
Source11:        winevkd3dcfg

ExclusiveArch:  %{ix86} x86_64


# mingw-binutils 2.35 or patched 2.34 is needed to prevent crashes
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-binutils >= 2.34-100
BuildRequires:  mingw64-binutils >= 2.34-100
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-headers >= 7.0
BuildRequires:  mingw64-winpthreads-static >= 7.0

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-headers >= 7.0
BuildRequires:  mingw32-winpthreads-static >= 7.0
BuildRequires:  mingw-w64-tools >= 7.0
BuildRequires:  pkgconfig(vulkan) >= 1.3.228
%if %{with sysspirv}
BuildRequires:  spirv-headers-devel >= 1.5.4
%endif
%if %{with sysvulkan}
BuildRequires:  vulkan-headers >= 1.3.228
%endif
BuildRequires:  gcc
BuildRequires:  gcc-c++

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson >= 0.51

Requires:       vulkan-loader >= 1.2

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Provides:       bundled(dxil-spirv) = 0~git%{shortcommit1}

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
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

tar -xf %{S:1} -C subprojects/dxil-spirv --strip-components 1
tar -xf %{S:2} -C subprojects/dxil-spirv/third_party/SPIRV-Tools --strip-components 1
tar -xf %{S:3} -C subprojects/dxil-spirv/third_party/SPIRV-Cross --strip-components 1
%if %{without sysvulkan}
tar -xf %{S:4} -C subprojects/Vulkan-Headers --strip-components 1
%endif
%if %{without sysspirv}
tar -xf %{S:5} -C subprojects/SPIRV-Headers --strip-components 1
rm -rf subprojects/dxil-spirv/third_party/spirv-headers
ln -sf ../../../subprojects/SPIRV-Headers subprojects/dxil-spirv/third_party/spirv-headers
%endif

find -type f -name '*.h' -exec chmod -x {} ';'

%if %{with sysvulkan}
mkdir -p subprojects/Vulkan-Headers/include
ln -sf %{_includedir}/vulkan \
  subprojects/Vulkan-Headers/include/vulkan
ln -sf %{_includedir}/vk_video \
  subprojects/Vulkan-Headers/include/vk_video
%endif

%if %{with sysspirv}
mkdir -p subprojects/SPIRV-Headers/include
ln -sf %{_includedir}/spirv \
  subprojects/SPIRV-Headers/include/spirv

mkdir -p subprojects/dxil-spirv/third_party/spirv-headers/include/
ln -sf %{_includedir}/spirv \
  subprojects/dxil-spirv/third_party/spirv-headers/include/spirv
%endif

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

cp -p subprojects/dxil-spirv/LICENSE.MIT LICENSE.MIT.dxil-spirv

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=[0-9]//'`"

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
  %{_vpath_builddir}${i} \
%{nil}

%ninja_build -C %{_vpath_builddir}${i}

done


%install

for dll in d3d12 d3d12core ;do

  case ${dll} in
    libvkd3d-proton-utils*)
      dlldir=vkd3d-utils
      ;;
    d3d12*)
      dlldir=${dll}
      ;;
  esac

  for i in %{targetbits} ;do
    instdir=%{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    dllname=${dll}
    mkdir -p ${instdir}
    install -pm%{instmode} %{_vpath_builddir}${i}/libs/${dlldir}/${dll}.%{winedll} \
      ${instdir}/${dllname}.%{winedll}
  done
done

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 winevkd3dcfg %{buildroot}%{_bindir}/


%files
%license COPYING LICENSE*
%doc README.md README.%{pkgname}
%{_bindir}/winevkd3dcfg
%{_datadir}/wine/%{pkgname}/*/*.dll

%files mingw-debuginfo
%{_prefix}/lib/debug/%{_datadir}/wine/%{pkgname}/*/*.debug


%changelog
* Sat May 20 2023 Phantom X <megaphantomx at hotmail dot com> - 2.9-1
- 2.9

* Tue Apr 04 2023 Phantom X <megaphantomx at hotmail dot com> - 2.8-3.20230331git42e3adc
- Add d3d12core new library

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 2.8-2
- Fix build with system vulkan headers

* Thu Dec 15 2022 Phantom X <megaphantomx at hotmail dot com> - 2.8-1
- 2.8

* Thu Oct 27 2022 Phantom X <megaphantomx at hotmail dot com> - 2.7-1
- 2.7

* Fri Oct 07 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-10.20221007gitc42f24a
- Use bundled SPIRV-Headers for now

* Wed Jul 27 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-9.20220726gitd00d035
- Bump

* Sun Jul 03 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-8.20220630git684e41f
- Update

* Mon Jun 20 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-7.20220617gitde5b751
- Bump

* Sat May 28 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-6.20220525gitcca7613
- Update

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-5.20220514git1a773cf
- Bump

* Mon May 02 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-4.20220428git4603c25
- Last snapshot

* Sat Apr 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-3.20220408git25c4bc1
- Update

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-2.20220324git2e8fb27
- Snapshot

* Fri Mar 04 2022 Phantom X <megaphantomx at hotmail dot com> - 2.6-1
- 2.6

* Sun Feb 27 2022 Phantom X <megaphantomx at hotmail dot com> - 2.5-3.20220225gitdc622fc
- Bump for extra fixes

* Fri Feb 25 2022 Phantom X <megaphantomx at hotmail dot com> - 2.5-2.20220225git4b07535
- Snapshot

* Mon Oct 18 2021 Phantom X <megaphantomx at hotmail dot com> - 2.5-1
- 2.5

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 2.4-2.20210916git2b13d06
- Snapshot

* Thu Jul 08 2021 Phantom X <megaphantomx at hotmail dot com> - 2.4-1
- 2.4

* Wed Apr 28 2021 Phantom X <megaphantomx at hotmail dot com> - 2.3.1-1
- 2.3.1

* Tue Apr 27 2021 Phantom X <megaphantomx at hotmail dot com> - 2.3-3
- Update script to architecture-specific dll directories

* Sun Apr 25 2021 Phantom X <megaphantomx at hotmail dot com> - 2.3-2
- Update script

* Thu Apr 22 2021 Phantom X <megaphantomx at hotmail dot com> - 2.3-1
- 2.3

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
