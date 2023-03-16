%global commit 2b5401034a6087050985bef6336f5686e9ae239c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220315
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global appname org.roger_ferrer.Eiciel_GTK3
%global pkgname eiciel
%global vc_url  https://github.com/rofirrim/%{pkgname}

Name:           %{pkgname}-gtk3
Version:        0.9.13.1
Release:        1%{?gver}%{?dist}
Summary:        Graphical editor for ACLs and xattr

License:        GPL-2.0-or-later
URL:            http://rofi.roger-ferrer.org/eiciel

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        http://rofi.roger-ferrer.org/%{pkgname}/files/%{pkgname}-%{version}.tar.bz2
%endif

Patch0:         0001-Rename-to-eiciel-GTK3.patch

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libattr)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib


%description
Graphical editor for access control lists (ACLs) and extended attributes
(xattr).

This is the GTK3 release, without Nautilus plugin support.


%prep
%autosetup %{?gver:-n %{pkgname}-%{commit}} -p1

rm -f src/eiciel_nautilus_page.*
mv src/org.roger-ferrer.Eiciel.appdata.xml src/%{appname}.appdata.xml
mv man/%{pkgname}.1 man/%{name}.1

iconv -f ISO-8859-1 -t UTF-8 AUTHORS > foo ; mv foo AUTHORS


%build
%meson
%meson_build


%install
%meson_install

%find_lang %{name}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml

%files -f %{name}.lang
%doc AUTHORS README.md
%license COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/gnome/help/%{name}/
%{_datadir}/applications/%{appname}.desktop
%{_mandir}/man1/%{name}*
%{_metainfodir}/%{appname}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Wed Sep 21 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.13.1-1.20220315git2b54010
- Initial spec

