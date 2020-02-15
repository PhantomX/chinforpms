%global commit 420c26a08aa5043a533ccf5d275173d73388d60c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200205
%global with_snapshot 0

%global commit1 6c1a73774dabd2be64f85543b1286e44632d1905
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 flightlessmango-ImGui

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname MangoHud
%global vc_url https://github.com/flightlessmango

Name:           mangohud
Version:        0.2.0
Release:        1%{?gver}%{?dist}
Summary:        A Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            %{vc_url}/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        %{vc_url}/ImGui/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  glslang
BuildRequires:  libXNVCtrl-devel
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3
BuildRequires:  python3-mako
BuildRequires:  vulkan-headers
Requires:       libglvnd%{?_isa}
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

sed \
  -e '/name/s|64bit|%{_arch}|g' \
  -e '/library_path/s|libMangoHud.so|%{_libdir}/%{name}/\0|g' \
  -i src/mangohud.json


%build

%meson \
  --libdir=%{_libdir}/%{name} \
  -Duse_system_vulkan=enabled \
%{nil}

%meson_build


%install
%meson_install

mv %{buildroot}%{_datadir}/vulkan/implicit_layer.d/mangohud.json \
   %{buildroot}%{_datadir}/vulkan/implicit_layer.d/mangohud.%{_arch}.json


%files
%license LICENSE
%doc README.md bin/%{pkgname}.conf
%{_libdir}/%{name}/lib%{pkgname}.so
%{_datadir}/vulkan/implicit_layer.d/mangohud.%{_arch}.json


%changelog
* Fri Feb 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2.0-1
- 0.2.0

* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.1.0-1.20200205git420c26a
- Initial spec
