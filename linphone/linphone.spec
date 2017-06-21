%global ffmpeg 0

Name:           linphone
Version:        3.11.1
Release:        1.chinfo%{?dist}
Summary:        Phone anywhere in the whole world by using the Internet

License:        GPLv2+
URL:            http://www.linphone.org/
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

Patch0:         linphone-ui.patch
Patch1:         linphone-pref.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  gettext
BuildRequires:  graphviz
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  desktop-file-utils
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(belle-sip)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libupnp)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(mediastreamer)
BuildRequires:  pkgconfig(ortp)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme
Requires(post): desktop-file-utils
Requires(postun): gtk-update-icon-cache
Requires(posttrans): gtk-update-icon-cache

Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Linphone is mostly sip compliant. It works successfully with these
implementations:
    * eStara softphone (commercial software for windows)
    * Pingtel phones (with DNS enabled and VLAN QOS support disabled).
    * Hotsip, a free of charge phone for Windows.
    * Vocal, an open source SIP stack from Vovida that includes a SIP proxy
        that works with linphone since version 0.7.1.
    * Siproxd is a free sip proxy being developed by Thomas Ries because he
        would like to have linphone working behind his firewall. Siproxd is
        simple to setup and works perfectly with linphone.
    * Partysip aims at being a generic and fully functionnal SIP proxy. Visit
        the web page for more details on its functionalities.

%package libs
Summary:        %{summary}

%description libs
%{summary}.

%package devel
Summary:        Development libraries for linphone
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(mediastreamer)
Obsoletes:      linphone-mediastreamer < %{version}

%description    devel
Libraries and headers required to develop software with linphone.

%prep
%autosetup -p1

intltoolize -f
autoreconf -ivf

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --disable-strict \
  --disable-rpath \
  --enable-external-mediastreamer \
%if !0%{?ffmpeg}
  --disable-ffmpeg \
  --disable-video \
%endif
  --enable-external-ortp \
  --enable-console_ui=yes \
  --enable-gtk_ui=yes \
  --enable-sqlite-storage=yes

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete

rm -f coreapi/help/doc/html/html.tar
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_datadir}/gnome

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}c
%{_bindir}/%{name}csh
%{_bindir}/%{name}-daemon
%{_bindir}/%{name}-daemon-pipetest
%{_bindir}/lp-autoanswer
%{_bindir}/lp-test-ecc
%{_mandir}/man1/*
%{_mandir}/cs/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/audio-assistant.desktop
%{_datadir}/pixmaps/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/sounds/%{name}
%{_datadir}/appdata/%{name}.appdata.xml

%files libs
%{_libdir}/lib%{name}.so.*

%files devel
%doc coreapi/help/doc/html
%{_bindir}/lpc2xml_test
%{_bindir}/xml2lpc_test
%{_bindir}/lp-gen-wrappers
%{_bindir}/lp-sendmsg
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/tutorials/%{name}

%changelog
* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.11.1-1.chinfo
- Initial spec
