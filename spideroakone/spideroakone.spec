%global debug_package %{nil}
%global __strip /bin/true

%global pkgname spideroak
%global pkgname1 SpiderOakONE
%global pkgrel 1

%global progdir %{_libdir}/%{pkgname1}

%ifarch x86_64
%global parch x86_64
%global larch x64
%else
%global parch i386
%global larch x86
%endif

# Do no blame SpiderOak devs if setting YES in these
# Set to 1 to use system libs
%global curl 1
%global dbusmenuqt 1
%global python 0
%global pillow 1
%global pyqt 0

Name:           spideroakone
Version:        6.3.0
Release:        1%{?dist}
Summary:        Online backup, storage, access, sharing tool
Epoch:          3

License:        Proprietary
URL:            https://spideroak.com/
Source0:        https://spideroak.com/release/spideroak/rpm_%{larch}#/%{pkgname}.%{version}.%{pkgrel}.%{parch}.rpm

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  binutils patchelf perl python2-rpm-macros ImageMagick
BuildRequires:  desktop-file-utils
%if 0%{?curl}
BuildRequires:  libcurl%{?_isa}
BuildRequires:  python-pycurl%{?_isa}
Requires:       libcurl%{?_isa}
Requires:       python-pycurl%{?_isa}
%endif
%if 0%{?dbusmenuqt}
BuildRequires:  dbusmenu-qt%{?_isa}
%endif
%if 0%{?python}
BuildRequires:  python2%{?_isa}
Requires:       python2%{?_isa}
%endif
%if 0%{?pillow}
BuildRequires:  python2-pillow%{?_isa}
Requires:       python2-pillow%{?_isa}
%endif
%if 0%{?pyopenssl}
BuildRequires:  pyOpenSSL
Requires:       pyOpenSSL
%endif
%if 0%{?pyqt}
BuildRequires:  qt%{?_isa}
BuildRequires:  PyQt4%{?_isa}
BuildRequires:  sip%{?_isa}
Requires:       qt%{?_isa}
Requires:       PyQt4%{?_isa}
Requires:       sip%{?_isa}
%endif

Requires:       sqlite-libs%{?_isa}

Requires:       hicolor-icon-theme

Conflicts:       SpiderOak < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       SpiderOak

%description
SpiderOak provides an easy, secure and consolidated online backup, storage,
access, sharing & tool.

%prep

RVER="$(rpm -qp --qf %{version} %{SOURCE0} 2> /dev/null)"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch"
  echo "You have ${RVER} in %{SOURCE0} instead %{version} "
  echo "Edit VERSION variable and try again"
  exit 1
fi

%setup -c -T
rpm2cpio %{SOURCE0} | cpio -imdv --no-absolute-filenames

mv usr/share/pixmaps/%{pkgname1}.png usr/share/pixmaps/%{name}.png
mv usr/share/applications/%{pkgname1}.desktop usr/share/applications/%{name}.desktop

sed -i -e "s|/opt/%{pkgname1}/lib|%{progdir}|g" usr/bin/%{pkgname1}

%build

%install

mkdir -p %{buildroot}%{progdir}

