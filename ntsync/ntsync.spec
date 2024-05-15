%global debug_package %{nil}

%global commit 1e5c8fe80527908d2849b8ac7beb63b855cd4d54
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240415

%global dist .%{date}git%{shortcommit}%{?dist}

%global vc_url https://repo.or.cz/linux/zf.git/blob_plain

Name:           ntsync
Version:        6.9~rc3
Release:        1%{?dist}
Summary:        NT synchronization primitive driver

License:        GPL-2.0-only
URL:            https://repo.or.cz/linux/zf.git/shortlog/refs/heads/ntsync5

Source0:        %{vc_url}/%{commit}:/Documentation/userspace-api/ntsync.rst#/ntsync.rst_%{shortcommit}
Source1:        %{vc_url}/%{commit}:/COPYING
Source2:        %{name}.udev
Source3:        %{name}.modules
Source4:        %{vc_url}/%{commit}:/include/uapi/linux/ntsync.h#/ntsync.h_%{shortcommit}

Provides:       %{name}-kmod-common = %{version}
Requires:       %{name}-kmod >= %{version}

BuildRequires:  systemd


%description
%{summary}.


%package devel
Summary:        %{summary}

%description devel
The %{name}-devel package contains the winesync header file.


%prep
%autosetup -cT -n %{name}-%{commit}

cp -p %{SOURCE0} ntsync.rst
cp -p %{SOURCE1} .

%build
# Nothing to do here...

%install

# header file
install -m644 -D %{SOURCE4} %{buildroot}%{_includedir}/linux/ntsync.h

%ifnarch %{ix86}
# systemd module autoinsert rule
install -m644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/modules-load.d/%{name}.conf

# udev rule
install -m644 -D %{SOURCE2} %{buildroot}/%{_udevrulesdir}/69-%{name}.rules
%endif


%ifnarch %{ix86}
%files
%license COPYING
%doc ntsync.rst
%{_prefix}/lib/modules-load.d/%{name}.conf
%{_udevrulesdir}/69-%{name}.rules
%endif

%files devel
%license COPYING
%{_includedir}/linux/ntsync.h


%changelog
* Mon May 13 2024 Phantom X <megaphantomx at hotmail dot com> - 6.9~rc3-1.20240415git1e5c8fe
- 6.9-rc3

* Wed Feb 21 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8~rc3-1.20240214git67ecf76
- Initial spec

