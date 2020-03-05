Name:           gamemode
Version:        1.5.1
Release:        100%{?dist}
Summary:        Daemon/lib that optimizes system performance on demand
Epoch:          1

License:        BSD
URL:            https://github.com/FeralInteractive/%{name}
Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.xz


BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  inih-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
Requires:       polkit
Requires:       PolicyKit-authentication-agent
Requires:       systemd

%description
GameMode is a daemon/lib combo for Linux that allows games to request
a set of optimizations be temporarily applied to the host OS.

%package devel
Summary:        GameMode development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files libraries needed for
application integration with %{name}.

%prep
%autosetup -p1

rm -rf subprojects/inih/*


%build
%meson --libexecdir=%{_libexecdir}/%{name}
%meson_build


%install
%meson_install

mkdir -p %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE.txt
%doc README.md example/%{name}.ini
%{_bindir}/%{name}*
%{_libdir}/lib*.so.*
%{_libexecdir}/%{name}
%{_userunitdir}/*.service
%{_mandir}/man8/*.8.*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/polkit-1/actions/*.policy
%dir %{_datadir}/%{name}

%files devel
%license LICENSE.txt
%{_includedir}/%{name}*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so


%changelog
* Thu Mar 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5.1-100
- 1.5.1

* Thu Jan 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.5-100
- 1.5

* Mon Jul 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.4-100
- 1.4

* Fri Mar 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.3.1-100
- 1.3.1
- tar.xz source

* Fri Mar 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3-100
- 1.3
- Drop wrapper and patch provided for multilib
- Add example ini file to docs
- Set libexecdir, have two binaries inside

* Sat Jul 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.2-100.chinfo
- 1.2
- Remove upstreamed patches

* Fri Jul 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-100
- Sync patches with Rawhide. dbus file, manpage changes and better library versioning
- Epoch

* Sat May 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-1
- 1.1

* Wed Apr 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1
- Initial spec
