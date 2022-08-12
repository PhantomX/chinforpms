# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

%ifnarch s390x
%global with_hardware 1
%global with_vulkan_hw 1
%global with_vdpau 1
%global with_vaapi 1
%if !0%{?rhel}
%global with_nine 1
%global with_omx 1
%global with_opencl 1
%endif
%global base_vulkan ,amd
%endif

%ifarch %{ix86} x86_64
%global with_crocus 1
%global with_iris   1
%global with_vmware 1
%global with_xa     1
%global platform_vulkan ,intel
%endif

%ifarch %{arm} aarch64
%if !0%{?rhel}
%global with_etnaviv   1
%global with_lima      1
%global with_vc4       1
%global with_v3d       1
%endif
%global with_freedreno 1
%global with_kmsro     1
%global with_panfrost  1
%global with_tegra     1
%global with_xa        1
%global platform_vulkan ,broadcom,freedreno
%endif

%ifnarch %{arm} s390x
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

%global vulkan_drivers swrast%{?base_vulkan}%{?platform_vulkan}
%global vulkan_layers device-select,overlay

%global with_lto 0

%global vc_url  https://gitlab.freedesktop.org/mesa/mesa
%global ixit_url  https://github.com/iXit/Mesa-3D/commit

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           mesa
Summary:        Mesa graphics libraries
# If rc, use "~" instead "-", as ~rc1
Version:        22.1.6
Release:        100%{?dist}

License:        MIT
URL:            http://www.mesa3d.org

Source0:        https://mesa.freedesktop.org/archive/%{name}-%{ver}.tar.xz
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source1:        Mesa-MLAA-License-Clarification-Email.txt

# Patches from Karol Herbst to make Tegra work again:
# https://bugzilla.redhat.com/show_bug.cgi?id=1989726#c46
# see also:
# https://gitlab.freedesktop.org/mesa/mesa/-/issues/5399
# Last four revert https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/3724
Patch0005: 0003-Revert-nouveau-Use-format-modifiers-in-buffer-alloca.patch
Patch0006: 0004-Revert-nouveau-no-modifier-the-invalid-modifier.patch
Patch0007: 0005-Revert-nouveau-Use-DRM_FORMAT_MOD_NVIDIA_BLOCK_LINEA.patch
Patch0008: 0006-Revert-nouveau-Stash-supported-sector-layout-in-scre.patch


BuildRequires:  meson >= 0.53
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext


%if 0%{?with_hardware}
BuildRequires:  kernel-headers
%endif
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.110
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.24
BuildRequires:  pkgconfig(wayland-client) >= 1.18
BuildRequires:  pkgconfig(wayland-server) >= 1.18
BuildRequires:  pkgconfig(wayland-egl-backend) >= 3
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
%if 0%{?with_vdpau}
BuildRequires:  pkgconfig(vdpau) >= 1.1
%endif
%if 0%{?with_vaapi}
BuildRequires:  pkgconfig(libva) >= 1.8.0
%endif
%if 0%{?with_omx}
BuildRequires:  pkgconfig(libomxil-bellagio)
%endif
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libglvnd) >= 1.3.2
BuildRequires:  llvm-devel >= 11.0.0
%if 0%{?with_opencl}
BuildRequires:  clang-devel
BuildRequires:  pkgconfig(libclc)
%endif
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  vulkan-headers
BuildRequires:  glslang
%if 0%{?with_vulkan_hw}
BuildRequires:  pkgconfig(vulkan)
%endif
BuildRequires:  pkgconfig(libzstd)

# vulkan-overlay
BuildRequires:  glslang
BuildRequires:  lm_sensors-devel
BuildRequires:  /usr/bin/pathfix.py


%description
%{summary}.

%package filesystem
Summary:        Mesa driver filesystem
Provides:       mesa-dri-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-dri-filesystem < %{?epoch:%{epoch}:}%{version}-%{release}

%description filesystem
%{summary}.

%package libGL
Summary:        Mesa libGL runtime libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-glx%{?_isa} >= 1:1.3.2

%description libGL
%{summary}.

%package libGL-devel
Summary:        Mesa libGL development package
Requires:       %{name}-libGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa} >= 1:1.3.2
Provides:       libGL-devel
Provides:       libGL-devel%{?_isa}
Recommends:     gl-manpages

%description libGL-devel
%{summary}.

%package libEGL
Summary:        Mesa libEGL runtime libraries
Requires:       libglvnd-egl%{?_isa} >= 1:1.3.2

%description libEGL
%{summary}.

%package libEGL-devel
Summary:        Mesa libEGL development package
Requires:       %{name}-libEGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa} >= 1:1.3.2
Requires:       %{name}-khr-devel%{?_isa}
Provides:       libEGL-devel
Provides:       libEGL-devel%{?_isa}

%description libEGL-devel
%{summary}.

%package dri-drivers
Summary:        Mesa-based DRI drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description dri-drivers
%{summary}.

%if 0%{?with_omx}
%package omx-drivers
Summary:        Mesa-based OMX drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description omx-drivers
%{summary}.
%endif

%if 0%{?with_vdpau}
%package        vdpau-drivers
Summary:        Mesa-based VDPAU drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description vdpau-drivers
%{summary}.
%endif

%package libOSMesa
Summary:        Mesa offscreen rendering libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libOSMesa
Provides:       libOSMesa%{?_isa}

%description libOSMesa
%{summary}.

%package libOSMesa-devel
Summary:        Mesa offscreen rendering development package
Requires:       %{name}-libOSMesa%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libOSMesa-devel
%{summary}.

%package libgbm
Summary:        Mesa gbm runtime library
Provides:       libgbm
Provides:       libgbm%{?_isa}

%description libgbm
%{summary}.

%package libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm-devel
Provides:       libgbm-devel%{?_isa}

%description libgbm-devel
%{summary}.

%if 0%{?with_xa}
%package libxatracker
Summary:        Mesa XA state tracker
Provides:       libxatracker
Provides:       libxatracker%{?_isa}

%description libxatracker
%{summary}.

%package libxatracker-devel
Summary:        Mesa XA state tracker development package
Requires:       %{name}-libxatracker%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libxatracker-devel
Provides:       libxatracker-devel%{?_isa}

%description libxatracker-devel
%{summary}.
%endif

%package libglapi
Summary:        Mesa shared glapi
Provides:       libglapi
Provides:       libglapi%{?_isa}

