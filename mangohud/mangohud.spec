%global commit 5f51f3f1ed357c2887bb7e2c05aea6a091f01840
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200802
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%bcond_with sysvulkan
%ifnarch s390x
%bcond_without tests
%endif

%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS

%global imgui_ver 1.89.9
%global implot_ver 0.16
%global vulkan_ver 1.2.158

%global pkgname MangoHud
%global vc_url https://github.com/flightlessmango

%global ver    %%(echo %{version} | sed -z 's/\\./-/3')

Name:           mangohud
Version:        0.7.2
Release:        100%{?dist}
Summary:        A Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            %{vc_url}/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{ver}/%{pkgname}-v%{ver}.tar.gz
%endif
Source3:        %{name}.in
Source4:        README.Fedora.md
Source10:       https://github.com/ocornut/imgui/archive/v%{imgui_ver}/imgui-%{imgui_ver}.tar.gz
Source11:       https://wrapdb.mesonbuild.com/v2/imgui_%{imgui_ver}-1/get_patch#/imgui-%{imgui_ver}-1-wrap.zip
%if %{without sysvulkan}
Source12:       https://github.com/KhronosGroup/Vulkan-Headers/archive/v%{vulkan_ver}.tar.gz#/Vulkan-Headers-%{vulkan_ver}.tar.gz
Source13:       https://wrapdb.mesonbuild.com/v2/vulkan-headers_%{vulkan_ver}-2/get_patch#/vulkan-headers_%{vulkan_ver}-2-wrap.zip
%endif
Source14:       https://github.com/epezent/implot/archive/v%{implot_ver}/implot-%{implot_ver}.zip
Source15:       https://wrapdb.mesonbuild.com/v2/implot_%{implot_ver}-1/get_patch#/implot-%{implot_ver}-1-wrap.zip

Patch1:         0001-Change-loader-files-names.patch

BuildRequires:  appstream
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  glslang
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
%if %{with tests}
BuildRequires:  libcmocka-devel
%endif
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(spdlog)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  python3
BuildRequires:  python3-mako
BuildRequires:  unzip
%if %{with sysvulkan}
BuildRequires:  cmake(VulkanHeaders) >= %{vulkan_ver}
%else
Provides:       bundled(vulkan-headers) = %{vulkan_ver}
%endif
Requires:       libglvnd%{?_isa}
Requires:       libglvnd-glx%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(imgui) = %{imgui_ver}
Provides:       bundled(implot) = %{implot_ver}

Recommends:     (mangohud(x86-32) if glibc(x86-32))

Suggests:       goverlay


%description
%{pkgname} is a modification of the Mesa Vulkan overlay. Including GUI
improvements, temperature reporting, and logging capabilities.


%package        mangoplot
Summary:        Local visualization "mangoplot" for %{name}
BuildArch:      noarch

BuildRequires:  python3-devel
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-matplotlib
Requires:       python3-numpy

%description    mangoplot
Local visualization "mangoplot" for %{name}.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

tar xf %{S:10} -C subprojects/
unzip %{S:11} -d subprojects/
%if %{without sysvulkan}
tar xf %{S:12} -C subprojects/
unzip %{S:13} -d subprojects/
%endif
unzip %{S:14} -d subprojects/
unzip %{S:15} -d subprojects/

rm -f include/nvml.h

cp -p %{S:4} .

cp -f -p %{S:3} bin/%{name}.in
sed -e 's|@version@|%{version}-%{release}|g' -i bin/%{name}.in

%py3_shebang_fix bin/mangoplot.py

%if %{with tests}
# Use system cmocka instead of subproject
# https://gitlab.archlinux.org/archlinux/packaging/packages/mangohud/-/blob/0.6.9.1-10/PKGBUILD?ref_type=tags#L32
sed -i "s/  cmocka = subproject('cmocka')//g" meson.build
sed -i "s/cmocka_dep = cmocka.get_variable('cmocka_dep')/cmocka_dep = dependency('cmocka')/g" meson.build
%endif

# https://github.com/flightlessmango/MangoHud/commit/dc1761e98a435aaee6a919e21f43b85cc38500ac
sed -e "s/, '-static-libstdc++'//" \
  -i src/meson.build

sed \
  -e "s|'git', 'describe', '--tags', '--dirty=+'|'echo','%{version}-%{release}'|g" \
  -i src/meson.build


%build
%meson \
  --libdir=%{_libdir} \
  -Dappend_libdir_mangohud=true \
  -Ddynamic_string_tokens=true \
  -Dglibcxx_asserts=false \
  -Duse_system_spdlog=enabled \
  -Dmangoapp=true \
  -Dmangoapp_layer=true \
  -Dmangohudctl=true \
  -Dinclude_doc=true \
  -Dwith_nvml=disabled \
  -Dwith_xnvctrl=disabled \
  -Dwith_wayland=enabled \
  -Dtests=%{?with_tests:enabled}%{!?with_tests:disabled} \
%{nil}

%meson_build


%install
%meson_install

chmod 0755 %{buildroot}%{_bindir}/%{name}

rm -rf %{buildroot}%{_datadir}/doc


%check
# https://github.com/flightlessmango/MangoHud/issues/812
# ? tag-invalid           : stock icon is not valid [io.github.flightlessmango.mangohud]
%dnl appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
%if %{with tests}
%meson_test
%endif


%files
%license LICENSE
%doc README.md README.Fedora.md data/%{pkgname}.conf
%{_bindir}/mangoapp
%{_bindir}/mangohud
%{_bindir}/mangohudctl
%{_libdir}/%{name}/lib%{pkgname}.so
%{_libdir}/%{name}/lib%{pkgname}_dlsym.so
%{_libdir}/%{name}/lib%{pkgname}_opengl.so
%{_libdir}/%{name}/libMangoApp.so
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/vulkan/implicit_layer.d/*.json
%{_mandir}/man1/mango*.1*
%{_metainfodir}/*.metainfo.xml

%files mangoplot
%{_bindir}/mangoplot


%changelog
* Tue May 28 2024 Phantom X <megaphantomx at hotmail dot com> - 0.7.2-100
- 0.7.2

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.7.1-100
- 0.7.1

* Mon Oct 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.7.0-100
- 0.7.0
- Rawhide sync

* Sat Aug 26 2023 Phantom X <megaphantomx at hotmail dot com> - 0.6.9.1-101
- Rename loader files

* Wed Aug 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.6.9.1-100
- 0.6.9-1
- Rawhide sync

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.6.8-101
- gcc 13 build fix
- Use bundled vulkan-headers and disable app for the time

* Tue Aug 02 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.8-100
- 0.6.8

* Fri May 06 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.7-101
- Enable wayland-support
- Enable MangoApp (system json patch)

* Thu May 05 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.7-100
- 0.6.7

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
