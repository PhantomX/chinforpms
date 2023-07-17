%global commit 0bc27f4740e382f2a2896dc1dabfec1d0ac96818
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20170507

BuildArch:      noarch

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname ZenStates-Linux
%global systemd_commit 82765d490290a99ba18282e187e9de3d7c11dd49

Name:           zenstates
Version:        6
Release:        1%{?dist}
Summary:        Dynamically edit AMD Ryzen processor P-States

License:        MIT
URL:            https://github.com/r4m0n/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
Source1:        https://github.com/jfredrickson/disable-c6/raw/82765d490290a99ba18282e187e9de3d7c11dd49/disable-c6.service.template
Source2:        https://aur.archlinux.org/cgit/aur.git/plain/enable-c6.service?h=disable-c6-systemd-with-modern-standby#/enable-c6.service

BuildRequires:  python3-devel
BuildRequires:  /usr/bin/pathfix.py
BuildRequires:  /usr/bin/pathfix.py
BuildRequires:  systemd
%dnl Requires:       %{py3_dist portio}

Provides:       ZenStates = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{summary}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

cp -a %{S:1} disable-c6.service
cp -a %{S:2} .

sed \
  -e 's|{{PREFIX}}/bin|%{_bindir}|g' \
  -e 's|\.py||g' \
  -i disable-c6.service

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" \
  togglecode.py %{name}.py


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.py %{buildroot}%{_bindir}/zenstates
%dnl install -pm0755 togglecode.py %{buildroot}%{_bindir}/zentates-togglecode

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 disable-c6.service %{buildroot}%{_unitdir}/
install -pm0644 enable-c6.service %{buildroot}%{_unitdir}/


%post
%systemd_post disable-c6.service

%preun
%systemd_preun disable-c6.service

%postun
%systemd_postun_with_restart disable-c6.service


%files
%license LICENSE
%doc README.md
%{_bindir}/zenstates
%dnl %{_bindir}/zentates-togglecode
%{_unitdir}/disable-c6.service
%{_unitdir}/enable-c6.service


%changelog
* Sun Jul 16 2023 Phantom X <megaphantomx at hotmail dot com> - 6-1.20170507git0bc27f4
- Initial spec

