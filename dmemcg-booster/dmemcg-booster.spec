%bcond check 0

Name:           dmemcg-booster
Version:        0.1.2
Release:        1%{?dist}
Summary:        Service for enabling and controlling dmem cgroup limits

License:        MIT
URL:            https://gitlab.steamos.cloud/holo/%{name}

Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
BuildRequires:  pkgconfig(dbus-1)
%{?systemd_requires}


%description
%{name} is a service for enabling and controlling dmem cgroup limits for
boosting foreground games.


%prep
%autosetup -p1

%cargo_prep
%generate_buildrequires
%cargo_generate_buildrequires


%build
%cargo_build

%install
%cargo_install

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 %{name}-system.service %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_userunitdir}
install -pm0644 %{name}-user.service %{buildroot}%{_userunitdir}


%if %{with check}
%check
%cargo_test
%endif


%post
%systemd_post %{name}-system.service

%preun
%systemd_preun %{name}-system.service

%postun
%systemd_postun_with_restart %{name}-system.service


%files
%{_bindir}/%{name}
%{_unitdir}/%{name}-system.service
%{_userunitdir}/%{name}-user.service


%changelog
* Fri Apr 17 2026 Phantom X <megaphantomx at hotmail dot com> - 0.1.2-1
- Initial spec