mv opt/%{pkgname1}/lib/* %{buildroot}%{progdir}

rm -fv %{buildroot}%{progdir}/lib{gcc_s,stdc++,z}.so.*
rm -fv %{buildroot}%{progdir}/libgssapi_krb5.so.*
rm -fv %{buildroot}%{progdir}/libsepol.so.*
rm -fv %{buildroot}%{progdir}/*/*/*.exe

#( cd %{buildroot}%{progdir}
#  # https://bugs.gentoo.org/show_bug.cgi?id=400979
#  for x in $(find) ; do
#    # Use \x7fELF header to separate ELF executables and libraries
#    [[ -f ${x} && $(od -t x1 -N 4 "${x}") == *"7f 45 4c 46"* ]] || continue
#    patchelf --set-rpath '$ORIGIN' "${x}"
#  done
#)

abs2rel(){
  perl -e 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])' "$1" "$2"
}

missing(){
  if ! [ -e "$1" ] ;then
    echo "File $1 is missing!"
    exit 5
  fi
}

# curl
%if 0%{?curl}
  reldir=$(abs2rel %{python2_sitearch} %{progdir})
  missing %{python2_sitearch}/pycurl.so
  rm -f %{buildroot}%{progdir}/pycurl.so
  ln -sf ${reldir}/pycurl.so %{buildroot}%{progdir}/pycurl.so
  rm -fv %{buildroot}%{progdir}/libcurl.so.*
  rm -fv %{buildroot}%{progdir}/libssh2.so.*
%endif

%if 0%{?dbusmenuqt}
  ( cd %{buildroot}%{progdir}
    for file in libdbusmenu-qt*.so* ;do
      SONAME=$(xtcsoname ${file})
      missing %{_libdir}/${SONAME}
      rm -fv ${file}
    done
  ) || exit $?
%endif

# python
%if 0%{?python}
  reldir=$(abs2rel %{_libdir}/python%{python2_version}/lib-dynload %{progdir})
  for file in \
    _bisect _collections _functools _locale _multibytecodec _random _socket \
    array fcntl grp itertools mmap parser select strop time zlib
  do
    missing %{_libdir}/python%{python2_version}/lib-dynload/${file}module.so
    ln -sf ${reldir}/${file}.so %{buildroot}%{progdir}/${file}module.so
  done
  for file in \
    _codecs_cn _codecs_hk _codecs_iso2022 _codecs_jp _codecs_kr _codecs_tw \
    _ctypes _csv _hashlib _heapq _hotshot _io _json _lsprof _sqlite3 \
    _ssl _struct binascii bz2 cPickle cStringIO bz2 cPickle cStringIO\
    datetime math operator pyexpat resource termios unicodedata
  do
    missing %{_libdir}/python%{python2_version}/lib-dynload/${file}.so
    rm -fv %{buildroot}%{progdir}/${file}.so
    ln -sf ${reldir}/${file}.so %{buildroot}%{progdir}/${file}.so
    rm -fv %{buildroot}%{progdir}/py
    rm -fv %{buildroot}%{progdir}/libexpat.so.*
    rm -fv %{buildroot}%{progdir}/libsqlite3.so.*
  done
%endif

%if 0%{?pillow}
  reldir=$(abs2rel %{python2_sitearch}/PIL %{progdir})
  missing %{python2_sitearch}/PIL/_imaging.so
  rm -fv %{buildroot}%{progdir}/PIL._imaging.so
  ln -sf ${reldir}/_imaging.so %{buildroot}%{progdir}/PIL._imaging.so
%endif

%if 0%{?pyqt}
  reldir=$(abs2rel %{python2_sitearch} %{progdir})

  missing %{python2_sitearch}/sip.so
  rm -f %{buildroot}%{progdir}/sip.so
  ln -sf ${reldir}/sip.so %{buildroot}%{progdir}/sip.so

  for file in Qt QtCore QtGui QtNetwork ;do
    missing %{python2_sitearch}/PyQt4/${file}.so
    rm -fv %{buildroot}%{progdir}/PyQt4.${file}.so
    ln -sf ${reldir}/PyQt4/${file}.so %{buildroot}%{progdir}/PyQt4.${file}.so
  done
  rm -fv %{buildroot}%{progdir}/lib{Qt,png12}*.so.*
  rm -rfv %{buildroot}%{progdir}/plugins
%endif

mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/bin/%{pkgname1} %{buildroot}%{_bindir}

mkdir -p %{buildroot}/usr/lib/sysctl.d
cat > %{buildroot}/usr/lib/sysctl.d/30-spideroak.conf <<'EOF'
fs.inotify.max_user_watches = 65536
EOF

mkdir -p %{buildroot}%{_mandir}/man1
zcat usr/share/man/man1/%{pkgname1}.1.gz > %{buildroot}%{_mandir}/man1/%{pkgname1}.1

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key="Encoding" \
  --remove-key="Version" \
  --remove-category="SpiderOak" \
  --remove-category="Archiving" \
  --remove-category="Utility" \
  --add-category="Qt" \
  --set-icon="%{name}" \
  --set-key="Exec" \
  --set-value="%{pkgname1}" \
  usr/share/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -pm0644 usr/share/pixmaps/%{name}.png \
  %{buildroot}%{_datadir}/pixmaps/
install -pm0644 usr/share/pixmaps/SpiderOakONEGlobalSync.png \
  %{buildroot}%{_datadir}/pixmaps/

for res in 16 24 32 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert usr/share/pixmaps/%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license usr/share/doc/%{pkgname1}/copyright
%{_bindir}/%{pkgname1}
%{progdir}
/usr/lib/sysctl.d/30-spideroak.conf
%{_mandir}/man1/%{pkgname1}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/pixmaps/*.png

%changelog
* Tue Jun 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 3:6.3.0-1
- 6.3.0

* Tue May 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 3:6.2.0-1
- 6.2.0

* Wed Apr 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 3:6.1.9-1
- 6.1.9

* Thu Jan 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 3:6.1.5-2
- Added %%{_isa} to requires

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 3:6.1.5-1
- Initial spec
