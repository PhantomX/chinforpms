# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global optdir  opt/f5/vpn

%global vc_id  9ea8593c72570211488943b1286317b239222def
%global vc_url  https://github.com/zrhoffman/f5vpn-arch/raw/%{vc_id}
#global dl_url  https://connect.healthsystem.virginia.edu/public/download
%global dl_url  https://vpn.brown.edu/public/download

Name:           f5vpn
Version:        7210.2020.0826.1
Release:        1%{?dist}
Summary:        F5 SSL VPN (vpn client)

# See LICENSE
License:        Proprietary
URL:            https://www.f5.com/

Source0:        %{dl_url}/linux_f5vpn.x86_64.rpm#/%{name}-%{version}.x86_64.rpm

Source1:        %{vc_url}/LICENSE
Source2:        %{vc_url}/README.rst
Source3:        %{name}run
Source5:        README.suid

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  execstack
Requires:       f5vpn-filesystem
Requires:       zenity
Requires:       hicolor-icon-theme

Provides:       bundled(libssl) = 1.0.0

%global __provides_exclude_from ^/%{optdir}/.*

%global __requires_exclude ^libssl.so.*
%global __requires_exclude %__requires_exclude|^libcrypto.so.*
%global __requires_exclude %__requires_exclude|^libicu.*.so.*
%global __requires_exclude %__requires_exclude|^libQt.*.so.*


%description
F5 VPN can establish SSL VPN network access connection with F5 BIG-IP APM.


%prep
%setup -c -T

RVER="$(rpm -qp --qf %%{version} %{SOURCE0} 2> /dev/null)"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch"
  echo "You have ${RVER} in %{SOURCE0} instead %{version} "
  echo "Edit VERSION variable and try again"
  exit 1
fi

%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp %{S:1} %{S:2} %{S:5} .

find opt/f5 -name '*.so*' | xargs chmod 0755

execstack -c %{optdir}/svpn
execstack -c %{optdir}/tunnelserver

# Ugly hack to make it respect FHS (a little)
sed \
  -e 's,/usr/local/lib/F5Networks/SSLVPN/var/run/svpn.pid,%{_rundir}/f5vpn/svpn.pid\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,g' \
  -i %{optdir}/f5vpn %{optdir}/svpn

sed \
  -e 's,/usr/local/ssl/certs,%{_sysconfdir}/ssl/certs\x00\x00\x00\x00\x00\x00,g' \
  -i %{optdir}/tunnelserver

cp -p %{optdir}/com.f5.f5vpn.desktop %{optdir}/com.f5.f5vpnrun.desktop


%build


%install

mkdir -p %{buildroot}/%{optdir}/{lib,platforms}
for i in %{name} svpn tunnelserver ;do
  install -pm0755 %{optdir}/$i %{buildroot}/%{optdir}/
done

for i in %{optdir}/lib/*.so* ;do
  install -pm0755 $i %{buildroot}/%{optdir}/lib/
done

for i in %{optdir}/platforms/*.so* ;do
  install -pm0755 $i %{buildroot}/%{optdir}/platforms/
done

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh

RPMDIR="/%{optdir}"

if [ "x${F5VPNVERBOSE}" = "x" ] ;then
  exec 1>/dev/null 2>&1
fi

exec ${RPMDIR}/%{name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/dbus-1/services
install -pm0644 %{optdir}/com.f5.f5vpn.service \
  %{buildroot}%{_datadir}/dbus-1/services/

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{S:3} %{buildroot}%{_bindir}/%{name}run

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --mode=0644 \
  --set-key=NoDisplay \
  --set-value=true \
  %{optdir}/com.f5.f5vpn.desktop

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --mode=0644 \
  --set-key=Name \
  --set-value="F5 VPN Runner" \
  --set-key=Exec \
  --set-value="%{name}run" \
  --remove-key=DBusActivatable \
  --remove-key=MimeType \
  %{optdir}/com.f5.f5vpnrun.desktop

for res in 16 24 32 48 64 96 128 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 %{optdir}/logos/${res}x${res}.png ${dir}/%{name}.png
done


%files
%license LICENSE
%doc README.rst README.suid
%{_bindir}/%{name}
%{_bindir}/%{name}run
%caps(cap_kill+ep) /%{optdir}/%{name}
%attr(4750,root,%{name}) /%{optdir}/svpn
/%{optdir}/tunnelserver
/%{optdir}/lib/*.so*
/%{optdir}/platforms/*.so*
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/*x*/apps/%{name}.png


%changelog
* Wed Oct 14 2020 - 7210.2020.0826.1-1
- 7210.2020.0826.1

* Mon Jul 06 2020 - 7190.2020.0221.1-2
- R: f5vpn-filesystem

* Wed May 20 2020 - 7190.2020.0221.1-1
- Initial spec
