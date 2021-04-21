Name:           radeon-profile
Version:        20200824
Release:        2%{?dist}
Summary:        Simple application to read current clocks of ATi Radeon cards

License:        GPLv2
URL:            https://github.com/marazmista/%{name}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdrm_amdgpu)
BuildRequires:  pkgconfig(libdrm_radeon)
BuildRequires:  pkgconfig(Qt5Charts)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  qt5-linguist

Requires:       glx-utils
Requires:       hicolor-icon-theme
Requires:       radeon-profile-daemon
Requires:       xrandr


%description
%{summary}.


%prep
%autosetup


%build
pushd %{name}

lrelease-qt5 %{name}.pro
%qmake_qt5 %{name}.pro

%make_build

popd

%install
make install INSTALL_ROOT=%{buildroot} -C %{name}

mkdir -p %{buildroot}%{_datadir}/%{name}
install -pm0644 %{name}/translations/*.qm %{buildroot}%{_datadir}/%{name}/

desktop-file-edit \
  --remove-category="HardwareSettings" \
  --remove-category="TrayIcon" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/%{name}/


%changelog
* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 20200824-2
- Replace xorg-x11-server-utils BR

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 20200824-1
- 20200824

* Mon Sep 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190903-1
- Initial spec
