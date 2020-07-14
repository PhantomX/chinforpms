%global commit 4ed9411f4dc2801d7f983734ae4003102b8f361d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200621
%global with_snapshot 0

%global with_gtk3  0
%global with_python  0

%if 0%{?with_gtk3}
%global with_fancy 1
# Only snapshot currently
%global with_snapshot 1
%else
%global with_fancy 0
%endif

%{!?with_autotools:%global with_autotools 0}

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%global with_autotools 1
%endif

# toggle to avoid temporary docbook-utils and Tex Live dependency issues
%global build_manual 1

Name:           claws-mail
Version:        3.17.6
Release:        100%{?gver}%{?dist}
Epoch:          1
Summary:        Email client and news reader based on GTK+
License:        GPLv3+
URL:            http://claws-mail.org

%global pluginapi %{version}.0

%if 0%{?with_snapshot}
Source0:        https://git.claws-mail.org/?p=claws.git;a=snapshot;h=%{commit};sf=tgz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://www.claws-mail.org/releases/%{name}-%{version}.tar.xz
%endif

# rhbz#1179279
Patch11:        claws-mail-system-crypto-policies.patch

# Useful patches from Debian
Patch50:        11mark_trashed_as_read.patch
Patch51:        12fix_manpage_header.patch

# added 20170310 / webkitgtk removal from fedora rhbz#1375803
%if !0%{with_fancy}
Obsoletes:      %{name}-plugins-fancy < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-plugins-fancy = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%if !0%{?with_python}
Obsoletes:      %{name}-plugins-python < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-plugins-python = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  flex, bison
BuildRequires:  glib2-devel >= 2.28.0
%if 0%{?with_gtk3}
BuildRequires:  gtk3-devel >= 3.24.0
%else
BuildRequires:  gtk2-devel >= 2.24.0
%endif
BuildRequires:  gnutls-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  openldap-devel >= 2.0.7
BuildRequires:  enchant-devel
%if !0%{?rhel}
%ifnarch s390 s390x
BuildRequires:  pilot-link-devel
%endif
%endif
BuildRequires:  bzip2-devel
BuildRequires:  gpgme-devel >= 1.0.1
BuildRequires:  desktop-file-utils startup-notification-devel
BuildRequires:  pkgconfig
BuildRequires:  gettext gettext-devel
BuildRequires:  libetpan-devel >= 1.4.1
%if !0%{?rhel}
BuildRequires:  compface-devel
%endif
BuildRequires:  perl-devel perl-generators perl(ExtUtils::Embed)
BuildRequires:  libSM-devel
BuildRequires:  NetworkManager-libnm-devel
BuildRequires:  dbus-glib-devel
%if 0%{?with_autotools}
BuildRequires:  autoconf
BuildRequires:  automake
%endif
BuildRequires:  libtool
%if 0%{build_manual}
BuildRequires:  docbook-utils docbook-utils-pdf
%endif

BuildRequires:  curl-devel
BuildRequires:  libxml2-devel expat-devel
BuildRequires:  libidn-devel
BuildRequires:  libarchive-devel
BuildRequires:  libytnef-devel
BuildRequires:  ghostscript
BuildRequires:  gumbo-parser-devel
BuildRequires:  poppler-glib-devel
# webkit removed since Fedora 27 due to unfixed security issues
%if 0%{with_fancy}
BuildRequires:  webkit2gtk3-devel
BuildRequires:  libsoup-devel
%endif
# fix #496149
BuildRequires:  libnotify-devel
%if 0%{?with_python}
%if 0%{?with_gtk3}
BuildRequires:  python3 python3-devel python3-gobject-devel
%else
BuildRequires:  python2 python2-devel pygtk2-devel
%endif
%endif
BuildRequires:  libcanberra-devel
# this is an optional subpackage not pulled in by libcanberra-devel
%if 0%{?with_gtk3}
BuildRequires:  libcanberra-gtk3
%else
BuildRequires:  libcanberra-gtk2
%endif
BuildRequires:  libgdata-devel >= 0.6.4
BuildRequires:  libgnome-devel
BuildRequires:  libical-devel
BuildRequires:  librsvg2-devel

# provide plugin api version (see /usr/include/claws-mail/common/version.h)
Provides:       claws-mail(plugin-api)%{?_isa} = %pluginapi


%description
Claws Mail is an email client (and news reader), based on GTK+, featuring
quick response, graceful and sophisticated interface, easy configuration,
intuitive operation, abundant features, and extensibility.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains the header files
and pkgconfig file needed for development with %{name}.


%package plugins
Summary:  Additional plugins for Claws Mail
Requires: %{name}-plugins-acpi-notifier = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-address-keeper = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-archive = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-att-remover = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-attachwarner = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-bogofilter = %{?epoch:%{epoch}:}%{version}-%{release}
%if !0%{?rhel}
Requires: %{name}-plugins-bsfilter = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires: %{name}-plugins-clamd = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-dillo = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{with_fancy}
Requires: %{name}-plugins-fancy = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires: %{name}-plugins-fetchinfo = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-gdata = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-litehtml = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-libravatar = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-mailmbox = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-managesieve = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-newmail = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-notification = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-pdf-viewer = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-perl = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-pgp = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?with_python}
Requires: %{name}-plugins-python = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires: %{name}-plugins-rssyl = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-smime = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-spamassassin = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-spam-report = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-tnef = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-plugins-vcalendar = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins
Additional plugins for Claws Mail.


