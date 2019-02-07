Name:           firejail
Version:        0.9.58
Release:        1%{?dist}
Summary:        GUI tools for firejail

License:        GPLv2
URL:            https://firejail.wordpress.com/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
Source1:        README.suid

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-devel


%description
Firejail is a SUID program that reduces the risk of security breaches by
restricting the running environment of untrusted applications using
Linux namespaces and seccomp-bpf.

%prep
%autosetup

cp %{SOURCE1} .

rm -f contrib/*.sh
chmod -x contrib/*.py
sed -e '1s|^#!.*$|#!%{__python3}|' -i contrib/*.py

sed \
  -e '/$(DOCDIR)/d' \
  -i Makefile.in

%build
%configure \
  --disable-apparmor \
 --disable-contrib-install \
%{nil}

%make_build DESTDIR=


%install
%make_install

chmod +x %{buildroot}%{_libdir}/%{name}/*.so

rm -rf %{buildroot}/usr/share/doc


%pre
getent group %{name} >/dev/null || groupadd -r %{name}

%files
%license COPYING
%doc README* RELNOTES contrib
%config(noreplace) %{_sysconfdir}/%{name}
%attr(4750,root,%{name}) %{_bindir}/%{name}
%{_bindir}/firecfg
%{_bindir}/firemon
%{_libdir}/%{name}/
%{_datadir}/bash-completion/completions/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*


%changelog
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
