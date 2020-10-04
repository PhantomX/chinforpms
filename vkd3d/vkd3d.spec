%global commit e09f129064494f2d51973910aa092433e0d49c28
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200930
%global with_snapshot 1

# Set to use proton fork
%global proton 1
%if 0%{?proton}
%global pkgname vkd3d-proton
%global vkheaders 1.2.140

%global commit1 8b37114bbfeb3d1647b5d756e08040c26f9d1e46
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 dxil-spirv

%global commit2 f15133788010b25b859a87fd82c60a4d6448fefc
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 SPIRV-Tools

%global commit3 5cc2e4f6348e3f70953f93fc5fcd0c6e8208c5b4
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 SPIRV-Cross

%else
%global pkgname vkd3d
%global vkheaders 1.1.113
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global kg_url https://github.com/KhronosGroup

Name:           vkd3d
Version:        1.1
Release:        115%{?gver}%{?dist}
Summary:        Direct3D 12 to Vulkan translation library

Epoch:          1

License:        LGPLv2+

%if 0%{?proton}
URL:            https://github.com/HansKristian-Work/%{pkgname}

Source0:        https://github.com/HansKristian-Work/%{pkgname}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
Source1:        https://github.com/HansKristian-Work/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{kg_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{kg_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz

Patch0:         0001-Install-shader-library-and-add-sonames.patch

%else
URL:            http://www.winehq.org/

Source0:        https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz
Source10:       https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz.sign
%endif

BuildRequires:  gcc
BuildRequires:  pkgconfig(vulkan) >= %{vkheaders}
BuildRequires:  pkgconfig(xcb-event)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  spirv-headers-devel >= 1.5.1
BuildRequires:  wine-devel
%if 0%{?proton}
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  glslang
%else
BuildRequires:  pkgconfig(SPIRV-Tools-shared)
%endif

# Wine does not build on aarch64 due to clang requires
# vulkan is not available in RHEL 7+ for aarch64 either
%if 0%{?rhel} >= 7
ExclusiveArch:  %{ix86} x86_64 %{arm}
%else
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%endif


%description
The vkd3d project includes libraries, shaders, utilities, and demos for
translating D3D12 to Vulkan.


%package -n libvkd3d
Summary:        D3D12 to Vulkan translation library

%description -n libvkd3d
libvkd3d is the main component of the vkd3d project. It's a 3D graphics
library built on top of Vulkan with an API very similar to Direct3D 12.


%package -n libvkd3d-devel
Summary:        Development files for vkd3d
Requires:       libvkd3d%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n libvkd3d-devel
Development files for vkd3d.


%package -n vkd3d-compiler
Summary:        Compiler tool for vkd3d

%description -n vkd3d-compiler
Compiler tool for vkd3d


%package -n libvkd3d-utils
Summary:        Utility library for vkd3d

%description -n libvkd3d-utils
libvkd3d-utils contains simple implementations of various functions which
might be useful for source ports of Direct3D 12 applications.


%package -n libvkd3d-shader
Summary:        Shader library for vkd3d
%if 0%{?proton}
Provides:       bundled(dxil-spirv) = 0~git%{shortcommit1}
%endif

%description -n libvkd3d-shader
Shader library for vkd3d


%package -n libvkd3d-shader-devel
Summary:        Development files for libvkd3d-shader
Requires:       libvkd3d-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libvkd3d-shader%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description -n libvkd3d-shader-devel
Development files for libvkd3d-shader


%package -n libvkd3d-utils-devel
Summary:        Development files for libvkd3d-utils
Requires:       libvkd3d-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libvkd3d-utils%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description -n libvkd3d-utils-devel
Development files for libvkd3d-utils.


%prep
%if 0%{?proton}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

%if 0%{?proton}
tar -xf %{S:1} -C subprojects/dxil-spirv --strip-components 1
tar -xf %{S:2} -C subprojects/dxil-spirv/third_party/SPIRV-Tools --strip-components 1
tar -xf %{S:3} -C subprojects/dxil-spirv/third_party/SPIRV-Cross --strip-components 1

find -type f -name '*.h' -exec chmod -x {} ';'

sed \
  -e 's|"unknown"|"%{shortcommit3}"|' \
  -e 's| unknown | %{shortcommit3} |' \
  -e 's|GIT_FOUND|GIT_FOUND_DISABLED|g' \
  -i subprojects/dxil-spirv/third_party/SPIRV-Cross/CMakeLists.txt

sed \
  -e 's|third_party/spirv-headers/include/spirv/unified1|%{_includedir}/spirv/unified1|g' \
  -i subprojects/dxil-spirv/meson.build

