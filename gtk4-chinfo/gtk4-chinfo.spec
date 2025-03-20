%if 0%{?fedora}
%global with_broadway 1
%endif

%global with_tracker 0

%global glib2_version 2.80.0
%global pango_version 1.56.0
%global cairo_version 1.18.0
%global gdk_pixbuf_version 2.30.0
%global gstreamer_version 1.24.0
%global harfbuzz_version 8.4
%global wayland_protocols_version 1.31
%global wayland_version 1.21.0
%global epoxy_version 1.4

%global bin_version 4.0.0

# Filter provides for private modules
%global __provides_exclude_from ^%{_libdir}/gtk-4.0

# FTBFS on i686 with GCC 14 -Werror=int-conversion
# https://gitlab.gnome.org/GNOME/gtk/-/issues/6033
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%ifarch %{ix86}
%global build_type_safety_c 1
%endif
%endif

%global pkgname gtk4
%global branch %%(echo %{version} | cut -d. -f-2)

Name:           %{pkgname}-chinfo
Version:        4.17.6
Release:        1%{?dist}
Summary:        GTK graphical user interface library - chinforpms modifications

Epoch:          1

License:        LGPL-2.0-or-later
URL:            https://www.gtk.org

Source0:        https://download.gnome.org/sources/gtk/%{branch}/gtk-%{version}.tar.xz
Source2:        chinfo-adwaita.css

# Disable this @#$& by default
Patch100:       0001-Disable-overlay-scrolling.patch
Patch101:       0001-set-atril-as-print-preview.patch
Patch102:       0001-CSD-server-side-shadow.patch
Patch103:       0001-CSD-Prefer-SSD-by-default.patch

Patch120:       0001-appearance-disable-backdrop.patch
Patch121:       0001-appearance-fix-black-border.patch
%dnl Patch122:       0001-CSD-disabled-by-default.patch

BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  glslc
BuildRequires:  meson
BuildRequires:  python3-gobject
BuildRequires:  pkgconfig(avahi-gobject)
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
BuildRequires:  pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires:  pkgconfig(colord)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(graphene-gobject-1.0)
BuildRequires:  pkgconfig(gstreamer-player-1.0) >= %{gstreamer_version}
BuildRequires:  pkgconfig(harfbuzz) >= %{harfbuzz_version}
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  pkgconfig(sysprof-capture-4)
%if 0%{?with_tracker}
BuildRequires:  pkgconfig(tracker-sparql-3.0)
%endif
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)

Requires:       %{pkgname}%{?_isa} >= %{branch}

Provides:       %{pkgname}-classic = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{pkgname}-classic%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude ^libgtk-4\\.so.*$


%description
GTK is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains a patched version 4 of GTK, with some dirty
fixes from chinforpms.


%prep
%autosetup -p1 -n gtk-%{version}

cat %{S:2} | tee -a gtk/theme/Default/Default-{light,dark}.css > /dev/null
cat %{S:2} | tee -a gtk/theme/Default/Default-hc{,-dark}.css > /dev/null


%build
%set_build_flags
export CFLAGS+=' -fno-strict-aliasing -DG_DISABLE_CAST_CHECKS -DG_DISABLE_ASSERT'
%meson \
%if 0%{?with_broadway}
        -Dbroadway-backend=true \
%endif
        -Dsysprof=enabled \
%if 0%{?with_tracker}
        -Dtracker=enabled \
%endif
        -Dcolord=enabled \
        -Ddocumentation=false \
        -Dman-pages=false \
        -Dintrospection=disabled \
        -Dbuild-demos=false \
        -Dbuild-testsuite=false \
        -Dbuild-examples=false \
        -Dbuild-tests=false \
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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_libdir}/%{name}/libgtk-4.so.1*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1:4.17.6-1
- 4.17.6

* Fri Jan 03 2025 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.12-1
- 4.16.12

* Tue Dec 17 2024 Phantom X - 1:4.16.7-3
- Again

* Mon Dec 16 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.7-2
- Fix overlay scrolling patch

* Sun Nov 24 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.7-1
- 4.16.7

* Thu Nov 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.6-1
- 4.16.6

* Fri Nov 01 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.54-1
- 4.16.5

* Fri Oct 04 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.3-1
- 4.16.3

* Tue Sep 24 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.2-1
- 4.16.2

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.16.1-1
- 4.16.1

* Sat Aug 24 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.14.5-1
- 4.14.5

* Mon May 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.14.4-2
- Provides and requires tweaks

* Sat May 04 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.14.4-1
- 4.14.4

* Sat Apr 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1:4.14.3-1
- Initial spec, rebased from gtk4 spec

