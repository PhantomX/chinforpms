%global commit c298bfb809d0f773e9226a68d438f19bfe752293
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190322
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url https://github.com/pixelb/%{name}

Name:           fslint
Version:        2.47
Release:        1%{?gver}%{?dist}
Summary:        File System "lint" discovery and cleaning utility

License:        GPLv2+
URL:            http://www.pixelbeat.org/fslint/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://www.pixelbeat.org/fslint/%{name}-%{version}.tar.xz
%endif

BuildArch:      noarch
BuildRequires:  gettext >= 0.13
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Requires:       cpio
Requires:       findutils
Requires:       pygtk2 >= 2.4
Requires:       pygtk2-libglade
Requires:       python2.7 >= 2.3
Requires:       hicolor-icon-theme


%description
FSlint is a utility to find redundant disk usage like duplicate files
for example. It can be used to reclaim disk space and fix other problems
like file naming issues and bad symlinks etc.
It includes a GTK+ GUI as well as a command line interface.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

sed -i -e 's|^liblocation=.*$|liblocation="%{_datadir}/%{name}" #RPM edit|' %{name}-gui
sed -i -e 's|^locale_base=.*$|locale_base=None #RPM edit|' %{name}-gui


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}-gui %{buildroot}%{_bindir}/%{name}-gui

mkdir -p %{buildroot}%{_datadir}/%{name}/%{name}/{fstool,supprt}

install -pm0644 %{name}.glade %{name}_icon.png \
  %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{_datadir}/pixmaps
ln -s ../%{name}/%{name}_icon.png \
  %{buildroot}%{_datadir}/pixmaps/%{name}_icon.png

install -pm0755 %{name}/{find*,fslint,zipdir} \
  %{buildroot}%{_datadir}/%{name}/%{name}
