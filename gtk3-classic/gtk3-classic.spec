%global with_broadway 1

%global with_cloudprovides 0
%global with_sysprof 1
%global with_tracker 0

%global glib2_version 2.57.2
%global pango_version 1.41.0
%global atk_version 2.32.0
%global cairo_version 1.14.0
%global gdk_pixbuf_version 2.30.0
%global xrandr_version 1.5.0
%global wayland_version 1.14.91
%global wayland_protocols_version 1.14
%global epoxy_version 1.4

%global bin_version 3.0.0

%global _changelog_trimtime %(date +%s -d "1 year ago")

# Filter provides for private modules
%global __provides_exclude_from ^%{_libdir}/gtk-3.0

%global classic_url https://github.com/lah7/gtk3-classic
%global classic_ver 3.24.43-2
%if 0%(echo %{classic_ver} | grep -q \\. ; echo $?) == 0
%global mspkgver %{classic_ver}
%else
%global mspkgver %(c=%{classic_ver}; echo ${c:0:7})
%endif
%global classic_dir gtk3-classic-%{classic_ver}

%global vc_url https://gitlab.gnome.org/GNOME/gtk/-

%global pkgname gtk3
%global branch %%(echo %{version} | cut -d. -f-2)

Name:           %{pkgname}-classic
Version:        3.24.43
Release:        1%{?dist}
Summary:        The GIMP ToolKit (GTK+), a library for creating GUIs for X

Epoch:          2

License:        LGPL-2.0-or-later
URL:            http://www.gtk.org

Source0:        http://download.gnome.org/sources/gtk+/%(echo %{version} | cut -d. -f-2)/gtk+-%{version}.tar.xz
Source1:        %{classic_url}/archive/%{classic_ver}/gtk3-classic-%{mspkgver}.tar.gz
Source2:        chinforpms-adwaita.css
Source3:        README.chinforpms

# Revert some good features dropped by upstream (3.10)
Patch100:       gtk+3-3.23.0-gtk-recent-files-limit.patch
Patch101:       0001-Restore-gtk-toolbar-icon-size.patch
Patch102:       gtk+3-3.22.0-gtk-toolbar-style.patch

# Disable this @#$& by default
Patch103:       0001-Disable-overlay-scrolling.patch

Patch104:       gtk+3-startup-mode-cwd.patch
Patch105:       gtk+3-dateformat-with_time.patch
Patch106:       gtk+3-location_mode-filename.patch
Patch107:       gtk+3-print-preview.patch
Patch108:       0001-CSD-Disable-shadows-by-default.patch
Patch109:       0001-CSD-Prefer-SSD-by-default.patch

# Debian
Patch200:       016_no_offscreen_widgets_grabbing.patch
Patch201:       017_no_offscreen_device_grabbing.patch

# Ubuntu
Patch300:       restore_filechooser_typeaheadfind.patch

Patch500:       0001-Rename-Settings.FileChooser.gschema-to-gtk-classic.patch

BuildRequires: pkgconfig(atk) >= %{atk_version}
BuildRequires: pkgconfig(atk-bridge-2.0)
BuildRequires: pkgconfig(avahi-gobject)
BuildRequires: pkgconfig(cairo) >= %{cairo_version}
BuildRequires: pkgconfig(cairo-gobject) >= %{cairo_version}
%if 0%{?with_cloudprovides}
BuildRequires:  pkgconfig(cloudproviders)
%endif
BuildRequires: pkgconfig(colord)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(epoxy) >= %{epoxy_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(iso-codes)
BuildRequires: pkgconfig(pango) >= %{pango_version}
%if 0%{?with_sysprof}
BuildRequires:  pkgconfig(sysprof-capture-4)
%endif
%if 0%{?with_tracker}
BuildRequires:  pkgconfig(tracker-sparql-3.0)
%endif
BuildRequires: pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xrandr) >= %{xrandr_version}
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xinerama)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: meson
BuildRequires:  make
#BuildRequires:  sassc

Requires:       %{pkgname}%{?_isa} >= %{branch}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude ^libgtk-3\\.so.*$
%global __requires_exclude ^libgdk-3\\.so.*$
%global __requires_exclude ^libgailutil-3\\.so.*$


%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 3 of GTK+, with gtk3-classic and other
usability and cosmetic modifications.


%prep
%autosetup -n gtk+-%{version} -N -p1 -a 1
%autopatch -M 499 -p1

patch_command(){
  %{__scm_apply_patch -p1 -q} -i %{classic_dir}/$1
}
patch_command appearance__buttons-menus-icons.patch
patch_command appearance__disable-backdrop.patch
patch_command appearance__file-chooser.patch
patch_command appearance__fix_black_border.patch
patch_command appearance__message-dialogs.patch
patch_command appearance__print-dialog.patch
patch_command appearance__smaller-statusbar.patch
patch_command csd__clean-headerbar.patch
patch_command csd__disabled-by-default.patch
patch_command csd__server-side-shadow.patch
patch_command fixes__labels-wrapping.patch
patch_command fixes__primary_selection.patch
patch_command fixes__wayland_dialogs_header_setting.patch
patch_command other__mnemonics-delay.patch
patch_command other__remove_dead_keys_underline.patch
patch_command popovers__color-chooser.patch
patch_command popovers__file-chooser-list.patch
patch_command popovers__places-sidebar.patch
patch_command notebook_wheel_scroll.patch
patch_command treeview__alternating_row_colours.patch
patch_command window__rgba-visual.patch

%patch -P 500 -p1
mv gtk/org.gtk.Settings.FileChooser.gschema.xml gtk/org.gtk-classic.Settings.FileChooser.gschema.xml

cp %{classic_dir}/README.md README-classic.md

cat %{S:2} | tee -a gtk/theme/Adwaita/gtk-contained{,-dark}.css > /dev/null

cp -p %{S:3} .

rm -fv gtk/gtkresources.c
rm -fv testsuite/gtk/gtkresources.c testsuite/gtk/gtkprivate.c

%build
%set_build_flags
export CFLAGS+=" -fno-strict-aliasing"

%meson \
%if 0%{?with_broadway}
        -Dbroadway_backend=true \
%endif
        -Dbuiltin_immodules=wayland,waylandgtk \
        -Dcolord=yes \
%if 0%{?with_cloudprovides}
        -Dcloudproviders=true \
%endif
        -Dgtk_doc=false \
        -Dinstalled_tests=false \
        -Dman=false \
%if 0%{?with_sysprof}
        -Dprofiler=true \
%endif
%if 0%{?with_tracker}
        -Dtracker3=true \
%endif
        -Dxinerama=yes \
%{nil}

%meson_build


%install
%meson_install

rm -f %{buildroot}%{_datadir}/glib-2.0/schemas/org.gtk.*.gschema.xml
mv %{buildroot}%{_datadir}/glib-2.0 _glib-2.0

rm -rf %{buildroot}%{_sysconfdir}/*
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}/*
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -f %{buildroot}%{_libdir}/*.so
rm -rf %{buildroot}%{_libdir}/*/

mv _glib-2.0 %{buildroot}%{_datadir}/glib-2.0

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license COPYING
%doc NEWS README.md README-classic.md README.chinforpms
%{_libdir}/%{name}/libgtk-3.so.*
%{_libdir}/%{name}/libgdk-3.so.*
%{_libdir}/%{name}/libgailutil-3.so.*
%{_datadir}/glib-2.0/schemas/org.gtk-classic.Settings.FileChooser.gschema.xml
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Wed Aug 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1:3.24.43-1
- Initial spec, rebased from gtk3 spec

