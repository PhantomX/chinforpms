%global commit f66209005191bebbe0b7a570b2bbdfb5a5912535
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200126
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname EccEdc

Name:           eccedc
Version:        20200126
Release:        1%{?gver}%{?dist}
Summary:        Checks or fix user data of the 2048 byte per sector of CD by using ecc/edc

License:        GPLv3

URL:            https://github.com/saramibreak/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-rpm-build-fixes.patch


BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{pkgname} checks or fixes the user data of the 2048 byte per sector by
using ecc/edc. This also creates 2352 sector with sync, addr, ecc,
edc (user data is all zero).


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

find %{pkgname} -type f \( -name '*.c*' -o -name '*.h*' \) -exec sed -e 's/\r//' -i {} ';'

sed -e 's|-O2||g' -i %{pkgname}/makefile


%build
%set_build_flags
%make_build -C %{pkgname}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{pkgname}/%{pkgname}_linux.out %{buildroot}%{_bindir}/%{pkgname}


%files
%license LICENSE
%doc README.md
%{_bindir}/%{pkgname}


%changelog
* Tue Aug 11 2020 Phantom X <megaphantomx at hotmail dot com> - 20200126-1
- Initial spec
