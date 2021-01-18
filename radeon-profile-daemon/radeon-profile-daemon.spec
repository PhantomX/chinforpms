Name:           radeon-profile-daemon
Version:        20190603
Release:        1%{?dist}
Summary:        Daemon for radeon-profile GUI 

License:        GPLv2
URL:            https://github.com/marazmista/%{name}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  systemd


%description
System daemon for reading info about Radeon GPU clocks and volts as well
as control card power profiles so the GUI radeon-profile application can
be run as normal user.


%prep
%autosetup


%build
pushd %{name}

%qmake_qt5 %{name}.pro

%make_build

popd

%install
make install INSTALL_ROOT=%{buildroot} -C %{name}


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service


%changelog
* Mon Sep 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190603-1
- Initial spec
