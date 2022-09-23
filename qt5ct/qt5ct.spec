Name:           qt5ct
Version:        1.5
Release:        104%{?dist}
Summary:        Qt5 Configuration Tool

License:        BSD
URL:            https://sourceforge.net/projects/%{name}/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        README.gtk3
Source2:        60-%{name}.sh

Patch0:         %{name}-gtk3-dialogs.patch

BuildRequires:  make
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
%setup -q -c

cp -a %{name}-%{version} %{name}-%{version}-gtk3

pushd %{name}-%{version}-gtk3
cp -a COPYING AUTHORS ChangeLog README ../

%patch0 -p1 -b.gtk3
popd

cp -p %{S:1} .
cp -p %{S:2} .

%build
pushd %{name}-%{version}
%{qmake_qt5}

%make_build
popd

pushd %{name}-%{version}-gtk3
%{qmake_qt5}

%make_build sub-src-qt5ct-all
popd

%install
make install -C %{name}-%{version}-gtk3/src/qt5ct INSTALL_ROOT=%{buildroot}
mv %{buildroot}%{_bindir}/%{name}{,-gtk3}

make install -C %{name}-%{version} INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d
install -pm0755 60-%{name}.sh \
  %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/60-%{name}.sh

sed -e '/^Name/s|$| - GTK3|g' %{buildroot}/%{_datadir}/applications/%{name}.desktop \
  > %{buildroot}/%{_datadir}/applications/%{name}-gtk3.desktop

desktop-file-edit \
  --set-key="Exec" \
  --set-value="%{name}-gtk3" \
  %{buildroot}/%{_datadir}/applications/%{name}-gtk3.desktop

# Copy translations into right place
install -d %{buildroot}%{_datadir}/%{name}/translations
install -D -pm 644 %{name}-%{version}/src/%{name}/translations/*.qm \
  %{buildroot}%{_datadir}/%{name}/translations/
%find_lang %{name} --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog README README.gtk3
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}*.desktop
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/colors/
%{_datadir}/%{name}/qss/
%{_qt5_plugindir}/platformthemes/libqt5ct.so
%{_qt5_plugindir}/styles/libqt5ct-style.so
%{_sysconfdir}/X11/xinit/xinitrc.d/60-%{name}.sh


%changelog
* Fri Sep 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1.5-104
- Rebuild (qt5)

* Wed Jul 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1.5-103
- Rebuild (qt5)

* Sun Jan 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1.5-102
- Update xinitrc.d

* Tue Jan 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1.5-101
- Add xinitrc.d script

* Wed Oct 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5-100
- 1.5

* Sun Sep 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1.3-100
- 1.3

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2-100
- 1.2

* Sat Dec 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1-101
- Rebuild (qt5)

* Thu Aug 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1-100
- 1.1, internal icon loading proper fix

* Tue Jul 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1.0-101
- Patch to fix icon themes with applications with internal iconsets

* Wed Jun 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0-100
- 1.0

* Sun Dec 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.41-102
- Rebuild (qt5)

* Thu Oct 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.41-101
- Rebuild (qt5)

* Thu Sep 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.41-100
- 0.41

* Wed Jul 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.39-101
- Rebuild (qt5)

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.39-100
- 0.39

* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.38-101
- Apply some upstream patches

* Fri Apr 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.38-100
- 0.38

* Tue Jan 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.37-103
- Rebuild (qt5)

* Fri Dec 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.37-102
- Install a -gtk3 binary, to set style with GTK3 dialogs and prevent some crashes

* Thu Dec 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.37-101
- Set GTK dialog options to use GTK3 dialogs instead GTK2

* Wed Dec 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.37-100
- 0.37

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
