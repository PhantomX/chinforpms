# Disable glycin
# https://gitlab.freedesktop.org/drm/amd/-/issues/4568
%bcond glycin 0

%global glib2_version 2.56.0

# Normally we want auto features enabled to ensure no important feature gets
# disabled by mistake. But in this package, the auto features are mostly legacy
# or unwanted, and we should manually enable only what we want.
%global __meson_auto_features disabled

%global branch %%(echo %{version} | cut -d. -f-2)

Name:           gdk-pixbuf2
Version:        2.44.1
Release:        100%{?dist}
Summary:        An image loading library

Epoch:          1

License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/gdk-pixbuf
Source0:        https://download.gnome.org/sources/gdk-pixbuf/%{branch}/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  docbook-style-xsl
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
%if %{with glycin}
BuildRequires:  pkgconfig(glycin-2)
%else
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libtiff-4)
%endif
BuildRequires:  libxslt
BuildRequires:  meson
BuildRequires:  pkgconfig(gobject-introspection-1.0)
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info
BuildRequires:  /usr/bin/rst2man

Requires: glib2%{?_isa} >= %{glib2_version}
# We also need MIME information at runtime
Requires: shared-mime-info

%if %{with glycin}
# All modules previously provided by gdk-pixbuf itself are obsoleted by Glycin.
Obsoletes: %{name}-modules < %{?epoch:%{epoch}:}%{version}-%{release}

# Most third-party pixbuf loaders are also obsolete. If Glycin supports the
# format, then it will take precedence and the third-party loader won't be used.
# The Provides can be removed when nothing in Fedora depends on them anymore.
Obsoletes: avif-pixbuf-loader <= 1.1.1-4
Provides:  avif-pixbuf-loader
Obsoletes: heif-pixbuf-loader <= 1.20.1-2
Provides:  heif-pixbuf-loader
Obsoletes: jxl-pixbuf-loader <= 0.11.1-4
Provides:  jxl-pixbuf-loader
Obsoletes: rsvg-pixbuf-loader <= 2.61.0-1
Provides:  rsvg-pixbuf-loader
Obsoletes: webp-pixbuf-loader <= 0.2.7-4
Provides:  webp-pixbuf-loader
%endif

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%if %{without glycin}
%package modules
Summary: GIF and TIFF modules for gdk-pixbuf2
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Recommend external pixbuf loaders for popular image formats only.
# Please do not recommend obscure image formats here.
%if ! 0%{?rhel}
# these are not shipped in RHEL
Recommends: avif-pixbuf-loader
Recommends: jxl-pixbuf-loader
Recommends: webp-pixbuf-loader
%endif
Recommends: rsvg-pixbuf-loader

%description modules
This package contains the additional modules that are needed to load GIF and
TIFF images.
%endif

%package devel
Summary: Development files for gdk-pixbuf2
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: glib2-devel%{?_isa} >= %{glib2_version}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends: gi-docgen-fonts

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf2.

%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -n gdk-pixbuf-%{version} -p1

%build
%meson \
       -Ddocumentation=true \
       -Dintrospection=enabled \
%if %{with glycin}
       -Dglycin=enabled \
%else
       -Dgif=enabled \
       -Djpeg=enabled \
       -Dpng=enabled \
       -Dtiff=enabled \
       -Dthumbnailer=enabled \
%endif
       %{nil}
%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
touch %{buildroot}%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

# Rename gdk-pixbuf-query-loaders
(cd %{buildroot}%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)
# ... and fix up gdk-pixbuf-query-loaders reference in the .pc file
sed -i -e 's/gdk-pixbuf-query-loaders/gdk-pixbuf-query-loaders-%{__isa_bits}/' \
    %{buildroot}%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc

%find_lang gdk-pixbuf

%transfiletriggerin -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%transfiletriggerpostun -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%files -f gdk-pixbuf.lang
%license COPYING
%doc NEWS README.md
%{_libdir}/libgdk_pixbuf-2.0.so.0{,.*}
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*
%if %{without glycin}
%{_bindir}/gdk-pixbuf-thumbnailer
%{_datadir}/thumbnailers/
%endif

%if %{without glycin}
%files modules
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so
%endif

%files devel
%dir %{_includedir}/gdk-pixbuf-2.0
%{_includedir}/gdk-pixbuf-2.0/gdk-pixbuf
%{_libdir}/libgdk_pixbuf-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0/
%{_mandir}/man1/gdk-pixbuf-csource.1*
%doc %{_datadir}/doc/gdk-pixbuf/
%doc %{_datadir}/doc/gdk-pixdata/

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
* Mon Sep 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.44.1-100
- Disable glycin for the time

