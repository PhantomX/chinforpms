# Binary package, no debuginfo should be generated
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

Name:           wine-mono
Version:        4.7.5
Release:        100%{?dist}
Summary:        Mono library required for Wine

License:        GPLv2 and LGPLv2 and MIT and BSD and MS-PL and MPLv1.1
URL:            http://wiki.winehq.org/Mono

Source0:        http://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-%{version}.msi
Source1:        https://github.com/madewokherd/wine-mono/raw/master/COPYING
Source2:        https://github.com/madewokherd/wine-mono/raw/master/README

# see git://github.com/madewokherd/wine-mono

BuildArch:      noarch
ExcludeArch:    %{power64} s390x s390

Requires:       wine-filesystem

%description
Windows Mono library required for Wine.

%prep
%setup -c -T

cp -p %{S:1} %{S:2} .

%build

%install
mkdir -p %{buildroot}%{_datadir}/wine/mono
install -p -m 0644 %{S:0} \
    %{buildroot}%{_datadir}/wine/mono/%{name}-%{version}.msi


%files
%license COPYING
%doc README
%{_datadir}/wine/mono/%{name}-%{version}.msi


%changelog
* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.7.5-100
- 4.7.5
