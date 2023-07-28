%global commit 899c0567b9b4cb86bd653db76ca72652feb45d87
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180509

BuildArch:      noarch

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           move-to-next-monitor
Version:        0
Release:        2%{?dist}
Summary:        Script to move windows from one monitor to the next

License:        GPL-3.0-only
URL:            https://github.com/vanaoff/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  python3-devel
Requires:       xdotool
Requires:       xprop
Requires:       xrandr
Requires:       wmctrl
Requires:       xwininfo


%description
%{name} is a script to move windows from one monitor to the next.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

%py3_shebang_fix %{name}


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Wed Apr 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0-2.20180509git899c056
- R: xwininfo

* Mon Mar 14 2022 Phantom X <megaphantomx at hotmail dot com> - 0-1.20180509git899c056
- Initial spec
