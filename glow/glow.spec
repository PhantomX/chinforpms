# Binary packaging only, go is hateful

%undefine _debugsource_packages
%global _build_id_links none

%ifarch x86_64
%global parch x86_64
%else
%global parch 386
%endif

%global vc_url  https://github.com/charmbracelet/%{name}

Name:           glow
Version:        1.4.1
Release:        1%{?dist}
Summary:        Render markdown on the CLI

License:        MIT
URL:            https://charm.sh/

Source0:        %{vc_url}/releases/download/v%{version}/%{name}_%{version}_linux_%{parch}.tar.gz

%description
Glow is a terminal based markdown reader designed from the ground up to bring
out the beauty and power of the CLI.


%prep
%autosetup -c -n %{name}-%{version}

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.4.1-1
- 1.4.1

* Fri Feb 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.3.0-1
- 1.3.0

* Wed Nov 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-1
- Initial spec
