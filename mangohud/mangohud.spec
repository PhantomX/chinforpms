%global commit 943c3459dad73e3bf2eb1c28352d38aada1497cb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200511
%global with_snapshot 1

%global commit1 1f02d240b38f445abb0381ade0867752d5d2bc7b
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 flightlessmango-ImGui

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname MangoHud
%global vc_url https://github.com/flightlessmango

Name:           mangohud
Version:        0.3.5
Release:        1%{?gver}%{?dist}
Summary:        A Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            %{vc_url}/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
#Source0:        %%{url}/releases/download/v%%{version}/%%{pkgname}-src-v%%{version}.tar.xz
%endif
Source1:        %{vc_url}/ImGui/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz

Patch0:         0001-preload-fix-for-multilib.patch


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  glslang
BuildRequires:  libXNVCtrl-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3
BuildRequires:  python3-mako
BuildRequires:  vulkan-headers
Requires:       libglvnd%{?_isa}
Requires:       libglvnd-glx%{?_isa}
Requires:       libXNVCtrl%{?_isa}
Requires:       vulkan-loader%{?_isa}

%description
%{pkgname} is a modification of the Mesa Vulkan overlay. Including GUI
improvements, temperature reporting, and logging capabilities.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif
tar -xf %{S:1} -C modules/ImGui/src --strip-components 1

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
  -Duse_system_vulkan=enabled \
  -Dinclude_doc=false \
%{nil}

%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md bin/%{pkgname}.conf
%{_bindir}/%{name}
%{_libdir}/%{name}/lib%{pkgname}.so
%{_libdir}/%{name}/lib%{pkgname}_dlsym.so
%{_datadir}/vulkan/implicit_layer.d/%{pkgname}.*.json


%changelog
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
