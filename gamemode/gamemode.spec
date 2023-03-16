%global commit 5163c01d24684a1ab535f2b4c9f8df02718a15ab
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200901
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           gamemode
Version:        1.7
Release:        101%{?gver}%{?dist}
Summary:        Daemon/lib that optimizes system performance on demand
Epoch:          1

License:        BSD-3-Clause
URL:            https://github.com/FeralInteractive/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.xz
%endif

Patch0:         %{url}/commit/4934191b1928ef695c3e8af21e75781f8591745f.patch#/%{name}-gh-4934191.patch

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
Requires:       polkit
Requires:       PolicyKit-authentication-agent
Requires:       systemd
Recommends:     (gamemode(x86-32) if glibc(x86-32))

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
%autosetup %{?gver:-n %{name}-%{commit}} -p1

rm -rf subprojects/inih-*

sed -e '/^GAMEMODEAUTO_NAME/s|lib|/usr/\\$LIB/lib|' -i data/%{name}run


%build
%meson --libexecdir=%{_libexecdir}/%{name}
%meson_build


%install
%meson_install

rm -f %{buildroot}%{_libdir}/*.a

%pre
%sysusers_create_compat %{buildroot}%{_sysusersdir}/%{name}.conf


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}*
%{_libdir}/lib*.so.*
%{_libexecdir}/%{name}
%{_userunitdir}/*.service
%{_mandir}/man1/*.1.*
%{_mandir}/man8/*.8.*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/%{name}/
%{_metainfodir}/*.metainfo.xml
%{_sysusersdir}/%{name}.conf

%files devel
%license LICENSE.txt
%{_includedir}/%{name}*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so


%changelog
* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.7-101
- glibc 2.36 fix

* Thu Jul 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.7-100
- 1.7

* Fri Feb 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:1.6.1-100
- 1.6.1

* Fri Sep 11 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.6-100
- 1.6

* Fri Sep 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.5.1-102.20200901git5163c01
- Bump

* Fri Aug 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.5.1-101.20200717git510a0a6
- Snapshot

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
