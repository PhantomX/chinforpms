%global sover 2.2

Name:           kddockwidgets
Version:        2.2.4
Release:        100%{?dist}
Summary:        Qt dock widget library

License:        GPL-3.0-only AND GPL-2.0-only AND BSD-3-Clause
URL:            https://github.com/KDAB/KDDockWidgets
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  cmake(Qt5QuickControls2)
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6QuickControls2)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  libxkbcommon-devel

%{?_qt5:Requires:       %{_qt5}%{?_isa} = %{_qt5_version}}

%description
Qt dock widget library written by KDAB, suitable for replacing QDockWidget
and implementing advanced functionalities missing in Qt.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        qt6
Summary:        Qt dock widget library for Qt 6

%{?_qt6:Requires:       %{_qt6}%{?_isa} = %{_qt6_version}}

%description    qt6
%{description}

%package        qt6-devel
Summary:        Development files for %{name}-qt6

Requires:       %{name}-qt6%{?_isa} = %{version}-%{release}
%description    qt6-devel
The %{name}-qt6-devel package contains libraries and header files for
developing applications that use %{name}-qt6.


%prep
%autosetup -n KDDockWidgets-%{version}


%build
%global _vpath_builddir %{_target_platform}-qt5
%cmake \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=Release
%cmake_build

%global _vpath_builddir %{_target_platform}-qt6
%cmake \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DKDDockWidgets_QT6=ON
%cmake_build

%install
%global _vpath_builddir %{_target_platform}-qt5
%cmake_install
rm -rf %{buildroot}%{_datadir}/doc

%global _vpath_builddir %{_target_platform}-qt6
%cmake_install
rm -rf %{buildroot}%{_datadir}/doc/KDDockWidgets-qt6

%files
%license LICENSES/* LICENSE.txt
%doc CONTRIBUTORS.txt Changelog README.md
%{_libdir}/libkddockwidgets.so.%{sover}*

%files devel
%{_includedir}/kddockwidgets
%{_libdir}/cmake/KDDockWidgets
%{_libdir}/libkddockwidgets.so
%{_libdir}/qt5/mkspecs/modules/qt_KDDockWidgets.pri

%files qt6
%license LICENSES/* LICENSE.txt
%doc CONTRIBUTORS.txt Changelog README.md
%{_libdir}/libkddockwidgets-qt6.so.%{sover}*

%files qt6-devel
%{_includedir}/kddockwidgets-qt6
%{_libdir}/cmake/KDDockWidgets-qt6
%{_libdir}/libkddockwidgets-qt6.so
%{_libdir}/qt6/mkspecs/modules/qt_KDDockWidgets.pri

%changelog
* Sat May 10 2025 Phantom X <megaphantomx at hotmail dot com> - 2.2.4-100
- 2.2.4

* Fri Apr 18 2025 Phantom X <megaphantomx at hotmail dot com> - 2.2.3-101
- Rebuild (qt6)

* Sun Apr 06 2025 Phantom X <megaphantomx at hotmail dot com> - 2.2.3-100
- 2.2.3

* Thu Mar 20 2025 Phantom X <megaphantomx at hotmail dot com> - 2.2.1-100
- 2.2.1

* Mon Feb 03 2025 Jan Grulich <jgrulich@redhat.com> - 1.7.0-19
- Rebuild (qt6)

* Wed Jan 22 2025 Jan Grulich <jgrulich@redhat.com> - 1.7.0-18
- Rebuild (qt5)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Jan Grulich <jgrulich@redhat.com> - 1.7.0-16
- Rebuild (qt5)

* Wed Dec 11 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-15
- Rebuild (qt6)

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-14
- Rebuild (qt6)

* Thu Sep 05 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-13
- Rebuild (qt5)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Vasiliy Glazov <vascom2@gmail.com> - 1.7.0-11
- Rebuild (qt6)

* Thu May 30 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-10
- Rebuild (qt5)

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-9
- Rebuild (qt6)

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-8
- Rebuild (qt6)

* Fri Mar 15 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-7
- Rebuild (qt5)

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-6
- Rebuild (qt6)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Jan Grulich <jgrulich@redhat.com> - 1.7.0-3
- Rebuild (qt5)

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 1.7.0-2
- Rebuild (qt6)

* Tue Oct 31 2023 Vasiliy Glazov <vascom2@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Fri Oct 13 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-13
- Rebuild (qt6)

* Mon Oct 09 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-12
- Rebuild (qt5)

* Thu Oct 05 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-11
- Rebuild (qt6)

* Mon Jul 24 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-10
- Rebuild (qt6)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-8
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-7
- Rebuild for qtbase private API version change

* Wed Jun 14 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-6
- Rebuild (qt5)

* Fri May 26 2023 Jan Grulich <jgrulich@redhat.com> - 1.6.0-5
- Rebuild (qt6)

* Fri Apr 14 2023 Vasiliy Glazov <vascom2@gmail.com> - 1.6.0-3
- Rebuild for new Qt 5 version

* Tue Apr 11 2023 Vasiliy Glazov <vascom2@gmail.com> - 1.6.0-3
- Add Qt6 version

* Tue Mar 28 2023 Vasiliy Glazov <vascom2@gmail.com> - 1.6.0-2
- Pin Qt5 version

* Fri Mar 24 2023 Vasiliy Glazov <vascom2@gmail.com> - 1.6.0-1
- Initial packaging.
