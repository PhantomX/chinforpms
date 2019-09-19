%global with_tests 0

Name:           retext
Version:        7.0.4
Release:        1%{?dist}
License:        GPLv3+
Summary:        Text editor for Markdown and reStructuredText
Summary(de):    Texteditor für Markdown und reStructuredText

URL:            https://github.com/retext-project/retext
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# English man pages are taken from the Debian package.
Source1:        %{name}.1

BuildArch:      noarch

BuildRequires:  desktop-file-utils
# For autosetup -S git
BuildRequires:  git
BuildRequires:  libappstream-glib
BuildRequires:  librsvg2-tools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  qt5-linguist

%if 0%{?with_tests}
BuildRequires:  python3-chardet
BuildRequires:  python3-docutils
BuildRequires:  python3-markdown
BuildRequires:  python3-markups
BuildRequires:  python3-pygments
BuildRequires:  python3-qt5
BuildRequires:  qt5-qtbase-gui
%endif

Requires:       hicolor-icon-theme
Requires:       python3-chardet
Requires:       python3-docutils
Requires:       python3-enchant
Requires:       python3-markdown
Requires:       python3-markups >= 2.0.0
Requires:       python3-pygments
Requires:       python3-qt5
Requires:       python3-qt5-webkit
Requires:       qt5-qtlocation


%description
ReText is a simple but powerful text editor for Markdown and reStructuredText.

%description -l de
ReText ist ein einfacher, aber leistungsfähiger Texteditor
für Markdown und reStructuredText.


%prep
%autosetup -S git

sed -e "s|'lrelease'|'lrelease-qt5'|" -i setup.py

%build
%py3_build

%install
%py3_install

mkdir -p %{buildroot}/%{_mandir}/man1
install -p -m 0644 %{S:1} %{buildroot}/%{_mandir}/man1

# Generate resized icons
for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert icons/%{name}.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 0644 icons/retext.svg %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/

#desktop-file-install \
#--dir=%{buildroot}%{_datadir}/applications \
#%{_builddir}/%{name}-%{version}/data/*.desktop


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml || :
desktop-file-validate %{buildroot}%{_datadir}/applications/me.mitya57.ReText.desktop

%if 0%{?with_tests}
%{__python3} setup.py test
%endif


%files
%doc changelog.md configuration.md README.md
%license  LICENSE_GPL
%{_bindir}/%{name}
%{_datadir}/metainfo/*.appdata.xml
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}/
%{_mandir}/man1/*.1.*
%{python3_sitelib}/ReText/
%{python3_sitelib}/*egg-info


%changelog
* Mon Jun 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 7.0.4-1
- 7.0.4
- Requirements update

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 7.0.3-2
- Rebuilt for Python 3.7

* Sat Jun 09 2018 Mike DePaulo <mikedep333@gmail.com> - 7.0.3-1
- New upstream version

* Tue Jun 05 2018 Mike DePaulo <mikedep333@gmail.com> - 7.0.1-2
- Fix the screenshot URL in the appdata file

* Tue Jun 05 2018 Mike DePaulo <mikedep333@gmail.com> - 7.0.1-1
- New upstream version
- Project moved to GitHub

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 Mario Blättermann <mario.blaettermann@gmail.com> - 7.0.0-1
- New upstream version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 6.0.2-2
- Rebuild for Python 3.6

* Tue Oct 04 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 6.0.2-1
- New upstream version
- Fixed download link

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Jul 10 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 6.0.1-1
- New upstream version

* Fri May 13 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 6.0.0-1
- New upstream version
- Bump requirement to python3-markups >= 2.0.0

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-4
- Requires: python3-qt5-webkit

* Wed Feb 17 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 5.3.0-3
- Patch for Enchant (RHBZ #1309365)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Mario Blättermann <mario.blaettermann@gmail.com> - 5.3.0-1
- New upstream version

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 05 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 5.2.1-1
- New upstream version
- Removed custom appdata file

* Fri Sep 11 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 5.1.0-1
- New upstream version
- Remove wpgen stuff

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 15 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.2-2
- New upstream version
- Add qt5-qtlocation to runtime requirements (bz #1215369)

* Sat Jan 31 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.1-7
- Fix file permissions
- Add update-desktop-database scripts
- Fix download location
- Extended description in appdata file, fix license declaration 

* Thu Jan 15 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.1-6
- Fix URLs of extra sources
- Add appdata file

* Sat Jan 10 2015 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.1-5
- Replace qt-devel with qt5-qttools-devel to use the correct
  linguist toolchain

* Tue Dec 30 2014 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.1-4
- Use the %%license macro
- Keep the tests enabled, but make them optional

* Wed Dec 17 2014 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.1-3
- Add qt-devel to BuildRequires

* Tue Dec 16 2014 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.1-2
- Add noarch tag

* Mon Dec 01 2014 Mario Blättermann <mario.blaettermann@gmail.com> - 5.0.1-1
- New upstream version
- Man pages from the Debian package
- Install *.desktop file
- Enable tests

* Wed Jan 08 2014 Mario Blättermann <mario.blaettermann@gmail.com> - 4.0.1-2
- Spec file cleanup

* Wed May 08 2013 Huaren Zhong <huaren.zhong@gmail.com> - 4.0.1
- Rebuild for Fedora

* Sat Feb 18 2012 i@marguerite.su
- update to 3.0beta1

* Thu Dec 29 2011 i@marguerite.su
- initial package 2.1.3
