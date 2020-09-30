%global commit c47ec67716f70b3e1ea8dfcca8c3192c78195b20
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200827
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/sithlord48/%{name}

Name:           blackchocobo
Version:        1.10.3
Release:        2%{?gver}%{?dist}
Summary:        Final Fantasy 7 Save Editor

License:        GPLv3
URL:            http://www.blackchocobo.com/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Quick)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Xml)
BuildRequires:  ImageMagick
Requires:       hicolor-icon-theme


%description
Black Chocobo is a FF7 save game editor. Black Chocobo can open and write both
PC and PSX save game formats as well as saves for most emulators. Also Supports
Converting Save Formats to PC or PSX. With it you can even export your ps3 saves.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

sed \
  -e 's|share/metadata/|share/metainfo/|' \
  -e '/licenses\/blackchocobo\//d' \
  -i CMakeLists.txt


%build
%cmake \
  -B %{__cmake_builddir} \
  -DQt5_LRELEASE_EXECUTABLE=lrelease-qt5 \
%{nil}

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_datadir}/menu

desktop-file-edit \
  --set-key=Exec \
  --set-value="%{name}" \
  %{buildroot}%{_datadir}/applications/Black_Chocobo.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
ln -s ../../../../pixmaps/Black_Chocobo.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/Black_Chocobo.png

for res in 16 24 32 48 64 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert icon/Black_Chocobo.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/Black_Chocobo.png
done

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/Black_Chocobo.appdata.xml

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
* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.3-2.20200827gitc47ec67
- Bump

* Mon Jul 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.3-1.20200712git1822ab9
- 1.10.3

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.10.0-2.20200527git16ba295
- New snapshot

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.10.0-1.20200510git812edfd
- Initial spec
