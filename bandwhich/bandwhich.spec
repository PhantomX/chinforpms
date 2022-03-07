# Binary packaging only, rust is hateful

%undefine _debugsource_packages

%global vc_id   acd1b0a95dbc2ee245648f2d5ef75494cf1cba54

Name:           bandwhich
Version:        0.20.0
Release:        1%{?dist}
Summary:        Terminal bandwidth utilization tool

License:        MIT
URL:            https://github.com/imsnif/%{name}

Source0:        %{url}/releases/download/%{version}/%{name}-v%{version}-x86_64-unknown-linux-musl.tar.gz
Source1:        %{url}/raw/%{vc_id}/LICENSE.md
Source2:        %{url}/raw/%{vc_id}/README.md
Source3:        %{url}/raw/%{vc_id}/docs/%{name}.1

ExclusiveArch:  x86_64

%description
%{name} is a CLI utility for displaying current network utilization by process,
connection and remote IP/hostname.


%prep
%autosetup -c

cp -p %{S:1} %{S:2} %{S:3} .


%build


%install
mkdir -p %{buildroot}%{_sbindir}
install -pm0755 %{name} %{buildroot}%{_sbindir}/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 %{name}.1 %{buildroot}%{_mandir}/man1/


%files
%license LICENSE.md
%doc README.md
%{_sbindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Feb 18 2022 Phantom X <megaphantomx at hotmail dot com> - 0.20.0-1
- Initial spec