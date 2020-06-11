Name:           quiterss
Version:        0.19.4
Release:        100%{?dist}
Summary:        RSS/Atom aggregator
License:        GPLv3
URL:            http://quiterss.org/

Source0:        https://github.com/QuiteRSS/quiterss/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         %{name}-defaults.patch

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  qt5-linguist
BuildRequires:  qtsingleapplication-qt5-devel
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme

%description
Qt-based RSS/Atom aggregator.

%prep
%autosetup -p1
# be asuree
rm -rf 3rdparty/{qtsingleapplication,sqlite}

%build
%{qmake_qt5} PREFIX=%{_prefix} SYSTEMQTSA=True DISABLE_PHONON=1
%make_build release

%install
make install INSTALL_ROOT=%{buildroot}
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{name}.appdata.xml \
  %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name} --with-qt --without-mo

%files -f %{name}.lang
%doc AUTHORS CHANGELOG README.md
%license COPYING
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/sound/
%{_datadir}/%{name}/style/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_metainfodir}/*.xml


%changelog
* Wed Jun 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.19.4-100
- 0.19.4

* Fri Feb 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.19.3-100.chinfo
- 0.19.3

* Thu Nov 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.19.2-100.chinfo
- 0.19.2

* Mon Nov 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.19.1-100.chinfo
- 0.19.1

* Wed Jul 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.18.12-100.chinfo
- 0.18.12

* Fri Jun 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.18.11-100.chinfo
- 0.18.11

* Thu May 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.18.10-100.chinfo
- 0.18.10
- metainfo file

* Thu Jan 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.18.9-100.chinfo
- 0.18.9
- Qt5

* Fri Aug 25 2017 TI_Eugene <ti.eugene@gmail.com> - 0.18.8-1
- Version bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 10 2016 TI_Eugene <ti.eugene@gmail.com> - 0.18.4-1
- Version bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-2
- use %%qmake_qt4 macro to ensure proper build flags

* Tue Oct 06 2015 TI_Eugene <ti.eugene@gmail.com> - 0.18.2-1
- Version bump
- all patches removed

* Tue Jun 30 2015 TI_Eugene <ti.eugene@gmail.com> - 0.17.7-1
- Version bump
- some spec fixes

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.17.6-2
- Rebuilt for GCC 5 C++11 ABI change

* Sun Mar 15 2015 TI_Eugene <ti.eugene@gmail.com> - 0.17.6-1
- Version bump

* Mon Jan 19 2015 TI_Eugene <ti.eugene@gmail.com> - 0.17.4-1
- Version bump

* Tue Nov 18 2014 TI_Eugene <ti.eugene@gmail.com> - 0.17.1-1
- Version bump

* Tue Sep 23 2014 TI_Eugene <ti.eugene@gmail.com> - 0.17.0-1
- Version bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 21 2014 TI_Eugene <ti.eugene@gmail.com> - 0.16.1-1
- Version bump

* Fri Jun 13 2014 TI_Eugene <ti.eugene@gmail.com> - 0.16.0-1
- Version bump

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 19 2014 TI_Eugene <ti.eugene@gmail.com> - 0.15.4-1
- Version bump

* Thu Mar 20 2014 TI_Eugene <ti.eugene@gmail.com> - 0.15.2-1
- Version bump

* Fri Jan 31 2014 TI_Eugene <ti.eugene@gmail.com> - 0.14.3-1
- Version bump

* Fri Jan 03 2014 TI_Eugene <ti.eugene@gmail.com> - 0.14.2-1
- Version bump

* Sun Dec 08 2013 TI_Eugene <ti.eugene@gmail.com> - 0.14.1-1
- Version bump
- phonon-devel BR added

* Sat Nov 16 2013 TI_Eugene <ti.eugene@gmail.com> - 0.14.0-1
- Version bump

* Sat Aug 31 2013 TI_Eugene <ti.eugene@gmail.com> - 0.13.3-1
- Version bump

* Wed Jul 31 2013 TI_Eugene <ti.eugene@gmail.com> - 0.13.2-1
- Version bump

* Mon Jul 01 2013 TI_Eugene <ti.eugene@gmail.com> - 0.13.1-1
- Version bump

* Sat Jun 01 2013 TI_Eugene <ti.eugene@gmail.com> - 0.13.0-1
- Version bump

* Tue May 07 2013 TI_Eugene <ti.eugene@gmail.com> - 0.12.5-3
- icon scriptlet update

* Sun May 05 2013 TI_Eugene <ti.eugene@gmail.com> - 0.12.5-2
- qmake-qt4 used directly
-_smp_flags added to make

* Sat Apr 27 2013 TI_Eugene <ti.eugene@gmail.com> - 0.12.5-1
- initial packaging for Fedora
