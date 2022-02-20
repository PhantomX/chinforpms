%global commit d4f447fb81c6e4b90b754bd06684acc3f77ac385
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210921

%global gver .%{date}git%{shortcommit}

Name:           u4pak
Version:        0
Release:        1%{?gver}%{?dist}
Summary:        Unreal Engine 4 .pak archive tool

License:        BSD
URL:            https://github.com/panzi/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Extracted from %%{name}.py
Source1:        LICENSE

BuildArch:      noarch

BuildRequires:  python3-devel


%description
%{name} unpacks, packs, lists, tests and mounts Unreal Engine 4 .pak archives.


%prep
%autosetup -n %{name}-%{commit}

cp -p %{S:1} .

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{name}.py


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.py %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Sat Feb 19 2022 Phantom X <megaphantomx at hotmail dot com> - 0-1.20210921gitd4f447f
- Initial spec
