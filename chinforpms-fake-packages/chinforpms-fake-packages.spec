%global fakeepoch 10
%global fakever   1000

Name:           chinforpms-fake-packages
Version:        6
Release:        1%{?dist}
Summary:        A package to obsolete and provides packages

License:        LicenseRef-Fedora-Public-Domain
URL:            https://github.com/PhantomX/chinforpms
Source0:        README

BuildArch:      noarch

Provides:       bash-completion = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      bash-completion < %{fakeepoch}:%{fakever}-%{release}
Provides:       bash-completion-devel = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      bash-completion-devel < %{fakeepoch}:%{fakever}-%{release}

Provides:       games-menus = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      games-menus < %{fakeepoch}:%{fakever}-%{release}

Provides:       GConf2 = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      GConf2 < %{fakeepoch}:%{fakever}-%{release}

Provides:       PackageKit-session-service = %{fakeepoch}:%{fakever}-%{release}
Obsoletes:      PackageKit-session-service < %{fakeepoch}:%{fakever}-%{release}

%description
This package exists to obsolete and provides other packages that chinforpms don't
like, but are dependencies to good ones.

Only use this if you don't like flatpak and know what you're doing.


%prep
%autosetup -c -T

cp -p %{S:0} .

cat > bash-completion.pc <<'EOF'
prefix=/usr
compatdir=/etc/bash_completion.d
completionsdir=${prefix}/share/bash-completion/completions
helpersdir=${prefix}/share/bash-completion/helpers

Name: bash-completion
Description: programmable completion for the bash shell
URL: https://github.com/scop/bash-completion
Version: %{fakever}
EOF

cat > gconftool-2 <<'EOF'
#!/bin/sh
# %{name} fake executable
true
EOF

%build

%install

mkdir -p %{buildroot}%{_datadir}/pkgconfig
install -pm0644 \
  bash-completion.pc \
  %{buildroot}%{_datadir}/pkgconfig/

mkdir -p %{buildroot}%{_bindir}
install -pm0755 gconftool-2 \
  %{buildroot}%{_bindir}/


%files
%doc README
%{_bindir}/*
%{_datadir}/pkgconfig/*.pc


%changelog
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 6-1
- Add bash-completion-devel

* Wed Nov 24 2021 Phantom X <megaphantomx at bol dot com dot br> - 5-1
- xdg-desktop-*

* Wed Oct 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 4-1
- GConf2 and fake gconftool-2

* Tue Oct 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 3-1
- PackageKit-session-service

* Wed Jul 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 2-1
- Add bash-completion pkgconfig file, for some spec BRs

* Sat Apr 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 1-1
- Initial spec
