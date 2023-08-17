Name:           firejail
Version:        0.9.72
Release:        100%{?dist}
Summary:        Linux namespaces sandbox program

License:        GPL-2.0-or-later
URL:            https://firejail.wordpress.com/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
Source1:        README.suid
Source2:        %{name}-sysusers.conf


BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libselinux-devel
BuildRequires:  python3-devel
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
Requires:       xdg-dbus-proxy
%{?sysusers_requires_compat}
%{?systemd_requires}


%description
Firejail is a SUID program that reduces the risk of security breaches by
restricting the running environment of untrusted applications using
Linux namespaces and seccomp-bpf.

%prep
%autosetup

cp %{SOURCE1} .

rm -f contrib/*.sh
chmod -x contrib/*.py
%py3_shebang_fix contrib/*.py

sed \
  -e '/$(docdir)/d' \
  -i Makefile

%build
%configure \
  --enable-selinux \
  --disable-apparmor \
  --disable-contrib-install \
%{nil}

%make_build DESTDIR=


%install
%make_install

chmod +x %{buildroot}%{_libdir}/%{name}/*.so

rm -rf %{buildroot}/usr/share/doc

install -Dpm 644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf


%pre
%sysusers_create_compat %{SOURCE2}


%files
%license COPYING
%doc README* RELNOTES contrib etc/templates/*
%config(noreplace) %{_sysconfdir}/%{name}
%attr(4750,root,%{name}) %{_bindir}/%{name}
%{_bindir}/firecfg
%{_bindir}/firemon
%{_bindir}/jailcheck
%{_libdir}/%{name}/
%{_datadir}/bash-completion/completions/*
%{_datadir}/zsh/site-functions/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_sysusersdir}/%{name}.conf


%changelog
* Tue Jan 17 2023 Phantom X <megaphantomx at hotmail dot com> - 0.9.72-1
- 0.9.72

* Fri Jun 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.70-1
- 0.9.70

* Sun Feb 06 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.68-1
- 0.9.68

* Wed Jun 30 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.66-1
- 0.9.66

* Mon Feb 08 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.64.4-1
- 0.9.64.4

* Fri Jan 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.64.2-1
- 0.9.64.2

* Mon Dec 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.64-2
- Fedora sync

* Mon Oct 26 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.64-1
- 0.9.64

* Tue Aug 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.62.4-1
- 0.9.62.4

* Tue Aug 11 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.62.2-1
- 0.9.62.2

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.9.62-1
- 0.9.62
- sysusers.d support

* Mon May 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.60-1
- 0.9.60

* Thu Apr 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.58.2-2
- Remove not compatible -fcf-protection with -mindirect-branch from optflags

* Fri Feb 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.58.2-1
- 0.9.58.2

* Mon Jan 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.58-1
- 0.9.58
- Place contrib scripts on docdir

* Tue Sep 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.56-1
- 0.9.56

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.54-1
- 0.9.54

* Wed Dec 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.52-1
- 0.9.52

* Sat Sep 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.50-1
- 0.9.50

* Wed Aug 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.48-1
- Initial spec.
