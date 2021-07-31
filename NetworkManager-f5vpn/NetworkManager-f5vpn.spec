Name:           NetworkManager-f5vpn
Version:        0.4
Release:        1%{?dist}
Summary:        NetworkManager VPN plugin for F5 SSL VPN

License:        GPLv2+
URL:            https://github.com/ohwgiles/%{name}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
Source2:        nmf5vpnservice.te

%global ppp_version %(sed -n 's/^#define\\s*VERSION\\s*"\\([^\\s]*\\)"$/\\1/p' %{_includedir}/pppd/patchlevel.h 2>/dev/null | grep . || echo bad)

BuildRequires:  checkpolicy
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  policycoreutils
BuildRequires:  ppp-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libnm)

Requires:       NetworkManager >= 1:1.2.0
Requires:       ppp = %{ppp_version}
Requires:       openssl
Requires(post): policycoreutils
Requires(preun): policycoreutils


%description
%{summary}.


%prep
%autosetup -p1

cp -p %{S:1} COPYING

cp -p %{S:2} .

sed \
  -e 's|lib/pppd|lib${LIB_SUFFIX}/pppd/%{ppp_version}|g' \
  -e '/libraries(f5vpn-cli/a install(TARGETS f5vpn-cli DESTINATION bin)' \
  -i CMakeLists.txt

sed -e 's|/usr/bin/pppd|%{_sbindir}/pppd|g' -i lib/f5vpn_connect.c


%build
%cmake \
  -DWITH_NM_PLUGIN:BOOL=ON \
  -DWITH_CLI_TOOL:BOOL=ON \
%{nil}

%cmake_build

checkmodule -M -m -o nmf5vpnservice.mod nmf5vpnservice.te
semodule_package -o nmf5vpnservice.pp -m nmf5vpnservice.mod


%install
%cmake_install

mkdir -p %{buildroot}%{_datadir}/%{name}
install -pm0644 nmf5vpnservice.{te,pp} %{buildroot}%{_datadir}/%{name}/


%preun
%systemd_preun %{name}d.service
/usr/sbin/semodule --remove nmf5vpnservice >/dev/null 2>&1 || :

%post
/usr/sbin/semodule --install %{_datadir}/%{name}/nmf5vpnservice.pp >/dev/null 2>&1 || :


%files
%license COPYING
%doc README
%{_bindir}/f5vpn-cli
%{_libdir}/NetworkManager/libnm-vpn-plugin-f5vpn.so
%{_datadir}/applications/nm-f5vpn-xdg-helper.desktop
%{_datadir}/dbus-1/system.d/nm-f5vpn-service.conf
%{_prefix}/lib/NetworkManager/VPN/nm-f5vpn-service.name
%{_libexecdir}/nm-f5vpn-auth-dialog
%{_libexecdir}/nm-f5vpn-service
%{_libexecdir}/nm-f5vpn-xdg-helper
%{_libdir}/pppd/%{ppp_version}/libpppd-plugin-f5vpn.so
%{_datadir}/%{name}/nmf5vpnservice.*


%changelog
* Thu Jul 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.4-1
- 0.4

* Tue Jun 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3-1
- Initial spec
