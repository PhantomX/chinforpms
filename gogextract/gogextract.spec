%global commit 6601b32feacecd18bc12f0a4c23a063c3545a095
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20161009

%global gver .%{date}git%{shortcommit}%{?dist}

Name:           gogextract
Version:        0
Release:        1%{?dist}
Summary:        Script for unpacking GOG Linux installers

License:        MIT
URL:            https://github.com/Yepoleb/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch:      noarch

BuildRequires:  /usr/bin/pathfix.py


%description
GOG Extract is a script for unpacking GOG Linux installers.


%prep
%autosetup -n %{name}-%{commit} -p1

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
* Tue Dec 07 2021 Phantom X <megaphantomx at hotmail dot com> - 0-1.20161009git6601b32
- Initial spec
