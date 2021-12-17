%global commit 7218522aac721f6b0dcc2efc1b38f7d286979c7a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210703
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           binmerge
Version:        1.0
Release:        2%{?gver}%{?dist}
Summary:        Tool to merge multiple bin/cue tracks into one

License:        GPLv2
URL:            https://github.com/putnam/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  /usr/bin/pathfix.py


%description
%{name} is a tool to merge multiple bin/cue tracks into one.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

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
