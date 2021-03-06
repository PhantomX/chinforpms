
%bcond_with nautilus

%if %{without nautilus}
%define debug_package %{nil}
%endif

Name:           nautilus-dropbox
Epoch:          2
Version:        2015.10.28
Release:        1%{?dist}
Summary:        Dropbox extension for Nautilus
License:        GPLv3+
URL:            https://www.dropbox.com
Source:         https://linux.dropbox.com/packages/%{name}-%{version}.tar.bz2

# add 10 second delay to autostart to ensure it loads on session startup
Patch0:         add_startup_delay.patch

Patch1:         %{name}-1.4.0-system-daemon.patch
Patch2:         %{name}-1.4.0-nognome.patch

ExclusiveArch:  i686 x86_64

BuildRequires:  desktop-file-utils
%if %{with nautilus}
BuildRequires: nautilus-devel
%endif
BuildRequires:  python-docutils
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pygobject2-devel
BuildRequires:  pygtk2-devel
Requires:       dropbox >= %{?epoch}:%{version}-%{release}
Requires:       hicolor-icon-theme

%description
Dropbox extension for nautilus file manager

%package -n dropbox
Summary:        Client for Linux
BuildArch:      noarch
Requires:       dropboxd
Requires:       pygtk2
Requires:       hicolor-icon-theme

%description -n dropbox
Dropbox allows you to sync your files online and across
your computers automatically.


%prep
%setup -q
%patch0 -p1
%patch1 -p0
%if %{without nautilus}
%patch2 -p1
%endif

mv ChangeLog ChangeLog.orig
head -n 1000 ChangeLog.orig > ChangeLog
touch -r ChangeLog.orig ChangeLog

sed -e 's|_LIBDIR_|%{_libdir}|g' -i dropbox.in

%if %{without nautilus}
autoreconf -ivf
%endif

%build
%configure \
  --disable-static \
  --disable-silent-rules

%make_build

%install
%make_install

%if %{with nautilus}
find %{buildroot}%{_libdir} -type f -name '*.la' -delete -print
%endif

desktop-file-validate %{buildroot}%{_datadir}/applications/dropbox.desktop


%files -n dropbox
%license COPYING
%doc ChangeLog README
%{_bindir}/dropbox
%{_datadir}/nautilus-dropbox/
%{_datadir}/icons/hicolor/*
%{_mandir}/man1/dropbox.1.gz
%{_datadir}/applications/dropbox.desktop

%if %{with nautilus}
%files
%{_libdir}/nautilus/extensions-3.0/libnautilus-dropbox.so
%endif

%changelog
* Mon Jan 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2:2015.10.28-1
- Optional nautilus support.
- System dropbox (R: dropboxd)

* Mon Aug 08 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:2015.10.28-1
- Updated to 2015.10.28

* Sun May 31 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.10.0-3
- add 10 second delay to autostart to ensure it loads on session startup

* Wed Jan 07 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.10.0-2
- add ExclusiveArch

* Tue Dec 16 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.10.0-1
- first build


