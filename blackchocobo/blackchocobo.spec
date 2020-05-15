%global commit 812edfde25d75c70ffb25827ecaac14ac7ae8c59
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200510
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/sithlord48/%{name}

Name:           blackchocobo
Version:        1.10.0
Release:        1%{?gver}%{?dist}
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


%build
mkdir %{_target_platform}
pushd %{_target_platform}

%cmake .. \
  -DQt5_LRELEASE_EXECUTABLE=lrelease-qt5 \
%{nil}

%make_build

popd


%install
%make_install -C %{_target_platform}

rm -rf %{buildroot}%{_datadir}/menu

desktop-file-edit \
  --remove-category="Application" \
  --remove-key="Encoding" \
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

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 %{name}.appdata.xml %{buildroot}%{_metainfodir}/

appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license COPYING.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_metainfodir}/*.appdata.xml
%{_datadir}/mime/packages/*.xml
%{_datadir}/pixmaps/*.png


%changelog
* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.10.0-1.20200510git812edfd
- Initial spec
