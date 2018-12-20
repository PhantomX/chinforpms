Name:           gamemode
Version:        1.2
Release:        100%{?dist}
Summary:        Daemon/lib that optimizes system performance on demand
Epoch:          1

License:        BSD
URL:            https://github.com/FeralInteractive/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}

# Use system inih
Patch0:         %{name}-system-inih.patch


BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  inih-devel
BuildRequires:  pkgconfig(libsystemd)
Requires:       PolicyKit-authentication-agent
Requires:       systemd

%description
GameMode is a daemon/lib combo for Linux that allows games to request
a set of optimizations be temporarily applied to the host OS.

%package devel
Summary:        GameMode development files
Requires:       gamemode%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files libraries needed for
application integration with %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build


%install
%meson_install

install -pm0755 %{S:1} %{buildroot}/%{_bindir}/%{name}


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}*
%{_libdir}/lib*.so.*
%{_libexecdir}/cpugovctl
%{_userunitdir}/*.service
%{_mandir}/man8/*.8.*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/polkit-1/actions/*.policy

%files devel
%license LICENSE.txt
%{_includedir}/%{name}*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so


%changelog
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
