%?mingw_package_header

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%undefine _hardened_build

%bcond_with tests

%global srcname vk9
%global vk9_dir %{_datadir}/wine/%{srcname}/%{__isa_bits}

Name:           mingw-wine-%{srcname}
Version:        970ae52381fc815c4323402a5135ebc1c9d619d4
Release:        1%{?dist}
Summary:        Vulkan-based D3D9 implementation for Linux / Wine

License:        zlib
URL:            https://github.com/disks86/VK9

Source0:        https://github.com/disks86/VK9/archive/%{version}.tar.gz#/VK9-%{version}.tar.gz
Source1:        README.vk9
Source2:        winevk9cfg

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  mingw%{__isa_bits}-filesystem
BuildRequires:  mingw%{__isa_bits}-boost-static
BuildRequires:  mingw%{__isa_bits}-eigen3
BuildRequires:  mingw%{__isa_bits}-gcc
BuildRequires:  mingw%{__isa_bits}-gcc-c++
BuildRequires:  mingw%{__isa_bits}-spirv
BuildRequires:  mingw%{__isa_bits}-winpthreads-static
BuildRequires:  mingw%{__isa_bits}-vulkan

# glslangValidator
BuildRequires:  glslang
# glslc
#BuildRequires:  shaderc
BuildRequires:  meson
BuildRequires:  wine-core
BuildRequires:  wine-devel >= 3.0

%description
Provides a Vulkan-based implementation of D3D9 in order to
run 3D applications on Linux using Wine.

%package        -n mingw%{__isa_bits}-wine-%{srcname}
Summary:        Vulkan-based D3D11 implementation for Linux / %{__isa_bits} bit Wine
BuildArch:      noarch
Enhances:       wine
Requires:       wine-common
%if %{__isa_bits} == 32
Requires:       wine-core(x86-32)
%endif
%if %{__isa_bits} == 64
Requires:       wine-core(x86-64)
Requires:       mingw32-wine-%{srcname} = %{version}-%{release}
%endif

%description   -n mingw%{__isa_bits}-wine-%{srcname}
Provides a Vulkan-based implementation of DXGI and D3D11 in order to
run 3D applications on Linux using Wine.

%prep
%autosetup -n VK9-%{version}

cp %{S:1} .

sed \
  -e '/dependency/s|vulkan-1|vulkan|g' \
  -e "/dependency/s|'eigen'|'eigen3'|g" \
  -i meson.build

%build

meson \
  --cross-file build-win%{__isa_bits}.txt \
  --buildtype "release" \
  --strip \
  %{?with_tests:-Denable_tests=false} \
  build.%{__isa_bits}

pushd build.%{__isa_bits}
ninja -v %{?_smp_mflags}
popd
exit 20
%install
mkdir -p %{buildroot}%{vk9_dir}

install -pm0644 build.%{__isa_bits}/src/dxgi/d3d9.dll \
  %{buildroot}%{vk9_dir}/d3d9_vk9.dll

%if %{with tests}
for file in \
  tests/d3d11/d3d11-{compute,triangle}.exe \
  tests/dxbc/dxbc-{compiler,disasm}.exe tests/dxbc/hlsl-compiler.exe \
  tests/dxgi/dxgi-factory.exe
do
  install -pm0755 build.%{__isa_bits}/${file} %{buildroot}%{vk9_dir}/
done
%{mingw_strip} --strip-unneeded %{buildroot}%{vk9_dir}/*.exe
%endif

%{mingw_strip} --strip-unneeded %{buildroot}%{vk9_dir}/*.dll

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:2} %{buildroot}/%{_bindir}/

%files -n mingw%{__isa_bits}-wine-%{srcname}
%license LICENSE
%doc README.md README.vk9
%{_bindir}/winevk9cfg
%{vk9_dir}/*.dll
%if %{with tests}
%{vk9_dir}/*.exe
%endif

%changelog
* Sun May 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.25.0-1
- Initial spec
