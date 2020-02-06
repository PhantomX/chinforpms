%global commit 420c26a08aa5043a533ccf5d275173d73388d60c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200205
%global with_snapshot 1

%global commit1 6c1a73774dabd2be64f85543b1286e44632d1905
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 flightlessmango-ImGui

%global commit2 fbe9fa0b6754ea98fc10df6a372cb5fcb8e565f4
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 Vulkan-Docs

%global commit3 7264358702061d3ed819d62d3d6fd66ab1da33c3
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 Vulkan-Headers

%global commit4 44ac9b2f406f863c69a297a77bd23c28fa29e78d
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 Vulkan-Loader

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname MangoHud
%global vc_url https://github.com/flightlessmango

Name:           mangohud
Version:        0.1.0
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
Source2:        https://github.com/KhronosGroup/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/KhronosGroup/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/KhronosGroup/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz

Patch10:        0001-Change-Hud-toggle-to-F10-key.patch


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  glslang
BuildRequires:  libXNVCtrl-devel
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3
BuildRequires:  python3-mako
#BuildRequires:  vulkan-headers
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
tar -xf %{S:2} -C modules/Vulkan-Docs --strip-components 1
tar -xf %{S:3} -C modules/Vulkan-Headers --strip-components 1
tar -xf %{S:4} -C modules/Vulkan-Loader --strip-components 1

#ln -sf %{_includedir}/vulkan modules/Vulkan-Headers/include

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

%meson --libdir=%{_libdir}/%{name}

%meson_build


%install
%meson_install

mv %{buildroot}%{_datadir}/vulkan/implicit_layer.d/mangohud.json \
   %{buildroot}%{_datadir}/vulkan/implicit_layer.d/mangohud.%{_arch}.json


%files
%license LICENSE
%doc README.md
%{_libdir}/%{name}/lib%{pkgname}.so
%{_datadir}/vulkan/implicit_layer.d/mangohud.%{_arch}.json


%changelog
* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.1.0-1.20200205git420c26a
- Initial spec
