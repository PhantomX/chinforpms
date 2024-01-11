# Binary packaging only, rust is hateful

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch aarch64
%global parch arm64
%else
%global parch amd64
%endif

%global vc_url  https://github.com/rustdesk/%{name}
%global rustdesk_id dbab22cbbcc51e5c188e76d4bffdcc331fab7e55

Name:           rustdesk-server
Version:        1.1.9
Release:        1%{?dist}
Summary:        RustDesk server program

License:        AGPL-3.0-only
URL:            https://rustdesk.com/

Source0:        %{vc_url}/releases/download/%{version}/%{name}-linux-%{parch}.zip#/%{name}-%{version}-linux-%{parch}.zip
Source1:        %{vc_url}/raw/%{rustdesk_id}/LICENSE
Source2:        %{vc_url}/raw/%{rustdesk_id}/README.md
Source3:        %{name}-hbbr.service
Source4:        %{name}-hbbs.service
Source5:        %{name}-sysusers.conf
Source6:        %{name}.firewalld

ExclusiveArch:  x86_64 arm64

BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}
%{?systemd_requires}

%description
Self-host your own RustDesk server, it is free and open source.

%prep
%autosetup -c

cp -p %{S:1} %{S:2} .

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{parch}/hbbr %{buildroot}%{_bindir}/
install -pm0755 %{parch}/hbbs %{buildroot}%{_bindir}/
install -pm0755 %{parch}/rustdesk-utils %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

install -Dpm 644 %{S:5} %{buildroot}%{_sysusersdir}/%{name}.conf

mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services
install -pm0644 %{S:6} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml


%pre
%sysusers_create_compat %{S:5}

%preun
%systemd_preun %{name}-hbbr.service
%systemd_preun %{name}-hbbs.service

%post
%systemd_post %{name}-hbbr.service
%systemd_post %{name}-hbbs.service

%postun
%systemd_postun %{name}-hbbr.service
%systemd_postun %{name}-hbbs.service


%files
%license LICENSE
%doc README.md
%{_bindir}/hbbr
%{_bindir}/hbbs
%{_bindir}/rustdesk-utils
%{_sysusersdir}/%{name}.conf
%dir %attr(0751, %{name}, %{name}) %{_localstatedir}/lib/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml


%changelog
* Tue Jan 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.1.9-1
- 1.1.9

* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.6-1
- Initial spec
