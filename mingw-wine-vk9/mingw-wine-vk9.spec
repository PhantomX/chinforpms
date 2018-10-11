%?mingw_package_header

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%undefine _hardened_build

%global srcname vk9
%global vk9_dir %{_datadir}/wine/%{srcname}/%{__isa_bits}

%global sdk_ver 1.1.85.0

Name:           mingw-wine-%{srcname}
Version:        0.28.1
Release:        1%{?dist}
Summary:        Vulkan-based D3D9 implementation for Linux / Wine

License:        zlib
URL:            https://github.com/disks86/VK9

Source0:        https://github.com/disks86/VK9/archive/%{version}.tar.gz#/VK9-%{version}.tar.gz
Source1:        README.vk9
Source2:        winevk9cfg
Source3:        https://sdk.lunarg.com/sdk/download/%{sdk_ver}/windows/VulkanSDK-%{sdk_ver}-Installer.exe?Human=true;u=#/VulkanSDK-%{sdk_ver}-Installer.exe

Patch0:         VK9-build-fixes.patch

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mingw%{__isa_bits}-filesystem
BuildRequires:  mingw%{__isa_bits}-boost-static
BuildRequires:  mingw%{__isa_bits}-eigen3
BuildRequires:  mingw%{__isa_bits}-gcc
BuildRequires:  mingw%{__isa_bits}-gcc-c++
BuildRequires:  mingw%{__isa_bits}-winpthreads-static
BuildRequires:  mingw%{__isa_bits}-vulkan
BuildRequires:  spirv-headers-devel

# glslangValidator
BuildRequires:  glslang
BuildRequires:  glslc
BuildRequires:  meson
BuildRequires:  wine-common
BuildRequires:  wine-core
BuildRequires:  wine-devel >= 3.5
BuildRequires:  p7zip-plugins

%description
Provides a Vulkan-based implementation of D3D9 in order to
run 3D applications on Linux using Wine.

%package        -n mingw%{__isa_bits}-wine-%{srcname}
Summary:        Vulkan-based D3D9 implementation for Linux / %{__isa_bits} bit Wine
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
Provides a Vulkan-based implementation of D3D9 in order to
run 3D applications on Linux using Wine.

%prep
%autosetup -n VK9-%{version}

rm -f dep*/*.pc

%ifarch %{ix86}
%global vlib 32
%endif

7z x %{S:3} Include/vulkan Source/lib%{?vlib}/vulkan-1.{dll,lib}

mkdir include
mv Include/vulkan include/

mkdir lib
mv Source/lib%{?vlib}/vulkan-1.{dll,lib} lib/

cp %{S:1} .

sed \
  -e "s|'-gdwarf-2'|\0, '-I/usr/include/spirv/1.2', '-I%{_builddir}/VK9-%{version}/include' |g" \
  -i build-win%{__isa_bits}.txt

%build

export WINEPREFIX="$(pwd)/VK9-build"

meson \
  --cross-file build-win%{__isa_bits}.txt \
  --buildtype "release" \
  %{?with_tests:-Denable_tests=false} \
  build.%{__isa_bits}

%ifarch x86_64
  %global mingwarch x86_64
%else
  %global mingwarch i686
%endif

pushd build.%{__isa_bits}
ninja -v %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}%{vk9_dir}

install -pm0644 build.%{__isa_bits}/VK9-Library/d3d9.dll \
  %{buildroot}%{vk9_dir}/d3d9_vk9.dll

%{mingw_strip} --strip-unneeded %{buildroot}%{vk9_dir}/*.dll

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:2} %{buildroot}/%{_bindir}/


%files -n mingw%{__isa_bits}-wine-%{srcname}
%license LICENSE.md
%doc README.md README.vk9 VK9-Library/VK9.conf
%{_bindir}/winevk9cfg
%{vk9_dir}/*.dll


%changelog
* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.28.1-1
- 0.28.1

* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.26.0-3
- BR: gcc
- BR: gcc-c++

* Mon Jul 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.26.0-2
- Proper build with LunarG Vulkan SDK
- BR: p7zip-plugins, for SDK files extraction

* Mon May 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.26.0-1
- Initial spec
