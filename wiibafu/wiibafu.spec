%global commit bdf226c4d35aead55acceeb99b91b83566867490
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20130713
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global binname WiiBaFu

Name:           wiibafu
Version:        2.0
Release:        0.1%{?gver}%{?dist}
Summary:        Wii Backup Fusion

License:        GPLv3
URL:            https://wiibafu.sourceforge.io/
Source0:        https://sourceforge.net/code-snapshots/git/w/wi/%{name}/code.git/%{name}-code-%{commit}.zip#/%{name}-code-%{shortcommit}.zip
Source1:        %{binname}.appdata.xml

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
Requires:       hicolor-icon-theme
Requires:       wiimms-iso-tools


%description
%{name} is the complete and simple to use backup solution for your Wii
games.


%prep
%autosetup -n %{name}-code-%{commit} -p1


%build
%{qmake_qt5}
%make_build


%install
make install INSTALL_ROOT=%{buildroot}

desktop-file-edit \
  --remove-category=Network \
  --add-category=Utility \
  %{buildroot}/%{_datadir}/applications/%{binname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
ln -sf ../../../../pixmaps/%{binname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{binname}.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert resources/images/%{binname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{binname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} \
  %{buildroot}%{_metainfodir}/%{binname}.appdata.xml


%files
%license COPYING
%doc AUTHORS README
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/pixmaps/%{binname}.png
%{_datadir}/icons/hicolor/*/apps/%{binname}.png
%{_metainfodir}/*.xml


%changelog
* Thu Feb 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.1.20130713gitbdf226c
- Initial spec
