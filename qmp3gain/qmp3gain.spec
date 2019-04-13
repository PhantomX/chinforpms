Name:           qmp3gain
Version:        0.9.0
Release:        2%{?dist}
Summary:        MP3Gain GUI front end

License:        GPLv2
URL:            http://sourceforge.net/projects/qmp3gain/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(QtGui)
BuildRequires:  pkgconfig(QtWebKit)
BuildRequires:  pkgconfig(phonon)
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       mp3gain

%description
Graphical user interface front end supporting MP3Gain engine which analyzes and
losslessly adjusts mp3 files to a specified target volume.

%prep
%autosetup -c


%build
%qmake_qt4 %{name}.pro
%make_build


%install
make install INSTALL_ROOT=%{buildroot}

desktop-file-edit \
  --remove-category="Application" \
  --add-mime-type="audio/mpeg" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/%{name}/


%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-2
- BR: desktop-file-utils

* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-1
- Initial spec.