%description libglapi
%{summary}.

%if 0%{?with_opencl}
%package libOpenCL
Summary:        Mesa OpenCL runtime library
Requires:       ocl-icd%{?_isa}
Requires:       libclc%{?_isa}
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       opencl-filesystem

%description libOpenCL
%{summary}.

%package libOpenCL-devel
Summary:        Mesa OpenCL development package
Requires:       %{name}-libOpenCL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libOpenCL-devel
%{summary}.
%endif

%if 0%{?with_nine}
%package libd3d
Summary:        Mesa Direct3D9 state tracker

%description libd3d
%{summary}.

%package libd3d-devel
Summary:        Mesa Direct3D9 state tracker development package
Requires:       %{name}-libd3d%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libd3d-devel
%{summary}.
%endif

%package vulkan-drivers
Summary:        Mesa Vulkan drivers
Requires:       vulkan%{_isa}

%description vulkan-drivers
The drivers with support for the Vulkan API.

%package vulkan-devel
Summary:        Mesa Vulkan development files
Requires:       %{name}-vulkan-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       vulkan-devel

%description vulkan-devel
Headers for development with the Vulkan API.

%package vulkan-lavapipe-layer
Summary:        Mesa Vulkan lavapipe layer
Requires:       %{name}-vulkan-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description vulkan-lavapipe-layer
The lavapipe layer is a gallium frontend. It takes the Vulkan API and roughly
translates it into the gallium API.


%package vulkan-overlay
Summary:        Mesa Vulkan overlay layer
Requires:       %{name}-vulkan-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description vulkan-overlay
A Vulkan layer to display information about the running application using
an overlay.


%prep
%autosetup -n %{name}-%{ver} -p1
cp %{SOURCE1} docs/

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" \
  src/vulkan/overlay-layer/mesa-overlay-control.py

%build
%if 0%{?with_lto}
%set_build_flags
MESA_LTO_FLAGS="-flto=%{_smp_build_ncpus} -ffat-lto-objects -flto-odr-type-merging"
MESA_COMMON_FLAGS="-falign-functions=32 -fno-semantic-interposition $MESA_LTO_FLAGS"

export CFLAGS+=" $MESA_COMMON_FLAGS"
export FCFLAGS="$CFLAGS"
export FFLAGS="$CFLAGS"
export CXXFLAGS+=" $MESA_COMMON_FLAGS"
export LDFLAGS+=" $MESA_LTO_FLAGS"

export CC=gcc
export CXX=g++
export AR="gcc-ar"
export NM="gcc-nm"
export RANLIB="gcc-ranlib"
%endif

%meson \
  -Dplatforms=x11,wayland \
  -Ddri3=enabled \
  -Dosmesa=true \
%if 0%{?with_hardware}
  -Dgallium-drivers=swrast,virgl,nouveau%{?with_r300:,r300}%{?with_crocus:,crocus}%{?with_iris:,iris}%{?with_vmware:,svga}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600}%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_v3d:,v3d}%{?with_kmsro:,kmsro}%{?with_lima:,lima}%{?with_panfrost:,panfrost}%{?with_vulkan_hw:,zink} \
%else
  -Dgallium-drivers=swrast,virgl \
%endif
  -Dgallium-vdpau=%{?with_vdpau:enabled}%{!?with_vdpau:disabled} \
  -Dgallium-xvmc=disabled \
  -Dgallium-omx=%{?with_omx:bellagio}%{!?with_omx:disabled} \
  -Dgallium-va=%{?with_vaapi:enabled}%{!?with_vaapi:disabled} \
  -Dgallium-xa=%{?with_xa:enabled}%{!?with_xa:disabled} \
  -Dgallium-nine=%{?with_nine:true}%{!?with_nine:false} \
  -Dgallium-opencl=%{?with_opencl:icd}%{!?with_opencl:disabled} \
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dvulkan-layers=%{?vulkan_layers} \
  -Dshared-glapi=enabled \
  -Dgles1=disabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
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
# likewise glvnd
rm -vf %{buildroot}%{_libdir}/libGLX_mesa.so
rm -vf %{buildroot}%{_libdir}/libEGL_mesa.so
# XXX can we just not build this
rm -vf %{buildroot}%{_libdir}/libGLES*

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd %{buildroot}%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd


%files filesystem
%doc docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%if 0%{?with_hardware}
%if 0%{?with_vdpau}
%dir %{_libdir}/vdpau
%endif
%endif

%files libGL
%{_libdir}/libGLX_mesa.so.0*
%{_libdir}/libGLX_system.so.0*
%files libGL-devel
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/libglapi.so

%files libEGL
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libEGL_mesa.so.0*
%files libEGL-devel
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglextchromium.h

%files libglapi
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%files libOSMesa
%{_libdir}/libOSMesa.so.8*
%files libOSMesa-devel
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%files libgbm
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*
%files libgbm-devel
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%if 0%{?with_xa}
%files libxatracker
%if 0%{?with_hardware}
%{_libdir}/libxatracker.so.2
%{_libdir}/libxatracker.so.2.*
%endif

%files libxatracker-devel
%if 0%{?with_hardware}
%{_libdir}/libxatracker.so
%{_includedir}/xa_tracker.h
%{_includedir}/xa_composite.h
%{_includedir}/xa_context.h
%{_libdir}/pkgconfig/xatracker.pc
%endif
%endif

%if 0%{?with_opencl}
%files libOpenCL
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd
%files libOpenCL-devel
%{_libdir}/libMesaOpenCL.so
%endif

