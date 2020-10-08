# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%undefine _debugsource_packages

%global pkgname SoulseekQt

Name:           soulseekqt
Version:        2018.1.30
Release:        1%{?dist}
Summary:        A desktop client for the Soulseek peer-to-peer file sharing network

License:        Proprietary
URL:            http://www.soulseekqt.net/news/

%global pkgver %(c=%{version}; echo ${c//./-})
Source0:        https://www.dropbox.com/s/0vi87eef3ooh7iy/%{pkgname}-%{pkgver}-64bit.tgz?dl=1#/%{pkgname}-%{pkgver}-64bit.tgz

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Requires:       hicolor-icon-theme

Provides:       %{pkgname} = %{version}-%{release}


%description
%{summary}.

%prep
%autosetup -c

./%{pkgname}-%{pkgver}-64bit.AppImage --appimage-extract

chrpath --delete squashfs-root/%{pkgname}

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 squashfs-root/%{pkgname} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=%{pkgname}
Comment=Soulseek music-sharing client
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;Network;FileTransfer;P2P;
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -pm0644 squashfs-root/soulseek.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

for res in 16 22 24 32 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert squashfs-root/soulseek.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Sun Jul 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 2018.1.30-1
- First spec
