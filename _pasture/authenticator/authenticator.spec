%global commit 3d3d479c0d189bbe405393523d575ae3e292e5cf
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200908
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname Authenticator

Name:           authenticator
Version:        3.32.2
Release:        1%{?gver}%{?dist}
Summary:        2FA code generator for GNOME

License:        GPLv3+
URL:            https://gitlab.gnome.org/World/Authenticator

%if 0%{?with_snapshot}
Source0:        %{url}/-/archive/%{commit}/%{pkgname}-%{commit}.tar.bz2#/%{pkgname}-%{shortcommit}.tar.bz2
%else
Source0:        %{url}/-/archive/%{version}/%{pkgname}-%{version}.tar.bz2
%endif

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(zbar)
Requires:       glib2
Requires:       gtk3
Requires:       libsecret
Requires:       %{py3_dist beautifulsoup4}
Requires:       %{py3_dist pillow}
Requires:       %{py3_dist pyfavicon}
Requires:       %{py3_dist pyotp}
Requires:       %{py3_dist pyzbar}
Requires:       %{py3_dist yoyo-migrations}
#Recommends:     gnome-shell


%description
Simple application that generates a two-factor authentication code, created for GNOME

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif


%build
%meson
%meson_build


%install
%meson_install

desktop-file-validate %{buildroot}%{_datadir}/applications/com.github.bilelmoussaoui.%{pkgname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.github.bilelmoussaoui.%{pkgname}.metainfo.xml

%find_lang %{pkgname}


%files -f %{pkgname}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/%{name}-search-provider
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/com.github.bilelmoussaoui.%{pkgname}/
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/gnome-shell/search-providers/com.github.bilelmoussaoui.%{pkgname}.*
%{_metainfodir}/*.metainfo.xml
%{python3_sitelib}/%{pkgname}


%changelog
* Fri Sep 18 2020 Phantom X <megaphantomx at hotmail dot com> - 3.32.2-1.20200908git3d3d479
- Initial spec
