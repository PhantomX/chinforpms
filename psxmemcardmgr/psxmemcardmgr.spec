%global commit 9c2868c0dcd18e28b3c2ecc64195218e61b90986
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210714
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global binname psxcardmgr
%global vc_url  https://github.com/raphnet/%{name}

Name:           psxmemcardmgr
Version:        0.9.1
Release:        1%{?gver}%{?dist}
Summary:        PSX Memory Card Manager

License:        GPLv3
URL:            https://www.raphnet.net/programmation/psxmemcardmgr/index_en.php

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

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
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%{qmake_qt5}
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{binname} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{binname}.desktop <<EOF
[Desktop Entry]
Name=PSX Memory Card Manager
Exec=%{binname}
Terminal=false
Icon=applications-games
Type=Application
Categories=Qt;Game;
EOF


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
