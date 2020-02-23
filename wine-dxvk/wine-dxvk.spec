%undefine _hardened_build
%global _default_patch_fuzz 2

%global commit 0e353895fdd1a811209e02221cfd293b4b824ea7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200221
%global with_snapshot 1

%ifarch %{ix86} x86_64
%global with_mingw 1
%endif

%global libext .so
%global cfname wine
%global targetbits %{__isa_bits}
%global instmode 0755

%if 0%{?with_mingw}
%{?mingw_package_header}

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%global instmode 0644
%endif

%global winedll dll%{?libext}

%global tkg_id e3d5a83aae06c5c63003bd1da2b7f6ed40db5a8e
%global tkg_url https://github.com/Tk-Glitch/PKGBUILDS/raw/%{tkg_id}/dxvk-tools/DXVKBUILD/patches

%global valve_url https://github.com/ValveSoftware/dxvk

%global dxvk_async 1

%global winecommonver 4.6

%global pkgname dxvk

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           wine-%{pkgname}
Version:        1.5.4
Release:        102%{?gver}%{?dist}
Epoch:          1
Summary:        Vulkan-based D3D9, D3D10 and D3D11 implementation for Linux / Wine

License:        zlib
URL:            https://github.com/doitsujin/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        README.%{pkgname}
Source2:        README.%{pkgname}-mingw
Source3:        wine%{pkgname}cfg
Source4:        README.async

%if 0%{?dxvk_async}
Patch100:       %{valve_url}/commit/5388a8db837f7dd61e331eebf7ffa24c554c75e9.patch#/%{name}-valve-5388a8d.patch
Patch101:       %{tkg_url}/dxvk-async.dxvkpatchb#/%{name}-tkg-dxvk-async.patch
Patch103:       0001-dxvk.conf-async-option.patch
%endif

ExclusiveArch:  %{ix86} x86_64

%if 0%{?with_mingw}
BuildArch:      noarch

BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-headers >= 6.0
BuildRequires:  mingw64-winpthreads-static >= 6.0
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-headers >= 6.0
BuildRequires:  mingw32-winpthreads-static >= 6.0
%endif
BuildRequires:  gcc
BuildRequires:  gcc-c++

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  wine-devel >= %{winecommonver}

Requires:       vulkan-loader >= 1.1

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Obsoletes:      %{name} < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-d9vk < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-dxvk-d3d9 < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      wine-dxvk-dxgi < %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       wine-d9vk = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       wine-dxvk-d3d9 = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       wine-dxvk-dxgi = %{?epoch:%{epoch}:}%{version}-%{release}

%if !0%{?with_mingw}
Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mingw%{__isa_bits}-%{name} < %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%endif


%description
Provides a Vulkan-based implementation of DXGI, D3D9, D3D10 and D3D11
in order to run 3D applications on Linux using Wine.


%if 0%{?with_mingw}
%package mingw-debuginfo
Summary:        Debug information for package %{name}
AutoReq:        0
AutoProv:       1
BuildArch:      noarch
%description mingw-debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.
%endif


%prep
%if 0%{?dxvk_async}
%if 0%{?with_snapshot}
%setup -q -n %{pkgname}-%{commit}
%else
%setup -q -n %{pkgname}-%{version}
%endif
%patch100 -p1
%patch101 -p1
%patch103 -p1

cp %{S:4} .
%else
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif
%endif


%if 0%{?with_mingw}
cp %{S:2} README.%{pkgname}

sed \
  -e '/^dllsuffix=/s|=.*|=""|g' \
  -e '/^wineext=/s|=.*|=%{winedll}|g' \
  -e "s|lib=''|lib=32|g" \
  -e 's|/usr/lib${lib}/wine|%{_datadir}/wine/%{pkgname}/${lib}|g' \
  %{S:3} > wine%{pkgname}cfg

%else
cp %{S:1} .
cp %{S:3} .
%endif

sed -e "/strip =/s|=.*|= 'true'|g" -i build-win*.txt

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

TEMP_CFLAGS="`echo "$TEMP_CFLAGS" | sed -e 's/-O2\b/-O3/'`"

%if 0%{?with_mingw}
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
  ` --param=ssp-buffer-size=4"

%else
TEMP_LDFLAGS="`mesonarray "%{build_ldflags}"`"
%endif

TEMP_CFLAGS="`mesonarray "${TEMP_CFLAGS}"`"

sed \
  -e "/^c_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^cpp_args/s|]|, '$TEMP_CFLAGS'\0|g" \
%if !0%{?with_mingw}
  -e "/^c_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
  -e "/^cpp_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
%endif
  -i build-win*.txt

sed -e "/^c_link_args =/acpp_args = ['$TEMP_CFLAGS']" -i build-win64.txt


%build
export WINEPREFIX="$(pwd)/%{_target_platform}/wine-build"

for i in %{targetbits}
do
meson \
  --cross-file build-%{cfname}${i}.txt \
  --buildtype "release" \
  %{_target_platform}${i}

pushd %{_target_platform}${i}
%ninja_build

%if !0%{?with_mingw}
  for spec in dxgi d3d9 d3d11 ;do
    winebuild --dll --fake-module -E ../src/${spec}/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
  done
  for spec in d3d10 d3d10core d3d10_1 ;do
    winebuild --dll --fake-module -E ../src/d3d10/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
  done
%endif
popd
done

%install

for dll in dxgi d3d9 d3d11 d3d10 d3d10_1 d3d10core ;do

  case ${dll} in
    dxgi|d3d9|d3d11)
      dlldir=${dll}
      ;;
    d3d10|d3d10_1|d3d10core)
      dlldir=d3d10
      ;;
  esac

  for i in %{targetbits} ;do
%if 0%{?with_mingw}
    instdir=%{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    dllname=${dll}
%else
    instdir=%{buildroot}/%{_libdir}/wine
    dllname=${dll}_%{pkgname}
%endif
    mkdir -p ${instdir}
    install -pm%{instmode} %{_target_platform}${i}/src/${dlldir}/${dll}.%{winedll} \
      ${instdir}/${dllname}.%{winedll}
  done
done

%if !0%{?with_mingw}
  mkdir -p %{buildroot}%{_libdir}/wine/fakedlls
  for fake in dxgi d3d9 d3d11 d3d10 d3d10_1 d3d10core ;do
    install -pm0755 %{_target_platform}/${fake}_%{pkgname}.dll.fake \
      %{buildroot}%{_libdir}/wine/fakedlls/${fake}_%{pkgname}.dll
  done
%endif

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 wine%{pkgname}cfg %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md README.dxvk dxvk.conf
%if 0%{?dxvk_async}
%doc README.async
%endif
%{_bindir}/wine%{pkgname}cfg
%if 0%{?with_mingw}
%{_datadir}/wine/%{pkgname}/*/*.dll
%else
%{_libdir}/wine/*.%{winedll}
%{_libdir}/wine/fakedlls/*.dll
%endif

%if 0%{?with_mingw}
%files mingw-debuginfo
%{_datadir}/wine/%{pkgname}/*/*.debug
%endif


%changelog
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
