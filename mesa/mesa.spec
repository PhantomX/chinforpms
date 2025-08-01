# Inconsistent
%global _lto_cflags %{nil}

%ifnarch s390x
%global with_hardware 1
%global with_radeonsi 1
%global with_vmware 1
%global with_vulkan_hw 1
%global with_vdpau 1
%global with_va 1
%if !0%{?rhel}
%global with_r300 1
%global with_r600 1
%global with_nine 1
%if 0%{?with_vulkan_hw}
%global with_nvk %{with_vulkan_hw}
%endif
%global with_opencl 1
%endif
%global base_vulkan %{?with_vulkan_hw:,amd}%{!?with_vulkan_hw:%{nil}}
%endif

%ifnarch %{ix86}
%if !0%{?rhel}
%global with_teflon 1
%endif
%endif

%ifarch %{ix86} x86_64
%global with_crocus 1
%global with_i915   1
%global with_iris   1
%global with_xa     1
%global with_intel_clc 1
%global intel_platform_vulkan %{?with_vulkan_hw:,intel,intel_hasvk}%{!?with_vulkan_hw:%{nil}}
%endif
%ifarch x86_64
%if !0%{?with_vulkan_hw}
%global with_intel_vk_rt 1
%endif
%endif

%ifarch aarch64 x86_64 %{ix86}
%global with_kmsro     1
%if !0%{?rhel}
%global with_lima      1
%global with_vc4       1
%global with_etnaviv   1
%global with_tegra     1
%endif
%global with_asahi     1
%global with_freedreno 1
%global with_panfrost  1
%global with_v3d       1
%global with_xa        1
%if 0%{?with_asahi}
%global asahi_platform_vulkan %{?with_vulkan_hw:,asahi}%{!?with_vulkan_hw:%{nil}}
%endif
%global extra_platform_vulkan %{?with_vulkan_hw:,broadcom,freedreno,panfrost,imagination-experimental}%{!?with_vulkan_hw:%{nil}}
%endif

%if !0%{?rhel}
%global with_libunwind 1
%global with_lmsensors 1
%endif

%ifarch %{valgrind_arches}
%bcond valgrind 1
%else
%bcond valgrind 0
%endif

# Enable patent encumbered video codecs acceleration
%bcond videocodecs 0

# Set to build with versioned LLVM packages
%dnl %global llvm_pkgver 16

%global vulkan_drivers swrast,virtio%{?base_vulkan}%{?intel_platform_vulkan}%{?asahi_platform_vulkan}%{?extra_platform_vulkan}%{?with_nvk:,nouveau}
%global vulkan_layers device-select,overlay

%global commit 94ed71dad161edb01ee7acaae02e555af3e5dcac
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20231012
%bcond snapshot 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://gitlab.freedesktop.org/mesa/mesa
%global ixit_url  https://github.com/iXit/Mesa-3D/commit

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           mesa
Summary:        Mesa graphics libraries
# If rc, use "~" instead "-", as ~rc1
Version:        25.1.7
Release:        100%{?dist}

License:        MIT AND BSD-3-Clause AND SGI-B-2.0
URL:            http://www.mesa3d.org

%if %{with snapshot}
Source0:        %{vc_url}/-/archive/%{commit}/%{name}-%{commit}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        https://archive.mesa3d.org/%{name}-%{ver}.tar.xz
%endif

# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source1:        Mesa-MLAA-License-Clarification-Email.txt


Patch10:        gnome-shell-glthread-disable.patch

Patch499:       mesa-20.1.1-fix-opencl.patch

Patch500:       mesa-23.1-x86_32-llvm-detection.patch

Patch1000:      0001-Versioned-LLVM-package-fix.patch

BuildRequires:  meson >= 1.3.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext


