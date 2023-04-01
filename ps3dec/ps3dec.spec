%global commit 7d1d27f028aa86cd961a89795d0d19a9b3771446
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20181216

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname PS3Dec

Name:           ps3dec
Version:        5
Release:        1%{?dist}
Summary:        ISO encryptor/decryptor for PS3 disc images

License:        WTFPL
URL:            https://github.com/al3xtjames/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
Source1:        http://www.wtfpl.net/txt/copying#/%{name}-LICENSE


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  mbedtls-devel


%description
An alternative ISO encryptor/decryptor for PS3 disc images .

%prep
%autosetup -n %{pkgname}-%{commit} -p1

rm -f external/*.h

cp -p %{S:1} LICENSE


%build
%cmake

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{_vpath_builddir}/Release/%{pkgname} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{pkgname}


%changelog
* Mon May 30 2022 Phantom X <megaphantomx at hotmail dot com> - 5-1.20181216git7d1d27f
- Initial spec
