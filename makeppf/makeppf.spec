Name:           makeppf
Version:        3.0
Release:        1%{?dist}
Summary:        PPF (Playstation Patch File) v3.0 creation tool

License:        LicenseRef-Fedora-Public-Domain
URL:            http://ftp.netbsd.org/pub/pkgsrc/current/pkgsrc/emulators/applyppf/

Source0:        http://ftp.netbsd.org/pub/pkgsrc/distfiles/%{name}3_src.zip
Source1:        README

BuildRequires:  gcc
BuildRequires:  unzip


%description
PPF (PlayStation Patch File) is a tool dedicated to all PlayStation coders and
developers out there who are creating PAL/NTSC patches, trainer options and even
cracks for your favourite console system. With the files in the PPF package you
are in the position to make patchfiles similar to IPS on SuperNES.

This package contains a tool to create PPF patches.


%prep
%autosetup -c

cp %{S:1} .


%build
$CC $CFLAGS \
  -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE \
  $LDFLAGS \
  %{name}3_linux.c -o %{name}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

%files
%doc README
%{_bindir}/%{name}


%changelog
* Tue Jun 01 2021 Phantom X <megaphantomx at hotmail dot com> - 3.0-1
- Initial spec
