# Disable this, like mesa full package.
%global _lto_cflags %{nil}

%ifnarch s390x
%if !0%{?rhel}
%global with_r300 1
%global with_r600 1
%endif
%global with_radeonsi 1
%endif

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%global commit d4d47ef6efa91a4f28b01fa0cd3f17f0442455b8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221004
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname mesa
%global vc_url  https://gitlab.freedesktop.org/mesa/mesa

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           %{pkgname}-freeworld
Summary:        Mesa-based video acceleration drivers - freeworld
# If rc, use "~" instead "-", as ~rc1
Version:        22.3.0~rc3
Release:        100%{?gver}%{?dist}

Epoch:          100

License:        MIT
URL:            http://www.mesa3d.org

%if 0%{?with_snapshot}
Source0:        %{vc_url}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        https://mesa.freedesktop.org/archive/%{pkgname}-%{ver}.tar.xz
%endif
Source2:        org.mesa3d.vaapi.freeworld.metainfo.xml
Source3:        org.mesa3d.vdpau.freeworld.metainfo.xml

BuildRequires:  meson >= 0.53
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext


BuildRequires:  kernel-headers
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.110
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xdamage) >= 1.1
BuildRequires:  pkgconfig(xfixes) >= 2.0
BuildRequires:  pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2) >= 1.8
BuildRequires:  pkgconfig(xcb-dri3) >= 1.13
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pkgconfig(xshmfence) >= 1.1
BuildRequires:  pkgconfig(dri2proto) >= 2.8
BuildRequires:  pkgconfig(glproto) >= 1.4.14
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xrandr) >= 1.3
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pkgconfig(vdpau) >= 1.1
BuildRequires:  pkgconfig(libva) >= 1.8.0
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libglvnd) >= 1.3.2
BuildRequires:  llvm-devel >= 11.0.0
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  pkgconfig(libzstd)

%description
%{summary}.


%package -n     %{pkgname}-va-drivers-freeworld
Summary:        Mesa-based VAAPI drivers - freeworld
Obsoletes:      %{pkgname}-va-drivers < %{?epoch:%{epoch}:}
Provides:       %{pkgname}-va-drivers = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{pkgname}-va-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{pkgname}-filesystem%{?_isa} >= %{version}
Enhances:       %{pkgname}%{?_isa}

%description -n %{pkgname}-va-drivers-freeworld
%{summary}.


%package -n     %{pkgname}-vdpau-drivers-freeworld
Summary:        Mesa-based VDPAU drivers- freeworld
Obsoletes:      %{pkgname}-vdpau-drivers < %{?epoch:%{epoch}:}
Provides:       %{pkgname}-vdpau-drivers = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{pkgname}-vdpau-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{pkgname}-filesystem%{?_isa} >= %{version}
Enhances:       %{pkgname}%{?_isa}

%description -n %{pkgname}-vdpau-drivers-freeworld
%{summary}.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{ver}} -p1

%build
%meson \
  -Dplatforms=x11 \
  -Ddri3=enabled \
  -Dosmesa=false \
  -Dgallium-drivers=virgl,nouveau%{?with_r300:,r300}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600} \
  -Dgallium-vdpau=enabled \
  -Dgallium-omx=disabled \
  -Dgallium-va=enabled \
  -Dgallium-xa=disabled \
  -Dgallium-nine=false \
  -Dgallium-opencl=disabled \
  -Dgallium-rusticl=false \
  -Dvulkan-drivers="" \
  -Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
  -Dshared-glapi=enabled \
  -Dgles1=disabled \
  -Dgles2=disabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=true \
  -Dglvnd=true \
  -Dmicrosoft-clc=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Db_ndebug=true \
  -Dbuild-tests=false \
  -Dselinux=true \
  %{nil}

%meson_build


%install
%meson_install

# libvdpau opens the versioned name, don't bother including the unversioned
rm -vf %{buildroot}%{_libdir}/vdpau/*.so

rm -rf %{buildroot}%{_libdir}/*.so*
rm -rf %{buildroot}%{_libdir}/dri/*_dri.so*
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}

# install Appdata files
mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 %{S:2} %{buildroot}%{_metainfodir}
install -pm0644 %{S:3} %{buildroot}%{_metainfodir}


%files -n %{pkgname}-va-drivers-freeworld
%license docs/license.rst
%{_libdir}/dri/nouveau_drv_video.so
%{_libdir}/dri/virtio_gpu_drv_video.so
%if 0%{?with_r600}
%{_libdir}/dri/r600_drv_video.so
%endif
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_drv_video.so
%endif
%{_metainfodir}/org.mesa3d.vaapi.freeworld.metainfo.xml

%files -n %{pkgname}-vdpau-drivers-freeworld
%license docs/license.rst
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%{_libdir}/vdpau/libvdpau_virtio_gpu.so.1*
%if 0%{?with_r300}
%{_libdir}/vdpau/libvdpau_r300.so.1*
%endif
%if 0%{?with_r600}
%{_libdir}/vdpau/libvdpau_r600.so.1*
%endif
%if 0%{?with_radeonsi}
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%{_metainfodir}/org.mesa3d.vdpau.freeworld.metainfo.xml


%changelog
* Sat Nov 19 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.3.0~rc3-100
- 22.3.0~rc3

* Thu Nov 17 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.2.4-100
- 22.2.4

* Thu Nov 10 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.2.3-101
- RPMFusion sync

* Wed Nov 09 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.2.3-100
- 22.2.3

* Wed Oct 19 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.2.2-100
- 22.2.2

* Wed Oct 12 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.2.1-100
- 22.2.1

* Wed Oct 05 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.2.0-101.202201004gitd4d47ef
- Rename vaapi to va

* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0-100.20220929git9d1f0e8
- Initial spec
