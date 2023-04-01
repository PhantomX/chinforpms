%global commit b91acc4b369eff0972202acb17f45f5e2728e490
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200726
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           zram-init
Version:        11.1
Release:        1%{?dist}
Summary:        A wrapper script for the zram kernel module

License:        GPL-2.0-only
URL:            https://github.com/vaeth/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
Source2:        %{name}.sysconfig

Patch100:       0001-systemd-environment-file-support.patch

BuildArch: noarch

%{?systemd_requires}
BuildRequires:  make
BuildRequires:  gettext
BuildRequires:  systemd
Requires:       btrfs-progs
Requires:       e2fsprogs
Requires:       gettext
Requires:       util-linux
Requires:       xfsprogs

%description
%{name} is a wrapper script for the zram kernel module with interactive
and init support.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

cp %{S:1} COPYING

sed \
  -e 's|/bin/|%{_bindir}/|g' \
  -e 's|/sbin/|%{_sbindir}/|g' \
  -i systemd/system/zram_*.service

sed \
  -e 's|/usr/local|%{_prefix}|g' \
  -e 's|$(PREFIX)/etc|%{_sysconfdir}|g' \
  -e 's|$(PREFIX)/sbin|%{_sbindir}|g' \
  -e 's|$(PREFIX)/share/man|%{_mandir}|g' \
  -e 's|$(PREFIX)/share|%{_datadir}|g' \
  -e 's|$(SYSCONFDIR)/modprobe.d|%{_modprobedir}|g' \
  -e 's|$(PREFIX)/lib/systemd/system|%{_unitdir}|g' \
  -i Makefile


%build
%make_build OPENRC=FALSE

%install
%make_install OPENRC=FALSE

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -pm0644 %{S:2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%find_lang %{name} --with-man


%postun
%systemd_postun zram_btrfs.service
%systemd_postun zram_tmp.service
%systemd_postun zram_swap.service
%systemd_postun zram_var_tmp.service


%files -f %{name}.lang
%license COPYING
%doc ChangeLog README.md
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man8/*.8*
%{_modprobedir}/zram.conf
%{_unitdir}/zram_btrfs.service
%{_unitdir}/zram_swap.service
%{_unitdir}/zram_tmp.service
%{_unitdir}/zram_var_tmp.service


%changelog
* Fri Feb 25 2022 Phantom X <megaphantomx at hotmail dot com> - 11.1-1
- 11.1

* Sat Aug 15 2020 Phantom X <megaphantomx at hotmail dot com> - 10.5-1
- 10.5
- Makefile and gettext

* Tue Nov 26 2019 Phantom X - 9.0-1.20180831git93fd4d0
- Initial spec.
