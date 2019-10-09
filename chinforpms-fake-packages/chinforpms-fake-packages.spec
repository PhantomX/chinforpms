%global fakeepoch 10
%global fakever   1000

Name:           chinforpms-fake-packages
Version:        3
Release:        1%{?dist}
Summary:        A package to obsolete and provides packages

License:        Public Domain
URL:            https://github.com/PhantomX/chinforpms
Source0:        README

BuildArch:      noarch

Provides:       bash-completion = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      bash-completion < %{fakeepoch}:%{fakever}-%{release}

Provides:       games-menus = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      games-menus < %{fakeepoch}:%{fakever}-%{release}

Provides:       PackageKit-session-service = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      PackageKit-session-service < %{fakeepoch}:%{fakever}-%{release}


%description
This package exists to obsolete and provides other packages that chinforpms don't
like, but are dependencies to good ones.


%prep
%autosetup -c -T

cp -p %{S:0} .

%build

%install

mkdir -p %{buildroot}%{_datadir}/pkgconfig
cat > %{buildroot}%{_datadir}/pkgconfig/bash-completion.pc <<'EOF'
prefix=/usr
compatdir=/etc/bash_completion.d
completionsdir=${prefix}/share/bash-completion/completions
helpersdir=${prefix}/share/bash-completion/helpers

Name: bash-completion
Description: programmable completion for the bash shell
URL: https://github.com/scop/bash-completion
Version: %{fakever}
EOF

%files
%doc README
%{_datadir}/pkgconfig/*.pc


%changelog
* Tue Oct 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 3-1
- PackageKit-session-service

* Wed Jul 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 2-1
- Add bash-completion pkgconfig file, for some spec BRs

* Sat Apr 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 1-1
- Initial spec
