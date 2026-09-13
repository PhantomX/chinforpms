%bcond check 0

%global commit 31f1b542f88e7b4be9a01e749920d857535fc715
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20260910

%global dist .%{date}git%{shortcommit}%{?dist}

%global soname_ver 0

Name:           tlottie
Version:        0.1.0
Release:        1%{?dist}
Summary:        Rust library for drawing Lottie animations

URL:            https://github.com/dkaraush/%{name}
License:        MIT

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  cmake
BuildRequires:  rust-packaging
BuildRequires:  gcc
BuildRequires:  g++

%description
%{name} is Rust library for drawing Lottie animations.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{commit} -p1

cat > build.rs <<'EOF'
pub fn main() {
    println!("cargo:rustc-cdylib-link-arg=-Wl,-soname,lib%{name}.so.%{soname_ver}");
}
EOF

%cargo_prep
%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build -f c-api
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies


%install
mkdir -p %{buildroot}/%{_libdir}
install -m 0755 target/rpm/lib%{name}.so \
  %{buildroot}%{_libdir}/lib%{name}.so.%{version}
ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{soname_ver}
ln -s lib%{name}.so.%{soname_ver} %{buildroot}%{_libdir}/lib%{name}.so

mkdir -p %{buildroot}%{_includedir}
install -pm0644 include/tlottie.h %{buildroot}%{_includedir}


%if %{with check}
%check
%cargo_test
%endif


%files
%doc README.md
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so


%changelog
* Tue Sep 08 2026 Phantom X <megaphantomx at hotmail dot com> - 0.1.0-1.20260906git758c7cb
- Initial spec
