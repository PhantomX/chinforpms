Name:           mednaffe
Version:        0.8.8
Release:        1%{?dist}
Summary:        A front-end (GUI) for mednafen emulator

License:        GPLv3
URL:            https://github.com/AmatCoder/%{name}
Source0:        https://github.com/AmatCoder/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.4
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gthread-2.0)
Requires:       mednafen >= 1.21.1
Requires:       hicolor-icon-theme

%description
Mednaffe is a front-end (GUI) for mednafen emulator.


%prep
%autosetup


%build
%configure \
  --disable-silent-rules \
  --enable-gtk3
%make_build


%install
%make_install

rm -rf %{buildroot}/%{_datadir}/doc

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.*
%{_datadir}/pixmaps/*.png
%{_metainfodir}/*.xml


%changelog
* Fri May 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-1
- Initial spec
