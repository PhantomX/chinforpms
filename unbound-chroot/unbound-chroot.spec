Name:           unbound-chroot
Version:        1
Release:        1%{?dist}
Summary:        Helps running unbound under chroot

License:        LicenseRef-Fedora-Public-Domain
URL:            https://github.com/PhantomX

BuildArch:      noarch

BuildRequires:  systemd
Requires:       /usr/bin/mount
Requires:       unbound
%{?systemd_requires}

%description
%{name} contains systemd files to help running unbound under chroot.


%prep

%build

%install

mkdir -p %{buildroot}%{_unitdir}/unbound.service.d
cat > %{buildroot}%{_unitdir}/%{name}.service <<'EOF'
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/mount --bind /etc/pki/ca-trust/extracted/pem /etc/unbound/ssl
ExecStart=/usr/bin/mount --bind %{_sharedstatedir}/unbound /etc/unbound%{_sharedstatedir}/unbound
ExecStop=/usr/bin/umount /etc/unbound/ssl
ExecStop=/usr/bin/umount /etc/unbound%{_sharedstatedir}/unbound
EOF

cat > %{buildroot}%{_unitdir}/unbound.service.d/%{name}.conf <<'EOF'
[Unit]
After=unbound-chroot.service
Requires=unbound-chroot.service
EOF

mkdir -p %{buildroot}%{_sysconfdir}/unbound/ssl
mkdir -p %{buildroot}%{_sysconfdir}/unbound/%{_sharedstatedir}/unbound


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%dir %{_sysconfdir}/unbound/ssl
%dir %attr(0755,unbound,unbound) %{_sysconfdir}/unbound%{_sharedstatedir}/unbound
%{_unitdir}/%{name}.service
%{_unitdir}/unbound.service.d/%{name}.conf


%changelog
* Wed Nov 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1-1
- Initial spec