%package plugins-acpi-notifier
Summary:        ACPI notification plugin for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-acpi-notifier
Enables mail notification via LEDs on some laptops. Options can be found on
the 'Plugins/Acpi Notifier' page of the preferences.


%package plugins-address-keeper
Summary:        Never forget a typed address in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-address-keeper
This plugin allows saving outgoing addresses to a designated folder
in the address book. Addresses are saved only if not found in the
address book to avoid unwanted duplicates.


%package plugins-archive
Summary:        Archiving features for Claws Mail 
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-archive
%{summary}


%package plugins-attachwarner
Summary:        Attachment warner plugin for Claws Mail 
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-attachwarner
Warns when the user composes a message mentioning an attachment in the message
body but without attaching any files to the message. 


%package plugins-att-remover
Summary:        Attachments remover plugin for Claws Mail 
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-att-remover
Enables the removal of attachments from emails. When right-clicking a message,
choose 'Remove attachments' from the sub-menu.

%package plugins-bogofilter
Summary:        Bogofilter plugin for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       bogofilter

%description plugins-bogofilter
%{summary}

%if !0%{?rhel}
%package plugins-bsfilter
Summary:        Bayesian spam filtering for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       bsfilter

%description plugins-bsfilter
Bayesian spam filtering for Claws Mail using Bsfilter.
%endif


%package plugins-clamd
Summary:        Use Clam AntiVirus to scan messages in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-clamd
This plugin uses Clam AntiVirus to scan all messages that are
received from an IMAP, LOCAL or POP account.
When a message attachment is found to contain a virus it can be
deleted or saved in a specially designated folder.
Options can be found in /Configuration/Preferences/Plugins/Clam AntiVirus.


%package plugins-dillo
Summary:        Display HTML emails in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       dillo

%description plugins-dillo
This plugin renders HTML email via the Dillo Web Browser.


%package plugins-litehtml
Summary:        Display HTML emails in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-litehtml
This plugin renders HTML email via the Gumbo parsing library.


%if 0%{with_fancy}
%package plugins-fancy
Summary:        Display HTML emails in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-fancy
This plugin renders HTML email via the GTK+ port of the WebKit library.
%endif


%package plugins-fetchinfo
Summary:        Modify headers of downloaded messages in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-fetchinfo
This plugin inserts headers containing some download information:
UIDL, Sylpheeds account name, POP server, user ID and retrieval time.


%package plugins-gdata
Summary:        Access to GData (Google services) for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-gdata
Access to GData (Google services) for Claws Mail.

The only currently implemented feature is inclusion of
Google contacts into the address completion.


%package plugins-mailmbox
Summary:        Add support for mailboxes in mbox format to Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-mailmbox
This plugin provides direct support for mailboxes in mbox format.

%package plugins-managesieve
Summary:        Add Manage sieve support to Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-managesieve
Manage sieve filters on a server using the ManageSieve protocol.

%package plugins-newmail
Summary:        Make Claws Mail write a message header summary to a file
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-newmail
Write a message header summary to a log file (defaults to ~/Mail/NewLog) on
arrival of new mail *after* sorting.


%package plugins-notification
Summary:        Various ways to notify about new messages in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-notification
This plugin collects various ways to notify the user of new (and possibly
unread) mail. Currently, a pop-up and a mail banner are implemented.


%package plugins-pdf-viewer
Summary:        Enables the viewing of PDF and PostScript attachments
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-pdf-viewer
This plugin handles PDF and Postscript attachments.


%package plugins-perl
Summary:        Perl based extended filtering engine for Claws Mail
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-perl
This plugin provides an extended filtering engine for the email client
Claws Mail. It allows for the use of full perl power in email filters.

%package plugins-pgp
Summary:        PGP plugin for signing and encrypting with Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pinentry-gui

%description plugins-pgp
%{summary}

%if 0%{?with_python}
%package plugins-python
Summary:        Python scripting access to Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-python
This plugin offers a Python scripting access to Claws Mail. Python code can be
entered interactively into an embedded Python console or stored in scripts
under ~/.claws-mail/python-scripts. The scripts are then accessible via the
menu of the main window.
%endif

%package plugins-libravatar
Summary:        Libravatar plugin for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-libravatar
This plugin allows showing the profile picture associated to email
addresses provided by https://www.libravatar.org/. You can read
more about what is this at http://wiki.libravatar.org/description/.

%package plugins-rssyl
Summary:        RSS plugin for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-rssyl
Allows you to read your favorite RSS news feeds in Claws Mail. RSS 1.0,
2.0 and Atom feeds are currently supported.


