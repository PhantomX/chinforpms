BuildArch:      noarch

Name:           xfce-session-target
Version:        1.3.2
Release:        1%{?dist}
Summary:        systemd Integration for xfce-session

License:        GPL-3.0-only
URL:            https://git.linux-help.org/infusix/%{name}

Source0:        %{url}/archive/1.3.2.tar.gz#/%{name}-%{version}.tar.gz
Source1:        Makefile

BuildRequires:  systemd
Requires:       xfce4-session

%description
%{summary}.


%prep
%autosetup -p1

sed -e 's|/bin/systemctl|%{_bindir}/systemctl|g' -i src/%{name}.sh

sed \
  -e '/^Exec=/s|=.*$|=%{_libdir}/xfce4/session/%{name}.sh login|' \
  -e '/^OnlyShowIn=/s|=.*$|=XFCE;|' \
  -i src/%{name}.desktop

sed \
  -e '/^Encoding/d' \
  -e '/^Version/d' \
  -e '/^Exec=/s|=.*$|=%{_libdir}/xfce4/session/%{name}.sh logout|' \
  -i src/Logout.desktop


%build


%install
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
install -pm0644 src/%{name}.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-login.desktop
install -pm0644 src/Logout.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-logout.desktop

mkdir -p %{buildroot}%{_libdir}/xfce4/session
install -pm0755 src/%{name}.sh %{buildroot}%{_libdir}/xfce4/session

mkdir -p %{buildroot}%{_userunitdir}
install -pm0644 src/xfce-session.target %{buildroot}%{_userunitdir}




%files
%license LICENSE
%doc README examples
%{_sysconfdir}/xdg/autostart/*.desktop
%{_libdir}/xfce4/session/%{name}.sh
%{_userunitdir}/xfce-session.target


%changelog
* Sun Apr 19 2026 Phantom X <megaphantomx at hotmail dot com> - 1.3.2-1
- Initial spec

