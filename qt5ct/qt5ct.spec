Name:           qt5ct
Version:        0.36
Release:        100%{?dist}
Summary:        Qt5 Configuration Tool

License:        BSD
URL:            https://sourceforge.net/projects/%{name}/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libXrender-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qttools-devel
# qt5ct-qtplugin uses gui-private
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

## FIXME?: ftbfs without this, not sure why yet -- rex
BuildRequires: pkgconfig(libudev)

%description
qt5ct allows users to configure Qt5 settings (theme, font, icons, etc.) under
DE/WM without Qt integration.

%prep
%autosetup


%build
%{qmake_qt5}
%make_build


%install
make install INSTALL_ROOT=%{buildroot}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Copy translations into right place
install -d %{buildroot}%{_datadir}/%{name}/translations
install -D -pm 644 src/%{name}/translations/*.qm %{buildroot}%{_datadir}/%{name}/translations/
%find_lang %{name} --with-qt


%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/*
%dir %{_datadir}/%{name}/translations/
%{_qt5_plugindir}/platformthemes/libqt5ct.so
%{_qt5_plugindir}/styles/libqt5ct-style.so


%changelog
* Mon Dec 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.36-100
- 0.36

* Wed Dec 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.35-6
- rebuild (qt5)

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 0.35-5
- rebuild (qt5)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.35-3
- rebuild (qt5)

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.35-2
- rebuild (qt5)

* Wed Apr 18 2018 Christian Dersch - 0.35-1
- new version

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 0.34-5
- rebuild (qt5)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Jan Grulich <jgrulich@redhat.com> - 0.34-3
- rebuild (qt5)

* Mon Nov 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.34-1
- qt5ct-0.34 is available (#1509757)

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.33-2
- rebuild (qt5)

* Mon Aug 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.33-1
- qt5ct-0.33 (#1450654)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.31-3
- rebuild (qt5)

* Sun May 07 2017 Christian Dersch <lupinix@mailbox.org> - 0.31-2
- Rebuilt for Qt 5.9 beta

* Mon Apr 10 2017 Christian Dersch <lupinix@mailbox.org> - 0.31-1
- new version

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.30-2
- rebuild (qt5)

* Thu Feb 09 2017 Christian Dersch <lupinix@mailbox.org> - 0.30-1
- new version

* Wed Jan 25 2017 Christian Dersch <lupinix@mailbox.org> - 0.29-1
- new version

* Thu Nov 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.27-2
- bump release

* Thu Nov 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.27-1.2
- branch rebuild (qt5)

* Tue Oct 04 2016 Christian Dersch <lupinix@mailbox.org> - 0.27-1
- new version

* Tue Sep 06 2016 Christian Dersch <lupinix@mailbox.org> - 0.26-1
- new version

* Thu Aug 11 2016 Christian Dersch <lupinix@mailbox.org> - 0.25-1
- new version

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.24-3
- rebuild (qt5-qtbase)

* Wed Jun 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.24-2
- add versioned dependency on qtbase version used to build

* Thu Jun 02 2016 Christian Dersch <lupinix@mailbox.org> - 0.24-1
- new version

* Mon May 02 2016 Christian Dersch <lupinix@mailbox.org> - 0.23-1
- new version (0.23)

* Tue Mar 29 2016 Christian Dersch <lupinix@mailbox.org> - 0.22-1
- initial spec
