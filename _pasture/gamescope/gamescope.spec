%global commit 8f9a284d32be04cf4a8e9bea23b872ab107bc377
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210312
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global perms_gs %caps(cap_sys_nice+ep)

Name:           gamescope
Version:        3.7.1
Release:        2%{?gver}%{?dist}
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/Plagman/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  meson >= 0.54.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(wlroots) >= 0.11.0
BuildRequires:  pkgconfig(libliftoff)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  /usr/bin/glslangValidator

Requires:       xorg-x11-server-Xwayland
Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%meson
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md
%{perms_gs} %{_bindir}/gamescope


%changelog
* Mon Mar 15 2021 Phantom X <megaphantomx at hotmail dot com> - 3.7.1-2.20210312git8f9a284
- Bump

* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 3.7.1-1.20210129gitc9acfb5
- 3.7.1 snapshot

* Mon Nov 02 2020 Phantom X <megaphantomx at hotmail dot com> - 3.7-2.20201023gitcd31090
- Snapshot

* Sun Oct  4 2020 Neal Gompa <ngompa13@gmail.com>
- Initial packaging
