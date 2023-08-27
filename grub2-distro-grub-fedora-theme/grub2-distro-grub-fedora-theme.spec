%global debug_package %{nil}

%global commit c1063effd1d15345661a15b12c148926d529d46d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230227
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global _grubthemedir /boot/grub2/themes

%global pkgname distro-grub-themes
%global vc_url https://github.com/AdisonCavani/%{pkgname}


Name:           grub2-distro-grub-fedora-theme
Version:        3.2
Release:        1%{?dist}
Summary:        A pack of GRUB2 themes for each Linux distribution - Fedora theme

License:        GPL-3.0-only
URL:            https://k1ng.dev/%{pkgname}

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

Source10:       README.fedora

# matches grub2 pkg archs
ExcludeArch:    s390 s390x %{arm}
%ifnarch aarch64
Requires:       (grub2-efi or grub2)
%else
Requires:       grub2-efi
%endif

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
A pack of GRUB2 themes for different Linux distributions and OSs.
It aims to replace the default GRUB look, with a nice and colorful theme.

Only Fedora theme is provided.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

install -m644 -p %{S:10} .


%build


%install
mkdir -p %{buildroot}%{_grubthemedir}/distro-grub-fedora/icons
install -pm0644 assets/{fonts,menu}/* %{buildroot}%{_grubthemedir}/distro-grub-fedora/
install -pm0644 assets/icons/* %{buildroot}%{_grubthemedir}/distro-grub-fedora/icons/
install -pm0644 assets/backgrounds/fedora.png %{buildroot}%{_grubthemedir}/distro-grub-fedora/background.png
install -pm0644 assets/theme.txt %{buildroot}%{_grubthemedir}/distro-grub-fedora

%files
%license LICENSE
%doc README.*
%{_grubthemedir}/distro-grub-fedora


%changelog
* Sat Aug 26 2023 Phantom X <megaphantomx at hotmail dot com> - 3.2-1
- 3.2

* Fri Mar 31 2023 Phantom X <megaphantomx at hotmail dot com> - 3.1-1.20230227gitc1063ef
- Initial spec
