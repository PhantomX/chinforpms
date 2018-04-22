%global fakeepoch 10
%global fakever   1000

Name:           chinforpms-fake-packages
Version:        1
Release:        1%{?dist}
Summary:        A package to obsolete and provides packages

License:        Public Domain
URL:            http://github.com/PhantomX/chinforpms
Source0:        README

BuildArch:      noarch

Provides:       bash-completion = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      bash-completion < %{fakeepoch}:%{fakever}-%{release}

Provides:       games-menus = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      games-menus < %{fakeepoch}:%{fakever}-%{release}

%description
This package exists to obsolete and provides other packages that chinforpms don't
like, but are dependencies to good ones.


%prep
%autosetup -c -T

cp -p %{S:0} .

%build

%install

%files
%doc README

%changelog
* Sat Apr 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 1-1
- Initial spec
