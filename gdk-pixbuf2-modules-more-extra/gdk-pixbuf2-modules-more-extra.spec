%global branch %%(echo %{version} | cut -d. -f-2)

Name:           gdk-pixbuf2-modules-more-extra
Version:        2.42.12
Release:        1%{?dist}
Summary:        More extra image loaders for gdk-pixbuf2

License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/gdk-pixbuf
Source0:        https://download.gnome.org/sources/gdk-pixbuf/%{branch}/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  meson
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info

Requires:       gdk-pixbuf2%{?_isa} > 2.43.0
Requires:       gdk-pixbuf2-modules-extra%{?_isa} > 2.43.0

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

This package contains contents a module for loading BMP, ICO, PNM and TGA images.

%prep
%autosetup -n gdk-pixbuf-%{version} -p1

%build
%meson \
       -Dpng=disabled \
       -Dtiff=disabled \
       -Djpeg=disabled \
       -Dgif=disabled \
       -Dothers=enabled \
       -Dbuiltin_loaders=none \
       -Ddocs=false \
       -Dgtk_doc=false \
       -Dintrospection=disabled \
       -Dman=false \
       -Dinstalled_tests=false \
       %{nil}

%global _smp_mflags -j1
%meson_build

%check
%meson_test

%install
%meson_install
rm -r %{buildroot}%{_bindir}
# gdk-pixbuf2 package includes locale data for our modules
rm -rf %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-{ani,icns,qtif,xbm,xpm}.so
rm -f %{buildroot}%{_libdir}/libgdk_pixbuf-2.0*
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_datadir}/thumbnailers

%files
%license COPYING
%doc NEWS README.md
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so

%changelog
* Tue Sep 23 2025 Phantom X <megaphantomx at hotmail dot com> - 2.42.12-1
- Initial spec

