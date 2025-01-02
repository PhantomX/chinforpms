%global appname com.dec05eba.gpu_screen_recorder
%global vc_url  https://git.dec05eba.com/%{name}

Name:           gpu-screen-recorder-gtk
Version:        5.0.0
Release:        1%{dist}
Summary:        GTK frontend for GPU Screen Recorder

License:        GPL-3.0-or-later
URL:            %{vc_url}/about

Source0:        https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       gpu-screen-recorder%{?_isa}


%description
%{summary}.


%prep
%autosetup -c -p1

sed -e '/gnome/d' -i meson.build


%build
%meson
%meson_build


%install
%meson_install

%check
%meson_test
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/*/*%{appname}*
%{_metainfodir}/%{appname}.appdata.xml


%changelog
* Wed Jan 01 2025 Phantom X <megaphantomx at hotmail dot com> - 5.0.0-1
- Initial spec
