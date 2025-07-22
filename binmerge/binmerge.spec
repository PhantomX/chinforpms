%global commit aa827005c71f18c8723017e26738d5b1920b26af
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240313
%bcond snapshot 1

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           binmerge
Version:        1.0.3
Release:        1%{?dist}
Summary:        Tool to merge multiple bin/cue tracks into one

License:        GPL-2.0-only
URL:            https://github.com/putnam/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  python3-devel


%description
%{name} is a tool to merge multiple bin/cue tracks into one.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

%py3_shebang_fix %{name}

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Wed May 22 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0.3-1.20240313gitaa82700
- 1.0.3

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0-2.20210703git7218522
- Bump

* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1.20200523git46834fe
- Initial spec
