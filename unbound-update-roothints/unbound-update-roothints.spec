Name:           unbound-update-roothints
Version:        1.1
Release:        1%{?dist}
Summary:        Updates unbound root-hints file

License:        Public Domain
URL:            https://github.com/PhantomX

BuildArch:      noarch

BuildRequires:  systemd
Requires:       coreutils
Requires:       curl
Requires:       unbound
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
unbound-update-roothints contains systemd timer files to update unbound
root-hints file.

%prep

%build

%install

# Adapted from https://wiki.archlinux.org/index.php/unbound#Roothints_systemd_timer

mkdir -p %{buildroot}%{_unitdir}
cat > %{buildroot}%{_unitdir}/%{name}.service <<'EOF'
[Unit]
Description=Update root hints for unbound
After=network.target network-online.target nss-lookup.target

[Service]
Type=oneshot
ExecStart=%{_bindir}/curl -o %{_sharedstatedir}/unbound/root.hints https://www.internic.net/domain/named.cache
ExecStartPost=-%{_bindir}/chown unbound. %{_sharedstatedir}/unbound/root.hints
EOF

cat > %{buildroot}%{_unitdir}/%{name}.timer <<'EOF'
[Unit]
Description=Run root.hints monthly
Wants=network-online.target

[Timer]
OnCalendar=monthly
Persistent=true
Unit=%{name}.service

[Install]
WantedBy=timers.target
EOF

%post
%systemd_post %{name}.timer

%preun
%systemd_preun %{name}.timer

%postun
%systemd_postun_with_restart %{name}.timer

%files
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer


%changelog
* Fri Mar 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1-1
- Run after network-online.target

* Fri Jun 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1
- First spec
