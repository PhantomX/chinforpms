%global commit 5391714b45d3a27991aa080fb0fe138a9d9eedd4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 202004716
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global cname  nicotine
%global vc_url  https://github.com/%{name}/%{name}

Name:           nicotine-plus
Version:        2.0.1
Release:        1%{?gver}%{?dist}
Summary:        A graphical client for the SoulSeek peer-to-peer system

# * nicotine+ - GPLv3 and LGPLv3  -- main tarball;
# * sounds/default/*.wav - CC0
License:        GPLv3 and LGPLv3 and CC0
URL:            https://www.nicotine-plus.org/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  python3-gobject
BuildRequires:  python3-devel
Requires:       gtk3
Requires:       libappindicator-gtk3
Requires:       libnotify
Requires:       python3-dbus
Requires:       python3-gobject
Requires:       python3-miniupnpc
Requires:       python3-mutagen
Requires:       hicolor-icon-theme
Recommends:     gspell
Recommends:     gsound

Provides:       %{cname}+ = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{cname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Nicotine+ is a graphical client for the Soulseek peer-to-peer file sharing
network. It is an attempt to keep Nicotine working with the latest libraries,
kill bugs, keep current with the Soulseek protocol, and add some new features
that users want and/or need.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%py3_build


%install
%py3_install

rm -rf %{buildroot}%{_datadir}/doc

%find_lang %{cname}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.nicotine_plus.Nicotine.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.nicotine_plus.Nicotine.appdata.xml


%files -f %{cname}.lang
%license COPYING
%doc AUTHORS.md NEWS README.md doc/TRANSLATORS.md
%{_bindir}/%{cname}
%{python3_sitelib}/%{cname}-*.egg-info
%{python3_sitelib}/py%{cname}/
%{_datadir}/%{cname}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_metainfodir}/*.appdata.xml
%{_mandir}/man1/*.1*


%changelog
* Fri Jul 17 2020 Phantom X <megaphantomx at hotmail dot com> - 2.0.1-1
- Initial spec
