%global _legacy_common_support 1

%global commit e58ce7463bc8829c46bcba52e8232f550e49c17c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210418
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url https://github.com/Wiimm/%{name}

Name:           wiimms-iso-tools
Version:        3.04a
Release:        1%{?gver}%{?dist}
Summary:        Tools to manipulate Wii and GameCube ISO images

License:        GPLv2+
URL:            http://wit.wiimm.de/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://download.wiimm.de/source/%{name}/%{name}.source-%{version}.txz
%endif
Source2:        wit.1

# Patches from Debian, fixes license issues too
Patch0:         0001-Use-system-libraries.patch
Patch1:         fix-usr-local.patch
Patch2:         0001-Disable-SUPPORT_USER_BIN-support.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  mhash-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(zlib)
Requires:       coreutils
Requires:       fuse
Requires:       wget

Provides:       wit = %{version}-%{release}

Conflicts:      wiimms-iso-tools <= 20170107

%description
Wiimms ISO Tools is a set of command line tools to manipulate Wii and GameCube
ISO images and WBFS containers.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}.source-%{version} -p1
%endif

rm -rf project/src/{libbz2,crypto} setup/*.exe

sed -e 's/\r//' -i project/templates/*.txt

sed \
  -e 's,^#!/usr/bin/env bash,#!/usr/bin/bash,' \
  -e '/^BASE_PATH=/d' \
  -e 's|@@SHARE-PATH@@|%{_datadir}/wit|g' \
  -e '/^SHARE_DIR=/s|\./share|"/tmp"|' \
  -i project/setup/load-titles.sh

sed -e 's|/usr/local|/usr|g' -i project/setup.sh

sed -i \
  -e 's|$(PRE)strip|/bin/true|g' \
  -e "s|-static-libgcc|%{build_ldflags} -Wl,-z,noexecstack|g" \
  -e "/CFLAGS/s|-O3|%{build_cflags}|g" \
  -e 's|^doc: $(MAIN_TOOLS)|doc:|g' \
  -e 's|@$(CC)|$(CC)|g' \
  -e 's|@if|if|g' \
  -e 's|@mkdir|mkdir|g' \
  -e '/Makefile\.local\./d' \
  project/Makefile

%build
%make_build -C project INSTALL_PATH=%{_prefix} HAVE_ZLIB=1
%make_build -C project doc

%install
mkdir -p %{buildroot}%{_bindir}
for i in wit wwt wdf wfuse ;do
  install -pm0755 project/${i} %{buildroot}%{_bindir}/
done

for i in wdf-cat wdf-dump ;do
  ln -sf wdf %{buildroot}%{_bindir}/${i}
done

mkdir -p %{buildroot}%{_datadir}/wit
install -pm0644 project/share/*.txt %{buildroot}%{_datadir}/wit/
install -pm0755 project/load-titles.sh %{buildroot}%{_datadir}/wit/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 %{S:2} %{buildroot}%{_mandir}/man1/wit.1

for i in wdf  wdf-cat  wdf-dump  wfuse  wwt ;do
  echo '.so man1/wit.1' > %{buildroot}%{_mandir}/man1/$i.1
done


%files
%license project/gpl-2.0.txt
%doc project/doc/*.txt
%{_bindir}/*
%{_datadir}/wit
%{_mandir}/man1/*.1*


%changelog
* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 3.04a-1.20210418gite58ce74
- 3.04a

* Fri Aug 14 2020 Phantom X <megaphantomx at hotmail dot com> - 3.03a-1.20200803gitfb217fb
- 3.03a

* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.02a-4
- Fix missing manpages redirects

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
