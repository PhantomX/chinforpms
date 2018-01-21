%?mingw_package_header

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%undefine _hardened_build

%global srcname dxvk

Name:           wine-%{srcname}
Version:        0.21
Release:        1%{?dist}
Summary:        Vulkan-based D3D11 implementation for Linux / Wine 

License:        zlib
URL:            https://github.com/doitsujin/dxvk

Source0:        https://github.com/doitsujin/%{srcname}/archive/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
Source1:        README.dxvk

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  glslang-devel
BuildRequires:  meson
BuildRequires:  mingw%{__isa_bits}-filesystem
BuildRequires:  mingw%{__isa_bits}-gcc
BuildRequires:  mingw%{__isa_bits}-gcc-c++
BuildRequires:  mingw%{__isa_bits}-winpthreads-static
BuildRequires:  wine-core
BuildRequires:  wine-devel

Enhances:       wine

Requires:       wine-common
%ifarch x86_64
Requires:       %{name}(x86-32) = %{version}-%{release}
%endif

%description
Provides a Vulkan-based implementation of DXGI and D3D11 in order to
run 3D applications on Linux using Wine.

%prep
%autosetup -n %{srcname}-%{version}

cp %{S:1} .

%build

meson \
  --cross-file build-win%{__isa_bits}.txt \
  build.%{__isa_bits}

pushd build.%{__isa_bits}
meson \
  -Dprefix=/usr \
  -Dlibdir=/usr/lib64 \
  -Dbuildtype=release
ninja -v %{?_smp_mflags}
popd


%install
mkdir -p %{buildroot}/%{_libdir}/wine/dxvk

for file in \
  src/dxgi/dxgi.dll src/d3d11/d3d11.dll \
  tests/d3d11/d3d11-{compute,triangle}.exe \
  tests/dxbc/dxbc-{compiler,disasm}.exe tests/dxbc/hlsl-compiler.exe \
  tests/dxgi/dxgi-factory.exe
do
  install -pm0755 build.%{__isa_bits}/${file} %{buildroot}/%{_libdir}/wine/dxvk/
done

%files
%license LICENSE
%doc README.md README.dxvk
%{_libdir}/wine/dxvk/*.dll
%{_libdir}/wine/dxvk/*.exe

%changelog
* Fri Jan 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.21-1
- Initial spec
