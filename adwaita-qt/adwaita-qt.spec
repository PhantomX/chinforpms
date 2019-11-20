%global commit 1d09ba4c764a62e4275ad0667ec3e61916fa9957
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20191104
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           adwaita-qt
Version:        1.1.0
Release:        101%{?gver}%{?dist}

License:        LGPLv2+
Summary:        Adwaita theme for Qt-based applications

Epoch:          1

Url:            https://github.com/MartinBriza/adwaita-qt

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

# Remove some ugly paddings
Patch10:        %{name}-chinforpms.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt4-devel
BuildRequires:  qt5-qtbase-devel

Requires:       adwaita-qt4

%description
Theme to let Qt applications fit nicely into Fedora Workstation


%package -n adwaita-qt4
Summary:        Adwaita Qt4 theme

%description -n adwaita-qt4
Adwaita theme variant for applications utilizing Qt4


%package -n adwaita-qt5
Summary:        Adwaita Qt5 theme

%description -n adwaita-qt5
Adwaita theme variant for applications utilizing Qt5


%package -n adwaita-qt-common
Summary:        Adwaita Qt common files

%description -n adwaita-qt-common


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif


%build
mkdir -p "%{_target_platform}-qt4"
pushd "%{_target_platform}-qt4"
%{cmake} -DUSE_QT4=true ..
popd

mkdir -p "%{_target_platform}-qt5"
pushd "%{_target_platform}-qt5"
%{cmake} ..
popd

%make_build -C "%{_target_platform}-qt4"
%make_build -C "%{_target_platform}-qt5"


%install
make install/fast DESTDIR=%{buildroot} -C "%{_target_platform}-qt4"
make install/fast DESTDIR=%{buildroot} -C "%{_target_platform}-qt5"


%files -n adwaita-qt4
%doc LICENSE.LGPL2 README.md
%{_qt4_plugindir}/styles/adwaita.so

%files -n adwaita-qt5
%doc LICENSE.LGPL2 README.md
%{_qt5_plugindir}/styles/adwaita.so

%files -n adwaita-qt-common

%files


%changelog
* Tue Nov 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1.0-101.20191104git1d09ba4
- Snapshot

* Fri Aug 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1.0-100
- 1.1.0
- Rawhide sync

* Wed Dec 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0-100
- Remove ugly paddings

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 26 2017 Martin Bříza <mbriza@redhat.com> - 1.0-1
- Update to 1.0

* Mon Feb 27 2017 Martin Briza <mbriza@redhat.com> - 0.98-1
- Update to 0.98
- Fixes #1410597

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.97-2
- drop hardcoded Requires: qt4/qt5-qtbase

* Wed Dec 14 2016 Martin Briza <mbriza@redhat.com> - 0.97-1
- Update to 0.97

* Tue Dec 13 2016 Martin Briza <mbriza@redhat.com> - 0.95-1
- Update to 0.95

* Thu Jun 30 2016 Jan Grulich <jgrulich@redhat.com> - 0.4-3
- Properly fix missing menubar in QtCreator

* Wed Jun 22 2016 Jan Grulich <jgrulich@redhat.com> - 0.4-2
- Attempt to fix missing menubar issue in QtCreator

* Thu Apr 21 2016 Jan Grulich <jgrulich@redhat.com> - 0.4-1
- Update to version 0.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 20 2015 Martin Briza <mbriza@redhat.com> - 0.3-1
- Updated to the latest release
- Added a Qt5 build

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.7.20141216git024b00bf
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0-0.6.20141216git024b00bf
- Rebuilt for GCC 5 C++11 ABI change

* Fri Jan 16 2015 Martin Briza <mbriza@redhat.com> - 0-0.5
- Package review cleanup
- Split into a base and a subpackage
- Fedora import

* Tue Dec 16 2014 Martin Briza <mbriza@redhat.com> - 0-0.4.copr
- Update to latest commit

* Fri Dec 05 2014 Martin Briza <mbriza@redhat.com> - 0-0.3.copr
- Update to latest commit

* Mon Sep 15 2014 Martin Briza <mbriza@redhat.com> - 0-0.2.copr
- Update to latest commit

* Mon Sep 15 2014 Martin Briza <mbriza@redhat.com> - 0-0.1.copr
- Initial build
