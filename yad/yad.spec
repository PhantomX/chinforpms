Name:           yad
Version:        7.3
Release:        1%{?dist}
Summary:        Display graphical dialogs from shell scripts or command line

License:        GPLv3+
URL:            https://github.com/v1cont/%{name}

Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  perl(XML::Parser)
BuildRequires:  intltool >= 0.40.0
BuildRequires:  pkgconfig(gspell-1)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtksourceview-3.0)
BuildRequires:  pkgconfig(webkit2gtk-4.0)
Requires:       hicolor-icon-theme
Requires:       rgb


%description
Yad (yet another dialog) is a fork of zenity with many improvements, such as
custom buttons, additional dialogs, pop-up menu in notification icon and more.

%prep
%autosetup -p1

%build
%configure \
  --enable-icon-browser \
  --enable-html \
  --enable-spell \
  --enable-sourceview \
  --with-rgb=%{_datadir}/X11/rgb.txt \
  --disable-schemas-compile \
%{nil}

%make_build

%install
%make_install

%find_lang %{name}

# Encoding key in group "Desktop Entry" is deprecated.
# Place the menu entry for yad-icon-browser under "Utilities".
desktop-file-edit \
  --remove-key Encoding \
  --remove-category Development \
  --add-category Utility \
  %{buildroot}%{_datadir}/applications/%{name}-icon-browser.desktop


