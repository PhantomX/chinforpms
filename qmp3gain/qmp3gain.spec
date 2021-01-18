%global commit 05fa4cfeb9954f8ca4b6782fe1600097e937ad63
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180213
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           qmp3gain
Version:        0.9.0
Release:        3%{?gver}%{?dist}
Summary:        MP3Gain GUI front end

License:        GPLv2
URL:            http://sourceforge.net/projects/qmp3gain/
%if 0%{?with_snapshot}
Source0:        https://github.com/luigino/%{name}-qt5/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  make
BuildRequires:  gcc-c++
%if 0%{?with_snapshot}
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5WebKit)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(phonon4qt5)
BuildRequires:  qt5-linguist
%else
BuildRequires:  pkgconfig(QtGui)
BuildRequires:  pkgconfig(QtWebKit)
BuildRequires:  pkgconfig(phonon)
%endif
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       mp3gain


%description
Graphical user interface front end supporting MP3Gain engine which analyzes and
losslessly adjusts mp3 files to a specified target volume.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-qt5-%{commit} -p1
%else
%autosetup -c
%endif


%build
%if 0%{?with_snapshot}
%qmake_qt5 %{name}.pro
%else
%qmake_qt4 %{name}.pro
%endif

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

desktop-file-edit \
  --remove-category="Application" \
  --add-mime-type="audio/mpeg" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name} --with-qt


%files -f %{name}.lang
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/help/
%{_datadir}/%{name}/resources/


%changelog
* Tue Apr 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-3.20180213git05fa4cf
- Change to Luigi Baldoni Qt5 port snapshot

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-2
- BR: desktop-file-utils

* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-1
- Initial spec.