%if 0%{?with_hardware}
BuildRequires:  kernel-headers
%endif
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.122
%if 0%{?with_libunwind}
BuildRequires:  pkgconfig(libunwind)
%endif
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.34
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
%if 0%{?with_lmsensors}
BuildRequires:  lm_sensors-devel
%endif
%if 0%{?with_vdpau}
BuildRequires:  pkgconfig(vdpau) >= 1.1
%endif
%if 0%{?with_va}
BuildRequires:  pkgconfig(libva) >= 1.8.0
%endif
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libglvnd) >= 1.3.2
BuildRequires:  llvm%{?llvm_pkgver}-devel >= 15.0.0
%if 0%{?with_teflon}
BuildRequires:  flatbuffers-devel
BuildRequires:  flatbuffers-compiler
BuildRequires:  xtensor-devel
%endif
%if 0%{?with_opencl} || 0%{?with_nvk} || 0%{?with_intel_clc} || 0%{?with_asahi} || 0%{?with_panfrost}
BuildRequires:  clang%{?llvm_pkgver}-devel
BuildRequires:  pkgconfig(libclc)
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  pkgconfig(LLVMSPIRVLib)
BuildRequires:  spirv-llvm-translator%{?llvm_pkgver}-devel
%endif
%if 0%{?with_opencl} || 0%{?with_nvk}
BuildRequires:  bindgen
BuildRequires:  rust-packaging
%endif
%if 0%{?with_nvk}
BuildRequires:  cbindgen
BuildRequires:  (crate(paste) >= 1.0.14 with crate(paste) < 2)
BuildRequires:  (crate(proc-macro2) >= 1.0.56 with crate(proc-macro2) < 2)
BuildRequires:  (crate(quote) >= 1.0.25 with crate(quote) < 2)
BuildRequires:  (crate(syn/clone-impls) >= 2.0.15 with crate(syn/clone-impls) < 3)
BuildRequires:  (crate(unicode-ident) >= 1.0.6 with crate(unicode-ident) < 2)
%endif
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
%if 0%{?with_intel_clc}
BuildRequires:  python3-ply
%endif
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyyaml
BuildRequires:  vulkan-headers
BuildRequires:  glslang
%if 0%{?with_vulkan_hw}
BuildRequires:  pkgconfig(vulkan)
%endif


%description
%{summary}.

%package filesystem
Summary:        Mesa driver filesystem
Provides:       mesa-dri-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-omx-drivers < %{?epoch:%{epoch}:}%{version}-%{release}

%description filesystem
%{summary}.

%package libGL
Summary:        Mesa libGL runtime libraries
Requires:       libglvnd-glx%{?_isa} >= 1:1.3.2
Requires:       %{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libOSMesa < 25.1.0~rc2-1

%description libGL
%{summary}.

%package libGL-devel
Summary:        Mesa libGL development package
Requires:       (%{name}-libGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} if %{name}-libGL%{?_isa})
Requires:       libglvnd-devel%{?_isa} >= 1:1.3.2
Provides:       libGL-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libGL-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends:     gl-manpages
Obsoletes:      %{name}-libOSMesa-devel < 25.1.0~rc2-1

%description libGL-devel
%{summary}.

%package libEGL
Summary:        Mesa libEGL runtime libraries
Requires:       libglvnd-egl%{?_isa} >= 1:1.3.2
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libEGL
%{summary}.

%package libEGL-devel
Summary:        Mesa libEGL development package
Requires:       (%{name}-libEGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} if %{name}-libEGL%{?_isa})
Requires:       libglvnd-devel%{?_isa} >= 1:1.3.2
Requires:       %{name}-khr-devel%{?_isa}
Provides:       libEGL-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libEGL-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libEGL-devel
%{summary}.

%package dri-drivers
Summary:        Mesa-based DRI drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?with_va}
Recommends:     %{name}-va-drivers%{?_isa}
%endif
Obsoletes:      %{name}-libglapi < 25.0.0~rc2-1

%description dri-drivers
%{summary}.

%if 0%{?with_va}
%package        va-drivers
Summary:        Mesa-based VA-API video acceleration drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description va-drivers
%{summary}.
%endif

%if 0%{?with_vdpau}
%package        vdpau-drivers
Summary:        Mesa-based VDPAU drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description vdpau-drivers
%{summary}.
%endif

%package libgbm
Summary:        Mesa gbm runtime library
Provides:       libgbm = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends:     %{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# If mesa-dri-drivers are installed, they must match in version. This is here to prevent using
# older mesa-dri-drivers together with a newer mesa-libgbm and its dependants.
# See https://bugzilla.redhat.com/show_bug.cgi?id=2193135 .
Requires:       (%{name}-dri-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} if %{name}-dri-drivers%{?_isa})

%description libgbm
%{summary}.

%package libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libgbm-devel
%{summary}.

%if 0%{?with_xa}
%package libxatracker
Summary:        Mesa XA state tracker
Provides:       libxatracker = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libxatracker%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libxatracker
%{summary}.

