%global commit 5a8fe21730872d67991211f1319c87f0780f2d0f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210401
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname DiscImageCreator

Name:           discimagecreator
Version:        20210401
Release:        1%{?gver}%{?dist}
Summary:        Disc and disk image creation tool 

License:        ASL 2.0

URL:            https://github.com/saramibreak/%{pkgname}

%if 0%{?with_snapshot}
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
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

rm -f Release_ANSI/E_WISE*
rm -f Release_ANSI/*.exe
rm -f %{pkgname}/_external/tinyxml2.*

mv "Release_ANSI/Doc/Firmware&Tool.md" Release_ANSI/Doc/Firmware_and_Tool.md

sed -e 's/\r//' -i Release_ANSI/Doc/*.txt Release_ANSI/*.{dat,txt}

find %{pkgname} -type f \( -name "*.cpp" -o -name "*.h" \) -exec sed -e 's/\r//' -i {} ';'

sed -e 's|-O2||g' -i %{pkgname}/makefile

sed \
  -e 's|_RPM_DATA_DIR_|%{_datadir}/%{pkgname}|g' \
  -e 's|_RPM_BIN_DIR_|%{_bindir}|g' \
  -i %{pkgname}/{get,xml}.cpp

%build
%set_build_flags
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
* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 20210401-1
- 20210401

* Tue Aug 11 2020 Phantom X <megaphantomx at hotmail dot com> - 20200716-1.20200807git953075a
- Initial spec
