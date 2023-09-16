%global commit abbef80868dfe5b58c1849f3a2cf6d238067a0f9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230309
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname EccEdc

Name:           eccedc
Version:        20230606
Release:        1%{?dist}
Summary:        Checks or fix user data of the 2048 byte per sector of CD by using ecc/edc

License:        GPLv3

URL:            https://github.com/saramibreak/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-rpm-build-fixes.patch
Patch1:         0001-gcc-13-build-fix.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{pkgname} checks or fixes the user data of the 2048 byte per sector by
using ecc/edc. This also creates 2352 sector with sync, addr, ecc,
edc (user data is all zero).


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

find %{pkgname} -type f \( -name '*.c*' -o -name '*.h*' \) -exec sed -e 's/\r//' -i {} ';'

sed -e 's|-O2||g' -i %{pkgname}/makefile


%build
%set_build_flags
%make_build -C %{pkgname}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{pkgname}/%{pkgname}.out %{buildroot}%{_bindir}/%{pkgname}


%files
%license LICENSE
%doc README.md
%{_bindir}/%{pkgname}


%changelog
* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 20230606-1
- 20230606

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 20230309-1.20230309gitabbef80
- 20230309

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 20200126-2.20220225git56226ce
- Snapshot

* Tue Aug 11 2020 Phantom X <megaphantomx at hotmail dot com> - 20200126-1
- Initial spec
