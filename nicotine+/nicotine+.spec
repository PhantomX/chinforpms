%global commit 646aa343679ae0814428905a2c3ea3c590665834
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210930
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global cname  nicotine
%global pkgname  nicotine-plus
%global vc_url  https://github.com/%{pkgname}/%{pkgname}

Name:           nicotine+
Version:        3.2.0
Release:        0.2%{?gver}%{?dist}
Summary:        A graphical client for the SoulSeek peer-to-peer system

#   (see pynicotine/geoip/README.md)
# - some icons are LPGPLv3+, GPLv3+ and MIT (see img/CREDITS.md) 
License:        GPLv3+ and CC-BY-SA and LGPLv3+ and MIT
URL:            https://www.nicotine-plus.org/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  %{py3_dist pygobject}
BuildRequires:  python3-devel
# check
BuildRequires:  gtk3
BuildRequires:  %{py3_dist pytest}
#BuildRequires:  xorg-x11-server-Xvfb
Requires:       gdbm
Requires:       gtk3
Requires:       libappindicator-gtk3
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
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

rm -rf %{buildroot}%{python3_sitelib}/pynicotine/plugins/examplars/

rm -rf %{buildroot}%{_datadir}/doc

%pyproject_save_files py%{cname}

%find_lang %{cname}


%check
%global __pytest xvfb-run /usr/bin/pytest
# Tests requiring an Internet connection are disabled
%dnl GDK_BACKEND=x11 %pytest --deselect=test/unit/test_version.py

desktop-file-validate %{buildroot}%{_datadir}/applications/org.nicotine_plus.Nicotine.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.nicotine_plus.Nicotine.metainfo.xml


%files -f %{cname}.lang -f %{pyproject_files}
%license COPYING
%doc AUTHORS.md NEWS.md README.md TRANSLATORS.md
%{_bindir}/%{cname}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_metainfodir}/*.metainfo.xml
%{_mandir}/man1/*.1*


%changelog
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
