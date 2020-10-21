Name:           vkd3d
Version:        1.2
Release:        100%{?gver}%{?dist}
Summary:        Direct3D 12 to Vulkan translation library

Epoch:          1

License:        LGPLv2+
URL:            http://www.winehq.org/

Source0:        https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz
Source10:       https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz.sign


BuildRequires:  gcc
BuildRequires:  pkgconfig(SPIRV-Tools-shared)
BuildRequires:  pkgconfig(vulkan) >= 1.1.113
BuildRequires:  pkgconfig(xcb-event)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  spirv-headers-devel >= 1.5.1
BuildRequires:  wine-devel

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
%autosetup -n %{name}-%{version} -p1


%build
%configure \
  --disable-static \
  --disable-silent-rules \
  --with-spirv-tools \
%{nil}

%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete


%files -n libvkd3d
%license COPYING LICENSE
%doc AUTHORS README
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
* Wed Oct 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.2-100
- 1.2
- Remove vkd3d-proton switch, better use standalone dll

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
