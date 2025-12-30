%undefine _cmake_shared_libs
%global _lto_cflags %{nil}
%undefine _hardened_build

%global with_extra_flags -O3 -Wp,-U_GLIBCXX_ASSERTIONS
%{?with_extra_flags:%global _pkg_extra_cflags %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?with_extra_flags}}
%{!?_hardened_build:%global _pkg_extra_ldflags -Wl,-z,now}

%global commit 3a3388c4c50e8735af125c1af4d89e457f5e9035
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20251221
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname melonDS
%global appname net.kuribo64.%{pkgname}
%global vc_url  https://github.com/Arisotura/%{pkgname}

%global ver %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", ""); print(ver)}

%global fatfs_ver 86631

Name:           melonds
Version:        1.1
Release:        2%{?dist}
Summary:        A NDS emulator

# fatfs - BSD
# sha1-reid - Public Domain
# teakra - MIT
# tiny-AES - Unlicense

License:        GPL-3.0-or-later AND MIT AND LicenseRef-Fedora-Public-Domain AND Unlicense
URL:            http://melonds.kuribo64.net/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{ver}/%{pkgname}-%{ver}.tar.gz
%endif
Source1:        net.kuribo64.%{pkgname}.metainfo.xml

Patch0:         0001-Use-system-libraries.patch

ExclusiveArch:  x86_64 %{ix86} %{arm} aarch64

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6OpenGLWidgets)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  extra-cmake-modules
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(faad2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(slirp)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11)

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       hicolor-icon-theme

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(fatfs) = %{fatfs_ver}
Provides:       bundled(sha1-reid)
Provides:       bundled(teakra) = 0~git
Provides:       bundled(tiny-AES-c)


%description
%{pkgname} is a NDS emulator.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

cp -p src/fatfs/LICENSE.txt LICENSE.fatfs
cp -p src/teakra/LICENSE LICENSE.teakra
cp -p src/tiny-AES-c/unlicense.txt LICENSE.tiny-AES-c

rm -rf \
  src/frontend/libslirp src/frontend/qt_sdl/pcap src/xxhash

sed -e '/include/s|xxhash/||g' -i src/NDSCart.cpp

sed \
  -e 's|STREQUAL Release|STREQUAL Release_disabled|g' \
  -e '/ -s"/d' \
  -i CMakeLists.txt

sed \
  -e '/-Wfatal-errors$/d' \
  -e '/-pedantic-errors$/d' \
  -i src/teakra/CMakeLists.txt


%build
export LDFLAGS+=" -Wl,-z,noexecstack"
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DMELONDS_VERSION_SUFFIX:STRING="-%{release}" \
  -DENABLE_LTO:BOOL=OFF \
  -DENABLE_LTO_RELEASE:BOOL=OFF \
  -DTEAKRA_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DUSE_SYSTEM_LIBSLIRP:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/*.metainfo.xml


%files
%doc README.md
%license LICENSE*
%{_bindir}/%{pkgname}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Tue Nov 18 2025 Phantom X <megaphantomx at hotmail dot com> - 1.1-1.20251117gitf82a7e4
- 1.1

* Tue Jul 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0-1.20250713git13a9825
- 1.0

* Thu Nov 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0~rc-1
- 1.0rc

* Sat Jan 20 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9.5-12.20240117git7897bd3
- Reenable Qt 6

* Tue Oct 24 2023 Phantom X <megaphantomx at hotmail dot com> - 0.9.5-9.20231022git3ab752b
- Build with Qt 5 until 6 is fixed

* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.5-1.20221111git5488e0b
- 0.9.5

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
