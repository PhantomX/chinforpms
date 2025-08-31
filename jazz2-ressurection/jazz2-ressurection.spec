%global commit 4540b7790bf7b3bf6814d4d480a83179248b9ff6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250823
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global binname jazz2
%global pkgname jazz2-native
%global vc_url https://github.com/deathkiller/jazz2-native

Name:           jazz2-ressurection
Version:        3.4.0
Release:        1%{?dist}
Summary:        Native C++ reimplementation of Jazz Jackrabbit 2 

License:        GPL-3.0 AND Apache-2.0
URL:            https://deat.tk/jazz2/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch10:        0001-JoyMappingDb-add-some-controllers.patch
Patch11:        0001-Use-NCINE_LINUX_PACKAGE-for-config-path.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  cmake(glfw3)
BuildRequires:  cmake(OpenAL)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libdw)
BuildRequires:  pkgconfig(libopenmpt)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme
Requires:       sdl_gamecontrollerdb


%description
Jazz² Resurrection is reimplementation of the game Jazz Jackrabbit 2 released in
1998. Supports various versions of the game.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

sed \
  -e 's|${NCINE_VERSION}|%{version}-%{release}|' \
  -i cmake/ncine_get_version.cmake

sed -e '/Ofast/d' -i cmake/ncine_compiler_options.cmake
sed -e '/Ofast/d' -i cmake/ncine_helpers.cmake

sed -e '/README_INSTALL_DESTINATION/d' -i cmake/ncine_installation.cmake


%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DNCINE_LINUX_PACKAGE="%{name}" \
  -DNCINE_VERSION:STRING="%{version}" \
  -DNCINE_LINKTIME_OPTIMIZATION:BOOL=OFF \
  -DNCINE_STRIP_BINARIES:BOOL=OFF \
  -DNCINE_DOWNLOAD_DEPENDENCIES:BOOL=OFF \
  -DNCINE_PREFERRED_BACKEND:STRING=GLFW \
  -DNCINE_VERSION_FROM_GIT:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

rm -f %{buildroot}%{_datadir}/%{name}/Content/Translations/*.po

rm -f %{buildroot}%{_datadir}/%{name}/Content/gamecontrollerdb.txt
ln -sf ../../SDL_GameControllerDB/gamecontrollerdb.txt \
  %{buildroot}%{_datadir}/%{name}/Content/gamecontrollerdb.txt


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{binname}
%{_datadir}/%{name}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{binname}.*


%changelog
* Sun Aug 31 2025 Phantom X <megaphantomx at hotmail dot com> - 3.4.0-1.20250823git4540b77
- 3.4.0

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.0-1.20250318git57b98ce
- 3.2.0

* Sat Jan 18 2025 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-1.20250118gitacfc2d5
- 3.1.0
- Use %%{name} as NCINE_LINUX_PACKAGE

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 2.8.0-1.20240912git2c41c52
- 2.8.0

* Sun Jun 02 2024 Phantom X <megaphantomx at hotmail dot com> - 2.7.0-1.20240501git2ec233f
- 2.7.0

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 2.6.0-2.20240323git5323404
- Update simdjson

* Fri Mar 22 2024 Phantom X <megaphantomx at hotmail dot com> - 2.6.0-1.20240318gitb2affe5
- 2.6.0

* Sat Jan 06 2024 Phantom X <megaphantomx at hotmail dot com> - 2.4.1-1.20240106git70c08fd
- Initial spec

