Name:           gpa
Summary:        Graphical user interface for GnuPG
Version:        0.11.0
Release:        1%{?dist}

License:        GPL-3.0-or-later
URL:            https://www.gnupg.org/related_software/gpa/
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2.sig

Patch1:         gpa-keyservers.patch

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnupg2
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(zlib)
Requires:       gnupg2
Requires:       gnupg2-smime
Requires:       hicolor-icon-theme

%description
GNU Privacy Assistant (GPA) is a graphical frontend for the GNU
Privacy Guard (GnuPG).  GPA can be used to encrypt, decrypt, and sign
files, to verify signatures and to manage the private and public keys.


%prep
%autosetup -p1

sed -e '/en_US.ISO8859-1/d' -i *.desktop

%build
export CFLAGS+=" -fno-exceptions -Wno-implicit-function-declaration"
%configure \
  --disable-silent-rules \
  --disable-rpath

%make_build


%install
%make_install

desktop-file-edit \
  --remove-category=Application \
  --remove-category=Utility \
  --add-category=System \
  --set-key=Exec \
  --set-value="gpa %%F" \
  --set-key=Keywords \
  --set-value="keyring;encryption;security;sign;" \
  --add-mime-type="application/pgp-encrypted" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/gpa.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -p -m644 gpa.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/gpa.png
rm -rf %{buildroot}%{_datadir}/pixmaps

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README* THANKS
%{_bindir}/gpa
%{_datadir}/gpa/
%{_datadir}/applications/gpa.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_mandir}/man1/*.1*


%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 0.11.0-1
- 0.11.0
- BR: gtk+-3.0

* Thu Apr 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.10.0-2
- http download links

* Wed Oct 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.10.0-1
- 0.10.0

* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.10-2
- BR: gcc

* Wed Apr 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.10-1
- 0.9.10
- Spec fully updated

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.0-1
- gpa-0.9.0
- make buildable against libassuan1 (f14+)

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.0-3
- Explicitly BR libassuan-static in accordance with the Packaging
  Guidelines (libassuan-devel is still static-only).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-1
- gpg-0.8.0
- optimize scriptlets

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 05 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.6-5
- BR: gnupg (#440849)
- validate .desktop file

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.6-4
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.6-3
- respin (BuildID)

* Thu Aug 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.6-2
- License: GPLv2+

* Thu May 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.6-1
- gpa-0.7.6

* Mon Feb 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.7.5-1
- gpa-0.7.5

* Thu Sep 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.4-2
- fc6 respin

* Tue Jul 25 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.4-1
- 0.7.4

* Thu May 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.3-2
- cleanup .dt patch
- update URL:, Source: tags

* Wed Mar 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.3-1
- 0.7.3

* Mon Feb 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.7.0-5
- follow fdo icon spec
- drop superfluous BR: gnupg

* Thu May 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.7.0-4
- Rebuild.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.7.0-3
- rebuilt

* Tue Nov 25 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.0-0.fdr.2
- Include fix against hang at startup when no private key exists (bug 864).

* Thu Oct 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.0-0.fdr.1
- Update to 0.7.0.
- Spec file and desktop entry cleanups.
- Use upstream icon for desktop entry.
- Update description.

* Tue Mar 25 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.1-0.fdr.3
- Fix icon in desktop entry (#64).
- Don't include INSTALL in %%doc.

* Sun Mar 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.1-0.fdr.2
- BuildRequire gnupg >= 1.2.1-3 for LDAP and HKP support.
- Add icon for the desktop entry (#64).

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.6.1-0.fdr.1
- Update to current Fedora guidelines.

* Wed Feb 12 2003 Warren Togami <warren@togami.com> 0.6.1-1.fedora.2
- Add BuildRequires zlib-devel

* Sun Feb  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.6.1-1cr
- First Fedora release.
