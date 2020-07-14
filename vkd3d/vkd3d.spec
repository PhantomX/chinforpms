%global commit 15106808f98ba1980e89b68fe1b198fa19f0b7c1
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200713
%global with_snapshot 1

# Set to use proton fork
%global proton 1
%if 0%{?proton}
%global pkgname vkd3d-proton
%else
%global pkgname vkd3d
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           vkd3d
Version:        1.1
Release:        108%{?gver}%{?dist}
Summary:        Direct3D 12 to Vulkan translation library

Epoch:          1

License:        LGPLv2+
URL:            http://www.winehq.org/

%if 0%{?with_snapshot}
Source0:        https://github.com/HansKristian-Work/%{pkgname}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz
Source10:       https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz.sign
%endif

BuildRequires:  gcc
BuildRequires:  pkgconfig(vulkan) >= 1.2.140
BuildRequires:  pkgconfig(xcb-event)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  spirv-headers-devel
BuildRequires:  pkgconfig(dxil-spirv-c-shared)
%if 0%{?with_snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  wine-devel
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


%package -n libvkd3d-utils
Summary:        Utility library for vkd3d


%description -n libvkd3d-utils
libvkd3d-utils contains simple implementations of various functions which
might be useful for source ports of Direct3D 12 applications.


%package -n libvkd3d-utils-devel
Summary:        Development files for libvkd3d-utils
Requires:       libvkd3d-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libvkd3d-utils%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description -n libvkd3d-utils-devel
Development files for libvkd3d-utils.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
autoreconf -ivf
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%configure \
  --disable-static \
  --disable-silent-rules \
%{nil}

%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete


%files -n libvkd3d
%license COPYING LICENSE
%doc AUTHORS README.md
%{_libdir}/libvkd3d.so.*
%{_libdir}/libvkd3d-shader.so.*


%files -n libvkd3d-devel
%dir %{_includedir}/vkd3d
%{_includedir}/vkd3d/vkd3d_d3d12.h
%{_includedir}/vkd3d/vkd3d_d3dcommon.h
%{_includedir}/vkd3d/vkd3d_d3d12sdklayers.h
%{_includedir}/vkd3d/vkd3d_dxgibase.h
%{_includedir}/vkd3d/vkd3d_dxgiformat.h
%{_includedir}/vkd3d/vkd3d.h
%{_includedir}/vkd3d/vkd3d_shader.h
%{_includedir}/vkd3d/vkd3d_sonames.h
%{_includedir}/vkd3d/vkd3d_types.h
%{_includedir}/vkd3d/vkd3d_windows.h
%{_libdir}/libvkd3d.so
%{_libdir}/libvkd3d-shader.so
%{_libdir}/pkgconfig/libvkd3d.pc
%{_libdir}/pkgconfig/libvkd3d-shader.pc


%files -n libvkd3d-utils
%{_libdir}/libvkd3d-utils.so.*


%files -n libvkd3d-utils-devel
%{_includedir}/vkd3d/vkd3d_utils.h
%{_libdir}/libvkd3d-utils.so
%{_libdir}/pkgconfig/libvkd3d-utils.pc


%changelog
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
