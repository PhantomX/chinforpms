%global vc_url  https://git.dec05eba.com/%{name}

Name:           gpu-screen-recorder-notification
Version:        1.0.8
Release:        1%{dist}
Summary:        A notification in the style of ShadowPlay

License:        GPL-3.0-or-later
URL:            %{vc_url}/about

Source0:        https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz

Patch0:         0001-Use-system-fonts.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  fonts-srpm-macros
BuildRequires:  pkgconfig(xext)
# mglpp
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)

Requires:       google-noto-sans-fonts

Provides:       bundled(mglpp) = 1.0.0


%description
GPU Screen Recorder Notification is a notification in the style of ShadowPlay.


%prep
%autosetup -c -p1

cp -p depends/mglpp/depends/mgl/LICENSE LICENSE.mglpp

rm -rf fonts
sed -e "/'fonts'/d" -i meson.build
sed -e 's|_RPM_FONTDIR_|%{_fontbasedir}/google-noto|g' -i src/main.cpp


%build
%meson
%meson_build


%install
%meson_install


%check
%meson_test

%files
%license LICENSE LICENSE.mglpp
%doc README.md
%{_bindir}/gsr-notify
%{_datadir}/gsr-notify


%changelog
* Tue Sep 16 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.8-1
- 1.0.8

* Sat May 17 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.7-1
- 1.0.7

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.4-1
- 1.0.4

* Wed Jan 01 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-1
- Initial spec
