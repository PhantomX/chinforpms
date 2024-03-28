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
Version:        1.5.1
Release:        1%{?dist}
Summary:        Render markdown on the CLI

License:        MIT
URL:            https://charm.sh/

Source0:        %{vc_url}/releases/download/v%{version}/%{name}_Linux_%{parch}.tar.gz

%description
Glow is a terminal based markdown reader designed from the ground up to bring
out the beauty and power of the CLI.


%prep
%autosetup -c -n %{name}-%{version}

RVER="$(strings %{name} | grep '^mod' |awk '{print $3}' |grep -v '^$' | head -n 1 | tr -d 'v' )"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch. You have ${RVER} in %{S:0} instead %{version} "
  echo "Edit Version and try again"
  exit 1
fi

gunzip manpages/*.1.gz


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 manpages/%{name}.1  %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{bash_completions_dir}/%{name}
install -pm0644 completions/%{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
mkdir -p %{buildroot}%{zsh_completions_dir}/_%{name}
install -pm0644 completions/%{name}.zsh %{buildroot}%{zsh_completions_dir}/_%{name}
mkdir -p %{buildroot}%{fish_completions_dir}/%{name}.fish
install -pm0644 completions/%{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/*.1.*
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish


%changelog
* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1.5.1-1
- 1.5.1

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.5.0-1
- 1.5.0

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.4.1-1
- 1.4.1

* Fri Feb 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.3.0-1
- 1.3.0

* Wed Nov 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-1
- Initial spec
