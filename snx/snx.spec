%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

Name:           snx
Version:        800007075
Release:        3%{?dist}
Summary:        Check Point SSL Network Extender (vpn client)

License:        Proprietary
URL:            https://www.checkpoint.com/

Source0:        https://starkers.keybase.pub/snx_install_linux30.sh?dl=1#/snx_install_linux30.sh
# https://www.checkpoint.com/support-services/software-license-agreement-limited-hardware-warranty/
Source1:        LICENSE
Source2:        snxrun.sh
Source3:        %{name}-sysusers.conf
Source4:        README.suid
Source5:        README.wrapper

ExclusiveArch:  %{ix86}

BuildRequires:  systemd


%description
%{summary}.


%package desktop
Summary:        Desktop helpers for snx startup
BuildArch:      noarch
Requires:       xterm
Requires:       gnome-icon-theme
Requires:       desktop-notification-daemon
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description desktop
This package contains desktop helpers for snx startup.


%prep
%setup -c -T

tail -n +$(head -n2 %{S:0} | grep ARCHIVE_OFFSET | cut -d= -f2) %{S:0} | tar xj

RVER="$(strings snx |grep '^Build Number=' | cut -d = -f2 )"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch. You have ${RVER} in %{S:0} instead %{version} "
  echo "Edit Version and try again"
  exit 1
fi

cat > snxrc <<'EOF'
server _PUT_SERVER_HERE_
username _PUT_USERNAME_HERE_
reauth yes
EOF

cp -p %{S:1} .
cp -p %{S:4} .
cp -p %{S:5} .
sed -e 's|_DOCDIR_|%{_docdir}/%{name}|g' -i README.wrapper

%build


%install

mkdir -p %{buildroot}%{_sbindir}
install -pm0755 %{name} %{buildroot}%{_sbindir}/

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
chmod 0700 %{buildroot}%{_localstatedir}/lib/%{name}

mkdir -p %{buildroot}%{_sysconfdir}
ln -sf ..%{_localstatedir}/lib/snx %{buildroot}%{_sysconfdir}/%{name}
ln -sf ../../../run/%{name} %{buildroot}%{_localstatedir}/lib/%{name}/tmp

mkdir -p %{buildroot}/run/%{name}/
chmod 0700 %{buildroot}/run/%{name}/

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d /run/snx 0700 root root -
EOF

install -Dpm 644 %{S:3} %{buildroot}%{_sysusersdir}/%{name}.conf

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{S:2} %{buildroot}%{_bindir}/snxrun


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/snxrun.desktop <<EOF
[Desktop Entry]
Name=Checkpoint VPN SSL Network Extender
Comment=Run or stop a running Checkpoint VPN SSL Network Extender
Comment[pt_BR]=Inicia ou para o Checkpoint VPN SSL Network Extender
Exec=snxrun
Terminal=false
Icon=applications-internet
Type=Application
Categories=Network;
EOF

%pre
%sysusers_create_package %{name} %{S:3}


%files
%license LICENSE
%doc snxrc README.*
%{_sysconfdir}/%{name}
%{_bindir}/snxrun
%attr(4750,root,%{name}) %{_sbindir}/%{name}
%dir /run/%{name}/
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%dir %{_localstatedir}/lib/%{name}/
%{_localstatedir}/lib/%{name}/tmp

%files desktop
%{_datadir}/applications/snxrun.desktop


%changelog
* Fri Mar 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 800007075-3
- suid and group

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 800007075-2
- Move transient files to /run and /var/lib

* Tue Mar 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 800007075-1
- Initial spec
