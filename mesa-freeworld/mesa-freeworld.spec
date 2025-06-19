# Disable this, like mesa full package.
%global _lto_cflags %{nil}

%ifnarch s390x
%if !0%{?rhel}
%global with_r600 1
%endif
%global with_radeonsi 1
%endif

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%global commit 94ed71dad161edb01ee7acaae02e555af3e5dcac
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20231012
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

# Set to build with versioned LLVM packages
%dnl %global llvm_pkgver 16

%global pkgname mesa
%global vc_url  https://gitlab.freedesktop.org/mesa/mesa

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           %{pkgname}-freeworld
Summary:        Mesa-based video acceleration drivers - freeworld
# If rc, use "~" instead "-", as ~rc1
Version:        25.1.4
Release:        100%{?dist}

Epoch:          100

License:        MIT
URL:            http://www.mesa3d.org

%if %{with snapshot}
Source0:        %{vc_url}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        https://archive.mesa3d.org/%{pkgname}-%{ver}.tar.xz
%endif
Source2:        org.mesa3d.vaapi.freeworld.metainfo.xml
Source3:        org.mesa3d.vdpau.freeworld.metainfo.xml

BuildRequires:  meson >= 1.0.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext


BuildRequires:  kernel-headers
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.121
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
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
BuildRequires:  llvm%{?llvm_pkgver}-devel >= 15.0.0
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  python3-pyyaml
BuildRequires:  pkgconfig(libzstd)

%description
%{summary}.

%package -n     %{pkgname}-dri-drivers-freeworld
Summary:        Mesa-based DRI drivers - freeworld
Requires:       %{pkgname}-filesystem%{?_isa} >= %{version}

%description -n %{pkgname}-dri-drivers-freeworld
%{summary}.


%package -n     %{pkgname}-va-drivers-freeworld
Summary:        Mesa-based VAAPI drivers - freeworld
Requires:       %{pkgname}-filesystem%{?_isa} >= %{version}
Requires:       %{pkgname}-dri-drivers-freeworld%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{pkgname}-va-drivers%{?_isa}
Enhances:       %{pkgname}%{?_isa}

%description -n %{pkgname}-va-drivers-freeworld
%{summary}.


%package -n     %{pkgname}-vdpau-drivers-freeworld
Summary:        Mesa-based VDPAU drivers- freeworld
Requires:       %{pkgname}-filesystem%{?_isa} >= %{version}
Requires:       %{pkgname}-dri-drivers-freeworld%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{pkgname}-vdpau-drivers%{?_isa}
Enhances:       %{pkgname}%{?_isa}

%description -n %{pkgname}-vdpau-drivers-freeworld
%{summary}.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

echo %{version}-freeworld > VERSION

%build
%meson \
  -Dplatforms=x11 \
  -Dgallium-drivers=virgl,nouveau%{?with_radeonsi:,radeonsi}%{?with_r600:,r600} \
  -Dgallium-vdpau=enabled \
  -Dgallium-va=enabled \
  -Dgallium-xa=disabled \
  -Dgallium-nine=false \
  -Dteflon=false \
  -Dgallium-opencl=disabled \
  -Dgallium-rusticl=false \
  -Dvulkan-drivers="" \
  -Dvideo-codecs=h264dec,h264enc,h265dec,h265enc,vc1dec \
  -Dshared-glapi=enabled \
  -Dgles1=disabled \
  -Dgles2=disabled \
  -Dopengl=true \
  -Dgbm=disabled \
  -Dglx=dri \
  -Degl=enabled \
  -Dglvnd=enabled \
  -Dintel-rt=disabled \
  -Dmicrosoft-clc=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Db_ndebug=true \
  -Dbuild-tests=false \
  -Dlmsensors=disabled \
  -Dandroid-libbacktrace=disabled \
%ifarch %{ix86}
  -Dglx-read-only-text=true
%endif
  %{nil}

%meson_build


%install
%meson_install

