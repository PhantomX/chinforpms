# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global pkgname spideroak
%global pkgname1 SpiderOakONE
%global pkgrel 1

%global progdir %{_libdir}/%{pkgname1}

%global parch x86_64
%global larch x64

# Do no blame SpiderOak devs if setting 1 in these
# Set to 1 to use system libs
%global with_dbusmenuqt 0
%global with_ffi 0
%global with_python 0
%if 0%{?with_python}
%global with_curl 0
%global with_pillow 0
%global with_pyqt 0
%endif

Name:           spideroakone
Version:        7.5.0
Release:        12%{?dist}
Summary:        Online backup, storage, access, sharing tool
Epoch:          3

License:        Proprietary
URL:            https://spideroak.com/
Source0:        https://spideroak.com/release/spideroak/rpm_%{larch}#/%{pkgname1}.%{version}.%{pkgrel}.%{parch}.rpm

ExclusiveArch:  x86_64

BuildRequires:  binutils
BuildRequires:  patchelf
BuildRequires:  systemd
BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
%if 0%{?with_curl}
BuildRequires:  libcurl%{?_isa}
BuildRequires:  python2-pycurl%{?_isa}
Requires:       libcurl%{?_isa}
Requires:       python2-pycurl%{?_isa}
%endif
%if 0%{?with_dbusmenuqt}
BuildRequires:  dbusmenu-qt%{?_isa}
%endif
%if 0%{?with_ffi}
BuildRequires:  libffi%{?_isa}
%endif
%if 0%{?with_python}
BuildRequires:  python2-rpm-macros
BuildRequires:  python2.7%{?_isa}
Requires:       python2.7%{?_isa}
%endif
%if 0%{?with_pillow}
BuildRequires:  python2-pillow%{?_isa}
Requires:       python2-pillow%{?_isa}
%endif
%if 0%{?with_pyqt}
BuildRequires:  qt4%{?_isa}
BuildRequires:  PyQt4%{?_isa}
BuildRequires:  python2-sip%{?_isa}
Requires:       qt4%{?_isa}
Requires:       PyQt4%{?_isa}
Requires:       python2-sip%{?_isa}
%endif

Requires:       sqlite-libs%{?_isa}

Requires:       hicolor-icon-theme

Provides:       bundled(libssl) = 1.0.0

Conflicts:       SpiderOak < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       SpiderOak = %{version}-%{release}

%global __provides_exclude_from ^%{progdir}/.*

%global __requires_exclude ^libssl\\.so.*$
%global __requires_exclude %__requires_exclude|^libcrypto\\.so.*$
%global __requires_exclude %__requires_exclude|^libgmp\\.so.*$
%global __requires_exclude %__requires_exclude|^libpng12\\.so.*$
%if !0%{?with_curl}
%global __requires_exclude %__requires_exclude|^libcurl\\.so.*$
%endif
%if !0%{?with_dbusmenuqt}
%global __requires_exclude %__requires_exclude|^libdbusmenu-qt\\.so.*$
%endif
%if !0%{?with_ffi}
%global __requires_exclude %__requires_exclude|^libffi\\.so.*$
%endif
%if !0%{?with_pyqt}
%global __requires_exclude %__requires_exclude|^libQt.*\\.so.*$
%global __requires_exclude %__requires_exclude|^PyQt4.Qt.*\\.so.*$
%endif

%description
SpiderOak provides an easy, secure and consolidated online backup, storage,
access, sharing & tool.

%prep

RVER="$(rpm -qp --qf %%{version} %{SOURCE0} 2> /dev/null)"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch"
  echo "You have ${RVER} in %{SOURCE0} instead %{version} "
  echo "Edit VERSION variable and try again"
  exit 1
fi

%setup -c -T
rpm2cpio %{SOURCE0} | cpio -imdv

mv usr/share/pixmaps/%{pkgname1}.png usr/share/pixmaps/%{name}.png
mv usr/share/applications/%{pkgname1}.desktop usr/share/applications/%{name}.desktop

sed -i -e "s|/opt/%{pkgname1}/lib|%{progdir}|g" usr/bin/%{pkgname1}

find opt/%{pkgname1}/lib/ -name '*.so*' | xargs chmod 0755

%build

%install

mkdir -p %{buildroot}%{progdir}

