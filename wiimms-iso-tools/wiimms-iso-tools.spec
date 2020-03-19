%global _legacy_common_support 1

%global revision 7606
%global date 20180923
%global with_snapshot 0

%if 0%{?with_snapshot}
%global svnver .%{date}svn%{revision}
%endif

Name:           wiimms-iso-tools
Version:        3.02a
Release:        3%{?svnver}%{?dist}
Summary:        Tools to manipulate Wii and GameCube ISO images

License:        GPLv2+
URL:            http://wit.wiimm.de/

%if 0%{?with_snapshot}
# Get with snap=date|rev=revision ./wiimms-iso-tools-snapshot.sh
Source0:        %{name}-r%{revision}.tar.xz
%else
Source0:       https://download.wiimm.de/source/%{name}/%{name}.source-%{version}.txz
%endif
Source1:        wiimms-iso-tools-snapshot.sh
Source2:        wit.1

# Patches from Debian, fixes license issues too
Patch0:         use-libbz2-and-mhash.patch
Patch1:         fix-usr-local.patch
Patch2:         0003-Don-t-link-wfuse-against-libdl.patch
Patch3:         0001-Disable-SUPPORT_USER_BIN-support.patch

BuildRequires:  gcc
BuildRequires:  mhash-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(zlib)
Requires:       fuse

Provides:       wit = %{version}-%{release}

Conflicts:      wiimms-iso-tools <= 20170107

%description
Wiimms ISO Tools is a set of command line tools to manipulate Wii and GameCube
ISO images and WBFS containers.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-r%{revision}
%else
%autosetup -n %{name}.source-%{version} -p1
%endif

rm -rf src/{libbz2,crypto} setup/*.exe

sed -e 's/\r//' -i templates/*.txt

sed -e 's,^#!/usr/bin/env bash,#!/usr/bin/bash,' -i setup/load-titles.sh


sed -e 's|/usr/local|/usr|g' -i setup.sh

sed -i \
  -e 's|$(PRE)strip|/bin/true|g' \
  -e "s|-static-libgcc|%{build_ldflags} -Wl,-z,noexecstack|g" \
  -e "/CFLAGS/s|-O3|%{build_cflags}|g" \
  -e 's|^doc: $(MAIN_TOOLS)|doc:|g' \
  -e 's|@$(CC)|$(CC)|g' \
  Makefile

%build
%make_build INSTALL_PATH=%{_prefix} HAVE_ZLIB=1
%make_build doc

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 wit wwt wdf wfuse %{buildroot}%{_bindir}/

for i in wdf-cat wdf-dump ;do
  ln -sf wdf %{buildroot}%{_bindir}/${i}
done

mkdir -p %{buildroot}%{_datadir}/wit
install -pm0644 share/*.txt %{buildroot}%{_datadir}/wit/
install -pm0755 load-titles.sh %{buildroot}%{_datadir}/wit/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 %{S:2} %{buildroot}%{_mandir}/man1/wit.1

for i in wdf  wdf-cat  wdf-dump  wfuse  wwt ;do
  echo '.so man1/wit.1' > $i.1
done


%files
%license gpl-2.0.txt
%doc doc/*.txt
%{_bindir}/*
%{_datadir}/wit
%{_mandir}/man1/*.1*


%changelog
* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.02a-3
- gcc 10 fix

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.02a-2
- Fix GC image conversion crash

* Thu Feb 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.02a-1
- 3.02a final
- Patches and manpage from Debian. Unbundles bzip2 and mhash instead OpenSSL SHA1
- Remove execstack with ldflags instead execstack binary
- Verbose make

* Tue Oct 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.02a-0.1.20180923svn7606
- New snapshot

* Sun Jan 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.01a-1.20171203svn7464
- 3.01a

* Sat Jun 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.40a-1.20170105svn7343
- New snapshot

* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.40a-1.20170105svn7340
- Update to last snapshot
- New version notation
- Remove execstacks

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170107-1
- Initial spec.
