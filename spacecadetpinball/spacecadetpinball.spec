%global commit cb9b7b886244a27773f66b0b19fdc2998392565e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240228
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

# Update SDL_GameControllerDB
%bcond gcdb 1

%global imgui_id 5a0ac1678c298dbff0d4aad7e82fb82ba989b20b

%global pkgname SpaceCadetPinball

Name:           spacecadetpinball
Version:        2.1.0
Release:        1%{?dist}
Summary:        3D Pinball for Windows - Space Cadet

License:        MIT
URL:            https://github.com/k4zmu2a/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif
%if %{with gcdb}
Source1:        https://github.com/ocornut/imgui/raw/%{imgui_id}/misc/fonts/binary_to_compressed_c.cpp
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cmake
BuildRequires:  gcc-g++
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  sdl_gamecontrollerdb
Requires:       hicolor-icon-theme

%description
%{summary}.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

%if %{with gcdb}
cp -p %{S:1} .

sed \
  -e '/const unsigned int EmbeddedData::SDL_GameControllerDB_compressed_size/,/#endif/d' \
  -i %{pkgname}/EmbeddedData.cpp
%endif

%build
%if %{with gcdb}
${CXX} ${CXXFLAGS} ${LDFLAGS} binary_to_compressed_c.cpp -o binary_to_compressed_c

./binary_to_compressed_c -u32 -nostatic \
  %{_datadir}/SDL_GameControllerDB/gamecontrollerdb.txt 'EmbeddedData::SDL_GameControllerDB' \
  > SDL_GameControllerDB.tmp

cat SDL_GameControllerDB.tmp >> %{pkgname}/EmbeddedData.cpp
echo '#endif' >> %{pkgname}/EmbeddedData.cpp

gcdb_val="$(grep SDL_GameControllerDB_compressed_data SDL_GameControllerDB.tmp | sed 's/.*\[\(.*\)\].*/\1/')"

sed -E "s/(SDL_GameControllerDB_compressed_data\[)[^]]*(\])/\1_RPM_GCDB_\2/" -i %{pkgname}/EmbeddedData.h
sed -e "s|_RPM_GCDB_|${gcdb_val}|" -i %{pkgname}/EmbeddedData.h
%endif


%cmake
%cmake_build


%install
%cmake_install


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{pkgname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{pkgname}.metainfo.xml


%files
%license LICENSE
%doc README.md
%{_bindir}/%{pkgname}
%{_datadir}/applications/%{pkgname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{pkgname}.*
%{_metainfodir}/%{pkgname}.metainfo.xml


%changelog
* Thu Sep 17 2026 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-1.20240228gitcb9b7b8
- Initial spec

