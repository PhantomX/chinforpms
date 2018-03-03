Name:           libcloudproviders
Version:        0.2.5
Release:        100.chinfo%{?dist}
Summary:        Library for integration of cloud storage providers
License:        LGPLv3+
URL:            https://gitlab.gnome.org/Incubator/libcloudproviders
Source0:        https://gitlab.gnome.org/Incubator/libcloudproviders/uploads/32bb0a808c397d55b6d72c61540c0171/libcloudproviders-0.2.5.tar.xz
BuildRequires:  gcc
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
%{?systemd_requires}
BuildRequires:  systemd

%description
Cross desktop library for desktop integration of cloud storage providers
and sync tools.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson -Denable-gtk-doc=true
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%doc CHANGELOG README.md
%license LICENSE
%{_libdir}/libcloudproviders.so.*

%files devel
%{_includedir}/cloudproviders/
%{_libdir}/pkgconfig/cloudproviders.pc
%{_libdir}/*.so
%{_datadir}/gtk-doc/

%changelog
* Wed Feb 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.5-100.chinfo
- f27

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 31 2017 Carlos Soriano <csoriano@redhat.com> - 0.2.5-0.1
- Initial RPM release
