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

%global commit 9d1f0e8c82911cb62f17a4a87e02b799e5ce2b81
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220929
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname mesa
%global vc_url  https://gitlab.freedesktop.org/mesa/mesa

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           mesa-drivers-freeworld
Summary:        Mesa-based video acceleration drivers - freeworld
# If rc, use "~" instead "-", as ~rc1
Version:        22.2.0
Release:        100%{?gver}%{?dist}

Epoch:          100

License:        MIT
URL:            http://www.mesa3d.org

%if 0%{?with_snapshot}
Source0:        %{vc_url}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        https://mesa.freedesktop.org/archive/%{pkgname}-%{ver}.tar.xz
%endif

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


%package -n     mesa-vaapi-drivers-freeworld
Summary:        Mesa-based VAAPI drivers - freeworld
Obsoletes:      mesa-vaapi-drivers < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mesa-vaapi-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mesa-filesystem%{?_isa} >= %{version}

%description -n mesa-vaapi-drivers-freeworld
%{summary}.


%package -n     mesa-vdpau-drivers-freeworld
Summary:        Mesa-based VDPAU drivers- freeworld
Obsoletes:      mesa-vdpau-drivers < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mesa-vdpau-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mesa-filesystem%{?_isa} >= %{version}

%description -n mesa-vdpau-drivers-freeworld
%{summary}.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{ver}} -p1

%build
%meson \
  -Dplatforms=x11 \
  -Ddri3=enabled \
  -Dosmesa=false \
  -Dgallium-drivers=nouveau%{?with_r300:,r300}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600} \
  -Dgallium-vdpau=enabled \
  -Dgallium-xvmc=disabled \
  -Dgallium-omx=disabled \
  -Dgallium-va=enabled \
  -Dgallium-xa=disabled \
  -Dgallium-nine=false \
  -Dgallium-opencl=disabled \
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


%files -n mesa-vaapi-drivers-freeworld
%{_libdir}/dri/nouveau_drv_video.so
%if 0%{?with_r600}
%{_libdir}/dri/r600_drv_video.so
%endif
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_drv_video.so
%endif

%files -n mesa-vdpau-drivers-freeworld
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


%changelog
* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0-100.20220929git9d1f0e8
- Initial spec
