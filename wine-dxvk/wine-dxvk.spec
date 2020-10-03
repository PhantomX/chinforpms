%undefine _annotated_build
%undefine _hardened_build
%global _default_patch_fuzz 2
# Disable LTO
%define _lto_cflags %{nil}

%global commit ccb782219c93d7665927ec1b0af7c7c4fdfc067d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200926
%global with_snapshot 1

%{?mingw_package_header}

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%global instmode 0644

%global winedll dll%{?libext}

%global sporif_id 8a026804bbe794b5a691392249cf597b6a52aa3f
%global sporif_url https://github.com/Sporif/dxvk-async/raw/%{sporif_id}

%global valve_url https://github.com/ValveSoftware/dxvk

%global dxvk_async 1

%global winecommonver 5.3

%global pkgname dxvk

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           wine-%{pkgname}
Version:        1.7.1
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
Source1:        README.%{pkgname}-mingw
Source2:        wine%{pkgname}cfg
Source3:        %{name}-README-chinforpms

%if 0%{?dxvk_async}
Patch100:       %{valve_url}/commit/5388a8db837f7dd61e331eebf7ffa24c554c75e9.patch#/%{name}-valve-5388a8d.patch
Patch101:       %{sporif_url}/dxvk-async.patch#/%{name}-sporif-dxvk-async.patch
Patch103:       0001-dxvk.conf-async-options.patch
Source4:        %{sporif_url}/dxvk-async.patch#/README.async
%endif

ExclusiveArch:  %{ix86} x86_64

BuildArch:      noarch

BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-headers >= 6.0
BuildRequires:  mingw64-winpthreads-static >= 6.0
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-headers >= 6.0
BuildRequires:  mingw32-winpthreads-static >= 6.0
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
%if 0%{?dxvk_async}
%if 0%{?with_snapshot}
%setup -q -n %{pkgname}-%{commit}
%else
%setup -q -n %{pkgname}-%{version}
%endif
%patch100 -p1
%patch101 -p1
%patch103 -p1

cp %{S:4} README.async
%else
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif
%endif

cp %{S:1} README.%{pkgname}

cp %{S:2} .
cp %{S:3} README-chinforpms

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
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'`"

# -fno-tree-dce: fix x86 gcc 10 crashes
TEMP_CFLAGS="$TEMP_CFLAGS -Wno-error -mno-avx -fno-tree-dce"

TEMP_CFLAGS="`echo "$TEMP_CFLAGS" | sed -e 's/-O2\b/-O3/'`"

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

TEMP_CFLAGS="`mesonarray "${TEMP_CFLAGS}"`"

sed \
  -e "/^c_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^cpp_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -i build-win*.txt

sed -e "/^c_link_args =/acpp_args = ['$TEMP_CFLAGS']" -i build-win64.txt


%build
export WINEPREFIX="$(pwd)/%{_target_platform}/wine-build"

for i in %{targetbits}
do
meson \
  --cross-file build-%{cfname}${i}.txt \
  --buildtype "plain" \
  %{_target_platform}${i}

%ninja_build -C %{_target_platform}${i}

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
    instdir=%{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    dllname=${dll}
    mkdir -p ${instdir}
    install -pm%{instmode} %{_target_platform}${i}/src/${dlldir}/${dll}.%{winedll} \
      ${instdir}/${dllname}.%{winedll}
  done
done

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 wine%{pkgname}cfg %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README-chinforpms README.md README.dxvk dxvk.conf
%if 0%{?dxvk_async}
%doc README.async
%endif
%{_bindir}/wine%{pkgname}cfg
%{_datadir}/wine/%{pkgname}/*/*.dll

%files mingw-debuginfo
%{_datadir}/wine/%{pkgname}/*/*.debug


%changelog
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