%package libxatracker-devel
Summary:        Mesa XA state tracker development package
Requires:       %{name}-libxatracker%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libxatracker-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libxatracker-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libxatracker-devel
%{summary}.
%endif

%if 0%{?with_opencl}
%package libOpenCL
Summary:        Mesa OpenCL runtime library
Requires:       (ocl-icd%{?_isa} or OpenCL-ICD-Loader%{?_isa})
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

%if 0%{?with_teflon}
%package libTeflon
Summary:        Mesa TensorFlow Lite delegate

%description libTeflon
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
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-vulkan-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description vulkan-drivers
The drivers with support for the Vulkan API.

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
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -N -p1
%autopatch -M 999 -p1

%if 0%{?llvm_pkgver}
%patch -P 1000 -p1
sed \
  -e 's|_RPM_CLANG_INC_|%{_libdir}/llvm%{?llvm_pkgver}/lib/clang/%{?llvm_pkgver}/include|g' \
  -i src/gallium/frontends/rusticl/meson.build
%endif

cp %{SOURCE1} docs/

%py3_shebang_fix \
  src/vulkan/overlay-layer/mesa-overlay-control.py

%build
# ensure standard Rust compiler flags are set
export RUSTFLAGS="%build_rustflags"

%if 0%{?with_nvk}
export MESON_PACKAGE_CACHE_DIR="%{cargo_registry}/"
# So... Meson can't actually find them without tweaks
%define inst_crate_nameversion() %(basename %{cargo_registry}/%{1}-*)
%define rewrite_wrap_file() sed -e "/source.*/d" -e "s/%{1}-.*/%{inst_crate_nameversion %{1}}/" -i subprojects/%{1}.wrap

%rewrite_wrap_file proc-macro2
%rewrite_wrap_file quote
%rewrite_wrap_file syn
%rewrite_wrap_file unicode-ident
%rewrite_wrap_file paste
%endif

%meson \
  -Dplatforms=x11,wayland \
%if 0%{?with_hardware}
  -Dgallium-drivers=llvmpipe,virgl,nouveau%{?with_r300:,r300}%{?with_crocus:,crocus}%{?with_i915:,i915}%{?with_iris:,iris}%{?with_vmware:,svga}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600}%{?with_asahi:,asahi}%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_v3d:,v3d}%{?with_lima:,lima}%{?with_panfrost:,panfrost}%{?with_vulkan_hw:,zink} \
%else
  -Dgallium-drivers=llvmpipe,virgl \
%endif
  -Dgallium-vdpau=%{?with_vdpau:enabled}%{!?with_vdpau:disabled} \
  -Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
  -Dgallium-xa=%{?with_xa:enabled}%{!?with_xa:disabled} \
  -Dgallium-nine=%{?with_nine:true}%{!?with_nine:false} \
  -Dteflon=%{?with_teflon:true}%{!?with_teflon:false} \
%if 0%{?with_opencl}
  -Dgallium-rusticl=true \
  -Dgallium-opencl=disabled \
%endif 
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dvulkan-layers=%{?vulkan_layers} \
%if 0%{?with_videocodecs}
  -Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
%endif
  -Dshared-glapi=enabled \
  -Dgles1=enabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
  -Dglvnd=enabled \
%if 0%{?with_intel_clc}
  -Dintel-clc=enabled \
%endif
  -Dintel-rt=%{?with_intel_vk_rt:enabled}%{!?with_intel_vk_rt:disabled} \
  -Dmicrosoft-clc=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Db_ndebug=true \
  -Dbuild-tests=false \
%if !0%{?with_libunwind}
  -Dlibunwind=disabled \
%endif
%if !0%{?with_lmsensors}
  -Dlmsensors=disabled \
%endif
  -Dandroid-libbacktrace=disabled \
%ifarch %{ix86}
  -Dglx-read-only-text=true \
%endif
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
for i in libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd


%files filesystem
%doc docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%dir %{_datadir}/drirc.d

%files libGL
%{_libdir}/libGLX_mesa.so.0*
%{_libdir}/libGLX_system.so.0*
%files libGL-devel
%dir %{_includedir}/GL
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc

%files libEGL
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libEGL_mesa.so.0*
%files libEGL-devel
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext_angle.h
%{_includedir}/EGL/eglmesaext.h

