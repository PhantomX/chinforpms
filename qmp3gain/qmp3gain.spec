Name:           qmp3gain
Version:        0.9.0
Release:        2%{?dist}
Summary:        MP3Gain GUI front end

License:        GPLv2
URL:            http://sourceforge.net/projects/qmp3gain/
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(QtGui)
BuildRequires:  pkgconfig(QtWebKit)
BuildRequires:  pkgconfig(phonon)
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       mp3gain
Requires(post): desktop-file-utils
Requires(postun): gtk-update-icon-cache
Requires(posttrans): gtk-update-icon-cache

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
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/%{name}


%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-2
- BR: desktop-file-utils

* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-1
- Initial spec.
