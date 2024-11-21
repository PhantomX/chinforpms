BuildArch:      noarch

Name:           ntsync
Version:        6.12
Release:        1%{?dist}
Summary:        NT synchronization primitive driver helper files

License:        GPL-2.0-only
URL:            https://repo.or.cz/linux/zf.git/shortlog/refs/heads/ntsync5

Source0:        %{name}.udev
Source1:        %{name}.modules

Provides:       %{name}-kmod-common = %{version}
Requires:       kmod(ntsync.ko)

BuildRequires:  systemd


%description
%{summary}.


%package devel
Summary:        %{summary}

%description devel
The %{name}-devel package contains the winesync header file.


%prep
%autosetup -cT -n %{name}-%{commit}


%build
# Nothing to do here...

%install

# systemd module autoinsert rule
install -m644 -D %{SOURCE1} %{buildroot}%{_prefix}/lib/modules-load.d/%{name}.conf

# udev rule
install -m644 -D %{SOURCE0} %{buildroot}/%{_udevrulesdir}/69-%{name}.rules


%files
%{_prefix}/lib/modules-load.d/%{name}.conf
%{_udevrulesdir}/69-%{name}.rules


%changelog
* Wed Nov 20 2024 Phantom X <megaphantomx at hotmail dot com> - 6.12-1
- 6.12
- Only helper files, needs full patched kernel module

* Mon May 13 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9~rc3-1.20240415git1e5c8fe
- 6.9-rc3

* Wed Feb 21 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8~rc3-1.20240214git67ecf76
- Initial spec

