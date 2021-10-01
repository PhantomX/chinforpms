Name:           chinforpms-rpm-config
Version:        7
Release:        1%{?dist}
Summary:        chinforpms specific rpm configuration files

License:        Public Domain
URL:            https://github.com/PhantomX/chinforpms

Source0:        macros.chinforpms
Source1:        rpmrc

BuildArch:      noarch

BuildRequires:  redhat-rpm-config
Requires:       redhat-rpm-config
Requires:       sed


%description
%{summary}.

The settings take precedence over redhat-rpm-config and rpm default ones.


%prep
%autosetup -c -T


%build


%install
mkdir -p %{buildroot}%{_sysconfdir}/rpm
install -pm0644 %{S:0} %{buildroot}%{_sysconfdir}/rpm/
install -pm0644 %{S:1} %{buildroot}%{_sysconfdir}/


%files
%{_sysconfdir}/rpmrc
%{_sysconfdir}/rpm/macros.chinforpms


%changelog
* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 7-1
- _gcc_lto_cflags future proof fix

* Sun Apr 18 2021 Phantom X <megaphantomx at hotmail dot com> - 6-1
- __cflags_arch_x86_64 fix (>=f34)

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 5-1
- Out of source cmake is default now (>=f33)
- Fixed cpus jobs in _gcc_lto_cflags

* Fri Jul 17 2020 Phantom X <megaphantomx at hotmail dot com> - 4-1
- Enable out of source cmake

* Mon Mar 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 3-1
- Remove -fno-diagnostics-color

* Wed Dec 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 2-1
- Clean log files with -fno-diagnostics-color optflag

* Tue Dec 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1-1
- Initial spec
