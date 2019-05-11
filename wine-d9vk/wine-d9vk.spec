%undefine _hardened_build

%global commit 70b8ce869e35a69a002921e9282d7bab1a55715b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190508
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global winecommonver 4.6

%global pkgname d9vk

Name:           wine-%{pkgname}
Version:        0.10
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
Source2:        wine%{pkgname}cfg

Patch0:         %{name}-optflags.patch

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++

BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  wine-devel >= %{winecommonver}

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       d3d9_%{pkgname}.dll.so%{?_isa} = %{?epoch:%{epoch}:}%{version}


%description
%{summary}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

cp %{S:1} .

sed -e "/strip =/s|=.*|= 'true'|g" -i build-wine*.txt

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s| |g" -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"
TEMP_CFLAGS="`mesonarray "$TEMP_CFLAGS"`"

TEMP_LDFLAGS="`mesonarray "%{build_ldflags}"`"

sed \
  -e "s|RPM_OPT_FLAGS|$TEMP_CFLAGS|g" \
  -e "s|RPM_LD_FLAGS|$TEMP_LDFLAGS|g" \
  -i build-wine%{__isa_bits}.txt

%build
export WINEPREFIX="$(pwd)/%{_target_platform}/wine-build"

meson \
  --cross-file build-wine%{__isa_bits}.txt \
  --buildtype "release" \
  %{_target_platform}

pushd %{_target_platform}
%ninja_build src/d3d9/d3d9.dll.so

for spec in d3d9 ;do
  winebuild --dll --fake-module -E ../src/${spec}/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
done
popd

%install
mkdir -p %{buildroot}/%{_libdir}/wine
mkdir -p %{buildroot}/%{_libdir}/wine/fakedlls

for dll in d3d9 ;do
  install -pm0755 %{_target_platform}/src/${dll}/${dll}.dll.so \
    %{buildroot}%{_libdir}/wine/${dll}_%{pkgname}.dll.so
done

for fake in d3d9 ;do
  install -pm0755 %{_target_platform}/${fake}_%{pkgname}.dll.fake \
    %{buildroot}/%{_libdir}/wine/fakedlls/${fake}_%{pkgname}.dll
done

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:2} %{buildroot}/%{_bindir}/


%files
%license LICENSE
%doc README.md README.%{pkgname}
%{_bindir}/wine%{pkgname}cfg
%{_libdir}/wine/*.dll.so
%{_libdir}/wine/fakedlls/*.dll


%changelog
* Wed May 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:0.10-1
- 0.10

* Mon Apr 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.0.1-0.2.20190429git65b8ace
- New snapshot
- Bump minimal wine version
- Remove meson fix

* Mon Apr 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.00-0.1.20190401git8867033
- Initial spec
