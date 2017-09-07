Name:           mangastream-downloader
Version:        1.1.2
Release:        1%{?dist}
Summary:        Downloads manga from MangaStream

License:        WTFPL
URL:            https://github.com/RikudouSage/%{name}
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-pt_BR.ts
Source2:        http://www.wtfpl.net/txt/copying#/LICENSE

BuildRequires:  icoutils
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
Requires:       hicolor-icon-theme

%description
MangaStream Downloader is a simple app written in Qt, it allows you to download
manga from MangaStream.

%prep
%autosetup

cp -p %{SOURCE1} translations/pt_BR.ts
cp -p %{SOURCE2} .

icotool -x -b 32 appicon.ico

sed \
  -e '/system/s|lupdate |lupdate-qt5 |g' \
  -e '/system/s|lrelease |lrelease-qt5 |g' \
  -e '/translations\/cs_CZ.ts/aTRANSLATIONS += translations/pt_BR.ts' \
  -i %{name}.pro

sed \
  -e '/translations\/cs_CZ.qm/a\        <file>translations/pt_BR.qm</file>' \
  -i translations.qrc

%build
%qmake_qt5 %{name}.pro
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=MangaStream Downloader
Comment=Downloads manga from MangaStream
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Qt;Network;
EOF

for res in 16 24 32 48 64 72 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 appicon_*_${res}x${res}x32.png ${dir}/%{name}.png
done

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Thu Sep  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.2-1
- Initial spec
