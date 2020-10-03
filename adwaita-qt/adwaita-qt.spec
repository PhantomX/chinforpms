%global commit ab902e8a4967e592676229e602d21e7be7950b28
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200925
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           adwaita-qt
Version:        1.1.90
Release:        100%{?gver}%{?dist}

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
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5X11Extras)


%description
Theme to let Qt applications fit nicely into Fedora Workstation


%package -n adwaita-qt5
Summary:        Adwaita Qt5 theme

%description -n adwaita-qt5
Adwaita theme variant for applications utilizing Qt5


%package libs
Summary:        Adwaita Qt common libraries
Obsoletes:      adwaita-qt4 < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-common < %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
Adwaita Qt common libraries.


%package libs-devel
Summary:        Development files for libvkd3d-utils
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libs-devel
Development files for %{name}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif


%build

%{cmake} \
%{nil}

%cmake_build


%install
%cmake_install


%files -n adwaita-qt5
%license LICENSE.LGPL2
%doc README.md
%{_qt5_plugindir}/styles/adwaita.so


%files libs
%license LICENSE.LGPL2
%doc README.md
%{_libdir}/libadwaitaqt.so.*
%{_libdir}/libadwaitaqtpriv.so.*


%files libs-devel
%license LICENSE.LGPL2
%{_includedir}/AdwaitaQt/*.h
%{_libdir}/libadwaitaqt.so
%{_libdir}/libadwaitaqtpriv.so
%{_libdir}/cmake/AdwaitaQt/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1.90-100.20200925gitab902e8
- 1.1.90
- libs package
- No more qt4 support

* Fri Jun 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:1.1.4-100
- 1.1.4

* Mon Jun 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1.2-101
- Rebuild (qt5)

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1.2-100
- 1.1.2
- Update patch

* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:1.1.1-100.20191211gitd1e7619
- 1.1.1

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