%files libgbm
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*
%files libgbm-devel
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_includedir}/gbm_backend_abi.h
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

%if 0%{?with_teflon}
%files libTeflon
%{_libdir}/libteflon.so
%endif

%if 0%{?with_opencl}
%files libOpenCL
%{_libdir}/libRusticlOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/rusticl.icd

%files libOpenCL-devel
%{_libdir}/libRusticlOpenCL.so
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
%{_datadir}/drirc.d/00-mesa-defaults.conf
%{_libdir}/libgallium-*.so
%{_libdir}/gbm/dri_gbm.so
%{_libdir}/dri/kms_swrast_dri.so
%{_libdir}/dri/libdril_dri.so
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
%{_libdir}/dri/i915_dri.so
%{_libdir}/dri/iris_dri.so
%endif
%ifarch aarch64 x86_64 %{ix86}
%if 0%{?with_asahi}
%{_libdir}/dri/apple_dri.so
%{_libdir}/dri/asahi_dri.so
%endif
%{_libdir}/dri/ingenic-drm_dri.so
%{_libdir}/dri/imx-drm_dri.so
%{_libdir}/dri/imx-lcdif_dri.so
%{_libdir}/dri/kirin_dri.so
%{_libdir}/dri/komeda_dri.so
%{_libdir}/dri/mali-dp_dri.so
%{_libdir}/dri/mcde_dri.so
%{_libdir}/dri/mxsfb-drm_dri.so
%{_libdir}/dri/rcar-du_dri.so
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
%{_libdir}/dri/panthor_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%endif
%if 0%{?with_kmsro}
%{_libdir}/dri/armada-drm_dri.so
%{_libdir}/dri/exynos_dri.so
%{_libdir}/dri/gm12u320_dri.so
%{_libdir}/dri/hdlcd_dri.so
%{_libdir}/dri/hx8357d_dri.so
%{_libdir}/dri/ili9163_dri.so
%{_libdir}/dri/ili9225_dri.so
%{_libdir}/dri/ili9341_dri.so
%{_libdir}/dri/ili9486_dri.so
%{_libdir}/dri/imx-dcss_dri.so
%{_libdir}/dri/mediatek_dri.so
%{_libdir}/dri/meson_dri.so
%{_libdir}/dri/mi0283qt_dri.so
%{_libdir}/dri/panel-mipi-dbi_dri.so
%{_libdir}/dri/pl111_dri.so
%{_libdir}/dri/repaper_dri.so
%{_libdir}/dri/rockchip_dri.so
%{_libdir}/dri/rzg2l-du_dri.so
%{_libdir}/dri/ssd130x_dri.so
%{_libdir}/dri/st7586_dri.so
%{_libdir}/dri/st7735r_dri.so
%{_libdir}/dri/sti_dri.so
%{_libdir}/dri/sun4i-drm_dri.so
%{_libdir}/dri/udl_dri.so
%{_libdir}/dri/vkms_dri.so
%{_libdir}/dri/zynqmp-dpsub_dri.so
%endif
%if 0%{?with_vulkan_hw}
%{_libdir}/dri/zink_dri.so
%endif

%if 0%{?with_va}
%files va-drivers
%{_libdir}/dri/nouveau_drv_video.so
%if 0%{?with_r600}
%{_libdir}/dri/r600_drv_video.so
%endif
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_drv_video.so
%endif
%{_libdir}/dri/virtio_gpu_drv_video.so
%endif

%if 0%{?with_vdpau}
%files vdpau-drivers
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%if 0%{?with_r600}
%{_libdir}/vdpau/libvdpau_r600.so.1*
%endif
%if 0%{?with_radeonsi}
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%{_libdir}/vdpau/libvdpau_virtio_gpu.so.1*
%endif

