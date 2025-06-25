# Inconsistent
%global _lto_cflags %{nil}

%global origname mesa

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           %{origname}-compat
Summary:        Mesa graphics libraries - legacy compatibility libraries
Version:        25.0.5
Release:        100%{?dist}
License:        MIT AND BSD-3-Clause AND SGI-B-2.0
URL:            http://www.mesa3d.org

Source0:        https://archive.mesa3d.org/mesa-%{ver}.tar.xz
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source1:        Mesa-MLAA-License-Clarification-Email.txt

# Fix https://bugs.winehq.org/show_bug.cgi?id=41930
# https://gitlab.freedesktop.org/mesa/mesa/-/issues/5094
# Ported from https://gitlab.freedesktop.org/bvarner/mesa/-/tree/feature/osmesa-preserve-buffer
Patch500:       mesa-24.0-osmesa-fix-civ3.patch
Patch501:       mesa-23.1-x86_32-llvm-detection.patch

BuildRequires:  meson >= 1.3.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
%if 0%{?with_hardware}
BuildRequires:  kernel-headers
%endif
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pkgconfig(libelf)
BuildRequires:  llvm-devel >= 15.0.0
BuildRequires:  pkgconfig(libdrm) >= 2.4.122
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyyaml

%description
%{summary}.

%package libOSMesa
Summary:        Mesa offscreen rendering libraries
Provides:       libOSMesa
Provides:       libOSMesa%{?_isa}
# New things should not rely on this as this library is dead upstream
Provides:       deprecated()

%description libOSMesa
%{summary}.

%package libOSMesa-devel
Summary:        Mesa offscreen rendering development package
Requires:       %{name}-libOSMesa%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# New things should not rely on this as this library is dead upstream
Provides:       deprecated()

%description libOSMesa-devel
%{summary}.

%prep
%autosetup -n %{origname}-%{ver} -p1

cp %{SOURCE1} docs/

%build
%meson \
  -Dplatforms= \
  -Dosmesa=true \
  -Dgallium-drivers=llvmpipe \
  -Dgallium-vdpau=disabled \
  -Dgallium-va=disabled \
  -Dgallium-xa=disabled \
  -Dgallium-nine=false \
  -Dgallium-opencl=disabled \
  -Dgallium-rusticl=false \
  -Dvulkan-drivers= \
  -Dshared-glapi=enabled \
  -Dgles1=disabled \
  -Dgles2=disabled \
  -Dopengl=true \
  -Dgbm=disabled \
  -Dglvnd=disabled \
  -Dglx=disabled \
  -Degl=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=disabled \
  -Dbuild-tests=false \
  -Dmesa-clc=auto \
  -Dmicrosoft-clc=disabled \
  -Dxlib-lease=disabled \
  -Dandroid-libbacktrace=disabled \
  -Dlibunwind=disabled \
  -Dlmsensors=disabled \
%ifarch %{ix86}
  -Dglx-read-only-text=true \
%endif
  %{nil}

%meson_build

%install
%meson_install

# trim some garbage, the mesa base package handles these
rm -rf %{buildroot}%{_datadir}/drirc.d
rm -rf %{buildroot}%{_includedir}/GL/gl*.h
rm -rf %{buildroot}%{_includedir}/KHR

%files libOSMesa
%{_libdir}/libOSMesa.so.8*
%files libOSMesa-devel
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc


%changelog
* Wed Apr 30 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.5-100
- 25.0.5

* Thu Apr 24 2025 Neal Gompa <ngompa@fedoraproject.org> - 25.0.4-1
- Initial split from mesa for compat libraries (rhbz#2362203)