install -pm0755 %{name}/fstool/* \
  %{buildroot}%{_datadir}/%{name}/%{name}/fstool

mkdir -p %{buildroot}%{_datadir}/%{name}/%{name}/supprt/rmlint/

install -pm0644 %{name}/supprt/fslver \
  %{buildroot}%{_datadir}/%{name}/%{name}/supprt
install -pm 755 %{name}/supprt/get* \
  %{buildroot}%{_datadir}/%{name}/%{name}/supprt
install -pm 755 %{name}/supprt/md5sum_approx \
  %{buildroot}%{_datadir}/%{name}/%{name}/supprt
install -pm 755 %{name}/supprt/rmlint/* \
  %{buildroot}%{_datadir}/%{name}/%{name}/supprt/rmlint

mkdir -p %{buildroot}%{_mandir}/man1
cp -a man/* \
  %{buildroot}%{_mandir}/man1/

make -C po DESTDIR=%{buildroot} LOCALEDIR=%{_datadir}/locale install

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --mode 644 \
  --remove-category=GTK \
  --remove-category=Utility \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
ln -s ../../../../%{name}/%{name}_icon.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}_icon.png

for res in 16 22 24 32 36 48 64 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{name}_icon.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}_icon.png
done


%find_lang %{name}



%files -f %{name}.lang
%doc doc/*
%{_mandir}/man1/%{name}*
%{_bindir}/%{name}-gui
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}_icon.png
%{_datadir}/pixmaps/%{name}_icon.png


%changelog
* Sun Oct 25 2020 Phantom X <megaphantomx at hotmail dot com> - 2.47-1.20190322gitc298bfb
- 2.47 snapshot

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.46-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 Pádraig Brady <P@draigBrady.com> - 2.46
- Latest upstream

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.2015.08.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.2015.08.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 22 2015 Moez Roy <moez.roy@gmail.com> - 2.45.2015.08.19
- Update to latest upstream which contain the following changes:
	* Fixes:
		* Selecting within and removal of GUI groups works again.
		  This regression was introduced in 2.44.
		* "Bad symlinks" functionality works in the GUI again.
		  This regression was introduced in 2.44.
		* Dangling symlinks are reported correctly for symlinks
		  whose names end in 2 digits.
		* Empty directories now only lists actual empty dirs
		  even if extra find parameters are specified.
		* Empty directories now ignore specified exluded paths, as
		  they can impact whether an "empty" directory can be removed.
	* Improvements:
		* findup now includes zero length files by default.  This can
		  be changed with -size +0c, or the new GUI min size option.
		* "Select from same folder" is no less CPU and RAM intensive.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 13 2014 Pádraig Brady <pbrady@redhat.com> - 2.44-1
- Latest upstream

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Jon Ciesla <limburgher@gmail.com> - 2.42-6
- Drop desktop vendor tag.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Pádraig Brady <P at draigBrady.com> - 2.42-1
- Update to 2.42

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Pádraig Brady <P at draigBrady.com> - 2.40-1
- Update to 2.40. Note this updates GTK+ and Python dependencies
  to 2.4 and 2.3 respectively (Fedora Core 2).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Pádraig Brady <P at draigBrady.com> - 2.28-3
- Remove redundant py[co] files (dependency on python(abi))

* Mon Nov 24 2008 Pádraig Brady <P at draigBrady.com> - 2.28-2
- Update summary as per Richard Hughes' request

* Tue Sep 09 2008 Pádraig Brady <P at draigBrady.com> - 2.28-1
- Update to 2.28

* Tue May 20 2008 Pádraig Brady <P at draigBrady.com> - 2.26-1
- Update to 2.26

* Wed Sep 19 2007 Pádraig Brady <P at draigBrady.com> - 2.24-1
- Update to 2.24

* Fri Aug 03 2007 Pádraig Brady <P at draigBrady.com> - 2.22-2
- clarify license

* Thu Jun 28 2007 Pádraig Brady <P at draigBrady.com> - 2.22-1
- Update to 2.22

* Fri Mar 09 2007 Pádraig Brady <P at draigBrady.com> - 2.20-1
- Update to 2.20
- Update description to make it easier to find
- Change symlink to fslint_icon.png from absolute to relative

* Fri Dec 29 2006 Pádraig Brady <P at draigBrady.com> - 2.18-1
- Update to 2.18

* Mon Oct 30 2006 Pádraig Brady <P at draigBrady.com> - 2.16-2
- Zero Epochs are superfluous nowadays and frowned upon in Fedora

* Mon Oct 30 2006 Pádraig Brady <P at draigBrady.com> - 0:2.16-1
- Update to 2.16 which has some minor packaging changes
  to align with the debian package (suggested by lintian) and also
- has man pages for fslint and fslint-gui.
  Other Packaging changes introduced in 2.14 were
- /usr/bin/{fs,FS}lint -> /usr/bin/fslint-gui
- Tidy up /usr/bin/fslint/fslint directory
- In addition to the above upstream changes I added
  the dist tag to the release version

* Tue Sep 19 2006 Pádraig Brady <P at draigBrady.com> - 2.11-3
- Rebuild for FC6 mass rebuild

* Fri Mar 18 2005 Pádraig Brady <P at draigBrady.com> - 2.11-2
- Update to 2.11

* Wed Mar 16 2005 Pádraig Brady <P at draigBrady.com> - 0:2.10-0.fdr.2
- Update to 2.10

* Thu Sep  9 2004 Pádraig Brady <P at draigBrady.com> - 0:2.08-0.fdr.2
- Fix locale support broken in previous version

* Wed Sep  1 2004 Pádraig Brady <P at draigBrady.com> - 0:2.08-0.fdr.1
- Update to 2.08.
- Remove redundant patch.

* Wed May  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.06-0.fdr.1
- Update to 2.06.
- Add %%{_bindir}/fslint symlink.
- Make installation Python version independent.

* Thu Aug 28 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.02-0.fdr.2
- Requires: cpio, remove redundant findutils dependency (bug 539).
- Fix version in dependency on python.

* Thu Jul 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.02-0.fdr.1
- First build, based on upstream specfile.
