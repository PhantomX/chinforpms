%global apiver  1

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:           libadwaita
Version:        1.2.1
Release:        100%{?dist}
Summary:        Building blocks for modern GNOME applications

Epoch:          1

License:        LGPLv2+
URL:            https://gitlab.gnome.org/GNOME/libadwaita
Source0:        https://download.gnome.org/sources/%{name}/%(echo %{version} | cut -d~ -f1 | cut -d. -f-2)/%{name}-%{tarball_version}.tar.xz
Source1:        chinforpms-adwaita.css

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gi-docgen
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 0.59.0
#BuildRequires:  sassc
BuildRequires:  vala

BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk4) >= 4.5

%description
Building blocks for modern GNOME applications.


%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       vala
Recommends:     %{name}-demo = %{?epoch:%{epoch}:}%{version}-%{release}
Recommends:     %{name}-doc = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
Development files for %{name}.


%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch

Recommends:     %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description    doc
Documentation files for %{name}.


%package        demo
Summary:        Demo files for %{name}
BuildArch:      noarch

Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Suggests:       %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description    demo
Demo files for %{name}.


%prep
%autosetup -p1 -n %{name}-%{tarball_version}

cat %{S:1} | tee -a src/stylesheet/base{,-hc}.css > /dev/null


%build
%meson \
    -Dgtk_doc=true \
    %{nil}

%meson_build


%install
%meson_install
%find_lang %{name}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%license COPYING
%doc README.md AUTHORS NEWS
%{_bindir}/adwaita-%{apiver}-demo
%{_libdir}/*-%{apiver}.so.0*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*-%{apiver}.gir
%{_datadir}/vala/vapi/%{name}-%{apiver}.*
%{_includedir}/%{name}-%{apiver}/
%{_libdir}/*-%{apiver}.so
%{_libdir}/pkgconfig/*-%{apiver}.pc

%files doc
%doc HACKING.md
%{_docdir}/%{name}-%{apiver}/

%files demo
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Jan 27 2023 Phantom X <megaphantomx at hotmail dot com> - 1:1.2.1-100
- 1.2.1

* Thu Sep 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.2.0-100
- 1.2.0

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.2~rc-100
- 1.2.rc

* Wed Jun 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.1.1-100
- 1.1.0

* Mon Apr 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.0-100
- Padding updates attempt

* Fri Mar 18 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.0-1
- chore(update): 1.1.0

* Mon Mar 07 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1~rc-1
- chore(update): 1.1.rc

* Mon Feb 14 2022 David King <amigadave@amigadave.com> - 1.1~beta-1
- Update to 1.1.beta (#2053942)

* Sat Feb 12 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.2-1
- chore(update): 1.0.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 02 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.1-1
- chore(update): 1.0.1

* Sat Jan 01 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-1
- chore(update): 1.0.0-1

* Tue Dec 07 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.7.beta.1
- chore(update): 1.0.0-0.7.beta.1

* Tue Nov 02 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.6.alpha.4
- chore(update): 1.0.0-0.6.alpha.4
- build: Add Demo subpackage

* Fri Oct 01 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.5.alpha.3
- chore(update): 1.0.0-0.5.alpha.3

* Mon Aug 30 2021 Lyes Saadi <fedora@lyes.eu> - 1.0.0-0.4.alpha.2
- Updating to alpha.2

* Thu Jun 24 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-0.3.alpha.1
- Initial package