%if 0%{?with_nine}
%files libd3d
%dir %{_libdir}/d3d/
%{_libdir}/d3d/*.so.*

%files libd3d-devel
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so
%endif

%files dri-drivers
%dir %{_datadir}/drirc.d
%{_datadir}/drirc.d/00-mesa-defaults.conf
%{_datadir}/drirc.d/00-radv-defaults.conf
%{_libdir}/dri/kms_swrast_dri.so
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/virtio_gpu_dri.so

%if 0%{?with_hardware}
%if 0%{?with_r300}
%{_libdir}/dri/r300_dri.so
%endif
%if 0%{?with_radeonsi}
%if 0%{?with_r600}
%{_libdir}/dri/r600_dri.so
%endif
%{_libdir}/dri/radeonsi_dri.so
%endif
%ifarch %{ix86} x86_64
%{_libdir}/dri/crocus_dri.so
%{_libdir}/dri/iris_dri.so
%endif
%ifarch %{arm} aarch64
%{_libdir}/dri/ingenic-drm_dri.so
%{_libdir}/dri/imx-drm_dri.so
%{_libdir}/dri/kirin_dri.so
%{_libdir}/dri/mali-dp_dri.so
%{_libdir}/dri/mcde_dri.so
%{_libdir}/dri/mxsfb-drm_dri.so
%{_libdir}/dri/stm_dri.so
%endif
%if 0%{?with_vc4}
%{_libdir}/dri/vc4_dri.so
%endif
%if 0%{?with_v3d}
%{_libdir}/dri/v3d_dri.so
%endif
%if 0%{?with_freedreno}
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%endif
%if 0%{?with_etnaviv}
%{_libdir}/dri/etnaviv_dri.so
%endif
%if 0%{?with_tegra}
%{_libdir}/dri/tegra_dri.so
%endif
%if 0%{?with_lima}
%{_libdir}/dri/lima_dri.so
%endif
%if 0%{?with_panfrost}
%{_libdir}/dri/panfrost_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%{_libdir}/dri/nouveau_drv_video.so
%if 0%{?with_r600}
%{_libdir}/dri/r600_drv_video.so
%endif
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_drv_video.so
%endif
%endif
%if 0%{?with_opencl}
%dir %{_libdir}/gallium-pipe
%{_libdir}/gallium-pipe/*.so
%endif
%if 0%{?with_kmsro}
%{_libdir}/dri/armada-drm_dri.so
%{_libdir}/dri/exynos_dri.so
%{_libdir}/dri/hx8357d_dri.so
%{_libdir}/dri/ili9225_dri.so
%{_libdir}/dri/ili9341_dri.so
%{_libdir}/dri/imx-dcss_dri.so
%{_libdir}/dri/mediatek_dri.so
%{_libdir}/dri/meson_dri.so
%{_libdir}/dri/mi0283qt_dri.so
%{_libdir}/dri/pl111_dri.so
%{_libdir}/dri/repaper_dri.so
%{_libdir}/dri/rockchip_dri.so
%{_libdir}/dri/st7586_dri.so
%{_libdir}/dri/st7735r_dri.so
%{_libdir}/dri/sun4i-drm_dri.so
%endif
%if 0%{?with_vulkan_hw}
%{_libdir}/dri/zink_dri.so
%endif

%if 0%{?with_omx}
%files omx-drivers
%{_libdir}/bellagio/libomx_mesa.so
%endif
%if 0%{?with_vdpau}
%files vdpau-drivers
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%if 0%{?with_r300}
%{_libdir}/vdpau/libvdpau_r300.so.1*
%endif
%if 0%{?with_r600}
%{_libdir}/vdpau/libvdpau_r600.so.1*
%endif
%if 0%{?with_radeonsi}
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%endif

%files vulkan-drivers
%{_libdir}/libVkLayer_MESA_device_select.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_device_select.json
%if 0%{?with_vulkan_hw}
%{_libdir}/libvulkan_radeon.so
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%ifarch %{ix86} x86_64
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%endif
%ifarch %{arm} aarch64
%{_libdir}/libvulkan_broadcom.so
%{_datadir}/vulkan/icd.d/broadcom_icd.*.json
%{_libdir}/libvulkan_freedreno.so
%{_datadir}/vulkan/icd.d/freedreno_icd.*.json
%endif
%endif

%files vulkan-devel

%files vulkan-lavapipe-layer
%{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json

%files vulkan-overlay
%doc src/vulkan/overlay-layer/README.rst
%{_bindir}/mesa-overlay-control.py
%{_libdir}/libVkLayer_MESA_overlay.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_MESA_overlay.json


%changelog
* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.6-100
- 22.1.6

* Wed Aug 03 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.5-100
- 22.1.5

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.4-100
- 22.1.4

* Wed Jun 29 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.3-100
- 22.1.3

* Thu Jun 16 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.2-100
- 22.1.2

* Wed Jun 01 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.1-100
- 22.1.1

* Wed May 18 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.0-100
- 22.1.0

* Sat May 07 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.3-100
- 22.0.3

* Fri Apr 22 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.2-100
- 22.0.2

* Mon Apr 11 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.1-101
- Rebuild (llvm)

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.1-100
- 22.0.1

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.0-101
- Rawhide sync

* Thu Mar 10 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.0-100
- 22.0.0

* Fri Mar 04 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.0~rc3-100
- 22.0.0-rc3

* Thu Feb 10 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.0~rc2-100
- 22.0.0-rc2
- Remove old unsupported dri drivers removed from tree from list

* Wed Jan 26 2022 Phantom X <megaphantomx at hotmail dot com> - 21.3.5-100
- 21.3.5

* Thu Jan 13 2022 Phantom X <megaphantomx at hotmail dot com> - 21.3.4-100
- 21.3.4

* Wed Dec 29 2021 Phantom X <megaphantomx at hotmail dot com> - 21.3.3-100
- 21.3.3

* Sat Dec 18 2021 Phantom X <megaphantomx at hotmail dot com> - 21.3.2-100
- 21.3.2

* Wed Dec 01 2021 Phantom X <megaphantomx at hotmail dot com> - 21.3.1-100
- 21.3.1

* Thu Nov 18 2021 Phantom X <megaphantomx at hotmail dot com> - 21.3.0-100
- 21.3.0

* Wed Nov 17 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.5-101
- Rebuild (llvm)

* Fri Oct 29 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.5-100
- 21.2.5

* Fri Oct 15 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.4-100
- 21.2.4

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.3-101
- Rawhide sync

* Wed Sep 29 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.3-100
- 21.2.3

* Tue Sep 21 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.2-100
- 21.2.2

* Thu Aug 19 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.1-100
- 21.2.1

* Wed Aug 04 2021 Phantom X <megaphantomx at hotmail dot com> - 21.2.0-100
- 21.2.0

* Wed Jul 28 2021 Phantom X <megaphantomx at hotmail dot com> - 21.1.6-100
- 21.1.6

* Thu Jul 15 2021 Phantom X <megaphantomx at hotmail dot com> - 21.1.5-100
- 21.1.5

* Wed Jun 30 2021 Phantom X <megaphantomx at hotmail dot com> - 21.1.4-100
- 21.1.4

* Sat Jun 19 2021 Phantom X <megaphantomx at hotmail dot com> - 21.1.3-100
- 21.1.3

* Wed Jun 02 2021 Phantom X <megaphantomx at hotmail dot com> - 21.1.2-100
- 21.1.2

* Wed May 19 2021 Phantom X <megaphantomx at hotmail dot com> - 21.1.1-100
- 21.1.1

* Wed May 05 2021 Phantom X <megaphantomx at hotmail dot com> - 21.1.0-100
- 21.1.0

* Sun May 02 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.3-102
- Fix mesa#3969

* Sat Apr 24 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.3-101
- Fix mesa#4691, patch from Arch

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.3-100
- 21.0.3

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.2-101
- Rawhide sync

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.2-100
- 21.0.2

* Sun Mar 28 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.1-101
- Rawhide sync

* Thu Mar 25 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.1-100
- 21.0.1

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 21.0.0-100
- 21.0.0

* Sun Mar 07 2021 Phantom X <megaphantomx at hotmail dot com> - 20.3.4-103
- More nine updates

* Fri Mar 05 2021 Phantom X <megaphantomx at hotmail dot com> - 20.3.4-102
- Add some iXit updates

* Fri Feb 26 2021 Phantom X - 20.3.4-101
- Upstream fixes

* Fri Jan 29 2021 Phantom X <megaphantomx at hotmail dot com> - 20.3.4-100
- 20.3.4

* Thu Jan 14 2021 Phantom X <megaphantomx at hotmail dot com> - 20.3.3-100
- 20.3.3

* Thu Dec 31 2020 Phantom X <megaphantomx at hotmail dot com> - 20.3.2-100
- 20.3.2

* Wed Dec 16 2020 Phantom X <megaphantomx at hotmail dot com> - 20.3.1-100
- 20.3.1

* Thu Dec 03 2020 Phantom X <megaphantomx at hotmail dot com> - 20.3.0-100
- 20.3.0
- Rawhide sync

* Tue Nov 24 2020 Phantom X <megaphantomx at hotmail dot com> - 20.2.3-100
- 20.2.3

* Sat Nov 07 2020 Phantom X <megaphantomx at hotmail dot com> - 20.2.2-100
- 20.2.2

* Wed Oct 14 2020 Phantom X <megaphantomx at hotmail dot com> - 20.2.1-100
- 20.2.1

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 20.2.0-100
- 20.2.0

* Wed Sep 16 2020 Phantom X <megaphantomx at hotmail dot com> - 20.1.8-100
- 20.1.8

* Wed Sep 02 2020 Phantom X <megaphantomx at hotmail dot com> - 20.1.7-100
- 20.1.7

* Wed Aug 19 2020 Phantom X <megaphantomx at hotmail dot com> - 20.1.6-100
- 20.1.6

* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 20.1.5-100
- 20.1.5

* Wed Jul 22 2020 Phantom X <megaphantomx at hotmail dot com> - 20.1.4-100
- 20.1.4

* Thu Jul 09 2020 Phantom X <megaphantomx at hotmail dot com> - 20.1.3-100
- 20.1.3

* Wed Jun 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.1.2-100
- 20.1.2

* Thu Jun 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.1.1-100
- 20.1.1

* Thu May 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.1.0-100
- 20.1.0

* Fri May 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.1.0~rc4-100
- 20.1.0-rc4

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.1.0~rc3-100
- 20.1.0-rc3
- Update iXit patchset

* Thu May 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.1.0~rc2-100
- 20.1.0-rc2
- Reenable LTO
- vulkan-device-select

* Thu Apr 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.1.0~rc1-100
- 20.1.0-rc1

* Thu Apr 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.6-100
- 20.0.6

* Wed Apr 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.5-100
- 20.0.5

* Fri Apr 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.4-100
- 20.0.4

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.3-100
- 20.0.3

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.2-100
- 20.0.2

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.1-101
- f32 sync

* Fri Mar 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.1-100
- 20.0.1

* Wed Feb 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.0-100
- 20.0.0

* Thu Feb 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.0~rc3-100
- 20.0.0-rc3

* Thu Feb 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.0~rc2-102
- Rawhide sync

* Tue Feb 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.0~rc2-101
- BR: ZSTD cache support

* Fri Feb 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.0~rc2-100
- 20.0.0-rc2
- vulkan-overlay

* Fri Jan 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.0.0~rc1-100
- 20.0.0-rc1

* Tue Jan 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 19.3.3-100
- 19.3.3

* Thu Jan 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 19.3.2-100
- 19.3.2

* Wed Dec 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.1-100
- 19.3.1

* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0-101
- Apply not upstreamed updates from iXit

* Thu Dec 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0-100
- 19.3.0

* Wed Dec 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0~rc6-101
- Enable zink driver
- Disable broken LTO
- Fix build with gnu++14 instead gnu++11

* Thu Dec 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0~rc6-100
- 19.3.0-rc6

* Thu Nov 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0~rc5-100
- 19.3.0-rc5

* Wed Nov 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0~rc4-100
- 19.3.0-rc4

* Wed Nov 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0~rc3-100
- 19.3.0-rc3

* Wed Nov 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.3.0~rc2-100
- 19.3.0-rc2
- Update file list for libglvnd 1.2
- LTO support borrowed from xxmitsu COPR

* Thu Oct 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.2.2-100
- 19.2.2

* Wed Oct 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.2.1-100
- 12.2.1

* Thu Sep 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.2.0-101
- Disk cache thread count patch

* Wed Sep 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.2.0-100
- 19.2.0
- Rawhide sync

* Tue Sep 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.7-100
- 19.1.7

* Tue Sep 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.6-100
- 19.1.6

* Fri Aug 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.5-100
- 19.1.5

* Wed Aug 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.4-100
- 19.1.4

* Tue Jul 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.3-100
- 19.1.3

* Tue Jul 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.2-100
- 19.1.2

* Tue Jun 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.1-100
- 19.1.1

* Tue Jun 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.1.0-100
- 19.1.0
- Rawhide sync

* Wed Jun 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.6-100
- 19.0.6

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.5-100
- 19.0.5

* Fri May 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.4-100
- 19.0.4

* Wed Apr 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.3-100
- 19.0.3

* Thu Apr 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-100
- 19.0.2

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.1-100
- 19.0.1

* Tue Mar 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.0-101
- -Db_ndebug=true

* Wed Mar 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.0.0-100
- 19.0.0
- Rawhide sync

* Mon Feb 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 18.3.4-100
- 18.3.4

* Thu Jan 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 18.3.3-100
- 18.3.3

* Thu Jan 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 18.3.2-100
- 18.3.2
- Rawhide sync

* Wed Dec 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.3.1-100
- 18.3.1

* Fri Dec 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.3.0-100
- 18.3.0
- Rawhide sync. meson, annotated build

* Wed Nov 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.6-100.chinfo
- 18.2.6

* Thu Nov 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.5-100.chinfo
- 18.2.5

* Fri Nov 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.4-101.chinfo
- Rebuild for rhbz#1645400 (gcc 8.2.1-4 miscompiles bitset code in mesa)

* Wed Oct 31 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.4-100.chinfo
- 18.2.4

* Fri Oct 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.3-100.chinfo
- 18.2.3

* Fri Oct 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.2-100.chinfo
- 18.2.2

* Fri Sep 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.1-100.chinfo
- 18.2.1

* Fri Sep 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.2.0-100.chinfo
- 18.2.0
- Rawhide sync

* Fri Aug 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.7-100.chinfo
- 18.1.7

* Mon Aug 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.6-100.chinfo
- 18.1.6

* Fri Jul 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.5-100.chinfo
- 18.1.5

* Fri Jul 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.4-100.chinfo
- 18.1.4

* Fri Jun 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.3-100.chinfo
- 18.1.3
- Rawhide sync

* Sun Jun 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.2-101.chinfo
- Rawhide sync

* Fri Jun 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.2-100.chinfo
- 18.1.2

* Fri Jun 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.1-100.chinfo
- 18.1.1

* Wed May 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-101.chinfo
- Updated patch to fix xserver 1.20 freezing

* Fri May 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.1.0-100.chinfo
- 18.1.0

* Thu May 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.0.4-100.chinfo
- 18.0.4

* Sun May 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.0.3-101.chinfo
- Try fix hangs with xserver 1.20

* Mon May 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.0.3-100.chinfo
- 18.0.3

* Sat Apr 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.0.2-100.chinfo
- 18.0.2
- f28 sync

* Wed Apr 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.0.1-100.chinfo
- 18.0.1

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 18.0.0-100.chinfo
- 18.0.0
- f28 sync

* Sun Mar 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 17.3.6-100.chinfo
- Backport fix

* Tue Feb 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 17.3.6-0
- 17.3.6
- f27 sync

* Mon Feb 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 17.3.5-0
- 17.3.5

* Thu Feb 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 17.3.4-0
- 17.3.4
- Fedora sync

* Fri Jan 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 17.3.3-0
- 17.3.3

* Tue Jan 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 17.3.2-0
- 17.3.2

* Thu Dec 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 17.3.1-0
- 17.3.1

* Fri Dec 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 17.3.0-0
- 17.3.0

* Mon Nov 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 17.2.6-0
- 17.2.6

* Fri Nov 10 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 17.2.4-2
- Sanitize tarball

* Tue Oct 31 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.4-1
- Update to 17.2.4 GA

* Mon Oct 23 2017 Tom Stellard <tstellar@redhat.com> - 17.2.3-2
- Rebuild for LLVM 5.0.0

* Thu Oct 19 2017 Gwyn Ciesla <limburgher@gmail.com> - 17.2.3-1
- 17.2.3, bugfix release.

* Wed Oct 11 2017 Peter Robinson <pbrobinson@fedoraproject.org> - 17.2.2-4
- Fix for vc4/Raspberry Pi

* Mon Oct 09 2017 Dave Airlie <airlied@redhat.com> - 17.2.2-3
- enable vulkan on 32-bit x86

* Tue Oct 03 2017 Adam Jackson <ajax@redhat.com> - 17.2.2-2
- Backport S3TC support from master

* Tue Oct  3 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.2-1
- Update to 17.2.2 GA

* Wed Sep 20 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.1-1
- Update to 17.2.1 GA

* Mon Sep 11 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.0-2
- Add upstream patch for glibc xlocale.h change (fdo bz 102454)

* Tue Sep  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.0-1
- Update to 17.2.0 GA

* Thu Aug 31 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.0-0.3.rc6
- Update to 17.2.0-rc6

* Tue Aug 22 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.0-0.2.rc5
- Update to 17.2.0-rc5

* Sun Aug 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.2.0-0.1.rc4
- Update to 17.2.0-rc4

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 17.1.5-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 17.1.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 7.1.5-1
- Update to 17.1.5

* Thu Jul 13 2017 Adam Jackson <ajax@redhat.com>
- Stop replacing eglext.h, we're up to date again

* Sat Jul  1 2017 Peter Robinson <pbrobinson@fedoraproject.org> 7.1.4-1
- Update to 17.1.4

* Mon Jun 19 2017 Peter Robinson <pbrobinson@fedoraproject.org> 7.1.3-2
- Fixes and perf improvements for vc4

* Mon Jun 19 2017 Peter Robinson <pbrobinson@fedoraproject.org> 7.1.3-1
- Update to 17.1.3

* Wed Jun 14 2017 Peter Robinson <pbrobinson@fedoraproject.org> 7.1.2-2
- Some etnaviv fixes

* Mon Jun  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 7.1.2-1
- Update to 17.1.2

* Mon Jun 05 2017 Adam Jackson <ajax@redhat.com> - 17.1.1-2
- Disable BGRA8 images on Fermi

* Thu May 25 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.1.1-1
- Update to 17.1.1

* Thu May 11 2017 Dave Airlie <airlied@redhat.com> - 17.1.0-1
- Update to 17.1.0

* Tue May  9 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.1.0-0.4.rc4
- Update to 17.1.0-rc4

* Fri Apr 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.1.0-0.3.rc2
- Enable renderonly support for i.MX SoC (rhbz #1424714)

* Mon Apr 24 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.1.0-0.2.rc2
- Update to 17.1.0-rc2

* Tue Apr 18 2017 Igor Gnatenko <ignatenko@redhat.com> - 17.1.0-0.1.rc1
- Update to 17.1.0-rc1

* Sun Apr 02 2017 Igor Gnatenko <ignatenko@redhat.com> - 17.0.3-1
- Update to 17.0.3

* Fri Mar 24 2017 Igor Gnatenko <ignatenko@redhat.com> - 17.0.2-2
- Rebuild for LLVM4

* Mon Mar 20 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.2-1
- Update to 17.0.2

* Mon Mar 20 2017 Hans de Goede <hdegoede@redhat.com> - 17.0.1-3
- Fix glXGetDriverConfig not working with glvnd (rhbz#1429894)
- Fix indirect rendering, add libGLX_indirect.so.0 symlink (rhbz#1427174)

* Tue Mar 14 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.1-2
- Rebuild for aarch64 llvmpipe fix (rhbz 1429050)

* Sun Mar 05 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 17.0.1-1
- Update to 17.0.1

* Mon Feb 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.0-1
- 17.0.0 GA

* Mon Feb  6 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.0-0.6.rc3
- Update to 17.0.0-rc3

* Mon Feb  6 2017 Hans de Goede <hdegoede@redhat.com> - 17.0.0-0.5.rc2
- Fix GLX_SGIX_fbconfig extension dispatching with glvnd, this fixes games such
  as "The Binding of Isaac: Rebirth" and "Crypt of the NecroDancer" from Steam

* Thu Feb  2 2017 Hans de Goede <hdegoede@redhat.com> - 17.0.0-0.4.rc2
- Update eglext.h to 20161230 version this brings in some new defines needed
  by some apps / libraries

* Sat Jan 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.0-0.3.rc2
- Update to 17.0.0-rc2

* Sat Jan 21 2017 Peter Robinson <pbrobinson@fedoraproject.org> 17.0.0-0.2.rc1
- Enable etnaviv gallium driver

* Fri Jan 20 2017 Igor Gnatenko <ignatenko@redhat.com> - 17.0.0-0.rc1
- Update to 17.0.0-rc1

* Tue Jan 17 2017 Hans de Goede <hdegoede@redhat.com> - 13.0.3-3
- Enable libglvnd support (rhbz#1413579)

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 13.0.3-2
- Add valgrind BuildRequires to have valgrind support

* Fri Jan  6 2017 Peter Robinson <pbrobinson@fedoraproject.org> 13.0.3-1
- 13.0.3 GA

* Mon Dec 12 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 13.0.2-2
- Use nettle for sha1

* Tue Nov 29 2016 Peter Robinson <pbrobinson@fedoraproject.org> 13.0.2-1
- 13.0.2 GA

* Tue Nov 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> 13.0.1-1
- 13.0.1 GA

* Wed Nov  2 2016 Peter Robinson <pbrobinson@fedoraproject.org> 13.0.0-3
- Don't ship duplicate vulkan devel headers

* Wed Nov  2 2016 Peter Robinson <pbrobinson@fedoraproject.org> 13.0.0-2
- Add options for enabling vulkan components
- Enable intel/radeon vulkan drivers

* Wed Nov  2 2016 Peter Robinson <pbrobinson@fedoraproject.org> 13.0.0-1
- 13.0.0 GA

* Tue Nov 01 2016 Dave Airlie <airlied@redhat.com> - 13.0.0-0.3.rc2
- rebuild for llvm 3.9

* Mon Oct 24 2016 Peter Robinson <pbrobinson@fedoraproject.org> 13.0.0-0.2.rc2
- 13.0.0-rc2

* Thu Oct 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 13.0.0-0.1.rc1
- 13.0.0-rc1

* Tue Oct 11 2016 Hans de Goede <hdegoede@redhat.com> - 12.0.3-2
- Add 2 patches from upstream to fix DRI3 vaapi crashes (rhbz1309446, fdo71759)

* Sun Sep 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 12.0.3-1
- 12.0.3

* Mon Sep  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 12.0.2-1
- 12.0.2

* Mon Sep  5 2016 Hans de Goede <hdegoede@redhat.com> - 12.0.1-7
- Fix PRIME fd leak

* Tue Aug 23 2016 Adam Jackson <ajax@redhat.com> - 12.0.1-6
- Remove BuildRequires: xorg-x11-server-devel

* Mon Aug 15 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.1-5
- Fix broken deps with OpenCL

* Sun Aug 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.1-4
- Fix broken deps

* Sun Aug 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.1-3
- Slightly refactor spec
- Drop virtual provides for OCL

* Tue Jul 19 2016 Orion Poplawski <orion@cora.nwra.com> - 12.0.1-2
- Add missing %%{?_isa} to requires in some devel sub-packages (bug #1138463)

* Sun Jul 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.1-1
- 12.0.1

* Fri Jul 08 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.0-1
- 12.0.0

* Wed Jun 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.0-0.3.rc4
- 12.0.0-rc4

* Mon Jun 20 2016 Adam Jackson <ajax@redhat.com> - 12.0.0-0.3.rc3
- Fix packaging error on s390*

* Mon Jun 20 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.0-0.2.rc3
- 12.0.0-rc3

* Tue Jun 14 2016 Dominik Mierzejewski <rpm@greysector.net> - 12.0.0-0.2.rc2
- add missing dependency for /etc/OpenCL/vendors ownership (RHBZ #1265948)

* Tue Jun 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.0-0.1.rc2
- 12.0.0-rc2

* Wed Jun 01 2016 Igor Gnatenko <ignatenko@redhat.com> - 12.0.0-0.1.rc1
- 12.0.0-rc1

* Sun May 01 2016 Igor Gnatenko <ignatenko@redhat.com> - 11.3.0-0.4.gitcbcd7b6
- cbcd7b6

* Thu Apr 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 11.3.0-0.3.git171a570
- 171a570

* Fri Apr 08 2016 Björn Esser <fedora@besser82.io> - 11.3.0-0.2.gitea2bff1
- add virtual Provides for ocl-icd (RHBZ #1317602)

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.3.0-0.1.gitea2bff1
- 11.3.0 (gitea2bff1)
- Add SWR state-tracker (but disable because build is broken)
- Use gallium-osmesa instead of classic osmesa (RHBZ #1305588)
- Remove very old changelogs

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.2.0-0.1.rc3.20160320
- Update to 11.2.0-rc3

* Fri Feb 19 2016 Dave Airlie <airlied@redhat.com> 11.2.0-0.devel.11
- rebuild against llvm 3.8.0

* Fri Feb 12 2016 Dave Airlie <airlied@redhat.com> 11.2.0-0.devel.10
- rebuild against new llvm packages

* Thu Feb 11 2016 Adam Jackson <ajax@redhat.com> 11.2.0-0.devel.9
- Fix OpenCL-enabled FTBFS by not forcing clang search path to /usr/lib

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.0-0.devel.8.24ea81a.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Adam Jackson <ajax@redhat.com> 11.2.0-0.devel.8
- Rebuild for llvm 3.7.1 library split

* Sun Jan 24 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.2.0-0.devel.7.24ea81a
- 24ea81a

* Thu Jan 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 11.2.0-0.devel.6.5e3edd4
- OpenCL now supported on aarch64

* Sun Jan 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.2.0-0.devel.5.5e3edd4
- 5e3edd4

* Thu Jan 07 2016 Adam Jackson <ajax@redhat.com>
- Mangle libtool even harder to get -static-libstdc++ to work

* Tue Dec 29 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.2.0-0.devel.3.70d8dbc
- 70d8dbc

* Wed Dec 02 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.2.0-0.devel.2.56aff6b
- 56aff6b

* Sun Nov 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.2.0-0.devel.1.86fc97d
- 86fc97d

* Thu Nov 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.13.5ae37ae
- 5ae37ae

* Thu Nov 05 2015 Adam Jackson <ajax@redhat.com> 11.1.0-0.devel.12.3994ef5
- Link with -static-libstdc++ to work around Steam bundling its own copy

* Fri Oct 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.11.3994ef5
- 3994ef5
- Enable VirGL driver

* Thu Oct 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.10.7182498
- 7182498
- Disable SWR rasterizer

* Wed Oct 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.9.4a168ad
- Enable experimental SWR rasterizer

* Wed Oct 14 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.8.4a168ad
- 4a168ad

* Wed Oct 07 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.7.47d1199
- 47d1199

* Sat Sep 26 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.6.9932142
- 9932142

* Wed Sep 16 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.5.47e18a5
- 47e18a5
- Rebuild against llvm 3.7

* Sun Sep 13 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 11.1.0-0.devel.4.d6fbcf6
- d6fbcf6

* Thu Sep 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 11.1.0-0.devel.3.60aea30
- Add brw_meta_fast_clear crash workaround patch (#1259443, fdo#86281)

* Wed Sep 02 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.1.0-0.devel.2.60aea30
- 60aea30

* Mon Aug 24 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.1.0-0.devel.1.4e5752e
- 4e5752e

* Sun Aug 09 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.0.0-0.devel.2.21ccdbd
- 21ccdbd
- add surfaceless EGL platform (RHBZ #1251747)

* Sat Aug 01 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 11.0.0-0.devel.1.6f2d889
- Update to 11.0.0

* Tue Jul 14 2015 Peter Robinson <pbrobinson@fedoraproject.org> 10.7.0-0.devel.4.ea633db
- Use %%license
- Minor spec cleanups

* Tue Jul 14 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.7.0-0.devel.3.ea633db
- ea633db

* Tue Jul 07 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.7.0-0.devel.2.8787141
- Drop unecessary make for s390

* Mon Jun 22 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.7.0-0.devel.1.8787141
- 8787141

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.6.0-0.devel.7.5a55f68.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.6.0-0.devel.7.5a55f68
- add git to BR everywhere

* Sun May 17 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.6.0-0.devel.6.5a55f68
- 5a55f68

* Thu May 07 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.6.0-0.devel.5.51e3453
- 51e3453

* Mon Apr 20 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.6.0-0.devel.4.c1485f4
- c1485f4

* Thu Apr 09 2015 Adam Jackson <ajax@redhat.com> 10.6.0-0.devel.3
- F23 rebuild against llvm 3.6.0

* Fri Feb 27 2015 Rob Clark <rclark@redhat.com - 10.6.0-0.devel.2.f80af89
- enable vc4 on arm

* Mon Feb 23 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.6.0-0.devel.1.f80af89
- f80af89

* Wed Feb 18 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-1.20150218
- 10.5.0

* Fri Jan 02 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.32.6171131
- 6171131

* Fri Jan 02 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.31.c3260f8
- c3260f8

* Fri Jan 02 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.30.290553b
- 290553b

* Thu Jan 01 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.28.b77eaaf
- b77eaaf

* Thu Jan 01 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.26.c633528
- c633528

* Thu Jan 01 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.25.a6f6d61
- a6f6d61

* Wed Dec 31 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.23.be0311c
- be0311c

* Wed Dec 31 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.21.609c3e5
- 609c3e5

* Wed Dec 31 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.19.3ba57ba
- 3ba57ba

* Tue Dec 30 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.17.64dcb2b
- 64dcb2b

* Mon Dec 29 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.15.6c18279
- 6c18279

* Sat Dec 27 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.13.0c7f895
- 0c7f895

* Fri Dec 26 2014 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.5.0-0.devel.11.cb5a372
- cb5a372

* Sun Dec 21 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.10.git0d7f4c8
- enable ilo gallium driver

* Fri Dec 19 2014 Dan Horák <dan[at]danny.cz> 10.5.0-0.devel.9
- Sync with_{vaapi,vdpau,nine} settings with F21

* Thu Dec 18 2014 Adam Jackson <ajax@redhat.com> 10.5.0-0.devel.8
- Sync ppc build config with F21

* Wed Dec 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.7.git0d7f4c8
- fix requirements for d3d

* Sun Dec 14 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.6.git0d7f4c8
- 0d7f4c8

* Sun Dec 14 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.5.git29c7cf2
- Enable VA state-tracker
- Enable Nine state-tracker (Direct3D9 API)

* Thu Dec 11 2014 Adam Jackson <ajax@redhat.com> 10.5.0-0.devel.4
- Restore hardware drivers on ppc64{,le}

* Tue Dec 02 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.3.git29c7cf2
- 29c7cf2

* Sat Nov 22 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.2.git3d9c1a9
- 3d9c1a9

* Wed Nov 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.5.0-0.devel.1.git9460cd3
- 9460cd3

* Mon Nov 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.8.gitf3b709c
- f3b709c

* Tue Oct 28 2014  10.4-0.devel.7.git1a17098
- rebuild for llvm

* Mon Oct 27 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.6.git1a17098
- 1a17098

* Sat Sep 27 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.5.gitc3f17bb
- c3f17bb18f597d7f606805ae94363dae7fd51582

* Sat Sep 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.4.git1f184bc
- apply patch for bigendian from karsten
- fix ppc filelist from karsten

* Sat Sep 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.3.git1f184bc
- 1f184bc114143acbcea373184260da777b6c6be1 commit

* Thu Aug 28 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.2.1.80771e47b6c1e47ab55f17311e1d4e227a9eb3d8
- add swrast to dri driver list

* Wed Aug 27 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.2.80771e47b6c1e47ab55f17311e1d4e227a9eb3d8
- 80771e47b6c1e47ab55f17311e1d4e227a9eb3d8 commit

* Sat Aug 23 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.4-0.devel.1.c2867f5b3626157379ef0d4d5bcaf5180ca0ec1f
- 10.4 c2867f5b3626157379ef0d4d5bcaf5180ca0ec1f

* Fri Aug 22 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.rc1.1.e7f2f2dea5acdbd1a12ed88914e64a38a97432f0
- e7f2f2dea5acdbd1a12ed88914e64a38a97432f0 commit

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.3-0.devel.2.c40d7d6d948912a4d51cbf8f0854cf2ebe916636.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.devel.2.c40d7d6d948912a4d51cbf8f0854cf2ebe916636
- c40d7d6d948912a4d51cbf8f0854cf2ebe916636 commit

* Fri Jul 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.devel.1.f381c27c548aa28b003c8e188f5d627ab4105f76
- Rebase to 'master' branch (f381c27c548aa28b003c8e188f5d627ab4105f76 commit)

* Fri Jul 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.3-1.20140711
- 10.2.3 upstream release

* Mon Jul  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 10.2.2-4.20140625
- Build aarch64 options the same as ARMv7
- Fix PPC conditionals

* Fri Jul 04 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.2-3.20140625
- Fix up intelInitScreen2 for DRI3 (RHBZ #1115323) (patch from drago01)

* Fri Jun 27 2014 Dave Airlie <airlied@redhat.com> 10.2.2-2.20140625
- add dri3 gnome-shell startup fix from Jasper.

* Wed Jun 25 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.2-1.20140625
- 10.2.2 upstream release

* Wed Jun 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.1-2.20140608
- drop radeonsi llvm hack

* Sun Jun 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.1-1.20140608
- 10.2.1 upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-0.11.rc5.20140531
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Dan Horák <dan[at]danny.cz> - 10.2-0.10.rc5.20140531
- fix build without hardware drivers

* Sat May 31 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.9.rc5.20140531
- 10.2-rc5 upstream release

* Wed May 28 2014 Brent Baude <baude@us.ibm.com> - 10.2-0.8.rc4.20140524
- Removing ppc64le arch from with_llvm

* Wed May 28 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.7.rc4.20140524
- i915: add a missing NULL pointer check (RHBZ #1100967)

* Sat May 24 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.6.rc4.20140524
- 10.2-rc4 upstream release
- add back updated radeonsi hack for LLVM

* Sat May 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.5.rc3.20140517
- 10.2-rc3 upstream release

* Sat May 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.4.rc2.20140510
- 10.2-rc2 upstream release
- drop radeonsi hack for LLVM

* Tue May 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.3.rc1.20140505
- Move gallium-pipe to the correct sub-package (RHBZ #1094588) (kwizart)
- Move egl_gallium.so to the correct location (RHBZ #1094588) (kwizart)
- Switch from with to enable for llvm shared libs (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.2.rc1.20140505
- Enable gallium-egl (needed by freedreeno) (RHBZ #1094199) (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.1.rc1.20140505
- Enable omx on x86 and arm (RHBZ #1094199) (kwizart)
- Split _with_xa from _with_vmware (RHBZ #1094199) (kwizart)
- Add _with_xa when arch is arm and _with_freedreeno (RHBZ #1094199) (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.rc1.20140505
- 10.2-rc1 upstream release

* Wed Apr 30 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-3.20140430
- Update to today snapshot
- apply as downstream patches for reporting GPU max frequency on r600 (FD.o #73511)

* Sat Apr 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-2.20140419
- fix buildrequires llvm 3.4-5 to 3.4-6, because 3.4-5 is not available for F20

* Sat Apr 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-1.20140419
- 10.1.1 upstream release

* Tue Apr 15 2014 Adam Jackson <ajax@redhat.com> 10.1-6.20140305
- Disable DRI3 in F20, it requires libxcb bits we haven't backported.

* Wed Mar 26 2014 Adam Jackson <ajax@redhat.com> 10.1-5.20140305
- Initial ppc64le enablement (no hardware drivers or vdpau yet)

* Fri Mar 21 2014 Adam Jackson <ajax@redhat.com> 10.1-4.20140305
- mesa: Don't optimize out glClear if drawbuffer size is 0x0 (fdo #75797)

* Wed Mar 19 2014 Dave Airlie <airlied@redhat.com> 10.1-3.20140305
- rebuild against backported llvm 3.4-5 for radeonsi GL 3.3 support.

* Wed Mar 12 2014 Dave Airlie <airlied@redhat.com> 10.1-2.20140305
- disable r600 llvm compiler (upstream advice)

* Wed Mar 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-1.20140305
- mesa: Bump version to 10.1 (final) (Ian Romanick)
- glx/dri2: fix build failure on HURD (Julien Cristau)
- i965: Validate (and resolve) all the bound textures. (Chris Forbes)
- i965: Widen sampler key bitfields for 32 samplers (Chris Forbes)

* Sat Mar 01 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc3.20140301
- 10.1-rc3

* Tue Feb 25 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc2.20140225
- really 10.1-rc2

* Sat Feb 22 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc2.20140222
- 10.1-rc2

* Sat Feb 08 2014 Adel Gadllah <adel.gadllah@gmail.com> - 10.1-0.rc1.20140208
- 10.1rc1
- Drop upstreamed patches

* Thu Feb 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.0.3-1.20140206
- 10.0.3 upstream release

* Tue Feb 04 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-6.20140118
- Fix accidentally inverted logic that meant radeonsi_dri.so went missing
  on all architectures instead of just ppc and s390. Sorry!

* Sun Feb 02 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-5.20140118
- Fix a thinko in previous commit wrt libdrm_nouveau2.

* Sun Feb 02 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-4.20140118
- Fix up building drivers on AArch64, enable LLVM there.
- Eliminate some F17 cruft from the spec, since we don't support it anymore.
- Conditionalize with_radeonsi on with_llvm instead of ppc,s390 && >F-17.
- Conditionalize libvdpau_radeonsi.so.1* on with_radeonsi instead of simply
  with_llvm to fix a build failure on AArch64.

* Sun Jan 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.0.2-3.20140118
- Enable OpenCL (RHBZ #887628)
- Enable r600 llvm compiler (RHBZ #1055098)
