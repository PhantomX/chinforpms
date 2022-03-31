%global commit 7a63073e0beb9b8c83f75a64345255e9d120bed6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220324
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Enable system qhexedit
%global with_qhexedit 0

%global ff7tk_ver 0.82

%global vc_url  https://github.com/sithlord48/%{name}

Name:           blackchocobo
Version:        1.80.0
Release:        1%{?gver}%{?dist}
Summary:        Final Fantasy 7 Save Editor

License:        GPLv3
URL:            http://www.blackchocobo.com/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Use-system-qhexedit.patch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  cmake(ff7tk) >= %{ff7tk_ver}
BuildRequires:  cmake(ff7tkWidgets) >= %{ff7tk_ver}
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Linguist)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  qt6-linguist
BuildRequires:  pkgconfig(xkbcommon)
%if 0%{?with_qhexedit}
BuildRequires:  pkgconfig(qhexedit2-qt6)
%else
Provides:       bundled(qhexedit2) = 0.8.6
%endif
BuildRequires:  ImageMagick
Requires:       hicolor-icon-theme


%description
Black Chocobo is a FF7 save game editor. Black Chocobo can open and write both
PC and PSX save game formats as well as saves for most emulators. Also Supports
Converting Save Formats to PC or PSX. With it you can even export your ps3 saves.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

rm -rf .git

%if 0%{?with_qhexedit}
  rm -rf qhexedit
%endif

sed \
  -e '/licenses\/blackchocobo\//d' \
  -i src/CMakeLists.txt

%if 0%{?with_snapshot}
  sed \
    -e 's|${CMAKE_PROJECT_VERSION_TWEAK}|%{shortcommit}|g' \
    -i CMakeLists.txt
%endif


%build
%cmake \
  -DQt6_LRELEASE_EXECUTABLE=lrelease-qt6 \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%if 0%{?with_qhexedit}
  -DUSE_SYSTEM_QHEXEDIT:BOOL=ON \
%endif
%{nil}

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_datadir}/menu

desktop-file-edit \
  --set-key=Exec \
  --set-value="%{name}" \
  %{buildroot}%{_datadir}/applications/org.sithlord48.%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
ln -s ../../../../pixmaps/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

for res in 16 24 32 48 64 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert deploy/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang bchoco --with-qt


%files -f bchoco.lang
%license COPYING.txt
%doc README.md
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_metainfodir}/*.appdata.xml
%{_datadir}/mime/packages/*.xml
%{_datadir}/pixmaps/*.png


%changelog
* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1.80.0-1.20220324git7a63073
- 1.80.0
- Qt6

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.10.5-2.20210415gitafa6866
- Bump

* Sat Dec 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.5-1.20201225gita77d0bf
- 1.10.5
- BR: ff7tk
- qhexedit switch

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.4-1.20201129git38011e1
- 1.10.4

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.3-2.20200827gitc47ec67
- Bump

* Mon Jul 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.3-1.20200712git1822ab9
- 1.10.3

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.0-2.20200527git16ba295
- New snapshot

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.10.0-1.20200510git812edfd
- Initial spec
