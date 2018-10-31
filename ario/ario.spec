Name:     ario
Version:  1.5.1
Release:  2%{?dist}
Summary:  Ario MPD Client
License:  GPLv2+
URL:      http://ario-player.sourceforge.net/index.php
Source0:  https://downloads.sourceforge.net/ario-player/%{name}-%{version}.tar.gz

BuildRequires: pkgconfig(avahi-glib)
BuildRequires: pkgconfig(gnutls)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libmpdclient)
BuildRequires: pkgconfig(libnotify)
BuildRequires: pkgconfig(libsoup-2.4)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(pygtk-2.0)
BuildRequires: pkgconfig(taglib)
BuildRequires: pkgconfig(unique-1.0)
BuildRequires: libgcrypt-devel
BuildRequires: gcc
BuildRequires: intltool
BuildRequires: desktop-file-utils
#BuildRequires: gettext
#BuildRequires: perl(XML::Parser)
#BuildRequires: autoconf automake libtool

%description
Ario is a GTK2 client for MPD (Music player daemon). The interface used to 
browse the library is inspired by Rhythmbox but Ario aims to be much lighter 
and faster.  It runs on Linux and Microsoft Windows

%prep
%autosetup

sed -i -e 's|<glib/gi18n\.h>|<glib.h>|g' src/ario-profiles.c
sed -i -e 's|<glib/gslist\.h>|<glib.h>|g' src/ario-profiles.h

%build
%configure \
  --enable-static=no \
  --disable-silent-rules \
  --enable-libmpdclient2 \
  --enable-python \
  --disable-dbus

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install INSTALL="install -p"

%find_lang ario
find %{buildroot} -name '*.la' -delete

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/ario.desktop


%files -f ario.lang
%defattr(-,root,root,-)
%doc ChangeLog TODO AUTHORS
%license COPYING
%{_bindir}/ario
%{_libdir}/ario
%{_datadir}/applications/ario.desktop
%{_datadir}/ario
%{_datadir}/icons/hicolor/*/apps/ario.*

%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.5.1-2
- Update BR format and Requires

* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.5.1-1
- Updated to 1.5.1

* Fri Mar 25 2011 John Ford <john@johnford.info> - 1.5-1
- Updated source to ario-1.5

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 16 2010 Adam Jackson <ajax@redhat.com> 1.1-9
- ario-1.1-add-needed.patch: Fix FTBFS from --no-add-needed

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 <johnhford.gmail@com> - 1.1-6
- Bumped release because I forgot to import specfile before
- running make tag

* Sun Nov 09 2008 <johnhford@gmail.com> - 1.1-5
- Removed gettext-devel from BuildRequires
- Removed gettext from Requires
- Modified sed routine on desktop files
- Removed .la libtool files
- Clean up of code

* Sat Nov 08 2008 johnhford@gmail.com - 1.1-4
- Corrected issue as per Mamoru Tasaka recomendations
-  *license tag correction
-  *Removed redundant BuildRequires and Requires
-  *Corrected perl dependancies
-  *Timestamp preservation
-  *Using find_lang macro now
-  *No static libraries
-  *Removed unneeded documents
-  *Fixed desktop file

*Fri Oct 10 2008 John Ford <johnhford@gmail.com> 1.1-3
- Ran mock build, added two build requirements

*Sun Sep 28 2008 John Ford <johnhford@gmail.com> 1.1-2
- Inserted %%post and %%postun for gtk-update-icon-cache

*Sun Sep 28 2008 John Ford <johnhford@gmail.com> 1.1-1
- Initial specfile written


