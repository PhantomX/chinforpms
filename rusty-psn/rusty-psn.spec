# Binary packaging only, rust is hateful

%global _build_id_links none
%undefine _debugsource_packages

%global vc_id   c5d2640a25137d55d8e9f01f6283ad209983df3d

Name:           rusty-psn
Version:        0.2.2
Release:        1%{?dist}
Summary:        Simple tool to grab updates for PS3 games

License:        MIT
URL:            https://github.com/RainbowCookie32/%{name}

Source0:        %{url}/releases/download/v%{version}/rusty-psn-cli-linux.zip#/%{name}-cli-%{version}-linux.zip
Source1:        %{url}/releases/download/v%{version}/rusty-psn-egui-linux.zip#/%{name}-egui-%{version}-linux.zip
Source2:        %{url}/raw/%{vc_id}/LICENSE
Source3:        %{url}/raw/%{vc_id}/README.md


%description
%{name} is a simple tool to grab updates for PS3 games.


%package egui
Summary:        Simple GUI tool to grab updates for PS3 games
Requires:       gnome-icon-theme

%description egui
%{name}-egui is a GUI simple tool to grab updates for PS3 games.


%prep
%autosetup -c -T
unzip -d cli %{S:0}
unzip -d egui %{S:1}

cp -p %{S:2} %{S:3} .


%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 cli/%{name} %{buildroot}%{_bindir}/%{name}
install -pm0755 egui/%{name} %{buildroot}%{_bindir}/%{name}-egui


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Name=%{name}-egui
Comment=Grab updates for PS3 games
Exec=%{name}-egui
Icon=applications-games
Terminal=false
Type=Application
Categories=Network;
EOF

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%files egui
%license LICENSE
%doc README.md
%{_bindir}/%{name}-egui
%{_datadir}/applications/%{name}.desktop


%changelog
* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2.2-1
- 0.2.2

* Thu Mar 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- Initial spec

