%global commit d4f447fb81c6e4b90b754bd06684acc3f77ac385
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210921

BuildArch:      noarch

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname u4pak

Name:           python-%{pkgname}
Version:        0
Release:        2%{?dist}
Summary:        Unreal Engine 4 .pak archive tool

License:        BSD-1-Clause
URL:            https://github.com/panzi/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
# Extracted from %%{name}.py
Source1:        LICENSE

BuildRequires:  python3-devel


%description
%{pkgname} unpacks, packs, lists, tests and mounts Unreal Engine 4 .pak archives.


%prep
%autosetup -n %{pkgname}-%{commit}

cp -p %{S:1} .

%py3_shebang_fix %{pkgname}.py


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{pkgname}.py %{buildroot}%{_bindir}/p%{pkgname}

%files
%license LICENSE
%doc README.md
%{_bindir}/p%{pkgname}


%changelog
* Wed Feb 23 2022 Phantom X <megaphantomx at hotmail dot com> - 0-2.20210921gitd4f447f
- Rename to python-u4pak (pu4pak)

* Sat Feb 19 2022 Phantom X <megaphantomx at hotmail dot com> - 0-1.20210921gitd4f447f
- Initial spec
