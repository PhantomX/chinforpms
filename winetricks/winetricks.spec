%global commit e73c4d8f71801fe842c0276b603d9c8024d6d957
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250212
%bcond_without snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global appname io.github.winetricks.Winetricks

Name:           winetricks
Version:        20250105
Release:        100%{?dist}

Summary:        Work around common problems in Wine

License:        LGPL-2.1-or-later
URL:            https://github.com/Winetricks/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

# need arch-specific wine, not available everywhere:
# - adopted from wine.spec
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
# - explicitly not ppc64* to hopefully not confuse koschei
ExcludeArch:    ppc64 ppc64le

BuildRequires:  make
BuildRequires:  wine-common
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       wine-common
Requires:       cabextract gzip unzip wget which
Requires:       hicolor-icon-theme
Requires:       (kdialog if kdialog else zenity)

%description
Winetricks is an easy way to work around common problems in Wine.

It has a menu of supported games/apps for which it can do all the
workarounds automatically. It also lets you install missing DLLs
or tweak various Wine settings individually.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed -i -e s:steam:: -e s:flash:: tests/*

%build
# not needed

%install
%make_install
# some tarballs do not install appdata
install -m0644 -D -t %{buildroot}%{_datadir}/metainfo src/%{appname}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license COPYING debian/copyright
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/%{appname}.metainfo.xml


%changelog
* Thu Feb 20 2025 Phantom X <megaphantomx at hotmail dot com> - 20250105-100.20250212gite73c4d8
- 20250105

* Thu Feb 15 2024 Phantom X <megaphantomx at hotmail dot com> - 20240105-100.20240210git6f40a93
- 20240105

* Sun Feb 26 2023 Phantom X <megaphantomx at hotmail dot com> - 20230212-100.20230224gita7e8a73
- 20230212

* Mon Aug 15 2022 Phantom X <megaphantomx at hotmail dot com> - 20220411-101.20220808git68ca8c3
- Snapshot

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 20220411-100
- 20220411

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 20220328-100
- 20220328

* Fri Feb 25 2022 Phantom X <megaphantomx at hotmail dot com> - 20211230-100.20220207gitd431b15
- 20211230-test snapshot

* Tue Dec 28 2021 Phantom X <megaphantomx at hotmail dot com> - 20210825-102.20211221gitccf2ed5
- Bump

* Sun Dec 12 2021 Phantom X <megaphantomx at hotmail dot com> - 20210825-101.20211205git164d243
- Snapshot

* Wed Aug 25 2021 Phantom X <megaphantomx at hotmail dot com> - 20210825-100
- 20210825

* Sun Jul 04 2021 Phantom X <megaphantomx at hotmail dot com> - 20210206-102.20210618git1b4f353
- Update

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 20210206-101.20210415git160b0b8
- Bump

* Sun Feb 14 2021 Phantom X <megaphantomx at hotmail dot com> - 20210206-100.20210209git8d5194b
- 20210206

* Sat Jan 23 2021 Phantom X <megaphantomx at hotmail dot com> - 20201206-101.20210113gitd7653d4
- Snapshot

* Mon Dec  7 2020 Phantom X <megaphantomx at hotmail dot com> - 20201206-100
- 20201206

* Tue Nov  3 2020 Phantom X <megaphantomx at hotmail dot com> - 20200412-103.20201024git9c542b6
- Update

* Wed Sep 30 2020 Phantom X <megaphantomx at hotmail dot com> - 20200412-102.20200929git604eccf
- New snapshot

* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 20200412-101.20200804gitfdd6b46
- Bump

* Sat May 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 20200412-100.20200523git24faee0
- Snapshot

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 - Ernestas Kulik <ekulik@redhat.com> - 20191224-1
- Update to 20191224

* Fri Sep 13 2019 - Ernestas Kulik <ekulik@redhat.com> - 20190912-1
- Update to 20190912

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190615-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 - Ernestas Kulik <ekulik@redhat.com> - 20190615-1
- Update to 20190615

* Tue Mar 12 2019 Ernestas Kulik <ekulik@redhat.com> - 20190310-1
- Update to 20190310

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Ernestas Kulik <ekulik@redhat.com> - 20181203-2
- Drop old path appdata exclude
- Add bash completions

* Sun Jan 20 2019 Ernestas Kulik <ekulik@redhat.com> - 20181203-1
- Update to 20181203

* Sun Jan 20 2019 Ernestas Kulik <ekulik@redhat.com> - 20180603-4
- Add dependency on zenity or kdialog for GUI

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180603-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Raphael Groner <projects.rg@smart.ms> - 20180603-2
- avoid shebang warning of rpmlint for appdata

* Sat Jun 23 2018 Raphael Groner <projects.rg@smart.ms> - 20180603-1
- new version

* Mon Mar 05 2018 Raphael Groner <projects.rg@smart.ms> - 20180217-1
- new version
- drop obsolete scriptlets
- move appdata into mimeinfo

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Ben Rosser <rosser.bjr@gmail.com> - 20171222-1
- Updated to latest upstream release. (#1528622)
- Moved appdata file to new appdata location, /usr/share/metainfo.
- Removed dependency on 'time' package as per #1533795.

* Sun Dec 03 2017 Raphael Groner <projects.rg@smart.ms> - 20171018-1
- new version
- ensure appdata gets installed

* Sun Aug 13 2017 Raphael Groner <projects.rg@smart.ms> - 20170731-1
- new snapshot
- add appdata

* Sun Aug 13 2017 Raphael Groner <projects.rg@smart.ms> - 20170614-1
- new version

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170517-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Raphael Groner <projects.rg@smart.ms> - 20170517-1
- new version

* Tue Mar 28 2017 Raphael Groner <projects.rg@smart.ms> - 20170326-1
- new version

* Sat Feb 11 2017 Raphael Groner <projects.rg@smart.ms> - 20170207-1
- new version
- drop additional icon and desktop file in favor of upstream ones

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161107-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 05 2016 Builder <projects.rg@smart.ms> - 20161107-2
- add ExcludeArch

* Wed Nov 09 2016 Raphael Groner <projects.rg@smart.ms> - 20161107-1
- new version

* Mon Nov 07 2016 Raphael Groner <projects.rg@smart.ms> - 20161012-1
- new version
- disable architectures without available wine
- don't check explicitly for wine version

* Sun Oct 09 2016 Raphael Groner <projects.rg@smart.ms> - 20161005-2
- use apps subfolder for icon

* Sun Oct 09 2016 Raphael Groner <projects.rg@smart.ms> - 20161005-1
- new version
- add copyright
- add icon

* Fri Jul 29 2016 Raphael Groner <projects.rg@smart.ms> - 20160724-1
- new version

* Mon Jul 11 2016 Raphael Groner <projects.rg@smart.ms> - 20160709-1
- initial
