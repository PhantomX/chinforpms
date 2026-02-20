%global vc_url  https://git.dec05eba.com/%{name}

Name:           gpu-screen-recorder-ui
Version:        1.10.8
Release:        1%{dist}
Summary:        A fullscreen overlay UI for GPU Screen Recorder

License:        GPL-3.0-or-later
URL:            %{vc_url}/about

Source0:        https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz

Patch0:         0001-Use-system-fonts.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  fonts-srpm-macros
BuildRequires:  systemd
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
# mglpp
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)

Requires:       google-noto-sans-fonts
Requires:       gpu-screen-recorder%{?_isa}
Requires:       gpu-screen-recorder-notification%{?_isa}

Provides:       bundled(mglpp) = 1.0.0


%description
GPU Screen Recorder UI is a fullscreen overlay UI for GPU Screen Recorder in
the style of ShadowPlay.


%prep
%autosetup -c -p1

cp -p depends/mglpp/depends/mgl/LICENSE LICENSE.mglpp

rm -rf fonts
sed \
  -e "/'fonts'/d" \
  -e '/update_desktop_database/d' \
  -i meson.build
sed -e 's|_RPM_FONTDIR_|%{_fontbasedir}/google-noto|g' -i src/Theme.cpp


%build
%meson \
  -Dcapabilities=false \
%{nil}

%meson_build


%install
%meson_install


%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/gpu-screen-recorder.desktop


%files
%license LICENSE LICENSE.mglpp
%doc README.md
%caps(cap_setuid+ep) %{_bindir}/gsr-global-hotkeys
%{_bindir}/gsr-hyprland-helper
%{_bindir}/gsr-kwin-helper
%{_bindir}/gsr-ui
%{_bindir}/gsr-ui-cli
%{_datadir}/gsr-ui
%{_datadir}/applications/gpu-screen-recorder.desktop
%{_datadir}/icons/hicolor/*/*/gpu-screen-recorder.*
%{_userunitdir}/%{name}.service


%changelog
* Tue Feb 17 2026 Phantom X <megaphantomx at hotmail dot com> - 1.10.8-1
- 1.10.8

* Sat Feb 07 2026 Phantom X <megaphantomx at hotmail dot com> - 1.10.7-1
- 1.10.7

* Tue Sep 16 2025 Phantom X <megaphantomx at hotmail dot com> - 1.7.5-1
- 1.7.5

* Sat May 17 2025 Phantom X <megaphantomx at hotmail dot com> - 1.6.3-1
- 1.6.3

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.3.0-1
- 1.3.0

* Wed Jan 01 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.3-1
- Initial spec
