# Generated by rust2rpm 20
%bcond_with check

%global commit 458eb6d53c21f38dfad8592720fe2acf86965210
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220213
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global crate u4pak

Name:           rust-%{crate}
Version:        1.3.0
Release:        1%{?gver}%{?dist}
Summary:        Unreal Engine 4 .pak archive tool

License:        MPLv2.0
URL:            https://github.com/panzi/rust-%{crate}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Disable-fuse-support.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging

%global _description %{expand:
%{crate} unpacks, packs, lists and tests Unreal Engine 4 .pak archives.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
License:        MPLv2.0

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE.txt
%doc README.md
%{_bindir}/%{crate}

%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

# Unneeded
rm -rf %{buildroot}%{cargo_registry}


%if %{with check}
%check
%cargo_test
%endif

%changelog
* Wed Feb 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.0-1
- Initial spec

