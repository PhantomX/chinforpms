%global revision 7343
%global date 20170105

Name:           wiimms-iso-tools
Version:        2.40a
Release:        2.%{date}svn%{revision}%{?dist}
Summary:        Tools to manipulate Wii and GameCube ISO images

License:        GPLv2
URL:            http://wit.wiimm.de/
# Get with snap=date|rev=revision ./wiimms-iso-tools-snapshot.sh
Source0:        %{name}-%{revision}.tar.xz
Source1:        wiimms-iso-tools-snapshot.sh

BuildRequires:  execstack
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(zlib)
Requires:       fuse

Provides:       wit = %{version}-%{release}
Provides:       bundled(bzip2) = 1.0.6

Conflicts:      wiimms-iso-tools <= 20170107

%description
Wiimms ISO Tools is a set of command line tools to manipulate Wii and GameCube
ISO images and WBFS containers.

%prep
%autosetup -n %{name}-%{revision}

sed -e 's/\r//' -i templates/*.txt

sed -e 's,^#!/usr/bin/env bash,#!/usr/bin/bash,' -i setup/load-titles.sh


sed -e 's|/usr/local|/usr|g' -i setup.sh

sed -i \
  -e 's|$(PRE)strip|/bin/true|g' \
  -e "s|-static-libgcc|%{__global_ldflags}|g" \
  -e "/CFLAGS/s|-O3|%{optflags}|g" \
  -e 's|^doc: $(MAIN_TOOLS)|doc:|g' \
  Makefile

%build
%make_build
%make_build doc

%install
execstack -c wit wwt wdf wfuse

mkdir -p %{buildroot}%{_bindir}
install -pm0755 wit wwt wdf wfuse %{buildroot}%{_bindir}/

for i in wdf-cat wdf-dump ;do
  ln -sf wdf %{buildroot}%{_bindir}/${i}
done

mkdir -p %{buildroot}%{_datadir}/wit
install -pm0644 share/*.txt %{buildroot}%{_datadir}/wit/
install -pm0755 load-titles.sh %{buildroot}%{_datadir}/wit/

%files
%license gpl-2.0.txt
%doc doc/*.txt
%{_bindir}/*
%{_datadir}/wit


%changelog
* Sat Jun 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.40a-1.20170105svn7343
- New snapshot

* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.40a-1.20170105svn7340
- Update to last snapshot
- New version notation
- Remove execstacks

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170107-1
- Initial spec.
