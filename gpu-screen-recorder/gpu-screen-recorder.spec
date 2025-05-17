%global vc_url  https://git.dec05eba.com/%{name}

Name:           gpu-screen-recorder
Version:        5.5.3
Release:        1%{dist}
Summary:        A shadowplay-like screen recorder

License:        GPL-3.0-or-later
URL:            %{vc_url}/about

Source0:        https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  systemd
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  cmake(VulkanHeaders)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)

Suggests:       (mesa-va-drivers or mesa-va-drivers-freeworld)
Suggests:       libva-intel-driver
Suggests:       intel-media-driver


%description
GPU Screen Recorder is a screen recorder that has minimal impact on system
performance by recording your monitor using the GPU only.


%prep
%autosetup -c -p1

%build
%meson \
  -Dcapabilities=false \
%{nil}

%meson_build


%install
%meson_install

%check
%meson_test


%files
%license LICENSE
%doc README.md
%{_bindir}/gpu-screen-recorder
%{_bindir}/gsr-dbus-server
%caps(cap_sys_admin+ep) %{_bindir}/gsr-kms-server
%{_modprobedir}/gsr-nvidia.conf
%{_userunitdir}/%{name}.service


%changelog
* Sat May 17 2025 Phantom X <megaphantomx at hotmail dot com> - 5.5.3-1
- 5.5.3

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 5.3.3-1
- 5.3.3

* Wed Jan 01 2025 Phantom X <megaphantomx at hotmail dot com> - 5.0.0-1
- Initial spec
