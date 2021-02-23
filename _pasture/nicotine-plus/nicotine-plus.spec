%global commit c4ff58305ff3b8dc4b94dcc2cc0a7f89a026336b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20201013
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global cname  nicotine
%global vc_url  https://github.com/%{name}/%{name}

Name:           nicotine-plus
Version:        3.0.0
Release:        100%{?gver}%{?dist}
Summary:        A graphical client for the SoulSeek peer-to-peer system

#   (see pynicotine/geoip/README.md)
# - some icons are LPGPLv3+, GPLv3+ and MIT (see img/CREDITS.md) 
License:        GPLv3+ and CC-BY-SA and LGPLv3+ and MIT
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
BuildRequires:  %{py3_dist pygobject}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  python3-devel
Requires:       gdbm
Requires:       gtk3
Requires:       libappindicator-gtk3
Requires:       %{py3_dist pygobject}
Requires:       hicolor-icon-theme
Recommends:     gspell

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

rm -rf %{buildroot}%{python3_sitelib}/pynicotine/plugins/examplars/

rm -rf %{buildroot}%{_datadir}/doc

%find_lang %{cname}


%check
# Tests requiring an Internet connection are disabled
%pytest --deselect=test/unit/test_version.py

desktop-file-validate %{buildroot}%{_datadir}/applications/org.nicotine_plus.Nicotine.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.nicotine_plus.Nicotine.metainfo.xml


%files -f %{cname}.lang
%license COPYING
%doc AUTHORS.md NEWS.md README.md TRANSLATORS.md files/icons/CREDITS.md
%{_bindir}/%{cname}
%{python3_sitelib}/*-*.egg-info
%{python3_sitelib}/py%{cname}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_metainfodir}/*.metainfo.xml
%{_mandir}/man1/*.1*


%changelog
* Mon Feb 22 2021 Phantom X <megaphantomx at hotmail dot com> - 3.0.0-100
- 3.0.0

* Thu Dec 24 2020 Phantom X <megaphantomx at hotmail dot com> - 2.2.2-100
- 2.2.2

* Mon Dec 14 2020 Phantom X <megaphantomx at hotmail dot com> - 2.2.1-100
- 2.2.1

* Fri Dec 04 2020 Phantom X <megaphantomx at hotmail dot com> - 2.2.0-100
- 2.2.0
- Remove unneeded dependencies

* Tue Oct 13 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.2-100.20201013gitc4ff583
- 2.1.2
- Rawhide sync

* Sun Sep 27 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.1-1.20200927git8631190
- 2.1.1

* Sat Sep 19 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-1.20200916git30e6394
- 2.1.0

* Tue Aug 25 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-0.3.20200825git868f9d5
- New snapshot

* Sun Aug 16 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-0.2.20200815git4fcaf09
- Bump

* Fri Aug 07 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-0.1.20200806git69d4c8d
- Snapshot
- BR: python3-mutagen -> python3-pytaglib

* Fri Jul 17 2020 Phantom X <megaphantomx at hotmail dot com> - 2.0.1-1
- Initial spec
