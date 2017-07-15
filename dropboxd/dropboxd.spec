%global debug_package %{nil}
%global __strip /bin/true

%global pkgname dropbox
%global progdir %{_libdir}/%{pkgname}

%ifarch x86_64
%global parch x86_64
%else
%global parch x86
%endif

# Do no blame Dropbox devs if setting 1 in these
# Set to 1 to use system libs
%global bzip2   1
%global popt    1
%global python  0

Name:           dropboxd
Version:        30.4.22
Release:        1%{?dist}
Summary:        Dropbox proprietary client

License:        Proprietary
URL:            http://www.getdropbox.com/
Source0:        http://www.dropbox.com/download?plat=lnx.%{parch}#/%{pkgname}-lnx.%{parch}-%{version}.tar.gz

ExclusiveArch:  %{ix86} x86_64

AutoReqProv:    no

%if 0%{?bzip2}
BuildRequires:  bzip2-libs%{?_isa}
Requires:       bzip2-libs%{?_isa}
%endif
BuildRequires:  gawk
%if 0%{?popt}
BuildRequires:  popt%{?_isa}
Requires:       popt%{?_isa}
%endif
BuildRequires:  perl
%if 0%{?python}
BuildRequires:  python2%{?_isa}
Requires:       python2%{?_isa}
%endif
Requires:       dbus-libs%{?_isa}
Requires:       freetype%{?_isa}
Requires:       fontconfig%{?_isa}
Requires:       glib2%{?_isa}
Requires:       libffi%{?_isa}
Requires:       libstdc++%{?_isa}
Requires:       libxcb%{?_isa}
Requires:       libxml2%{?_isa}
Requires:       libxslt%{?_isa}
Requires:       libICE%{?_isa}
Requires:       libSM%{?_isa}
Requires:       libX11%{?_isa}
Requires:       libXcomposite%{?_isa}
Requires:       libXext%{?_isa}
Requires:       libXrender%{?_isa}
Requires:       mesa-libGL%{?_isa}
Requires:       ncurses-compat-libs%{?_isa}
Requires:       wmctrl%{?_isa}
Requires:       zlib%{?_isa}

%description
Dropbox backup, storage, access, sharing tool proprietary client.

%prep
%autosetup -c

mv .%{pkgname}-dist %{pkgname}

RVER="$( cat %{pkgname}/VERSION 2> /dev/null | head -n 1 )"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch"
  echo "You have ${RVER} in %{SOURCE0} instead %{version} "
  echo "Edit Version and try again"
  exit 1
fi

rm -fv %{pkgname}/*/lib{dbus*,drm,ffi,GL,stdc++,X11-xcb,z}.so*

mv %{pkgname}/%{pkgname}-lnx.%{parch}-%{version}/ACKNOWLEDGEMENTS .
mv %{pkgname}/%{pkgname}-lnx.%{parch}-%{version}/README README.orig
cp -p README.orig README
sed -e 's|~/.dropbox-dist|%{progdir}|g' -i README
touch -r README.orig README

%build

%install

mkdir -p %{buildroot}%{progdir}

mv %{pkgname}/%{pkgname}-lnx.%{parch}-%{version}/* %{buildroot}%{progdir}/


abs2rel(){
  perl -e 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])' "$1" "$2"
}

xtcsoname(){
  objdump -p "${1}" | grep SONAME | awk '{print $2}'
}

missing(){
  if ! [ -e "$1" ] ;then
    echo "File $1 is missing!"
    exit 5
  fi
}

# bzip2
%if 0%{?bzip2}
  pushd %{buildroot}%{progdir}
    for file in libbz2*.so* ;do
      SONAME=$(xtcsoname ${file})
      missing %{_libdir}/${SONAME}
      rm -fv ${file}
    done
  popd
%endif

# popt
%if 0%{?popt}
  pushd %{buildroot}%{progdir}
    for file in libpopt*.so* ;do
      SONAME=$(xtcsoname ${file})
      missing %{_libdir}/${SONAME}
      rm -fv ${file}
    done
  popd
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

reldir=$(abs2rel %{_bindir} %{progdir})
ln -sf ${reldir}/wmctrl %{buildroot}%{progdir}/wmctrl

cat > %{buildroot}%{progdir}/dropboxd <<'EOF'
#!/bin/sh
PAR=%{progdir}
exec "${PAR}/dropbox" "$@"
EOF
chmod 0755 %{buildroot}%{progdir}/dropboxd

%files
%license ACKNOWLEDGEMENTS
%doc README
%{progdir}


%changelog
* Sat Jul 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 30.4.22-1
- 30.4.22

* Fri Jun 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 28.4.14-1
- 28.4.14

* Thu May 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 26.4.24-1
- 26.4.24

* Tue May 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 25.4.28-1
- 25.4.28

* Tue Apr 11 2017 Phantom X <megaphantomx at bol dot com dot br> - 23.4.18-1
- 23.4.18

* Sat Feb 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 19.4.13-1
- 19.4.13

* Thu Jan 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 18.4.32-1
- 18.4.32
- Added %%{_isa} to requires

* Mon Jan  9 2017 Phantom X <megaphantomx at bol dot com dot br> - 17.4.33-1
- Initial spec.
