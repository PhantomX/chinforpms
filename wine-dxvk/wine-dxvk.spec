%undefine _hardened_build

%ifarch %{ix86} x86_64
%global wine_mingw 1
%endif

%global libext .so
%global cfname wine
%global targetbits 64 32

%if 0%{?wine_mingw}
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global libext %{nil}
%global cfname win
%global targetbits 64 32
%endif

%global winedll dll%{?libext}

%global winecommonver 4.6

%global pkgname dxvk

Name:           wine-%{pkgname}
Version:        1.3
Release:        2%{?dist}
Summary:        Vulkan-based D3D11 implementation for Linux / Wine

License:        zlib
URL:            https://github.com/doitsujin/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
Source1:        README.%{pkgname}
Source2:        README.%{pkgname}-mingw
Source3:        wine%{pkgname}cfg

ExclusiveArch:  %{ix86} x86_64

%if 0%{?wine_mingw}
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

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

%if 0%{?wine_mingw}
Obsoletes:      %{name}(x86-64) < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}(x86-32) < %{?epoch:%{epoch}:}%{version}-%{release}

%else

Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mingw%{__isa_bits}-%{name} < %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       dxgi_%{pkgname}.%{winedll}%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d11_%{pkgname}.%{winedll}%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d10_%{pkgname}.%{winedll}%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d10_1_%{pkgname}.%{winedll}%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d10core_%{pkgname}.%{winedll}%{?_isa} = %{?epoch:%{epoch}:}%{version}
%endif


%description
Provides a Vulkan-based implementation of DXGI and D3D11 in order to
run 3D applications on Linux using Wine.


%if 0%{?wine_mingw}
%global mingw_build_win32 0
%{?mingw_package_header}
%endif


%prep
%autosetup -n %{pkgname}-%{version} -p1

%if 0%{?wine_mingw}
cp %{S:2} README.%{pkgname}
%else
cp %{S:1} .
%endif

sed \
  -e '/^dllsuffix=/s|=.*|=""|g' \
  -e '/^wineext=/s|=.*|=%{winedll}|g' \
  -e "s|lib=''|lib=32|g" \
  -e 's|/usr/lib${lib}/wine|%{_datadir}/wine/%{pkgname}/${lib}|g' \
  %{S:3} > wine%{pkgname}cfg

sed -e "/strip =/s|=.*|= 'true'|g" -i build-win*.txt

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

TEMP_LDFLAGS="%{build_ldflags}"

%if 0%{?wine_mingw}
export TEMP_CFLAGS="`echo $TEMP_CFLAGS | sed \
  -e 's/-m64//' \
  -e 's/-m32//' \
  -e 's/-fstack-protector-strong//' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,' \
  -e 's/-fstack-clash-protection//' \
  -e 's/-fcf-protection//' \
  `"

export TEMP_LDFLAGS="`echo ${TEMP_LDFLAGS} | sed -e 's/-Wl,-z,relro//' -e 's/-Wl,-z,now//'` -Wl,-S"
%endif

TEMP_CFLAGS="`mesonarray "${TEMP_CFLAGS}"`"
TEMP_LDFLAGS="`mesonarray "${TEMP_LDFLAGS}"`"

sed \
  -e "/^c_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^cpp_args/s|]|, '$TEMP_CFLAGS'\0|g" \
  -e "/^c_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
  -e "/^cpp_link_args/s|]|, '$TEMP_LDFLAGS'\0|g" \
  -i build-win*.txt


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

%if !0%{?wine_mingw}
  for spec in dxgi d3d11 ;do
    winebuild --dll --fake-module -E ../src/${spec}/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
  done
  for spec in d3d10 d3d10core d3d10_1 ;do
    winebuild --dll --fake-module -E ../src/d3d10/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
  done
%endif
popd
done

%install

for dll in dxgi d3d11 d3d10 d3d10_1 d3d10core ;do

  case ${dll} in
    dxgi|d3d11)
      dlldir=${dll}
      ;;
    d3d10|d3d10_1|d3d10core)
      dlldir=d3d10
      ;;
  esac

%if 0%{?wine_mingw}
  for i in %{targetbits} ;do
    mkdir -p %{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    install -pm0755 %{_target_platform}${i}/src/${dlldir}/${dll}.%{winedll} \
      %{buildroot}%{_datadir}/wine/%{pkgname}/${i}/${dll}.%{winedll}
  done
%else
  mkdir -p %{buildroot}/%{_libdir}/wine
  install -pm0755 %{_target_platform}%{targetbits}/src/${dlldir}/${dll}.%{winedll} \
    %{buildroot}%{_libdir}/wine/${dll}_%{pkgname}.%{winedll}
%endif
done

%if !0%{?wine_mingw}
  mkdir -p %{buildroot}/%{_libdir}/wine/fakedlls
  for fake in dxgi d3d11 d3d10 d3d10_1 d3d10core ;do
    install -pm0755 %{_target_platform}/${fake}_%{pkgname}.dll.fake \
      %{buildroot}/%{_libdir}/wine/fakedlls/${fake}_%{pkgname}.dll
  done
%endif

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 wine%{pkgname}cfg %{buildroot}/%{_bindir}/


%files
%license LICENSE
%doc README.md README.dxvk
%{_bindir}/wine%{pkgname}cfg
%if 0%{?wine_mingw}
%{_datadir}/wine/%{pkgname}/*/*.dll
%else
%{_libdir}/wine/*.%{winedll}
%{_libdir}/wine/fakedlls/*.dll
%endif


%changelog
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
