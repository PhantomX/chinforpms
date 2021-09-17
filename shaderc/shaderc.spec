%global commit c42db5815fad0424f0f1311de1eec92cdd77203d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210825
%global gver .%{date}git%{shortcommit}

# Glslang revision from packaged version
%global glslang_version 6abdde3ce5119e8ca3dd4e5351aa3a70f25bb689

Name:           shaderc
Version:        2021.2
Release:        100%{?gver}%{?dist}
Summary:        A collection of tools, libraries, and tests for Vulkan shader compilation

License:        ASL 2.0
URL:            https://github.com/google/shaderc

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Patch to unbundle 3rd party code
Patch1:         0001-Drop-third-party-code-in-CMakeLists.txt.patch
Patch2:         glslang_linker_flags.patch

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  glslang-devel
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools
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

%package    -n  glslc
Summary:        A command line compiler for GLSL/HLSL to SPIR-V

%description -n glslc
A command line compiler for GLSL/HLSL to SPIR-V.

%package    -n  libshaderc
Summary:        A library for compiling shader strings into SPIR-V

%description -n libshaderc
A library for compiling shader strings into SPIR-V.

%package -n     libshaderc-devel
Summary:        Development files for libshaderc
Requires:       libshaderc%{?_isa} = %{version}-%{release}

%description -n libshaderc-devel
A library for compiling shader strings into SPIR-V.

Development files for libshaderc.

%package -n     libshaderc-static
Summary:        A library for compiling shader strings into SPIR-V (static libraries)

%description -n libshaderc-static
A library for compiling shader strings into SPIR-V.

Static libraries for libshaderc.

%prep
%autosetup -p1 -n %{name}-%{commit}

rm -rf third_party

# Stolen from Gentoo
# Create build-version.inc since we want to use our packaged
# SPIRV-Tools and glslang
echo \"shaderc $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\? [[:digit:]]\{4\}-[[:digit:]]\{2\}-[[:digit:]]\{2\}$' CHANGES)\" \
        > glslc/src/build-version.inc
echo \"spirv-tools $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\? [[:digit:]]\{4\}-[[:digit:]]\{2\}-[[:digit:]]\{2\}$' /usr/share/doc/spirv-tools/CHANGES)\" \
        >> glslc/src/build-version.inc
echo \"glslang %{glslang_version}\" >> glslc/src/build-version.inc

# Point to correct include
sed -i 's|SPIRV/GlslangToSpv.h|glslang/SPIRV/GlslangToSpv.h|' libshaderc_util/src/compiler.cc

%build
# We disable the tests because they don't work with our unbundling of 3rd party.
# See https://github.com/google/shaderc/issues/470
%cmake3 \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_SKIP_RPATH=True \
  -DSHADERC_SKIP_TESTS=True \
  -DSHADERC_ENABLE_EXAMPLES=False \
  -DPYTHON_EXE=%{__python3} \
  -GNinja \
%{nil}

%cmake3_build

%install
%cmake3_install

%check
%ctest3

%files -n glslc
%doc glslc/README.asciidoc
%license LICENSE
%{_bindir}/glslc

%files -n libshaderc
%doc AUTHORS CHANGES CONTRIBUTORS README.md
%license LICENSE
%{_libdir}/libshaderc_shared.so.1*

%files -n libshaderc-devel
%{_includedir}/%{name}/
%{_libdir}/libshaderc_shared.so
%{_libdir}/pkgconfig/shaderc.pc

%files -n libshaderc-static
%license LICENSE
%{_libdir}/libshaderc.a
%{_libdir}/libshaderc_combined.a
%{_libdir}/pkgconfig/shaderc_static.pc
%{_libdir}/pkgconfig/shaderc_combined.pc

%changelog
* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.2-100.20210825gitc42db58
- 2021.2

* Sun Jul 04 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.1-100.20210621git00c8f73
- 2021.1

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.0-100.20210316git3fe94c6
- 2021.0-dev

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 2020.5-100.20210118git73b54fa
- 2020.5-dev

* Sat Dec 26 15:21:39 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2020.4-1
- Update to 2020.4
- Close: rhbz#1906260

* Sat Dec 05 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2020.3-1
- Update to 2020.3
- Close: rhbz#1875183

* Sat Aug 08 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2020.2-1
- Update to 2020.2

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 17 20:15:27 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2020.1-1
- Update to 2020.1

* Sun Feb 02 20:53:01 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2019.1-1
- Update to 2019.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 00:18:18 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 2019.0-1
- Release 2019.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 03 2018 Robert-André Mauchin <zebob.m@gmail.com> - 2018.0-1
- Release 2018.0

* Mon Sep 24 2018 Robert-André Mauchin <zebob.m@gmail.com> - 2017.2-1
- Initial build

