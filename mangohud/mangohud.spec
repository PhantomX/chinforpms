%global commit 5f51f3f1ed357c2887bb7e2c05aea6a091f01840
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200802
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global imgui_ver 1.81

%global pkgname MangoHud
%global vc_url https://github.com/flightlessmango

Name:           mangohud
Version:        0.6.6
Release:        100%{?gver}%{?dist}
Summary:        A Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            %{vc_url}/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-v%{version}.tar.gz
%endif
Source3:        %{name}.in
Source10:       https://github.com/ocornut/imgui/archive/v%{imgui_ver}/imgui-%{imgui_ver}.tar.gz
Source11:       https://wrapdb.mesonbuild.com/v2/imgui_%{imgui_ver}-1/get_patch#/imgui-%{imgui_ver}-1-wrap.zip


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  glslang
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(spdlog)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3
BuildRequires:  python3-mako
BuildRequires:  unzip
BuildRequires:  vulkan-headers
Requires:       libglvnd%{?_isa}
Requires:       libglvnd-glx%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(imgui) = %{imgui_ver}

Recommends:     (mangohud(x86-32) if glibc(x86-32))


%description
%{pkgname} is a modification of the Mesa Vulkan overlay. Including GUI
improvements, temperature reporting, and logging capabilities.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

tar xf %{S:10} -C subprojects/
unzip %{S:11} -d subprojects/

rm -f include/nvml.h

cp -f -p %{S:3} bin/%{name}.in

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s\s\s\s| |g" -e "s|\s\s\s| |g" -e "s|\s\s| |g" -e 's|^\s||g' -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')

TEMP_CFLAGS="`mesonarray "%{optflags}"`"

sed -e "/-D__STDC_CONSTANT_MACROS/i\  '${TEMP_CFLAGS}'," -i meson.build


%build

%meson \
  --libdir=%{_libdir} \
  -Dappend_libdir_mangohud=true \
  -Dglibcxx_asserts=false \
  -Duse_system_spdlog=enabled \
  -Duse_system_vulkan=enabled \
  -Dinclude_doc=false \
  -Dwith_nvml=disabled \
  -Dwith_xnvctrl=disabled \
%{nil}

%meson_build


%install
%meson_install

chmod 0755 %{buildroot}%{_bindir}/%{name}


%files
%license LICENSE
%doc README.md bin/%{pkgname}.conf
%{_bindir}/%{name}
%{_libdir}/%{name}/lib%{pkgname}.so
%{_libdir}/%{name}/lib%{pkgname}_dlsym.so
%{_datadir}/vulkan/implicit_layer.d/%{pkgname}.json
%{_mandir}/man1/%{name}.1*


%changelog
* Tue Oct 19 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.6-100
- 0.6.6

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.5-1
- 0.6.5

* Thu Jun 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.4-1
- 0.6.4

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-1
- 0.6.3

* Tue Dec 01 2020 Phantom X <megaphantomx at hotmail dot com> - 0.6.1-1
- 0.6.1

* Tue Nov 17 2020 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-2
- Fix wrapper again

* Mon Aug 17 2020 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-1
- 0.5.1

* Sat Aug 15 2020 Phantom X <megaphantomx at hotmail dot com> - 0.4.1-2.20200802git5f51f3f
- Snapshot
- Manpage

* Thu Jun 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.4.1-1.20200611git8ed5fe6
- 0.4.1
- sanitized sources, without nvml support

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.3.5-1.20200511git943c345
- 0.3.5
- BR: dbus-1

* Thu Mar 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.3.1-1
- 0.3.1
- Remove now unneeded __filter_GLIBC_PRIVATE

* Sat Mar 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-1
- 0.3.0
- __filter_GLIBC_PRIVATE 1 until upstream fix __libc_dlsym usage

* Fri Feb 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2.0-1
- 0.2.0

* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.1.0-1.20200205git420c26a
- Initial spec