%package plugins-smime
Summary:        S/MIME support for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       claws-mail-plugins-pgp%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-smime
This plugin handles S/MIME signed and/or encrypted mails. You can decrypt
mails, verify signatures or sign and encrypt your own mails.


%package plugins-spamassassin
Summary:        Spamassassin plugin for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       spamassassin

%description plugins-spamassassin
%{summary}


%package plugins-spam-report
Summary:        Report spam mail to various places with Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-spam-report
This plugin for Claws Mail can report spam mail to various places.


%package plugins-tnef
Summary:        TNEF message parsing for Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-tnef
This plugin allows reading of application/ms-tnef attachments.


%package plugins-vcalendar
Summary:        Handling of vCalendar messages in Claws Mail
Requires:       claws-mail%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins-vcalendar
This plugin enables vCalendar message handling like that produced by
Evolution or Outlook. It also supports subscribing to remote webCal feeds, and
exporting of your meetings or all your calendars.


%prep
%if 0%{?with_snapshot}
%setup -q -n claws-%{shortcommit}
echo 'echo %{version}-%{shortcommit}' > version
%else
%setup -q
%endif

%if 0%{?fedora} > 20
%patch11 -p1 -b.syscrypto
%endif

%patch50 -p1 -b.trash
%patch51 -p1 -b.manheader

%if 0%{?with_autotools}
NOCONFIGURE=1 ./autogen.sh
%endif

# change DEFAULT_INC_PATH for the optional external "inc" tool to match
# Fedora's "nmh" package // unimportant fix, but add a grep guard, too
sed -i -e 's!\"/usr/bin/mh/inc\"!\"/usr/bin/inc\"!g' src/common/defs.h
grep DEFAULT_INC_PATH src/common/defs.h || exit -1

# avoid relinking with several shared libs used by libperl
# when linking with libperl
grep 'PERL_LDFLAGS *=' configure || exit -1
sed -i 's!\(PERL_LDFLAGS *=\).*$!\1-lperl!g' configure

