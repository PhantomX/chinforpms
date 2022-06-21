# Binary packaging only, go is hateful

%global _build_id_links none
%undefine _debugsource_packages

%global vc_url  https://github.com/yggdrasil-network/yggdrasil-go
%global vc_id   408d381591e99c273bf8db520a185478cdd8024f

%global pkgrel 1

Name:           yggdrasil
Version:        0.4.3
Release:        1%{?dist}
Summary:        End-to-end encrypted IPv6 networking

License:        GPLv3
URL:            https://yggdrasil-network.github.io

Source0:        %{vc_url}/releases/download/v%{version}/yggdrasil-%{version}-%{pkgrel}.x86_64.rpm
Source1:        %{vc_url}/raw/%{vc_id}/LICENSE
Source2:        %{vc_url}/raw/%{vc_id}/README.md
Source3:        %{name}-sysusers.conf
Source4:        %{vc_url}/raw/%{vc_id}/contrib/systemd/%{name}-default-config.service

ExclusiveArch:  x86_64

%{?systemd_requires}


%description
Yggdrasil is a proof-of-concept to explore a wholly different approach to
network routing. Whereas current computer networks depend heavily on very
centralised design and configuration, Yggdrasil breaks this mould by making
use of a global spanning tree to form a scalable IPv6 encrypted mesh network.


%prep
%autosetup -c -T

rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp -p %{S:1} %{S:2} .
cp -p %{S:4} .


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/bin/%{name} %{buildroot}%{_bindir}/
install -pm0755 usr/bin/%{name}ctl %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 etc/systemd/system/yggdrasil.service %{buildroot}%{_unitdir}/
install -pm0644 %{name}-default-config.service %{buildroot}%{_unitdir}/


%pre
%sysusers_create_compat %{SOURCE3}

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service


%files
%license LICENSE
%doc README.md
%{_bindir}/yggdrasil
%{_bindir}/yggdrasilctl
%{_unitdir}/%{name}-default-config.service
%{_unitdir}/%{name}.service


%changelog
* Fri Feb 18 2022 Phantom X <megaphantomx at hotmail dot com> - 0.4.3-1
- 0.4.3

* Sat Jan 15 2022 Phantom X <megaphantomx at hotmail dot com> - 0.4.2-1
- Initial spec

