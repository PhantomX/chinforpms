BuildArch:      noarch

%global pkgname ProtonShim

Name:           proton-shim
Version:        2.5.1
Release:        1%{?dist}
Summary:        Easily run programs and scripts inside Steam game prefixes

License:        MIT
URL:            https://gitlab.com/Wisher/%{pkgname}

Source0:        %{url}/-/archive/%{version}/%{pkgname}-%{version}.tar.bz2

BuildRequires:  pandoc >= 3
Requires:       coreutils
Requires:       file
Requires:       findutils
Requires:       grep
Requires:       sed
Requires:       sudo
Recommends:     steam


%description
%{name} is a lightweight launcher for running Windows executables and
scripts using Proton, complete with support for AppID-based compatdata,
interactive or scripted mode, and advanced logging options.


%prep
%autosetup -n %{pkgname}-%{version} -p1


%build
pandoc -s -f markdown-smart -t man %{name}.1.md -o %{name}.1

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.sh %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 %{name}.1 %{buildroot}%{_mandir}/man1/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Jul 02 2025 Phantom X <megaphantomx at hotmail dot com> - 2.5.1-1
- Initial spec
