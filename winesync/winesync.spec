%global debug_package %{nil}

%global commit ee18b220dde45003cd7ce7360fe3e633678b97df
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211202

%global gver .%{date}git%{shortcommit}

%global vc_url https://repo.or.cz/linux/zf.git/blob_plain

Name:           winesync
Version:        5.15.5
Release:        1%{?gver}%{?dist}
Summary:        Wine synchronization primitive driver

License:        GPLv2
URL:            https://repo.or.cz/linux/zf.git/shortlog/refs/heads/winesync3

Source0:        %{vc_url}/%{commit}:/Documentation/userspace-api/winesync.rst#/winesync.rst_%{shortcommit}
Source1:        %{vc_url}/%{commit}:/COPYING
Source2:        %{name}.udev
Source3:        %{name}.modules
Source4:        %{vc_url}/%{commit}:/include/uapi/linux/winesync.h#/winesync.h_%{shortcommit}

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

cp -p %{SOURCE0} winesync.rst
cp -p %{SOURCE1} .

%build
# Nothing to do here...

%install

# header file
install -m644 -D %{SOURCE4} %{buildroot}%{_includedir}/linux/winesync.h

# systemd module autoinsert rule
install -m644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/modules-load.d/%{name}.conf

# udev rule
install -m644 -D %{SOURCE2} %{buildroot}/%{_udevrulesdir}/69-%{name}.rules

%files
%license COPYING
%doc winesync.rst
%{_prefix}/lib/modules-load.d/%{name}.conf
%{_udevrulesdir}/69-%{name}.rules


%files devel
%{_includedir}/linux/winesync.h


%changelog
* Mon Dec 06 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.5-1.20211202gitee18b22
- 5.15.5

* Mon Aug 30 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.10-1.20210610gitf12fad2
- 5.12.10
- Add header file

* Sat May 22 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12-1.20210507git73f1881
- Initial spec
