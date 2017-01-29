%global debug_package %{nil}
%global __strip /bin/true

%global binname Telegram
%global gitlink https://github.com/telegramdesktop/tdesktop/raw/master

%ifarch %{ix86}
%global parch 32
%endif

Name:           telegram
Version:        1.0.2
Release:        2%{?dist}
Summary:        A messenger application

License:        GPLv3
URL:            https://telegram.org/
Source0:        https://updates.tdesktop.com/tlinux%{?parch}/tsetup%{?parch}.%{version}.tar.xz
Source1:        %{gitlink}/LICENSE
Source2:        %{gitlink}/%{binname}/Resources/art/icon32.png
Source3:        %{gitlink}/%{binname}/Resources/art/icon48.png
Source4:        %{gitlink}/%{binname}/Resources/art/icon64.png
Source5:        %{gitlink}/%{binname}/Resources/art/icon256.png
Source6:        %{gitlink}/%{binname}/Resources/art/icon512.png

BuildRequires:  chrpath
BuildRequires:  ImageMagick
Requires:       dbus

%description
Telegram is a messaging app with a focus on speed and security, it’s super-fast,
simple and free. You can use Telegram on all your devices at the same time — your
messages sync seamlessly across any number of your phones, tablets or computers.

%prep
%autosetup -n %{binname}

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} .

chrpath --delete %{binname}

%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{binname} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/telegramdesktop.desktop <<EOF
[Desktop Entry]
Name=%{binname} Desktop
Comment=Official desktop version of %{binname} messaging app
Exec=%{binname}
Icon=%{name}
Terminal=false
StartupWMClass=%{binname}
Type=Application
Categories=Qt;Network;
MimeType=x-scheme-handler/tg;
EOF

for res in 32 48 64 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 icon${res}.png ${dir}/%{name}.png
done

for res in 16 22 24 48 42 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert icon512.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%{_bindir}/Telegram
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png

%changelog
* Fri Jan 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-2
- Fix desktop file

* Thu Jan 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-1
- new version

* Thu Jan 12 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.0-1
- new version

* Thu Jan 12 2017 Phantom X <megaphantomx at bol dot com dot br>
- new version

* Mon Jan  9 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.10.20-1
- Initial spec.