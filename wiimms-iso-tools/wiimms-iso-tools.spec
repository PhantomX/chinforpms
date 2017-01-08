Name:           wiimms-iso-tools
Version:        20170107
Release:        1%{?dist}
Summary:        Tools to manipulate Wii and GameCube ISO images

License:        GPLv2
URL:            http://wit.wiimm.de/
# Get with snap=date ./wiimms-iso-tools-snapshot.sh
Source0:        %{name}-%{version}.tar.xz
Source1:        wiimms-iso-tools-snapshot.sh

BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(zlib)
Requires:       fuse

Provides:       bundled(bzip2) = 1.0.6

%description
Wiimms ISO Tools is a set of command line tools to manipulate Wii and GameCube
ISO images and WBFS containers.

%prep
%autosetup

sed -i -e 's|/usr/local|/usr|g' setup.sh || exit 1

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
rm -rf %{buildroot}

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
* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170107-1
- Initial spec.
