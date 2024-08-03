# Glslang revision from packaged version
%global glslang_version 436237a4ab2be3225acedc66016ea2aa82946b37

%global commit feb2460bf3a504d67011246edeb810c45ea58826
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240728

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname shaderc

Name:           %{pkgname}-patched
Version:        2024.3
Release:        1%{?dist}
Epoch:          1
Summary:        Collection of tools, libraries, and tests for Vulkan shader compilation

License:        Apache-2.0
URL:            https://github.com/stenzek/shaderc

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

# Patch to unbundle 3rd party code
Patch0:         0001-Drop-third-party-code-in-CMakeLists.txt.patch
Patch1:         glslang_linker_flags.patch
Patch10:        0001-shared-patched-cmake.patch


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  sed
BuildRequires:  spirv-tools

BuildRequires:  glslang-devel
BuildRequires:  python3-devel
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools-devel

%description
A collection of tools, libraries and tests for shader compilation.

Shaderc aims to to provide:
 - a command line compiler with GCC- and Clang-like usage, for better
   integration with build systems
 - an API where functionality can be added without breaking existing clients
 - an API supporting standard concurrency patterns across multiple
   operating systems
 - increased functionality such as file #include support

This build is patched for some emulators.

%package    -n  lib%{name}
Summary:        A library for compiling shader strings into SPIR-V

%description -n lib%{name}
A library for compiling shader strings into SPIR-V.

This build is patched for some emulators.

%package -n     lib%{name}-devel
Summary:        Development files for libshaderc
Requires:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n lib%{name}-devel
A library for compiling shader strings into SPIR-V.

Development files for lib%{name}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

rm -rf third_party

# Point to correct include
sed -i 's|SPIRV/GlslangToSpv.h|glslang/SPIRV/GlslangToSpv.h|' libshaderc_util/src/compiler.cc

%build
# We disable the tests because they don't work with our unbundling of 3rd party.
# See https://github.com/google/shaderc/issues/470
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -DSHADERC_SKIP_TESTS:BOOL=ON \
  -DSHADERC_ENABLE_COPYRIGHT_CHECK:BOOL=ON \
  -DPYTHON_EXECUTABLE=%{python3} \
  -GNinja \
%{nil}

%cmake_build

%install
%cmake_install

sed -e '/^#include/s|shaderc/|%{name}/|g' -i %{buildroot}%{_includedir}/%{name}/shaderc.h

%check
%ctest

%files -n lib%{name}
%doc AUTHORS CHANGES CONTRIBUTORS README.md
%license LICENSE
%{_libdir}/lib%{name}_shared.so.1*

%files -n lib%{name}-devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}_shared.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Aug 03 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.3-1.20240728gitfeb2460
- 2024.3

* Sat May 18 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.1-1
- Initial spec

