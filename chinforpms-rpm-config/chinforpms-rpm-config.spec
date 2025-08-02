%global rrc_ver 342-4


Name:           chinforpms-rpm-config
Version:        15
Release:        1%{?dist}
Summary:        chinforpms specific rpm configuration files

License:        LicenseRef-Fedora-Public-Domain
URL:            https://github.com/PhantomX/chinforpms

Source0:        macros.chinforpms
Source1:        rpmrc

BuildArch:      noarch

BuildRequires:  redhat-rpm-config >= %{rrc_ver}
Requires:       redhat-rpm-config >= %{rrc_ver}
Requires:       coreutils


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
* Fri Aug 01 2025 Phantom X <megaphantomx at hotmail dot com> - 15-1
- Add %%rustflags_debuginfo

* Tue Apr 15 2025 Phantom X <megaphantomx at hotmail dot com> - 14-1
- Fix _gcc_lto_cflags, redhat-rpm-config 342-4 required

* Tue Apr 16 2024 Phantom X <megaphantomx at hotmail dot com> - 13-1
- Simplify macros

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 12-1
- Fedora 40 update

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 11-1
- Fedora 40 update

* Thu Sep 14 2023 Phantom X <megaphantomx at hotmail dot com> - 11-1
- Fedora 39 update

* Wed Mar 22 2023 Phantom X <megaphantomx at hotmail dot com> - 10-1
- Remove sed requirement

* Sat Mar 18 2023 Phantom X <megaphantomx at hotmail dot com> - 9-1
- Simplify macros

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 8-1
- Undefine _include_frame_pointers

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
