Name:           devilspie2
Version:        0.44
Release:        1%{?dist}
Summary:        A window-matching utility

License:        GPL-3.0-or-later
URL:            http://www.nongnu.org/devilspie2/
Source0:        http://download.savannah.nongnu.org/releases/%{name}/%{name}_%{version}-src.tar.xz

BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  gettext
BuildRequires:  gcc
BuildRequires:  make

%description
Devilspie2 is a window matching utility, allowing the user to perform scripted
actions on windows as they are created. For example you can script a terminal
program to always be positioned at a specific screen position, or position a
window on a specific workspace. It is based on the program Devilspie by Ross
Burton.

%prep
%autosetup -p1

# preserve timestamps
sed -i 's/^\tinstall\s\+/\0-p /' Makefile

%build
%make_build INSTALL_PREFIX=%{_prefix}

%install
%make_install INSTALL_PREFIX=%{_prefix}

%find_lang %{name}

%files -f %{name}.lang
%doc README README.translators ChangeLog COPYING AUTHORS GPL3.txt
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Mon Apr 15 2024 Phantom X <megaphantomx at hotmail dot com> - 0.44-1
- 0.44 chinforpms release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 09 2020 Michal Minář <miminar@redhat.com> - 0.43-8
- Fixed build error due to deprecated LUA_QL macro
- Resolves bz#1863421

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Michal Minář <miminar@redhat.com> - 0.43-3
- Added gcc as a BR.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 16 2018 Michal Minář <miminar@redhat.com> - 0.43-1
- New upstream version.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 23 2017 Michal Minar <miminar@redhat.com> 0.42-1
- New upstream version.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 21 2016 Michal Minar <miminar@redhat.com> 0.41-1
- New upstream version.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 07 2015 Michal Minar <miminar@redhat.com> 0.39-1
- New upstream version.

* Sat Dec 20 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.38-3
- Build with $RPM_OPT_FLAGS

* Thu Dec 18 2014 Michal Minar <miminar@redhat.com> 0.38-2
- Fix license field and ship license file.
- Using pkgconfig for build dependencies.

* Tue Nov 18 2014 Michal Minar <miminar@redhat.com> 0.38-1
- Initial release.

