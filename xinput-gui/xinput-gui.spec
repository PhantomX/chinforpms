%global commit 2b0f02b3c2fbcd76bc6d1fd680217c73f6ac5752
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180709
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           xinput-gui
Version:        0.3.1
Release:        1%{?gver}%{?dist}
Summary:        A simple GUI for Xorg's Xinput tool

License:        GPLv3
URL:            https://github.com/IvanFon/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
Requires:       gtk3
Requires:       python3
Requires:       %{py3_dist pygobject}
Requires:       xorg-x11-server-utils
#Requires:       hicolor-icon-theme


%description
xinput allows you to edit properties of devices like keyboards, mice,
and touchpads. This GUI wraps around the xinput command to make editing
them faster and more user-friendly.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif


%build
%py3_build


%install
%py3_install

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=XInput GUI
Comment=A simple GUI for Xorg's Xinput tool
Exec=%{name}
Icon=image-missing
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;
EOF


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/xinput_gui/
%{python3_sitelib}/xinput_gui-*.egg-info
%{_datadir}/applications/%{name}.desktop


%changelog
* Mon Aug 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3.1-1
- 0.3.1

* Wed Jul 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.1.1-1.20180709git2b0f02b
- Initial spec
