%global commit 11edbc6625c6962c491afc1b00e8dbc01c2246ca
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211226
%bcond_with snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global cname  nicotine
%global pkgname  nicotine-plus
%global appdata_id org.nicotine_plus.Nicotine
%global vc_url  https://github.com/%{pkgname}/%{pkgname}

Name:           nicotine+
Version:        3.3.5
Release:        100%{?dist}
Summary:        A graphical client for the SoulSeek peer-to-peer system

#   (see pynicotine/geoip/README.md)
# - some icons are LPGPLv3+, GPLv3+ and MIT (see img/CREDITS.md) 
License:        GPL-3.0-or-later AND CC-BY-SA-4.0 AND LGPL-3.0-or-later AND MIT
URL:            https://www.nicotine-plus.org/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-Disable-header_bar-as-default.patch
Patch1:         0001-Set-GTK3-as-default.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  %{py3_dist pygobject}
BuildRequires:  python3-devel
# check
BuildRequires:  ( gtk3 or gtk4 )
BuildRequires:  %{py3_dist pytest}
#BuildRequires:  xorg-x11-server-Xvfb
Requires:       gdbm
Requires:       ( gtk3 or gtk4 )
Requires:       %{py3_dist pygobject}
Requires:       hicolor-icon-theme
Recommends:     gspell

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{cname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Nicotine+ is a graphical client for the Soulseek peer-to-peer file sharing
network. It is an attempt to keep Nicotine working with the latest libraries,
kill bugs, keep current with the Soulseek protocol, and add some new features
that users want and/or need.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

%generate_buildrequires
%pyproject_buildrequires -r


%build
# This fixes files installation below
touch data/%{appdata_id}.desktop
touch data/%{appdata_id}.appdata.xml

%pyproject_wheel


%install
%pyproject_install

rm -rf %{buildroot}%{python3_sitelib}/pynicotine/plugins/examplars/

rm -rf %{buildroot}%{_datadir}/doc

%pyproject_save_files py%{cname}


%check
# Tests requiring an Internet connection are disabled
%pytest -k "not test_update_check"

desktop-file-validate %{buildroot}%{_datadir}/applications/%{appdata_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appdata_id}.appdata.xml


%files -f %{pyproject_files}
%license COPYING
%doc AUTHORS.md NEWS.md README.md TRANSLATORS.md
%{_bindir}/%{cname}
%{_datadir}/applications/%{appdata_id}.desktop
%{_datadir}/icons/hicolor/*/*/*.{png,svg}
%{_metainfodir}/%{appdata_id}.appdata.xml
%{_mandir}/man1/%{cname}.1*


%changelog
* Sun Sep 22 2024 Phantom X <megaphantomx at hotmail dot com> - 3.3.5-100
- 3.3.5

* Tue May 07 2024 Phantom X <megaphantomx at hotmail dot com> - 3.3.4-100
- 3.3.4

* Mon May 06 2024 Phantom X <megaphantomx at hotmail dot com> - 3.3.3-100
- 3.3.3

* Mon Feb 26 2024 Phantom X <megaphantomx at hotmail dot com> - 3.3.2-100
- 3.3.2

* Sat Feb 24 2024 Phantom X <megaphantomx at hotmail dot com> - 3.3.1-100
- 3.3.1

* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 3.3.0-100
- 3.3.0

* Sun Mar 05 2023 Phantom X <megaphantomx at hotmail dot com> - 3.2.9-100
- 3.2.9

* Sat Jan 07 2023 Phantom X <megaphantomx at hotmail dot com> - 3.2.8-100
- 3.2.8

* Thu Dec 01 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.7-100
- 3.2.7

* Fri Oct 21 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.6-100
- 3.2.6

* Wed Aug 31 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.5-100
- 3.2.5

* Sun Aug 07 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.4-100
- 3.2.4

* Sat Aug 06 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.3-100
- 3.2.3

* Sat Mar 19 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.2-100
- 3.2.2

* Thu Feb 10 2022 Phantom X <megaphantomx at hotmail dot com> - 3.2.1-100
- 3.2.1

* Mon Dec 27 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-101.20211226git11edbc6
- Snapshot

* Sun Dec 19 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-100
- 3.2.0

* Sat Nov 27 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-0.3.20211127git3b37806
- 3.2.0-rc2

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-0.2.20210930git646aa34
- Bump

* Sat Sep 18 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-0.1.20210917git0543b5e
- 3.2.0 dev
- Update to best packaging practices

* Tue Aug 03 2021 Phantom X <megaphantomx at hotmail dot com> - 3.1.1-100.20210803git211acd6
- 3.1.1

* Sun Aug 01 2021 Phantom X <megaphantomx at hotmail dot com> - 3.1.1-0.1.20210801git36d5014
- 3.1.1 snapshot

* Sun Jul 25 2021 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-100.20210724gitf5ba044
- 3.1.0
- Add xvfb-run BR for %%check depending on X

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 3.0.6-100
- 3.0.6

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 3.0.4-100
- 3.0.4

* Thu Apr 01 2021 Phantom X <megaphantomx at hotmail dot com> - 3.0.3-100.20210401gitaeba38d
- 3.0.3

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
