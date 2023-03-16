%global pkgname tap-plugins
%global vc_url https://github.com/tomszilagyi/%{pkgname}

Name:           ladspa-%{pkgname}
Version:        1.0.1
Release:        101%{?dist}
Summary:        Tom's Audio Processing plugin

License:        GPL-2.0-or-later
URL:            https://tomscii.sig7.se/%{pkgname}/

Source0:        %{vc_url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  ladspa-devel
BuildRequires:  make
Requires:       ladspa
Obsoletes:      tap-plugins <= 0.7.0-1
Provides:       tap-plugins = %{version}-%{release}

%description
TAP-plugins is short for Tom's Audio Processing plugins. It is a bunch
of LADSPA plugins for digital audio processing, intended for use in a
professional DAW environment such as Ardour.


%prep
%autosetup -n %{pkgname}-%{version} -p1

# use the system version of ladspa.h
rm -f ladspa.h

sed \
  -e '/^CFLAGS  =/s|CFLAGS  = -I. -O3 -Wall -fomit-frame-pointer -funroll-loops|CFLAGS +=|g' \
  -e 's|^LDFLAGS = |LDFLAGS +=|g' \
  -i Makefile


%build
%set_build_flags
%make_build


%install
mkdir -p %{buildroot}%{_libdir}/ladspa
%make_install \
  INSTALL_PLUGINS_DIR=%{buildroot}%{_libdir}/ladspa/ \
  INSTALL_LRDF_DIR=%{buildroot}%{_datadir}/ladspa/rdf/


%files
%doc CREDITS README
%license COPYING
%{_libdir}/ladspa/*.so
%{_datadir}/ladspa/rdf/*


%changelog
* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.0.1-101
- Fix for package_note_file

* Tue Dec 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.1-100
- 1.0.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.7.0-21
- Use Fedora link flags
- Add BR: gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.0-5
- Autorebuild for GCC 4.3

* Thu Oct  4 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.0-4
- Use system version of ladspa.h

* Wed Oct  3 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7.0-3
- Various specfile improvements to match the Fedora Packaging Guidelines
- Submit for review for Fedora inclusion

* Mon Apr 16 2007 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.7.0-2
- change name from tap-plugins to ladspa-tap-plugins, build on fc6

* Mon Dec 20 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- spec file cleanup

* Fri Dec  3 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- added proper compilation flags, leave original optimization alone

* Wed Aug 18 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.7.0-1
- updated to 0.7.0

* Sun Jul  4 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.6.0-1
- updated to 0.6.0
- documentation is now on a separate package

* Thu May 13 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.5.0-1
- updated to 0.5.0, added documentation files

* Wed Mar  3 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.4.2-1
- updated to 0.4.2

* Wed Feb 18 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.4.0-1
- do not depend on ladspa package explicitly

* Wed Feb  4 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.3.0-1
- updated to 0.3.0

* Thu Jan 29 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.0-1
- initial build
