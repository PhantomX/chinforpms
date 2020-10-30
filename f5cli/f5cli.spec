# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global vc_id  9ea8593c72570211488943b1286317b239222def
%global vc_url  https://github.com/zrhoffman/f5vpn-arch/raw/%{vc_id}
#global dl_url  https://connect.healthsystem.virginia.edu/public/download
%global dl_url  https://vpn.brown.edu/public/download

Name:           f5cli
Version:        7210.2020.0826
Release:        1%{?dist}
Summary:        F5 Command Line VPN Client

# See LICENSE
License:        Proprietary
URL:            https://www.f5.com/

Source0:        %{dl_url}/linux_f5cli.x86_64.rpm#/%{name}-%{version}.x86_64.rpm

Source1:        %{vc_url}/LICENSE
Source3:        README.suid

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  execstack
Requires:       f5vpn-filesystem


%description
BIG-IP Command Line VPN Client for Linux to establish network access.


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

cp %{S:1} %{S:3} .

execstack -c usr/local/lib/F5Networks/f5fpc_x86_64
execstack -c usr/local/lib/F5Networks/SSLVPN/svpn_x86_64

# Ugly hack to make it respect FHS (recount \x00, if edit)
sed \
  -e 's,/usr/local/lib/F5Networks/SSLVPN/svpn_x86_64,%{_libexecdir}/f5vpn/svpn_x86_64\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,g' \
  -e 's,/usr/local/lib/F5Networks/SSLVPN/var/run/svpn.pid,%{_rundir}/f5vpn/svpn.pid\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,g' \
  -e 's,/usr/local/ssl/certs,%{_sysconfdir}/ssl/certs\x00\x00\x00\x00\x00\x00,g' \
  -i usr/local/lib/F5Networks/f5fpc_x86_64 usr/local/lib/F5Networks/SSLVPN/svpn_x86_64


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/local/lib/F5Networks/f5fpc_x86_64 %{buildroot}%{_bindir}/f5fpc

mkdir -p %{buildroot}%{_libexecdir}/f5vpn
install -pm0755 usr/local/lib/F5Networks/SSLVPN/svpn_x86_64 \
  %{buildroot}%{_libexecdir}/f5vpn/svpn_x86_64

%files
%license LICENSE
%doc README.suid
%caps(cap_kill+ep) %{_bindir}/f5fpc
%attr(4750,root,f5vpn) %{_libexecdir}/f5vpn/svpn_x86_64


%changelog
* Wed Oct 14 2020 - 7210.2020.0826-1
- 7210.2020.0826

* Wed May 20 2020 - 7190.2020.0221.1-1
- Initial spec
