%global commit 22ea668aa4ecf848149ea4c150aa840a25dc6ff8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220703
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global appdata_id org.rnd2.cpupower_gui
%global files_id org.rnd2.cpupower-gui

Name:           cpupower-gui
Version:        1.0.0
Release:        1%{?gver}%{?dist}
Summary:        A GUI utility to set CPU frequency limits

License:        GPLv3
URL:            https://github.com/vagnum08/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz
%endif

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  python-devel
BuildRequires:  systemd-rpm-macros
Requires:       glib2
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       kernel-tools
Requires:       libappindicator-gtk3
Requires:       libhandy
Requires:       polkit
Requires:       PolicyKit-authentication-agent
Requires:       %{py3_dist dbus-python}
Requires:       python3-gobject
Requires:       %{py3_dist pyxdg}
%{?systemd_requires}


%description
%{name} is designed to allow you to change the frequency limits of your cpu and
its governor. The application is similar in functionality to cpupower.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1


%build
%meson \
  -Duse_libexec=true \
%{nil}

%meson_build


%install
%meson_install


%find_lang %{name} --with-man

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appdata_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appdata_id}.appdata.xml


%preun
%systemd_preun %{name}-helper.service %{name}.service

%post
%systemd_post %{name}-helper.service %{name}.service

%postun
%systemd_postun %{name}-helper.service %{name}.service


%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md
%dir %{_sysconfdir}/cpupower_gui.d
%{_sysconfdir}/cpupower_gui.d/my_profile.profile.ex
%{_sysconfdir}/cpupower_gui.d/README
%config(noreplace) %{_sysconfdir}/cpupower_gui.conf
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-helper.service
%{_userunitdir}/%{name}-user.service
%{_datadir}/dbus-1/services/%{appdata_id}.service
%{_datadir}/dbus-1/system.d/%{appdata_id}.helper.conf
%{_datadir}/dbus-1/system-services/%{appdata_id}.helper.service
%{_datadir}/glib-2.0/schemas/%{appdata_id}.gschema.xml
%{_datadir}/polkit-1/actions/%{files_id}.policy
%{_datadir}/polkit-1/rules.d/%{files_id}.rules
%{_datadir}/applications/%{appdata_id}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appdata_id}.*
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/%{appdata_id}.appdata.xml


%changelog
* Wed Feb 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-1.20220118git97f8ac0
- Initial spec
