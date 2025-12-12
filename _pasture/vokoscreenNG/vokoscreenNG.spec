%global forgeurl https://github.com/vkohaupt/%{name}

Name:           vokoscreenNG
Version:        4.7.3
%forgemeta
Release:        100%{?dist}
Summary:        Powerful screencast creator to record the screen

License:        GPL-2.0-only
URL:            %{forgeurl}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# AppData manifest
Source1:        https://raw.githubusercontent.com/flathub/com.github.vkohaupt.%{name}/master/%{name}.appdata.xml

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  make

BuildRequires:  cmake(Qt6) >= 6.6
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)

BuildRequires:  pkgconfig(gstreamermm-1.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)
# Player
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)

%if 0%{?fedora} >= 38
Requires:       gstreamer1-plugin-gif
%endif

%description
vokoscreenNG for Windows and Linux is a powerful screencast creator in many
languages to record the screen, an area or a window (Linux only). Recording of
audio from multiple sources is supported. With the built-in camera support,
you can make your video more personal. Other tools such as systray, magnifying
glass, countdown, timer, Showclick and Halo support will help you do a good
job.


%prep
%forgeautosetup -p1
mkdir -p src/%{_target_platform}


%build
pushd src/%{_target_platform}
%qmake_qt6 ..
popd
%make_build -C src/%{_target_platform}


%install
%make_install -C src/%{_target_platform}
install -D -p -m 0755 src/%{_target_platform}/%{name} \
    %{buildroot}%{_bindir}/%{name}

# Desktop file
install -D -p -m 0644 src/applications/%{name}.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

# AppData manifest
install -D -p -m 0644 %{SOURCE1} -t %{buildroot}%{_metainfodir}/

# Icon
install -D -p -m 0644 src/applications/%{name}.png \
    %{buildroot}%{_datadir}/pixmaps/%{name}.png


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%license COPYING
%doc .github/README.md info-licences-changelog-install/CHANGELOG.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_metainfodir}/*.xml


%changelog
* Sat Dec 06 2025 Phantom X <megaphantomx at hotmail dot com> - 4.7.3-100
- 4.7.3

* Sat Dec 06 2025 Phantom X <megaphantomx at hotmail dot com> - 4.7.1-100
- 4.7.1

* Fri Nov 14 2025 Phantom X <megaphantomx at hotmail dot com> - 4.7.0-100
- 4.7.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 29 2025 Packit <hello@packit.dev> - 4.6.0-1
- Update to 4.6.0 upstream release
- Resolves: rhbz#2375397
