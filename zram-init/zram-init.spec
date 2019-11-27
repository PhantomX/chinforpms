%global commit 93fd4d01c15733a496e8d990df3ebb2c0f5ab316
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180831
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           zram-init
Version:        9.0
Release:        1%{?gver}%{?dist}
Summary:        A wrapper script for the zram kernel module

License:        GPLv2
URL:            https://github.com/vaeth/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
Source2:        %{name}.sysconfig

Patch100:       0001-systemd-environment-file-support.patch

BuildArch: noarch

%{?systemd_requires}
BuildRequires: systemd
Requires:      btrfs-progs
Requires:      e2fsprogs
Requires:      util-linux

%description
%{name} is a wrapper script for the zram kernel module with interactive
and init support.


%prep
%autosetup -n %{name}-%{commit} -p1

cp %{S:1} COPYING

sed \
  -e 's|/bin/|%{_bindir}/|g' \
  -e 's|/sbin/|%{_sbindir}/|g' \
  -i systemd/system/zram_*.service

%build


%install
mkdir -p %{buildroot}%{_sbindir}
install -pm0755 sbin/%{name} %{buildroot}%{_sbindir}/%{name}

mkdir -p %{buildroot}%{_modprobedir}
install -pm0644 modprobe.d/zram.conf %{buildroot}%{_modprobedir}/zram.conf

mkdir -p %{buildroot}%{_unitdir}
for i in btrfs swap tmp var_tmp ;do
  install -pm0644 systemd/system/zram_$i.service %{buildroot}%{_unitdir}/zram_$i.service
done

mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
install -pm0644 zsh/_%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -pm0644 %{S:2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}


%postun
%systemd_postun zram_btrfs.service
%systemd_postun zram_tmp.service
%systemd_postun zram_swap.service
%systemd_postun zram_var_tmp.service


%files
%license COPYING
%doc ChangeLog README.md
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_modprobedir}/zram.conf
%{_unitdir}/zram_btrfs.service
%{_unitdir}/zram_swap.service
%{_unitdir}/zram_tmp.service
%{_unitdir}/zram_var_tmp.service


%changelog
* Tue Nov 26 2019 Phantom X - 9.0-1.20180831git93fd4d0
- Initial spec.