%files -f %{name}.lang
%doc README.md AUTHORS COPYING NEWS THANKS TODO
%{_bindir}/pfd
%{_bindir}/%{name}
%{_bindir}/%{name}-icon-browser
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}-icon-browser.desktop
%{_datadir}/aclocal/%{name}.m4
%{_datadir}/glib-2.0/schemas/%{name}.gschema.xml
%{_mandir}/man1/*.1.*


%changelog
* Thu Oct 22 2020 Phantom X <megaphantomx at hotmail dot com> - 7.3-1
- 7.3
- New project URL

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 19 2017 Oliver Haessler <oliver@redhat.com> - 0.40.0-2
- added BuildRequires: webkitgtk43-devel for Fedora <=26 and EPEL (#1455282)

* Sun Nov 19 2017 Oliver Haessler <oliver@redhat.com> - 0.40.0-1
- Update to 0.40.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 27 2017 Oliver Haessler <oliver@redhat.com> - 0.39.0-1
- Update to 0.39.0

* Sat Apr 08 2017 Oliver Haessler <oliver@redhat.com> - 0.38.2-3
- increment number, as bodhi has issues with the previous version,
so fixing it by updating the minor version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Oliver Haessler <oliver@redhat.com> - 0.38.2-1
- Update to 0.38.2

* Mon Jan 09 2017 Oliver Haessler <oliver@redhat.com> - 0.38.1-1
- Update to 0.38.1

* Sun Dec 11 2016 Oliver Haessler <oliver@redhat.com> - 0.38.0-1
- Update to 0.38.0

* Tue Aug 23 2016 Oliver Haessler <oliver@redhat.com> - 0.37.0-1
- Update to 0.37.0

* Wed May 18 2016 Oliver Haessler <oliver@redhat.com> - 0.36.3-1
- Update to 0.36.3

* Sun May 01 2016 Oliver Haessler <oliver@redhat.com> - 0.36.2-1
- Update to 0.36.2

* Fri Apr 29 2016 Oliver Haessler <oliver@redhat.com> - 0.36.1-1
- Update to 0.36.1

* Tue Mar 22 2016 Oliver Haessler <oliver@redhat.com> - 0.35.0-1
- Update to 0.35.0

* Mon Feb 29 2016 Oliver Haessler <oliver@redhat.com> - 0.34.2-1
- Update to 0.34.2

* Thu Feb 25 2016 Oliver Haessler <oliver@redhat.com> - 0.34.1-1
- Update to 0.34.1

* Mon Feb 22 2016 Oliver Haessler <oliver@redhat.com> - 0.34.0-1
- Update to 0.34.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Oliver Haessler <oliver@redhat.com> - 0.33.1-1
- Update to 0.33.1

* Fri Jan 08 2016 Oliver Haessler <oliver@redhat.com> - 0.33.0-1
- Update to 0.33.0

* Thu Nov 19 2015 Oliver Haessler <oliver@redhat.com> - 0.32.0-1
- Update to 0.32.0

* Thu Nov 05 2015 Oliver Haessler <oliver@redhat.com> - 0.31.3-1
- Update to 0.31.3

* Mon Oct 12 2015 Elder Marco <eldermarco@fedoraproject.org> - 0.31.2-1
- Update to 0.31.2

* Wed Sep 09 2015 Elder Marco <eldermarco@fedoraproject.org> - 0.30.0-1
- Update to 0.30.0

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 15 2015 Elder Marco <eldermarco@fedoraproject.org> - 0.28.1-1
- update to new version, 0.28.1.
- Build yad with HTML widget enabled
- Removed patch to fix-missing-buttons.patch
- Added patch to fix undefined reference to strip_new_line

* Wed Aug 27 2014 Elder Marco <eldermarco@fedoraproject.org> - 0.27.0-1
- New upstream version
- New branches: el5, el6 and epel7

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 21 2014 Elder Marco <eldermarco@fedoraproject.org> - 0.26.1-2
- Patch to fix missing buttons (BZ #1111285)

* Tue Jun 10 2014 Elder Marco <eldermarco@fedoraproject.org> - 0.26.1-1
- Update to 0.26.1
- Project moved to SourceForge due to google politics about file hosting
- New address: https://sourceforge.net/projects/yad-dialog/

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 06 2013 Elder Marco <eldermarco@fedoraproject.org> - 0.25.1-1
- Update to 0.25.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Elder Marco <eldermarco@fedoraproject.org> - 0.22.1-1
- Update to 0.22.1

* Sun Jun 09 2013 Elder Marco <eldermarco@fedoraproject.org> - 0.21.0-1
- Update to 0.21.0

* Sat Apr 06 2013 Elder Marco <eldermarco@fedoraproject.org> - 0.20.3-1
- Update to 0.20.3
- Added perl(XML::Parser) as BR

* Sun Mar 24 2013 Elder Marco <eldermarco@fedoraproject.org> - 0.20.1-1
- Update to 0.20.1

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Elder Marco <eldermarco@fedoraproject.org> - 0.19.1-1
- Update to 0.19.1

* Wed Dec 26 2012 Elder Marco <eldermarco@fedoraproject.org> - 0.19.0-1
- Update to 0.19.0

* Sun Dec 09 2012 Elder Marco <eldermarco@fedoraproject.org> - 0.18.0-1
* Update to 0.18.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Elder Marco <eldermarco@fedoraproject.org> - 0.17.1.1-1
- Update to 0.17.1.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.16.3-1
- Update to new version

* Tue Nov 15 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.15.2-1
- Update to new version
- Removed condition %%if 0%%{?fedora} < 15.

* Sun Nov 06 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.15.1-1
- Update to new version

* Sun Oct 16 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.15.0-1
- Update to new version

* Thu Sep 08 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.14.2-1
- Update to new version

* Sat Aug 13 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.13.0-1
- New upstream release

* Fri Jul 08 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.12.4-2
- Menu entry for yad-icon-browser placed under "Utilities"

* Fri Jul 01 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.12.4-1
- Update to 0.12.4
- Removed patch to fix FSF address (now, it's not necessary)

* Tue Jun 28 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.12.3-3
- Added patch to fix FSF address (from upstream)

* Sun Jun 26 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.12.3-2
- Edited spec file to conform to the fedora guidelines

* Sat Jun 25 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.12.3-1
- New upstream release

* Sat May 21 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.11.0-1
- New upstream release

* Sun May 01 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.10.2-1
- New upstream release

* Tue Apr 12 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.10.1-1
- New upstream release

* Wed Mar 30 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.10.0-1
- New upstream release
- Added build option --disable-deprecated

* Sun Mar 13 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.9.1-1
- New upstream release
- Added desktop-file-utils as BuildRequires.
- Removed clean section and BuildRoot tag (not required any more).
- Removed Encoding key from .desktop file.

* Tue Mar 08 2011 Elder Marco <eldermarco@fedoraproject.org> - 0.9.0-1
- Initial package
