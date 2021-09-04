%undefine _cmake_shared_libs

%global commit 9514efe4a0a5acfa2a27cc014808d450af653ed2
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210902
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname melonDS
%global vc_url  https://github.com/Arisotura/%{pkgname}

%global fatfs_ver 86631

Name:           melonds
Version:        0.9.3
Release:        1%{?gver}%{?dist}
Summary:        A Nintendo DS emulator

# fatfs - BSD
# sha1-reid - Public Domain
# teakra - MIT
# tiny-AES - Unlicense

License:        GPLv3
URL:            http://melonds.kuribo64.net/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        net.kuribo64.%{pkgname}.metainfo.xml

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Change-savefiles-location.patch

ExclusiveArch:  x86_64 %{ix86} %{arm} aarch64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(slirp)

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  hicolor-icon-theme

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(fatfs_ver) = %{fatfs_ver}
Provides:       bundled(sha1-reid)
Provides:       bundled(teakra) = 0~git
Provides:       bundled(tiny-AES-c)


%description
%{pkgname} is a Nintendo DS emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

cp -p src/fatfs/LICENSE.txt LICENSE.fatfs
cp -p src/teakra/LICENSE LICENSE.teakra
cp -p src/tiny-AES-c/unlicense.txt LICENSE.tiny-AES-c

rm -rf \
  src/frontend/qt_sdl/pcap src/xxhash

sed \
  -e 's|STREQUAL Release|STREQUAL Release_disabled|g' \
  -i CMakeLists.txt

%build
%cmake \
  -DENABLE_LTO:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/net.kuribo64.%{pkgname}.metainfo.xml


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/net.kuribo64.%{pkgname}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/*.metainfo.xml


%files
%doc README.md
%license LICENSE*
%{_bindir}/%{pkgname}
%{_datadir}/applications/net.kuribo64.%{pkgname}.desktop
%{_datadir}/icons/hicolor/*/apps/net.kuribo64.%{pkgname}.*
%{_metainfodir}/*.metainfo.xml


%changelog
* Fri Sep 03 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-1
- Initial spec