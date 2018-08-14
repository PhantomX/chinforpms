Name:           linphone
Version:        3.12.0
Release:        2.chinfo%{?dist}
Summary:        Phone anywhere in the whole world by using the Internet

License:        GPLv2+
URL:            http://www.linphone.org/
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

Patch0:         linphone-ui.patch
Patch1:         linphone-gitversion.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  graphviz
BuildRequires:  desktop-file-utils
BuildRequires:  bcmatroska2-devel
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(belcard)
BuildRequires:  pkgconfig(belr)
BuildRequires:  pkgconfig(belle-sip)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libbzrtp)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(mediastreamer)
BuildRequires:  pkgconfig(ortp)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python2
BuildRequires:  python2-six
BuildRequires:  pystache
Requires:       hicolor-icon-theme

Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:      linphone-mediastreamer < %{version}

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
Provides:       liblinphone = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      liblinphone < %{version}-%{release}

%description libs
%{summary}.

%package devel
Summary:        Development libraries for linphone
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(mediastreamer)
Provides:       liblinphone-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      liblinphone-devel < %{version}-%{release}


%description    devel
Libraries and headers required to develop software with linphone.

%prep
%autosetup -p1

sed \
  -e 's|@prefix@|%{_prefix}|g' \
  -e 's|@exec_prefix@|%{_exec_prefix}|g' \
  -e 's|@includedir@|%{_includedir}|g' \
  -e 's|@libdir@|%{_libdir}|g' \
  -e "s,@VERSION@,$(awk '/%{name} VERSION/{print $3}' CMakeLists.txt),g" \
  -e "s|@LINPHONE_LIBS@|-L%{_libdir} -l%{name}|g" \
  -e "s|@LINPHONE_CFLAGS@|-I%{_includedir} -I%{_includedir}/%{name}|g" \
  share/%{name}.pc.in > %{name}.pc

echo '#define LIBLINPHONE_GIT_VERSION "%{version}-%{release}"' > coreapi/liblinphone_gitversion.h

%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
  -DENABLE_TESTS:BOOL=OFF \
  -DENABLE_STRICT:BOOL=OFF \
  -DENABLE_CONSOLE_UI:BOOL=ON \
  -DENABLE_DAEMON:BOOL=ON \
  -DENABLE_GTK_UI:BOOL=ON \
  -DENABLE_LIME:BOOL=ON \
  -DENABLE_NOTIFY:BOOL=ON \
  -DENABLE_ROOTCA_DOWNLOAD:BOOL=OFF \
  -DENABLE_SQLITE_STORAGE:BOOL=ON \
  -DENABLE_TURORIALS:BOOL=OFF \
  -DENABLE_UPDATE_CHECK:BOOL=OFF \
  -DENABLE_VIDEO:BOOL=ON

%make_build

%install
%make_install -C builddir

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 share/%{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

rm -f %{buildroot}%{_bindir}/buddy_status
rm -f %{buildroot}%{_bindir}/chatroom
rm -f %{buildroot}%{_bindir}/filetransfer
rm -f %{buildroot}%{_bindir}/helloworld
rm -f %{buildroot}%{_bindir}/notify
rm -f %{buildroot}%{_bindir}/realtimetext_*
rm -f %{buildroot}%{_bindir}/registration

rm -f builddir/coreapi/help/doc/html/html.tar
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_datadir}/gnome

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}c
%{_bindir}/%{name}csh
%{_bindir}/%{name}-daemon
%{_bindir}/%{name}-daemon-pipetest
%{_bindir}/lp-auto-answer
%{_bindir}/lp-sendmsg
%{_bindir}/lp-test-ecc
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/audio-assistant.desktop
%{_datadir}/pixmaps/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/sounds/%{name}
%{_metainfodir}/%{name}.appdata.xml

%files libs
%{_libdir}/lib%{name}*.so.*

%files devel
%doc builddir/coreapi/help/doc/doxygen/html
%{_bindir}/lpc2xml_test
%{_bindir}/xml2lpc_test
%{_bindir}/lp-sendmsg
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}++/*.hh
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/Linphone*/cmake/*.cmake

%changelog
* Sat Sep 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.12.0-2.chinfo
- cmake and fixes for it

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.12.0-1.chinfo
- 3.12.0

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.11.1-1.chinfo
- Initial spec
