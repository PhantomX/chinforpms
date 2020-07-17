Name:           chinforpms-rpm-config
Version:        4
Release:        1%{?dist}
Summary:        chinforpms specific rpm configuration files

License:        Public Domain
URL:            https://github.com/PhantomX/chinforpms

Source0:        macros.chinforpms
Source1:        rpmrc

BuildArch:      noarch

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
* Fri Jul 17 2020 Phantom X <megaphantomx at hotmail dot com> - 4-1
- Enable out of source cmake

* Mon Mar 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 3-1
- Remove -fno-diagnostics-color

* Wed Dec 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 2-1
- Clean log files with -fno-diagnostics-color optflag

* Tue Dec 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1-1
- Initial spec
