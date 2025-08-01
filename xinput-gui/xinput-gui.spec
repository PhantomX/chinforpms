%global commit 2b0f02b3c2fbcd76bc6d1fd680217c73f6ac5752
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180709
%bcond snapshot 0

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           xinput-gui
Version:        0.3.1
Release:        3%{?dist}
Summary:        A simple GUI for Xorg's Xinput tool

License:        GPL-3.0-only
URL:            https://github.com/IvanFon/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
Requires:       gtk3
Requires:       python3
Requires:       %{py3_dist pygobject}
Requires:       xinput
#Requires:       hicolor-icon-theme


%description
xinput allows you to edit properties of devices like keyboards, mice,
and touchpads. This GUI wraps around the xinput command to make editing
them faster and more user-friendly.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

cat > %{name}.desktop <<EOF
[Desktop Entry]
Name=XInput GUI
Comment=A simple GUI for Xorg's Xinput tool
Exec=%{name}
Icon=input-keyboard
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;
EOF


%build
%py3_build


%install
%py3_install

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/xinput_gui/
%{python3_sitelib}/xinput_gui-*.egg-info
%{_datadir}/applications/%{name}.desktop


%changelog
* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.1-3
- BR: desktop-file-utils

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3.1-2
- Replace xorg-x11-server-utils BR

* Mon Aug 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3.1-1
- 0.3.1

* Wed Jul 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.1.1-1.20180709git2b0f02b
- Initial spec
