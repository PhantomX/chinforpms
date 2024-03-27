%global commit ab0e989499d96c6351ede4adcd086418802ab6e4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240326
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname DiscImageCreator

Name:           discimagecreator
Version:        20240101
Release:        1%{?dist}
Summary:        Disc and disk image creation tool 

License:        Apache-2.0

URL:            https://github.com/saramibreak/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-rpm-build-fixes.patch


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(tinyxml2)
Requires:       eccedc

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{pkgname} dumps a disc (CD, GD, DVD, HD-DVD, BD, GC/Wii, XBOX, XBOX 360) and
disk (Floppy, MO, USB etc).
CD and GD, it can dump considering a drive + CD (=combined) offset.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

rm -f Release_ANSI/E_WISE*
rm -f Release_ANSI/*.exe
rm -f %{pkgname}/_external/tinyxml2.*

mv "Release_ANSI/Doc/Firmware&Tool.md" Release_ANSI/Doc/Firmware_and_Tool.md

sed -e 's/\r//' -i Release_ANSI/Doc/*.txt Release_ANSI/*.{dat,txt}

find %{pkgname} -type f \( -name '*.c*' -o -name '*.h*' \) -exec sed -e 's/\r//' -i {} ';'

sed -e 's|-O2||g' -i %{pkgname}/makefile

sed \
  -e 's|_RPM_BIN_DIR_|%{_bindir}|g' \
  -i %{pkgname}/get.cpp

%build
%make_build -C %{pkgname}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{pkgname}/%{pkgname} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{pkgname}
install -pm0644 Release_ANSI/*.{dat,txt}  %{buildroot}%{_datadir}/%{pkgname}/


%files
%license LICENSE
%doc README.md Release_ANSI/Doc/{KnownIssue,TestedDrive}.txt Release_ANSI/Doc/Firmware_and_Tool.md
%{_bindir}/%{pkgname}
%{_datadir}/%{pkgname}/


%changelog
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 20240101-1
- 20240101

* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 20230909-1
- 20230909

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 20220909-1.202209013gitbb05d98
- 20220909

* Mon Jul 04 2022 Phantom X <megaphantomx at hotmail dot com> - 20220606-1.20220626gitf6ac92b
- 20220606

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 20220301-1
- 20220301

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 20210701-1.20210916git32007ef
- 20210701

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 20210401-1
- 20210401

* Tue Aug 11 2020 Phantom X <megaphantomx at hotmail dot com> - 20200716-1.20200807git953075a
- Initial spec
