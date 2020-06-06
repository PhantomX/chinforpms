%global commit 46834fe327099e0fd51fa7a2e6683b964166a3d0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200523
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           binmerge
Version:        1.0
Release:        1%{?gver}%{?dist}
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
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

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
* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1.20200523git46834fe
- Initial spec