mv opt/%{pkgname1}/lib/* %{buildroot}%{progdir}

rm -fv %{buildroot}%{progdir}/lib{gcc_s,stdc++,z}.so.*
rm -fv %{buildroot}%{progdir}/libgssapi_krb5.so.*
rm -fv %{buildroot}%{progdir}/libsepol.so.*
rm -fv %{buildroot}%{progdir}/libsqlite3.so.*
rm -fv %{buildroot}%{progdir}/*/*/*.exe

abs2rel(){
  realpath -m --relative-to="$2" "$1"
}

missing(){
  if ! [ -e "$1" ] ;then
    echo "File $1 is missing!"
    exit 5
  fi
}

xtcsoname(){
  objdump -p "${1}" | grep SONAME | awk '{print $2}'
}

# curl
%if 0%{?with_curl}
  reldir=$(abs2rel %{python2_sitearch} %{progdir})
  missing %{python2_sitearch}/pycurl.so
  rm -f %{buildroot}%{progdir}/pycurl.so
  ln -sf ${reldir}/pycurl.so %{buildroot}%{progdir}/pycurl.so
  rm -fv %{buildroot}%{progdir}/libcurl.so.*
  rm -fv %{buildroot}%{progdir}/libssh2.so.*
%endif

%if 0%{?with_dbusmenuqt}
  ( cd %{buildroot}%{progdir}
    for file in libdbusmenu-qt.so* ;do
      SONAME=$(xtcsoname ${file})
      missing %{_libdir}/${SONAME}
      rm -fv ${file}
    done
  ) || exit $?
%endif

%if 0%{?with_ffi}
  ( cd %{buildroot}%{progdir}
    for file in libffi*.so* ;do
      SONAME=$(xtcsoname ${file})
      missing %{_libdir}/${SONAME}
      rm -fv ${file}
    done
  ) || exit $?
%endif

# python
%if 0%{?with_python}
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
  done
%endif

%if 0%{?with_pillow}
  reldir=$(abs2rel %{python2_sitearch}/PIL %{progdir})
  missing %{python2_sitearch}/PIL/_imaging.so
  rm -fv %{buildroot}%{progdir}/PIL._imaging.so
  ln -sf ${reldir}/_imaging.so %{buildroot}%{progdir}/PIL._imaging.so
%endif

%if 0%{?with_pyqt}
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

mkdir -p %{buildroot}%{_sysctldir}
cat > %{buildroot}%{_sysctldir}/30-spideroak.conf <<'EOF'
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
  magick usr/share/pixmaps/%{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done


%files
%license usr/share/doc/%{pkgname1}/copyright
%{_bindir}/%{pkgname1}
%{progdir}
%{_sysctldir}/30-spideroak.conf
%{_mandir}/man1/%{pkgname1}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_datadir}/pixmaps/*.png


%changelog
* Mon Apr 15 2024 - 3:7.5.0-12
- Add missing __requires_exclude

* Thu Mar 16 2023 - 3:7.5.0-11
- Fix python switch

* Wed Mar 30 2022 - 3:7.5.0-10
- with_ffi 0

* Fri Nov 06 2020 - 3:7.5.0-9
- with_python 0

* Wed Sep 30 2020 - 3:7.5.0-8
- python2.7

* Fri Mar 20 2020 - 3:7.5.0-7
- with_pillow 0

* Thu Mar 19 2020 - 3:7.5.0-6
- with_curl 0

* Tue Oct 08 2019 - 3:7.5.0-5
- with_dbusmenuqt 0

* Tue Sep 24 2019 - 3:7.5.0-4
- with_python 0

* Thu Sep 19 2019 - 3:7.5.0-4
- Update python2 requirements for Fedora 31 for real

* Wed Sep 18 2019 - 3:7.5.0-3
- Update python2 requirements for Fedora 31

* Mon Aug 26 2019 - 3:7.5.0-2
- Fix requires

* Tue Mar 05 2019 - 3:7.5.0-1
- 7.5.0

* Tue Dec 25 2018 - 3:7.4.0-1
- 7.4.0

* Fri Sep 14 2018 - 3:7.3.0-1
- 7.3.0
- Only x86_64 now

* Sat Jun 23 2018 - 3:7.2.0-1
- 7.2.0

* Sat Apr 28 2018 - 3:7.1.0-1
- 7.1.0

* Thu Feb 08 2018 - 3:7.0.1-1
- 7.0.1

* Sun Jan 21 2018 - 3:7.0.0-1
- 7.0.0

* Sun Oct 15 2017 - 3:6.4.0-2
- Exclude libpng12 provides

* Fri Oct 13 2017 - 3:6.4.0-1
- 6.4.0

* Thu Sep 14 2017 - 3:6.3.1-2
- Exclude provides
- Remove sqlite bundled library

* Sat Aug 05 2017 - 3:6.3.1-1
- 6.3.1
- R: libffi

* Tue Jun 06 2017 - 3:6.3.0-1
- 6.3.0

* Tue May 09 2017 - 3:6.2.0-1
- 6.2.0

* Wed Apr 05 2017 - 3:6.1.9-1
- 6.1.9

* Thu Jan 26 2017 - 3:6.1.5-2
- Added %%{_isa} to requires

* Wed Dec 28 2016 - 3:6.1.5-1
- Initial spec
