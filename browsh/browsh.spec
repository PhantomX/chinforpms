%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

Name:           browsh
Version:        1.6.4
Release:        1%{?dist}
Summary:        A text-based browser

License:        LGPLv2
URL:            https://www.brow.sh/

%global vc_url  https://github.com/browsh-org/%{name}
Source0:        %{vc_url}/releases/download/v%{version}/%{name}_%{version}_linux_amd64.rpm
Source1:        %{vc_url}/raw/master/LICENSE
Source2:        %{vc_url}/raw/master/README.md

ExclusiveArch:  x86_64

Requires:       firefox >= 63


%description
Browsh is a purely text-based browser that can run in most TTY terminal
environments and in any browser. The terminal client is currently more
advanced than the browser client.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp -p %{S:1} .
cp -p %{S:2} .

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/local/bin/%{name} %{buildroot}%{_bindir}/%{name}


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Fri Jun 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.6.4-1
- Initial spec.
