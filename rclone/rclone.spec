%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch x86_64
%global parch amd64
%else
%global parch i386
%endif

%global vc_url  https://github.com/%{name}/%{name}

Name:           rclone
Version:        1.52.3
Release:        1%{?dist}
Summary:        Rsync for cloud storage

License:        MIT
URL:            http://rclone.org/

Source0:        https://downloads.rclone.org/v%{version}/%{name}-v%{version}-linux-%{parch}.zip
Source1:        %{vc_url}/raw/master/COPYING
Source2:        %{vc_url}/raw/master/MANUAL.html
Source3:        %{vc_url}/raw/master/MANUAL.md

BuildRequires:  unzip


%description
Rclone is a command line program to sync files and directories to and
from various cloud services.


%prep
%autosetup -n %{name}-v%{version}-linux-%{parch}

cp -p %{S:1} %{S:2} %{S:3} .


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 %{name}.1 %{buildroot}%{_mandir}/man1/

%files
%license COPYING
%doc MANUAL.html MANUAL.md README.txt
%{_bindir}/rclone
%{_mandir}/man1/rclone.1*


%changelog
* Sat Aug 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1.52.3-1
- 1.52.3

* Sun Jun 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1.52.2-1
- Initial spec
