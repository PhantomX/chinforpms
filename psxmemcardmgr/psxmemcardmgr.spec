%global commit 9c2868c0dcd18e28b3c2ecc64195218e61b90986
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210714
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global binname psxcardmgr
%global vc_url  https://github.com/raphnet/%{name}

Name:           psxmemcardmgr
Version:        0.9.1
Release:        1%{?dist}
Summary:        PSX Memory Card Manager

License:        GPL-2.0-only
URL:            https://www.raphnet.net/programmation/psxmemcardmgr/index_en.php

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  gcc-g++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
Requires:       gnome-icon-theme


%description
PSX Memory Card Manager is a very simple Playstation memory card image
manipulation tool with a GUI. Combined with the right hardware, transfering
data to and from a real memory card is also possible.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

cat > %{binname}.desktop <<EOF
[Desktop Entry]
Name=PSX Memory Card Manager
Exec=%{binname}
Terminal=false
Icon=applications-games
Type=Application
Categories=Qt;Game;
EOF


%build
%{qmake_qt5}
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{binname} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{binname}.desktop


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop


%changelog
* Mon Sep 27 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.1-1.20210714git9c2868c
- Initial spec