sed \
  -e '/-Wno-format/d' \
  -e '/command/s|git|true|g' \
  -e 's|./subprojects/Vulkan-Headers/include|%{_includedir}|g' \
  -e 's|./subprojects/SPIRV-Headers/include|%{_includedir}|g' \
  -i meson.build

sed -e 's|@VCS_TAG@|%{shortcommit}|g' -i vkd3d_version.c.in

%endif

%build
%if 0%{?proton}
%meson \
  -Denable_extras=true \
%{nil}
%meson_build

%else
%configure \
  --disable-static \
  --disable-silent-rules \
  --with-spirv-tools \
%{nil}

%make_build
%endif


%install
%if 0%{?proton}
%meson_install

rm -f %{buildroot}%{_bindir}/{gears,triangle}

# Install all headers, can break things, but...
install -pm0755 include/vkd3d_shader.h %{buildroot}%{_includedir}/vkd3d/

for header in d3d12 d3d12sdklayers d3dcommon dxgibase dxgiformat swapchain_factory dxgi1_2 ;do
  install -pm0644 "$(find -name "vkd3d_${header}.h" | head -n1)" %{buildroot}%{_includedir}/vkd3d/
done

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/libvkd3d-shader.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: vkd3d-shader
Description: The vkd3d Shader Translation Library
Version: %{version}
Cflags: -I${includedir}/vkd3d
Libs: -L${libdir} -lvkd3d-shader
EOF

%else
%make_install
%endif


find %{buildroot} -name '*.la' -delete


%files -n libvkd3d
%license COPYING LICENSE
%doc AUTHORS README.md
%{_libdir}/libvkd3d.so.*


%files -n libvkd3d-devel
%dir %{_includedir}/vkd3d
%{_includedir}/vkd3d/vkd3d.h
%{_includedir}/vkd3d/vkd3d_d3d12.h
%{_includedir}/vkd3d/vkd3d_d3d12sdklayers.h
%{_includedir}/vkd3d/vkd3d_d3dcommon.h
%{_includedir}/vkd3d/vkd3d_dxgibase.h
%{_includedir}/vkd3d/vkd3d_dxgiformat.h
%{_includedir}/vkd3d/vkd3d_types.h
%{_includedir}/vkd3d/vkd3d_windows.h
%if 0%{?proton}
%{_includedir}/vkd3d/vkd3d_dxgi1_2.h
%{_includedir}/vkd3d/vkd3d_sonames.h
%{_includedir}/vkd3d/vkd3d_swapchain_factory.h
%{_includedir}/vkd3d/vkd3d_win32.h
%endif
%{_libdir}/libvkd3d.so
%{_libdir}/pkgconfig/libvkd3d.pc


%files -n vkd3d-compiler
%{_bindir}/vkd3d-compiler


%files -n libvkd3d-shader
%license COPYING LICENSE
%{_libdir}/libvkd3d-shader.so.*


%files -n libvkd3d-shader-devel
%{_includedir}/vkd3d/vkd3d_shader.h
%{_libdir}/libvkd3d-shader.so
%{_libdir}/pkgconfig/libvkd3d-shader.pc


%files -n libvkd3d-utils
%{_libdir}/libvkd3d-utils.so.*


%files -n libvkd3d-utils-devel
%{_includedir}/vkd3d/vkd3d_utils.h
%{_libdir}/libvkd3d-utils.so
%{_libdir}/pkgconfig/libvkd3d-utils.pc


%changelog
* Sat Oct 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-115.20200930gite09f129
- New snapshot
- Build with meson
- Bundle dxil-spirv

* Sat Sep 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-114.20200922git7238802
- Bump

* Sat Sep 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-113.20200911git1ce14c2
- New snapshot

* Sat Aug 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-112.20200821gite9aab2b
- Bump

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-111.20200801git376a05e
- New snapshot

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-110.20200724git376a05e
- Bump

* Wed Jul 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-109.20200714gitdebb93f
- New snapshot

* Mon Jul 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-108.20200713git1510680
- Bump

* Mon Jul 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-107.20200706gitcb1da02
- New snapshot
- Proton fork switch

* Wed Jul 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-106.20200701git211b9c3
- Bump

* Fri Jun 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-105.20200626git12b71b9
- New snapshot

* Tue Jun 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1-104.20200616gitbfd7127
- Bump

* Sat Jun 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1-103.20200603gitf0c9627
- New snapshot

* Tue May 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1-102.20200514git71034ac
- Bump

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1-101.20200506git0d74a13
- HansKristian snapshot
- dxil-spirv support

* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1-100
- 1.1

* Sun Oct 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0-102.chinfo
- BR:gcc

* Fri Jun 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0-101.chinfo
- Sync with Fedora

* Sat May 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0-100.chinfo
- Initial spec
