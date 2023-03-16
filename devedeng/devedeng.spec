Name:           devedeng
Version:        4.17.0
Release:        100%{?dist}
Summary:        A program to create video DVDs and CDs (VCD, sVCD or CVD)

Epoch:          1

License:        GPL-3.0-only
URL:            http://www.rastersoft.com/programas/devede.html
Source0:        https://gitlab.com/rastersoft/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Provides:       devede = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      devede < 4.0

BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       (mplayer or mpv or vlc)
Requires:       ffmpeg
Requires:       dvdauthor
Requires:       vcdimager
Requires:       genisoimage
Requires:       (xfburn or k3b or brasero)
Requires:       ImageMagick
Requires:       python3-urllib3
Requires:       python3-gobject
Requires:       python3-cairo
Requires:       python3-dbus
Requires:       dejavu-sans-fonts
Requires:       hicolor-icon-theme


%description
DevedeNG is a program to create video DVDs and CDs (VCD, sVCD or CVD), 
suitable for home players, from any number of video files, in any of the 
formats supported by FFMpeg.

The suffix NG is because it is a rewrite from scratch of the old Devede, to 
work with Python3 and Gtk3, and with a new internal architecture that allows 
to expand it and easily add new features.


%prep
%autosetup -n %{name}-%{version}

sed -e "s|copy_files_verbose|%{name}_\0|g" \
  -i setup.py src/copy_files_verbose.py src/%{name}/file_copy.py
mv src/copy_files_verbose.py src/%{name}_copy_files_verbose.py

sed -e "/locale/s|'/usr', ||g" -i setup.py

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files %{name}


# Fix desktop file
desktop-file-edit \
  --add-category X-OutputGeneration \
  --set-icon %{name}_icon \
  %{buildroot}%{_datadir}/applications/devede_ng.py.desktop

# Remove icon
rm -f %{buildroot}%{_datadir}/pixmaps/%{name}.svg

# Add docs
mv %{buildroot}%{_pkgdocdir} _docs/

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name}


%files -f %{pyproject_files} -f %{name}.lang
%doc _docs/* HISTORY.md README.md
%license COPYING
%{_bindir}/devede_ng.py
%{_bindir}/%{name}_copy_files_verbose.py
%{_datadir}/%{name}
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/applications/devede_ng.py.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%exclude %{_mandir}/man1/devede.1*


%changelog
* Thu Mar 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:4.17.0-100
- 4.17.0
- Update to best packaging practices

* Tue Oct 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16.0-100
- 4.16.0

* Mon Jul 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.15.0-100
- 4.15.0

* Mon May 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14.0-100
- Boolean requires

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Feb 08 2019 Andrea Musuruane <musuruan@gmail.com> - 4.14.0-1
- Updated to new upstream release

* Fri Feb 01 2019 Andrea Musuruane <musuruan@gmail.com> - 4.13.0-1
- Updated to new upstream release

* Sun Sep 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.12.0-4
- Require genisoimage as mkisofs virtual provides was removed

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Miro Hrončok <mhroncok@redhat.com> - 4.12.0-2
- Rebuilt for Python 3.7

* Sat Jun 30 2018 Andrea Musuruane <musuruan@gmail.com> - 4.12.0-1
- Updated to new upstream release
- Upstream git repository moved to gitlab

* Thu May 17 2018 Andrea Musuruane <musuruan@gmail.com> - 4.11.0-2
- Fixed AppData file

* Thu May 03 2018 Andrea Musuruane <musuruan@gmail.com> - 4.11.0-1
- Updated to new upstream release

* Mon Apr 30 2018 Andrea Musuruane <musuruan@gmail.com> - 4.10.0-1
- Updated to new upstream release

* Wed Apr 18 2018 Andrea Musuruane <musuruan@gmail.com> - 4.9.0-1
- Updated to new upstream release

* Thu Jan 25 2018 Andrea Musuruane <musuruan@gmail.com> 4.8.12-1
- Updated to new upstream release
- Removed obsolete scriptlets

* Tue Dec 26 2017 Andrea Musuruane <musuruan@gmail.com> 4.8.11-1
- Updated to new upstream release

* Sat Dec 02 2017 Andrea Musuruane <musuruan@gmail.com> 4.8.10-1
- Updated to new upstream release
- Added AppData file
- Preserved timestamps

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 4.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Andrea Musuruane <musuruan@gmail.com> 4.8.9-1
- Updated to new upstream release

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 4.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 08 2017 Andrea Musuruane <musuruan@gmail.com> 4.8.8-1
- Updated to new upstream release

* Thu Feb 02 2017 Andrea Musuruane <musuruan@gmail.com> 4.8.7-1
- Updated to new upstream release

* Sat Dec 17 2016 Andrea Musuruane <musuruan@gmail.com> 4.8.6-1
- Updated to new upstream release

* Sat Nov 26 2016 Andrea Musuruane <musuruan@gmail.com> 4.8.5-1
- Updated to new upstream release

* Sat Nov 05 2016 Andrea Musuruane <musuruan@gmail.com> 4.8.4-1
- Updated to new upstream release

* Sat Oct 29 2016 Andrea Musuruane <musuruan@gmail.com> 4.8.3-1
- Updated to new upstream release

* Sun Sep 25 2016 Andrea Musuruane <musuruan@gmail.com> 4.8.2-1
- Updated to new upstream release

* Tue Sep 06 2016 Andrea Musuruane <musuruan@gmail.com> 4.8.1-1
- Updated to new upstream release

* Sun Aug 14 2016 Andrea Musuruane <musuruan@gmail.com> 4.8.0-1
- Updated to new upstream release

* Thu Aug 04 2016 Andrea Musuruane <musuruan@gmail.com> 4.7.1-1
- Updated to new upstream release

* Mon Apr 25 2016 Andrea Musuruane <musuruan@gmail.com> 4.7.0-1
- Updated to new upstream release

* Thu Mar 17 2016 Andrea Musuruane <musuruan@gmail.com> 4.6.1-1
- First release 

