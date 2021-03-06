%global real_name gnome-colors

Name:           gnome-colors-icon-theme
Summary:        GNOME-Colors icon theme
Version:        5.5.1
Release:        102.chinfo%{?dist}

License:        GPLv2
Url:            https://github.com/gnome-colors/gnome-colors
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/%{real_name}/%{real_name}-src-%{version}.tar.gz

Patch1:         %{name}-nostdin.patch

BuildArch:      noarch

Requires:       gnome-icon-theme
BuildRequires:  icon-naming-utils >= 0.8.7
BuildRequires:  inkscape
BuildRequires:  ImageMagick

%description
The GNOME-Colors is a project that aims to make the GNOME desktop as 
elegant, consistent and colorful as possible.

The current goal is to allow full color customization of themes, icons, 
GDM logins and splash screens. There are already seven full color-schemes 
available; Brave (Blue), Human (Orange), Wine (Red), Noble (Purple), Wise 
(Green), Dust (Chocolate) and Illustrious (Pink). An unlimited amount of 
color variations can be rebuilt and recolored from source, so users need 
not stick to the officially supported color palettes.

GNOME-Colors is mostly inspired/based on Tango, GNOME, Elementary, 
Tango-Generator and many other open-source projects. More information 
can be found in the AUTHORS file.

%prep
%setup -q -c %{real_name}--icon-theme-%{version}
%patch1

# link the start-here icon to the Fedora icon
for dir in gnome-colors-common/*/places; do
  cd $dir
  ln -sf ../apps/fedora-logo-icon.* start-here.*
  cd -
done
# change name from GNOME -> GNOME-Colors
rename 'gnome' '%{real_name}' themes/*
sed -i -e 's/GNOME/GNOME-Colors/' themes/*

%build
%make_build

%install
%make_install

find %{buildroot}%{_datadir}/icons -name '*.xpm' -delete

%files
%license COPYING
%doc AUTHORS README ChangeLog
%{_datadir}/icons/gnome-colors-common/
%{_datadir}/icons/gnome-colors-brave/
%{_datadir}/icons/gnome-colors-carbonite/
%{_datadir}/icons/gnome-colors-dust/
%{_datadir}/icons/gnome-colors-human/
%{_datadir}/icons/gnome-colors-illustrious/
%{_datadir}/icons/gnome-colors-noble/
%{_datadir}/icons/gnome-colors-tribute/
%{_datadir}/icons/gnome-colors-wine/
%{_datadir}/icons/gnome-colors-wise/

%changelog
* Mon Mar 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.5.1-102.chinfo
- Remove obsolete scriptlets

* Tue Oct 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.5.1-101.chinfo
- Fix new inkscape crash with stdin

* Thu Feb 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.5.1-100.chinfo
- Update url and source link
- Remove xpm files
- Use %%{make_build}
- Fix post scripts
- Use %%license

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Miro Hrončok <mhroncok@redhat.com> - 5.5.1-6
- Use %%global instead of %%define
- Use %%{make_install}
- Use icon cache scriplets from wiki

* Sun Sep 01 2013 Miro Hrončok <mhroncok@redhat.com> - 5.5.1-5
- Link the start-here icon to the Fedora icon

* Fri Aug 30 2013 Miro Hrončok <mhroncok@redhat.com> - 5.5.1-4
- Removed BuildRoot definition and Group
- Removed %%clean section
- Removed rm -rf from %%install
- Removed %%defattr from %%files

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 18 2009 Michal Nowak <mnowak@redhat.com> - 5.5.1-1
- 5.5.1

* Tue Aug  4 2009 Michal Nowak <mnowak@redhat.com> - 5.3-1
- 5.3
- Requires: gnome-icon-theme

* Mon Aug  3 2009 Michal Nowak <mnowak@redhat.com> - 5.2.2-1
- initial packaging

