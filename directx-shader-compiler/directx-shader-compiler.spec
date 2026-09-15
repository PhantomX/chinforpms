%undefine _cmake_shared_libs

%global toolchain clang

%global commit10 980971e835876dc0cde415e8f9bc646e64667bf7
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 DirectX-Headers

%global commit11 29981f65241605e08b0ede4cfeb999fe3b723c6a
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 SPIRV-Headers

%global commit12 1c336172641682bab6e066767d09fdff1d826467
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 SPIRV-Tools

%global kg_url https://github.com/KhronosGroup

%global pkgname DirectXShaderCompiler

Name:           directx-shader-compiler
Version:        1.10.2605.37
Release:        1%{?dist}
Summary:        Compiler for HLSL to DXIL

License:        Apache-2.0 WITH LLVM-exception OR NCSA
URL:            https://github.com/microsoft/DirectXShaderCompiler

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
Source10:       https://github.com/microsoft/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       %{kg_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       %{kg_url}/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz

Patch0:         https://gitlab.archlinux.org/archlinux/packaging/packages/%{name}/-/raw/62ef9ecfc19cc6d15f518d3f3c625ffd7dea6638/0001-Install-more-components.patch#/%{name}-archlinux-0001-Install-more-components.patch


BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  compiler-rt
BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  lld
BuildRequires:  git
BuildRequires:  python3
BuildRequires:  pkgconfig(libxml-2.0)
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
The DirectX Shader Compiler project includes a compiler and related
tools used to compile High-Level Shader Language (HLSL) programs into
DirectX Intermediate Language (DXIL) for DirectX and the Standard Portable
Intermediate Representation (SPIR-V) for Vulkan.


%package libs
Summary:        Compiler for HLSL to DXIL - libraries

%description libs
Compiler for HLSL to DXIL - libraries.


%package devel
Summary:        Compiler for HLSL to DXIL - development files
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Compiler for HLSL to DXIL - development files.


%prep
%autosetup -n %{pkgname}-%{version} -p1

tar -xf %{S:10} -C external/%{srcname10} --strip-components 1
tar -xf %{S:11} -C external/%{srcname11} --strip-components 1
tar -xf %{S:12} -C external/%{srcname12} --strip-components 1


%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING=Release \
%if "%{?_lib}" == "lib64"
  -DLLVM_LIBDIR_SUFFIX:STRING=64 \
%endif
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -C "$(pwd)/cmake/caches/PredefinedParams.cmake" \
  -DHLSL_INCLUDE_TESTS:BOOL=OFF \
  -DHLSL_OFFICIAL_BUILD:BOOL=ON \
  -DLLVM_BUILD_TOOLS:BOOL=OFF \
  -DLLVM_INCLUDE_TESTS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}/%{_bindir}/dxl*
rm -rf %{buildroot}/%{_bindir}/dxopt*
rm -rf %{buildroot}/%{_bindir}/llvm*
rm -rf %{buildroot}/%{_libdir}/*.a
rm -rf %{buildroot}/%{_includedir}/clang*
rm -rf %{buildroot}/%{_includedir}/llvm*
rm -rf %{buildroot}/%{_datadir}/llvm*


%files
%license LICENSE.TXT
%doc README.md
%{_bindir}/dxa*
%{_bindir}/dxc*
%{_bindir}/dxr*
%{_bindir}/dxv*

%files libs
%license LICENSE.TXT
%{_libdir}/libdxcompiler.so
%{_libdir}/libdxil.so

%files devel
%license LICENSE.TXT
%{_includedir}/dxc
%{_includedir}/hlsl


%changelog
* Mon Sep 14 2026 Phantom X <megaphantomx at hotmail dot com> - 1.10.2605.37-1
- Initial spec