%if 0%{?with_python}
# a really ugly hack to have the Python plug-in dlopen the versioned
# run-time lib, with grep guards so we don't need a patch
#
# ensure that the definition exists
grep 'PYTHON_SHARED_LIB=.*\.so\"$' configure || exit -1
# append .1.0
sed -i 's!\(PYTHON_SHARED_LIB=.*\.so\)\"$!\1.1.0\"!' configure
# ensure that the definition no longer ends with .so"
grep 'PYTHON_SHARED_LIB=.*\.so\"$' configure && exit -1
# ensure that the code that uses it is still there
grep 'dlopen.*PYTHON_SHARED_LIB' src/plugins/python/* -R || exit -1
%endif

%if 0%{?fedora}
cat << EOF > README.Fedora
Firefox and Claws Mail

    Be sure to set the TMPDIR environment variable, so both applications
    always use the same directory for temporary files. Else the directory
    would vary depending on whether or not Claws Mail is launched as mailer
    from within Firefox. [ https://bugzilla.redhat.com/956380 ]
EOF
%endif


%build
%configure \
           --disable-rpath \
%if 0%{?rhel}
           --disable-bsfilter-plugin \
%endif
%if !0%{with_fancy}
           --disable-fancy-plugin \
%endif
%if !0%{?with_python}
           --disable-python-plugin \
%endif
           --enable-appdata \
%{nil}

# guard for pluginapi
SOURCEAPI=$(grep -A 1 VERSION_NUMERIC src/common/version.h | tr -d '\n' | perl -ne 's/[\\\s]//g; m/(\d+),(\d+),(\d+),(\d+)/; print("$1.$2.$3.$4");')
[ "%pluginapi" == "$SOURCEAPI" ] || exit -1

%make_build LIBTOOL=%{_bindir}/libtool

%install

export LIBTOOL=%{_bindir}/false
%make_install

%find_lang claws-mail

# use provided desktop file
desktop-file-install \
--add-category="Office" \
--remove-category="GTK" \
--remove-key="Encoding" \
--remove-key="Info" \
--dir=%{buildroot}%{_datadir}/applications \
%{name}.desktop

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

rm -f %{buildroot}%{_infodir}/dir

find %{buildroot} -type f -name '*.la' -delete
find %{buildroot}%{_libdir}/claws-mail/plugins/ -type f -name \
"*.a" -exec rm -f {} ';'

%if 0%{build_manual}
# we include the manual in the doc section
rm -rf _tmp_manual && mkdir _tmp_manual
mv %{buildroot}%{_datadir}/doc/claws-mail/manual _tmp_manual
rm -f %{buildroot}%{_datadir}/doc/claws-mail/RELEASE_NOTES
%endif

# cleanup non utf8 files
for file in AUTHORS;
do iconv -f iso8859-1 -t utf-8 ${file} > \
 ${file}.conv && mv -f ${file}.conv ${file}
done;

# don't think we need icon-theme.cache
rm -f %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

# set same date on config.h across builds for multilib (#340871)
touch -r NEWS %{buildroot}%{_includedir}/%{name}/config.h


%files -f claws-mail.lang
%license COPYING
%doc ABOUT-NLS AUTHORS NEWS README RELEASE_NOTES TODO
%if !0%{with_snapshot}
%doc ChangeLog
%endif
%if 0%{?fedora}
%doc README.Fedora
%endif
%if 0%{build_manual}
%doc _tmp_manual/manual
%endif
%{_bindir}/*
%dir %{_libdir}/claws-mail
%dir %{_libdir}/claws-mail/plugins
%{_mandir}/man1/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
#%%{_metainfodir}/claws-mail.appdata.xml

%files devel
%{_includedir}/claws-mail/
%{_libdir}/pkgconfig/claws-mail.pc

%files plugins
# meta-package only


%files plugins-acpi-notifier
%{_libdir}/claws-mail/plugins/acpi_notifier*
#%%{_metainfodir}/claws-mail-acpi_notifier.metainfo.xml


%files plugins-archive
%{_libdir}/claws-mail/plugins/archive*
#%%{_metainfodir}/claws-mail-archive.metainfo.xml


%files plugins-attachwarner
%{_libdir}/claws-mail/plugins/attachwarner*
#%%{_metainfodir}/claws-mail-attachwarner.metainfo.xml


%files plugins-address-keeper
%{_libdir}/claws-mail/plugins/address_keeper*
#%%{_metainfodir}/claws-mail-address_keeper.metainfo.xml


%files plugins-att-remover
%{_libdir}/claws-mail/plugins/att_remover*
#%%{_metainfodir}/claws-mail-att_remover.metainfo.xml


%files plugins-bogofilter
%{_libdir}/claws-mail/plugins/bogofilter.so
#%%{_metainfodir}/claws-mail-bogofilter.metainfo.xml


%if !0%{?rhel}
%files plugins-bsfilter
%{_libdir}/claws-mail/plugins/bsfilter*
#%%{_metainfodir}/claws-mail-bsfilter.metainfo.xml
%endif


%files plugins-clamd
%{_libdir}/claws-mail/plugins/clamd*
#%%{_metainfodir}/claws-mail-clamd.metainfo.xml


%files plugins-dillo
%{_libdir}/claws-mail/plugins/dillo*
#%%{_datadir}/_metainfodir/claws-mail-dillo.metainfo.xml


%files plugins-litehtml
%{_libdir}/claws-mail/plugins/litehtml*
#%%{_datadir}/appdata/claws-mail-litehtml.metainfo.xml


%if 0%{with_fancy}
%files plugins-fancy
%{_libdir}/claws-mail/plugins/fancy*
#%%{_metainfodir}/claws-mail-fancy.metainfo.xml
%endif


%files plugins-fetchinfo
%{_libdir}/claws-mail/plugins/fetchinfo*
#%%{_metainfodir}/claws-mail-fetchinfo.metainfo.xml


%files plugins-gdata
%{_libdir}/claws-mail/plugins/gdata*
#%%{_metainfodir}/claws-mail-gdata.metainfo.xml


%files plugins-mailmbox
%{_libdir}/claws-mail/plugins/mailmbox*
#%%{_metainfodir}/claws-mail-mailmbox.metainfo.xml


%files plugins-managesieve
%{_libdir}/claws-mail/plugins/managesieve.so


%files plugins-newmail
%{_libdir}/claws-mail/plugins/newmail.so
#%%{_metainfodir}/claws-mail-newmail.metainfo.xml


%files plugins-notification
%{_libdir}/claws-mail/plugins/notification.so
#%%{_metainfodir}/claws-mail-notification.metainfo.xml


%files plugins-pdf-viewer
%{_libdir}/claws-mail/plugins/pdf_viewer.so
#%%{_metainfodir}/claws-mail-pdf_viewer.metainfo.xml


%files plugins-perl
%{_libdir}/claws-mail/plugins/perl.so
#%%{_metainfodir}/claws-mail-perl.metainfo.xml


%files plugins-pgp
%{_libdir}/claws-mail/plugins/pgp*.so
%{_libdir}/claws-mail/plugins/pgp*.deps
#%%{_metainfodir}/claws-mail-pgp*.metainfo.xml


%if 0%{?with_python}
%files plugins-python
%{_libdir}/claws-mail/plugins/python*
#%%{_metainfodir}/claws-mail-python.metainfo.xml
%endif


%files plugins-libravatar
%{_libdir}/claws-mail/plugins/libravatar*
#%%{_metainfodir}/claws-mail-libravatar.metainfo.xml


%files plugins-rssyl
%{_libdir}/claws-mail/plugins/rssyl*
#%%{_metainfodir}/claws-mail-rssyl.metainfo.xml


%files plugins-smime
%{_libdir}/claws-mail/plugins/smime.so
%{_libdir}/claws-mail/plugins/smime.deps
#%%{_metainfodir}/claws-mail-smime.metainfo.xml


%files plugins-spamassassin
%{_libdir}/claws-mail/plugins/spamassassin.so
#%%{_metainfodir}/claws-mail-spamassassin.metainfo.xml


%files plugins-spam-report
%{_libdir}/claws-mail/plugins/spamreport.so
#%%{_metainfodir}/claws-mail-spam_report.metainfo.xml


%files plugins-tnef
%{_libdir}/claws-mail/plugins/tnef*
#%%{_metainfodir}/claws-mail-tnef_parse.metainfo.xml


%files plugins-vcalendar
%{_libdir}/claws-mail/plugins/vcalendar*
#%%{_metainfodir}/claws-mail-vcalendar.metainfo.xml


%changelog
* Mon Jul 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:3.17.6-100
- 3.17.6

* Tue Jun 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1:3.17.5-101.20200621git4ed9411
- Snapshot

* Mon Feb 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.5-100
- 3.17.5

* Fri Nov 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.4-104.20191125git5f1063a
- New snapshot

* Thu Oct 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.4-103.20191030gitf08f60c
- New snapshot

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.4-102.20190904git2795946
- New snapshot

* Mon Aug 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.4-101.20190813git6da2dcb
- Snapshot to get some fixes

* Fri Jul 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.4-100
- 3.17.4

* Fri Jun 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.3-102.20190529git08293cc
- gtk2 again, gtk3 needs more work

* Thu Jun 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:3.17.3-103.20190518git3c18210
- Snapshot and gtk3
- litehtml plugin, BR: gumbo-parser-devel
- Optional python2 plugin
- Epoch
- Explicit plugins Requires, instead plugin-abi

* Tue Dec 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.17.3-100
- 3.17.3

* Fri Dec 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.17.2-100.chinfo
- 3.17.2

* Sat Sep 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.17.1-100.chinfo
- 3.17.1

* Thu Aug 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.17.0-100.chinfo
- 3.17.0
- dillo plugin again

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.16.0-101.chinfo
- f28 sync

* Wed Jan 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.16.0-100.chinfo
- 3.16.0
- Remove dillo again

* Tue Oct 03 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.15.1-101.chinfo
- Missing fancy plugin f27 obsoletes

* Wed Sep 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.15.1-100.chinfo
- 3.15.1
- f26 sync

* Sat Jul 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.15.0-103.chinfo
- Reenable fancy, dillo plugin is not good yet

* Sat Jul 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.15.0-102.chinfo
- Disable fancy again
- Upstream patch to add dillo plugin
- BR: autoconf, automake and fuzz 2, for dillo patch

* Thu Jul 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.15.0-101.chinfo
- SVG support with librsvg2

* Thu Jul 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.15.0-100.chinfo
- Download URL
- Reenable fancy for the time
- Some patches from Debian
- Make rpmlint happy

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.15.0-3
- Perl 5.26 rebuild

* Thu Mar 30 2017 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.15.0-2
- fix build

* Tue Mar 28 2017 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.15.0-1
- version upgrade
- use external libical

* Thu Mar 09 2017 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.14.1-5
- remove webkitgtk support (see rhbz#1375803)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.14.1-3
- Rebuild for gpgme 1.18

* Sat Dec 10 2016 Andreas Bierfert <andreas.bierfert@lowlatency.de> - 3.14.1-2
- rebuild for libetpan 1.7.2 soname change

* Fri Nov 25 2016 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.14.1-1
- update to current release
- update system-crypto-policies patch

* Sun Aug 07 2016 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.14.0-1
- version upgrade

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.13.2-3
- Perl 5.24 rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.13.2-1
- version upgrade, includes fix for CVE-2015-8708

* Tue Dec 22 2015 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.13.1-4
- fix the broken while-loop in conv_jistoeuc() (upstream bug 3584)

* Mon Dec 21 2015 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.13.1-2
- build with the bundled libical to avoid breakage (#1225903)
- merge the separate claws-mail-plugins meta-package

* Sun Dec 20 2015 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.13.1-1.1
- force libtoolize so F22 build succeeds, too

* Sun Dec 20 2015 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.13.1-1
- upgrade to 3.13.1, includes fix for CVE-2015-8614
- obsolete geolocation/libchamplain plugin / deleted upstream
- drop old Obsoletes tags

* Fri Dec 18 2015 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.13.0-2
- merge the fix for the gtkcmctree crash / summary_mark_row_as_read
  (#1172963)

* Sun Oct 25 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.13.0-1
- version upgrade

* Thu Jul 23 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.12.0-1
- version upgrade
- add managesieve plugin subpackage

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.11.1-10
- Perl 5.22 rebuild

* Sat Apr 25 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.11.1-9
- rebuild for gdata

* Mon Feb 23 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 3.11.1-8
- Run libtoolize to update libtool files and fix FTBFS (#1195313).
- BR libcanberra-gtk2 which is not pulled in by libcanberra-devel.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.11.1-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 04 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.11.1-6
- fix clamav preferences crash (rhbz#118891, rhbz#118774)

* Tue Feb 03 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.11.1-5
- enable gdata plugin on epel

* Tue Feb 03 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.11.1-4
- workaround for crashes in gtk_cmctree (rhbz#1172963, rhbz#1165158)
- enable tnef plugin on epel
- disable bsfilter plugin on epel

* Thu Jan 15 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.11.1-3
- fix segfault in wizard and account prefs (rhbz#1123895, rhbz#1182146)
- do not own icon directories owned by hicolor-icon-theme (rhbz#1171902)
  patch by David King
- add patch to build with system libical (rhbz#1079729)
- add patch to utilize system crypto-policies >=f21 (rhbz#1179279)
- require pinentry-gui on >f19 again (rhbz#587326,rhbz#981923)

* Sat Nov 01 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.11.1-2
- bump for libetpan 1.6

* Fri Oct 31 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.11.1-1
- version upgrade
- appdata removed upstream

* Sat Oct 25 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.11.0-1
- version upgrade (rhbz#1155086)
- disable SSLv3 (rhbz#1153970)
- include plugin appdata

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.10.1-3
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.10.1-1
- version upgrade

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.10.0-1
- version upgrade (fixes rhbz: 569478,601982,977924,982533,990650,1011098,
  1010993,1035851,1036346,1063035,1070480,1071327,1076387,1078996,1079509,
  1079620,1081224,1085382,1090300,1096041,1096895 and similar crashes)
- add libravatar plugin
- add appdata file

* Sun May 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.9.3-4
- No longer needs old gnome-libs v1 for gnome-config

* Sat May 17 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.3-3
- rebuild for new libetpan

* Thu Apr 17 2014 Adam Williamson <awilliam@redhat.com> - 3.9.3-2
- rebuild for new libgdata

* Sun Dec 15 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.3-1
- version upgrade

* Mon Aug  5 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.9.2-7
- BR libgcrypt-devel for src/common/ssl.c

* Mon Aug  5 2013 Michael Schwendt <mschwendt@fedoraproject.org> 
- 3.9.2-6
- fix FTBFS (#992061) / basically libetpan FTBFS for armv7hl
- fix Python plug-in crash: it dlopen's libpython2.7.so (#991138)
  which would only be found in the optional -devel package, so replace
  that with the fully versioned run-time libname in %%prep

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.9.2-4
- Perl 5.18 rebuild

* Sat Jul 13 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.9.2-3
- for Fedora based builds, require pinentry-gtk instead of the virtual
  pinentry-gui, because pinentry-qt fails silently (#981923)
- fix crash in Plugins/Fancy "Save Image As" (#979700)
- in %%prep section create a README.Fedora %%doc file which mentions
  setting $TMPDIR when using Claws Mail together with Firefox (#956380)

* Mon Jul  8 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.9.2-2
- fix double-free crash in "Preferences for new account" (#981889)

* Mon Jun 17 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.2-1
- version upgrade

* Wed May 22 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.9.1-2
- also include the README.Fedora for the missing GeoLocation plugin
  and build the empty -plugins-geolocation package as before to fix
  upgrade path broken dep

* Thu May 09 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.1-1
- version upgrade

* Wed Mar 13 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-9.cvs122
- upgrade to cvs122 to fix upstream bug #2882

* Fri Mar  8 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- require bsfilter in -bsfilter package
- let -fancy obsolete -dillo and -gtkhtml2-viewer packages
- fix minor typos in -dillo Provides and -gdata Group

* Thu Mar 07 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-7.cvs107
- bump to release 7 so new core plugins win EVR against old extra plugins

* Wed Mar 06 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-3.cvs107
- upgrade to latest cvs and integrate plugins from -extra which have been
  moved to the base package
- retire trayicon plugin
- retire dillo plugin

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-1

* Mon Oct 22 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.8.1-3
- fix null-ptr crash (rhbz#862578, CVE-2012-4507)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.8.1-1
- version upgrade

* Sun Jan 22 2012 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.8.0-3
- merge fix for expanded mimeview drag'n'drop (#783399)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.8.0-1
- version upgrade
- cleanup patches
- own plugin include directory in -devel

* Wed Nov 30 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.10-7
- merge fix from 3.7.10cvs47 for odd mimeview_start_drag crash (#748384)
- include built/installed manual and not its XML source
- add scriptlets for icon cache update
- add scriptlets for update-desktop-database (#690298)
- add BR gnome-libs-devel so gnome-config script is available
- drop ancient Obsoletes/Provides
- drop old spec sections not needed anymore

* Fri Nov 25 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.10-6
- fix for new glib2 where only glib.h must be included (#755308)

* Wed Sep 28 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-5
- drop unneeded plugin requires

* Tue Sep 27 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-4
- drop plugin api script

* Mon Sep 26 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-3
- make plugin api isa dependent

* Sun Sep 25 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-2
- change plugin dependencies to depend on plugin api version
  (rhbz#740662)

* Tue Aug 30 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-1
- version upgrade

* Thu Aug 04 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-6
- deprecate gtkhtml2 on f16 upwards

* Tue Jul 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-5
- bump for libetpan soname change

* Thu Jun 09 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-4
- change workaround to fix focus issues (#711257)

* Sat Jun  4 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.9-3
- merge fix for startup notification crash (#708192)

* Mon Apr 11 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-2
- include gnome-shell fix again (3.7.9cvs2)
- move some obsoletes from -plugins to main package
- spec cleanup

* Sun Apr 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-1
- version upgrade

* Sat Apr 09 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-0.3.20110409cvs
- add workaround/fix for hidden window in gnome-shell (#693846)

* Sun Apr 03 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-0.2.20110403cvs
- pull fix for upstream bug #2365

* Tue Mar 29 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-0.1.20110329cvs
- upgrade to cvs snapshot, drop cvs patches
- enhance desktop file to be option for default mailer (#690298)
- cleanup spec file

* Sun Mar 27 2011 Christopher Aillon <caillon@redhat.com> - 3.7.8-7
- Rebuild against NetworkManager 0.9

* Tue Feb 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-6
- fix for possible mouse wheel problems (#661766)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-4
- remove icons fom /usr/share/pixmaps (#673235)
- switch to upstream desktop file

* Sun Jan 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-3
- add plugin dep files to respective plugins (#667377)
- disable dillo on rhel

* Wed Dec 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-2
- retire cachesaver and synce plugins
- unretire clamav plugin now called clamd

* Sat Dec 04 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-1
- version upgrade

* Tue May 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.6-1
- version upgrade
- require pinentry-gui instead of -gtk for more flexibility (#587326)

* Sun Apr 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.5-2
- smime needs pgpcore (#572184)

* Mon Mar 08 2010 Karsten Hopp <karsten@redhat.com> 3.7.5-1.1
- don't buildrequire pilot-link-devel on s390(x)

* Mon Feb 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.5-1
- version upgrade (#562353)

* Fri Jan 08 2010 Kevin Fenzi <kevin@tummy.com> 
- 3.7.4-1

* Wed Nov 25 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.3-2
- fix for crash #537499

* Mon Oct 12 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.3-1
- version upgrade (including gtk 2.18 fixes #527065)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 04 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.2-1
- version upgrade
- drop gssapi patch -> upstream

* Wed Jun 17 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.1-2
- fix gssapi auth (#486422)

* Fri Mar 27 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.1-1
- version upgrade

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.0-1
- version upgrade

* Fri Nov 21 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.6.1-1
- version upgrade
- replace openssl by gnutls
- provide spell checking support via enchant

* Sat Oct 04 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.6.0-1
- version upgrade
- transition smime from claws-mail-plugins to claws-mail package

* Thu Jul 10 2008 Nikolay Vladimirov <nikolay@vladimiroff.com> 
- 3.5.0-2
- rebuild for libetpan

* Mon Jun 30 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.5.0-1
- version upgrade (#453405, #448750)
- completely fix (#449209)
- provide upgrade path from dropped pdf plugin

* Tue Jun 17 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.4.0-2
- rebuild for libetpan
- fix nm support
- fix BR (#449209)

* Wed Apr 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.4.0-1
- version upgrade

* Fri Mar 28 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.1-4
- apply some upstream patches (#439382)
- fix #431735

* Tue Mar 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.1-3
- add obsoletes for deprecated clamav plugin

* Mon Feb 25 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.1-2
- build with NetworkManager support

* Sat Feb 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.1-1
- version upgrade

* Fri Feb 08 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.0-1
- version upgrade
- clamav plugin move to plugins srpm

* Mon Jan 21 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.2.0-3
- bump

* Sun Dec 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.2.0-2
- bump

* Mon Dec 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.2.0-1
- version upgrade

* Sun Dec 09 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.1.0-4
- fix #340871 multilib

* Sat Dec 08 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.1.0-3
- fix desktop file

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 3.1.0-2
- Rebuild for deps

* Mon Nov 19 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.1.0-1
- version upgrade

* Fri Oct 05 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.0.2-1
- version upgrade

* Fri Sep 21 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.0.1-1
- version upgrade

* Mon Sep 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.0.0-1
- version upgrade
- new license tag (upstream switch to GPLv3+)
- fix #254121 (CVE-2007-2958)

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.10.0-4
- new license tag

* Wed Jul 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.10.0-3
- build against libSM (#248675)

* Mon Jul 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.10.0-2
- add requires for bogofilter (#246125)

* Tue Jul 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.10.0-1
- version upgrade
- fix #246230

* Tue May 15 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9.2-1
- version upgrade

* Sat Apr 21 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9.1-1
- version upgrade which fixes CVE-2007-1558 (see #237293)

* Mon Apr 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9.0-1
- version upgrade (should resolve #232675)
- fix BR

* Tue Mar 06 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.8.1-1
- version upgrade

* Sun Mar 04 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.8.0-2
- bump (clamav)

* Tue Feb 27 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.8.0-1
- version upgrade
- fix #228160
- devel subpackage does not require claws-mail anymore
- fix rpath issues
- fix pkg-config file

* Sun Feb 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.7.2-2
- bump

* Wed Feb 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.7.2-1
- version upgrade
- fix #223436
- another try on #221708

* Wed Jan 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.7.1-1
- version upgrade #222279
- fix xface support #221708

* Thu Jan 11 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.7.0-1
- version upgrade

* Fri Dec 22 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.6.1-2
- fix Obsoletes/Requires

* Mon Dec 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.6.1-1
- version upgrade
- package is now named claws-mail instead of sylpheed-claws
- fix #218190, #218187

* Mon Nov 06 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.6.0-1
- version upgrade

* Thu Oct 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.6-1
- version upgrade

* Thu Oct 12 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.5-1
- version upgrade

* Sat Oct 07 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.3-1
- version upgrade

* Wed Sep 27 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.2-1
- version upgrade

* Tue Sep 26 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.1-1
- version upgrade
- should fix (#204340)

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.4.0-2
- FE6 rebuild

* Mon Jul 31 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.4.0-1
- version upgrade

* Mon Jun 26 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.3.1-1
- version upgrade

* Mon Jun 12 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.3.0-1
- version upgrade

* Fri Jun 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.2.3-1
- version upgrade

* Mon Jun 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.2.1-1
- version upgrade

* Mon May 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.2.0-1
- version upgrade

* Sat Apr 22 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.1.1-1
- split plugins from main package to ease requirements (#189113)
- version upgrade (#183357)
- fix libpisock (#189585)

* Wed Apr 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.1.0-1
- version upgrade

* Fri Mar 31 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-4
- #187383: add BR libgnomeprintui22-devel

* Thu Mar 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-3
- Fix .desktop 

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-2
- Rebuild for Fedora Extras 5

* Fri Feb 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-1
- version upgrade
- fix summary

* Wed Jan 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-0.rc4
- version upgrade

* Mon Jan 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-0.rc3
- version upgrade

* Sun Dec 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-0.rc2
- version upgrade

* Sun Dec 04 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-0.rc1
- version upgrade

* Mon Nov 21 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.100-2
- drop program suffix (causes sylpheed-claws-claws bin)

* Thu Nov 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.100-1
- version upgrade

* Sat Oct 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.15-1
- version upgrade

* Fri Sep 09 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.14-1
- version upgrade

* Mon Aug 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-4
- fix files

* Mon Aug 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-3
- add gmp-devel BR

* Mon Aug 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-2
- add bzip2-devel BR

* Sun Jul 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-1
- upgrade
- switch s/gpgme03/gpgme/
- need libetpan

* Thu Jul 07 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.12-2
- add some doc
- fix pixmap installation

* Wed Jul 06 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.12-1
- version upgrade
- add dist tag

* Thu May 26 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.11-1
- change to gtk2 version

* Thu Apr 14 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.4-2
- minor cleanups
- remove aspell version check

* Thu Mar 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.4-1
- Version upgrade

* Wed Mar 23 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.3-1
- Version upgrade

* Fri Mar 18 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.0.1-3
- Don't include static libs in plugin directory.
- Set --with-gpgme-prefix to use relocated gpgme03 package contents.
- BR startup-notification-devel

* Sat Mar 05 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0.1-2
- fixed some sylpheed/sylpheed-claws
- removed Conflictes sylpheed

* Wed Feb 09 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:1.0.1-1
- version upgrade
- cleaned up BuildRequires/Requires and configure options

* Tue Dec 21 2004 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.13-1
- version upgrade
- remove old configure options for GnuPG support (moved to a new plugin now)
- enable new pgpmime-plugin

* Tue Jul 20 2004 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.12-1
- version upgrade
- lots of s/sylpheed/sylpheed-claws/

* Mon May 31 2004 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.11-0.fdr.1
- version upgrade

* Tue Mar 09 2004 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.10-0.fdr.1
- new upstream version

* Fri Feb 13 2004 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.9-0.fdr.1
- version upgrade
* Thu Jan 01 2004 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.8-0.fdr.1
- version upgrade

* Thu Dec 18 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.7-0.fdr.2
- added missing defattr to devel rpm (fixes pending issue)

* Thu Nov 27 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.7-0.fdr.1
- version upgrade

* Wed Oct 08 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.6-0.fdr.8
- version upgrade

* Tue Sep 16 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.5-0.fdr.7
- minor fixes (see #545 #2{1,2})

* Mon Sep 15 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.5-0.fdr.6
- added specfile changes provided by Michael Schwendt
- made aspell-devel conditional severn only

* Fri Sep 12 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.5-0.fdr.5
- version upgrade (thus devel package)
- readded aspell-devel (still only works for > severn but 'a nice to have')

* Sat Aug 30 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.4-0.fdr.4
- reintroduced --enable-aspell without BuildRequires so that it will work in
  severn and just be ignored on > shrike
- changed openssl cflags (now via pkg-config)

* Wed Aug 06 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.4-0.fdr.3
- upgrade to new version
- no aspell support till version >= 0.5.0 is aviable

* Sat Aug 02 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.3-0.fdr.2
- Added BuildRequires openldap-devel, pilot-link-devel
- Excluded static archives
- Changed desktop file

* Fri Aug 01 2003 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:0.9.3-0.fdr.1
- Initial RPM release.
