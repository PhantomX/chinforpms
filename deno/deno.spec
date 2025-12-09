# Binary packaging only, rust is hateful

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global vc_id  02f6e49276bb4c03634af4aec4487a5a0a9dbebf

Name:           deno
Version:        2.5.6
Release:        1%{?dist}
Summary:        A secure JavaScript and TypeScript runtime

License:        MIT
URL:            https://github.com/denoland/%{name}

Source0:        %{url}/releases/download/v%{version}/%{name}-x86_64-unknown-linux-gnu.zip#/%{name}-v%{version}.zip
Source1:        %{url}/raw/%{vc_id}/LICENSE.md
Source2:        %{url}/raw/%{vc_id}/README.md

ExclusiveArch:  x86_64

BuildRequires:  unzip

%description
Deno is a JavaScript, TypeScript, and WebAssembly runtime with secure defaults
and a great developer experience. It's built on V8, Rust, and Tokio.


%prep
%autosetup -c -T -a0

cp -p %{S:1} %{S:2} .


%build
./%{name} completions bash > %{name}.bash
./%{name} completions fish > %{name}.fish
./%{name} completions zsh > %{name}.zsh


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{bash_completions_dir}
install -pm0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}

mkdir -p %{buildroot}%{fish_completions_dir}
install -pm0644 %{name}.fish %{buildroot}%{fish_completions_dir}/%{name}.fish

mkdir -p %{buildroot}%{zsh_completions_dir}
install -pm0644 %{name}.zsh %{buildroot}%{zsh_completions_dir}/_%{name}


%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}


%changelog
* Wed Nov 12 2025 Phantom X <megaphantomx at hotmail dot com> - 2.5.6-1
- 2.5.6

* Wed Oct 22 2025 Phantom X <megaphantomx at hotmail dot com> - 2.5.4-1
- Initial spec

