%global commit 1fb7dff45e177ed115aceb85c20df580d38cceca
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240426
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

# Update simdjson
%bcond_without simdjson

%global simdjson_ver 3.9.2

%global binname jazz2
%global pkgname jazz2-native
%global vc_url https://github.com/deathkiller/jazz2-native

Name:           jazz2-ressurection
Version:        2.6.0
Release:        3%{?dist}
Summary:        Native C++ reimplementation of Jazz Jackrabbit 2 

License:        GPL-3.0 AND Apache-2.0
URL:            https://deat.tk/jazz2/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif
%if %{with simdjson}
Source10:       https://github.com/simdjson/simdjson/releases/download/v%{simdjson_ver}/simdjson.cpp#/simdjson-%{simdjson_ver}.cpp
Source11:       https://github.com/simdjson/simdjson/releases/download/v%{simdjson_ver}/simdjson.h#/simdjson-%{simdjson_ver}.h
%endif

Patch10:        0001-JoyMappingDb-add-some-controllers.patch

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  cmake(glfw3)
BuildRequires:  cmake(OpenAL)
BuildRequires:  cmake(simdjson)
BuildRequires:  pkgconfig(libopenmpt)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme

Provides:       bundle(simdjson) = %{simdjson_ver}


%description
Jazz² Resurrection is reimplementation of the game Jazz Jackrabbit 2 released in
1998. Supports various versions of the game.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

%if %{with simdjson}
cp -f %{S:10} Sources/simdjson/simdjson.cpp
cp -f %{S:11} Sources/simdjson/simdjson.h
%endif

sed \
  -e 's|${NCINE_VERSION}|%{version}-%{release}|' \
  -i cmake/ncine_get_version.cmake

sed -e '/Ofast/d' -i cmake/ncine_compiler_options.cmake
sed -e '/Ofast/d' -i cmake/ncine_helpers.cmake

sed -e '/README_INSTALL_DESTINATION/d' -i cmake/ncine_installation.cmake


%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
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


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{binname}
"%{_datadir}/Jazz² Resurrection"
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{binname}.*


%changelog
* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 2.6.0-2.20240323git5323404
- Update simdjson

* Fri Mar 22 2024 Phantom X <megaphantomx at hotmail dot com> - 2.6.0-1.20240318gitb2affe5
- 2.6.0

* Sat Jan 06 2024 Phantom X <megaphantomx at hotmail dot com> - 2.4.1-1.20240106git70c08fd
- Initial spec

