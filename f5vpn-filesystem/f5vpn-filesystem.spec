%global pkgname f5vpn

Name:           %{pkgname}-filesystem
Version:        1
Release:        1%{?dist}
Summary:        f5vpn filesytem layout

License:        LicenseRef-Fedora-Public-Domain

Source0:        %{pkgname}-sysusers.conf

BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}
%{?systemd_requires}


%description
This package provides some directories required by packages which use F5 SSL VPN
technologies.


%prep

%build

%install
mkdir -p %{buildroot}%{_localstatedir}/log/%{pkgname}
chmod 0700 %{buildroot}%{_localstatedir}/log/%{pkgname}

mkdir -p %{buildroot}/run/%{pkgname}/
chmod 0700 %{buildroot}/run/%{pkgname}/

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{pkgname}.conf <<EOF
d /run/%{pkgname} 0700 root root -
EOF

mkdir -p %{buildroot}%{_libexecdir}/%{pkgname}/var
ln -sf ../../../../var/log/%{pkgname} %{buildroot}%{_libexecdir}/%{pkgname}/var/log
ln -sf ../../../../run/%{pkgname} %{buildroot}%{_libexecdir}/%{pkgname}/var/run

install -Dpm 644 %{S:0} %{buildroot}%{_sysusersdir}/%{pkgname}.conf


%pre
%sysusers_create_compat %{S:0}


%files
%{_tmpfilesdir}/%{pkgname}.conf
%{_sysusersdir}/%{pkgname}.conf
%{_libexecdir}/%{pkgname}/var/log
%{_libexecdir}/%{pkgname}/var/run
%dir /run/%{pkgname}/
%dir %{_localstatedir}/log/%{pkgname}/


%changelog
* Mon Jul 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1-1
- Initial spec
