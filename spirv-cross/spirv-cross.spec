%global commit 6fd1f75636b1c424b809ad8a84804654cf5ae48b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240619
%bcond snapshot 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname SPIRV-Cross

Name:           spirv-cross
Version:        1.4.341.0
Release:        1%{?dist}
Summary:        API and commands for processing SPIR-V modules

License:        Apache-2.0
URL:            https://github.com/KhronosGroup/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/vulkan-sdk-%{version}/%{name}-vulkan-sdk-%{version}.tar.gz
%endif

BuildRequires:  cmake3
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

%description
%{pkgname} is a tool designed for parsing and converting SPIR-V to other shader
languages.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
Development files for %{name}.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:vulkan-sdk-%{version}} -p1

sed \
  -e '/spirv-cross-build-version/s|unknown|vulkan-sdk-%{version}|g' \
  -e 's|GIT_FOUND|GIT_FOUND_DISABLED|g' \
  -e 's|CMAKE_INSTALL_DATAROOTDIR}/${config_name}/cmake|CMAKE_INSTALL_LIBDIR}/cmake/${config_name}|g' \
  -i CMakeLists.txt

%build
%cmake3 \
  -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DSPIRV_CROSS_SHARED:BOOL=ON \
  -DSPIRV_CROSS_STATIC:BOOL=OFF \
  -DSPIRV_CROSS_CLI:BOOL=OFF \
  -DSPIRV_CROSS_ENABLE_TESTS:BOOL=OFF \
  -DSPIRV_CROSS_ENABLE_GLSL:BOOL=ON \
  -DSPIRV_CROSS_ENABLE_HLSL:BOOL=ON \
  -DSPIRV_CROSS_ENABLE_MSL:BOOL=ON \
  -DSPIRV_CROSS_ENABLE_CPP:BOOL=ON \
  -DSPIRV_CROSS_ENABLE_REFLECT:BOOL=ON \
  -DSPIRV_CROSS_ENABLE_C_API:BOOL=ON \
  -DSPIRV_CROSS_ENABLE_UTIL:BOOL=ON \
%{nil}

%cmake3_build

%install
%cmake3_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libspirv-cross-c-shared.so.*

%files devel
%{_includedir}/spirv_cross/
%{_libdir}/cmake/spirv_cross_c_shared/
%{_libdir}/libspirv-cross-c-shared.so
%{_libdir}/pkgconfig/spirv-cross-c-shared.pc


%changelog
* Sun Feb 15 2026 Phantom X <megaphantomx at hotmail dot com> - 1.4.341.0-1
- 1.4.341.0

* Wed Sep 17 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.321.0-1
- 1.4.321.0

* Tue Feb 04 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.304.0-1
- 1.4.304.0

* Sat Aug 03 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.290.0-1
- 1.3.290.0

* Wed Jun 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.283.0-1
- Initial spec

