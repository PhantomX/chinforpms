%undefine _cmake_shared_libs

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 98903f80764c3be5c01ab149b50d1eb55fec4bfd
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220727
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname melonDS
%global vc_url  https://github.com/Arisotura/%{pkgname}

%global fatfs_ver 86631

Name:           melonds
Version:        0.9.4
Release:        8%{?gver}%{?dist}
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
Patch10:        %{vc_url}/pull/1402.patch#/%{name}-gh-pr1402.patch

ExclusiveArch:  x86_64 %{ix86} %{arm} aarch64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6OpenGLWidgets)
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

Provides:       bundled(fatfs) = %{fatfs_ver}
Provides:       bundled(sha1-reid)
Provides:       bundled(teakra) = 0~git
Provides:       bundled(tiny-AES-c)


%description
%{pkgname} is a Nintendo DS emulator.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

cp -p src/fatfs/LICENSE.txt LICENSE.fatfs
cp -p src/teakra/LICENSE LICENSE.teakra
cp -p src/tiny-AES-c/unlicense.txt LICENSE.tiny-AES-c

rm -rf \
  src/frontend/qt_sdl/pcap src/xxhash

sed \
  -e 's|STREQUAL Release|STREQUAL Release_disabled|g' \
  -e '/ -s"/d' \
  -i CMakeLists.txt

sed \
  -e '/-Wfatal-errors$/d' \
  -e '/-pedantic-errors$/d' \
  -i src/teakra/CMakeLists.txt


%build
%set_build_flags
export LDFLAGS+=" -Wl,-z,noexecstack"
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DENABLE_LTO:BOOL=OFF \
  -DTEAKRA_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DUSE_QT6:BOOL=ON \
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
* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-8.20220727git98903f8
- Last snapshot
- Qt6

* Sat Jul 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-7.20220707gitf5c1094
- Update

* Fri May 27 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-6.20220523gitf85925f
- Bump

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-5.20220513git4cc3412
- Update

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-4.20220420gited2121d
- Bump

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-3.20220327git02b859a
- Bump

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-2.20220314git709a598
- Return to snapshot

* Wed Mar 09 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-1.20220308git20c39eb
- 0.9.4

* Mon Feb 28 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-8.20220228git2c21787
- Update

* Sat Jan 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-7.20220128git0761fe7
- Bump

* Sun Jan 09 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-6.20220109gitdff8980
- Last snapshot
- File location patch removed, upstream support custom paths now

* Wed Nov 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-5.20211123gitc04e437
- Update

* Sat Nov 06 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-4.20211103git139c009
- Bump

* Mon Oct 11 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-3.20211010gita8613af
- Update

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-2.20211002gitb7992cc
- Snapshot

* Fri Sep 03 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-1
- Initial spec
