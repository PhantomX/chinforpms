%?mingw_package_header

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%undefine _hardened_build

%bcond_with tests

%global srcname dxvk
%global dxvk_dir %{_datadir}/wine/%{srcname}/%{__isa_bits}

%global winever 3.10

Name:           mingw-wine-%{srcname}
Version:        0.81
Release:        2%{?dist}
Summary:        Vulkan-based D3D11 implementation for Linux / Wine

License:        zlib
URL:            https://github.com/doitsujin/dxvk

Source0:        https://github.com/doitsujin/%{srcname}/archive/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
Source1:        README.dxvk
Source2:        winedxvkcfg

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  mingw%{__isa_bits}-filesystem
BuildRequires:  mingw%{__isa_bits}-gcc
BuildRequires:  mingw%{__isa_bits}-gcc-c++
BuildRequires:  mingw%{__isa_bits}-winpthreads-static

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  wine-core >= %{winever}
BuildRequires:  wine-devel >= %{winever}

%description
Provides a Vulkan-based implementation of DXGI and D3D11 in order to
run 3D applications on Linux using Wine.

%package        -n mingw%{__isa_bits}-wine-%{srcname}
Summary:        Vulkan-based D3D11 implementation for Linux / %{__isa_bits} bit Wine
BuildArch:      noarch
Enhances:       wine
Requires:       wine-common
%if %{__isa_bits} == 32
Requires:       wine-core(x86-32) >= %{winever}
%endif
%if %{__isa_bits} == 64
Requires:       wine-core(x86-64) >= %{winever}
Requires:       mingw32-wine-%{srcname} = %{version}-%{release}
%endif

%description   -n mingw%{__isa_bits}-wine-%{srcname}
Provides a Vulkan-based implementation of DXGI and D3D11 in order to
run 3D applications on Linux using Wine.

%prep
%autosetup -n %{srcname}-%{version}

cp %{S:1} .

%build

meson \
  --cross-file build-win%{__isa_bits}.txt \
  --buildtype "release" \
  --strip \
  %{?with_tests:-Denable_tests=true} \
  build.%{__isa_bits}

pushd build.%{__isa_bits}
ninja -v %{?_smp_mflags}
popd

%install
mkdir -p %{buildroot}%{dxvk_dir}

install -pm0644 build.%{__isa_bits}/src/dxgi/dxgi.dll \
  %{buildroot}%{dxvk_dir}/dxgi_vk.dll

install -pm0644 build.%{__isa_bits}/src/d3d11/d3d11.dll \
  %{buildroot}%{dxvk_dir}/d3d11_vk.dll

for dll in d3d10 d3d10_1 d3d10core ;do
  install -pm0644 build.%{__isa_bits}/src/d3d10/${dll}.dll \
    %{buildroot}%{dxvk_dir}/${dll}_vk.dll
done

%if %{with tests}
for file in \
  tests/d3d11/d3d11-{compute,triangle}.exe \
  tests/dxbc/dxbc-{compiler,disasm}.exe tests/dxbc/hlsl-compiler.exe \
  tests/dxgi/dxgi-factory.exe
do
  install -pm0755 build.%{__isa_bits}/${file} %{buildroot}%{dxvk_dir}/
done
%{mingw_strip} --strip-unneeded %{buildroot}%{dxvk_dir}/*.exe
%endif

%{mingw_strip} --strip-unneeded %{buildroot}%{dxvk_dir}/*.dll

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:2} %{buildroot}/%{_bindir}/

%files -n mingw%{__isa_bits}-wine-%{srcname}
%license LICENSE
%doc README.md README.dxvk
%{_bindir}/winedxvkcfg
%{dxvk_dir}/*.dll
%if %{with tests}
%{dxvk_dir}/*.exe
%endif


%changelog
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
