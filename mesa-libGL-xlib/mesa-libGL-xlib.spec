%dnl %global _lto_cflags %{nil}

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%global commit 032a428fac08f67828d2939f72073ed27b7bae46
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230323
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname mesa
%global vc_url  https://gitlab.freedesktop.org/mesa/mesa

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           mesa-libGL-xlib
Summary:        Mesa libGL runtime libraries with xlib support
# If rc, use "~" instead "-", as ~rc1
Version:        23.0.1
Release:        1%{?gver}%{?dist}

License:        MIT
URL:            http://www.mesa3d.org

%if 0%{?with_snapshot}
Source0:        %{vc_url}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        https://mesa.freedesktop.org/archive/%{pkgname}-%{ver}.tar.xz
%endif

BuildRequires:  meson >= 1.0.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext


# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.110
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes) >= 2.0
BuildRequires:  pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2) >= 1.8
BuildRequires:  pkgconfig(dri2proto) >= 2.8
BuildRequires:  pkgconfig(glproto) >= 1.4.14
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xrandr) >= 1.3
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pkgconfig(libelf)
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  pkgconfig(libzstd)
Recommends:     x2goserver
Requires:       %{pkgname}-libglapi%{?_isa} >= %{version}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*


%description
%{summary}.

Needed as workaround for getting GLX 1.4 working with x2goserver.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{ver}} -p1

cat > xlibgl.sh <<'EOF'
#!/usr/bin/sh
# Launch things with xlib libGL

LD_LIBRARY_PATH="/usr/\${LIB}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

exec env LD_LIBRARY_PATH="${LD_LIBRARY_PATH}" "$@"
EOF

cat > xlibglp.sh <<'EOF'
#!/usr/bin/sh
# Launch things with old official SDL - preload variant

GLX_LIB=libGL.so.1
LD_PRELOAD="/usr/\${LIB}/%{name}/${GLX_LIB}${LD_PRELOAD:+:$LD_PRELOAD}"

exec env LD_PRELOAD="${LD_PRELOAD}" "$@"
EOF

%build
%meson \
  -Dplatforms=x11 \
  -Ddri3=disabled \
  -Dgallium-drivers=swrast \
  -Dgallium-vdpau=disabled \
  -Dgallium-omx=disabled \
  -Dgallium-va=disabled \
  -Dgallium-xa=disabled \
  -Dgallium-nine=false \
  -Dgallium-opencl=disabled \
  -Dgallium-rusticl=false \
  -Ddri-drivers="" \
  -Dvulkan-drivers="" \
  -Dshared-glapi=enabled \
  -Dgles1=disabled \
  -Dgles2=disabled \
  -Dopengl=true \
  -Dgbm=disabled \
  -Dglx=xlib \
  -Degl=disabled \
  -Dglvnd=false \
  -Dmicrosoft-clc=disabled \
  -Dllvm=disabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Db_ndebug=true \
  -Dbuild-tests=false \
  -Dselinux=true \
  %{nil}

%meson_build


%install
%meson_install

rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -f %{buildroot}%{_libdir}/libglapi.so*
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_includedir}

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd %{buildroot}%{_libdir}
for i in libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd

rm -f %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_bindir}
install -pm0755 xlibgl.sh %{buildroot}%{_bindir}/xlibgl
install -pm0755 xlibglp.sh %{buildroot}%{_bindir}/xlibglp


%files
%license docs/license.rst
%{_bindir}/xlibgl*
%{_libdir}/%{name}/libGL.so.1*


%changelog
* Sat Mar 25 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.1-1
- 23.0.1

* Fri Mar 24 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0-3.20230323git032a428
- Reenable LTO

* Thu Feb 23 2023 Phantom X - 23.0.0-1
- 23.0.0

* Fri Feb 17 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc5-1.20230216git07b9046
- 23.0.0-rc5

* Thu Feb 02 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc4-1.20230201git8bb100f
- 23.0.0-rc4

* Thu Jan 26 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc3-1.20230126git406ef42
- 23.0.0-rc3

* Thu Jan 19 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0~rc2-1.20230119git41648b0
- 23.0.0-rc2

* Thu Jan 12 2023 Phantom X <megaphantomx at hotmail dot com> - 22.3.3-1
- 22.3.3

* Sat Dec 31 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.2-1
- 22.3.2

* Thu Dec 15 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.1-1
- 22.3.1

* Thu Dec 01 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.0-1
- 22.3.0

* Thu Nov 24 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.0~rc4-1
- 22.3.0-rc4

* Sat Nov 19 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.0~rc3-1
- 22.3.0~rc3

* Thu Nov 17 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.4-1
- 22.2.4

* Wed Nov 09 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.3-1
- 22.2.3

* Wed Oct 26 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.2-1
- Initial spec