%files vulkan-drivers
%{_libdir}/libvulkan_virtio.so
%{_datadir}/vulkan/icd.d/virtio_icd.*.json
%{_libdir}/libVkLayer_MESA_device_select.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_device_select.json
%if 0%{?with_vulkan_hw}
%{_libdir}/libvulkan_radeon.so
%{_datadir}/drirc.d/00-radv-defaults.conf
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%if 0%{?with_nvk}
%{_libdir}/libvulkan_nouveau.so
%{_datadir}/vulkan/icd.d/nouveau_icd.*.json
%endif
%ifarch %{ix86} x86_64
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%{_libdir}/libvulkan_intel_hasvk.so
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.*.json
%endif
%ifarch aarch64 x86_64 %{ix86}
%if 0%{?with_asahi}
%{_libdir}/libvulkan_asahi.so
%{_datadir}/vulkan/icd.d/asahi_icd.*.json
%endif
%{_libdir}/libvulkan_broadcom.so
%{_datadir}/vulkan/icd.d/broadcom_icd.*.json
%{_libdir}/libvulkan_freedreno.so
%{_datadir}/vulkan/icd.d/freedreno_icd.*.json
%{_libdir}/libvulkan_panfrost.so
%{_datadir}/vulkan/icd.d/panfrost_icd.*.json
%{_libdir}/libpowervr_rogue.so
%{_libdir}/libvulkan_powervr_mesa.so
%{_datadir}/vulkan/icd.d/powervr_mesa_icd.*.json
%endif
%endif

