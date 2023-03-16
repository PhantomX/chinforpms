%global smoothver 0.9.9

%global appname org.%{name}.%{name}

%global ver     %%(echo %{version} | tr '~' '-' | tr '_' '-')

Name:           freac
Version:        1.1.6
Release:        1%{?dist}
Summary:        A free audio converter and CD ripper

License:        GPL-2.0-only
URL:            http://www.freac.org/

Source0:        https://downloads.sourceforge.net/bonkenc/%{name}-%{ver}.tar.gz

Patch0:         0001-appdata-fix-ampersand-character.patch

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  boca-devel
BuildRequires:  smooth-devel >= %{smoothver}
BuildRequires:  pkgconfig(libudev)
BuildRequires:  libappstream-glib
Requires:       hicolor-icon-theme
Requires:       flac
Requires:       lame
Requires:       libsamplerate
Requires:       opus-tools
Requires:       shntool
Requires:       speex
Requires:       timidity++
Requires:       twolame
Requires:       vorbis-tools
Requires:       wavpack
Requires:       xmp
#Suggests:       aften
Suggests:       ffmpeg


%description
fre:ac is a free audio converter and CD ripper with support for various
popular formats and encoders. It currently converts between MP3, MP4/M4A,
WMA, Ogg Vorbis, FLAC, AAC, WAV and Bonk formats.


%prep
%autosetup -n %{name}-%{ver} -p1

sed -e 's/\r//' -i COPYING Readme

sed \
  -e 's|-L$(prefix)/lib\b||g' \
  -e 's|-L/usr/X11R6/lib -L/usr/local/lib||g' \
  -i Makefile

sed -e 's|/lib/|/%{_lib}/|g' -i src/loader/console.cpp src/loader/gui.cpp

%build
%set_build_flags

%make_build prefix=/usr libdir=%{_libdir}


%install

%make_install prefix=/usr libdir=%{_libdir}

chmod +x %{buildroot}%{_libdir}/%{name}/*.so*

mv %{buildroot}%{_datadir}/doc _docs

desktop-file-edit \
  --set-key="Exec" \
  --set-value="%{name} --scale:1.2" \
%{buildroot}%{_datadir}/applications/%{appname}.desktop


desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml


%files
%license COPYING
%doc _docs/*
%{_bindir}/%{name}*
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/*.xml


%changelog
* Thu Mar 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.6-1
- 1.1.6

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.1.5-1
- 1.1.5

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.1.4-1
- 1.1.4

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1.3-1
- 1.1.3

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1.2-1
- 1.1.2

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1.1-1
- 1.1.1

* Tue Mar 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1-1
- 1.1

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1~rc1-1
- 1.1-rc1

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1~beta3-1
- 1.1-beta3

* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1~beta1-1
- 1.1-beta1

* Tue Apr 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1~alpha_20190423-1
- 1.1-alpha-20190423

* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1~alpha_20181201a-1
- 1.1-alpha-20181201a

* Sun Sep 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.4.alpha.20180913
- 1.1-20180913

* Fri Jul 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.3.alpha.20180710
- 1.1-20180710

* Wed May 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.2.alpha.20180306
- Fix dangling icon link

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.1.alpha.20180306
- Initial spec
