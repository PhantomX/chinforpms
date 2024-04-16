%global src_hash cb7633a7e0f92f70adc7e2b89f1e3578

Summary:        Bluecurve xmms skin
Name:           bluecurve-xmms-skin
Version:        1.0.0
Release:        26%{?dist}

BuildArch:      noarch

License:        GPL-1.0-or-later
URL:            http://www.redhat.com

Source0:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}.tar.bz2/%{src_hash}/%{name}-%{version}.tar.bz2

BuildRequires:  zip
BuildRequires:  make
Requires:       audacious


%description
This package contains a skin for the Audacious music player that matches Bluecurve.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

mv %{buildroot}%{_datadir}/xmms %{buildroot}%{_datadir}/audacious

# These are empty
rm -f ChangeLog NEWS README

# The upstream packages may gain po files at some point in the near future
# %find_lang %{name} || touch %{name}.lang


%files
%doc AUTHORS COPYING
%{_datadir}/audacious/Skins/Bluecurve-xmms.zip

%changelog
* Mon Apr 15 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-26
- Rebase for Audacious

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 06 2016 Filipe Rosset <rosset.filipe@gmail.com> - 1.0.0-13
- Fix FTBFS in rawhide rhbz #1307356 plus spec cleanup

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr  5 2009 Matthias Clasen  <mclasen@redhat.com> - 1.0.0-3
- Drop xmms dependency (#365821)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 25 2007 Ray Strode <rstrode@redhat.com> - 1.0.0-1
- Initial import, version 1.0.0
