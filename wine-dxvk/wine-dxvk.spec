%undefine _annotated_build
%undefine _hardened_build
%global _default_patch_fuzz 2
# Disable LTO
%global _lto_cflags %{nil}

%global commit 525fd53bbc6c2c0ff73560bca9f543652035eddc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210423
%global with_snapshot 1

%{?mingw_package_header}

# Disable sse3 flags
%bcond_without sse3

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%global instmode 0644

%global winedll dll%{?libext}

%global sporif_id be40dd7a9687373cdd5a3748d973b826465df0ed
%global sporif_url https://github.com/Sporif/dxvk-async/raw/%{sporif_id}

%global valve_url https://github.com/ValveSoftware/dxvk

%global dxvk_async 1

%global winecommonver 5.3

%global pkgname dxvk

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           wine-%{pkgname}
Version:        1.8.1
Release:        105%{?gver}%{?dist}
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

Patch100:       %{valve_url}/commit/01352d5441b3c27b20b4126243e1f83b230e8e7d.patch#/%{name}-valve-01352d5.patch
Patch101:       %{url}/pull/1582.patch#/%{name}-gh-pr1582.patch

%if 0%{?dxvk_async}
Patch200:       %{sporif_url}/dxvk-async.patch#/%{name}-sporif-dxvk-async.patch
Patch201:       0001-dxvk.conf-async-options.patch
Source4:        %{sporif_url}/README.md#/README.async.md
%endif

ExclusiveArch:  %{ix86} x86_64

BuildArch:      noarch

# mingw-binutils 2.35 or patched 2.34 is needed to prevent crashes
BuildRequires:  mingw32-binutils >= 2.34-100
BuildRequires:  mingw64-binutils >= 2.34-100
BuildRequires:  mingw64-gcc >= 10.0
BuildRequires:  mingw64-gcc-c++ >= 10.0
BuildRequires:  mingw64-headers >= 8.0
BuildRequires:  mingw64-winpthreads-static >= 8.0
BuildRequires:  mingw32-gcc >= 10.0
BuildRequires:  mingw32-gcc-c++ >= 10.0
BuildRequires:  mingw32-headers >= 8.0
BuildRequires:  mingw32-winpthreads-static >= 8.0
BuildRequires:  gcc
BuildRequires:  gcc-c++

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  ninja-build
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

%patch200 -p1
%patch201 -p1

cp %{S:4} README.async.md
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

TEMP_CFLAGS="`echo "$TEMP_CFLAGS" | sed -e 's/-O2\b/-O3/'`"

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
  -e "/static-libstdc++/a\  add_global_link_arguments('$TEMP_LDFLAGS', language : 'cpp')" \
  -e "/static-libstdc++/a\  add_global_link_arguments('$TEMP_LDFLAGS', language : 'c')" \
  -e "/static-libstdc++/a\  add_project_arguments('$TEMP_CFLAGS', language : 'cpp')" \
  -e "/static-libstdc++/a\  add_project_arguments('$TEMP_CFLAGS', language : 'c')" \
%if %{without sse3}
  -e "s|if dxvk_compiler.has_argument('-msse3')|if dxvk_compiler.has_argument('-msse3_disabled')|g" \
  -e "s|and dxvk_compiler.has_argument('-msse3')||g" \
  -e "s| '-msse3',||g" \
%endif
  -i meson.build

%build
export WINEPREFIX="$(pwd)/%{_target_platform}/wine-build"

for i in %{targetbits}
do
meson \
  --wrap-mode=nodownload \
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
%doc README.async.md
%endif
%{_bindir}/wine%{pkgname}cfg
%{_datadir}/wine/%{pkgname}/*/*.dll

%files mingw-debuginfo
%{_datadir}/wine/%{pkgname}/*/*.debug


%changelog
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
