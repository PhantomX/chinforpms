%undefine _hardened_build

%global commit 70b8ce869e35a69a002921e9282d7bab1a55715b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190508
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%ifarch %{ix86} x86_64
%global wine_mingw 1
%endif

%global libext .so
%global cfname wine
%global targetbits %{__isa_bits}

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

%global pkgname d9vk

Name:           wine-%{pkgname}
Version:        0.13f
Release:        1%{?gver}%{?dist}
Summary:        A D3D9 to VK Translation Layer for Linux / Wine

Epoch:          1

License:        zlib
URL:            https://github.com/Joshua-Ashton/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif
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

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       d3d9_%{pkgname}.%{winedll}%{?_isa} = %{?epoch:%{epoch}:}%{version}
%endif


%description
%{summary}.


%if 0%{?wine_mingw}
%global mingw_build_win32 0
%{?mingw_package_header}
%endif


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

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

sed -e "/strip =/s|=.*|= 'true'|g" -i build-wine*.txt

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
%ninja_build src/d3d9/d3d9.%{winedll}

%if !0%{?wine_mingw}
  for spec in d3d9 ;do
    winebuild --dll --fake-module -E ../src/${spec}/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
  done
%endif
popd
done

%install
for dll in d3d9 ;do
%if 0%{?wine_mingw}
  for i in %{targetbits} ;do
    mkdir -p %{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    install -pm0755 %{_target_platform}${i}/src/${dll}/${dll}.%{winedll} \
      %{buildroot}%{_datadir}/wine/%{pkgname}/${i}/${dll}.%{winedll}
  done
%else
  mkdir -p %{buildroot}/%{_libdir}/wine
  install -pm0755 %{_target_platform}%{targetbits}/src/${dll}/${dll}.%{winedll} \
    %{buildroot}%{_libdir}/wine/${dll}_%{pkgname}.%{winedll}
%endif
done

%if !0%{?wine_mingw}
  mkdir -p %{buildroot}/%{_libdir}/wine/fakedlls
  for fake in d3d9 ;do
    install -pm0755 %{_target_platform}%{targetbits}/${fake}_%{pkgname}.dll.fake \
      %{buildroot}/%{_libdir}/wine/fakedlls/${fake}_%{pkgname}.dll
  done
%endif

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 wine%{pkgname}cfg %{buildroot}/%{_bindir}/


%files
%license LICENSE
%doc README.md README.%{pkgname}
%{_bindir}/wine%{pkgname}cfg
%if 0%{?wine_mingw}
%{_datadir}/wine/%{pkgname}/*/*.dll
%else
%{_libdir}/wine/*.%{winedll}
%{_libdir}/wine/fakedlls/*.dll
%endif


%changelog
* Mon Jul 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.13f-1
- 0.13f
- mingw build fu

* Tue Jul 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.13-1
- 0.13

* Wed May 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.12-1
- 0.12

* Sun May 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.11-1
- 0.11

* Wed May 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.10-1
- 0.10

* Mon Apr 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0.1-0.2.20190429git65b8ace
- New snapshot
- Bump minimal wine version
- Remove meson fix

* Mon Apr 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.00-0.1.20190401git8867033
- Initial spec