# libvdpau opens the versioned name, don't bother including the unversioned
rm -vf %{buildroot}%{_libdir}/vdpau/*.so

mv %{buildroot}%{_libdir}/libgallium-*-freeworld.so .
rm -rf %{buildroot}%{_libdir}/*.so*
mv libgallium-*-freeworld.so %{buildroot}%{_libdir}/
rm -rf %{buildroot}%{_libdir}/dri/*_dri.so*
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}

# install Appdata files
mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 %{S:2} %{buildroot}%{_metainfodir}
install -pm0644 %{S:3} %{buildroot}%{_metainfodir}

%files -n %{pkgname}-dri-drivers-freeworld
%license docs/license.rst
%{_libdir}/libgallium-*-freeworld.so

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
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%{_libdir}/vdpau/libvdpau_virtio_gpu.so.1*
%if 0%{?with_r600}
%{_libdir}/vdpau/libvdpau_r600.so.1*
%endif
%if 0%{?with_radeonsi}
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%{_metainfodir}/org.mesa3d.vdpau.freeworld.metainfo.xml


%changelog
* Thu Jun 19 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.1.4-100
- 25.1.4

* Sat Jun 07 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.1.3-100
- 25.1.3

* Wed Jun 04 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.1.2-100
- 25.1.2

* Wed May 21 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.1.1-100
- 25.1.1

* Wed May 07 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.1.0-100
- 25.1.0

* Wed Apr 30 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.1.0~rc3-100
- 25.1.0-rc3

* Thu Apr 17 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.0.4-100
- 25.0.4

* Wed Apr 02 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.0.3-100
- 25.0.3

* Thu Mar 20 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.0.2-100
- 25.0.2

* Thu Mar 06 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.0.1-100
- 25.0.1

* Wed Feb 19 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.0.0-100
- 25.0.0

* Wed Feb 12 2025 Phantom X <megaphantomx at hotmail dot com> - 100:25.0.0~rc3-100
- 25.0.0-rc3

* Thu Jan 23 2025 Phantom X <megaphantomx at hotmail dot com> - 100:24.3.4-100
- 24.3.4

* Fri Jan 03 2025 Phantom X <megaphantomx at hotmail dot com> - 100:24.3.3-100
- 24.3.3

* Thu Dec 19 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.3.2-100
- 24.3.2

* Thu Dec 05 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.3.1-100
- 24.3.1

* Thu Nov 21 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.3.0-100
- 24.3.0

* Wed Nov 13 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.3.0~rc2-100
- 24.3.0-rc2

* Sat Nov 09 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.3.0~rc1-100
- 24.3.0-rc1

* Wed Oct 30 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.2.6-100
- 24.2.6

* Wed Oct 16 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.2.5-100
- 24.2.5

* Thu Oct 03 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.4-100
- 24.2.4

* Wed Sep 18 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.2.3-100
- 24.2.3

* Fri Sep 06 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.2.2-100
- 24.2.2

* Thu Aug 29 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.2.1-100
- 24.2.1

* Wed Jul 31 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.1.5-100
- 24.1.5

* Thu Jul 18 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.1.4-100
- 24.1.4

* Wed Jul 03 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.1.3-100
- 24.1.3

* Wed Jun 19 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.1.2-100
- 24.1.2

* Wed Jun 05 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.1.1-100
- 24.1.1

* Wed May 22 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.1.0-100
- 24.1.0

* Wed May 08 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.7-100
- 24.0.7

* Thu Apr 25 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.6-100
- 24.0.6

* Thu Apr 11 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.5-100
- 24.0.5

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.4-100
- 24.0.4

* Thu Mar 14 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.3-100
- 24.0.3

* Wed Feb 28 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.2-100
- 24.0.2

* Thu Feb 15 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.1-100
- 24.0.1

* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 100:24.0.0-100
- 23.4.0

* Thu Jan 25 2024 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.4-100
- 23.3.4

* Thu Jan 11 2024 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.3-100
- 23.3.3

* Thu Dec 28 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.2-100
- 23.3.2

* Wed Dec 13 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.1-100
- 23.3.1

* Wed Nov 29 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.0-100
- 23.3.0

* Sat Nov 25 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.0~rc5-100
- 23.3.0-rc5

* Thu Nov 16 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.0~rc4-100
- 23.3.0-rc4

* Thu Nov 09 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.3.0~rc3-100
- 23.3.0-rc3

* Fri Sep 29 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.2.1-100
- 23.2.1

* Tue Sep 05 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.2.0~rc3-100.20230905gitc111021
- 23.2.0-rc3

* Sat Jul 29 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.2.0-100
- 23.2.0

* Fri Jul 21 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.4-100
- 23.1.4

* Thu Jun 22 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.3-100
- 23.1.3

* Thu Jun 08 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.2-100
- 23.1.1

* Sun May 28 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.1-101
- Disable LTO for the time

* Fri May 26 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.1-100
- 23.1.1

* Wed May 10 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.0-100
- 23.1.0

* Thu May 04 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.0~rc4-100
- 23.1.0-rc4

* Thu Apr 27 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.0~rc3-100
- 23.1.0-rc3

* Wed Apr 19 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.0~rc2-100
- 23.1.0-rc2

* Sat Apr 15 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.1.0~rc1-100
- 23.1.0-rc1

* Thu Apr 13 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.2-2.20230413git7d0aee9
- Rebuild (llvm)

* Fri Apr 07 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.2-1
- 23.0.2

* Sat Mar 25 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.1-100
- 23.0.1

* Fri Mar 24 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.0-102.20230323git032a428
- Reenable LTO

* Thu Feb 23 2023 Phantom X - 100:23.0.0-100
- 23.0.0

* Fri Feb 17 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.0~rc5-100.20230216git07b9046
- 23.0.0-rc5

* Thu Feb 02 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.0~rc4-100.20230201git8bb100f
- 23.0.0-rc4

* Thu Jan 26 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.0~rc3-100.20230126git406ef42
- 23.0.0-rc3

* Thu Jan 19 2023 Phantom X <megaphantomx at hotmail dot com> - 100:23.0.0~rc2-100.20230119git41648b0
- 23.0.0-rc2

* Thu Jan 12 2023 Phantom X <megaphantomx at hotmail dot com> - 22.3.3-1
- 22.3.3

* Sat Dec 31 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.3.2-100
- 22.3.2

* Thu Dec 15 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.3.1-100
- 22.3.1

* Thu Dec 01 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.3.0-100
- 22.3.0

* Thu Nov 24 2022 Phantom X <megaphantomx at hotmail dot com> - 100:22.3.0~rc4-100
- 22.3.0-rc4

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
