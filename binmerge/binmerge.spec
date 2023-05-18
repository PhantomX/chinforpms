%global commit 6e26cc41f1839cb24c1068fe673b1510a2cef258
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220311
%bcond_without snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           binmerge
Version:        1.0
Release:        3%{?dist}
Summary:        Tool to merge multiple bin/cue tracks into one

License:        GPL-2.0-only
URL:            https://github.com/putnam/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  /usr/bin/pathfix.py


%description
%{name} is a tool to merge multiple bin/cue tracks into one.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{name}

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0-2.20210703git7218522
- Bump

* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1.20200523git46834fe
- Initial spec
