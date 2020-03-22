%global commit b17198e00a0614c23afef46a91708e27cc311af7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180501
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           snxvpn
Version:        1.2
Release:        2%{?gver}%{?dist}
Summary:        Command-line utility to connect to a Checkpoint SSL VPN 

License:        BSD
URL:            https://github.com/agnis-mateuss/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.sh
Source2:        README.wrapper

Patch0:         0001-Change-settings-to-HOME-.config.patch
Patch1:         0001-Hardcode-snx-path.patch

BuildArch:      noarch

BuildRequires:  python3-devel
Requires:       snx
Requires:       gnome-icon-theme
Requires:       desktop-notification-daemon
Requires:       python3-beautifulsoup4
Requires:       python3-crypto
Requires:       python3-lxml
Requires:       python3-soupsieve

Provides:       snxconnect = %{?epoch:%{epoch}:}%{version}-%{release}


%description
This is a project to connect to a Checkpoint SSL-VPN from a Linux client.
The current version of checkpoint SNX (SSL Network Extender) for Linux no longer
supports a command-line mode.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

cat > %{name}rc <<'EOF'
host _PUT_SERVER_HERE_
username _PUT_USERNAME_HERE_
password _PUT_PASSWORD_HERE_
save-cookies false
skip-cert true
EOF

cp -p %{S:2} .
sed -e 's|_DOCDIR_|%{_docdir}/%{name}|g' -i README.wrapper

echo 'VERSION="%{version}"' > snxvpnversion.py


%build
%py3_build


%install
%py3_install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{S:1} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=SNX-VPN
Comment=Run or stop a running SNX-VPN
Comment[pt_BR]=Inicia ou para o SNX-VPN
Exec=%{name}
Terminal=false
Icon=applications-internet
Type=Application
Categories=Network;
EOF


%files
%license LICENSE.TXT
%doc README.* %{name}rc
%{_bindir}/snxconnect
%{_bindir}/%{name}
%{python3_sitelib}/snxconnect.py
%{python3_sitelib}/snxvpnversion.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/*-*.egg-info
%{_datadir}/applications/%{name}.desktop


%changelog
* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2-2.20180501gitb17198e
- Fix %%{python3_sitelib}/__pycache__/ owning

* Fri Mar 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2-1.20180501gitb17198e
- Initial spec
