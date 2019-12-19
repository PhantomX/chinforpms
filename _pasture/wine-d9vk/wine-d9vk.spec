%undefine _hardened_build

%global commit 70b8ce869e35a69a002921e9282d7bab1a55715b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190508
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

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

%global winecommonver 4.6

%global pkgname d9vk

Name:           wine-%{pkgname}
Version:        0.40.1
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

BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  wine-devel >= %{winecommonver}

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Obsoletes:      %{name} < %{?epoch:%{epoch}:}%{version}-%{release}
%if !0%{?with_mingw}
Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name} < %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       d3d9_%{pkgname}.%{winedll}%{?_isa} = %{?epoch:%{epoch}:}%{version}
%endif


%description
%{summary}.


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
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
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

sed -e "/strip =/s|=.*|= 'true'|g" -i build-wine*.txt

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
  -Denable_dxgi=false \
  -Denable_d3d10=false \
  -Denable_d3d11=false \
  %{_target_platform}${i}

pushd %{_target_platform}${i}
%ninja_build

%if !0%{?with_mingw}
  for spec in d3d9 ;do
    winebuild --dll --fake-module -E ../src/${spec}/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
  done
%endif
popd
done

%install
for dll in d3d9 ;do
  for i in %{targetbits} ;do
%if 0%{?with_mingw}
    instdir=%{buildroot}%{_datadir}/wine/%{pkgname}/${i}
    dllname=${dll}
%else
    instdir=%{buildroot}%{_libdir}/wine
    dllname=${dll}_%{pkgname}
%endif
    mkdir -p ${instdir}
    install -pm%{instmode} %{_target_platform}${i}/src/${dll}/${dll}.%{winedll} \
      ${instdir}/${dllname}.%{winedll}
  done
done

%if !0%{?with_mingw}
  mkdir -p %{buildroot}%{_libdir}/wine/fakedlls
  for fake in d3d9 ;do
    install -pm0755 %{_target_platform}%{targetbits}/${fake}_%{pkgname}.dll.fake \
      %{buildroot}%{_libdir}/wine/fakedlls/${fake}_%{pkgname}.dll
  done
%endif

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 wine%{pkgname}cfg %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md README.%{pkgname} dxvk.conf
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
* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.40.1-1
- 0.40.1

* Sun Dec 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.40-1
- 0.40

* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.30-1
- 0.30

* Sun Sep 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.22-1
- 0.22

* Tue Sep 24 2019 Phantom X <megaphantomx at bol dot com dot br>  - 1:0.21-1
- 0.21

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.20-2
- Fix obsoletes

* Mon Aug 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.20-1
- 0.20

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