%files vulkan-lavapipe-layer
%{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json

%files vulkan-overlay
%doc src/vulkan/overlay-layer/README.rst
%{_bindir}/mesa-overlay-control.py
%{_libdir}/libVkLayer_MESA_overlay.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_MESA_overlay.json


%changelog
* Wed Jul 30 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.7-100
- 25.1.7

* Wed Jul 16 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.6-100
- 25.1.6

* Wed Jul 02 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.5-100
- 25.1.5

* Thu Jun 19 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.4-100
- 25.1.4

* Sat Jun 07 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.3-100
- 25.1.3

* Wed Jun 04 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.2-100
- 25.1.2

* Wed May 21 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.1-100
- 25.1.1

* Wed May 07 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.0-100
- 25.1.0

* Wed Apr 30 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.0~rc3-100
- 25.1.0-rc3
- Rawhide sync

* Thu Apr 17 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.4-100
- 25.0.4

* Wed Apr 02 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.3-100
- 25.0.3

* Thu Mar 20 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.2-100
- 25.0.2

* Thu Mar 06 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.1-100
- 25.0.1

* Wed Feb 19 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.0-100
- 25.0.0

* Wed Feb 12 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.0~rc3-100
- 25.0.0-rc3

* Thu Jan 23 2025 Phantom X <megaphantomx at hotmail dot com> - 24.3.4-100
- 24.3.4

* Fri Jan 03 2025 Phantom X <megaphantomx at hotmail dot com> - 24.3.3-100
- 24.3.3

* Thu Dec 19 2024 Phantom X <megaphantomx at hotmail dot com> - 24.3.2-100
- 24.3.2

* Thu Dec 05 2024 Phantom X <megaphantomx at hotmail dot com> - 24.3.1-100
- 24.3.1

* Thu Nov 21 2024 Phantom X <megaphantomx at hotmail dot com> - 24.3.0-100
- 24.3.0
- Rawhide sync

* Wed Nov 13 2024 Phantom X <megaphantomx at hotmail dot com> - 24.3.0~rc2-100
- 24.3.0-rc2

* Sat Nov 09 2024 Phantom X <megaphantomx at hotmail dot com> - 24.3.0~rc1-100
- 24.3.0-rc1

* Wed Oct 30 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.6-100
- 24.2.6

* Wed Oct 16 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.5-100
- 24.2.5

* Thu Oct 03 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.4-100
- 24.2.4

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.3-101
- Rawhide sync

* Wed Sep 18 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.3-100
- 24.2.3

* Fri Sep 06 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.2-100
- 24.2.2

* Thu Sep 05 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.1-101
- Upstream fixes

* Thu Aug 29 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.1-100
- 24.2.1

* Wed Jul 31 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.5-100
- 24.1.5

* Thu Jul 18 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.4-100
- 24.1.4

* Wed Jul 03 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.3-100
- 24.1.3

* Wed Jun 19 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.2-100
- 24.1.2

* Wed Jun 05 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.1-100
- 24.1.1

* Wed May 22 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.0-100
- 24.1.0

* Wed May 08 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.7-100
- 24.0.7

* Fri Apr 26 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.6-100
- 24.0.6

* Thu Apr 11 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.5-100
- 24.0.5

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.4-100
- 24.0.4

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.3-101
- Rawhide sync

* Thu Mar 14 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.3-100
- 24.0.3

* Wed Feb 28 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.2-100
- 24.0.2

* Thu Feb 15 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.1-100
- 24.0.1

* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.0-100
- 24.0.0

* Thu Jan 25 2024 Phantom X <megaphantomx at hotmail dot com> - 23.3.4-100
- 23.3.4

* Thu Jan 11 2024 Phantom X <megaphantomx at hotmail dot com> - 23.3.3-100
- 23.3.3

* Thu Dec 28 2023 Phantom X <megaphantomx at hotmail dot com> - 23.3.2-100
- 23.3.2

* Wed Dec 13 2023 Phantom X <megaphantomx at hotmail dot com> - 23.3.1-100
- 23.3.1

* Wed Nov 29 2023 Phantom X <megaphantomx at hotmail dot com> - 23.3.0-100
- 23.3.0

* Sat Nov 25 2023 Phantom X <megaphantomx at hotmail dot com> - 23.3.0~rc5-100
- 23.3.0-rc5

* Thu Nov 16 2023 Phantom X <megaphantomx at hotmail dot com> - 23.3.0~rc4-100
- 23.3.0-rc4

* Thu Nov 09 2023 Phantom X <megaphantomx at hotmail dot com> - 23.3.0~rc3-100
- 23.3.0-rc3

* Fri Oct 13 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.1-101.20231012git94ed71d
- Add some patches from OpenMandriva
- Fix build with LLVM 17.

* Fri Sep 29 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.1-100
- 23.2.1

* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.0~rc3-101.20230914git3317f14
- Add llvm_pkgver define to set versioned LLVM packages, when needed

* Tue Sep 05 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.0~rc3-100.20230905gitc111021
- 23.2.0-rc3

* Sat Jul 29 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.0-100
- 23.2.0

* Fri Jul 21 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.4-100
- 23.1.4

* Thu Jun 22 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.3-100
- 23.1.3

* Thu Jun 08 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.2-100
- 23.1.2

* Sun May 28 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.1-101
- Rawhide sync
- Disable LTO for the time

* Fri May 26 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.1-100
- 23.1.1

* Wed May 10 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.0-100
- 23.1.0

* Thu May 04 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.0~rc4-100
- 23.1.0-rc4

* Thu Apr 27 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.0~rc3-100
- 23.1.0-rc3

* Wed Apr 19 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.0~rc2-100
- 23.1.0-rc2

* Sat Apr 15 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.0~rc1-100
- 23.1.0-rc1

* Thu Apr 13 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.2-101.20230413git7d0aee9
- Rebuild (llvm)

* Fri Apr 07 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.2-100
- 23.0.2

* Sat Mar 25 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.1-100
- 23.0.1

* Fri Mar 24 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0-102.20230323git032a428
- Reenable LTO

* Thu Feb 23 2023 Phantom X - 23.0.0-100.20230222git8b9b246
- 23.0.0

* Fri Feb 17 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc5-100.20230216git07b9046
- 23.0.0-rc5

* Thu Feb 02 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc4-100.20230201git8bb100f
- 23.0.0-rc4

* Thu Jan 26 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc3-100.20230126git406ef42
- 23.0.0-rc3

* Thu Jan 19 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc2-100.20230119git41648b0
- 23.0.0-rc2

* Wed Jan 11 2023 Phantom X <megaphantomx at hotmail dot com> - 22.3.3-100
- 22.3.3

* Sat Dec 31 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.2-100
- 22.3.2

* Thu Dec 15 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.1-100
- 22.3.1

* Thu Dec 01 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.0-100
- 22.3.0

* Thu Nov 24 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.0~rc4-100
- 22.3.0-rc4

* Sat Nov 19 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.0~rc3-100
- 22.3.0~rc3
- Rawhide sync

* Thu Nov 17 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.4-100
- 22.2.4

* Wed Nov 09 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.3-100
- 22.2.3

* Wed Oct 19 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.2-100
- 22.2.2

* Wed Oct 12 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.1-100
- 22.2.1

* Wed Oct 05 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0-104.20221004gitd4d47ef
- Rawhide sync

* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0-103.20220929git9d1f0e8
- Snapshot
- Split vaapi package

* Wed Sep 21 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0-101
- Disable video codecs

* Tue Sep 20 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0-100
- 22.2.0

* Sat Sep 17 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0~rc3-101.20220916gitb47e856
- Staging snapshot

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0~rc3-100
- 22.2.0-rc3
- Rawhide sync

* Wed Aug 17 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.7-100
- 22.1.7

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
