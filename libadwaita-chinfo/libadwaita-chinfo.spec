%global apiver  1
%global gtk_version 4.15.2
%global glib_version 2.76.0

%global pkgname libadwaita
%global tarball_version %%(echo %{version} | tr '~' '.')
%global branch %%(echo %{version} | cut -d. -f-2)

Name:           %{pkgname}-chinfo
Version:        1.7.6
Release:        1%{?dist}
Summary:        Building blocks for modern GNOME applications - chinforpms modifications

License:        LGPL-2.1-or-later AND MIT
URL:            https://gitlab.gnome.org/GNOME/libadwaita
Source0:        https://download.gnome.org/sources/%{pkgname}/%(echo %{version} | cut -d~ -f1 | cut -d. -f-2)/%{pkgname}-%{tarball_version}.tar.xz
Source1:        chinfo-adwaita.css

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson >= 0.59.0
BuildRequires:  sassc

BuildRequires:  pkgconfig(appstream)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib_version}
BuildRequires:  pkgconfig(gtk4) >= %{gtk_version}

Requires:       %{pkgname}%{?_isa} >= %{branch}

Provides:       %{pkgname}-classic = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{pkgname}-classic%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude ^libadwaita-%{apiver}\\.so.*$


%description
Building blocks for modern GNOME applications.

This package contains a patched version of %{pkgname}, with some dirty
fixes from chinforpms.


%prep
%autosetup -p1 -n %{pkgname}-%{tarball_version}

cat %{S:1} | tee -a src/stylesheet/base{,-hc}.{,s}css > /dev/null


%build
%meson \
  -Dexamples=false \
  -Dgtk_doc=false \
  -Dintrospection=disabled \
  -Dtests=false \
  -Dvapi=false \
%{nil}

%meson_build


%install

%meson_install

rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -f %{buildroot}%{_libdir}/*.so
rm -rf %{buildroot}%{_libdir}/*/

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files
%license COPYING
%doc README.md AUTHORS NEWS
%{_libdir}/%{name}/*-%{apiver}.so.0*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Sun Sep 14 2025 Phantom X <megaphantomx at hotmail dot com> - 1.7.6-1
- 1.7.6

* Sun Mar 16 2025 Phantom X <megaphantomx at hotmail dot com> - 1.6.2-1
- 1.6.2

* Sun Oct 13 2024 Phantom X <megaphantomx at hotmail dot com> - 1.6.1-1
- 1.6.1

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1.6.0-1
- 1.6.0

* Mon May 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1.5.0-2
- Provides and requires tweaks

* Wed May 01 2024 Phantom X <megaphantomx at hotmail dot com> - 1.5.0-1
- Initial spec, rebased from libadwaita spec
